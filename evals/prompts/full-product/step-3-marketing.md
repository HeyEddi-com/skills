@heyeddi-design @primevue-openprops-architect

**Goal:** Public marketing site + sign-in for TaskFlow (see `.heyeddi/product.md` **Personas** and **Per-route intent** for `/` and `/login`).

`DESIGN.md` is a draft — incomplete component catalog and layout rules. Follow your full design workflow:

1. `load_context` — check `audience_ready`; read personas for **Sam** (evaluator) on brand routes.
2. **`shape`** for feature **`taskflow-marketing`** — include **Audience** section in brief; read `reference/audience-design.md` + `modern-reference.md`; write `research.md` with **Audience fit**.
3. When brief is confirmed → `craft` home (`/`) and login (`/login`) plus app shell nav.
4. After craft → `audience-fit` rubric (PASS before done).

This is a **brand/marketing** surface (not the settings handoff — mockups for that are under `.heyeddi/designs/settings/`).

**Eval harness:** After this turn, screenshots of `/` and `/login` are saved to `.heyeddi/audits/eval-process/marketing-and-login/`.

Build production UI — OpenProps tokens, PrimeVue, no hex colors. Microcopy matches **Voice & tone** in product.md.

**Scope:** `npm test` + `npm run build` only. No dev servers or Playwright in this turn.

**Unit tests:** When adding `LoginView.spec.ts`, use `createViewRouter("/login", LoginView)` from `tests/helpers/createViewRouter.ts` — never `createWebHistory()`.
