# Design (eval handoff)

Draft — `@heyeddi-handoff` should align implementation with this file and update component/layout notes.

## System

- Semantic tokens in `src/styles/tokens.css` — **OpenProps** on HeyEddi scaffold (`open-props` in `package.json`); custom `:root` vars OK on brownfield. See `heyeddi-design/reference/token-strategy.md`.
- PrimeVue for UI primitives — wire Aura preset to project brand token (not mockup PNG colors).
- **Component catalog:** `AppShell`, `AppSidebar`, `AppTopBar`, `Card`, `InputText`, `Button`, `ToggleSwitch`

## Settings mockups

`.heyeddi/designs/settings/` — designer attachments for SecureVault:
- `desktop.png` / `mobile.png` — layout references (regenerate: `uv run poe mockups`)
- `handoff.json` — route + contract notes only

**The skill authors `mockup-brief.md`** by interpreting the PNGs (`reference/interpret-mockups.md`), then syncs layout into this file via `describe_handoff --sync-design`.

**Mockup contract:** PNGs show **where** regions go. **Colors** come from this file and `tokens.css` — do not sample hues from PNG pixels.
