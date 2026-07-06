#!/usr/bin/env python3
"""Seed a professional mockup-brief.md for a feature (translator-owned brief)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import designs_dir, product_md
from _product_schema import format_audience_block
from _skill_cli import emit, fail, resolve_project_root

BRIEF_TEMPLATE = """# Mockup brief — {feature_title} ({app_name})

Authored by `@product-translator` from user intent + layout mockups. Colors from `.heyeddi/design.md` tokens — not PNG pixels.

## Audience (from product.md)

{audience_block}

## Designer read (first impression)

{designer_read}

## Layout topology

### Desktop
| Zone | Size / position | Behavior |
|------|-----------------|----------|
| App sidebar | 248px fixed left | Logo, nav pills, user chip pinned bottom |
| Main content | max-width ~720px, padded | Page title + card stack |
| Stat / cards | 16px gap | Elevated surfaces, 12px radius |

### Mobile
| Zone | Behavior |
|------|----------|
| Top bar | App name + menu |
| Content | Full-width cards, 16px horizontal inset |
| Primary CTA | Full-width or pinned bottom |

## Region map

### Desktop
| Region | What the user sees | Build |
|--------|-------------------|-------|
| Sidebar | Nav + active pill | AppSidebar custom + tokens |
| Profile card | Display name + email fields | PrimeVue Card `#content` |
| Notifications card | Toggle row | Card `#content` + ToggleSwitch |
| Save CTA | Primary button outside cards | Filled Button, right-aligned |

## Spacing & alignment (designer rules)

- Card internal padding: **≥ 16px** (`var(--size-4)` or `--size-5`)
- Gap between cards: **16–24px**
- Sidebar width token: **248px** (`--sidebar-width`)
- Save button **outside** card stack, not inside Profile card

## Implementation spec

| Component / region | Token or CSS rule | File(s) |
|--------------------|-------------------|---------|
| Sidebar width | `--sidebar-width: 248px` | `tokens.css`, `AppSidebar.vue` |
| Card body padding | `.p-card-body {{ padding: var(--size-5) }}` | route scoped CSS |
| Card stack gap | `gap: var(--size-4)` | route container |
| Nav active | brand subtle bg + brand text | `AppSidebar.vue` |
| Card content slot | `<template #content>` | all Card usages |

## Theme notes

- Light/dark coherent with app shell — see `heyeddi-design/reference/modern-reference.md`
- Avoid flat admin-template look: borders + surface-2 cards

## Responsive

- Desktop: sidebar persistent
- Mobile: drawer or bottom nav per product.md

_Source route: `{route}` · Feature folder: `.heyeddi/designs/{feature}/`_
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed mockup-brief.md")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--route", default=None)
    parser.add_argument("--app-name", default="HeyEddi App")
    parser.add_argument("--designer-read", default="Calm in-app settings — clear hierarchy, generous card padding, modern SaaS (Linear/Stripe density).")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = resolve_project_root(args.project_root)
    feature_dir = designs_dir(root) / args.feature
    brief_path = feature_dir / "mockup-brief.md"
    route = args.route or f"/{args.feature}"

    if brief_path.is_file() and not args.force:
        emit(json.dumps({"status": "skipped", "path": str(brief_path)}, indent=2))
        return

    handoff_path = feature_dir / "handoff.json"
    if handoff_path.is_file():
        try:
            meta = json.loads(handoff_path.read_text())
            route = meta.get("route") or route
            args.app_name = meta.get("app") or args.app_name
        except json.JSONDecodeError:
            pass

    p_path = product_md(root)
    product_text = p_path.read_text(errors="replace") if p_path and p_path.is_file() else None
    audience_block = format_audience_block(product_text, route)

    content = BRIEF_TEMPLATE.format(
        feature_title=args.feature.replace("-", " ").title(),
        app_name=args.app_name,
        audience_block=audience_block,
        designer_read=args.designer_read,
        route=route,
        feature=args.feature,
    )

    if args.dry_run:
        emit(json.dumps({"status": "dry_run", "chars": len(content)}, indent=2))
        return

    feature_dir.mkdir(parents=True, exist_ok=True)
    brief_path.write_text(content)
    emit(json.dumps({"status": "ok", "path": str(brief_path), "route": route}, indent=2))


if __name__ == "__main__":
    main()
