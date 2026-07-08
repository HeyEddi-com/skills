@heyeddi-handoff @primevue-openprops-architect

## Settings handoff

Mockups: `.heyeddi/designs/settings/` (`desktop.png`, `mobile.png`).

### Pass 1 — Designer (no Vue)
1. `load_handoff` for `/settings`
2. Write `mockup-brief.md` with **Implementation spec** (sidebar 248px, nav pill, user chip pinned, Card `#content` slots)
3. `describe_handoff --sync-design`
4. **Stop** — announce designer pass done

### Pass 2 — Implementer
5. Shell → `verify_handoff --phase shell --check`
6. `SettingsView` → `verify_handoff --phase full --check` + `verify_theme --check`
7. Decision log in `design.md`; SettingsView unit test

**Unit tests:** Use `createViewRouter` from `tests/helpers/createViewRouter.ts` (not `createWebHistory`). **Before finishing:** fix any existing view specs (`LoginView.spec.ts`, `App.spec.ts`) so full `npm test` has **zero Vue Router warnings**.

**Scope:** `npm test` + `npm run build` only. **Do not** run `npm run dev`, Playwright, or `@visual-auditor` — the eval harness captures screenshots after this turn.
