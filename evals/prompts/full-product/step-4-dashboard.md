@heyeddi-design @primevue-openprops-architect

**Goal:** Main app dashboard at `/dashboard` — team users via `useUsers()` (see `.heyeddi/product.md` — primary persona **Jordan**).

Follow your workflow:

1. `load_context` — `audience_ready` + read **Per-route intent** for `/dashboard`.
2. **`shape`** → `designs/taskflow-dashboard/brief.md` with **Audience** section; read `audience-design.md` + `modern-reference.md`.
3. `craft` the dashboard for Jordan's job (roster/status, not generic KPI theater).
4. `audience-fit` rubric before done.

## Dashboard shape (TaskFlow — not wireframe KPI grid)

- **Primary content:** PrimeVue DataTable (or list) of users from `useUsers()`
- **Optional:** 1–2 summary stat cards (member count, data source) — **do not need 3 KPI tiles**
- Welcome heading, Refresh action, loading / empty / offline demo states
- Calm density for team lead — Stripe Dashboard / Linear patterns, not plain admin

## Eval constraints (important)

- **`useUsers()` must render without a live API** — demo rows, empty state, or graceful error when API is down. Do **not** start `uvicorn` or curl `:8090` / `:8000`.
- **`npm test` + `npm run build` only** — no `npm run dev`, Playwright, or backend servers.
- **Do not edit** `.heyeddi/audits/eval-process/` — the harness writes proof captures after this turn.

**Eval harness:** Screenshots save to `.heyeddi/audits/eval-process/dashboard/` when the turn completes. Hard gate expects **user table rows**, not 3 stat cards.

**Unit tests:** Use `createMemoryHistory("/dashboard")` (not `createWebHistory`) and register stub routes for `/`, `/dashboard`, and `/settings` so `npm test` emits **no Vue Router warnings**. See `tests/helpers/createViewRouter.ts`.
