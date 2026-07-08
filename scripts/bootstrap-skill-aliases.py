#!/usr/bin/env python3
"""Create deprecated alias skill folders that symlink canonical scripts/context."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
ALIASES_FILE = REPO_ROOT / "scripts" / "skill-name-aliases.json"

ALIAS_SKILL_MD = """---
name: {alias}
description: Deprecated alias for @{canonical}. Use @{canonical} — renamed in v2.0.0.
disable-model-invocation: true
deprecated: true
canonical: {canonical}
---

# {alias} (deprecated)

**Renamed to `@{canonical}` in HeyEddi Skills v2.0.0.**

When this alias is invoked:

1. Read and follow **`{canonical}/SKILL.md`** from the same skills install root.
2. Do not write new docs or routing JSON using `{alias}`.

This folder exists for backward compatibility only. It will be removed in v3.0.0.
"""


def load_aliases() -> dict[str, str]:
    data = json.loads(ALIASES_FILE.read_text(encoding="utf-8"))
    return dict(data["aliases"])


def symlink_or_copy(src: Path, dest: Path) -> None:
    if dest.is_symlink() or dest.exists():
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        elif dest.is_dir():
            shutil.rmtree(dest)
    rel = os.path.relpath(src, dest.parent)
    dest.symlink_to(rel, target_is_directory=src.is_dir())


def main() -> None:
    aliases = load_aliases()
    for alias, canonical in aliases.items():
        alias_dir = SKILLS_DIR / alias
        canonical_dir = SKILLS_DIR / canonical
        if not canonical_dir.is_dir():
            raise SystemExit(f"missing canonical skill: {canonical_dir}")

        alias_dir.mkdir(parents=True, exist_ok=True)
        (alias_dir / "SKILL.md").write_text(
            ALIAS_SKILL_MD.format(alias=alias, canonical=canonical),
            encoding="utf-8",
        )

        manifest_src = canonical_dir / "manifest.json"
        if manifest_src.is_file():
            manifest = json.loads(manifest_src.read_text(encoding="utf-8"))
            manifest["skill"] = alias
            manifest["alias_of"] = canonical
            manifest["deprecated"] = True
            (alias_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        for sub in ("scripts", "context", "reference", "fixtures"):
            src = canonical_dir / sub
            dest = alias_dir / sub
            if src.is_dir():
                symlink_or_copy(src, dest)

        print(f"alias {alias} -> {canonical}")


if __name__ == "__main__":
    main()
