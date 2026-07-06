#!/usr/bin/env python3
"""Read Firestore rules / schema hints."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, resolve_project_root

COLLECTION_RE = re.compile(r"match\s+/([a-zA-Z0-9_/-]+)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Firestore schema hints")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    rules = root / "firestore.rules"
    schema = root / "firestore.schema.json"
    firebase_json = root / "firebase.json"
    result = {"collections": [], "files_found": [], "dart_hint": "lib/models/firestore_collections.dart"}

    if rules.is_file():
        result["files_found"].append(str(rules))
        text = rules.read_text()
        result["collections"] = sorted(set(COLLECTION_RE.findall(text)))
    if schema.is_file():
        result["files_found"].append(str(schema))
        try:
            result["schema"] = json.loads(schema.read_text())
        except json.JSONDecodeError as exc:
            result["schema_error"] = str(exc)
    if firebase_json.is_file():
        result["files_found"].append(str(firebase_json))

    if not result["files_found"]:
        result["hint"] = "No firestore.rules — add Firebase config or use FastAPI backend only"
    emit(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
