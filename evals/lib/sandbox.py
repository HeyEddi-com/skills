"""Create isolated eval workspaces from project templates."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from evals.lib.fs_utils import robust_rmtree

# Never copy install artifacts — npm bin stubs break when copytree'd.
SANDBOX_COPY_IGNORE = shutil.ignore_patterns(
    "node_modules",
    "dist",
    ".vite",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "*.pyc",
)


def install_skills(hub_root: Path, project_root: Path, skill_names: list[str]) -> None:
    """Install skills for both skills CLI and local Cursor agent discovery."""
    for dest_root in (
        project_root / ".agents" / "skills",
        project_root / ".cursor" / "skills",
    ):
        dest_root.mkdir(parents=True, exist_ok=True)
        for name in skill_names:
            src = hub_root / "skills" / name
            dest = dest_root / name
            if dest.exists():
                robust_rmtree(dest)
            shutil.copytree(src, dest)


def create_sandbox(
    hub_root: Path,
    template_name: str,
    skill_names: list[str],
    work_dir: Path,
    eval_id: str,
) -> Path:
    template = hub_root / "evals" / "projects" / template_name
    if not template.is_dir():
        raise FileNotFoundError(f"Eval template not found: {template_name}")

    sandbox = work_dir / eval_id
    if sandbox.exists():
        robust_rmtree(sandbox)
    shutil.copytree(template, sandbox, ignore=SANDBOX_COPY_IGNORE)
    install_skills(hub_root, sandbox, skill_names)
    return sandbox


def ensure_npm_deps(sandbox: Path, *, quiet: bool = False) -> None:
    """Fresh npm install after template copy (node_modules is never copied)."""
    if not (sandbox / "package.json").is_file():
        return
    if (sandbox / "node_modules").is_dir() and not (sandbox / "package-lock.json").is_file():
        return
    lock = sandbox / "package-lock.json"
    cmd = ["npm", "ci"] if lock.is_file() else ["npm", "install"]
    if not quiet:
        label = "npm ci" if lock.is_file() else "npm install"
        print(f"  sandbox: {label}…", flush=True)
    proc = subprocess.run(
        cmd,
        cwd=sandbox,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        tail = ((proc.stdout or "") + (proc.stderr or "")).strip()[-600:]
        raise RuntimeError(f"{' '.join(cmd)} failed in sandbox:\n{tail}")
