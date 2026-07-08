"""Load skill script modules without cross-skill `_heyeddi_paths` collisions."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).resolve().parent.parent

# Sibling script modules reused across skills share bare names — clear between loads.
_COLLIDING = frozenset(
    {
        "_heyeddi_paths",
        "_product_schema",
        "_skill_cli",
        "_contrast_math",
        "verify_intake",
        "verify_theme",
        "verify_handoff",
    }
)


def _clear_colliding_modules() -> None:
    for name in list(sys.modules):
        if name in _COLLIDING or name.startswith("heyeddi_skill_script."):
            del sys.modules[name]


def load_skill_script(skill: str, script: str) -> ModuleType:
    """Import `skills/<skill>/scripts/<script>.py` with an isolated import path."""
    scripts_dir = (REPO / "skills" / skill / "scripts").resolve()
    script_path = scripts_dir / f"{script}.py"
    if not script_path.is_file():
        raise FileNotFoundError(script_path)

    _clear_colliding_modules()
    inserted = str(scripts_dir)
    if inserted not in sys.path:
        sys.path.insert(0, inserted)
    elif sys.path[0] != inserted:
        sys.path.remove(inserted)
        sys.path.insert(0, inserted)

    unique_name = f"heyeddi_skill_script.{skill}.{script}"
    spec = importlib.util.spec_from_file_location(unique_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {script_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = mod
    spec.loader.exec_module(mod)
    return mod
