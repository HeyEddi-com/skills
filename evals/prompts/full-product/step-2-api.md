@backend-type-bridger @composable-patterns

The FastAPI backend and `openapi.json` are in this repo. We need the **frontend data layer** so views can load users from the API.

Follow each skill's process: sync types from OpenAPI, use composable patterns from your context docs, add tests. Document any API assumptions in code comments if schema is ambiguous.

**Scope:** backend pytest only (`cd backend && poetry run pytest -q`). **Do not** start a long-running `uvicorn` — API default port is **8090** (see `.heyeddi/stack.json`), not 8000.
