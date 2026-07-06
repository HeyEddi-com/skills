
#!/usr/bin/env python3
"""Resolve handoff inputs for Flutter implementation."""
from __future__ import annotations

import argparse
import json

from _heyeddi_paths import design_md, designs_dir, product_md
from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Load Flutter design handoff brief")
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    feature = args.feature or args.route.strip("/").replace("/", "-") or "home"
    feature_dir = designs_dir(root) / feature
    screenshots: list[str] = []
    if feature_dir.is_dir():
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            screenshots.extend(str(p) for p in feature_dir.glob(ext))

    mockup_brief = feature_dir / "mockup-brief.md"
    wireframe_md = feature_dir / "wireframe.md"
    d_path = design_md(root)
    p_path = product_md(root)

    brief = {
        "route": args.route,
        "feature": feature,
        "frontend": "flutter",
        "designs_dir": str(feature_dir),
        "screenshots": screenshots,
        "wireframe_md": str(wireframe_md) if wireframe_md.is_file() else None,
        "mockup_brief": str(mockup_brief) if mockup_brief.is_file() else None,
        "design_md": str(d_path) if d_path else None,
        "product_md": str(p_path) if p_path else None,
        "workflow": [
            "1. load_handoff",
            "2. Author mockup-brief.md (Material 3 widget spec)",
            "3. describe_handoff --sync-design",
            "4. AppShell / NavigationDrawer per reference/material-handoff.md",
            "5. Route screen in lib/screens/ → verify_handoff --phase full",
        ],
        "theme_file": "lib/theme/app_theme.dart",
        "shell_widget": "lib/widgets/app_shell.dart",
    }
    if mockup_brief.is_file():
        brief["mockup_brief_text"] = mockup_brief.read_text()
        brief["interpret_required"] = False
    else:
        brief["interpret_required"] = True
        brief["interpret_hint"] = "AUTHOR mockup-brief.md before implementing Flutter widgets."
    emit(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()
