#!/usr/bin/env python3
"""Add or repair HeyEddi standard Flutter scaffold files."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from _skill_cli import emit, resolve_project_root

SCAFFOLD_ROOT = Path(__file__).resolve().parent.parent / "scaffold" / "flutter"


def copy_tree(src_root: Path, dest_root: Path, *, force: bool, dry_run: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    for src in src_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(src_root)
        dest = dest_root / rel
        if dest.exists() and not force:
            skipped.append(str(rel))
            continue
        if dry_run:
            created.append(str(rel))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        created.append(str(rel))
    return created, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold Flutter engineering baseline")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    created, skipped = copy_tree(SCAFFOLD_ROOT, root, force=args.force, dry_run=args.dry_run)

    stack_cfg = root / ".heyeddi" / "stack.json"
    stack_src = Path(__file__).resolve().parent.parent / "scaffold" / "stack-flutter.json"
    if stack_src.is_file() and (not stack_cfg.exists() or args.force):
        if not args.dry_run:
            stack_cfg.parent.mkdir(parents=True, exist_ok=True)
            stack_cfg.write_text(stack_src.read_text())
        created.append(".heyeddi/stack.json")
    elif stack_cfg.exists():
        skipped.append(".heyeddi/stack.json")

    emit(
        json.dumps(
            {
                "status": "ok",
                "stack": "flutter",
                "dry_run": args.dry_run,
                "created": created,
                "skipped": skipped,
                "next": "ensure_flutter → dev_server_info",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
