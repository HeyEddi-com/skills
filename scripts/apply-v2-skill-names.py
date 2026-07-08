#!/usr/bin/env python3
"""Bulk-apply v2 canonical skill names across hub (excludes evals/runs sandboxes)."""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALIASES_FILE = REPO_ROOT / "scripts" / "skill-name-aliases.json"

SKIP_PARTS = {".git", "node_modules", "__pycache__", "evals/runs"}
PROTECT_TOKEN = "design-handoff-flutter"

INCLUDE_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".toml", ".sh", ".txt"}


def load_aliases() -> dict[str, str]:
    data = json.loads(ALIASES_FILE.read_text(encoding="utf-8"))
    return dict(data["aliases"])


def should_process(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if any(part in rel.split("/") for part in ("evals/runs", ".git", "node_modules", "__pycache__")):
        return False
    if path.suffix not in INCLUDE_SUFFIXES and path.name not in ("skills-registry.json",):
        return False
    return True


def ordered_replacements(aliases: dict[str, str]) -> list[tuple[str, str]]:
    pairs = sorted(aliases.items(), key=lambda item: len(item[0]), reverse=True)
    return pairs


def transform(text: str, aliases: dict[str, str]) -> str:
    text = text.replace("design-handoff-flutter", PROTECT_TOKEN)
    for old, new in ordered_replacements(aliases):
        text = text.replace(f"@{old}", f"@{new}")
        text = text.replace(old, new)
    text = text.replace(PROTECT_TOKEN, "design-handoff-flutter")
    return text


def update_canonical_frontmatter(skill_dir: Path, canonical_name: str) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return
    text = skill_md.read_text(encoding="utf-8")
    text = re.sub(r"^name: .*$", f"name: {canonical_name}", text, count=1, flags=re.M)
    skill_md.write_text(text, encoding="utf-8")

    manifest = skill_dir / "manifest.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["skill"] = canonical_name
        data.pop("alias_of", None)
        data.pop("deprecated", None)
        manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    aliases = load_aliases()
    canonical_names = set(aliases.values())

    for name in canonical_names:
        update_canonical_frontmatter(REPO_ROOT / "skills" / name, name)

    changed = 0
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or not should_process(path):
            continue
        if path == ALIASES_FILE:
            continue
        if path.is_relative_to(REPO_ROOT / "skills") and any(
            path.is_relative_to(REPO_ROOT / "skills" / alias) for alias in aliases
        ):
            # Skip alias stub files — bootstrap manages those
            if path.name in ("SKILL.md", "manifest.json"):
                continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = transform(original, aliases)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(REPO_ROOT)}")

    print(f"done — {changed} files updated")


if __name__ == "__main__":
    main()
