#!/usr/bin/env python3
"""Detect broken circular CSS custom-property aliases in tokens.css."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _skill_cli import emit, fail, resolve_project_root

DEFAULT_TOKENS = Path("src/styles/tokens.css")
CIRCULAR_ALIAS = re.compile(
    r"^\s*(--[\w-]+)\s*:\s*var\(\s*(--[\w-]+)\s*\)\s*;",
    re.MULTILINE,
)


def verify_tokens_css(text: str) -> dict:
    circular: list[str] = []
    for match in CIRCULAR_ALIAS.finditer(text):
        lhs, rhs = match.group(1), match.group(2)
        if lhs == rhs:
            circular.append(lhs)
    return {
        "ok": not circular,
        "circular_aliases": circular,
    }


def verify_tokens_file(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path), "error": "tokens.css missing"}
    result = verify_tokens_css(path.read_text(encoding="utf-8", errors="replace"))
    result["path"] = str(path)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify tokens.css has no circular aliases")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--tokens-path", default=str(DEFAULT_TOKENS))
    parser.add_argument("--check", action="store_true", help="Exit 1 if verification fails")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    result = verify_tokens_file(root / args.tokens_path)
    emit(result)

    if args.check and not result.get("ok"):
        detail = result.get("error") or ", ".join(result.get("circular_aliases") or [])
        fail(
            "tokens.css verification failed: "
            + detail
            + ". Remove same-name aliases like `--size-6: var(--size-6)`; use OpenProps "
            "scale vars directly or map to a different semantic name."
        )


if __name__ == "__main__":
    main()
