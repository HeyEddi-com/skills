#!/usr/bin/env python3
"""Write or merge .heyeddi/product.md from structured translation JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _heyeddi_paths import canonical_product_path, heyeddi_dir, intake_dir
from _product_schema import product_json_path, validate_product_json
from _skill_cli import emit, fail, resolve_project_root


def _table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def render_personas(personas: list[Any]) -> list[str]:
    lines = [
        "## Personas",
        "",
        _table_row(["Name", "Role", "Primary job", "Anxiety", "Design implication"]),
        _table_row(["------", "------", "-------------", "---------", "--------------------"]),
    ]
    for row in personas:
        if not isinstance(row, dict):
            continue
        lines.append(
            _table_row(
                [
                    str(row.get("name", "")),
                    str(row.get("role", "")),
                    str(row.get("primary_job", "")),
                    str(row.get("anxiety", "")),
                    str(row.get("design_implication", "")),
                ]
            )
        )
    lines.append("")
    return lines


def render_route_intent(routes: list[Any]) -> list[str]:
    lines = [
        "## Per-route intent",
        "",
        _table_row(["Route", "Register", "Primary persona", "User mindset", "Success feeling"]),
        _table_row(["-------", "---------", "-----------------", "--------------", "-----------------"]),
    ]
    for row in routes:
        if not isinstance(row, dict):
            continue
        lines.append(
            _table_row(
                [
                    f"`{row.get('route', '/')}`",
                    str(row.get("register", "product")),
                    str(row.get("primary_persona", "")),
                    str(row.get("mindset", "")),
                    str(row.get("success_feeling", "")),
                ]
            )
        )
    lines.append("")
    return lines


def render_product(data: dict[str, Any]) -> str:
    name = data.get("product_name", "Product")
    audience = data.get("audience_summary") or data.get("audience", "Describe your users.")
    stack = data.get("stack_note", "Vue or Flutter frontend; FastAPI and/or Firebase backend.")
    pages = data.get("pages") or []
    personality = data.get("brand_personality", data.get("voice_tone", "Clear, confident, modern SaaS."))
    references = data.get("design_references") or ["Linear: crisp borders", "Stripe Dashboard: calm data UI"]
    anti = data.get("anti_references") or ["Generic unstyled PrimeVue admin template"]
    personas = data.get("personas") or []
    route_intent = data.get("route_intent") or []
    competitors = data.get("competitors") or []
    competitive_edge = data.get("competitive_edge", "")
    anti_audience = data.get("anti_audience", "")
    voice_tone = data.get("voice_tone") or personality

    lines = [f"# {name}", "", audience, ""]
    lines.extend(render_personas(personas))
    lines.extend(render_route_intent(route_intent))
    lines.extend(
        [
            "## Stack",
            "",
            stack,
            "",
            "## Pages",
            "",
            "| Route | View | Purpose |",
            "|-------|------|---------|",
        ]
    )
    for row in pages:
        if isinstance(row, dict):
            lines.append(f"| `{row.get('route', '/')}` | `{row.get('view', 'View')}` | {row.get('purpose', '')} |")
        elif isinstance(row, (list, tuple)) and len(row) >= 3:
            lines.append(f"| `{row[0]}` | `{row[1]}` | {row[2]} |")

    lines.extend(["", "## Brand personality", "", personality, "", "## Competitors", ""])
    if competitors:
        lines.append(f"- Users compare us to: {', '.join(str(c) for c in competitors)}")
    if competitive_edge:
        lines.append(f"- We win on: {competitive_edge}")
    lines.append("")

    lines.extend(["## Anti-audience", "", anti_audience or "(define who this is NOT for)", ""])
    lines.extend(["## Voice & tone", "", voice_tone, "", "## Design references", ""])
    for ref in references:
        lines.append(f"- {ref}")

    lines.extend(["", "## Anti-references", ""])
    for item in anti:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Downstream skills",
            "",
            "See `.heyeddi/docs/intake/skill-routing.json` for which `@skill` runs per route.",
            "",
            "_Authored by `@heyeddi-intake` via `write_product.py`: do not edit structure by hand._",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write .heyeddi/product.md from translation JSON")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", default=None, help="JSON string or path to JSON file")
    parser.add_argument("--merge", action="store_true", help="Skip if product.md exists unless --force")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    if not args.json:
        fail("--json required: never hand-write product.md; see reference/audience-intake.md")

    try:
        data = json.loads(args.json)
    except json.JSONDecodeError:
        json_path = Path(args.json)
        if not json_path.is_file():
            fail(f"invalid JSON and not a file path: {args.json[:120]}")
        try:
            data = json.loads(json_path.read_text())
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON file {json_path}: {exc}")

    ok, errors = validate_product_json(data)
    if not ok:
        fail("product JSON validation failed:\n- " + "\n- ".join(errors))

    target = canonical_product_path(root)
    if target.is_file() and args.merge and not args.force:
        emit({"skipped": True, "path": str(target), "reason": "exists: use --force"})
        return

    content = render_product(data)
    json_dest = product_json_path(root)

    if args.dry_run:
        emit(
            {
                "dry_run": True,
                "path": str(target),
                "json_path": str(json_dest),
                "personas": len(data.get("personas") or []),
                "route_intent": len(data.get("route_intent") or []),
                "preview_lines": content.splitlines()[:24],
            }
        )
        return

    heyeddi_dir(root).mkdir(parents=True, exist_ok=True)
    intake_dir(root).mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    json_dest.write_text(json.dumps(data, indent=2) + "\n")

    emit(
        {
            "ok": True,
            "path": str(target),
            "json_path": str(json_dest.relative_to(root)),
            "personas": len(data.get("personas") or []),
            "route_intent": len(data.get("route_intent") or []),
            "next": "write_translation → generate_wireframe or ingest_mockups → seed_brief → build_routing --write",
        }
    )


if __name__ == "__main__":
    main()
