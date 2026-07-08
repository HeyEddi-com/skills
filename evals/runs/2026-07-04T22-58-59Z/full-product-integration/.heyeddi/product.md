# TaskFlow

Small B2B teams (5–30 people) coordinating work without heavyweight project-management sprawl.

## Personas

| Name | Role | Primary job | Anxiety | Design implication |
| ------ | ------ | ------------- | --------- | -------------------- |
| Jordan | Team lead | See blockers and team capacity | Missing updates, tool sprawl | Calm dashboard density, clear roster status |
| Riley | IC contributor | Update work quickly | Clutter, slow flows | Focused app chrome; minimal marketing inside app |
| Sam | Evaluator (buyer) | Judge if tool fits team | Wasted onboarding time | Trustworthy marketing, plain language |

## Per-route intent

| Route | Register | Primary persona | User mindset | Success feeling |
| ------- | --------- | ----------------- | -------------- | ----------------- |
| `/` | brand | Sam | Skeptical, comparing tools | Trustworthy and focused — worth trying |
| `/login` | brand | Sam | Ready to try, cautious | Simple, professional sign-in |
| `/dashboard` | product | Jordan | Monday morning, rushed | Team status in seconds |
| `/settings` | product | Riley | Wants control over profile | Clear settings, one obvious save |

## Stack

Vue 3 SPA with PrimeVue and OpenProps; FastAPI backend in backend/ (port 8090); Vite proxies /api → 127.0.0.1:8090.

## Pages

| Route | View | Purpose |
|-------|------|---------|
| `/` | `HomeView` | Public marketing page: product name, hero headline, 3 feature bullets, primary CTA linking to /login |
| `/login` | `LoginView` | Email + password fields, Sign in button |
| `/dashboard` | `DashboardView` | Main app: welcome heading, table or list of users from GET /api/users |
| `/settings` | `SettingsView` | User settings — implement from .heyeddi/designs/settings/ screenshots |

## Brand personality

Confident, calm B2B SaaS — approachable for small teams

## Competitors

- Users compare us to: Asana, Linear, Trello
- We win on: Simple team roster view without project-management sprawl

## Anti-audience

Enterprise IT teams requiring SSO-only procurement and deep compliance workflows — not our first release.

## Voice & tone

Plain, confident, no buzzwords. Verb-first buttons (Start free trial, Sign in). Errors helpful, not cute.

## Design references

- Linear — crisp app chrome
- Stripe Dashboard — calm data UI for Jordan
- Vercel marketing — hero rhythm for Sam

## Anti-references

- Generic unstyled PrimeVue admin template
- 3-tile KPI dashboard when roster table is the job

## Downstream skills

See `.heyeddi/docs/intake/skill-routing.json` for which `@skill` runs per route.

_Authored by `@heyeddi-intake` via `write_product.py` — do not edit structure by hand._
