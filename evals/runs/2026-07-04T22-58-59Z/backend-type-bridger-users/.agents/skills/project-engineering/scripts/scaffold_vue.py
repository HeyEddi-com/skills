#!/usr/bin/env python3
"""Add or repair HeyEddi standard Vue + Vite + Vitest scaffold files."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _skill_cli import emit, resolve_project_root

SCAFFOLD_ROOT = Path(__file__).resolve().parent.parent / "scaffold" / "vue"

FILE_MAP = {
    "package.json": "package.json",
    "vite.config.ts": "vite.config.ts",
    "vitest.config.ts": "vitest.config.ts",
    "tsconfig.json": "tsconfig.json",
    "tsconfig.app.json": "tsconfig.app.json",
    "tsconfig.node.json": "tsconfig.node.json",
    "index.html": "index.html",
    "src/env.d.ts": "src/env.d.ts",
    "src/main.ts": "src/main.ts",
    "src/styles/tokens.css": "src/styles/tokens.css",
    "src/router/index.ts": "src/router/index.ts",
    "tests/unit/setup.ts": "tests/unit/setup.ts",
    "tests/unit/App.spec.ts": "tests/unit/App.spec.ts",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold Vue engineering baseline")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold-managed files")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    created: list[str] = []
    skipped: list[str] = []

    for rel, template_name in FILE_MAP.items():
        dest = root / rel
        src = SCAFFOLD_ROOT / template_name
        if not src.is_file():
            continue
        if dest.exists() and not args.force:
            skipped.append(rel)
            continue
        if args.dry_run:
            created.append(rel)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text())
        created.append(rel)

    # App.vue: only create if missing
    app_vue = root / "src" / "App.vue"
    app_template = SCAFFOLD_ROOT / "src" / "App.vue"
    if app_template.is_file():
        if not app_vue.is_file() or args.force:
            if not args.dry_run:
                app_vue.parent.mkdir(parents=True, exist_ok=True)
                app_vue.write_text(app_template.read_text())
            created.append("src/App.vue")
        else:
            skipped.append("src/App.vue")

    for doc in ("DESIGN.md", "PRODUCT.md"):
        dest = root / doc
        src = SCAFFOLD_ROOT / doc
        if src.is_file() and not dest.is_file():
            if not args.dry_run:
                dest.write_text(src.read_text())
            created.append(doc)

    # Canonical HeyEddi workspace (.heyeddi/README.md, product.md, design.md, …)
    he_cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "scaffold_heyeddi.py"),
        "--project-root",
        str(root),
    ]
    if args.dry_run:
        he_cmd.append("--dry-run")
    if args.force:
        he_cmd.append("--force")
    subprocess.run(he_cmd, check=False)

    emit(
        json.dumps(
            {
                "status": "ok",
                "dry_run": args.dry_run,
                "created": created,
                "skipped": skipped,
                "next": "Run ensure_npm then audit_scaffold",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
