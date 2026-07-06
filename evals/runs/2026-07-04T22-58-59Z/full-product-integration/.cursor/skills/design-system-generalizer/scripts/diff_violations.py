#!/usr/bin/env python3
"""Diff target route patterns against a golden reference route."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, fail, resolve_project_root

TOKEN_RE = re.compile(r"var\(--[a-z0-9-]+\)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PRIMEVUE_RE = re.compile(r"from ['\"]primevue/([^'\"]+)['\"]")
CLASS_RE = re.compile(r"class=\"([^\"]+)\"|:class=\"[^\"]*['\"]([^'\"]+)['\"]")


def vue_files_for_route(root: Path, route: str) -> list[Path]:
    slug = route.strip("/").replace("/", "-") or "home"
    candidates: list[Path] = []
    for pattern in (
        f"**/views/**/*{slug}*",
        f"**/pages/**/*{slug}*",
        f"**/components/**/*{slug}*",
    ):
        candidates.extend(root.glob(pattern))
    if slug == "settings":
        candidates.extend(root.glob("**/SettingsView.vue"))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        if path.suffix == ".vue" and path not in seen:
            seen.add(path)
            unique.append(path)
    return unique[:20]


def aggregate_route(root: Path, route: str) -> dict:
    files = vue_files_for_route(root, route)
    tokens: set[str] = set()
    hex_colors: set[str] = set()
    components: set[str] = set()
    utilities: set[str] = set()
    scanned: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        scanned.append(str(path.relative_to(root)))
        tokens |= set(TOKEN_RE.findall(text))
        hex_colors |= set(HEX_RE.findall(text))
        components |= set(PRIMEVUE_RE.findall(text))
        for match in CLASS_RE.finditer(text):
            for cls in (match.group(1) or match.group(2) or "").split():
                if cls and ("__" in cls or cls.startswith("card-")):
                    utilities.add(cls)
    return {
        "route": route,
        "files": scanned,
        "tokens": tokens,
        "hex_colors": hex_colors,
        "primevue_components": components,
        "utility_classes": utilities,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Diff violations vs golden route")
    parser.add_argument("--golden", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true", help="Exit 1 when violations found")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    golden = aggregate_route(root, args.golden)
    target = aggregate_route(root, args.target)

    violations: list[dict] = []

    missing_tokens = sorted(golden["tokens"] - target["tokens"])
    if missing_tokens:
        violations.append(
            {
                "type": "missing_openprops_tokens",
                "severity": "warn",
                "values": missing_tokens[:20],
                "count": len(missing_tokens),
            }
        )

    extra_hex = sorted(target["hex_colors"] - golden["hex_colors"])
    if extra_hex:
        violations.append(
            {
                "type": "hex_color_not_on_golden",
                "severity": "error",
                "values": extra_hex,
            }
        )

    missing_components = sorted(golden["primevue_components"] - target["primevue_components"])
    if missing_components and golden["primevue_components"]:
        violations.append(
            {
                "type": "missing_primevue_components",
                "severity": "warn",
                "values": missing_components,
            }
        )

    missing_utilities = sorted(golden["utility_classes"] - target["utility_classes"])
    if missing_utilities:
        violations.append(
            {
                "type": "missing_utility_classes",
                "severity": "info",
                "values": missing_utilities[:15],
                "count": len(missing_utilities),
            }
        )

    if not target["files"]:
        violations.append(
            {
                "type": "target_route_not_found",
                "severity": "error",
                "values": [args.target],
            }
        )

    report = {
        "golden": args.golden,
        "target": args.target,
        "golden_summary": {
            "files": golden["files"],
            "token_count": len(golden["tokens"]),
            "primevue_components": sorted(golden["primevue_components"]),
        },
        "target_summary": {
            "files": target["files"],
            "token_count": len(target["tokens"]),
            "primevue_components": sorted(target["primevue_components"]),
        },
        "violations": violations,
        "ok": not any(v["severity"] == "error" for v in violations),
    }
    emit(json.dumps(report, indent=2))

    if args.check and not report["ok"]:
        fail(
            f"Design system diff failed for {args.target} vs golden {args.golden}: "
            + ", ".join(v["type"] for v in violations if v["severity"] == "error")
        )


if __name__ == "__main__":
    main()
