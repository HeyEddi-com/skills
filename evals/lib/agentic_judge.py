"""Agentic eval judge — uses agent CLI to review changes and command output."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from evals.lib.command_capture import format_command_results, run_verify_commands
from evals.lib.hard_gates import recommendations_for_issues, run_design_handoff_hard_gates
from evals.lib.sandbox_git import diff_against_baseline, list_design_assets, read_changed_sources, stage_worktree_for_judge
from evals.lib.visual_capture import append_process_manifest, run_visual_audit
from evals.backends.results import AgentRunResult

JUDGE_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "judge-turn.md"
DEFAULT_JUDGE_TIMEOUT = 900


@dataclass
class JudgeVerdict:
    pass_: bool
    summary: str
    process_ok: bool
    outcome_ok: bool
    command_issues: list[str]
    file_findings: list[str]
    recommendations: list[str]
    raw_output: str

    @property
    def ok(self) -> bool:
        return self.pass_


def _load_judge_system() -> str:
    return JUDGE_PROMPT_PATH.read_text()


def _parse_verdict(text: str) -> JudgeVerdict:
    text = text.strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return JudgeVerdict(
            pass_=False,
            summary="Judge did not return JSON",
            process_ok=False,
            outcome_ok=False,
            command_issues=[],
            file_findings=[text[:500]],
            recommendations=[],
            raw_output=text,
        )
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return JudgeVerdict(
            pass_=False,
            summary="Judge JSON parse error",
            process_ok=False,
            outcome_ok=False,
            command_issues=[],
            file_findings=[text[:500]],
            recommendations=[],
            raw_output=text,
        )
    return JudgeVerdict(
        pass_=bool(data.get("pass")),
        summary=str(data.get("summary", "")),
        process_ok=bool(data.get("process_ok")),
        outcome_ok=bool(data.get("outcome_ok")),
        command_issues=list(data.get("command_issues") or []),
        file_findings=list(data.get("file_findings") or []),
        recommendations=list(data.get("recommendations") or []),
        raw_output=text,
    )


def build_judge_prompt(
    *,
    case_id: str,
    turn_name: str,
    skills: list[str],
    user_prompt: str,
    judge_criteria: str,
    worker_result: AgentRunResult,
    sandbox: Path,
    command_results: list[dict],
    visual_evidence: str = "",
    hard_gate_evidence: str = "",
) -> str:
    diff = diff_against_baseline(sandbox)
    files = read_changed_sources(sandbox)
    design_assets = list_design_assets(sandbox)
    commands = format_command_results(command_results)
    skill_tags = ", ".join(f"@{s}" for s in skills)

    return f"""{_load_judge_system()}

---

## Eval case: {case_id}
## Turn: {turn_name}
## Skills invoked: {skill_tags}

## User goal (worker prompt)
{user_prompt}

## Success criteria for this turn
{judge_criteria}

## Worker agent output
{worker_result.output[:8000]}

## Git diff stat
{diff['stat']}

## Git diff patch
```
{diff['patch'][:40000]}
```

## Design / handoff assets on disk (baseline + new)
{design_assets}

## Changed file contents (full sources)
{files}

