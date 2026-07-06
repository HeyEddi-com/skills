# Low-fidelity mockups — wireframe / ASCII / sketch

Handoff works from **layout intent**, not only polished PNGs. The agent **interprets** structure and produces the same `mockup-brief.md` + Implementation spec — then implements with `design.md` tokens.

## Supported inputs

| Fidelity | Files | Agent reads |
|----------|-------|-------------|
| **Polished PNG** | `desktop.png`, `mobile.png` | Vision + `interpret-mockups.md` |
| **ASCII / markdown wireframe** | `wireframe.md`, `wireframe-desktop.md` | Text regions + topology |
| **Sketch / photo** | `sketch.png`, `whiteboard.jpg` | Vision; treat as layout-only (same as PNG contract) |

`load_handoff.py` sets `mode: wireframe` when `wireframe.md` exists (with or without PNGs).

## Workflow (wireframe)

1. `load_handoff` — note `fidelity: wireframe`, `interpret_required: true`.
2. Read `wireframe.md` (+ optional sketch PNG). **Do not expect pixel color or polish.**
3. Write `mockup-brief.md` — **extra detail** on regions, spacing, and component choices because wireframes are ambiguous.
4. In brief, state **assumptions** explicitly (e.g. "ASCII shows table → PrimeVue DataTable").
5. `describe_handoff --sync-design` → implementer pass per `handoff-to-code.md`.
6. Theme coherence per `theme-coherence.md`.

## Wireframe.md template

```markdown
# Wireframe — <Feature>

Fidelity: wireframe (layout only). Colors from design.md.

## Desktop (ASCII)

\`\`\`
+--sidebar--+-- main ----------------------------------+
| Logo       | Topbar [ search........ ] [avatar]     |
| Nav        | Title: Dashboard                       |
| - Dash *   | +----------------+ +----------------+  |
| - Team     | | Stat: Users 12 | | Stat: Open  3  |  |
|            | +----------------+ +----------------+  |
|            | Recent items (table)                   |
| [user]     | [ Primary action ]                     |
+------------+----------------------------------------+
\`\`\`

## Mobile

\`\`\`
[≡] App    [A]
Dashboard
[ stat ][ stat ]
[ table rows... ]
[ Primary action full width ]
\`\`\`

## Regions (required)
| Region | Desktop | Mobile | Suggested component |
|--------|---------|--------|---------------------|
| ... | ... | ... | Card / DataTable / Button |
```

## Generalization expectation

Wireframes test whether the agent can **infer** production UI from sparse input:

- ASCII box → `Card` or custom panel
- `[ table ]` → `DataTable` with columns from labels
- `[ search ]` → `InputText` in top bar
- `*` on nav → active route styling

Wireframe inputs are supported by the skill; run handoff manually or extend `eval-integration` — dedicated wireframe eval cases were removed (2026-07-04).
