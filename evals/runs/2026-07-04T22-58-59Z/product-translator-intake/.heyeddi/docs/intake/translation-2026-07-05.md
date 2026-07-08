# Product translation — 2026-07-05

## User prompt

# User request (eval fixture)

Build **TaskFlow** — a B2B team task manager for small teams.

- Public marketing homepage at `/`
- Login at `/login`
- App dashboard at `/dashboard` showing team members from an API
- Settings at `/settings` with profile fields and notification toggle
- Vue frontend + FastAPI backend
- Modern SaaS look (not plain admin template)

We have no mockups yet — generate professional layout references and briefs.

## Interpretation

TaskFlow is a B2B team task manager for small teams (5–25 people). Four routes: marketing homepage (/), login (/login), team roster dashboard (/dashboard), and settings (/settings). Vue 3 + PrimeVue frontend with FastAPI backend. Modern SaaS aesthetic — not a generic admin template. Settings is the heyeddi-handoff feature with generated mockups and brief.

## Decisions

- Three personas: Sam (buyer/evaluator), Jordan (team lead), Riley (IC contributor)
- All four page routes have route_intent entries for @heyeddi-design audience gates
- Competitive positioning: simpler roster view vs Asana/Linear/Trello sprawl
- Settings route uses heyeddi-handoff with generated mockups; other routes use heyeddi-design craft mode
- Stack: Vue 3 SPA + FastAPI; PrimeVue for components with custom tokens

## Open questions

_None — proceed to mockups and routing._

## Next

Run `write_routing.py` then chain skills listed in `skill-routing.json`.
