#!/usr/bin/env python3
"""Verify complete @product-translator intake artifacts."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from _heyeddi_paths import canonical_product_path, designs_dir, intake_dir, product_md
from _product_schema import (
    load_json,
    product_json_path,
    validate_product_json,
    validate_product_md,
)
from _skill_cli import emit, resolve_project_root

# Baseline Vue shell files allowed on scaffolded repos — intake must not add feature UI.
ALLOWED_VUE_REL = frozenset(
    {
        Path("src/App.vue"),
    }
)


def _disallowed_vue(root: Path) -> list[str]:
    disallowed: list[str] = []
    src = root / "src"
    if not src.is_dir():
        return disallowed
    for path in src.rglob("*.vue"):
        rel = path.relative_to(root)
        if rel not in ALLOWED_VUE_REL:
            disallowed.append(str(rel))
    return sorted(disallowed)


def _check_repo_buildable(root: Path) -> tuple[bool, str]:
    if not (root / "package.json").is_file():
        return True, "no package.json — skip build gate"
    if not (root / "node_modules").is_dir():
        return True, "node_modules missing — skip build gate"
    try:
        proc = subprocess.run(
            ["npm", "run", "build"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"npm run build failed: {exc}"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip()[-600:]
        return False, tail or f"exit {proc.returncode}"
    return True, "npm run build exit 0"


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify product-translator intake")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true", help="Exit 1 if any check fails")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    issues: list[str] = []
    checks: list[dict] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            issues.append(f"{name}: {detail}")

    p_path = product_md(root) or canonical_product_path(root)
    if not p_path.is_file():
        record("product-md", False, "missing .heyeddi/product.md")
    else:
        text = p_path.read_text(errors="replace")
        ok, errs = validate_product_md(text)
        record("product-md-sections", ok, "; ".join(errs) if errs else "all required sections present")

    json_path = product_json_path(root)
    if not json_path.is_file():
        record("product-translation-json", False, f"missing {json_path.relative_to(root)}")
    else:
        data = load_json(json_path)
        ok, errs = validate_product_json(data)
        record("product-translation-json", ok, "; ".join(errs) if errs else "schema valid")

    intake = intake_dir(root)
    translations = list(intake.glob("translation-*.md"))
    record("translation-log", bool(translations), f"found {len(translations)} translation-*.md")

    routing_path = intake / "skill-routing.json"
    if not routing_path.is_file():
        record("skill-routing", False, "missing skill-routing.json")
    else:
        routing = load_json(routing_path)
        routes = routing.get("routes") or []
        record("skill-routing", len(routes) >= 1, f"{len(routes)} routes")
        if json_path.is_file():
            data = load_json(json_path)
            page_routes = {p["route"] for p in data.get("pages", []) if isinstance(p, dict) and p.get("route")}
            routed = {r["route"] for r in routes if isinstance(r, dict) and r.get("route")}
            missing = sorted(page_routes - routed)
            record("routing-coverage", not missing, f"missing routes: {missing}" if missing else "all pages routed")

    settings = designs_dir(root) / "settings"
    for artifact, label in (
        (settings / "desktop.png", "settings-desktop-png"),
        (settings / "mobile.png", "settings-mobile-png"),
        (settings / "mockup-brief.md", "settings-brief"),
        (settings / "handoff.json", "settings-handoff-json"),
    ):
        record(label, artifact.is_file(), str(artifact.relative_to(root)))

    brief = settings / "mockup-brief.md"
    if brief.is_file():
        btext = brief.read_text(errors="replace")
        record("brief-implementation-spec", "Implementation spec" in btext, "section present")
        record(
            "brief-audience",
            "## Audience" in btext and "Primary persona:" in btext and "_(missing" not in btext,
            "audience block filled from product.md",
        )

    disallowed_vue = _disallowed_vue(root)
    if disallowed_vue:
        record(
            "no-vue-implementation",
            False,
            f"feature Vue not allowed during intake: {', '.join(disallowed_vue)} "
            "(baseline src/App.vue shell only)",
        )
    else:
        record(
            "no-vue-implementation",
            True,
            "no feature views — baseline App.vue shell OK" if (root / "src/App.vue").is_file() else "no src/**/*.vue",
        )

    build_ok, build_detail = _check_repo_buildable(root)
    record("repo-buildable", build_ok, build_detail)

    result = {
        "ok": len(issues) == 0,
        "issue_count": len(issues),
        "issues": issues,
        "checks": checks,
    }
    emit(json.dumps(result, indent=2))

    if args.check and issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
