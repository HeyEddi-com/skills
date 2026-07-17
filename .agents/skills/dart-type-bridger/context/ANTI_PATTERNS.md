# Anti-patterns

- Never use `dynamic` for API payloads when schemas exist.
- Never guess field names without running `sync_openapi`.
- Never pass a remote `--url` into `sync_openapi`: write `openapi.json` to disk first, then sync from the local file.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
