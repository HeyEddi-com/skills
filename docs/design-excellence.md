# Design excellence — HeyEddi layers

**Date:** 2026-07-04

How HeyEddi skills produce **world-class, audience-driven** UI — not generic “modern SaaS.”

## The stack (bottom → top)

| Layer | Artifact / skill | What it does |
|-------|------------------|--------------|
| **1. Intake** | `@product-translator` → `product.md` | Personas, per-route intent, competitors, voice |
| **2. Routing** | `skill-routing.json`, `@skill-orchestrator` | Which skill runs per route; skills index cache |
| **3. Discovery** | `@heyeddi-design discover` | Ask until purpose, audience, scene are clear |
| **4. Research** | `designs/<feature>/research.md` | Category + competitor + audience-specific trends |
| **5. Direction** | `audience-design.md` + `modern-reference.md` | Map persona → aesthetic; technique execution |
| **6. Explore** | Wireframes + concept direction | User picks a direction before code |
| **7. Brief** | `designs/<feature>/brief.md` | Confirmed contract — persona, states, components |
| **8. Craft / handoff** | `@heyeddi-design craft`, `@design-handoff` | Build from brief + DESIGN.md |
| **9. Audience-fit critique** | `audience-fit.md` | “Would Alex trust this?” gate |
| **10. Polish + visual proof** | `@visual-auditor`, `@primevue-openprops-architect` | Responsive proof, token compliance |

Skip a layer → cap quality at that layer.

## `product.md` contract (required for flagship routes)

Sections every greenfield product should have:

- **Personas** — name, role, job, anxiety, design implication
- **Per-route intent** — register, mindset, success feeling, primary persona
- **Competitors & anti-audience** — what users compare you to; who this is NOT for
- **Voice & tone** — microcopy direction

See `skills/product-translator/reference/audience-intake.md`.

## Flagship route rule

For `/`, `/login`, `/dashboard`, `/settings`:

1. `product.md` audience sections present
2. `shape` completed OR brief exists with persona cited
3. `research.md` ties recommendations to a persona
4. Decision log cites **persona + pattern borrowed**

## Related

- [heyeddi-folder.md](./heyeddi-folder.md)
- [clarify-before-act.md](./clarify-before-act.md)
- `skills/heyeddi-design/reference/audience-design.md`
- `skills/heyeddi-design/reference/audience-fit.md`
