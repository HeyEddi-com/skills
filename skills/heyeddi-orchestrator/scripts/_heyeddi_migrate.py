"""Migrate `.heyeddi/` artifacts from deprecated v1 skill names to v2 canonical names."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROTECT_TOKEN = "__DESIGN_HANDOFF_FLUTTER__"
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}
SYNC_STATE = "sync-state.json"


def find_aliases_file(hub_root: Path | None, skill_dir: Path | None) -> Path | None:
    candidates: list[Path] = []
    if hub_root:
        candidates.extend(
            [
                hub_root / "scripts" / "skill-name-aliases.json",
                hub_root / "skills-registry.json",
            ]
        )
    if skill_dir:
        candidates.append(skill_dir.parent / "reference" / "skill-name-aliases.json")
        candidates.append(skill_dir / ".." / "reference" / "skill-name-aliases.json")
    for path in candidates:
        resolved = path.resolve()
        if resolved.is_file():
            return resolved
    return None


def load_aliases(hub_root: Path | None = None, skill_dir: Path | None = None) -> tuple[str, dict[str, str]]:
    path = find_aliases_file(hub_root, skill_dir)
    if not path:
        return "0", {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if "aliases" in data and isinstance(data["aliases"], dict):
        version = str(data.get("version", "2.0.0"))
        return version, {str(k): str(v) for k, v in data["aliases"].items()}
    # skills-registry.json fallback
    return str(data.get("version", "2.0.0")), {str(k): str(v) for k, v in data.get("aliases", {}).items()}


def resolve_canonical(name: str, aliases: dict[str, str]) -> str:
    return aliases.get(name, name)


def transform_text(text: str, aliases: dict[str, str]) -> str:
    text = text.replace("design-handoff-flutter", PROTECT_TOKEN)
    for old, new in sorted(aliases.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(f"@{old}", f"@{new}")
        text = text.replace(old, new)
    return text.replace(PROTECT_TOKEN, "design-handoff-flutter")


def _migrate_routing(data: dict[str, Any], aliases: dict[str, str]) -> bool:
    changed = False
    for route in data.get("routes") or []:
        if not isinstance(route, dict):
            continue
        skill = route.get("skill")
        if isinstance(skill, str):
            canonical = resolve_canonical(skill, aliases)
            if canonical != skill:
                route["skill"] = canonical
                changed = True
    post = data.get("post_intake") or []
    if isinstance(post, list):
        new_post: list[str] = []
        for item in post:
            if not isinstance(item, str):
                new_post.append(item)
                continue
            updated = transform_text(item, aliases)
            if updated != item:
                changed = True
            new_post.append(updated)
        data["post_intake"] = new_post
    scaffold = data.get("scaffold") or []
    if isinstance(scaffold, list):
        new_scaffold: list[str] = []
        for item in scaffold:
            if not isinstance(item, str):
                new_scaffold.append(item)
                continue
            parts = item.split()
            if parts:
                parts[0] = resolve_canonical(parts[0], aliases)
            updated = " ".join(parts)
            if updated != item:
                changed = True
            new_scaffold.append(updated)
        data["scaffold"] = new_scaffold
    return changed


def _migrate_skills_index(data: dict[str, Any], aliases: dict[str, str]) -> bool:
    changed = False
    skills = data.get("skills")
    if not isinstance(skills, list):
        return False
    for entry in skills:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if isinstance(name, str):
            canonical = resolve_canonical(name, aliases)
            if canonical != name:
                entry["name"] = canonical
                entry["invoke_as"] = f"@{canonical}"
                changed = True
    return changed


def migrate_json_file(path: Path, aliases: dict[str, str]) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    rel = path.as_posix()
    changed = False
    if path.name == "skill-routing.json":
        changed = _migrate_routing(data, aliases)
    elif path.name == "skills-index.json":
        changed = _migrate_skills_index(data, aliases)
    else:
        text = json.dumps(data, indent=2) + "\n"
        updated = transform_text(text, aliases)
        if updated != text:
            data = json.loads(updated)
            changed = True
    if not changed:
        return False
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def migrate_text_file(path: Path, aliases: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = transform_text(original, aliases)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def routing_has_legacy_names(project_root: Path, aliases: dict[str, str]) -> bool:
    routing = project_root / ".heyeddi" / "docs" / "intake" / "skill-routing.json"
    if not routing.is_file():
        return False
    try:
        data = json.loads(routing.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    for route in data.get("routes") or []:
        skill = route.get("skill") if isinstance(route, dict) else None
        if skill in aliases:
            return True
    for item in data.get("post_intake") or []:
        if isinstance(item, str) and any(old in item for old in aliases):
            return True
    return False


def load_sync_state(heyeddi: Path) -> dict[str, Any]:
    path = heyeddi / SYNC_STATE
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_sync_state(heyeddi: Path, payload: dict[str, Any]) -> None:
    heyeddi.mkdir(parents=True, exist_ok=True)
    (heyeddi / SYNC_STATE).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def migrate_heyeddi(
    project_root: Path,
    *,
    hub_root: Path | None = None,
    skill_dir: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """Update `.heyeddi/` skill name references to v2 canonical names."""
    heyeddi = project_root / ".heyeddi"
    if not heyeddi.is_dir():
        return {
            "status": "skip",
            "reason": "no .heyeddi/ folder",
            "project_root": str(project_root),
        }

    version, aliases = load_aliases(hub_root, skill_dir)
    if not aliases:
        return {
            "status": "skip",
            "reason": "no skill name aliases configured",
            "project_root": str(project_root),
        }

    state = load_sync_state(heyeddi)
    already = state.get("skill_names_version") == version and not routing_has_legacy_names(project_root, aliases)
    if already and not force:
        return {
            "status": "ok",
            "reason": "already at skill_names_version",
            "skill_names_version": version,
            "project_root": str(project_root),
            "files_changed": 0,
            "paths": [],
        }

    changed_paths: list[str] = []
    for path in sorted(heyeddi.rglob("*")):
        if not path.is_file():
            continue
        if path.name == SYNC_STATE:
            continue
        if path.suffix not in TEXT_SUFFIXES:
            continue
        rel = str(path.relative_to(project_root))
        if dry_run:
            original = path.read_text(encoding="utf-8")
            if path.suffix == ".json":
                try:
                    data = json.loads(original)
                    probe = json.dumps(data, indent=2)
                    if path.name == "skill-routing.json":
                        if _migrate_routing(data, aliases):
                            changed_paths.append(rel)
                        continue
                    if path.name == "skills-index.json":
                        if _migrate_skills_index(data, aliases):
                            changed_paths.append(rel)
                        continue
                except json.JSONDecodeError:
                    pass
            if transform_text(original, aliases) != original:
                changed_paths.append(rel)
            continue

        if path.suffix == ".json":
            if migrate_json_file(path, aliases):
                changed_paths.append(rel)
        elif migrate_text_file(path, aliases):
            changed_paths.append(rel)

    result = {
        "status": "ok",
        "skill_names_version": version,
        "project_root": str(project_root),
        "dry_run": dry_run,
        "files_changed": len(changed_paths),
        "paths": changed_paths,
    }

    if not dry_run:
        write_sync_state(
            heyeddi,
            {
                "skill_names_version": version,
                "migrated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "files_updated": changed_paths,
                "aliases_applied": aliases,
            },
        )
        log_dir = heyeddi / "docs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"skill-name-migration-{version}.json"
        log_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        result["log"] = str(log_path.relative_to(project_root))

    return result
