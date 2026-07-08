# Engineering scaffold audit — TaskFlow

**Date:** 2026-07-04  
**Skill:** `@project-engineering`  
**Product:** TaskFlow (Vue 3 + FastAPI)

## Summary

Structural engineering baseline is **complete**. The repo builds, tests pass, and local dev servers are configured. Remaining work is **feature-level**: UI routes/views (`@heyeddi-design`), auth API, and design system documentation.

| Layer | Audit status | Notes |
|-------|--------------|-------|
| Vue (Vite/Vitest) | ✅ ok | PrimeVue + OpenProps wired; empty router intentional |
| FastAPI | ✅ ok | Health + stub users endpoint; poetry deps installed |
| Firebase | ✅ scaffolded, inactive | Files present from `--stack full`; not in `stack.json` backends |
| `.heyeddi/` workspace | ✅ ok | product, stack, design draft, intake routing present |

## Audit results (`audit_scaffold`)

```json
{
  "vue": { "status": "ok", "missing_required": [], "warnings": [] },
  "fastapi": { "status": "ok", "missing_required": [], "warnings": ["venv check — poetry uses shared env; tests pass"] },
  "firebase": { "status": "ok", "missing_required": [] }
}
```

**Stack declaration** (`.heyeddi/stack.json`):

```json
{ "frontend": "vue", "backends": ["fastapi"], "api_port": 8090 }
```

## What exists

### Frontend

| Artifact | Status |
|----------|--------|
| `package.json` — dev, build, test scripts | ✅ |
| Vite + proxy `/api` → `:8090` | ✅ |
| Vitest + `tests/unit/App.spec.ts` | ✅ |
| PrimeVue Aura preset + `src/styles/tokens.css` | ✅ |
| `src/App.vue` shell with `<router-view>` | ✅ |
| `src/router/index.ts` | ⚠️ empty `routes: []` |

### Backend

| Artifact | Status |
|----------|--------|
| `backend/pyproject.toml` + `poetry.lock` | ✅ |
| `GET /health` | ✅ |
| `GET /api/users` (stub) | ✅ |
| `backend/tests/test_health.py` | ✅ |
| `backend/tests/test_users.py` | ✅ (added this audit) |
| `openapi.json` | ✅ synced with live endpoints |

### Product / routing intent

From `.heyeddi/product.md` and `skill-routing.json`:

| Route | View | Next skill |
|-------|------|------------|
| `/` | `HomeView` | `@heyeddi-design` craft (brand) |
| `/login` | `LoginView` | `@heyeddi-design` craft (brand) |
| `/dashboard` | `DashboardView` | `@heyeddi-design` craft (product) |
| `/settings` | `SettingsView` | `@heyeddi-handoff` (mockups in `.heyeddi/designs/settings/`) |

## Gaps (by owner)

### `@heyeddi-design` — UI

- [ ] Register routes in `src/router/index.ts`
- [ ] Create views: `HomeView`, `LoginView`, `DashboardView`
- [ ] Run `document` to complete `.heyeddi/design.md` (currently draft)
- [ ] Dashboard: fetch and display `GET /api/users`

### `@heyeddi-handoff` — Settings

- [ ] Implement `/settings` from `.heyeddi/designs/settings/` mockups + brief

### API / backend (feature work)

- [ ] `POST /api/auth/login` (or equivalent) for login flow
- [ ] User persistence (DB or in-memory store for MVP)
- [ ] Expand `openapi.json` as endpoints ship
- [ ] Run `@backend-type-bridger` to generate TypeScript types from OpenAPI

### Optional / inactive

- Firebase emulator scaffold exists (`firebase.json`, rules) but **not** declared in `stack.json` backends — ignore unless product adds Firestore/Auth.

## Verification (2026-07-04)

| Check | Result |
|-------|--------|
| `ensure_npm` | ✅ node_modules present |
| `ensure_python` | ✅ poetry install (uvicorn 0.50.0) |
| `npm test` | ✅ 1 passed |
| `run_backend_tests` | ✅ 2 passed (health + users) |
| `npm run build` | ✅ production build OK |

## Local dev servers

Run each in its **own terminal**:

| Stack | Command | URL |
|-------|---------|-----|
| Vue | `npm run dev` | http://localhost:5173 |
| FastAPI | `cd backend && poetry run uvicorn app.main:app --reload --port 8090` | http://localhost:8090/docs |

Vite proxies `/api/*` to the API on port 8090.

## Recommended next steps

1. `@heyeddi-design document` — fill design system in `.heyeddi/design.md`
2. `@heyeddi-design craft` — flagship routes per `skill-routing.json` order (`/` → `/login` → `/dashboard`)
3. `@heyeddi-handoff` — `/settings` from existing mockups
4. `@backend-type-bridger` — sync OpenAPI → TypeScript after API expands

---

_Authored by `@project-engineering` audit workflow._
