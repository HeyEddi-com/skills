"""sync_openapi must not fetch remote URLs."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load(skill: str):
    path = REPO / "skills" / skill / "scripts" / "sync_openapi.py"
    spec = importlib.util.spec_from_file_location(f"{skill}_sync_openapi", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_backend_rejects_url_shaped_openapi(tmp_path: Path) -> None:
    mod = _load("backend-type-bridger")
    assert mod.resolve_openapi_path(tmp_path, "http://evil.example/openapi.json") is None
    assert mod.resolve_openapi_path(tmp_path, "../outside.json") is None


def test_dart_rejects_url_shaped_openapi(tmp_path: Path) -> None:
    mod = _load("dart-type-bridger")
    assert mod.resolve_openapi_path(tmp_path, "https://evil.example/openapi.json") is None


def test_backend_sync_local_only(tmp_path: Path) -> None:
    openapi = {
        "openapi": "3.0.0",
        "paths": {},
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {"id": {"type": "string"}, "email": {"type": "string"}},
                }
            }
        },
    }
    (tmp_path / "openapi.json").write_text(json.dumps(openapi), encoding="utf-8")
    mod = _load("backend-type-bridger")
    # Simulate argv via main would need monkeypatch; call resolve + generation path
    path = mod.resolve_openapi_path(tmp_path, "openapi.json")
    assert path is not None
    assert path.name == "openapi.json"


def test_no_urllib_in_sync_openapi_sources() -> None:
    for skill in ("backend-type-bridger", "dart-type-bridger"):
        text = (REPO / "skills" / skill / "scripts" / "sync_openapi.py").read_text(encoding="utf-8")
        assert "urllib" not in text
        assert "urlopen" not in text
        assert "--url" not in text
