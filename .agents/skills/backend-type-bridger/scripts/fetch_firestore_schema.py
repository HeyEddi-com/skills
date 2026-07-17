#!/usr/bin/env python3
"""Read Firestore rules / schema hints — summary only (no raw schema dump)."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, resolve_project_root

COLLECTION_RE = re.compile(r"match\s+/([a-zA-Z0-9_/-]+)")


def _schema_summary(data: object) -> dict:
    """Emit structure metadata only — never full free-text field dumps."""
    if not isinstance(data, dict):
        return {"type": type(data).__name__}
    collections = data.get("collections") if isinstance(data.get("collections"), dict) else None
    if collections is not None:
        return {
            "collection_keys": sorted(str(k) for k in collections.keys())[:50],
            "collection_count": len(collections),
        }
    return {"top_level_keys": sorted(str(k) for k in data.keys())[:50]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Firestore schema hints")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    rules = root / "firestore.rules"
    schema = root / "firestore.schema.json"
    firebase_json = root / "firebase.json"
    result: dict = {"collections": [], "files_found": []}

    if rules.is_file():
        result["files_found"].append(str(rules.relative_to(root)))
        text = rules.read_text(encoding="utf-8", errors="replace")
        result["collections"] = sorted(set(COLLECTION_RE.findall(text)))
    if schema.is_file():
        result["files_found"].append(str(schema.relative_to(root)))
        try:
            result["schema_summary"] = _schema_summary(json.loads(schema.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            result["schema_error"] = str(exc)
    if firebase_json.is_file():
        result["files_found"].append(str(firebase_json.relative_to(root)))
        result["firebase_project"] = True

    if not result["files_found"]:
        result["hint"] = "No firestore.rules or firestore.schema.json — add Firebase config to project root"
    result["note"] = "schema_summary is structural only — read firestore.schema.json on disk for full schema"
    emit(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
