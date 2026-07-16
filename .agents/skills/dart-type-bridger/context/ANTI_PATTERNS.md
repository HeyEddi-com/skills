# Anti-patterns

- Never use `dynamic` for API payloads when schemas exist.
- Never guess field names without running `sync_openapi`.
- Never pass a remote `--url` into `sync_openapi` — write `openapi.json` to disk first, then sync from the local file.
