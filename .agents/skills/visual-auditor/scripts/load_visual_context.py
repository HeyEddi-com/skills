#!/usr/bin/env python3
"""Load product + design spec context for visual review of a route."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from _heyeddi_paths import screenshot_dir, visual_audit_dir
from _skill_cli import emit, resolve_project_root
from _spec_context import feature_slug, load_route_context


def _design_md(root: Path) -> Path | None:
    for rel in (".heyeddi/design.md", ".heyeddi/DESIGN.md", "DESIGN.md"):
        p = root / rel
        if p.is_file():
            return p
    return None


def _product_md(root: Path) -> Path | None:
    for rel in (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md"):
        p = root / rel
        if p.is_file():
            return p
    return None


def _designs_dir(root: Path) -> Path:
    for rel in (".heyeddi/designs", "designs"):
        p = root / rel
        if p.is_dir():
            return p
    return root / ".heyeddi" / "designs"


def _write_review_template(root: Path, route: str, ctx: dict) -> Path:
    slug = feature_slug(route)
    reviews = visual_audit_dir(root) / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    path = reviews / f"{slug}-review-{date.today().isoformat()}.md"
    if path.is_file():
        return path

    intent = ctx.get("route_intent") or {}
    lines = [
        f"# Visual review — `{route}`",
        "",
        f"**Date:** {date.today().isoformat()}",
        "",
        "## Specification",
        "",
        f"- **Page purpose:** {ctx.get('page_purpose') or '_(see product.md)_'}",
        f"- **Primary persona:** {intent.get('primary_persona', '—')}",
        f"- **Success feeling:** {intent.get('success_feeling', '—')}",
        f"- **Product:** `{ctx.get('product_md')}`",
        f"- **Design:** `{ctx.get('design_md')}`",
        f"- **Mockup brief:** `{ctx.get('mockup_brief')}`",
        "",
        "## Captures reviewed",
        "",
    ]
    for cap in ctx.get("captures", []):
        lines.append(f"- `{cap}`")
    if not ctx.get("captures"):
        lines.append("- _(run capture_screenshots first)_")
    lines.extend(
        [
            "",
            "## vs product.md",
            "",
            "_Agent: what matches / diverges from purpose and persona job?_",
            "",
            "## vs design.md + mockup brief",
            "",
            "_Agent: hierarchy, spacing, tokens, component choices vs design spec_",
            "",
            "## Automated contrast",
            "",
            f"Report: `{ctx.get('contrast', {}).get('path', '—')}`",
            "",
            "## Issues found",
            "",
            "| # | Issue | Spec ref | Severity |",
            "|---|-------|----------|----------|",
            "",
            "## Fixes applied",
            "",
            "_Use append_fix_log.py per fix — entries mirror below._",
            "",
            "## Re-verify",
            "",
            "- [ ] `capture_screenshots` re-run",
            "- [ ] `audit_contrast --check` pass",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Load visual review context for a route")
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--write-review", action="store_true", help="Create review markdown template")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    ctx = load_route_context(
        root,
        args.route,
        product_path=_product_md(root),
        design_path=_design_md(root),
        designs_root=_designs_dir(root),
        visual_dir=visual_audit_dir(root),
        screenshot_dir=screenshot_dir(root),
    )

    review_path = None
    if args.write_review:
        review_path = _write_review_template(root, args.route, ctx)
        ctx["review_doc"] = str(review_path.relative_to(root))

    ctx["next"] = [
        "1. Read captures + product.md route intent + design.md + mockup-brief",
        "2. Fix issues in Vue/CSS immediately — do not only list them",
        "3. append_fix_log.py per fix",
        "4. Re-run capture_screenshots + audit_contrast --check",
        "5. finalize_visual_review.py",
    ]
    emit(json.dumps(ctx, indent=2))


if __name__ == "__main__":
    main()
