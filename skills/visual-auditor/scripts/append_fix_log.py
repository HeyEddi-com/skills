#!/usr/bin/env python3
"""Append a documented fix entry after correcting a visual issue."""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime

from _heyeddi_paths import visual_audit_dir
from _skill_cli import emit, resolve_project_root
from _spec_context import feature_slug


def main() -> None:
    parser = argparse.ArgumentParser(description="Log a visual fix with spec references")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--route", required=True)
    parser.add_argument("--issue", required=True, help="What was wrong visually")
    parser.add_argument("--fix", required=True, help="What you changed")
    parser.add_argument("--files", default="", help="Comma-separated paths touched")
    parser.add_argument("--spec-ref", default="", help="product.md / design.md / contrast rule violated")
    parser.add_argument("--severity", default="error", choices=["error", "warn", "info"])
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    slug = feature_slug(args.route)
    out = visual_audit_dir(root)
    out.mkdir(parents=True, exist_ok=True)

    files = [f.strip() for f in args.files.split(",") if f.strip()]
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "route": args.route,
        "issue": args.issue,
        "fix": args.fix,
        "files": files,
        "spec_ref": args.spec_ref,
        "severity": args.severity,
    }

    log_path = out / "fix-log.md"
    if not log_path.is_file():
        log_path.write_text(f"# Visual auditor fix log\n\n**Started:** {date.today().isoformat()}\n\n", encoding="utf-8")

    block = [
        f"### {entry['timestamp']}: `{args.route}` [{args.severity}]",
        "",
        f"- **Issue:** {args.issue}",
        f"- **Spec:** {args.spec_ref or ' - '}",
        f"- **Fix:** {args.fix}",
        f"- **Files:** {', '.join(f'`{f}`' for f in files) if files else ' - '}",
        "",
    ]
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(block))

    # Update session review doc if present
    reviews = out / "reviews"
    review_files = sorted(reviews.glob(f"{slug}-review-*.md"), reverse=True) if reviews.is_dir() else []
    if review_files:
        review = review_files[0]
        text = review.read_text(encoding="utf-8")
        row = f"| {date.today().isoformat()} | {args.issue[:60]} | {args.spec_ref or ' - '} | {args.severity} |"
        fix_line = f"- **{args.issue}** → {args.fix} (`{', '.join(files)}`)"
        if "## Issues found" in text and row not in text:
            text = text.replace(
                "|---|-------|----------|----------|",
                "|---|-------|----------|----------|\n" + row,
                1,
            )
        if "## Fixes applied" in text and fix_line not in text:
            text = text.replace(
                "_Use append_fix_log.py per fix: entries mirror below._",
                fix_line + "\n\n_Use append_fix_log.py per fix: entries mirror below._",
                1,
            )
        review.write_text(text, encoding="utf-8")
        entry["review_doc"] = str(review.relative_to(root))

    jsonl = out / "fix-log.jsonl"
    with jsonl.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    emit(json.dumps({"status": "ok", "log": str(log_path.relative_to(root)), **entry}, indent=2))


if __name__ == "__main__":
    main()
