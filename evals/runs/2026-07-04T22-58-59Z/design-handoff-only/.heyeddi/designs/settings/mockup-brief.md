# Mockup brief — Settings (SecureVault)

Designer-eye description for frontend implementation. Authored from mockup PNGs — read before writing Vue.
Colors from `.heyeddi/design.md` + tokens, not PNG pixels.

## Designer read (first impression)

SecureVault Settings is a calm, in-app account page — not a marketing surface. The shell (sidebar + top bar) frames a narrow content column with two stacked cards and a detached save action. Hierarchy is clear: page title and subtitle first, then profile fields, then notification preference, then primary CTA below the cards. Desktop feels spacious; mobile compresses to a single column with the sidebar hidden behind a hamburger and a full-width save button pinned at the bottom.

## Layout topology

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

## Region map

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

## Component build sheet

| Piece | Choice | Rationale |
|-------|--------|-----------|
| App shell | `AppShell` composes sidebar + main column | Reusable layout for all routes |
| Sidebar | `AppSidebar` flex column | Nav scroll + user chip pinned bottom |
| Top bar | `AppTopBar` fixed height | Consistent chrome across routes |
| Settings cards | PrimeVue `Card` with `#title`, `#subtitle`, `#content` | Card slots required — body in `#content` only |
| Form fields | PrimeVue `InputText` | Catalog component; token-backed borders |
| Toggle | PrimeVue `ToggleSwitch` | Notifications preference |
| Save action | PrimeVue `Button` severity primary | Detached below card stack |

## Spacing & alignment (designer rules)

- Sidebar nav items: min-height 44px; active pill inset horizontally from sidebar edges (`padding-inline: var(--size-3)`).
- User chip sits at sidebar bottom — never floats mid-column.
- Content column centered with max-width; horizontal padding on route root.
- Card stack uses consistent vertical gap (`var(--size-6)`).
- Card internal padding overrides PrimeVue default — use `:deep(.p-card-body) { padding: var(--size-6) }`.
- Save button: `margin-top: var(--size-6)` below cards; desktop right-aligned (`justify-content: flex-end`).
- Active nav uses brand subtle background — not gray surface fill.

## Implementation spec

Measurable layout for the frontend dev — implement exactly; adjust tokens.css first.

| Component / region | Token or CSS rule | File(s) |
|--------------------|-------------------|---------|
| Sidebar width | `--sidebar-width: 15.5rem` (248px) | `src/styles/tokens.css`, `src/components/layout/AppSidebar.vue` |
| Sidebar column | `display: flex; flex-direction: column; min-height: 100%` | `src/components/layout/AppSidebar.vue` |
| Nav scroll area | `flex: 1` on nav wrapper | `src/components/layout/AppSidebar.vue` |
| User chip pin | `margin-top: auto` on user block | `src/components/layout/AppSidebar.vue` |
| Nav row height | `min-height: 2.75rem` (44px) | `src/components/layout/AppSidebar.vue` |
| Nav active pill | `background: var(--brand-subtle); color: var(--brand); border-radius: var(--radius-2); padding: var(--size-2) var(--size-3); padding-inline: var(--size-3)` with horizontal inset | `src/components/layout/AppSidebar.vue` |
| Top bar height | `--topbar-height: 4rem` (64px); `height: var(--topbar-height)` | `src/styles/tokens.css`, `src/components/layout/AppTopBar.vue` |
| Content max-width | `--content-max-width: 45rem` (~720px) | `src/styles/tokens.css`, `src/views/SettingsView.vue` |
| Content padding | `padding: var(--size-6) var(--size-5)` on route root | `src/views/SettingsView.vue` |
| Card stack gap | `gap: var(--size-6)` on `.settings__cards` | `src/views/SettingsView.vue` |
| Card body padding | `:deep(.p-card-body) { padding: var(--size-6) }` | `src/views/SettingsView.vue` |
| Save CTA | below cards; desktop `justify-content: flex-end`; `margin-top: var(--size-6)` on `.settings__save` | `src/views/SettingsView.vue` |
| User chip | bordered card (`border: 1px solid var(--surface-3)`), avatar circle, pinned bottom | `src/components/layout/AppSidebar.vue` |

## Theme notes

- Colors from `tokens.css` semantic tokens (`--brand`, `--brand-subtle`, `--surface-*`, `--text-*`).
- PrimeVue Aura preset wired in `main.ts`; Card/Input surfaces follow token overrides in `tokens.css`.
- Do not sample hex from PNG pixels.

## Responsive deltas

| Desktop | Mobile |
|---------|--------|
| Persistent sidebar 248px | Sidebar hidden; hamburger opens drawer |
| Top bar: breadcrumb + search + avatar | Top bar: hamburger + brand + avatar |
| Full subtitle: "Manage your profile and how we reach you." | Short subtitle: "Profile and notifications" |
| Notifications: toggle row | Notifications: empty-state copy |
| Save button right-aligned below cards | Save button full-width at bottom |

## Anti-patterns (do not ship)

- Gray or full-bleed active nav highlight — use brand-subtle pill with horizontal inset.
- User chip floating mid-sidebar — must use `margin-top: auto`.
- Form fields outside Card `#content` slot — PrimeVue drops loose children.
- Save button inside Card footer — CTA belongs below the card stack.
- Same-name token aliases (`--size-6: var(--size-6)`) — breaks spacing cascade.
- Sampling colors from PNG pixels instead of design tokens.

## Frontend dev checklist

- [ ] `tokens.css` updated with layout tokens (no self-referencing aliases)
- [ ] `AppShell` → `AppSidebar` → `AppTopBar` built and wired in router/App
- [ ] `verify_handoff --phase shell --check` passes
- [ ] `SettingsView` with Profile + Notifications cards using `#content` slots
- [ ] Card padding and stack gap per spec
- [ ] Save CTA outside cards, right-aligned on desktop
- [ ] `verify_handoff --phase full --check` passes
- [ ] `npm test` and `npm run build` pass
- [ ] Decision log appended to `design.md`
