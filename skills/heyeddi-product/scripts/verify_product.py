#!/usr/bin/env python3
"""Verify PM artifacts — audit + feature matrix gate.

Security: only execs allowlisted sibling scripts under this skill's scripts/
directory (no path args from the user, no shell).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _heyeddi_paths import product_md
from _skill_cli import emit, fail, resolve_project_root

# Exact basenames only — never accept a caller-supplied script path.
_ALLOWED_SCRIPTS = frozenset({"audit_product.py", "check_features.py"})


def _resolve_sibling(script_name: str) -> Path:
    if script_name not in _ALLOWED_SCRIPTS:
        raise ValueError(f"script not allowlisted: {script_name}")
    scripts = Path(__file__).resolve().parent
    script = (scripts / script_name).resolve()
    if script.parent != scripts or not script.is_file():
        raise ValueError(f"sibling script missing or escaped: {script_name}")
    return script


def _run(script_name: str, root: Path, extra: list[str]) -> tuple[int, str]:
    script = _resolve_sibling(script_name)
    # Extra flags are fixed allowlisted tokens from this file only.
    safe_extra = [flag for flag in extra if flag in {"--check"}]
    cmd = [sys.executable, str(script), "--project-root", str(root), *safe_extra]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=script.parent)
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify product docs and feature implementation")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--skip-features", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    if not product_md(root):
        fail("missing .heyeddi/product.md")

    checks: list[dict] = []

    code, _out = _run("audit_product.py", root, ["--check"] if args.check else [])
    checks.append({"name": "audit_product", "exit": code, "ok": code == 0})

    if not args.skip_features:
        code2, _out2 = _run("check_features.py", root, ["--check"] if args.check else [])
        checks.append({"name": "check_features", "exit": code2, "ok": code2 == 0})

    failed = [c for c in checks if not c["ok"]]
    emit(
        json.dumps(
            {
                "status": "fail" if failed else "ok",
                "checks": checks,
                "failed": [c["name"] for c in failed],
            },
            indent=2,
        )
    )
    if args.check and failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
