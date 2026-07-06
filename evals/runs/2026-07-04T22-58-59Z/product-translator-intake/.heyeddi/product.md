# TaskFlow

B2B small teams (5–25 people) who need lightweight task coordination without enterprise overhead.

## Personas

| Name | Role | Primary job | Anxiety | Design implication |
| ------ | ------ | ------------- | --------- | -------------------- |
| Jordan | Team lead | See blockers and team capacity at a glance | Missing updates and tool sprawl | Calm dashboard density, clear roster status |
| Riley | IC contributor | Update work quickly without friction | Clutter and slow multi-step flows | Focused app chrome; settings in obvious card stack |
| Sam | Evaluator (buyer) | Decide if the product fits the team | Wasted onboarding on the wrong tool | Trustworthy marketing; plain professional sign-in |

## Per-route intent

| Route | Register | Primary persona | User mindset | Success feeling |
| ------- | --------- | ----------------- | -------------- | ----------------- |
| `/` | brand | Sam | Skeptical, comparing tools | Trustworthy and focused — worth trying |
| `/login` | brand | Sam | Ready to try, still cautious | Simple, professional sign-in |
| `/dashboard` | product | Jordan | Monday morning, time-pressed | Team status in seconds |
| `/settings` | product | Riley | Wants control over profile and notifications | Clear settings, one obvious save |

## Stack

Vue 3 SPA with PrimeVue; FastAPI backend for auth, team roster, and settings.

## Pages

| Route | View | Purpose |
|-------|------|---------|
| `/` | `MarketingHome` | Public marketing homepage — hero, features, CTA to /login |
| `/login` | `LoginView` | Email/password sign-in |
| `/dashboard` | `DashboardView` | Team roster table from FastAPI — not KPI stat grid |
| `/settings` | `SettingsView` | Profile fields and notification toggle |

## Brand personality

Confident, calm B2B SaaS — approachable for small teams

## Competitors

- Users compare us to: Asana, Linear, Trello
- We win on: Simple team roster view without project-management sprawl

## Anti-audience

Enterprise IT teams requiring SSO-only procurement and deep compliance workflows

## Voice & tone

Plain, confident, no buzzwords. Verb-first CTAs. Helpful errors, not cute.

## Design references

- Linear — crisp borders and focused density
- Stripe Dashboard — calm data UI
- Vercel marketing — hero rhythm for Sam

## Anti-references

- Generic unstyled PrimeVue admin template
- Dense ERP grid with no whitespace

## Downstream skills

See `.heyeddi/docs/intake/skill-routing.json` for which `@skill` runs per route.

_Authored by `@product-translator` via `write_product.py` — do not edit structure by hand._
