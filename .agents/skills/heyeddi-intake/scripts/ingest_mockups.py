#!/usr/bin/env python3
"""Copy user-provided mockup images into .heyeddi/designs/<feature>/."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from _heyeddi_paths import designs_dir
from _skill_cli import emit, resolve_project_root

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest user mockup images")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--route", default=None)
    parser.add_argument("--app-name", default="App")
    parser.add_argument("--source", action="append", default=[], help="Image file path (repeatable)")
    parser.add_argument("--source-dir", default=None, help="Directory of images to copy")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    dest = designs_dir(root) / args.feature
    dest.mkdir(parents=True, exist_ok=True)

    sources: list[Path] = [Path(s) for s in args.source]
    if args.source_dir:
        d = Path(args.source_dir)
        if d.is_dir():
            sources.extend(p for p in sorted(d.iterdir()) if p.suffix.lower() in IMAGE_EXTS)

    copied: list[str] = []
    for i, src in enumerate(sources):
        if not src.is_file():
            continue
        if src.name.lower() in ("desktop.png", "mobile.png"):
            name = src.name
        elif "mobile" in src.name.lower():
            name = "mobile.png" if src.suffix.lower() == ".png" else src.name
        elif "desktop" in src.name.lower() or i == 0:
            name = "desktop.png" if src.suffix.lower() == ".png" and not (dest / "desktop.png").exists() else src.name
        else:
            name = src.name
        target = dest / name
        shutil.copy2(src, target)
        copied.append(str(target.relative_to(root)))

    handoff = dest / "handoff.json"
    meta = {
        "route": args.route or f"/{args.feature.replace('-', '/')}",
        "app": args.app_name,
        "mockup_contract": "user_provided",
        "sources_ingested": copied,
        "notes": [
            "User-provided mockups ingested by @heyeddi-intake",
            "mockup-brief.md may be seeded via seed_brief.py or refined by @heyeddi-handoff",
        ],
    }
    handoff.write_text(json.dumps(meta, indent=2) + "\n")

    emit(
        json.dumps(
            {
                "status": "ok" if copied else "warn",
                "feature": args.feature,
                "dest": str(dest),
                "copied": copied,
                "hint": "Run seed_brief.py if mockup-brief.md missing" if copied else "No images copied",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
