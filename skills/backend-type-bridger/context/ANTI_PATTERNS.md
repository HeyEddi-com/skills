
# Anti-patterns — Type bridger

- NEVER guess API response fields without syncing OpenAPI.
- NEVER use `any` for API payloads when types can be generated.
- NEVER pass a remote `--url` into `sync_openapi` — write `openapi.json` to disk first, then sync from the local file.
