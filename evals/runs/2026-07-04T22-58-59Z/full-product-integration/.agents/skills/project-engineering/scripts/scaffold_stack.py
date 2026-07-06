#!/usr/bin/env python3
"""Scaffold the right HeyEddi stacks: vue, fastapi, firebase, or full."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from _project_detect import detect, infer_backends
from _skill_cli import emit, resolve_project_root

SCRIPTS = Path(__file__).resolve().parent


def run_script(name: str, root: Path, *, dry_run: bool, force: bool) -> dict:
    cmd = [sys.executable, str(SCRIPTS / name), "--project-root", str(root)]
    if dry_run:
        cmd.append("--dry-run")
    if force:
        cmd.append("--force")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {"script": name, "status": "fail", "output": proc.stderr or proc.stdout}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"script": name, "status": "ok", "output": proc.stdout}


def resolve_stacks(root: Path, stack: str) -> list[str]:
    if stack == "auto":
        detected = detect(root)
        stacks: list[str] = []
        if detected["vue"] or (root / "package.json").is_file() or (root / "src").is_dir():
            stacks.append("vue")
        for b in infer_backends(root):
            if b not in stacks:
                stacks.append(b)
        if not stacks:
            stacks = ["vue"]
        return stacks

    if stack == "full":
        return ["vue", "fastapi", "firebase"]

    return [stack]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold HeyEddi project stacks")
    parser.add_argument("--project-root", default=None)
    parser.add_argument(
        "--stack",
        choices=["auto", "vue", "fastapi", "firebase", "full"],
        default="auto",
        help="Which stack(s) to scaffold (default: auto from detection)",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    stacks = resolve_stacks(root, args.stack)
    results: list[dict] = []

    mapping = {
        "vue": "scaffold_vue.py",
        "fastapi": "scaffold_fastapi.py",
        "firebase": "scaffold_firebase.py",
    }
    for name in stacks:
        script = mapping.get(name)
        if script:
            results.append(run_script(script, root, dry_run=args.dry_run, force=args.force))

    results.append(run_script("scaffold_heyeddi.py", root, dry_run=args.dry_run, force=args.force))

    emit(
        json.dumps(
            {
                "status": "ok",
                "stacks": stacks,
                "detected": detect(root),
                "dry_run": args.dry_run,
                "results": results,
                "next": "ensure_npm / ensure_python → dev_server_info",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
