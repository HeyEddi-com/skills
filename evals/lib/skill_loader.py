"""Load skill instructions and tools from skills/<name>/."""
from __future__ import annotations

import json
import re
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)


def load_skill_context(hub_root: Path, skill_name: str) -> dict:
    skill_dir = hub_root / "skills" / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"Skill not found: {skill_name}")

    text = skill_md.read_text()
    frontmatter: dict[str, str] = {}
    body = text
    m = FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                frontmatter[k.strip()] = v.strip()
        body = m.group(2).strip()

    context_parts: list[str] = []
    ctx_dir = skill_dir / "context"
    if ctx_dir.is_dir():
        for md in sorted(ctx_dir.glob("*.md")):
            context_parts.append(f"## {md.name}\n\n{md.read_text()}")

    manifest: dict = {"tools": []}
    manifest_path = skill_dir / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())

    return {
        "name": skill_name,
        "dir": str(skill_dir),
        "frontmatter": frontmatter,
        "instructions": body,
        "context": "\n\n".join(context_parts),
        "manifest": manifest,
    }


def build_system_prompt(hub_root: Path, skill_names: list[str]) -> str:
    blocks: list[str] = [
        "You are executing a skill evaluation. Follow the skill instructions exactly.",
        "You may edit files in the project workspace. Run skill scripts when instructed.",
    ]
    for name in skill_names:
        ctx = load_skill_context(hub_root, name)
        blocks.append(f"# Skill: {name}\n\n{ctx['instructions']}")
        if ctx["context"]:
            blocks.append(ctx["context"])
    return "\n\n---\n\n".join(blocks)
