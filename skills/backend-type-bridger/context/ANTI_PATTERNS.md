
# Anti-patterns: Type bridger

- NEVER guess API response fields without syncing OpenAPI.
- NEVER use `any` for API payloads when types can be generated.
- NEVER pass a remote `--url` into `sync_openapi`: write `openapi.json` to disk first, then sync from the local file.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
