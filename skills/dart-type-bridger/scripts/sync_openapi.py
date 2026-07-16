#!/usr/bin/env python3
"""Sync local OpenAPI schema to Dart model stubs under lib/models/.

Security: reads only a local file under the project root. Never fetches remote
URLs (avoids SSRF / third-party content in agent context). Agents must place
``openapi.json`` on disk first (scaffold, export, or curl to a file).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, resolve_project_root


def resolve_openapi_path(root: Path, relative: str) -> Path | None:
    """Return an openapi file path if it exists and stays under project root."""
    if "://" in relative:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate


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
            lines.append(
                f"      {prop}: json['{prop}'] != null ? DateTime.parse(json['{prop}'] as String) : null,"
            )
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
    parser = argparse.ArgumentParser(
        description="Sync local openapi.json to Dart models (no network fetch)"
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument(
        "--openapi",
        default="openapi.json",
        help="Path relative to project root (default: openapi.json)",
    )
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    openapi_path = resolve_openapi_path(root, args.openapi)
    if openapi_path is None:
        emit(
            json.dumps(
                {
                    "error": "no local openapi file",
                    "hint": (
                        "Place OpenAPI JSON at openapi.json (or pass --openapi <relpath>). "
                        "Do not fetch URLs inside this skill — export from FastAPI or: "
                        "curl -fsS http://127.0.0.1:8090/openapi.json -o openapi.json"
                    ),
                },
                indent=2,
            )
        )
        return

    try:
        spec = json.loads(openapi_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        emit(json.dumps({"error": f"invalid openapi JSON: {exc}", "source": str(openapi_path)}, indent=2))
        return

    schemas = spec.get("components", {}).get("schemas", {})
    out_dir = root / "lib" / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "api_models.dart"

    parts = [
        "// Generated stub from OpenAPI — refine types as needed.",
        f"// Source: {openapi_path.name}",
        "",
    ]
    written: list[str] = []
    for name, schema in list(schemas.items())[:40]:
        safe = re.sub(r"[^a-zA-Z0-9_]", "", name)
        if not safe:
            continue
        if schema.get("type") == "object" or "properties" in schema:
            parts.append(render_class(safe, schema))
            parts.append("")
            written.append(safe)

    out_file.write_text("\n".join(parts))

    emit(
        json.dumps(
            {
                "source": str(openapi_path.relative_to(root)),
                "schema_count": len(schemas),
                "written": str(out_file.relative_to(root)),
                "interfaces": written,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
