#!/usr/bin/env python3
"""Validate mockup brief and sync design.md for Flutter handoff."""
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime

from _heyeddi_paths import canonical_design_path, design_md, designs_dir
from _skill_cli import emit, fail, resolve_project_root

BRIEF_FILENAME = "mockup-brief.md"


def feature_dir(root, route: str, feature: str | None):
    feat = feature or route.strip("/").replace("/", "-") or "home"
    return feat, designs_dir(root) / feat


def check_brief(feature_path) -> dict:
    bp = feature_path / BRIEF_FILENAME
    if not bp.is_file():
        return {"ok": False, "missing": True, "hint": f"Write {BRIEF_FILENAME} before implementing"}
    text = bp.read_text()
    ok = len(text.strip()) > 150 and "## implementation spec" in text.lower()
    return {"ok": ok, "chars": len(text), "has_implementation_spec": "## implementation spec" in text.lower()}


def sync_design_md(root, feature_path, *, dry_run: bool = False) -> dict:
    d_path = design_md(root) or canonical_design_path(root)
    bp = feature_path / BRIEF_FILENAME
    if not bp.is_file():
        fail(f"Cannot sync without {bp}")
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    injection = f"""## Layout: {feature_path.name} Flutter handoff ({today})

**Source:** `.heyeddi/designs/{feature_path.name}/{BRIEF_FILENAME}`

Implement with Material 3 widgets: `lib/theme/app_theme.dart`, `lib/widgets/app_shell.dart`.
"""
    if dry_run:
        return {"design_md": str(d_path), "dry_run": True}
    d_path.parent.mkdir(parents=True, exist_ok=True)
    existing = d_path.read_text() if d_path.is_file() else "# Design\n\nFlutter Material 3.\n"
    marker = f"## Layout: {feature_path.name} Flutter handoff"
    if marker not in existing:
        existing = existing.rstrip() + "\n\n" + injection
    d_path.write_text(existing)
    return {"design_md": str(d_path), "synced": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sync-design", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    feat, fdir = feature_dir(root, args.route, args.feature)
    status = check_brief(fdir)
    result = {"route": args.route, "feature": feat, "brief_status": status, "frontend": "flutter"}
    if args.sync_design:
        result["design_sync"] = sync_design_md(root, fdir, dry_run=args.dry_run)
    emit(json.dumps(result, indent=2))
    if args.check and not status.get("ok"):
        fail(status.get("hint", "brief incomplete"))


if __name__ == "__main__":
    main()
