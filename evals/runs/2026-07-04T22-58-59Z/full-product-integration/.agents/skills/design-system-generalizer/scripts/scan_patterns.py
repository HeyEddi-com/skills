#!/usr/bin/env python3
"""Scan token, component, and layout patterns from a golden route."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from _skill_cli import emit, resolve_project_root

TOKEN_RE = re.compile(r"var\(--[a-z0-9-]+\)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
IMPORT_RE = re.compile(r"from ['\"]([^'\"]+)['\"]")
PRIMEVUE_RE = re.compile(r"from ['\"]primevue/([^'\"]+)['\"]")
CLASS_RE = re.compile(r"class=\"([^\"]+)\"|:class=\"[^\"]*['\"]([^'\"]+)['\"]")
DEEP_RE = re.compile(r":deep\(\.([a-z0-9_-]+)\)")


def vue_files_for_route(root: Path, route: str) -> list[Path]:
    slug = route.strip("/").replace("/", "-") or "home"
    candidates: list[Path] = []
    for pattern in (
        f"**/views/**/*{slug}*",
        f"**/pages/**/*{slug}*",
        f"**/components/**/*{slug}*",
    ):
        candidates.extend(root.glob(pattern))
    # Settings special-case
    if slug == "settings":
        candidates.extend(root.glob("**/SettingsView.vue"))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        if path.suffix == ".vue" and path not in seen:
            seen.add(path)
            unique.append(path)
    return unique[:20]


def scan_file(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    tokens = TOKEN_RE.findall(text)
    classes: list[str] = []
    for match in CLASS_RE.finditer(text):
        classes.extend((match.group(1) or match.group(2) or "").split())
    return {
        "path": str(path.relative_to(root)),
        "openprops_tokens": sorted(set(tokens)),
        "token_counts": dict(Counter(tokens)),
        "hex_colors": sorted(set(HEX_RE.findall(text))),
        "primevue_components": sorted(set(PRIMEVUE_RE.findall(text))),
        "utility_classes": sorted({c for c in classes if c and ("__" in c or c.startswith("card-"))}),
        "deep_overrides": sorted(set(DEEP_RE.findall(text))),
        "imports": sorted(set(IMPORT_RE.findall(text)))[:40],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan design patterns on a golden route")
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    files = vue_files_for_route(root, args.route)
    if not files:
        emit(
            json.dumps(
                {
                    "route": args.route,
                    "files": [],
                    "hint": "No matching Vue files — check route slug or views/ naming",
                },
                indent=2,
            )
        )
        return

    file_reports = [scan_file(f, root) for f in files]
    all_tokens: Counter[str] = Counter()
    all_components: set[str] = set()
    all_utilities: set[str] = set()
    for report in file_reports:
        all_tokens.update(report.get("token_counts") or {})
        all_components.update(report.get("primevue_components") or [])
        all_utilities.update(report.get("utility_classes") or [])

    emit(
        json.dumps(
            {
                "route": args.route,
                "golden": True,
                "files": file_reports,
                "summary": {
                    "token_count": len(all_tokens),
                    "top_tokens": [t for t, _ in all_tokens.most_common(15)],
                    "primevue_components": sorted(all_components),
                    "utility_classes": sorted(all_utilities),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
