#!/usr/bin/env python3
"""Light static checks on Dart provider/repository files."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, resolve_project_root

WARN_PATTERNS = [
    (re.compile(r"\bDio\s*\("), "Consider injecting ApiClient instead of raw Dio()"),
    (re.compile(r"FirebaseFirestore\.instance"), "OK in repository; avoid in widgets"),
    (re.compile(r"http\."), "Prefer ApiClient/dio for HTTP"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Dart provider file")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    target = root / args.path
    if not target.is_file():
        emit(json.dumps({"status": "fail", "error": f"not found: {target}"}, indent=2))
        return

    text = target.read_text()
    warnings = [msg for pat, msg in WARN_PATTERNS if pat.search(text)]
    emit(
        json.dumps(
            {
                "status": "ok" if not warnings else "warn",
                "path": str(target),
                "warnings": warnings,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
