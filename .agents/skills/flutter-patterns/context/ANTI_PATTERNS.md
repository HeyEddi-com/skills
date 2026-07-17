# Anti-patterns: Flutter patterns

- No `Dio` calls inside `build()`.
- No guessing JSON field names: sync OpenAPI via `@dart-type-bridger` first.
- No Firebase Admin SDK in the Flutter client.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
