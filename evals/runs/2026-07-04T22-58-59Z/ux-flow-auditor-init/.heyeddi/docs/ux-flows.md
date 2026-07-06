# UX flows index

**Last updated:** 2026-07-04

Task-oriented flow audits — click depth, friction, ease of use. Maintained by `@ux-flow-auditor`.

| Task ID | Goal | Route | Max clicks | Last run | Report |
|---------|------|-------|------------|----------|--------|
| update-profile | Change display name and save | /settings | 4 | — | [update-profile.md](ux-flows/update-profile.md) |

## How to add a flow

1. Add a row above
2. Create `ux-flows/<task-id>.flow.json` (see `update-profile.flow.json`)
3. Run `trace_flow.py --task-id <task-id> --check`

## Metrics

- **Click depth** — interactions from landing to success
- **Friction** — failed steps, hidden controls, extra navigation
- **Pass** — within `max_clicks` and all steps succeed
