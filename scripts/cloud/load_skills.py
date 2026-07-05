#!/usr/bin/env python3
"""Discover skills under skills/ and load manifests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def find_skills_root(hub_root: Path) -> Path:
    return hub_root / "skills"


def load_skill(skill_dir: Path) -> dict[str, Any] | None:
    skill_md = skill_dir / "SKILL.md"
    manifest_path = skill_dir / "manifest.json"
    if not skill_md.is_file():
        return None

    manifest: dict[str, Any] = {"skill": skill_dir.name, "version": "0.0.0", "tools": []}
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())

    frontmatter: dict[str, str] = {}
    text = skill_md.read_text()
    if text.startswith("---"):
        _, fm, _ = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip()] = val.strip()

    return {
        "name": skill_dir.name,
        "path": str(skill_dir),
        "manifest": manifest,
        "frontmatter": frontmatter,
    }


def load_all_skills(hub_root: Path) -> list[dict[str, Any]]:
    root = find_skills_root(hub_root)
    skills: list[dict[str, Any]] = []
    if not root.is_dir():
        return skills
    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith("_"):
            loaded = load_skill(child)
            if loaded:
                skills.append(loaded)
    return skills


if __name__ == "__main__":
    import sys

    hub = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(json.dumps(load_all_skills(hub), indent=2))
