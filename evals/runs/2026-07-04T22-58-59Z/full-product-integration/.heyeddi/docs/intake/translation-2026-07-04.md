# Product translation — 2026-07-04

## User prompt

TaskFlow integration eval — team task manager for small B2B teams (5–30 people). Vue + FastAPI stack with marketing home, login, dashboard roster, and settings handoff.

## Interpretation

TaskFlow targets small B2B teams who need lightweight task coordination without enterprise PM sprawl. Three personas: Jordan (team lead), Riley (IC), Sam (buyer/evaluator). Four routes: public marketing (/), sign-in (/login), team roster dashboard (/dashboard), and settings (/settings) with heyeddi-handoff mockups. Stack is Vue 3 + PrimeVue + OpenProps frontend with FastAPI backend on port 8090.

## Decisions

- ≥3 personas including buyer + daily users
- route_intent covers all four page routes
- settings routed to heyeddi-handoff with existing PNG mockups
- no feature Vue during intake — baseline App.vue shell only

## Open questions

_None — proceed to mockups and routing._

## Next

Run `write_routing.py` then chain skills listed in `skill-routing.json`.
