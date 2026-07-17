#!/usr/bin/env python3
"""Write a feature spec markdown from JSON (user stories + acceptance criteria)."""
from __future__ import annotations

import argparse
import json
from datetime import date

from _heyeddi_paths import features_dir
from _skill_cli import emit, fail, resolve_project_root


def render_spec(data: dict) -> str:
    route = data.get("route", "/")
    title = data.get("title") or f"Feature: {route}"
    problem = data.get("problem", "")
    stories = data.get("user_stories") or []
    ac = data.get("acceptance_criteria") or []
    metric = data.get("success_metric", "")
    alternatives = data.get("alternatives_considered") or []
    out_of_scope = data.get("out_of_scope") or []

    lines = [
        f"# {title}",
        "",
        f"**Route:** `{route}` · **Updated:** {date.today().isoformat()}",
        "",
    ]
    if problem:
        lines.extend(["## Problem / user job", "", problem, ""])
    lines.append("## User stories")
    lines.append("")
    for s in stories:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## Acceptance criteria")
    lines.append("")
    for i, item in enumerate(ac, 1):
        lines.append(f"{i}. {item}")
    lines.append("")
    if metric:
        lines.extend(["## Success metric", "", metric, ""])
    if alternatives:
        lines.extend(["## Alternatives considered", ""])
        for alt in alternatives:
            lines.append(f"- {alt}")
        lines.append("")
    if out_of_scope:
        lines.extend(["## Out of scope", ""])
        for item in out_of_scope:
            lines.append(f"- {item}")
        lines.append("")
    lines.extend(
        [
            "## PM review checklist",
            "",
            "- [ ] `@ux-flow-auditor`: task completes within click budget",
            "- [ ] `@heyeddi-design critique`: fits primary persona",
            "- [ ] `@visual-auditor audit_contrast --check`: legible",
            "- [ ] `@engineering-excellence`: no over-engineering",
            "- [ ] `check_features`: status not placeholder",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Write feature spec from JSON")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json", required=True, help="Feature spec JSON string or path")
    parser.add_argument("--slug", default=None, help="Filename slug (default from route)")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    raw = args.json
    if raw.endswith(".json") and (root / raw).is_file():
        data = json.loads((root / raw).read_text())
    else:
        data = json.loads(raw)

    route = data.get("route", "/")
    slug = args.slug or route.strip("/").replace("/", "-") or "home"
    out = features_dir(root) / f"{slug}.md"
    if out.is_file() and not args.force:
        emit(json.dumps({"status": "skipped", "path": str(out.relative_to(root))}, indent=2))
        return

    body = render_spec(data)
    if args.dry_run:
        emit(body)
        return

    features_dir(root).mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    emit(json.dumps({"status": "ok", "path": str(out.relative_to(root))}, indent=2))


if __name__ == "__main__":
    main()
