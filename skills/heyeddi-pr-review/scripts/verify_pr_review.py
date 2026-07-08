#!/usr/bin/env python3
"""Verify PR submission review report completeness."""
from __future__ import annotations

import argparse
import json
import re
import sys

from _heyeddi_paths import pr_review_path
from _skill_cli import emit, resolve_project_root

REQUIRED_SECTIONS = [
    "## Summary",
    "## Product fit",
    "## Docs drift",
    "## Engineering",
    "## Tests",
    "## Gate results",
    "## Verdict",
]

VERDICT_PATTERN = re.compile(
    r"\*\*Decision:\*\*\s*(Approve|Request changes|Block)",
    re.IGNORECASE,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify PR submission review report")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true", help="Exit 1 when incomplete")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    path = pr_review_path(root, args.pr)
    missing: list[str] = []
    if not path.is_file():
        missing.append("report file missing")
        payload = {"pr": args.pr, "status": "fail", "missing": missing}
        emit(json.dumps(payload, indent=2))
        if args.check:
            sys.exit(1)
        return

    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            missing.append(f"missing section: {section}")

    if not VERDICT_PATTERN.search(text):
        missing.append("verdict not set (Approve | Request changes | Block)")

    placeholders = [
        "_fill after reading diff",
        "_Delegate `@heyeddi-product`",
        "_Run `check_doc_drift`",
        "_Run `audit_pr_changes`",
        "_Run `@pre-merge-gate`",
        "_one paragraph citing",
    ]
    stale = [p for p in placeholders if p in text]
    if stale:
        missing.append(f"unfinished placeholders: {len(stale)}")

    status = "ok" if not missing else "fail"
    payload = {
        "pr": args.pr,
        "status": status,
        "report": str(path.relative_to(root)),
        "missing": missing,
    }
    emit(json.dumps(payload, indent=2))
    if args.check and missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
