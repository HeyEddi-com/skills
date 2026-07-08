#!/usr/bin/env python3
"""Migrate `.heyeddi/` skill references to v2 canonical names."""
from __future__ import annotations

import argparse
from pathlib import Path

from _catalog import find_hub_root
from _heyeddi_migrate import migrate_heyeddi
from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate .heyeddi/ skill name references")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--hub-root", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-run even if sync-state matches")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root, auto_sync=False)
    hub_root = Path(args.hub_root).resolve() if args.hub_root else find_hub_root(project_root)
    skill_dir = Path(__file__).resolve().parent

    emit(
        migrate_heyeddi(
            project_root,
            hub_root=hub_root,
            skill_dir=skill_dir,
            dry_run=args.dry_run,
            force=args.force,
        )
    )


if __name__ == "__main__":
    main()
