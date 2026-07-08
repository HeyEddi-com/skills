#!/usr/bin/env python3
"""Sync OpenAPI schema to TypeScript types under src/types/api.ts."""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from _skill_cli import emit, resolve_project_root

ALLOWED_URL_SCHEMES = ("http", "https")


def validate_fetch_url(url: str) -> str | None:
    """Return an error string if the URL is unsafe to fetch, else None.

    Guards against SSRF vectors: only http/https, no embedded credentials,
    and a host must be present. Blocks file://, ftp://, gopher:// and similar.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_URL_SCHEMES:
        return f"refusing URL scheme '{parsed.scheme or '(none)'}': only http/https allowed"
    if not parsed.hostname:
        return "refusing URL without a host"
    if parsed.username or parsed.password:
        return "refusing URL with embedded credentials"
    return None


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
    parser = argparse.ArgumentParser(description="Sync OpenAPI to TypeScript types")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--url", default=None)
    parser.add_argument("--output", default="src/types/api.ts")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    local = root / "openapi.json"
    spec = None
    source = None

    if local.is_file():
        spec = json.loads(local.read_text())
        source = str(local)
    elif args.url:
        url_error = validate_fetch_url(args.url)
        if url_error:
            emit(json.dumps({"error": url_error, "hint": "Pass an http(s) URL such as http://localhost:8090/openapi.json"}, indent=2))
            return
        try:
            request = urllib.request.Request(args.url, method="GET")
            with urllib.request.urlopen(request, timeout=10) as resp:
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
                    "hint": "Add openapi.json to project root or pass --url http://localhost:8090/openapi.json",
                },
                indent=2,
            )
        )
        return

    schemas = spec.get("components", {}).get("schemas", {})
    out_file = root / args.output
    out_file.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        "/** Generated from OpenAPI — refine types as needed. */",
        f"// Source: {source}",
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

    emit(
        json.dumps(
            {
                "source": source,
                "schema_count": len(schemas),
                "written": str(out_file),
                "interfaces": written,
                "path_count": len(spec.get("paths", {})),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
