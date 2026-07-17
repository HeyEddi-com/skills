#!/usr/bin/env python3
"""Scaffold a holistic product review plan with delegation slots for UX, design, engineering."""
from __future__ import annotations

import argparse
import json
from datetime import date

from _heyeddi_paths import product_docs_dir
from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Write product review plan with cross-skill research slots")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--title", default="Product review")
    parser.add_argument("--scope", default="full", choices=["full", "route", "release"])
    parser.add_argument("--route", default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    out_dir = product_docs_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = date.today().isoformat()
    if args.route:
        slug += "-" + args.route.strip("/").replace("/", "-") or "home"
    path = out_dir / f"review-plan-{slug}.md"
    if path.is_file() and not args.force:
        emit(json.dumps({"status": "skipped", "path": str(path.relative_to(root))}, indent=2))
        return

    route_line = f"**Scope route:** `{args.route}`" if args.route else f"**Scope:** {args.scope}"
    body = REVIEW_PLAN.format(today=date.today().isoformat(), title=args.title, route_line=route_line)
    path.write_text(body, encoding="utf-8")
    emit(
        json.dumps(
            {
                "status": "ok",
                "path": str(path.relative_to(root)),
                "next": "Run load_product_context → delegate rows below → fill synthesis sections",
            },
            indent=2,
        )
    )


REVIEW_PLAN = """# {title}

**Date:** {today}  
{route_line}

PM-owned review: **does the product work, is it useful, is something else better?**  
You orchestrate specialists: you do not replace them.

## 1. Context (tools)

- [ ] `load_product_context.py`
- [ ] `audit_product.py`
- [ ] `check_features.py`

## 2. Delegate research

| Lens | Skill | Action | Findings (paste summary) |
|------|-------|--------|--------------------------|
| **Task completion** | `@ux-flow-auditor` | `trace_flow` on critical `.flow.json` tasks | |
| **UX / persona fit** | `@heyeddi-design` | `critique` on flagship routes | |
| **Legibility / layout** | `@visual-auditor` | `audit_contrast --check` + screenshots | |
| **Engineering fit** | `@engineering-excellence` | `audit_engineering` | |
| **Duplicate / waste** | `@no-duplicate-ui` | scan if UI sprawl suspected | |

## 3. PM judgment (you write)

### Does it work?
- What breaks or blocks the primary user job?
- Which acceptance criteria are not met?

### Is it useful?
- Does this solve the persona's `primary_job` from `product.md`?
- What would users do instead (competitors, spreadsheets, nothing)?

### Would something else be better?
- Simpler scope, different route structure, cut a feature, merge screens?
- Cite evidence from delegated findings: not gut feel alone.

## 4. Recommendations

| Priority | Change | Rationale | Owner skill |
|----------|--------|-----------|-------------|
| P0 | | | |
| P1 | | | |

## 5. Definition of done (this review)

- [ ] Every delegated row has findings or explicit N/A
- [ ] P0 recommendations have acceptance criteria
- [ ] `backlog.md` updated if priorities shift
- [ ] Feature specs updated if scope changes

"""


if __name__ == "__main__":
    main()
