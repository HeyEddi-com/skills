# Examples

## Sync types from local OpenAPI

```bash
# Prefer existing scaffold file. Refresh from a running API only by writing a file:
curl -fsS http://127.0.0.1:8090/openapi.json -o openapi.json

python scripts/sync_openapi.py --project-root .
# optional: python scripts/sync_openapi.py --project-root . --openapi docs/openapi.json
```

## Firestore hints

```bash
python scripts/fetch_firestore_schema.py --project-root .
```
