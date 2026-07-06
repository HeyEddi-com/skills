#!/usr/bin/env python3
"""Append an engineering ADR to `.heyeddi/docs/engineering/decisions.md`."""
from __future__ import annotations

import argparse
from datetime import date

from _heyeddi_paths import engineering_docs_dir
from _skill_cli import emit, fail, resolve_project_root

INIT_ENGINEERING = "Run init_engineering_docs.py first."


def main() -> None:
    parser = argparse.ArgumentParser(description="Append engineering decision")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--title", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--consequences", default="")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    decisions = engineering_docs_dir(root) / "decisions.md"
    if not decisions.is_file():
        fail(INIT_ENGINEERING)

    today = date.today().isoformat()
    block = f"""
### {today} — {args.title}

**Context:** {args.context}

**Decision:** {args.decision}

**Consequences:** {args.consequences or "Document follow-ups in next audit."}
"""
    text = decisions.read_text(encoding="utf-8")
    decisions.write_text(text.rstrip() + "\n" + block + "\n", encoding="utf-8")
    emit({"ok": True, "path": str(decisions.relative_to(root)), "title": args.title})


if __name__ == "__main__":
    main()
