#!/usr/bin/env python3
"""Verify PM artifacts — audit + feature matrix gate."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _heyeddi_paths import product_md
from _skill_cli import emit, fail, resolve_project_root


def _run(script: Path, root: Path, extra: list[str]) -> tuple[int, str]:
    cmd = [sys.executable, str(script), "--project-root", str(root), *extra]
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

    scripts = Path(__file__).parent
    checks: list[dict] = []

    code, out = _run(scripts / "audit_product.py", root, ["--check"] if args.check else [])
    checks.append({"name": "audit_product", "exit": code, "ok": code == 0})

    if not args.skip_features:
        code2, out2 = _run(scripts / "check_features.py", root, ["--check"] if args.check else [])
        checks.append({"name": "check_features", "exit": code2, "ok": code2 == 0})
        out = out + "\n" + out2

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
