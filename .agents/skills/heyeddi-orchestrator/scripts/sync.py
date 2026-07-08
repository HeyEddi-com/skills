#!/usr/bin/env python3
"""Full `.heyeddi/` sync — migrate names, refresh index, init workflow if new."""
from __future__ import annotations

import argparse
from pathlib import Path

from _catalog import find_hub_root, write_skills_index
from _heyeddi_migrate import migrate_heyeddi
from _skill_cli import emit, resolve_project_root
from init_workflow_sync import scaffold_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync .heyeddi/ workspace for installed skills")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--hub-root", default=None)
    parser.add_argument("--force-migrate", action="store_true")
    parser.add_argument("--skip-workflow", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root, auto_sync=False)
    hub_root = Path(args.hub_root).resolve() if args.hub_root else find_hub_root(project_root)
    skill_dir = Path(__file__).resolve().parent

    migration = migrate_heyeddi(
        project_root,
        hub_root=hub_root,
        skill_dir=skill_dir,
        dry_run=args.dry_run,
        force=args.force_migrate,
    )

    if args.dry_run:
        emit(
            {
                "dry_run": True,
                "heyeddi_migration": migration,
                "would_write": [".heyeddi/skills-index.json", ".heyeddi/skills-index.md"],
            }
        )
        return

    payload = {"heyeddi_migration": migration, **write_skills_index(project_root, hub_root)}

    workflow_readme = project_root / ".heyeddi" / "docs" / "workflow" / "README.md"
    if not args.skip_workflow and not workflow_readme.is_file():
        payload["workflow"] = scaffold_workflow(project_root)
        payload["workflow_initialized"] = workflow_readme.is_file()

    emit(payload)


if __name__ == "__main__":
    main()
