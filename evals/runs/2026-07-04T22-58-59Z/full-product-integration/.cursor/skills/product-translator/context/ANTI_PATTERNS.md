# Anti-patterns

- **Never hand-write `product.md`** — use `write_product` only (validates personas + route_intent)
- **Never skip `verify_intake --check`** at end of intake
- Do not implement Vue/Flutter/FastAPI — route to downstream skills
- Do not generate mockups without `seed_brief --force` afterward
- Do not overwrite user mockups without `--force`
- Do not use incomplete JSON (missing `competitive_edge`, `anti_audience`, or <2 personas)
- Do not call `write_routing` before `product-translation.json` exists — prefer `build_routing --write`
