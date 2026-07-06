# Examples — TaskFlow intake

Copy `reference/product-translation.template.json` as starting point, then:

```bash
python scripts/load_intake.py --project-root . --prompt-file USER_PROMPT.md
python scripts/write_product.py --project-root . --json .heyeddi/docs/intake/product-translation.json --force
python scripts/write_translation.py --project-root . \
  --user-prompt "$(cat USER_PROMPT.md)" \
  --summary "TaskFlow B2B task manager for small teams." \
  --decisions '["Vue+FastAPI","4 routes","settings via design-handoff"]'
python scripts/generate_wireframe.py --project-root . --feature settings --route /settings --force
python scripts/seed_brief.py --project-root . --feature settings --app-name TaskFlow --force
python scripts/build_routing.py --project-root . --write --save-input
python scripts/verify_intake.py --project-root . --check
```

User-supplied PNGs (screenshots, sketches):

```bash
python scripts/ingest_mockups.py --project-root . --feature settings --route /settings --source-dir ./user-mockups/
python scripts/seed_brief.py --project-root . --feature settings --app-name TaskFlow --force
```

AI PNG handoff (no user images, polished layout references needed):

```bash
python scripts/prepare_mockup_prompts.py --project-root . --feature settings --route /settings --force
# Agent generates desktop.png + mobile.png from mockup-prompts.json (see reference/ai-mockup-images.md)
python scripts/seed_brief.py --project-root . --feature settings --app-name TaskFlow --force
```
