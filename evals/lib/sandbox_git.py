"""Git baseline in eval sandboxes to track all agent changes."""
from __future__ import annotations

import subprocess
from pathlib import Path

EVAL_GITIGNORE = """node_modules/
dist/
.venv/
__pycache__/
*.pyc
.pytest_cache/
coverage/
.turbo/
.heyeddi/_eval_agent_prompt.md
"""

MAX_FILE_BYTES = 48_000
MAX_TOTAL_BYTES = 280_000
TEXT_SUFFIXES = {
    ".vue", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".css", ".html",
    ".yaml", ".yml", ".toml", ".py", ".sh", ".txt", ".svg",
}


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode, out


def stage_worktree_for_judge(sandbox: Path) -> None:
    """Stage new/untracked agent files so git diff includes them for the judge."""
    _run(["git", "add", "-A"], sandbox)


def list_design_assets(sandbox: Path) -> str:
    """Inventory handoff PNGs/mockups (baseline or new) for judge context."""
    roots = [sandbox / ".heyeddi" / "designs", sandbox / "designs"]
    lines: list[str] = []
    seen: set[str] = set()
    for base in roots:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(sandbox).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            lines.append(f"- {rel} ({path.stat().st_size} bytes)")
    return "\n".join(lines) if lines else "(no design assets under .heyeddi/designs/ or designs/)"


def init_baseline(sandbox: Path) -> None:
    """Create git repo + initial commit after template copy."""
    gitignore = sandbox / ".gitignore"
    if not gitignore.is_file():
        gitignore.write_text(EVAL_GITIGNORE)
    elif "node_modules" not in gitignore.read_text():
        gitignore.write_text(gitignore.read_text().rstrip() + "\n" + EVAL_GITIGNORE)

    _run(["git", "init"], sandbox)
    _run(["git", "config", "user.email", "eval@heyeddi.local"], sandbox)
    _run(["git", "config", "user.name", "HeyEddi Eval"], sandbox)
    _run(["git", "add", "-A"], sandbox)
    _run(["git", "commit", "-m", "eval baseline", "--allow-empty"], sandbox)


def diff_against_baseline(sandbox: Path) -> dict[str, str]:
    """Return diff stat and patch vs first commit."""
    _, stat = _run(["git", "diff", "--stat", "HEAD"], sandbox)
    _, patch = _run(["git", "diff", "HEAD"], sandbox)
    _, names = _run(["git", "diff", "--name-only", "HEAD"], sandbox)
    return {
        "stat": stat or "(no changes)",
        "patch": patch or "(no patch)",
        "files": names or "",
    }


def read_changed_sources(sandbox: Path) -> str:
    """Full text of changed source files for the judge (size-capped)."""
    _, names_raw = _run(["git", "diff", "--name-only", "HEAD"], sandbox)
    if not names_raw.strip():
        return "(no changed files)"

    parts: list[str] = []
    total = 0
    for rel in names_raw.splitlines():
        rel = rel.strip()
        if not rel or rel.startswith(".agents/") or rel.startswith(".cursor/"):
            continue
        path = sandbox / rel
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in TEXT_SUFFIXES and suffix:
            parts.append(f"\n### {rel}\n(binary or skipped suffix)\n")
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if len(data) > MAX_FILE_BYTES:
            text = data[:MAX_FILE_BYTES].decode("utf-8", errors="replace")
            text += f"\n… [truncated at {MAX_FILE_BYTES} bytes]"
        else:
            text = data.decode("utf-8", errors="replace")
        block = f"\n### {rel}\n```\n{text}\n```\n"
        if total + len(block) > MAX_TOTAL_BYTES:
            parts.append("\n… [remaining files omitted — diff too large]\n")
            break
        parts.append(block)
        total += len(block)
    return "".join(parts) if parts else "(no readable changed files)"
