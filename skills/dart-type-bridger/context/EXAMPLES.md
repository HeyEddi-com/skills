# Examples

## Sync Dart models from local OpenAPI

```bash
curl -fsS http://127.0.0.1:8090/openapi.json -o openapi.json
python scripts/sync_openapi.py --project-root .
```

## Firestore hints

```bash
python scripts/fetch_firestore_schema.py --project-root .
```
