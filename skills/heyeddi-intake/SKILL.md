---
name: heyeddi-intake
description: Translates vague user prompts into HeyEddi product docs (personas, route intent, voice), route-specific handoff artifacts (wireframes, user mockups, or briefs), and skill-routing under .heyeddi/. Use first on new projects before @heyeddi-design, @heyeddi-handoff, or @flutter-engineering. Never hand-write product.md — use write_product.
paths:
  - ".heyeddi/**"
  - "PRODUCT.md"
version: 1.3.0
---

# HeyEddi Intake

**Upstream intake agent** — turns vague user language into `.heyeddi/product.md`, handoff artifacts, and skill routing for downstream HeyEddi skills.

You are **not** the implementer. You interpret, document, produce handoff artifacts, route, and **verify**.

## When to use

- New project or empty / thin `.heyeddi/product.md`
- User describes an app in plain language
- **User attached images** → `ingest_mockups` (screenshots, sketches, competitor refs)
- **No images** → `generate_wireframe` per handoff route (default)
- Before any `@heyeddi-design` / `@heyeddi-handoff` / scaffold work

## Mockup decision tree

Read **`reference/mockup-strategy.md`** (mandatory).

| Situation | Action |
|-----------|--------|
| User gave screenshots / mockups | `ingest_mockups` → tailor `mockup-brief.md` to their layout |
| No images, route needs handoff | `generate_wireframe` → **refine** `wireframe.md` for this product → `seed_brief --force` |
| No images, polished PNG handoff needed | `prepare_mockup_prompts` → **AI-generate** `desktop.png` / `mobile.png` (see `reference/ai-mockup-images.md`) → `seed_brief --force` |
| No images, route needs visual design first | Route `@heyeddi-design` — do not emit template PNGs |

**The skill package does not ship sample PNGs** and has **no Pillow/template PNG drawer**. Eval hub tooling (`uv run poe mockups`) is maintainer-only — not part of this skill.

## Mandatory pipeline

See **`reference/pipeline.md`**. Summary:

1. `load_intake`
2. Draft **`product-translation.json`** (`reference/audience-intake.md`) — template: `reference/product-translation.template.json`
3. **`write_product --json … --force`** — validates schema; writes `product.md` + saves JSON
4. `write_translation`
5. Handoff features: **`generate_wireframe`** (or `ingest_mockups` / AI PNGs per strategy) → **`seed_brief --force`**
6. **`build_routing --write --save-input`**
7. **`verify_intake --check`** — must pass before you stop

## Never

- Hand-write `product.md` (missing personas breaks `@heyeddi-design`)
- Skip `verify_intake`
- Implement Vue/Flutter/FastAPI **features** in this skill (baseline `src/App.vue` shell on scaffolded repos is OK)
- Delete `src/App.vue` or break `npm run build` to pass verify
- Use `write_routing` unless overriding `build_routing` output
- Bundle or draw cookie-cutter PNG mockups from skill scripts

## Outputs (`.heyeddi/`)

| Path | Tool |
|------|------|
| `docs/intake/product-translation.json` | `write_product` (canonical) |
| `product.md` | `write_product` |
| `docs/intake/translation-*.md` | `write_translation` |
| `docs/intake/skill-routing.json` | `build_routing --write` |
| `designs/<feature>/wireframe.md` | `generate_wireframe` (default without user images) |
| `designs/<feature>/mockup-prompts.json` | `prepare_mockup_prompts` (before AI image gen) |
| `designs/<feature>/desktop.png` | `ingest_mockups` or **agent AI image gen** after prompts |
| `designs/<feature>/mockup-brief.md` | `seed_brief` (Audience + Implementation spec) |

## Clarify before act

Read `reference/clarify-before-act.md`. One round if personas/competitors missing from user prompt.

## Related

- `reference/audience-intake.md` — JSON schema
- `reference/downstream-routing.md` — routing examples
- `reference/mockup-strategy.md` — when wireframe vs ingest vs AI PNG
- `reference/ai-mockup-images.md` — AI generation workflow (no bundled PNGs)
- `reference/mockup-quality.md` — quality bar per format
- `@heyeddi-orchestrator` — `write_skills_index` after intake (integration eval)
