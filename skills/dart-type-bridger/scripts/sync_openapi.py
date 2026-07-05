#!/usr/bin/env python3
"""Sync OpenAPI schema to Dart model stub."""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from _skill_cli import emit, resolve_project_root


def dart_type(openapi_type: str | None, fmt: str | None = None) -> str:
    if fmt == "date-time":
        return "DateTime"
    mapping = {
        "string": "String",
        "integer": "int",
        "number": "double",
        "boolean": "bool",
        "array": "List<dynamic>",
        "object": "Map<String, dynamic>",
    }
    return mapping.get(openapi_type or "object", "dynamic")


def render_class(name: str, schema: dict) -> str:
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    lines = [f"class {name} {{", f"  const {name}({{"]
    for prop, meta in props.items():
        t = dart_type(meta.get("type"), meta.get("format"))
        req = "required " if prop in required else ""
        lines.append(f"    {req}this.{prop},")
    lines.append("  });")
    lines.append("")
    for prop, meta in props.items():
        t = dart_type(meta.get("type"), meta.get("format"))
        lines.append(f"  final {t}? {prop};")
    lines.append("")
    lines.append(f"  factory {name}.fromJson(Map<String, dynamic> json) {{")
    lines.append(f"    return {name}(")
    for prop, meta in props.items():
        t = dart_type(meta.get("type"), meta.get("format"))
        if t == "DateTime":
            lines.append(f"      {prop}: json['{prop}'] != null ? DateTime.parse(json['{prop}'] as String) : null,")
        elif t == "int":
            lines.append(f"      {prop}: (json['{prop}'] as num?)?.toInt(),")
        elif t == "double":
            lines.append(f"      {prop}: (json['{prop}'] as num?)?.toDouble(),")
        else:
            lines.append(f"      {prop}: json['{prop}'] as {t}?,")
    lines.append("    );")
    lines.append("  }")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync OpenAPI to Dart models")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--url", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    local = root / "openapi.json"
    spec = None
    source = None

    if local.is_file():
        spec = json.loads(local.read_text())
        source = str(local)
    elif args.url:
        try:
            with urllib.request.urlopen(args.url, timeout=10) as resp:
                spec = json.loads(resp.read().decode())
            source = args.url
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            emit(json.dumps({"error": str(exc), "hint": "Start FastAPI or place openapi.json in project root"}, indent=2))
            return
    else:
        emit(
            json.dumps(
                {
                    "error": "no openapi source",
                    "hint": "Add openapi.json or pass --url http://localhost:8090/openapi.json",
                },
                indent=2,
            )
        )
        return

    schemas = spec.get("components", {}).get("schemas", {})
    out_dir = root / "lib" / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "api_models.dart"

    parts = [
        "// Generated stub from OpenAPI — refine types as needed.",
        "// Source: " + str(source),
        "",
    ]
    for name, schema in list(schemas.items())[:40]:
        safe = re.sub(r"[^a-zA-Z0-9_]", "", name)
        if not safe:
            continue
        if schema.get("type") == "object" or "properties" in schema:
            parts.append(render_class(safe, schema))
            parts.append("")

    content = "\n".join(parts)
    out_file.write_text(content)

    emit(
        json.dumps(
            {
                "source": source,
                "schema_count": len(schemas),
                "written": str(out_file),
                "sample_schemas": list(schemas.keys())[:20],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
