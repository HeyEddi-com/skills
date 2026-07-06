# Architecture

**Last updated:** 2026-07-04

How this system works — modules, data flow, and boundaries. Update when structure changes.

## Stack

| Layer | Tech | Notes |
|-------|------|-------|
| Frontend | Vue 3 + TypeScript + Vite | PrimeVue 4 (Aura preset), Open Props tokens |
| Backend | FastAPI (`backend/app/`) | Port **8090**; Vite proxies `/api` |
| API contract | `openapi.json` | `User` schema for `/api/users` |
| Tests | Vitest + `@vue/test-utils` | `tests/unit/` smoke specs |

## Module map (current)

| Layer | Location | Status | Responsibility |
|-------|----------|--------|----------------|
| App shell | `src/App.vue` | ✅ exists | `<router-view>` wrapper; Open Props surface tokens |
| Router | `src/router/index.ts` | ⚠️ empty routes | Paths only — thin |
| Views / pages | `src/views/` | ❌ missing | Route UI only — no business rules |
| Components | `src/components/` | ❌ missing | Reusable UI; layout vs feature |
| Composables | `src/composables/` | ❌ missing | Client state + API calls (`useApi`, `useUsers`) |
| Types | `src/types/api.ts` | ❌ missing | OpenAPI-derived TS types |
| Backend | `backend/app/main.py` | ✅ exists | `/health`, `/api/users` inline handlers |
| Tests | `tests/unit/App.spec.ts` | ✅ exists | App shell smoke test |

## Data flow

1. User action in view
2. Composable or service call
3. API / store
4. Reactive UI update

## Boundaries (SOLID)

- **Single responsibility:** one reason to change per file
- **Open/closed:** extend via composables/wrappers, not forks
- **Dependency direction:** views → composables → services — not the reverse

## What not to build

See `reuse-catalog.md` before adding new abstractions.
