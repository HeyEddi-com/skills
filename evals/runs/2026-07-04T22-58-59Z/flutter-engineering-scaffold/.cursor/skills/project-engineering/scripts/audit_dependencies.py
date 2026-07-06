#!/usr/bin/env python3
"""Audit npm/poetry dependency hygiene."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_hub = Path(__file__).resolve().parents[3]
if str(_hub) not in sys.path:
    sys.path.insert(0, str(_hub))

from scripts.lib.quality_gate import audit_dependencies  # noqa: E402

from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit dependency hygiene")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--max-major-behind", type=int, default=1)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    ok, detail = audit_dependencies(root, max_major_behind=args.max_major_behind)
    emit(json.dumps({"status": "ok" if ok else "fail", "detail": detail}, indent=2))


if __name__ == "__main__":
    main()
