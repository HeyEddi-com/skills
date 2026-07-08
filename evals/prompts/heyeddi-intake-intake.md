@heyeddi-intake

Read `USER_PROMPT.md` and run the **full mandatory pipeline** (`reference/pipeline.md`):

1. `load_intake --prompt-file USER_PROMPT.md`
2. Create `.heyeddi/docs/intake/product-translation.json` with **full schema** (`reference/audience-intake.md`):
   - ≥2 **personas**, **route_intent** for every page route, **competitors**, **competitive_edge**, **anti_audience**, **voice_tone**, pages, stack_note, design_references
3. **`write_product --json .heyeddi/docs/intake/product-translation.json --force`** — never hand-write product.md
4. `write_translation` — summary + decisions JSON array
5. `generate_wireframe --feature settings --route /settings --force` — refine `wireframe.md` for TaskFlow if needed
6. `seed_brief --feature settings --app-name TaskFlow --force`
7. **`build_routing --write --save-input`**
8. **`verify_intake --check`** — must exit 0

**Do not** implement Vue/FastAPI code. **Do not** skip validation tools.

Read all `.heyeddi/` artifacts when done.
