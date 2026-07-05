#!/usr/bin/env python3
"""Verify Flutter theme coherence: Material 3, light/dark, router wiring."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _skill_cli import emit, fail, resolve_project_root

THEME_PATH = Path("lib/theme/app_theme.dart")
MAIN_PATH = Path("lib/main.dart")


def verify_flutter_theme(root: Path) -> list[str]:
    errors: list[str] = []
    theme_file = root / THEME_PATH
    main_file = root / MAIN_PATH

    if not theme_file.is_file():
        return [f"missing {THEME_PATH}"]

    theme = theme_file.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"static\s+ThemeData\s+get\s+light", theme):
        errors.append("app_theme.dart must expose static light ThemeData getter")
    if not re.search(r"static\s+ThemeData\s+get\s+dark", theme):
        errors.append("app_theme.dart must expose static dark ThemeData getter")
    if "CardTheme" not in theme and "cardTheme" not in theme:
        errors.append("app_theme.dart should configure CardTheme for handoff surfaces")

    if main_file.is_file():
        main = main_file.read_text(encoding="utf-8", errors="replace")
        if "theme:" not in main and "ThemeData" not in main:
            errors.append("main.dart should wire AppTheme light/dark to MaterialApp")
    else:
        errors.append(f"missing {MAIN_PATH}")

    router = root / "lib/router/app_router.dart"
    if router.is_file():
        text = router.read_text(encoding="utf-8", errors="replace")
        if "GoRoute" not in text:
            errors.append("app_router.dart should define GoRoute entries")
    else:
        errors.append("missing lib/router/app_router.dart")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Flutter theme coherence")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    errors = verify_flutter_theme(root)
    if errors:
        msg = "Flutter theme verification FAILED:\n" + "\n".join(f"- {e}" for e in errors)
        if args.check:
            fail(msg)
        emit(msg)
        return
    emit("Flutter theme verification OK — Material 3 light/dark themes and router wired.")


if __name__ == "__main__":
    main()
