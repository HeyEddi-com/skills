@flutter-engineering @dart-type-bridger @flutter-patterns on the Flutter + FastAPI template:

1. `audit_scaffold` → `sync_openapi` from root `openapi.json`.
2. Create `lib/repositories/users_repository.dart` and `lib/providers/users_provider.dart` using generated `User` model from `lib/models/api_models.dart`.
3. Wire `usersProvider` into a simple list on home or settings screen (demo/empty when API down).
4. Run `verify_build --skip-build` if Flutter SDK available; otherwise stop after files written.

Do not start uvicorn. Read all changed Dart files.
