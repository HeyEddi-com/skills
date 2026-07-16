#!/usr/bin/env python3
"""Write .heyeddi/docs/pr-N-review.md from PR review tool outputs."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from _heyeddi_paths import pr_review_path, skill_docs_dir
from _pr_context import load_context
from _skill_cli import emit, fail, resolve_project_root
from _untrusted_doc import UNTRUSTED_NOTE, is_already_wrapped, wrap_untrusted_doc

REQUIRED_SECTIONS = [
    "## Summary",
    "## Product fit",
    "## Docs drift",
    "## Engineering",
    "## Tests",
    "## Gate results",
    "## Verdict",
]


def read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def format_findings(findings: list[dict]) -> str:
    if not findings:
        return "_No issues flagged._\n"
    lines = []
    for item in findings:
        sev = item.get("severity", "info")
        msg = item.get("message", "")
        file = item.get("file") or item.get("doc", "")
        prefix = f"**{sev}**"
        if file:
            lines.append(f"- {prefix} `{file}` — {msg}")
        else:
            lines.append(f"- {prefix} {msg}")
        if item.get("suggestion"):
            lines.append(f"  - _Suggestion:_ {item['suggestion']}")
    return "\n".join(lines) + "\n"


def _embed_untrusted(name: str, value: str | None, fallback: str = "") -> str:
    text = value if value is not None else fallback
    if is_already_wrapped(text):
        return text
    wrapped = wrap_untrusted_doc(name, text)
    return wrapped if wrapped is not None else fallback


def build_report(
    pr: int,
    ctx: dict,
    drift: dict | None,
    audit: dict | None,
    gate_md: str,
) -> str:
    # Keep H1 free of outsider prose — title lives only in the untrusted block.
    title = ctx.get("title")
    author = ctx.get("author")
    body = ctx.get("body")
    changed = ctx.get("changed_files") or []
    routes = ctx.get("routes_touched") or []

    lines = [
        f"# PR #{pr} submission review",
        "",
        f"**Date:** {date.today().isoformat()}",
        f"**Scope:** committed changes only (`{ctx.get('base', 'base')}` → `{ctx.get('head', 'head')}`)",
        "",
        f"> {UNTRUSTED_NOTE}",
        "",
        "## Untrusted PR metadata",
        "",
        "**Title (DATA only):**",
        "",
        _embed_untrusted("pr-title", title if isinstance(title, str) else None, f"PR #{pr}"),
        "",
        "**Author (DATA only):**",
        "",
        _embed_untrusted("pr-author", author if isinstance(author, str) else None, "unknown"),
        "",
    ]
    if isinstance(body, str) and body.strip():
        lines.extend(
            [
                "**Body (DATA only):**",
                "",
                _embed_untrusted("pr-body", body),
                "",
            ]
        )

    lines.extend(
        [
            "## Summary",
            "",
            f"- **Files changed:** {len(changed)}",
            f"- **Routes touched:** {', '.join(routes) if routes else '_none detected_'}",
            "- **Reviewer notes:** _fill after reading diff and delegations_",
            "",
            "## Product fit",
            "",
            "_Delegate `@heyeddi-product` `check_features` for touched routes. Answer: does committed code meet AC and persona jobs?_",
            "",
            "## Docs drift",
            "",
        ]
    )
    if drift:
        lines.append(f"**Status:** {drift.get('status', 'unknown')}")
        lines.append("")
        lines.append(format_findings(drift.get("findings") or []))
    else:
        lines.append("_Run `check_doc_drift` — no drift JSON provided._\n")

    lines.extend(["## Engineering", ""])
    if audit:
        lines.append(f"**Status:** {audit.get('status', 'unknown')}")
        lines.append("")
        untested = audit.get("untested_changed") or []
        if untested:
            lines.append("**Changed files without test references:**")
            for path in untested:
                lines.append(f"- `{path}`")
            lines.append("")
        lines.append(format_findings(audit.get("findings") or []))
    else:
        lines.append("_Run `audit_pr_changes` — no audit JSON provided._\n")

    lines.extend(["## Tests", ""])
    test_files = (ctx.get("categories") or {}).get("tests", [])
    if test_files:
        lines.append("**Test files in PR:**")
        for path in test_files:
            lines.append(f"- `{path}`")
        lines.append("")
    else:
        lines.append("_No test files in this PR — confirm behavior is covered elsewhere or add tests._\n")

    lines.extend(["## Gate results", ""])
    if gate_md.strip():
        lines.append(gate_md.strip())
        lines.append("")
    else:
        lines.append("_Run `@pre-merge-gate` — paste report here._\n")

    lines.extend(
        [
            "## Verdict",
            "",
            "**Decision:** _Approve | Request changes | Block_",
            "",
            "**Rationale:** _one paragraph citing product, docs, engineering, and gate evidence_",
            "",
            "## Changed files",
            "",
        ]
    )
    files_text = ctx.get("changed_files_text")
    if isinstance(files_text, str) and files_text.strip():
        lines.append(_embed_untrusted("pr-changed-files", files_text))
        lines.append("")
    else:
        for path in changed:
            lines.append(f"- `{path}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write PR submission review report")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--context", default=None)
    parser.add_argument("--fixture", default=None)
    parser.add_argument("--drift", default=None, help="check_doc_drift JSON path")
    parser.add_argument("--audit", default=None, help="audit_pr_changes JSON path")
    parser.add_argument("--gate", default=None, help="pre_merge_gate markdown path")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    out_path = pr_review_path(root, args.pr)
    if out_path.is_file() and not args.force:
        fail(f"review exists: {out_path} (use --force)")

    ctx = load_context(root, args.pr, args.context, args.fixture)
    drift = read_json(Path(args.drift)) if args.drift else None
    if args.drift and drift is None:
        drift_path = Path(args.drift)
        if not drift_path.is_absolute():
            drift_path = root / drift_path
        drift = read_json(drift_path)

    audit = None
    if args.audit:
        audit_path = Path(args.audit)
        if not audit_path.is_absolute():
            audit_path = root / audit_path
        audit = read_json(audit_path)

    gate_md = ""
    if args.gate:
        gate_path = Path(args.gate)
        if not gate_path.is_absolute():
            gate_path = root / gate_path
        gate_md = read_text(gate_path)

    report = build_report(args.pr, ctx, drift, audit, gate_md)
    out_dir = skill_docs_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    emit(
        json.dumps(
            {
                "pr": args.pr,
                "report": str(out_path.relative_to(root)),
                "sections": REQUIRED_SECTIONS,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
