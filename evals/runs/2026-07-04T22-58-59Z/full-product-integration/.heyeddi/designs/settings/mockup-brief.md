# Mockup brief — Settings (TaskFlow)

Designer-eye description for frontend implementation. Authored from mockup PNGs — read before writing Vue.
Colors from `.heyeddi/design.md` + tokens, not PNG pixels.

## Audience (from product.md)

- **Primary persona:** Riley
- **Mindset:** Wants control over profile
- **Success feeling:** Clear settings, one obvious save
- **Register:** product · Direction: `heyeddi-design/reference/audience-design.md`

## Designer read (first impression)

Calm in-app settings — clear hierarchy, generous card padding, modern SaaS (Linear/Stripe density). Riley should see profile and notification controls at a glance with one obvious save action below the cards, not buried inside them.

## Layout topology

### Desktop
| Zone | Size / position | Behavior |
|------|-----------------|----------|
| App sidebar | 248px fixed left | Logo, nav pills, user chip pinned bottom |
| Top bar | 64px height | Page breadcrumb/title left; locale/actions right |
| Main content | max-width ~720px, padded | Page title + subtitle + card stack |
| Card stack | 16–24px gap | Elevated surfaces, 12px radius |
| Save CTA | below cards, right-aligned | Primary button outside card stack |

### Mobile
| Zone | Behavior |
|------|----------|
| Top bar | App name + menu toggle (sidebar drawer) |
| Content | Full-width cards, 16px horizontal inset |
| Primary CTA | Full-width save button below cards |

## Region map

### Desktop
| Region | What the user sees | Build |
|--------|-------------------|-------|
| Sidebar brand | TaskFlow + workspace label | Custom block in `AppSidebar` |
| Sidebar nav | Team + Settings with active pill | `RouterLink` rows in `AppSidebar` |
| User chip | Avatar, name, email pinned bottom | Bordered card, `margin-top: auto` |
| Top bar | Settings label + locale | `AppTopBar` |
| Page header | Settings title + subtitle | Route root in `SettingsView` |
| Profile card | Display name + email fields | PrimeVue `Card` `#content` + `InputText` |
| Notifications card | Email updates toggle row | Card `#content` + `ToggleSwitch` |
| Save CTA | "Save changes" primary button | PrimeVue `Button`, outside cards |

### Mobile
| Region | Build |
|--------|-------|
| Sidebar | Hidden; hamburger opens drawer overlay |
| Cards | Stack full-width with same `#content` slots |
| Save CTA | Full-width button below cards |

## Component build sheet
| Piece | Choice | Rationale |
|-------|--------|-----------|
| App chrome | `AppShell` + `AppSidebar` + `AppTopBar` | Sidebar layout from mockup; replaces horizontal `ProductNav` for app routes |
| Profile fields | PrimeVue `InputText` | Matches dashboard/login form patterns |
| Notifications | PrimeVue `ToggleSwitch` | Standard binary preference control |
| Save | PrimeVue `Button` severity primary | Verb-first CTA per product voice |
| User chip | Custom bordered block | Mockup shows avatar circle + name/email |

## Spacing & alignment (designer rules)

- Card internal padding: **≥ 24px** (`var(--size-6)` via `:deep(.p-card-body)`)
- Gap between cards: **24px** (`var(--size-6)`)
- Sidebar width token: **248px** (`--sidebar-width: 15.5rem`)
- Nav row min-height: **44px** with horizontal pill inset
- Save button **outside** card stack, not inside Profile card
- Content column max-width **720px** (`--content-max-width: 45rem`)

## Implementation spec

Measurable layout for the frontend dev — implement exactly; adjust tokens.css first.

| Component / region | Token or CSS rule | File(s) |
|--------------------|-------------------|---------|
| Sidebar width | `--sidebar-width: 15.5rem` | `src/styles/tokens.css`, `src/components/layout/AppSidebar.vue` |
| Top bar height | `--topbar-height: 4rem` | `src/styles/tokens.css`, `src/components/layout/AppTopBar.vue` |
| Content max-width | `--content-max-width: 45rem` | `src/styles/tokens.css`, `src/views/SettingsView.vue` |
| Sidebar column | `display:flex; flex-direction:column; min-height:100%` | `src/components/layout/AppSidebar.vue` |
| Nav scroll area | `flex: 1` on nav wrapper | `src/components/layout/AppSidebar.vue` |
| User chip pin | `margin-top: auto` on user block | `src/components/layout/AppSidebar.vue` |
| Nav active pill | `background: var(--brand-subtle); border-radius: var(--radius-2); padding: var(--size-2) var(--size-3)` | `src/components/layout/AppSidebar.vue` |
| App shell layout | `display:flex; min-height:100vh` with sidebar + main column | `src/components/layout/AppShell.vue` |
| Content padding | `padding: var(--size-6) var(--size-5)` on route root | `src/views/SettingsView.vue` |
| Card stack gap | `gap: var(--size-6)` | `src/views/SettingsView.vue` |
| Card body | `:deep(.p-card-body) { padding: var(--size-6) }` | `src/views/SettingsView.vue` |
| Card content slot | `<template #content>` for all body UI | `src/views/SettingsView.vue` |
| Save CTA | below cards; desktop `justify-content: flex-end`; `margin-top: var(--size-6)` | `src/views/SettingsView.vue` |

## Theme notes

- Light/dark coherent with app shell — see `heyeddi-design/reference/modern-reference.md`
- Avoid flat admin-template look: borders + surface-2 cards
- Active nav uses `brand-subtle` + `brand` text — not gray full-bleed highlight

## Responsive deltas
| Desktop | Mobile |
|---------|--------|
| Sidebar persistent 248px | Sidebar hidden; menu in top bar |
| Save button right-aligned | Save button full-width |
| Two-column shell | Single column stack |

## Anti-patterns (do not ship)

- Gray full-width active nav (use brand pill with inset)
- User chip floating mid-sidebar (missing `margin-top: auto`)
- Form fields outside Card `#content` slot (renders empty cards)
- Save button inside Profile card footer
- Cramped PrimeVue default card padding without override

## Frontend dev checklist

- [ ] Tokens updated before shell components
- [ ] `verify_handoff --phase shell --check` passes
- [ ] Profile + Notifications cards use `#content` slots
- [ ] Save CTA outside card stack with `settings__save` class
- [ ] `verify_handoff --phase full --check` + `verify_theme --check` pass
- [ ] Decision log appended to `design.md`

_Source route: `/settings` · Feature folder: `.heyeddi/designs/settings/`_
