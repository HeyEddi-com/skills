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

## Layout — settings handoff (2026-07-04)

**Route:** `/settings` · **App:** SecureVault

### Layout topology

### Desktop

| Zone | Size / position | Behavior |
|------|-----------------|----------|
| App sidebar | Fixed left, `--sidebar-width` (248px) | Full viewport height; brand + nav scroll area + user chip pinned bottom |
| App top bar | Full width minus sidebar, `--topbar-height` (64px) | Fixed at top of main column; breadcrumb left, search + avatar right |
| Main content | Remaining width, max `--content-max-width` (~720px) | Scrolls vertically; padded route root |
| Settings cards | Stacked in content column | Profile card, Notifications card, gap between |
| Save CTA | Below card stack, right-aligned | Outside cards; not inside Card footer |

### Mobile

| Zone | Behavior |
|------|----------|
| Sidebar | Hidden off-canvas; hamburger in top bar opens drawer |
| Top bar | Full width; hamburger + "SecureVault" center + avatar |
| Content | Single column; page header + cards stack |
| Save CTA | Full-width button at bottom of content area |

### Region map

### Desktop

| Region | What the user sees | Build |
|--------|-------------------|-------|
| Sidebar brand | "SecureVault" + "Workspace" subtitle | Custom in `AppSidebar` |
| Sidebar nav | Dashboard, Documents, Team, Settings links | Custom nav list with active pill on Settings |
| Sidebar user chip | Avatar "A", Alex Rivera, alex@example.com in bordered card | Custom; pinned with `margin-top: auto` |
| Top bar breadcrumb | "Settings" label | `AppTopBar` |
| Top bar search | Rounded search input "Search…" | PrimeVue `InputText` |
| Top bar avatar | Blue circle | Custom avatar |
| Page header | "Settings" title + "Manage your profile and how we reach you." | Route root in `SettingsView` |
| Profile card | Title, subtitle, Display name + Email fields | PrimeVue `Card` + `InputText` in `#content` |
| Notifications card | Title, subtitle, Email updates row + toggle | PrimeVue `Card` + `ToggleSwitch` in `#content` |
| Save CTA | "Save changes" primary button | PrimeVue `Button`; below cards |

### Mobile

| Region | Build |
|--------|-------|
| Hamburger | `AppTopBar` menu button toggles sidebar drawer |
| Page subtitle | Shortened: "Profile and notifications" |
| Notifications card | Empty state copy: "No channels configured" + hint |
| Save CTA | Full-width `Button` at bottom |

### Component build sheet

| Piece | Choice | Rationale |
|-------|--------|-----------|
| App shell | `AppShell` composes sidebar + main column | Reusable layout for all routes |
| Sidebar | `AppSidebar` flex column | Nav scroll + user chip pinned bottom |
| Top bar | `AppTopBar` fixed height | Consistent chrome across routes |
| Settings cards | PrimeVue `Card` with `#title`, `#subtitle`, `#content` | Card slots required — body in `#content` only |
| Form fields | PrimeVue `InputText` | Catalog component; token-backed borders |
| Toggle | PrimeVue `ToggleSwitch` | Notifications preference |
| Save action | PrimeVue `Button` severity primary | Detached below card stack |

**Source:** `.heyeddi/designs/settings/mockup-brief.md` — implement from this brief; PNGs are spatial checks only.

## Decision log (2026-07-04)

| Region | Component | Rationale |
|--------|-----------|-----------|
| App layout | `AppShell` | Composes sidebar + main column; mobile backdrop for drawer |
| Sidebar brand + nav | `AppSidebar` | Flex column with `flex: 1` nav and `margin-top: auto` user chip per spec |
| Active nav | `.nav-link--active` pill | `brand-subtle` background with horizontal inset — not full-bleed gray |
| User chip | Custom bordered block in sidebar | Avatar + name/email; pinned bottom with border on `surface-3` |
| Top bar | `AppTopBar` | 64px height; breadcrumb/search/avatar desktop; hamburger + brand mobile |
| Settings page | `SettingsView` | Max-width content column; page header outside cards |
| Profile fields | PrimeVue `Card` + `InputText` in `#content` | Card slots required; fields inside `#content` slot |
| Notifications | PrimeVue `Card` + `ToggleSwitch` | Desktop toggle row; mobile empty-state copy per responsive delta |
| Save action | PrimeVue `Button` in `.settings__save` | Detached below card stack; right-aligned desktop, full-width mobile |
| Layout tokens | `tokens.css` | `--sidebar-width: 15.5rem`, `--topbar-height: 4rem`, `--content-max-width: 45rem` |
