#!/usr/bin/env python3
"""Detect documentation drift for files and routes changed in a PR."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _heyeddi_paths import design_md, engineering_docs_dir, product_md
from _pr_context import load_context
from _skill_cli import emit, resolve_project_root


def routes_in_product(text: str) -> list[str]:
    routes: list[str] = []
    for match in re.finditer(r"`(/[^`]+)`", text):
        route = match.group(1)
        if route not in routes:
            routes.append(route)
    return routes


def main() -> None:
    parser = argparse.ArgumentParser(description="Check doc drift for PR changed files")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--context", default=None, help="fetch_pr_context JSON path")
    parser.add_argument("--fixture", default=None, help="Fixture when context omitted")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    ctx = load_context(root, args.pr, args.context, args.fixture)
    changed: list[str] = ctx.get("changed_files") or []
    routes_touched: list[str] = ctx.get("routes_touched") or []
    categories = ctx.get("categories") or {}

    findings: list[dict] = []
    doc_files_changed = categories.get("docs", [])
    ui_changed = categories.get("ui", [])
    api_changed = [p for p in categories.get("api", []) if p not in doc_files_changed]

    pm = product_md(root)
    dm = design_md(root)
    eng_dir = engineering_docs_dir(root)

    if (ui_changed or api_changed or routes_touched) and not doc_files_changed:
        if ui_changed or routes_touched:
            findings.append(
                {
                    "severity": "warn",
                    "doc": str(pm.relative_to(root)) if pm else ".heyeddi/product.md",
                    "message": "UI or route code changed but no product/design docs updated in PR",
                    "suggestion": "Update acceptance criteria or route intent in product.md; design.md Decision log if UI changed",
                }
            )

    if pm and routes_touched:
        product_text = pm.read_text(encoding="utf-8")
        known_routes = routes_in_product(product_text)
        for route in routes_touched:
            if route not in known_routes:
                findings.append(
                    {
                        "severity": "warn",
                        "doc": str(pm.relative_to(root)),
                        "message": f"Route `{route}` touched in code but not documented in product.md",
                        "suggestion": f"Add `{route}` to Per-route intent or pages table",
                    }
                )

    if dm and ui_changed:
        design_text = dm.read_text(encoding="utf-8").lower()
        for path in ui_changed:
            stem = Path(path).stem.lower()
            if stem not in design_text and "decision log" not in design_text:
                findings.append(
                    {
                        "severity": "info",
                        "doc": str(dm.relative_to(root)),
                        "message": f"`{path}` changed — confirm design.md or Decision log mentions the UI change",
                        "suggestion": "Append Decision log entry citing component/token choices",
                    }
                )

    if api_changed and eng_dir.is_dir():
        arch = eng_dir / "architecture.md"
        if arch.is_file():
            arch_text = arch.read_text(encoding="utf-8")
            for path in api_changed:
                if Path(path).name not in arch_text and Path(path).stem not in arch_text:
                    findings.append(
                        {
                            "severity": "info",
                            "doc": str(arch.relative_to(root)),
                            "message": f"API file `{path}` changed — architecture.md may need module map update",
                            "suggestion": "Update architecture.md or append engineering ADR",
                        }
                    )
        elif api_changed:
            findings.append(
                {
                    "severity": "info",
                    "doc": str(eng_dir.relative_to(root)),
                    "message": "API changed but no engineering docs folder — run @engineering-excellence init",
                    "suggestion": "init_engineering_docs then document API surface",
                }
            )

    pr_body = (ctx.get("body") or "").strip()
    if not pr_body and changed:
        findings.append(
            {
                "severity": "info",
                "doc": "PR description",
                "message": "PR body is empty — reviewers need product intent and test plan",
                "suggestion": "Add summary, routes affected, and how to verify",
            }
        )

    status = "fail" if any(f["severity"] == "warn" for f in findings) else "ok"
    payload = {
        "pr": args.pr,
        "status": status,
        "changed_files": len(changed),
        "doc_files_in_pr": doc_files_changed,
        "routes_touched": routes_touched,
        "findings": findings,
    }
    emit(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
