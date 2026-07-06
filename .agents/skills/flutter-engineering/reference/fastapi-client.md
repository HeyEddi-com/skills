# FastAPI client — Flutter

1. Sync types: `@dart-type-bridger` → `lib/models/api_models.dart`
2. Use `ApiClient` in `lib/services/api_client.dart` (Dio, base `kApiBaseUrl`)
3. Repositories in `lib/repositories/` — no raw Dio in widgets
4. Riverpod providers in `lib/providers/` expose async data to screens

Default API: `http://127.0.0.1:8090` (see `.heyeddi/stack.json` `api_port`).
