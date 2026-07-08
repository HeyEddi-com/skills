#!/usr/bin/env python3
"""
Agent-based skill evals — run skills against fresh project sandboxes.

Invokes a real agent with skill instructions, then an **agentic judge** reviews
all git changes, changed file contents, and full command output (npm warnings, etc.).

Multi-step cases run up to 5 sequential @skill turns (like a real user).

Backends:
  local    — Cursor Agent CLI on this PC (`agent` binary, default)
  cursor   — Cursor SDK (optional; CURSOR_API_KEY, for CI)
  pydantic — Pydantic AI agent + skill tools (EVAL_MODEL, mirrors Cloud Run)

Usage:
  python3 scripts/run-evals.py --list
  python3 scripts/run-evals.py --dry-run
  python3 scripts/run-evals.py heyeddi-handoff-only
  python3 scripts/run-evals.py --deterministic heyeddi-handoff-only  # legacy gates
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_DIR = REPO_ROOT / "evals"
sys.path.insert(0, str(REPO_ROOT))

from evals.backends.results import AgentTransientError

from evals.lib.agentic_judge import print_verdict, run_agentic_judge
from evals.lib.assertions import run_assertions
from evals.lib.case_loader import (
    MAX_STEPS,
    case_skill_names,
    is_stepped,
    iter_turns,
    load_case,
)
from evals.lib.sandbox import create_sandbox, ensure_npm_deps
from evals.lib.sandbox_git import init_baseline
from evals.lib.skill_loader import build_system_prompt
from scripts.lib.quality_gate import warn_busy_eval_ports


def list_cases() -> list[Path]:
    return sorted(EVALS_DIR.glob("cases/*.yaml"))


def run_agent_turn(
    backend: str,
    skills: list[str],
    user_prompt: str,
    sandbox: Path,
    hub_root: Path,
    **kwargs,
) -> object:
    skill_tags = " ".join(f"@{s}" for s in skills)
    full_prompt = f"{skill_tags}\n\n{user_prompt}"

    if backend == "local":
        from evals.backends.local_agent import run_local_agent_eval

        return run_local_agent_eval(
            full_prompt,
            sandbox,
            model=kwargs.get("model"),
            timeout_s=kwargs.get("timeout"),
        )

    if backend == "cursor":
        from evals.backends.cursor import run_cursor_eval

        return run_cursor_eval(full_prompt, sandbox)

    if backend == "pydantic":
        from evals.backends.pydantic_run import run_pydantic_eval

        system = build_system_prompt(hub_root, skills)
        return run_pydantic_eval(system, full_prompt, hub_root, sandbox, skills)

    raise ValueError(f"Unknown backend: {backend}")


def run_agent_turn_with_retries(
    *,
    backend: str,
    skills: list[str],
    user_prompt: str,
    sandbox: Path,
    hub_root: Path,
    model: str | None,
    timeout: int | None,
    max_retries: int,
) -> object:
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        if attempt > 0:
            wait_s = min(120, 30 * attempt)
            print(
                f"  agent: transient API error — retry {attempt}/{max_retries} in {wait_s}s…",
                flush=True,
            )
            time.sleep(wait_s)
        try:
            return run_agent_turn(
                backend,
                skills,
                user_prompt,
                sandbox,
                hub_root,
                model=model,
                timeout=timeout,
            )
        except AgentTransientError as exc:
            last_exc = exc
            if attempt >= max_retries:
                raise
        except RuntimeError as exc:
            last_exc = exc
            from evals.backends.local_agent import is_transient_agent_error

            if attempt >= max_retries or not is_transient_agent_error(str(exc)):
                raise
    assert last_exc is not None
    raise last_exc


def resolve_work_root(args: argparse.Namespace) -> tuple[Path, object]:
    if args.output_dir:
        work = Path(args.output_dir).expanduser().resolve()
        work.mkdir(parents=True, exist_ok=True)
        return work, None

    if args.keep_sandbox:
        run_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        work = REPO_ROOT / "evals" / "runs" / run_id
        work.mkdir(parents=True, exist_ok=True)
        return work, None

    tmp = tempfile.TemporaryDirectory(prefix="heyeddi-eval-")
    return Path(tmp.name), tmp


def print_sandbox_hint(sandbox: Path, *, kept: bool) -> None:
    print(f"  sandbox: {sandbox}")
    if kept:
        print(f"  kept — inspect: cursor {sandbox}")
        print(f"  kept — preview:  cd {sandbox} && npm run dev  # http://localhost:5173")


def print_turn_header(turn_index: int, turn_total: int, turn: dict) -> None:
    skills = ", ".join(f"@{s}" for s in turn["skills"])
    print(f"\n  --- Turn {turn_index}/{turn_total}: {turn['name']} ({skills}) ---")
    preview = turn["prompt"].replace("\n", " ")[:100]
    print(f"  user: {preview}...")


def run_turn_gate(
    *,
    agentic: bool,
    backend: str,
    case_id: str,
    turn: dict,
    sandbox: Path,
    hub_root: Path,
    worker_result: object,
    model: str | None,
    judge_timeout: int | None,
    quiet: bool,
    turn_index: int = 0,
) -> bool:
    if agentic:
        print("  judge: agentic review (git diff + files + command output)...", flush=True)
        verdict = run_agentic_judge(
            backend=backend,
            case_id=case_id,
            turn=turn,
            sandbox=sandbox,
            hub_root=hub_root,
            worker_result=worker_result,
            model=model,
            timeout_s=judge_timeout,
            turn_index=turn_index,
        )
        print_verdict(verdict, quiet=quiet)
        return verdict.ok

    specs = turn.get("assertions", [])
    if not specs:
        print("  gate: (no assertions — pass)")
        return True
    print(f"  gate: deterministic {len(specs)} checks...", flush=True)
    results = run_assertions(sandbox, hub_root, specs, verbose=not quiet)
    return all(ar.ok for ar in results)


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent-based skill evals")
    parser.add_argument("case_id", nargs="?", help="Eval case id (filename stem)")
    parser.add_argument("--all", action="store_true", help="Run all cases")
    parser.add_argument("--list", action="store_true", help="List case ids")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without agent/API")
    parser.add_argument(
        "--deterministic",
        action="store_true",
        help="Use legacy file/regex assertions instead of agentic judge (default: agentic)",
    )
    parser.add_argument(
        "--backend",
        choices=["local", "cursor", "pydantic"],
        default="local",
        help="Agent runtime (default: local = `agent` CLI on this PC)",
    )
    parser.add_argument("--agent-bin", default=None, help="Path to agent binary")
    parser.add_argument("--model", default=None, help="Model for worker agent")
    parser.add_argument(
        "--judge-timeout",
        type=int,
        default=None,
        help="Judge agent timeout seconds (default: EVAL_JUDGE_TIMEOUT or 300)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Worker agent timeout per turn (default: EVAL_AGENT_TIMEOUT or 600)",
    )
    parser.add_argument(
        "--agent-retries",
        type=int,
        default=None,
        help="Retries on transient API errors (default: EVAL_AGENT_RETRIES or 2)",
    )
    parser.add_argument("--keep-sandbox", action="store_true", help="Keep sandbox under evals/runs/")
    parser.add_argument("--quiet", action="store_true", help="Hide live worker agent output")
    parser.add_argument("--output-dir", metavar="DIR", help="Custom sandbox output dir")
    args = parser.parse_args()

    agentic = not args.deterministic

    cases_paths = list_cases()
    if args.list:
        gate = "agentic" if agentic else "deterministic"
        for p in cases_paths:
            c = load_case(p, EVALS_DIR)
            turns = iter_turns(c)
            mode = f"{len(turns)} turns" if is_stepped(c) else "1 turn"
            print(f"{c['id']}\t{','.join(case_skill_names(c))}\t{c['project_template']}\t{mode}\t{gate}")
        return 0

    if args.case_id:
        cases_paths = [
            p for p in cases_paths
            if p.stem == args.case_id or load_case(p, EVALS_DIR)["id"] == args.case_id
        ]
        if not cases_paths:
            print(f"Case not found: {args.case_id}", file=sys.stderr)
            return 1
    elif not args.all:
        parser.error("Provide case_id, --all, or --list")

    if args.agent_bin:
        os.environ["AGENT_BIN"] = args.agent_bin
    if args.quiet:
        os.environ["EVAL_AGENT_QUIET"] = "1"

    if args.output_dir:
        args.keep_sandbox = True

    failed = 0
    work_root, cleanup = resolve_work_root(args)
    kept = cleanup is None

    try:
        for case_path in cases_paths:
            case = load_case(case_path, EVALS_DIR)
            eval_id = case["id"]
            turns = iter_turns(case)
            if len(turns) > MAX_STEPS:
                print(f"Case {eval_id} exceeds {MAX_STEPS} turns", file=sys.stderr)
                failed += 1
                continue

            gate_label = "agentic judge" if agentic else "deterministic"
            print(f"\n=== Eval: {eval_id} ({args.backend}, {gate_label}) ===")
            if eval_id == "full-product-integration":
                warn_busy_eval_ports()
            if is_stepped(case):
                print(f"  mode: {len(turns)} sequential @skill turns (max {MAX_STEPS})")
            else:
                print("  mode: single turn")

            if args.dry_run:
                print(f"  skills installed: {case_skill_names(case)}")
                print(f"  template: {case['project_template']}")
                for i, turn in enumerate(turns, 1):
                    skills = ", ".join(turn["skills"])
                    cmds = turn.get("verify_commands") or "(auto: npm test/build, pytest)"
                    print(f"  turn {i}: {turn['name']} [@{skills}]")
                    print(f"    verify: {cmds}")
                    if turn.get("visual_audit"):
                        va = turn["visual_audit"]
                        routes = va.get("routes") or [va.get("route", "/")]
                        print(f"    visual QA: {routes} → .heyeddi/audits/eval-process/{turn['name']}/")
                    if agentic:
                        j = (turn.get("judge") or "")[:80]
                        print(f"    judge: {j}...")
                    else:
                        print(f"    assertions: {len(turn.get('assertions', []))}")
                if kept:
                    print(f"  would keep at: {work_root / eval_id}")
                continue

            sandbox = create_sandbox(
                REPO_ROOT,
                case["project_template"],
                case_skill_names(case),
                work_root,
                eval_id,
            )
            init_baseline(sandbox)
            try:
                ensure_npm_deps(sandbox, quiet=args.quiet)
            except RuntimeError as exc:
                print(f"  SANDBOX SETUP FAILED: {exc}")
                failed += 1
                continue
            print_sandbox_hint(sandbox, kept=kept)

            case_ok = True
            agent_retries = (
                args.agent_retries
                if args.agent_retries is not None
                else int(os.environ.get("EVAL_AGENT_RETRIES", "2"))
            )
            for i, turn in enumerate(turns, 1):
                print_turn_header(i, len(turns), turn)
                try:
                    agent_result = run_agent_turn_with_retries(
                        backend=args.backend,
                        skills=turn["skills"],
                        user_prompt=turn["prompt"],
                        sandbox=sandbox,
                        hub_root=REPO_ROOT,
                        model=args.model,
                        timeout=turn.get("agent_timeout") or case.get("agent_timeout") or args.timeout,
                        max_retries=agent_retries,
                    )
                    print(f"  agent status: {agent_result.status}")
                    print(f"  agent output: {str(agent_result.output)[:200]}...")
                except Exception as exc:  # noqa: BLE001
                    print(f"  AGENT FAILED: {exc}")
                    case_ok = False
                    break

                if not run_turn_gate(
                    agentic=agentic,
                    backend=args.backend,
                    case_id=eval_id,
                    turn=turn,
                    sandbox=sandbox,
                    hub_root=REPO_ROOT,
                    worker_result=agent_result,
                    model=args.model,
                    judge_timeout=args.judge_timeout,
                    quiet=args.quiet,
                    turn_index=i,
                ):
                    print(f"  === turn {turn['name']}: FAILED ===")
                    case_ok = False
                    break
                print(f"  === turn {turn['name']}: PASSED ===")

            if not case_ok:
                failed += 1
                if kept:
                    print(f"  sandbox kept for debugging: {sandbox}")
            else:
                print(f"  === {eval_id}: PASSED ({len(turns)} turns) ===")
    finally:
        if cleanup is not None:
            cleanup.cleanup()

    if kept and not args.dry_run:
        print(f"\nSandboxes kept under: {work_root}")

    if args.dry_run:
        return 0
    print(f"\n{'=' * 60}\nEvals failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
