# FastAPI backend (HeyEddi)

## Layout

```
backend/
  pyproject.toml
  app/main.py
  tests/
openapi.json          # frontend type generation (backend-type-bridger)
```

## Setup

```bash
scaffold_stack --stack fastapi
ensure_python
```

## Run API locally

```bash
cd backend
poetry run uvicorn app.main:app --reload --port 8090
```

- API: http://localhost:8090
- OpenAPI docs: http://localhost:8090/docs
- Health: http://localhost:8090/health

Port is declared in `.heyeddi/stack.json` as `"api_port": 8090` (HeyEddi default — avoids common :8000 conflicts).

Run Vue dev server separately on port 5173 — CORS is preconfigured.

## Tests

```bash
cd backend && poetry run pytest
# or: run_backend_tests from project-engineering
```

## Types for Vue

After API changes: `@backend-type-bridger` → `sync_openapi`
