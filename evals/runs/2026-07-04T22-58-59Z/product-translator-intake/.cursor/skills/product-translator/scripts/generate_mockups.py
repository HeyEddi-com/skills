#!/usr/bin/env python3
"""Generate professional layout mockup PNGs when user did not supply images."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import designs_dir
from _layout_mockups import MockupSpec, draw_settings_desktop, draw_settings_mobile, pillow_available
from _skill_cli import emit, fail, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate professional handoff mockups")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", default="settings")
    parser.add_argument("--preset", choices=["settings-app-shell"], default="settings-app-shell")
    parser.add_argument("--route", default="/settings")
    parser.add_argument("--app-name", default="HeyEddi App")
    parser.add_argument("--page-title", default="Settings")
    parser.add_argument("--page-subtitle", default="Profile and notifications")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not pillow_available():
        emit(
            json.dumps(
                {
                    "status": "fail",
                    "error": "Pillow not installed",
                    "hint": "uv sync --group hub-tools",
                },
                indent=2,
            )
        )
        return

    root = resolve_project_root(args.project_root)
    out_dir = designs_dir(root) / args.feature
    spec = MockupSpec(
        app_name=args.app_name,
        route=args.route,
        feature=args.feature,
        page_title=args.page_title,
        page_subtitle=args.page_subtitle,
    )

    if args.dry_run:
        emit(json.dumps({"status": "dry_run", "dest": str(out_dir), "preset": args.preset}, indent=2))
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    if args.preset == "settings-app-shell":
        draw_settings_desktop(spec).save(out_dir / "desktop.png", "PNG")
        draw_settings_mobile(spec).save(out_dir / "mobile.png", "PNG")

    handoff = {
        "route": args.route,
        "app": args.app_name,
        "mockup_contract": "layout_professional",
        "generated_by": "heyeddi-intake",
        "notes": [
            "Professional layout reference — colors from .heyeddi/design.md tokens at implement time",
            "mockup-brief.md seeded by seed_brief.py; refine before @heyeddi-handoff if needed",
        ],
    }
    (out_dir / "handoff.json").write_text(json.dumps(handoff, indent=2) + "\n")

    emit(
        json.dumps(
            {
                "status": "ok",
                "feature": args.feature,
                "artifacts": [
                    str((out_dir / "desktop.png").relative_to(root)),
                    str((out_dir / "mobile.png").relative_to(root)),
                ],
                "next": "seed_brief.py --feature " + args.feature,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
