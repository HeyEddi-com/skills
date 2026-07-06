# Reuse catalog

**Last updated:** 2026-07-04

**DRY rule:** search this file before creating a new component, composable, or helper.

| Name | Path | Use when |
|------|------|----------|
| App shell | `src/App.vue` | Root layout; wrap all routes in `<main class="app-shell">` |
| Design tokens | `src/styles/tokens.css` | Open Props CSS variables for surface/text colors |
| PrimeVue preset | `src/main.ts` (`HeyEddiAura`) | Theme config — extend here, do not duplicate per view |
| Router factory | `src/router/index.ts` | Add routes; keep file thin |
| FastAPI app | `backend/app/main.py` | Health + users endpoints; extract routers when >2 domains |
| Test router helper | `tests/helpers/createViewRouter.ts` | Mount views with memory history in specs |
| User schema | `openapi.json` → `#/components/schemas/User` | Source of truth for `src/types/api.ts` |

## Patterns to prefer

- Shared UI: `src/components/ui/` before new PrimeVue wrappers
- API access: one composable per domain (`useUsers`, `useTasks`)
- Layout: `AppShell`, `AppSidebar`, `AppTopBar` — do not duplicate shell markup per route

## Anti-patterns

- Copy-pasting a Card+form block across views → extract wrapper
- Second `api.ts` fetch helper → extend existing composable
