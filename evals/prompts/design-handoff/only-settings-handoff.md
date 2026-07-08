@heyeddi-handoff @primevue-openprops-architect

**Goal:** Implement `/settings` from mockups in `.heyeddi/designs/settings/`.

## Two passes (do not merge)

### Pass 1 — Designer
1. `load_handoff` for `/settings`
2. Study `desktop.png` + `mobile.png`; write `mockup-brief.md` per `interpret-mockups.md`
3. **Required:** `## Implementation spec` table — sidebar 248px (`--sidebar-width: 15.5rem`), top bar 64px, nav pill inset, `margin-top: auto` on user chip, card `:deep(.p-card-body)` padding, gap between cards
4. `describe_handoff --sync-design`
5. **Stop** — announce designer pass done before any `.vue` files

### Pass 2 — Implementer
6. Read `handoff-to-code.md` + Implementation spec; update `tokens.css` (no `--size-N: var(--size-N)` aliases)
7. Build `AppShell` → `AppSidebar` → `AppTopBar` → `verify_tokens --check` → `verify_handoff --phase shell --check`
8. Build `SettingsView` → `verify_handoff --phase full --check`
9. Decision log in `design.md`

**Scope:** `npm test` + `npm run build` pass. No Playwright/dev in agent turn.
