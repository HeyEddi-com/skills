"""Unit tests for hardened auto-sync allowlisting."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "skills" / "heyeddi-orchestrator" / "scripts"
PRODUCT_SCRIPTS = REPO_ROOT / "skills" / "heyeddi-product" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from _auto_sync import (  # noqa: E402
    _allowed_orchestrator_scripts,
    _load_catalog,
    _orchestrator_scripts,
    ensure_heyeddi,
)


def test_allowlist_excludes_home_env_and_foreign_project(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HEYEDDI_SKILLS_ROOT", str(tmp_path / "evil-hub"))
    (tmp_path / "evil-hub" / "skills" / "heyeddi-orchestrator" / "scripts").mkdir(parents=True)
    (tmp_path / "evil-hub" / "skills" / "heyeddi-orchestrator" / "scripts" / "_catalog.py").write_text(
        "def find_hub_root(x): return None\n", encoding="utf-8"
    )
    fake_home = tmp_path / "home"
    cursor_scripts = fake_home / ".cursor" / "skills" / "heyeddi-orchestrator" / "scripts"
    cursor_scripts.mkdir(parents=True)
    (cursor_scripts / "_catalog.py").write_text("x=1\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    # From product skill: only sibling orchestrator in the same skills tree
    allowed = _allowed_orchestrator_scripts(tmp_path, PRODUCT_SCRIPTS)
    assert allowed == [(PRODUCT_SCRIPTS.parent.parent / "heyeddi-orchestrator" / "scripts").resolve()]
    assert all("evil-hub" not in str(p) for p in allowed)

    # Project-local plant must NOT be loaded when calling skill is hub product
    project_scripts = tmp_path / ".agents" / "skills" / "heyeddi-orchestrator" / "scripts"
    project_scripts.mkdir(parents=True)
    (project_scripts / "_catalog.py").write_text(
        "def find_hub_root(x):\n    return None\n\ndef write_skills_index(a, b):\n    return {}\n",
        encoding="utf-8",
    )
    allowed2 = _allowed_orchestrator_scripts(tmp_path, PRODUCT_SCRIPTS)
    assert project_scripts.resolve() not in allowed2


def test_orchestrator_scripts_prefers_self() -> None:
    found = _orchestrator_scripts(REPO_ROOT)
    assert found is not None
    assert found == SCRIPTS.resolve()


def test_load_catalog_no_sys_path_pollution() -> None:
    before = list(sys.path)
    mod = _load_catalog(SCRIPTS.resolve())
    assert hasattr(mod, "write_skills_index")
    assert hasattr(mod, "find_hub_root")
    assert sys.path == before


def test_ensure_heyeddi_uses_install_tree_not_project_plant(tmp_path: Path) -> None:
    heyeddi = tmp_path / ".heyeddi"
    heyeddi.mkdir()
    (heyeddi / "skills-index.json").write_text('{"skills":[]}\n', encoding="utf-8")
    agents = tmp_path / ".agents" / "skills" / "heyeddi-orchestrator" / "scripts"
    agents.mkdir(parents=True)
    (agents / "_catalog.py").write_text(
        "def find_hub_root(project_root):\n"
        "    return None\n"
        "def write_skills_index(project_root, hub_root=None):\n"
        "    raise AssertionError('project plant must not run')\n",
        encoding="utf-8",
    )
    # ensure_heyeddi imported from hub orchestrator — uses hub catalog
    result = ensure_heyeddi(tmp_path, once_per_process=False)
    assert result is not None
    assert result.get("status") == "ok"


def test_no_sys_path_or_migrate_in_auto_sync_sources() -> None:
    text = (SCRIPTS / "_auto_sync.py").read_text(encoding="utf-8")
    assert "sys.path" not in text or "never mutates" in text.lower() or "no sys.path" in text
    assert "sys.path.insert" not in text
    assert "_heyeddi_migrate" not in text
    assert "HEYEDDI_SKILLS_ROOT" not in text
    assert "Path.home" not in text
