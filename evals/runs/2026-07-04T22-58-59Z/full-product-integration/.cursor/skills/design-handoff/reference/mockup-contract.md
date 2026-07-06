# Mockup contract — layout only

Handoff PNGs are **spatial references**, not pixel-perfect color specs. Colors, typography, and component chrome come from **`.heyeddi/design.md`** and project semantic tokens (`tokens.css`) — never sampled from mockup hex values. **OpenProps is optional** — see `heyeddi-design/reference/token-strategy.md`.

## What mockups define

| Mockup shows | Implement as |
|--------------|--------------|
| App shell topology | **Layout components** — `AppShell`, `AppSidebar`, `AppTopBar` (or catalog equivalents in `design.md`) |
| Sidebar + main column (desktop) | Flex/grid shell; sidebar fixed width; main scrolls |
| Top bar only (mobile) | Hide sidebar; hamburger + logo + avatar in top bar |
| Content regions (cards, sections) | PrimeVue `Card`, `Panel`, or named catalog wrappers — **not** bare headings on a flat page |
| Field order and labels | `InputText`, `Select`, etc. in the same order as the mockup |
| CTA placement | Button position (right-aligned desktop, full-width mobile) — label from brief/notes |
| Responsive deltas | What stacks, hides, or swaps (e.g. toggle on desktop → empty state on mobile) |
| Active nav / page title | Which route is highlighted; page `h1` text |

## What mockups do **not** define

- Brand primary hue, button color, toggle color — use `{colors.primary}` / PrimeVue theme wired to tokens
- Exact shadow, border radius, font family — use `design.md` **Components** and **Typography**
- Mockup generator palette (e.g. blue in eval PNGs) is **illustrative layout only**

## Implementation rules

1. **Shell first** — if the mockup shows in-app UI (sidebar, top bar), implement or reuse layout components **before** route content. Never ship route-only HTML on a gray background.
2. **Component strategy (FE dev hat)** — for every mockup region, explicitly choose one path and document it:

| Situation | Choose |
|-----------|--------|
| Catalog has `SettingsSection`, `PageHeader`, `AppShell`, … | **Reuse** — import from `@/components/` |
| Standard form/table/dialog pattern | **PrimeVue as-is** — `Card`, `InputText`, `DataTable`, `Dialog`, … |
| Repeated pattern across routes, minor token styling | **Thin wrapper** — e.g. `UiSettingsCard.vue` composing PrimeVue + slots |
| PrimeVue layout/behavior doesn't fit (split pane, custom nav rail, complex responsive swap) | **Custom component** — new `.vue` under `src/components/`; register in `design.md` **Components** |

3. **Styling** — use project semantic tokens (`var(--surface-*)`, `var(--brand)`). OpenProps only if the project already has `open-props` installed; do not add it otherwise (`heyeddi-design/reference/token-strategy.md`).
4. **PrimeVue + tokens** — when using PrimeVue, wire Aura preset to project brand/surface tokens in `main.ts` / `tokens.css`.
5. **Catalog before inventing** — check `design.md` **Components** and `@/components/` before creating anything new.
6. **Region mapping** — in Decision log, document mockup **regions → component names + build choice** (reuse / PrimeVue / wrapper / custom), not hex values:
   > Desktop left rail → `AppSidebar` (custom layout); Profile block → PrimeVue `Card` + `InputText` ×2; Save CTA → `Button` primary; Notifications row → `ToggleSwitch` (PrimeVue sufficient).
7. **Visual audit** — `@visual-auditor` compares **layout hierarchy** (shell, cards, field stack, CTA position). Pass when regions align; **do not** fail because primary button hue differs from PNG.

## Anti-patterns

- Bare `<form>` / unstyled inputs on `body` background when mockup shows cards in a shell
- Copying mockup colors into CSS instead of `design.md` tokens
- Skipping layout components because “the route is just settings”
- Default Aura green primary left unwired when `design.md` defines `{colors.primary}`
- Using PrimeVue when it fights the layout — build a custom component instead of hacking CSS
- Creating custom components when catalog or PrimeVue already covers the pattern
- Adding `open-props` mid-project when `package.json` has no `open-props` and `design.md` does not specify it

See `reference/screenshot-mode.md` for the step-by-step workflow and `reference/interpret-mockups.md` for the mandatory **mockup-brief.md** step before coding.
