#!/usr/bin/env python3
"""Add HeyEddi Firebase tooling (rules, emulators config, env template)."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from _skill_cli import emit, resolve_project_root

SCAFFOLD = Path(__file__).resolve().parent.parent / "scaffold" / "firebase"

ROOT_FILES = (
    "firebase.json",
    ".firebaserc",
    "firestore.rules",
    "firestore.indexes.json",
    ".env.firebase.example",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold Firebase tooling")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    created: list[str] = []
    skipped: list[str] = []

    for name in ROOT_FILES:
        src = SCAFFOLD / name
        dest = root / name
        if not src.is_file():
            continue
        if dest.exists() and not args.force:
            skipped.append(name)
            continue
        if args.dry_run:
            created.append(name)
            continue
        shutil.copy2(src, dest)
        created.append(name)

    stack_cfg = root / ".heyeddi" / "stack.json"
    if not stack_cfg.exists() and not args.dry_run:
        stack_cfg.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            Path(__file__).resolve().parent.parent / "scaffold" / "stack-firebase.json",
            stack_cfg,
        )
        created.append(".heyeddi/stack.json")

    emit(
        json.dumps(
            {
                "status": "ok",
                "stack": "firebase",
                "dry_run": args.dry_run,
                "created": created,
                "skipped": skipped,
                "next": "Install Firebase CLI; run dev_server_info for emulator command",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
