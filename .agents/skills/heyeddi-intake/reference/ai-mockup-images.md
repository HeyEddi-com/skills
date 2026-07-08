# AI mockup images (heyeddi-intake)

**Date:** 2026-07-06

The **skill package does not ship sample PNGs** and does **not** draw template PNGs with Pillow. Mockup images belong in the **consumer project** (`.heyeddi/designs/<feature>/`), created one of three ways:

## 1. User-provided (preferred when available)

```bash
ingest_mockups.py --feature <name> --source-dir ./user-screenshots/
```

Use when the user attaches screenshots, Figma exports, sketches, or competitor references.

## 2. AI-generated (when polished PNG handoff is needed, no user images)

1. Run `prepare_mockup_prompts.py --feature <name> --route /path`
2. Read `mockup-prompts.json` → `prompts.desktop` and `prompts.mobile`
3. **Generate images** with the agent harness image tool (same pattern as `@heyeddi-design` `explore`)
4. Save as `desktop.png` and `mobile.png` in `.heyeddi/designs/<feature>/`
5. Update `handoff.json` → `fidelity: ai_generated`
6. `seed_brief --force` — interpret layout from images; tailor brief to **this product**

Prompts must reflect **page purpose** from `product-translation.json` — not a reusable settings template.

## 3. Wireframe only (default when no images)

```bash
generate_wireframe.py --feature <name> --route /path --force
```

Use for `@heyeddi-handoff` wireframe mode — no PNG required.

## Hub eval tooling (not in skill package)

Eval/fixture projects may use **`uv run poe mockups`** (`scripts/generate-handoff-mockups.py` at repo root). That script is **hub maintainer tooling only** — never bundled in `skills/heyeddi-intake/` and never the default consumer path.

## Anti-patterns

- Shipping `desktop.png` / `mobile.png` inside `skills/` directories
- Pillow preset drawings masquerading as product design
- Same layout PNG with only product name changed

## Related

- `mockup-strategy.md` — decision tree
- `heyeddi-design/reference/explore.md` — visual direction probes
