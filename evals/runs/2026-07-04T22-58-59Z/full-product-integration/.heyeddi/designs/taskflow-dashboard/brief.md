# Design brief — TaskFlow dashboard (`/dashboard`)

**Status:** Confirmed (eval harness — proceed to craft)  
**Date:** 2026-07-04

## Feature summary

Main app dashboard for Jordan (team lead): a calm roster view showing team members from `GET /api/users` via `useUsers()`. Monday-morning scan — who's on the team, refresh when needed — without KPI theater or PM sprawl.

## Audience

- **Primary persona:** Jordan — Team lead
- **Route intent:** Monday morning, rushed → team status in seconds
- **Direction row:** B2B team lead, ops → calm density, trust (Stripe Dashboard + Linear app)
- **Secondary:** Riley — focused app chrome, no marketing inside app
- **Differentiation:** Simple team roster without Asana boards or Trello card sprawl — status in one table, not 3-tile KPI grid

## Primary user action

Scan team roster and refresh data when updates are missing.

## Design direction

- **Register:** product — shell + focused main, verb-first actions
- **Surfaces:** `--surface-1` page, `--surface-2` elevated cards, `--border-1` borders
- **Typography:** page title at body+ scale (not marketing display); muted `--text-2` subtitle
- **Density:** Stripe Dashboard table hierarchy — calm neutrals, striped rows OK
- **Scene:** Linear-crisp app chrome; data table is the hero, not stat tiles

## Scope

- Production UI for `/dashboard` with `ProductShell` app chrome
- `useUsers()` integration with offline demo fallback (no live API required for eval)
- i18n: `en` + `es`
- Out of scope: settings craft, auth guard, row actions, pagination

## Layout strategy

### Product shell (`ProductShell`)

| Region | Content |
|--------|---------|
| Skip link | Skip to main content |
| Header | Logo → `/dashboard`, Team (active on dashboard), Settings → `/settings`, locale toggle |
| Main | `<router-view />` |

### Dashboard (`/dashboard`)

| Region | Hierarchy |
|--------|-----------|
| Page header | Welcome title + subtitle + Refresh button (secondary, outlined) |
| Offline banner | PrimeVue `Message` warn — shown when API unavailable, demo rows loaded |
| Summary row | **Optional 2 stat cards** — member count, data source (not 3 KPI tiles) |
| Roster table | PrimeVue `DataTable` in elevated card — id, email columns; primary content |

## Key states

| State | Behavior |
|-------|----------|
| Loading | DataTable loading indicator; Refresh disabled/spinner |
| Live data | Table rows from API; data source card = "Live API" |
| Empty | API returned `[]` — empty slot copy, no demo injection |
| Offline demo | Fetch failed — demo roster rows + warn banner; data source = "Demo data" |
| Error (with empty users) | Same as offline demo for eval resilience |

## Interaction model

- Mount → auto-fetch users
- Refresh → re-fetch; success clears offline banner
- Nav: RouterLink between dashboard and settings stub
- Locale toggle in product shell

## Content requirements

| Element | Copy (en) |
|---------|-----------|
| Title | Team roster |
| Subtitle | See who's on your team at a glance. |
| Refresh | Refresh |
| Stat members | Team members |
| Stat source | Data source |
| Source live | Live API |
| Source demo | Demo data |
| Offline banner | API unavailable — showing demo roster so you can explore TaskFlow. |
| Empty | No team members yet. Invite your team to get started. |
| Column email | Email |
| Column id | ID |

Spanish equivalents in locale files — plain, verb-first.

## Component map

| Region | Components |
|--------|------------|
| App shell | Custom `ProductShell`, `ProductNav` |
| Header actions | PrimeVue `Button` (outlined, refresh icon) |
| Offline notice | PrimeVue `Message` severity warn |
| Stats | PrimeVue `Card` × 2 |
| Roster | PrimeVue `DataTable`, `Column` in elevated card |

## Deferred wiring

| UI element | Shipped as | Wire later |
|------------|------------|------------|
| Row click / profile | Static rows | User detail route |
| Status / capacity columns | Email + id only | Work status API |
| Invite button | Not on v1 dashboard | Invite flow |
| Auth guard | Open route from login stub | Session middleware |

## Open questions

None — brief confirmed for eval craft.
