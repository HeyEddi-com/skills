#!/usr/bin/env python3
"""Audit project scaffold against HeyEddi engineering standards (Vue + backends)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _project_detect import BACKEND_DIR, detect, fastapi_root, has_fastapi, has_firebase, has_vue
from _skill_cli import emit, resolve_project_root

VUE_REQUIRED = (
    "package.json",
    "vite.config.ts",
    "vitest.config.ts",
    "tsconfig.json",
    "src/main.ts",
    "src/App.vue",
    "src/router/index.ts",
)

VUE_RECOMMENDED = ("DESIGN.md", "PRODUCT.md", "tests/unit/setup.ts", "src/env.d.ts")

FASTAPI_REQUIRED = (
    f"{BACKEND_DIR}/pyproject.toml",
    f"{BACKEND_DIR}/app/main.py",
    f"{BACKEND_DIR}/tests/test_health.py",
)

FASTAPI_RECOMMENDED = ("openapi.json",)

FIREBASE_REQUIRED = ("firebase.json", "firestore.rules")

FIREBASE_RECOMMENDED = (".firebaserc", "firestore.indexes.json", ".env.firebase.example")

PACKAGE_SCRIPTS = ("dev", "build", "test")


def _load_package(root: Path) -> dict | None:
    pkg = root / "package.json"
    if not pkg.is_file():
        return None
    try:
        return json.loads(pkg.read_text())
    except json.JSONDecodeError:
        return {"_parse_error": True}


def _audit_vue(root: Path) -> dict:
    missing_required: list[str] = []
    missing_recommended: list[str] = []
    warnings: list[str] = []

    for rel in VUE_REQUIRED:
        if not (root / rel).is_file():
            missing_required.append(rel)
    for rel in VUE_RECOMMENDED:
        if not (root / rel).is_file():
            missing_recommended.append(rel)

    pkg = _load_package(root)
    if pkg and isinstance(pkg, dict) and "_parse_error" not in pkg:
        for name in PACKAGE_SCRIPTS:
            script = pkg.get("scripts", {}).get(name, "")
            if name not in pkg.get("scripts", {}):
                missing_required.append(f"package.json scripts.{name}")
            elif str(script).strip().startswith("echo "):
                warnings.append(f"scripts.{name} is a stub: run scaffold_stack --stack vue")

    if pkg and not (root / "node_modules").is_dir():
        warnings.append("node_modules missing: run ensure_npm")

    status = "ok" if not missing_required else "incomplete"
    if status == "ok" and (warnings or missing_recommended):
        status = "needs_attention"

    return {
        "status": status,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "warnings": warnings,
    }


def _audit_fastapi(root: Path) -> dict:
    missing_required: list[str] = []
    missing_recommended: list[str] = []
    warnings: list[str] = []

    for rel in FASTAPI_REQUIRED:
        if not (root / rel).is_file():
            missing_required.append(rel)
    for rel in FASTAPI_RECOMMENDED:
        if not (root / rel).is_file():
            missing_recommended.append(rel)

    api = fastapi_root(root)
    if not (api / ".venv").is_dir() and not list(api.glob("**/site-packages")):
        warnings.append("Python venv/deps may be missing: run ensure_python")

    status = "ok" if not missing_required else "incomplete"
    return {
        "status": status,
        "backend_root": str(api),
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "warnings": warnings,
    }


def _audit_firebase(root: Path) -> dict:
    missing_required: list[str] = []
    missing_recommended: list[str] = []
    warnings: list[str] = []

    for rel in FIREBASE_REQUIRED:
        if not (root / rel).is_file():
            missing_required.append(rel)
    for rel in FIREBASE_RECOMMENDED:
        if not (root / rel).is_file():
            missing_recommended.append(rel)

    status = "ok" if not missing_required else "incomplete"
    return {
        "status": status,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "warnings": warnings,
    }


def audit(root: Path) -> dict:
    stacks = detect(root)
    layers: dict = {"detected": stacks}
    next_steps: list[str] = []

    if stacks["vue"] or has_vue(root) or (root / "package.json").is_file():
        layers["vue"] = _audit_vue(root)
        if layers["vue"]["status"] != "ok":
            next_steps.append("scaffold_stack --stack vue")

    if stacks["fastapi"] or has_fastapi(root):
        layers["fastapi"] = _audit_fastapi(root)
        if layers["fastapi"]["status"] != "ok":
            next_steps.append("scaffold_stack --stack fastapi")

    if stacks["firebase"] or has_firebase(root):
        layers["firebase"] = _audit_firebase(root)
        if layers["firebase"]["status"] != "ok":
            next_steps.append("scaffold_stack --stack firebase")

    if not next_steps and stacks["backends"]:
        next_steps.append("Set .heyeddi/stack.json backends: fastapi | firebase | both")

    statuses = [v["status"] for k, v in layers.items() if k != "detected" and isinstance(v, dict)]
    overall = "ok"
    if any(s == "incomplete" for s in statuses):
        overall = "incomplete"
    elif any(s == "needs_attention" for s in statuses):
        overall = "needs_attention"

    return {
        "project_root": str(root),
        "status": overall,
        "layers": layers,
        "next_steps": next_steps or ["dev_server_info for local URLs"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit HeyEddi project scaffold")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    emit(json.dumps(audit(root), indent=2))


if __name__ == "__main__":
    main()
