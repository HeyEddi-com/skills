You are on a Vue + FastAPI project.

## 1. Project engineering

1. Run `audit_scaffold`.
2. Run `scaffold_stack --stack auto` if anything is incomplete.
3. Run `ensure_npm` and `ensure_python` — **must report `status: ok`** (fix `backend/pyproject.toml` if Poetry fails; do not use `--no-root` workarounds).
4. Run `dev_server_info` (Vue :5173 + API :8090).

## 2. Backend type bridger

1. Run `sync_openapi` (openapi.json at project root).
2. Ensure `src/types/api.ts` has TypeScript interfaces for the `User` schema from OpenAPI.

## 3. Composable patterns

1. Read `context/fastapi-jwt.md` (or project auth pattern).
2. Create `src/composables/useUsers.ts` as a **`useUsers()` composable** (not a bare `fetchUsers` export):
   - `loading` / `error` refs
   - typed `User[]` from `@/types/api`
   - `fetch()` against `/api/users` with error handling
3. Run `validate_composable.py --path src/composables/useUsers.ts --check` — must pass.

Implement files. Run `run_backend_tests` if backend was scaffolded. Finish when `npm test`, `npm run build`, and backend pytest pass.
