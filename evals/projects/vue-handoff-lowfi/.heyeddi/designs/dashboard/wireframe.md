# Wireframe — Dashboard

Fidelity: **wireframe** (layout only). Colors from `.heyeddi/design.md` tokens.

## Desktop (ASCII)

```
+--sidebar------+-- main ----------------------------------------+
| SecureVault  | Topbar [ search............... ] [avatar A]     |
| Workspace    |                                                 |
| > Dashboard *|  Dashboard                                      |
|   Team       |  Welcome back — here's your workspace.          |
|   Settings   |  +-------------+ +-------------+ +-------------+ |
|              |  | Open tasks  | | Done today  | | Team online | |
|              |  |     12      | |      8      | |      4      | |
|              |  +-------------+ +-------------+ +-------------+ |
|              |  Recent activity (table)                        |
|              |  | Item          | Status   | Updated          | |
|              |  | Deploy API    | Done     | 2h ago           | |
|              |  | Review PR #42 | Open     | 1d ago           | |
| [user chip]  |  [ New task ]  (primary, left under table)     |
+--------------+-------------------------------------------------+
```

## Mobile (ASCII)

```
[≡] SecureVault                              [A]
Dashboard
Welcome back
[ Open 12 ] [ Done 8 ] [ Team 4 ]   <- stat cards stack or 2-col
Recent activity
- Deploy API — Done
- Review PR #42 — Open
[ New task ]  full width
```

## Regions

| Region | Desktop | Mobile | Suggested component |
|--------|---------|--------|---------------------|
| Stat row | 3 equal cards | stack or 2+1 | PrimeVue `Card` |
| Activity | DataTable 3 cols | stacked list | `DataTable` or list |
| Primary CTA | below table, left | full width | `Button` primary |
| Page title | h1 + subtitle | same | typography tokens |

## Notes

- Reuse existing `AppShell` from settings handoff if present
- No mockup colors — use design system surfaces
