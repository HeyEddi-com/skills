# Mockup strategy (product-translator)

**Date:** 2026-07-06

Handoff needs **layout intent** for `@design-handoff`. It does **not** need bundled template PNGs or Pillow drawings shipped with the skill.

## Decision tree

```
User attached images / screenshots?
├─ YES → ingest_mockups.py
│         Optionally refine mockup-brief from what you see
└─ NO  → Does product.md describe a route that needs handoff now?
          ├─ YES → generate_wireframe.py (default)
          │         Agent refines wireframe.md regions for this product
          │         seed_brief --force (expand Implementation spec from wireframe)
          ├─ NEED polished PNG handoff, no user images?
          │         prepare_mockup_prompts.py → agent AI-generates desktop.png + mobile.png
          │         (see ai-mockup-images.md — skill does not draw PNGs)
          └─ NO  → Route to @heyeddi-design (shape/craft) — do not fake PNGs
```

## Allowed outputs (no user images)

| Format | Tool / action | When |
|--------|---------------|------|
| **ASCII / markdown wireframe** | `generate_wireframe.py` + agent edits | **Default** — layout from `product-translation.json` page purpose |
| **Mermaid / diagram** | Agent writes `wireframe.md` or `diagram.mmd` | Complex flows, onboarding, multi-step |
| **Text-only brief** | Agent writes `mockup-brief.md` with rich Implementation spec | Sparse apps; wireframe optional if spec is measurable |
| **AI PNG mockups** | `prepare_mockup_prompts.py` + agent image generation | When `@design-handoff` needs PNGs and user gave none |

## Forbidden

- Shipping sample PNGs inside `skills/product-translator/`
- Pillow/template PNG scripts in the skill package (removed — hub `poe mockups` is eval-only)
- Reusing identical layout PNGs on every product regardless of `pages[].purpose`
- Skipping `seed_brief` after wireframe, ingest, or AI PNGs

## User screenshots as guidance

When the user provides reference screenshots (competitor UI, sketch, whiteboard):

1. `ingest_mockups` into `.heyeddi/designs/<feature>/`
2. Read images — capture **layout topology**, not pixel colors
3. Write or update `mockup-brief.md` with regions matching **their** structure
4. `@design-handoff` implements from brief + images

## Downstream

- Wireframe mode: `@design-handoff` reads `wireframe.md` (`reference/low-fidelity-mockups.md`)
- PNG mode: `@design-handoff` reads `desktop.png` / `mobile.png` (user or AI-generated in project)
- Polish needed: route to `@heyeddi-design` before handoff
