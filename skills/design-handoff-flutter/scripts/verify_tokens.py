#!/usr/bin/env python3
"""Verify Flutter theme tokens in lib/theme/app_theme.dart."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _skill_cli import emit, fail, resolve_project_root

DEFAULT_THEME = Path("lib/theme/app_theme.dart")


def verify_theme_tokens(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path), "error": "app_theme.dart missing"}

    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []

    if "useMaterial3" not in text or not re.search(r"useMaterial3:\s*true", text):
        errors.append("ThemeData must set useMaterial3: true")

    if "Brightness.light" not in text:
        errors.append("missing light ThemeData (Brightness.light)")
    if "Brightness.dark" not in text:
        errors.append("missing dark ThemeData (Brightness.dark)")

    if "ColorScheme" not in text:
        errors.append("ThemeData should define ColorScheme (fromSeed or explicit)")

    # Hardcoded colors outside theme file are OK in widgets; theme should centralize brand
    if not re.search(r"Color\s*\(\s*0x", text):
        errors.append("theme file should define at least one brand Color(0x...) constant")

    return {
        "ok": not errors,
        "path": str(path),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Flutter theme tokens")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--theme-path", default=str(DEFAULT_THEME))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    result = verify_theme_tokens(root / args.theme_path)
    emit(result)

    if args.check and not result.get("ok"):
        detail = result.get("error") or "; ".join(result.get("errors") or [])
        fail(f"Flutter theme token verification failed: {detail}")


if __name__ == "__main__":
    main()
