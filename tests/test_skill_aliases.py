"""Tests for v2 skill naming — aliases resolve to canonical names."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALIASES_FILE = REPO_ROOT / "scripts" / "skill-name-aliases.json"
SKILLS_DIR = REPO_ROOT / "skills"


def load_aliases() -> dict[str, str]:
    return json.loads(ALIASES_FILE.read_text(encoding="utf-8"))["aliases"]


def test_alias_folders_exist_with_symlinked_scripts():
    aliases = load_aliases()
    for alias, canonical in aliases.items():
        alias_dir = SKILLS_DIR / alias
        canonical_dir = SKILLS_DIR / canonical
        assert alias_dir.is_dir(), f"missing alias folder: {alias}"
        assert canonical_dir.is_dir(), f"missing canonical folder: {canonical}"
        assert (alias_dir / "SKILL.md").is_file()
        assert (alias_dir / "scripts").is_symlink() or (alias_dir / "scripts").is_dir()
        fm = (alias_dir / "SKILL.md").read_text(encoding="utf-8")
        assert f"name: {alias}" in fm
        assert f"canonical: {canonical}" in fm


def test_canonical_frontmatter_matches_folder():
    aliases = load_aliases()
    for canonical in set(aliases.values()):
        skill_md = SKILLS_DIR / canonical / "SKILL.md"
        manifest = SKILLS_DIR / canonical / "manifest.json"
        assert skill_md.is_file()
        text = skill_md.read_text(encoding="utf-8")
        assert f"name: {canonical}" in text
        if manifest.is_file():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            assert data["skill"] == canonical


def test_registry_aliases_match_file():
    registry = json.loads((REPO_ROOT / "skills-registry.json").read_text(encoding="utf-8"))
    assert registry.get("version") == "2.0.0"
    assert registry.get("aliases") == load_aliases()


def test_suggest_skills_resolves_routing_alias(tmp_path: Path):
    """skill-routing with v1 name resolves to canonical in suggest_skills output."""
    heyeddi = tmp_path / ".heyeddi" / "docs" / "intake"
    heyeddi.mkdir(parents=True)
    routing = {
        "routes": [{"route": "/settings", "skill": "design-handoff", "feature": "settings"}],
        "scaffold": ["project-engineering"],
    }
    (heyeddi / "skill-routing.json").write_text(json.dumps(routing), encoding="utf-8")

    import os

    script = SKILLS_DIR / "heyeddi-orchestrator" / "scripts" / "suggest_skills.py"
    env = os.environ.copy()
    env["HEYEDDI_SKILLS_ROOT"] = str(REPO_ROOT)
    result = subprocess.run(
        [sys.executable, str(script), "--project-root", str(tmp_path), "--user-prompt", "settings handoff"],
        capture_output=True,
        text=True,
        env=env,
        cwd=script.parent,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    skills = [item["skill"] for item in payload["suggestions"]]
    assert "heyeddi-handoff" in skills
    assert "design-handoff" not in skills


def test_migrate_heyeddi_updates_routing_json(tmp_path: Path):
    heyeddi = tmp_path / ".heyeddi" / "docs" / "intake"
    heyeddi.mkdir(parents=True)
    routing = {
        "routes": [{"route": "/settings", "skill": "design-handoff", "feature": "settings"}],
        "post_intake": ["@skill-orchestrator write_skills_index"],
        "scaffold": ["project-engineering"],
    }
    (heyeddi / "skill-routing.json").write_text(json.dumps(routing, indent=2), encoding="utf-8")

    sys.path.insert(0, str(SKILLS_DIR / "heyeddi-orchestrator" / "scripts"))
    from _heyeddi_migrate import migrate_heyeddi  # noqa: PLC0415

    result = migrate_heyeddi(tmp_path, hub_root=REPO_ROOT, skill_dir=SKILLS_DIR / "heyeddi-orchestrator" / "scripts")
    assert result["files_changed"] >= 1
    updated = json.loads((heyeddi / "skill-routing.json").read_text(encoding="utf-8"))
    assert updated["routes"][0]["skill"] == "heyeddi-handoff"
    assert "heyeddi-orchestrator" in updated["post_intake"][0]
    assert (tmp_path / ".heyeddi" / "sync-state.json").is_file()


def test_sync_dry_run():
    fixture = REPO_ROOT / "fixtures" / "sample-vue-app"
    script = SKILLS_DIR / "heyeddi-orchestrator" / "scripts" / "sync.py"
    import os

    env = os.environ.copy()
    env["HEYEDDI_SKILLS_ROOT"] = str(REPO_ROOT)
    result = subprocess.run(
        [sys.executable, str(script), "--project-root", str(fixture), "--dry-run", "--skip-workflow"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "heyeddi_migration" in payload
