@flutter-engineering on a thin Flutter repo:

1. Run `audit_scaffold` and read gaps.
2. Run `scaffold_stack --stack full` (flutter + fastapi) if anything missing.
   `@project-engineering` is installed — FastAPI scaffold must succeed (backend/, openapi.json).
3. Run `ensure_flutter` when pubspec exists.
4. Run `dev_server_info --route /settings` and report URLs (web :8085, API :8090).
5. Do **not** start long-running servers in this turn.

Read all scaffold output JSON. Confirm `.heyeddi/stack.json` has `"frontend": "flutter"` and backends include fastapi.
Re-run `audit_scaffold` after scaffold and report status.
