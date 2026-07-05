"""Run verification commands and capture full output for agentic judge."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

DEFAULT_TIMEOUT = 600


def _has_script(pkg: dict, name: str) -> bool:
    script = pkg.get("scripts", {}).get(name, "")
    return bool(script) and not str(script).strip().startswith("echo ")


def default_verify_commands(sandbox: Path) -> list[str]:
    """Sensible checks when turn does not specify verify_commands."""
    cmds: list[str] = []
    pkg_path = sandbox / "package.json"
    if pkg_path.is_file():
        pkg = json.loads(pkg_path.read_text())
        if _has_script(pkg, "test"):
            cmds.append("npm test")
        if _has_script(pkg, "build"):
            cmds.append("npm run build")
    backend = sandbox / "backend"
    if (backend / "tests").is_dir():
        if (backend / "pyproject.toml").is_file():
            cmds.append("cd backend && poetry run pytest -q")
        else:
            cmds.append("cd backend && python3 -m pytest -q")
    return cmds


def run_verify_commands(sandbox: Path, commands: list[str] | None) -> list[dict]:
    """Run commands; return full stdout/stderr and exit code for each."""
    to_run = commands if commands is not None else default_verify_commands(sandbox)
    results: list[dict] = []
    for cmd in to_run:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=sandbox,
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT,
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        combined = stdout + stderr
        results.append(
            {
                "command": cmd,
                "exit_code": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "combined": combined,
            }
        )
    return results


def format_command_results(results: list[dict]) -> str:
    if not results:
        return "(no verification commands run)"
    parts: list[str] = []
    for r in results:
        parts.append(
            f"### $ {r['command']}\n"
            f"exit_code: {r['exit_code']}\n"
            f"```\n{(r['combined'] or '(empty)')[-12000:]}\n```\n"
        )
    return "\n".join(parts)
