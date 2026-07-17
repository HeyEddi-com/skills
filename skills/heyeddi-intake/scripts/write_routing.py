#!/usr/bin/env python3
"""Write skill-routing.json: which @skills run per route/feature."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import intake_dir
from _skill_cli import emit, fail, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Write downstream skill routing manifest")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", required=True, help="Routing manifest JSON (file path or inline)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    try:
        data = json.loads(args.json)
    except json.JSONDecodeError:
        json_path = Path(args.json)
        if not json_path.is_file():
            fail(f"invalid JSON and not a file path: {args.json[:120]}")
        data = json.loads(json_path.read_text())

    if "routes" not in data and "features" in data:
        data["routes"] = data.pop("features")

    dest = intake_dir(root) / "skill-routing.json"
    if args.dry_run:
        emit(json.dumps({"status": "dry_run", "path": str(dest)}, indent=2))
        return

    intake_dir(root).mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, indent=2) + "\n")
    emit(json.dumps({"status": "ok", "path": str(dest), "route_count": len(data.get("routes", []))}, indent=2))


if __name__ == "__main__":
    main()
