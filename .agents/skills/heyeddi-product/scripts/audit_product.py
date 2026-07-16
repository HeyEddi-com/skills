#!/usr/bin/env python3
"""Audit product.md and feature specs for PM completeness."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from _heyeddi_paths import features_dir, product_docs_dir, product_md
from _product_scan import feature_spec_paths, parse_pages_from_product, product_sections_present
from _skill_cli import emit, fail, resolve_project_root
from _untrusted_doc import UNTRUSTED_NOTE, wrap_untrusted_doc


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit product intake and feature specs")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true", help="Exit 1 on error-level findings")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    pm = product_md(root)
    if not pm:
        fail("missing .heyeddi/product.md — run @heyeddi-intake first")

    text = pm.read_text(encoding="utf-8")
    pages = parse_pages_from_product(text)
    sections = product_sections_present(text)
    specs = feature_spec_paths(root, features_dir(root))

    findings: list[dict] = []

    if not sections.get("personas"):
        findings.append(_f("error", "missing-personas", "product.md has no Personas section"))
    if not sections.get("competitors"):
        findings.append(_f("warn", "missing-competitors", "No Competitors section — hard to judge differentiation"))
    if pages and not sections.get("route_intent"):
        findings.append(_f("error", "missing-route-intent", "Pages listed but no per-route intent"))
    if not pages:
        findings.append(_f("warn", "no-pages", "No page routes documented"))

    for page in pages:
        slug = page["route"].strip("/").replace("/", "-") or "home"
        spec_path = features_dir(root) / f"{slug}.md"
        if not spec_path.is_file() and not any(slug in p.stem for p in specs):
            findings.append(
                _f(
                    "warn",
                    "missing-feature-spec",
                    f"No feature spec for {page['route']} — write_feature_spec or features/{slug}.md",
                    route=page["route"],
                )
            )

    if not sections.get("acceptance") and not specs:
        findings.append(
            _f(
                "error",
                "no-acceptance-criteria",
                "No user stories or acceptance criteria in product.md or features/",
            )
        )

    errors = sum(1 for f in findings if f["severity"] == "error")
    warns = sum(1 for f in findings if f["severity"] == "warn")

    report = _render_report(findings, pages, errors, warns)
    out_dir = product_docs_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"product-audit-{date.today().isoformat()}.md"
    report_path.write_text(report, encoding="utf-8")

    emit(
        json.dumps(
            {
                "status": "fail" if errors else "ok",
                "errors": errors,
                "warnings": warns,
                "report": str(report_path.relative_to(root)),
                "findings": findings,
                "product_md_text": wrap_untrusted_doc("product.md", text, max_chars=12000),
                "untrusted_content_note": UNTRUSTED_NOTE,
            },
            indent=2,
        )
    )
    if args.check and errors:
        sys.exit(1)


def _f(severity: str, code: str, message: str, **extra: str) -> dict:
    row = {"severity": severity, "code": code, "message": message}
    row.update(extra)
    return row


def _render_report(findings: list[dict], pages: list, errors: int, warns: int) -> str:
    lines = [
        f"# Product audit — {date.today().isoformat()}",
        "",
        f"**Errors:** {errors} · **Warnings:** {warns}",
        "",
        f"**Routes in product.md:** {len(pages)}",
        "",
    ]
    for f in findings:
        lines.append(f"- **[{f['severity'].upper()}]** `{f['code']}` — {f['message']}")
    if not findings:
        lines.append("_No intake gaps detected._")
    lines.append("")
    lines.append("## Next")
    lines.append("")
    lines.append("1. `check_features` — spec vs code")
    lines.append("2. Delegate UX / design / engineering research (see `reference/delegation.md`)")
    lines.append("3. `write_review_plan` — synthesis and recommendations")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
