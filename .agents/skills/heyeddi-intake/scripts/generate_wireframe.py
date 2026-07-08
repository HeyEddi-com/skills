#!/usr/bin/env python3
"""Generate product-specific wireframe.md when user did not supply mockup images."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import designs_dir
from _product_schema import load_json, product_json_path
from _skill_cli import emit, fail, resolve_project_root
from _wireframe_layouts import build_wireframe, page_context_from_product


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate route-specific wireframe.md for handoff")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--route", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing wireframe.md")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    json_path = product_json_path(root)
    if not json_path.is_file():
        fail(f"missing {json_path.relative_to(root)} — run write_product first")

    data = load_json(json_path)
    ctx = page_context_from_product(data, feature=args.feature, route=args.route)
    content = build_wireframe(ctx)
    out_dir = designs_dir(root) / args.feature
    wireframe_path = out_dir / "wireframe.md"

    if wireframe_path.is_file() and not args.force:
        emit(json.dumps({"status": "skipped", "path": str(wireframe_path)}, indent=2))
        return

    if args.dry_run:
        emit(json.dumps({"status": "dry_run", "route": ctx.route, "chars": len(content)}, indent=2))
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    wireframe_path.write_text(content)

    handoff = {
        "route": ctx.route,
        "app": ctx.product_name,
        "mode": "wireframe",
        "fidelity": "wireframe",
        "mockup_contract": "wireframe_layout",
        "generated_by": "heyeddi-intake",
        "notes": [
            "Layout derived from product-translation.json page purpose — not a generic PNG template",
            "Refine regions in wireframe.md before @heyeddi-handoff if product intent changed",
            "mockup-brief.md seeded by seed_brief.py; expand Implementation spec from wireframe",
        ],
    }
    (out_dir / "handoff.json").write_text(json.dumps(handoff, indent=2) + "\n")

    emit(
        json.dumps(
            {
                "status": "ok",
                "feature": args.feature,
                "route": ctx.route,
                "artifacts": [str(wireframe_path.relative_to(root)), str((out_dir / "handoff.json").relative_to(root))],
                "next": f"seed_brief.py --feature {args.feature} --force",
                "hint": "Agent must tailor wireframe regions to product.md before handoff if scaffold is too generic",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
