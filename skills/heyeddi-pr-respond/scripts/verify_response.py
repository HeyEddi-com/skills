#!/usr/bin/env python3
"""Verify PR review response workflow: tracking complete and optional gate."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _skill_cli import emit, resolve_project_root

TRACKING_NAME = "pr-{pr}-tracking.md"
REPLIES_NAME = "pr-{pr}-replies.md"
REQUIRED_TRACKING_COLS = ("Comment ID", "Action", "Status")
RESPONDED_MARKERS = ("RESPONDED", "responded", "replied", "drafted")


def docs_dir(root: Path) -> Path:
    return root / ".heyeddi" / "docs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify PR review response completeness")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--fixture", default=None, help="Fixture comments JSON to count expected replies")
    parser.add_argument("--require-gate", action="store_true", help="Fail if pre-merge gate report shows BLOCKED")
    parser.add_argument("--check", action="store_true", help="Exit 1 when incomplete")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    missing: list[str] = []
    tracking_path = docs_dir(root) / TRACKING_NAME.format(pr=args.pr)
    replies_path = docs_dir(root) / REPLIES_NAME.format(pr=args.pr)

    if not tracking_path.is_file():
        missing.append(f"missing tracking: {tracking_path.relative_to(root)}")
    else:
        tracking_text = tracking_path.read_text(encoding="utf-8")
        for col in REQUIRED_TRACKING_COLS:
            if col not in tracking_text:
                missing.append(f"tracking missing column: {col}")
        rows = [line for line in tracking_text.splitlines() if line.startswith("|") and "---" not in line]
        data_rows = [r for r in rows if "Comment ID" not in r]
        if not data_rows:
            missing.append("tracking table has no comment rows")
        for row in data_rows:
            if not any(marker in row for marker in RESPONDED_MARKERS):
                missing.append(f"unresponded row: {row[:80]}")

    expected_comments = 0
    if args.fixture:
        fixture_path = Path(args.fixture)
        if not fixture_path.is_absolute():
            fixture_path = root / fixture_path
        if fixture_path.is_file():
            data = json.loads(fixture_path.read_text(encoding="utf-8"))
            inline = data.get("inline") or []
            discussion = (data.get("discussion") or {}).get("comments") or []
            reviews = [r for r in (data.get("reviews") or []) if (r.get("body") or "").strip()]
            expected_comments = len(inline) + len(discussion) + len(reviews)

    if expected_comments and tracking_path.is_file():
        id_hits = len(re.findall(r"\b\d{6,}\b", tracking_path.read_text(encoding="utf-8")))
        if id_hits < expected_comments:
            missing.append(f"tracking may miss comments (expected ~{expected_comments} IDs)")

    if not replies_path.is_file():
        missing.append(f"missing replies draft: {replies_path.relative_to(root)}")
    elif "summary" not in replies_path.read_text(encoding="utf-8").lower():
        missing.append("replies file missing summary section")

    if args.require_gate:
        gate_candidates = list(docs_dir(root).glob("ship-report.md")) + list(docs_dir(root).glob("*gate*"))
        gate_text = ""
        for path in gate_candidates:
            if path.is_file():
                gate_text += path.read_text(encoding="utf-8", errors="replace")
        if "BLOCKED" in gate_text:
            missing.append("pre-merge gate reports BLOCKED")

    status = "ok" if not missing else "fail"
    payload = {
        "pr": args.pr,
        "status": status,
        "tracking": str(tracking_path.relative_to(root)) if tracking_path.is_file() else None,
        "replies": str(replies_path.relative_to(root)) if replies_path.is_file() else None,
        "missing": missing,
    }
    emit(json.dumps(payload, indent=2))
    if args.check and missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
