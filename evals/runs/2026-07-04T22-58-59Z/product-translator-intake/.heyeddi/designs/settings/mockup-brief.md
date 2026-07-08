# Mockup brief — Settings (TaskFlow)

Authored by `@heyeddi-intake` from user intent + layout mockups. Colors from `.heyeddi/design.md` tokens — not PNG pixels.

## Audience (from product.md)

- **Primary persona:** Riley
- **Mindset:** Wants control over profile and notifications
- **Success feeling:** Clear settings, one obvious save
- **Register:** product · Direction: `heyeddi-design/reference/audience-design.md`

## Designer read (first impression)

Calm in-app settings — clear hierarchy, generous card padding, modern SaaS (Linear/Stripe density).

## Layout topology

### Desktop
| Zone | Size / position | Behavior |
|------|-----------------|----------|
| App sidebar | 248px fixed left | Logo, nav pills, user chip pinned bottom |
| Main content | max-width ~720px, padded | Page title + card stack |
| Stat / cards | 16px gap | Elevated surfaces, 12px radius |

### Mobile
| Zone | Behavior |
|------|----------|
| Top bar | App name + menu |
| Content | Full-width cards, 16px horizontal inset |
| Primary CTA | Full-width or pinned bottom |

## Region map

### Desktop
| Region | What the user sees | Build |
|--------|-------------------|-------|
| Sidebar | Nav + active pill | AppSidebar custom + tokens |
| Profile card | Display name + email fields | PrimeVue Card `#content` |
| Notifications card | Toggle row | Card `#content` + ToggleSwitch |
| Save CTA | Primary button outside cards | Filled Button, right-aligned |

## Spacing & alignment (designer rules)

- Card internal padding: **≥ 16px** (`var(--size-4)` or `--size-5`)
- Gap between cards: **16–24px**
- Sidebar width token: **248px** (`--sidebar-width`)
- Save button **outside** card stack, not inside Profile card

## Implementation spec

| Component / region | Token or CSS rule | File(s) |
|--------------------|-------------------|---------|
| Sidebar width | `--sidebar-width: 248px` | `tokens.css`, `AppSidebar.vue` |
| Card body padding | `.p-card-body { padding: var(--size-5) }` | route scoped CSS |
| Card stack gap | `gap: var(--size-4)` | route container |
| Nav active | brand subtle bg + brand text | `AppSidebar.vue` |
| Card content slot | `<template #content>` | all Card usages |

## Theme notes

- Light/dark coherent with app shell — see `heyeddi-design/reference/modern-reference.md`
- Avoid flat admin-template look: borders + surface-2 cards

## Responsive

- Desktop: sidebar persistent
- Mobile: drawer or bottom nav per product.md

_Source route: `/settings` · Feature folder: `.heyeddi/designs/settings/`_
