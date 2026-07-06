# Design brief — TaskFlow marketing (`/` + `/login`)

**Status:** Confirmed (eval harness — proceed to craft)  
**Date:** 2026-07-04

## Feature summary

Public marketing home and sign-in for TaskFlow, targeting small B2B team buyers (Sam). Home establishes trust and differentiation; login offers a professional, low-friction trial entry. Shared **brand shell** nav links home ↔ sign-in.

## Audience

- **Primary persona:** Sam — Evaluator (buyer)
- **Route intent:** `/` skeptical comparing tools → trustworthy and focused, worth trying; `/login` ready to try, cautious → simple professional sign-in
- **Direction row:** Evaluator / buyer → credibility, clarity (Vercel marketing + Stripe.com trust)
- **Secondary:** SMB founder warmth — approachable copy, not cold enterprise gray
- **Differentiation:** Simple team roster view without project-management sprawl (vs Asana boards, Linear eng focus, Trello cards)

## Primary user action

- **`/`:** Start free trial → `/login`
- **`/login`:** Sign in with email + password

## Design direction

- **Register:** brand — editorial width, hero + proof, outcome-led copy
- **Surfaces:** `--surface-1` page, `--surface-2` elevated cards, `--border-1` subtle borders
- **Typography:** display scale for hero; muted `--text-2` for subcopy
- **Accent:** subtle radial gradient mesh behind hero (low opacity, token-based)
- **Scene:** Calm indigo-primary B2B SaaS — confident, not playful

## Scope

- Production UI for `/` and `/login` + brand shell nav
- Fidelity: shippable marketing + auth surface
- i18n: `en` + `es` for all user-facing strings
- Out of scope this turn: dashboard, settings, auth API wiring

## Layout strategy

### Brand shell (`BrandShell`)

| Region | Content |
|--------|---------|
| Skip link | Skip to main content |
| Header | Logo → `/`, Features anchor (home), Sign in → `/login`, locale toggle |
| Main | `<router-view />` |
| Footer | © TaskFlow, plain legal line |

### Home (`/`)

| Region | Hierarchy |
|--------|-----------|
| Hero | Product name, headline, subcopy, primary CTA, secondary text link |
| Features | 3 columns — icon, title, one-line outcome |
| Proof strip | One line social proof (team size focus) |

### Login (`/login`)

| Region | Hierarchy |
|--------|-----------|
| Page intro | Title + subtitle (reassuring, plain) |
| Auth card | Email, password, remember me, forgot password link |
| Primary CTA | Sign in button below fields |
| Footer hint | Start free trial cross-link for new teams |

## Key states

| Route | States |
|-------|--------|
| `/` | Default only (static marketing) |
| `/login` | Default, validation error (empty fields), submitting (button loading), auth error (inline message stub) |

## Interaction model

- Nav: RouterLink; active state on Sign in when on `/login`
- Home CTA: RouterLink to `/login`
- Login submit: validate required fields → stub redirect to `/dashboard` on success (deferred real auth)
- Locale toggle: persists `localStorage`, updates `document.documentElement.lang`

## Content requirements

| Element | Copy (en) |
|---------|-----------|
| Hero headline | See your team’s status without the PM overhead |
| Hero sub | TaskFlow gives small teams a clear roster view—who’s on what, what’s blocked—without boards and sprawl. |
| CTA primary | Start free trial |
| Feature 1 | Team roster — Everyone’s work in one calm view |
| Feature 2 | Blockers visible — Spot stuck work before standup |
| Feature 3 | Built for small teams — No enterprise setup or training |
| Login title | Sign in to TaskFlow |
| Login subtitle | Use your work email to continue to your team. |
| Sign in button | Sign in |
| Forgot password | Forgot password? |
| Remember me | Remember me on this device |

Spanish equivalents in locale files — same tone, verb-first buttons.

## Component map

| Region | Components |
|--------|------------|
| Brand shell | Custom `BrandShell`, `BrandNav` |
| Hero CTA | PrimeVue `Button` (RouterLink) |
| Features | Custom cards on `--surface-2` |
| Login form | PrimeVue `Card`, `InputText`, `Password`, `Checkbox`, `Button`, `Message` |
| Errors | PrimeVue `Message` severity error |

## Deferred wiring

| UI element | Shipped as | Wire later |
|------------|------------|------------|
| Sign in submit | Client validation + navigate `/dashboard` stub | POST auth API + session |
| Forgot password link | RouterLink placeholder route or `#` with aria | Reset email API |
| Remember me | Checkbox state local only | Secure persistence policy |
| Auth error message | Generic “Check email and password” | API error mapping |

## Open questions

None — brief confirmed for eval craft.
