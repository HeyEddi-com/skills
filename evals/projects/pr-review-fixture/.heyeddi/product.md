# TaskFlow — eval fixture

## Personas

| Persona | Role | Primary job |
|---------|------|-------------|
| Alex | Team lead | See who is on the roster |

## Per-route intent

| Route | Purpose |
|-------|---------|
| `/dashboard` | Roster table — list team members from API |

## Pages

| Route | View | Purpose |
|-------|------|---------|
| `/dashboard` | DashboardView | Team roster |

## Acceptance criteria

- `/dashboard` loads users from `useUsers` composable
- API returns paginated user list (1-based page index)
