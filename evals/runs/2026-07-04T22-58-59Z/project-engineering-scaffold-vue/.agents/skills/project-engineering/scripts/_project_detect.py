"""Detect HeyEddi project stacks (Vue, FastAPI, Firebase)."""
from __future__ import annotations

import json
from pathlib import Path

BACKEND_DIR = "backend"


def load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def load_stack_config(root: Path) -> dict:
    cfg = load_json(root / ".heyeddi" / "stack.json")
    return cfg or {}


def has_vue(root: Path) -> bool:
    pkg = load_json(root / "package.json")
    if pkg:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "vue" in deps:
            return True
    return (root / "src").is_dir() and (root / "package.json").is_file()


def has_fastapi(root: Path) -> bool:
    for base in (root / BACKEND_DIR, root):
        pyproject = base / "pyproject.toml"
        if pyproject.is_file() and "fastapi" in pyproject.read_text().lower():
            return True
        if (base / "app" / "main.py").is_file():
            return True
    return (root / "openapi.json").is_file() and (root / BACKEND_DIR).is_dir()


def has_firebase(root: Path) -> bool:
    if (root / "firebase.json").is_file():
        return True
    if (root / "firestore.rules").is_file():
        return True
    cfg = load_stack_config(root)
    return cfg.get("backend") == "firebase"


def fastapi_root(root: Path) -> Path:
    if (root / BACKEND_DIR / "pyproject.toml").is_file():
        return root / BACKEND_DIR
    if (root / "pyproject.toml").is_file() and "fastapi" in (root / "pyproject.toml").read_text().lower():
        return root
    return root / BACKEND_DIR


def infer_backends(root: Path) -> list[str]:
    cfg = load_stack_config(root)
    declared = cfg.get("backends") or cfg.get("backend")
    if isinstance(declared, str):
        declared = [declared]
    if isinstance(declared, list):
        return [b for b in declared if b in ("fastapi", "firebase")]

    backends: list[str] = []
    product = root / "PRODUCT.md"
    text = product.read_text().lower() if product.is_file() else ""
    if has_fastapi(root) or "fastapi" in text or (root / "openapi.json").is_file():
        backends.append("fastapi")
    if has_firebase(root) or "firebase" in text or "firestore" in text:
        backends.append("firebase")
    return backends


def detect(root: Path) -> dict:
    cfg = load_stack_config(root)
    vue = has_vue(root)
    backends = infer_backends(root)
    return {
        "vue": vue,
        "fastapi": "fastapi" in backends or has_fastapi(root),
        "firebase": "firebase" in backends or has_firebase(root),
        "backends": backends,
        "fastapi_root": str(fastapi_root(root)),
        "stack_config": str(root / ".heyeddi" / "stack.json") if cfg else None,
    }
