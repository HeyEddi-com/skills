---
name: product-translator
description: Translates vague user prompts into HeyEddi product docs (personas, route intent, voice), professional mockups, mockup briefs, and skill-routing under .heyeddi/. Use first on new projects before @heyeddi-design, @design-handoff, or @flutter-engineering. Never hand-write product.md — use write_product.
paths:
  - ".heyeddi/**"
  - "PRODUCT.md"
version: 1.1.0
---

# Product Translator

**Upstream intake agent** — turns user language into structured artifacts other HeyEddi skills consume.

You are **not** the implementer. You interpret, document, produce mockups/briefs, route, and **verify**.

## When to use

- New project or empty / thin `.heyeddi/product.md`
- User describes an app in plain language
- User attaches mockups → `ingest_mockups`; **no mockups** → `generate_mockups` + `seed_brief`
- Before any `@heyeddi-design` / `@design-handoff` / scaffold work

## Mandatory pipeline

See **`reference/pipeline.md`**. Summary:

1. `load_intake`
2. Draft **`product-translation.json`** (`reference/audience-intake.md`) — template: `reference/product-translation.template.json`
3. **`write_product --json … --force`** — validates schema; writes `product.md` + saves JSON
4. `write_translation`
5. Handoff features: `generate_mockups` → `seed_brief --force`
6. **`build_routing --write --save-input`**
7. **`verify_intake --check`** — must pass before you stop

## Never

- Hand-write `product.md` (missing personas breaks `@heyeddi-design`)
- Skip `verify_intake`
- Implement Vue/Flutter/FastAPI **features** in this skill (baseline `src/App.vue` shell on scaffolded repos is OK)
- Delete `src/App.vue` or break `npm run build` to pass verify
- Use `write_routing` unless overriding `build_routing` output

## Outputs (`.heyeddi/`)

| Path | Tool |
|------|------|
| `docs/intake/product-translation.json` | `write_product` (canonical) |
| `product.md` | `write_product` |
| `docs/intake/translation-*.md` | `write_translation` |
| `docs/intake/skill-routing.json` | `build_routing --write` |
| `designs/<feature>/desktop.png` | `generate_mockups` / `ingest_mockups` |
| `designs/<feature>/mockup-brief.md` | `seed_brief` (Audience + Implementation spec) |

## Clarify before act

Read `reference/clarify-before-act.md`. One round if personas/competitors missing from user prompt.

## Related

- `reference/audience-intake.md` — JSON schema
- `reference/downstream-routing.md` — routing examples
- `reference/mockup-quality.md` — PNG quality bar
- `@skill-orchestrator` — `write_skills_index` after intake (integration eval)
