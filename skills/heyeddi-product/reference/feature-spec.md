# Feature spec schema — `write_feature_spec --json`

```json
{
  "route": "/dashboard",
  "title": "Team roster dashboard",
  "problem": "Jordan needs team status in seconds on Monday morning without opening three tools.",
  "user_stories": [
    "As Jordan (team lead), I want to see who is active and blocked so that I can unblock work before standup.",
    "As Riley (IC), I want to scan the roster without clicking into each person so that I stay in flow."
  ],
  "acceptance_criteria": [
    "Dashboard loads roster from GET /api/users within 2s on dev build",
    "Table shows name, role, status — no empty placeholder rows",
    "Jordan completes 'see team status' in ≤3 clicks from /login (ux-flow trace)",
    "Primary persona success feeling from product.md is met per design critique"
  ],
  "success_metric": "Jordan rates 'found blockers' in first session (qualitative) or trace_flow passes",
  "alternatives_considered": [
    "KPI stat cards — rejected; job is roster not analytics",
    "Kanban board — out of scope per anti_audience"
  ],
  "out_of_scope": ["Filtering", "SSO", "Export CSV"]
}
```

Acceptance criteria must be **testable** — trace_flow, API contract, contrast audit, or explicit manual check.
