# Design — TaskFlow

> Canonical design system for TaskFlow. Token source: OpenProps via `src/styles/tokens.css`.

## System

- **Stack:** OpenProps semantic tokens + PrimeVue Aura (indigo primary via `definePreset` in `main.ts`)
- **Registers:** `brand` for marketing (`/`, `/login`); `product` for app routes
- **Token source:** OpenProps aliases — `--surface-*`, `--text-*`, `--border-1`, `--brand`

## Foundations (always on)

- Responsive mobile-first (375 / 768 / 1440)
- System light/dark via `prefers-color-scheme`
- Locales: `en` (fallback) + `es` via `useLocale` composable
- WCAG 2.2 AA baseline — skip link, labels, focus-visible

## Components

| Component | Role | Notes |
|-----------|------|-------|
| `BrandShell` | Brand register layout | Skip link, nav, footer |
| `BrandNav` | Marketing header | Logo, features, sign-in, locale |
| `ProductShell` | Product register layout (legacy) | Skip link, app nav — superseded by AppShell for app routes |
| `ProductNav` | App header (legacy) | Team, settings, locale |
| `AppShell` | Product sidebar layout | Sidebar + top bar + main slot |
| `AppSidebar` | App navigation | 248px, nav pills, user chip pinned |
| `AppTopBar` | App top bar | Page title, locale, mobile menu |
| PrimeVue `Button` | Primary CTAs | Verb-first labels |
| PrimeVue `Card` | Elevated panels | Login auth card, dashboard stats/table |
| PrimeVue `DataTable` | Team roster | Striped rows, sortable columns |
| PrimeVue `InputText` / `Password` | Form fields | Full-width on login |
| PrimeVue `Checkbox` | Remember me | Binary |
| PrimeVue `Message` | Inline errors / banners | Login validation, offline demo |

## Layout / density rules

- **Brand:** max-width `--content-max` (72rem); hero editorial center; feature grid 3-col ≥768px
- **Login:** narrow `--content-narrow` (28rem); card padding `--size-5`
- **Product:** max-width `--content-max`; page padding `--size-5`; 2-col stat row ≥480px; table in elevated card

## Implemented surfaces

| Route | Status |
|-------|--------|
| `/` | Shipped — marketing home |
| `/login` | Shipped — sign-in |
| `/settings` | Shipped — profile + notifications handoff |
| `/dashboard` | Shipped — team roster |

## Decision log

### 2026-07-04 — taskflow-marketing `/` + `/login` (@heyeddi-design craft)

**Context:** Sam (evaluator) needs trustworthy marketing and simple sign-in without enterprise SSO noise.

**Audience:** Evaluator/buyer direction row — Vercel marketing hero rhythm + Stripe.com trust clarity.

**We chose:**
- `BrandShell` + `BrandNav` for shared brand chrome (custom — no PrimeVue app shell on marketing)
- Hero outcome headline emphasizing roster without PM sprawl (differentiation vs Asana/Trello boards)
- Subtle `--hero-glow` radial gradient on home — not stock-photo hero
- Login as single-column card with remember me + forgot password affordances (stub wiring)
- `en` + `es` via lightweight `useLocale` composable

**Component strategy:**
- Marketing features → custom elevated cards on `--surface-2`
- Login → PrimeVue `Card` + form primitives
- CTA → PrimeVue `Button` inside `RouterLink`

**We rejected:**
- Split-panel login with marketing sidebar (Sam is already trial-ready on `/login`)
- SSO row on v1 (anti-audience enterprise IT; deferred)
- Generic 3-tile KPI marketing pattern

**Deferred wiring:** Auth API, forgot-password email, remember-me persistence policy.

**Open questions:** none

### 2026-07-04 — taskflow-dashboard `/dashboard` (@heyeddi-design craft)

**Context:** Jordan (team lead) needs team roster at a glance on Monday morning — calm density, not KPI theater.

**Audience:** B2B team lead direction row — Stripe Dashboard table hierarchy + Linear app chrome.

**We chose:**
- `ProductShell` + `ProductNav` for focused app chrome (Team + Settings)
- Primary content = PrimeVue `DataTable` roster via `useUsers()`
- Optional 2 stat cards (member count, data source) — not 3-tile KPI grid
- Offline demo fallback with warn banner when API unavailable (eval + local dev resilience)
- Refresh as sole header secondary action

**Component strategy:**
- Stats + table → PrimeVue `Card` on `--surface-2` with border + subtle shadow
- Roster → `DataTable` striped, sortable email/id columns
- Offline → PrimeVue `Message` severity warn

**We rejected:**
- 3-tile KPI dashboard (anti-reference in product.md)
- Generic unstyled admin table without elevation
- Silent failure when API down

**Deferred wiring:** Auth guard, row actions, status/capacity columns, invite flow.

**Open questions:** none

### 2026-07-04 — settings `/settings` (@heyeddi-handoff)

**Context:** Riley needs clear profile and notification controls with one obvious save action — sidebar app chrome from handoff mockups.

**Audience:** IC contributor direction row — Linear app chrome + Stripe settings card density.

**We chose:**
- `AppShell` + `AppSidebar` (248px) + `AppTopBar` replacing horizontal `ProductNav` for app routes
- Sidebar nav pills with `brand-subtle` active state; user chip pinned via `margin-top: auto`
- Profile + Notifications as elevated PrimeVue `Card` stacks with `#content` slots
- Save CTA outside cards, right-aligned desktop / full-width mobile
- Demo profile data (Alex Rivera) until auth wiring lands

**Component strategy:**
- Shell → custom sidebar/topbar on semantic tokens (`--sidebar-width`, `--topbar-height`)
- Profile fields → PrimeVue `InputText` in Card `#content`
- Notifications → PrimeVue `ToggleSwitch` row in Card `#content`
- Save → PrimeVue `Button` in `settings__save` block below card stack

**We rejected:**
- Save button inside Profile card footer
- Gray full-bleed active nav highlight
- Keeping horizontal-only `ProductNav` for settings (mockup specifies sidebar)

**Deferred wiring:** Persist settings to API, auth-linked profile, push notification channels.

**Open questions:** none

## Layout — settings handoff (2026-07-04)

**Route:** `/settings` · **App:** TaskFlow

### Layout topology

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

### Region map

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

### Component build sheet

| Piece | Choice | Rationale |
|-------|--------|-----------|
| App chrome | `AppShell` + `AppSidebar` + `AppTopBar` | Sidebar layout from mockup; replaces horizontal `ProductNav` for app routes |
| Profile fields | PrimeVue `InputText` | Matches dashboard/login form patterns |
| Notifications | PrimeVue `ToggleSwitch` | Standard binary preference control |
| Save | PrimeVue `Button` severity primary | Verb-first CTA per product voice |
| User chip | Custom bordered block | Mockup shows avatar circle + name/email |

**Source:** `.heyeddi/designs/settings/mockup-brief.md` — implement from this brief; PNGs are spatial checks only.