## Command runs (complete output — check warnings/errors)
{commands}
{hard_gate_evidence}{visual_evidence}
"""


def _visual_audit_routes(visual_cfg: dict) -> list[str]:
    routes = visual_cfg.get("routes")
    if routes:
        return [str(r) for r in routes]
    route = visual_cfg.get("route")
    return [str(route or "/")]


def _references_for_route(visual_cfg: dict, route: str) -> list[str] | None:
    per_route = visual_cfg.get("references_by_route") or {}
    if route in per_route:
        refs = per_route[route]
        return [str(r) for r in refs] if refs else None
    if route.rstrip("/").endswith("settings") or route == "/settings":
        refs = visual_cfg.get("references")
        return [str(r) for r in refs] if refs else None
    return None


def _hard_gate_mode(visual_cfg: dict, skills: list[str]) -> str:
    explicit = visual_cfg.get("hard_gates")
    if explicit in ("handoff", "visual", "none"):
        return explicit
    if "heyeddi-handoff" in skills:
        return "handoff"
    return "visual"


def run_agentic_judge(
    *,
    backend: str,
    case_id: str,
    turn: dict,
    sandbox: Path,
    hub_root: Path,
    worker_result: AgentRunResult,
    model: str | None = None,
    timeout_s: int | None = None,
    turn_index: int = 0,
) -> JudgeVerdict:
    command_results = run_verify_commands(
        sandbox,
        turn.get("verify_commands"),
    )

    visual_evidence = ""
    hard_gate_evidence = ""
    visual_cfg = turn.get("visual_audit")
    vresults: list = []
    vresult = None
    if visual_cfg:
        step_name = str(visual_cfg.get("step") or turn.get("name") or f"turn-{turn_index}")
        routes = _visual_audit_routes(visual_cfg)
        gate_mode = _hard_gate_mode(visual_cfg, turn.get("skills") or [])
        print(
            f"  visual QA: Playwright proof for {step_name} ({', '.join(routes)})...",
            flush=True,
        )
        for route in routes:
            vresult = run_visual_audit(
                sandbox,
                route=route,
                widths=visual_cfg.get("widths"),
                references=_references_for_route(visual_cfg, route),
                min_similarity=float(visual_cfg.get("min_similarity", 0.12)),
                color_schemes=visual_cfg.get("color_schemes"),
                step_name=step_name,
            )
            vresults.append(vresult)
            visual_evidence += "\n" + vresult.format_for_judge(sandbox)

        append_process_manifest(
            sandbox,
            step_name=step_name,
            turn_index=turn_index,
            routes=routes,
            results=vresults,
        )

        failed_capture = [r for r in vresults if r.skipped or not r.artifacts]
        if failed_capture:
            errors = []
            for r in failed_capture:
                errors.extend(r.errors or ["no captures"])
            print(f"  visual QA: FAILED — {errors}", flush=True)
            return JudgeVerdict(
                pass_=False,
                summary="Playwright visual capture failed — no screenshots for agentic QA",
                process_ok=False,
                outcome_ok=False,
                command_issues=errors,
                file_findings=["Install Playwright: ./scripts/setup-evals.sh"],
                recommendations=[],
                raw_output="",
            )

        total_arts = sum(len(r.artifacts) for r in vresults)
        print(
            f"  visual QA: captured {total_arts} screenshot(s) → .heyeddi/audits/eval-process/{step_name}/",
            flush=True,
        )
        for r in vresults:
            for art in r.artifacts:
                print(f"    - {Path(art).name}", flush=True)
        for r in vresults:
            for row in r.spacing_checks:
                mark = "ok" if row.get("ok") else "FAIL"
                print(
                    f"    spacing [{mark}]: {row.get('name')} = {row.get('value_px')}px",
                    flush=True,
                )
            for row in r.content_checks:
                mark = "ok" if row.get("ok") else "FAIL"
                detail = row.get("detail") or row.get("value_px")
                print(
                    f"    content [{mark}]: {row.get('name')} = {detail}",
                    flush=True,
                )

        if gate_mode != "none":
            primary_route = routes[0]
            for r in vresults:
                if not r.ok:
                    vresult = r
                    break
            else:
                vresult = vresults[-1]
            hard = run_design_handoff_hard_gates(
                sandbox,
                route=primary_route,
                command_results=command_results,
                visual_result=vresult,
                mode="handoff" if gate_mode == "handoff" else "visual",
            )
            hard_gate_evidence = "\n" + hard.format_for_judge()
            if not hard.ok:
                print("  hard gates: FAILED (skipping agentic judge)", flush=True)
                for issue in hard.issues:
                    print(f"    - {issue}", flush=True)
                return JudgeVerdict(
                    pass_=False,
                    summary="Deterministic hard gates failed — " + (hard.issues[0] if hard.issues else "unknown"),
                    process_ok=False,
                    outcome_ok=False,
                    command_issues=hard.issues,
                    file_findings=hard.issues,
                    recommendations=recommendations_for_issues(hard.issues),
                    raw_output="",
                )
            print("  hard gates: passed", flush=True)

    criteria = turn.get("judge") or turn.get("judge_criteria") or (
        "Skill(s) should complete the user goal with proper process and working code. "
        "No command warnings or errors."
    )
    prompt = build_judge_prompt(
        case_id=case_id,
        turn_name=turn["name"],
        skills=turn["skills"],
        user_prompt=turn["prompt"],
        judge_criteria=criteria,
        worker_result=worker_result,
        sandbox=sandbox,
        command_results=command_results,
        visual_evidence=visual_evidence,
        hard_gate_evidence=hard_gate_evidence,
    )

    judge_timeout = timeout_s or int(os.environ.get("EVAL_JUDGE_TIMEOUT", DEFAULT_JUDGE_TIMEOUT))
    judge_model = (
        model
        or os.environ.get("EVAL_JUDGE_MODEL")
        or os.environ.get("EVAL_AGENT_MODEL")
    )
    # Visual QA turns need a vision-capable judge when possible
    if visual_cfg and not os.environ.get("EVAL_JUDGE_MODEL"):
        judge_model = judge_model or "composer-2.5"

    stage_worktree_for_judge(sandbox)

    if backend == "local":
        from evals.backends.local_agent import run_local_agent_eval

        result = run_local_agent_eval(
            prompt,
            sandbox,
            model=judge_model,
            timeout_s=judge_timeout,
            stream=False,
        )
    elif backend == "cursor":
        from evals.backends.cursor import run_cursor_eval

        result = run_cursor_eval(prompt, sandbox, model=judge_model or "composer-2.5")
    else:
        from evals.lib.skill_loader import build_system_prompt
        from evals.backends.pydantic_run import run_pydantic_eval

        system = build_system_prompt(hub_root, ["eval-judge"])
        result = run_pydantic_eval(system, prompt, hub_root, sandbox, [])

    return _parse_verdict(result.output)


def print_verdict(verdict: JudgeVerdict, *, quiet: bool = False) -> None:
    mark = "PASS" if verdict.ok else "FAIL"
    print(f"  judge: {mark} — {verdict.summary[:300]}", flush=True)
    if not quiet:
        if verdict.command_issues:
            print("  command issues:", flush=True)
            for issue in verdict.command_issues[:10]:
                print(f"    - {issue}", flush=True)
        if verdict.file_findings:
            print("  file findings:", flush=True)
            for finding in verdict.file_findings[:10]:
                print(f"    - {finding}", flush=True)
        if verdict.recommendations and not verdict.ok:
            print("  recommendations:", flush=True)
            for rec in verdict.recommendations[:5]:
                print(f"    - {rec}", flush=True)
