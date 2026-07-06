# Engineering decisions

**Last updated:** 2026-07-04

Engineering ADRs — separate from the **Design Decision log** in `.heyeddi/design.md`.

## Template

```markdown
### YYYY-MM-DD — Title

**Context:** …
**Decision:** …
**Consequences:** …
```

### 2026-07-04 — Composable-based API access

**Context:** TaskFlow views (Dashboard, Settings) need data from FastAPI on port 8090 via Vite proxy. Inline fetch in views duplicates URL handling, error parsing, and loading state; product spec requires useUsers and useApi composables.

**Decision:** All HTTP access goes through src/composables/useApi.ts (base URL + fetch wrapper) and domain composables (e.g. useUsers.ts). Views call composables only — no direct fetch in .vue files.

**Consequences:** New endpoints get a typed composable and reuse useApi; tests mock composables instead of global fetch. Backend remains thin; business rules stay in composables until a second consumer justifies a service module.

