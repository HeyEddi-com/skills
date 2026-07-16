"""Keep `.heyeddi/` in sync automatically — no manual session-start command.

Security: loads ``_catalog.py`` only from the same skill install tree as this
file (sibling ``heyeddi-orchestrator/scripts``). Never uses ``sys.path``, never
reads ``HEYEDDI_*`` env roots, never scans the user home directory, and never
imports from a project-relative ``.agents`` / ``.cursor`` path that is not the
calling skill's own install tree.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_ENSURED: set[str] = set()
_CATALOG_MODULE = "heyeddi_orchestrator_catalog_secure"


def _allowed_orchestrator_scripts(_project_root: Path, here: Path) -> list[Path]:
    """Allowlist: only the skill-tree sibling (or this dir if we *are* orchestrator)."""
    here = here.resolve()
    candidates: list[Path] = []
    # Running from heyeddi-orchestrator/scripts itself
    if here.name == "scripts" and here.parent.name == "heyeddi-orchestrator":
        candidates.append(here)
    # Sibling install: <skills-root>/heyeddi-orchestrator/scripts
    sibling = (here.parent.parent / "heyeddi-orchestrator" / "scripts").resolve()
    if sibling not in candidates:
        candidates.append(sibling)

    allowed: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        catalog = path / "_catalog.py"
        if path.is_dir() and catalog.is_file():
            allowed.append(path)
    return allowed


def _orchestrator_scripts(project_root: Path) -> Path | None:
    here = Path(__file__).resolve().parent
    allowed = _allowed_orchestrator_scripts(project_root, here)
    return allowed[0] if allowed else None


def _load_catalog(scripts_dir: Path) -> ModuleType:
    """Load `_catalog.py` from an allowlisted directory via importlib (no sys.path)."""
    scripts_dir = scripts_dir.resolve()
    catalog_path = (scripts_dir / "_catalog.py").resolve()
    if not catalog_path.is_file():
        raise ImportError(f"orchestrator catalog missing: {catalog_path}")
    if catalog_path.parent != scripts_dir:
        raise ImportError("orchestrator catalog path escape blocked")

    existing = sys.modules.get(_CATALOG_MODULE)
    if existing is not None and getattr(existing, "__file__", None) == str(catalog_path):
        return existing

    spec = importlib.util.spec_from_file_location(_CATALOG_MODULE, catalog_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load orchestrator catalog: {catalog_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[_CATALOG_MODULE] = module
    spec.loader.exec_module(module)
    return module


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

    allowed = set(_allowed_orchestrator_scripts(project_root, Path(__file__).resolve().parent))
    if scripts not in allowed:
        return {"status": "skipped", "reason": "orchestrator scripts path not allowlisted"}

    if once_per_process:
        _ENSURED.add(key)

    catalog = _load_catalog(scripts)
    hub_root = catalog.find_hub_root(project_root)
    result: dict[str, Any] = {"status": "ok"}
    index_path = project_root / ".heyeddi" / "skills-index.json"
    if refresh_index and not index_path.is_file():
        result.update(catalog.write_skills_index(project_root, hub_root))
    return result
