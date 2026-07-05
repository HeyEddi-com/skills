@heyeddi-design @primevue-openprops-architect

**Goal:** The `/login` screen **already exists** but looks bad (black native inputs, hex colors, cramped layout). **Critique first, then polish** — not greenfield `shape` + `craft`.

## Mandatory order

1. `load_context` — read `.heyeddi/product.md` and `.heyeddi/design.md`.
2. **Critique** (`reference/critique.md`) — study `LoginView.vue`; write `.heyeddi/docs/login-critique.md` (P0/P1 issues, token drift, fix directions).
3. **Document** — update `.heyeddi/design.md` where drift vs intended tokens/components.
4. **Polish** (`reference/polish.md`) — fix P0/P1 from your critique: PrimeVue + OpenProps, no hex, spacing/hierarchy.
5. Validate with `@primevue-openprops-architect`.
6. **Append** Decision log — reference critique findings + what you fixed.

**Scope / stop rules:**
- Finish when `npm test` and `npm run build` pass.
- Do **not** run Playwright, `@visual-auditor`, or `npm run dev` — harness runs visual QA after your turn.

No designer mockups — judge critique quality + implementation improvements.
