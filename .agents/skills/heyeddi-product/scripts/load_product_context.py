#!/usr/bin/env python3
"""Load product context — spec, code routes, feature specs, delegation hints."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import features_dir, product_json, product_md, routing_json
from _product_scan import (
    build_feature_matrix,
    feature_spec_paths,
    parse_pages_from_product,
    product_sections_present,
    ux_flow_tasks,
    vue_routes,
)
from _skill_cli import emit, resolve_project_root
from _untrusted_doc import UNTRUSTED_NOTE, wrap_purpose_fields, wrap_untrusted_doc


def main() -> None:
    parser = argparse.ArgumentParser(description="Load PM context snapshot")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    pm_path = product_md(root)
    product_text = pm_path.read_text(encoding="utf-8") if pm_path else ""
    pages = wrap_purpose_fields(parse_pages_from_product(product_text)) if product_text else []
    sections = product_sections_present(product_text) if product_text else {}
    specs = feature_spec_paths(root, features_dir(root))
    # Parse matrix from raw text so status logic sees unwrapped purpose; wrap for emit.
    raw_pages = parse_pages_from_product(product_text) if product_text else []
    matrix = wrap_purpose_fields(build_feature_matrix(root, raw_pages)) if raw_pages else []

    feature_spec_texts: dict[str, str] = {}
    for spec in specs:
        rel = str(spec.relative_to(root))
        feature_spec_texts[rel] = wrap_untrusted_doc(
            f"feature-spec:{spec.name}",
            spec.read_text(encoding="utf-8", errors="replace"),
            max_chars=6000,
        ) or ""

    delegation = []
    if pages:
        delegation.append(
            {
                "question": "Can users complete core tasks?",
                "skill": "ux-flow-auditor",
                "tool": "trace_flow",
                "when": "After routes implemented; define .flow.json per critical task",
            }
        )
    delegation.append(
        {
            "question": "Is UI right for personas and legible?",
            "skill": "heyeddi-design",
            "tool": "critique",
            "when": "Flagship routes with real UI — not wireframe-only",
        }
    )
    delegation.append(
        {
            "question": "Contrast and responsive layout proof?",
            "skill": "visual-auditor",
            "tool": "audit_contrast --check",
            "when": "Before calling a route done",
        }
    )
    delegation.append(
        {
            "question": "Is implementation simple and maintainable?",
            "skill": "engineering-excellence",
            "tool": "audit_engineering",
            "when": "After feature ships or before large refactor",
        }
    )

    payload = {
        "product_md": str(pm_path.relative_to(root)) if pm_path else None,
        "product_json": str(product_json(root).relative_to(root)) if product_json(root) else None,
        "skill_routing": str(routing_json(root).relative_to(root)) if routing_json(root) else None,
        "product_md_text": wrap_untrusted_doc("product.md", product_text, max_chars=12000)
        if product_text
        else None,
        "sections": sections,
        "pages": pages,
        "feature_specs": [str(p.relative_to(root)) for p in specs],
        "feature_spec_texts": feature_spec_texts,
        "code_routes": vue_routes(root),
        "feature_matrix": matrix,
        "ux_flow_tasks": ux_flow_tasks(root),
        "delegation": delegation,
        "gaps": _gaps(sections, pages, specs, matrix),
        "next": "audit_product → delegate per delegation → write_review_plan",
        "untrusted_content_note": UNTRUSTED_NOTE,
    }
    emit(json.dumps(payload, indent=2))


def _gaps(
    sections: dict[str, bool],
    pages: list,
    specs: list[Path],
    matrix: list[dict],
) -> list[str]:
    gaps: list[str] = []
    if not sections.get("personas"):
        gaps.append("product.md missing Personas — run @heyeddi-intake or init")
    if pages and not sections.get("route_intent"):
        gaps.append("product.md missing per-route intent")
    if pages and len(specs) < len(pages):
        gaps.append(f"feature specs: {len(specs)}/{len(pages)} routes covered")
    for row in matrix:
        if row.get("status") in {"missing", "placeholder"}:
            gaps.append(f"{row['route']}: {row['status']} ({', '.join(row.get('flags', []))})")
    if not sections.get("acceptance"):
        gaps.append("no acceptance criteria / user stories in product.md or features/")
    return gaps


if __name__ == "__main__":
    main()
