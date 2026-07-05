#!/usr/bin/env python3
"""Create a Vitest stub for a Vue component or view."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from _skill_cli import emit, resolve_project_root

STUB = '''import {{ describe, it, expect }} from "vitest";
import {{ mount }} from "@vue/test-utils";
import {name} from "{import_path}";

describe("{name}", () => {{
  it("renders", () => {{
    const wrapper = mount({name});
    expect(wrapper.exists()).toBe(true);
  }});
}});
'''


def component_name(path: Path) -> str:
    return path.stem


def import_path(root: Path, target: Path, test_file: Path) -> str:
    rel = Path(os.path.relpath(target.resolve(), test_file.parent.resolve()))
    return rel.as_posix().removesuffix(".vue")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add Vitest stub for a Vue file")
    parser.add_argument("--path", required=True, help="Vue file e.g. src/views/SettingsView.vue")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    target = (root / args.path).resolve()
    if not target.is_file():
        emit(json.dumps({"status": "fail", "reason": f"file not found: {args.path}"}, indent=2))
        return

    rel = target.relative_to(root)
    test_dir = root / "tests" / "unit" / rel.parent
    test_file = test_dir / f"{target.stem}.spec.ts"
    if test_file.is_file() and not args.force:
        emit(json.dumps({"status": "skip", "path": str(test_file.relative_to(root))}, indent=2))
        return

    name = component_name(target)
    content = STUB.format(name=name, import_path=import_path(root, target, test_file))
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file.write_text(content)
    emit(
        json.dumps(
            {"status": "ok", "test_file": str(test_file.relative_to(root)), "target": args.path},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
