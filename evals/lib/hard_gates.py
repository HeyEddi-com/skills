"""Deterministic eval gates — fail before the agentic judge when objective checks fail."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from evals.lib.visual_capture import VisualCaptureResult

CIRCULAR_ALIAS = re.compile(
    r"^\s*(--[\w-]+)\s*:\s*var\(\s*(--[\w-]+)\s*\)\s*;",
    re.MULTILINE,
)


def verify_tokens_file(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "error": "tokens.css missing"}
    circular: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for match in CIRCULAR_ALIAS.finditer(text):
        lhs, rhs = match.group(1), match.group(2)
        if lhs == rhs:
            circular.append(lhs)
    return {"ok": not circular, "circular_aliases": circular}


@dataclass
class HardGateResult:
    ok: bool
    issues: list[str] = field(default_factory=list)

    def format_for_judge(self) -> str:
        if self.ok:
            return "## Hard gates\n\nAll deterministic checks passed.\n"
        lines = ["## Hard gates (AUTO-FAIL)", ""]
        for issue in self.issues:
            lines.append(f"- {issue}")
        lines.append("")
        lines.append(
            "These gates run before the agentic judge. "
            "High PNG similarity or passing npm test does not override them."
        )
        return "\n".join(lines)


def _run_script(sandbox: Path, rel_script: str, *args: str) -> tuple[int, str]:
    script = sandbox / rel_script
    if not script.is_file():
        return 127, f"script missing: {rel_script}"
    proc = subprocess.run(
        ["python3", str(script), *args],
        cwd=sandbox,
        capture_output=True,
        text=True,
        timeout=120,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, combined.strip()


def run_design_handoff_hard_gates(
    sandbox: Path,
    *,
    route: str,
    command_results: list[dict],
    visual_result: VisualCaptureResult | None,
    mode: str = "handoff",
) -> HardGateResult:
    """Deterministic gates before agentic judge.

    mode:
      - ``handoff`` — full design-handoff checks (verify_handoff, content gates)
      - ``visual`` — captures + tokens only (integration UI turns)
    """
    issues: list[str] = []

    for row in command_results:
        if row.get("exit_code", 0) != 0:
            issues.append(f"verify command failed (exit {row['exit_code']}): {row.get('command')}")

    token_result = verify_tokens_file(sandbox / "src/styles/tokens.css")
    if not token_result.get("ok"):
        if token_result.get("error"):
            issues.append(f"tokens.css: {token_result['error']}")
        else:
            aliases = ", ".join(token_result.get("circular_aliases") or [])
            issues.append(
                f"tokens.css has circular aliases ({aliases}) — spacing vars resolve to 0 in the browser"
            )

    if mode == "handoff":
        code, out = _run_script(
            sandbox,
            ".agents/skills/design-handoff/scripts/verify_handoff.py",
            "--route",
            route,
            "--check",
        )
        if code != 0:
            issues.append(f"verify_handoff failed: {out[:500]}")

        code, out = _run_script(
            sandbox,
            ".agents/skills/design-handoff/scripts/verify_tokens.py",
            "--check",
        )
        if code != 0:
            issues.append(f"verify_tokens failed: {out[:400]}")

    if visual_result:
        if visual_result.skipped or not visual_result.artifacts:
            issues.append("Playwright captures missing — cannot verify rendered spacing")
        for err in visual_result.errors:
            issues.append(f"visual capture error: {err}")
        for row in visual_result.spacing_checks:
            if not row.get("ok"):
                issues.append(
                    f"rendered spacing: {row.get('name')} = {row.get('value_px')}px "
                    f"(expected {row.get('expect')})"
                )
        for row in visual_result.content_checks:
            if not row.get("ok"):
                detail = row.get("detail") or row.get("value_px")
                issues.append(
                    f"rendered content: {row.get('name')} = {detail} "
                    f"(expected {row.get('expect')})"
                )

    return HardGateResult(ok=not issues, issues=issues)


def recommendations_for_issues(issues: list[str]) -> list[str]:
    """Actionable fixes keyed to which deterministic gate failed."""
    if not issues:
        return []

    joined = " ".join(issues).lower()
    recs: list[str] = []

    if "circular alias" in joined or "tokens.css has circular" in joined:
        recs.append("Fix tokens.css circular aliases (--size-N: var(--size-N))")
    if "rendered spacing" in joined or "card body padding" in joined or "sidebar width" in joined:
        recs.append("Ensure OpenProps spacing resolves (card padding >= 16px, sidebar ~248px)")
    if "verify_handoff" in joined or "settings form" in joined or "#content" in joined:
        recs.append("Wrap PrimeVue Card body in <template #content> — see primevue-card-slots.md")
    if "dashboard stat values" in joined or "dashboard summary stats" in joined:
        recs.append(
            "Dashboard KPI wireframes need >= 3 stat cards; TaskFlow roster dashboards need "
            "a user DataTable (>= 1 row) plus optional 1–2 summary stats — see product.md"
        )
    if "dashboard user table" in joined or "datatable row" in joined:
        recs.append(
            "Team roster dashboard: show demo/offline rows via useUsers() when API is down; "
            "table must render in static preview"
        )
    if "settings notification toggle" in joined:
        recs.append("Settings: include ToggleSwitch inside Card #content with Save CTA outside cards")
    if "playwright captures missing" in joined:
        recs.append("Ensure preview build serves the route before harness capture (npm run build + preview)")

    if "verify_handoff" in joined or "handoff" in joined:
        recs.append("Re-run verify_handoff --check after implementation")

    if not recs:
        recs.append("Fix the listed hard-gate failures, then re-run the eval turn")

    # De-dupe while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in recs:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique
