"""Keep `.heyeddi/` in sync automatically — no manual session-start command."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_ENSURED: set[str] = set()


def _orchestrator_scripts(project_root: Path) -> Path | None:
    here = Path(__file__).resolve().parent
    if (here / "_catalog.py").is_file():
        return here

    candidates: list[Path] = []
    hub = os.environ.get("HEYEDDI_SKILLS_ROOT")
    if hub:
        candidates.append(Path(hub).resolve() / "skills" / "heyeddi-orchestrator" / "scripts")
    for base in (".agents/skills", ".cursor/skills"):
        candidates.append(project_root / base / "heyeddi-orchestrator" / "scripts")
    candidates.append(Path.home() / ".cursor" / "skills" / "heyeddi-orchestrator" / "scripts")
    candidates.append(here.parent.parent / "heyeddi-orchestrator" / "scripts")

    for path in candidates:
        if path.is_dir() and (path / "_catalog.py").is_file():
            return path
    return None


def ensure_heyeddi(
    project_root: Path,
    *,
    refresh_index: bool = True,
    once_per_process: bool = True,
) -> dict[str, Any] | None:
    """Refresh skills index when missing."""
    key = str(project_root.resolve())
    if once_per_process and key in _ENSURED:
        return None

    scripts = _orchestrator_scripts(project_root)
    if not scripts:
        return {"status": "skipped", "reason": "heyeddi-orchestrator not installed"}

    if once_per_process:
        _ENSURED.add(key)

    scripts_key = str(scripts)
    if scripts_key not in sys.path:
        sys.path.insert(0, scripts_key)

    from _catalog import find_hub_root, write_skills_index  # noqa: PLC0415

    hub_root = find_hub_root(project_root)
    result: dict[str, Any] = {"status": "ok"}
    index_path = project_root / ".heyeddi" / "skills-index.json"
    if refresh_index and not index_path.is_file():
        result.update(write_skills_index(project_root, hub_root))
    return result
