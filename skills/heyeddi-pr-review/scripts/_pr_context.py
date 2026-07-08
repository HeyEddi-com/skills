"""Shared PR context helpers for heyeddi-pr-review scripts."""
from __future__ import annotations

import json
from pathlib import Path

from _heyeddi_paths import pr_context_cache
from _skill_cli import fail


UI_EXTENSIONS = {".vue", ".css", ".scss"}
API_PREFIXES = ("backend/", "app/", "src/composables/", "src/services/")
DOC_PATHS = (".heyeddi/product.md", ".heyeddi/design.md", "product.md", "design.md")
TEST_MARKERS = (".spec.", ".test.", "_test.py", "test_")


def load_fixture(root: Path, fixture_arg: str, pr: int) -> dict:
    fixture_path = Path(fixture_arg)
    if not fixture_path.is_absolute():
        fixture_path = root / fixture_path
    if not fixture_path.is_file():
        return {"error": "fixture not found", "path": str(fixture_path)}
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    if "pr" not in data:
        data["pr"] = pr
    return data


def load_context(root: Path, pr: int, context_arg: str | None, fixture: str | None) -> dict:
    if context_arg:
        path = Path(context_arg)
        if not path.is_absolute():
            path = root / path
        if not path.is_file():
            fail(f"context file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    cache = pr_context_cache(root, pr)
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))

    if fixture:
        payload = load_fixture(root, fixture, pr)
        if "error" in payload:
            fail(payload["error"])
        return payload

    fail("Provide --context, --fixture, or run fetch_pr_context --write-cache first")


def categorize_file(path: str) -> list[str]:
    tags: list[str] = []
    lower = path.lower()
    suffix = Path(path).suffix.lower()
    if suffix in UI_EXTENSIONS or "/views/" in lower or "/components/" in lower:
        tags.append("ui")
    if any(lower.startswith(p) or f"/{p}" in lower for p in API_PREFIXES) or lower.endswith(".py"):
        if "test" not in lower:
            tags.append("api")
    if any(doc in lower for doc in DOC_PATHS) or lower.startswith(".heyeddi/docs/"):
        tags.append("docs")
    if any(marker in lower for marker in TEST_MARKERS):
        tags.append("tests")
    return tags or ["other"]


def routes_from_files(files: list[str]) -> list[str]:
    routes: list[str] = []
    for path in files:
        name = Path(path).stem.lower()
        if "login" in name:
            routes.append("/login")
        elif "settings" in name:
            routes.append("/settings")
        elif "dashboard" in name:
            routes.append("/dashboard")
        elif "home" in name or name == "index":
            routes.append("/")
        elif "users" in name and "composable" in path.lower():
            routes.append("/dashboard")
    return list(dict.fromkeys(routes))
