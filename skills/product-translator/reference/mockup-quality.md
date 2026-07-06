# Mockup quality bar

**Date:** 2026-07-06

## Principle

Mockups must reflect **this product's routes and purpose** from `product-translation.json` — not a single reusable settings screenshot with the app name changed.

## User-provided images

When ingested, quality means:

1. **Faithful topology** — regions match what the user showed
2. **Brief documents assumptions** — `mockup-brief.md` names components and spacing
3. **Colors illustrative** — implementation uses `.heyeddi/design.md` tokens

## Generated wireframes (default without user images)

`generate_wireframe.py` picks layout class from page **purpose**:

| Class | Signals in purpose/route | Layout |
|-------|--------------------------|--------|
| marketing | `/`, hero, homepage | Hero + feature grid |
| login | `/login`, sign-in | Centered auth card |
| dashboard | roster, table, team | **DataTable** — not generic stat cards |
| settings | profile, notifications | Card stack + save CTA |
| generic | other | Placeholder — **agent must replace** |

Agent **must refine** `wireframe.md` before handoff if scaffold does not match product.md.

## AI-generated PNGs (when PNG handoff is required)

1. `prepare_mockup_prompts.py` — product-specific desktop/mobile prompts
2. Agent generates images (native image tool) — **not** bundled skill assets
3. `seed_brief --force` — brief matches generated layout

Prompts must cite page purpose and persona success feeling from `product-translation.json`.

## Hub eval mockups (not in skill package)

`uv run poe mockups` (`scripts/generate-handoff-mockups.py`) is **maintainer tooling** for eval/fixture projects only. Never the default consumer path for `@product-translator`.
