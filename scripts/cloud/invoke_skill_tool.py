#!/usr/bin/env python3
"""Invoke a skill script with JSON or CLI args. Used by Cloud Run agent."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def build_cmd(script_path: Path, args: dict[str, Any], project_root: Path) -> list[str]:
    if script_path.suffix == ".sh":
        cmd = ["bash", str(script_path), "--project-root", str(project_root)]
    else:
        cmd = [sys.executable, str(script_path), "--project-root", str(project_root)]
    for key, value in args.items():
        if key == "project_root":
            continue
        flag = f"--{key.replace('_', '-')}"
        if isinstance(value, bool):
            if value:
                cmd.append(flag)
        elif isinstance(value, list):
            for item in value:
                cmd.extend([flag, str(item)])
        elif value is not None:
            cmd.extend([flag, str(value)])
    return cmd


def invoke_skill_tool(
    skill_dir: Path,
    script: str,
    args: dict[str, Any],
    *,
    project_root: Path,
    timeout: int = 600,
) -> str:
    script_path = skill_dir / script
    if not script_path.is_file():
        return f"[error] script not found: {script_path}"

    cmd = build_cmd(script_path, args, project_root)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"[error] timed out after {timeout}s: {' '.join(cmd)}"

    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        return f"[exit {result.returncode}]\n{output}".strip()
    return output.strip() or "(success, no output)"


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoke a skill tool script")
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--script", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--args-json", default="{}")
    parser.add_argument("--timeout", type=int, default=600)
    ns = parser.parse_args()

    args = json.loads(ns.args_json)
    out = invoke_skill_tool(
        Path(ns.skill_dir),
        ns.script,
        args,
        project_root=Path(ns.project_root),
        timeout=ns.timeout,
    )
    print(out)


if __name__ == "__main__":
    main()
