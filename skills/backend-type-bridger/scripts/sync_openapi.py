#!/usr/bin/env python3
"""Sync local OpenAPI schema to TypeScript types under src/types/api.ts.

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
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    # Refuse URL-shaped arguments that somehow landed in --openapi
    if "://" in relative:
        return None
    return candidate


def ts_type(openapi_type: str | None, fmt: str | None = None) -> str:
    if fmt == "date-time":
        return "string"
    if fmt == "uuid":
        return "string"
    mapping = {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "array": "unknown[]",
        "object": "Record<string, unknown>",
    }
    return mapping.get(openapi_type or "object", "unknown")


def render_interface(name: str, schema: dict) -> str:
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    lines = [f"export interface {name} {{"]
    for prop, meta in props.items():
        optional = "" if prop in required else "?"
        prop_type = ts_type(meta.get("type"), meta.get("format"))
        if "$ref" in meta:
            ref_name = meta["$ref"].rsplit("/", 1)[-1]
            prop_type = ref_name
        elif meta.get("type") == "array" and "items" in meta:
            item = meta["items"]
            if "$ref" in item:
                item_type = item["$ref"].rsplit("/", 1)[-1]
            else:
                item_type = ts_type(item.get("type"), item.get("format"))
            prop_type = f"{item_type}[]"
        lines.append(f"  {prop}{optional}: {prop_type};")
    lines.append("}")
    return "\n".join(lines)


def resolve_refs(spec: dict, schema: dict) -> dict:
    """Inline simple $ref for code generation."""
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/components/schemas/"):
            name = ref.rsplit("/", 1)[-1]
            components = spec.get("components", {}).get("schemas", {})
            return dict(components.get(name, schema))
    return schema


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync local openapi.json to TypeScript types (no network fetch)"
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument(
        "--openapi",
        default="openapi.json",
        help="Path relative to project root (default: openapi.json)",
    )
    parser.add_argument("--output", default="src/types/api.ts")
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
                        "Do not fetch URLs inside this skill: export from FastAPI or: "
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
    out_file = root / args.output
    out_file.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        "/** Generated from OpenAPI: refine types as needed. */",
        f"// Source: {openapi_path.name}",
        "",
    ]
    written: list[str] = []
    for name, raw_schema in list(schemas.items())[:40]:
        safe = re.sub(r"[^a-zA-Z0-9_]", "", name)
        if not safe:
            continue
        schema = resolve_refs(spec, raw_schema)
        if schema.get("type") == "object" or "properties" in schema:
            parts.append(render_interface(safe, schema))
            parts.append("")
            written.append(safe)

    content = "\n".join(parts).rstrip() + "\n"
    out_file.write_text(content)

    # Emit summary only: never dump raw OpenAPI into agent context
    emit(
        json.dumps(
            {
                "source": str(openapi_path.relative_to(root)),
                "schema_count": len(schemas),
                "path_count": len(spec.get("paths", {})),
                "written": str(out_file.relative_to(root)),
                "interfaces": written,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
