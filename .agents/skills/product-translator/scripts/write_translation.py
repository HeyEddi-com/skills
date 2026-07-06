#!/usr/bin/env python3
"""Persist translation session notes for downstream skills."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from _heyeddi_paths import intake_dir
from _skill_cli import emit, fail, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Write intake translation record")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--user-prompt", required=True)
    parser.add_argument("--summary", required=True, help="One-paragraph product interpretation")
    parser.add_argument("--decisions", default="[]", help="JSON array of decision strings")
    parser.add_argument("--open-questions", default="[]", help="JSON array")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    out_base = intake_dir(root)
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    path = out_base / f"translation-{today}.md"

    try:
        decisions = json.loads(args.decisions)
        questions = json.loads(args.open_questions)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    body = f"""# Product translation — {today}

## User prompt

{args.user_prompt.strip()}

## Interpretation

{args.summary.strip()}

## Decisions

"""
    for d in decisions:
        body += f"- {d}\n"
    body += "\n## Open questions\n\n"
    if questions:
        for q in questions:
            body += f"- {q}\n"
    else:
        body += "_None — proceed to mockups and routing._\n"
    body += "\n## Next\n\nRun `write_routing.py` then chain skills listed in `skill-routing.json`.\n"

    if args.dry_run:
        emit(json.dumps({"status": "dry_run", "path": str(path)}, indent=2))
        return

    out_base.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    index = out_base / "index.md"
    if not index.is_file():
        index.write_text("# Intake translations\n\nSession notes from `@product-translator`.\n\n")
    emit(json.dumps({"status": "ok", "path": str(path)}, indent=2))


if __name__ == "__main__":
    main()
