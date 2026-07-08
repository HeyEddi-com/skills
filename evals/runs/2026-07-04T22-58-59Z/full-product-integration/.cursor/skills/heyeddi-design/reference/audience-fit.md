# Audience-fit critique

**Date:** 2026-07-04

Run after `reference/critique.md` visual/UX pass — or merge into the same report under **## Audience fit**.

Answers: *Was this designed for our persona, or generic SaaS?*

## Prerequisites

1. Read `product.md` — **Personas**, **Per-route intent**, **Competitors**, **Voice & tone**
2. Read route's `designs/<feature>/brief.md` — **Audience** section
3. View route (code + optional `@visual-auditor`)

## Rubric (score each 1–5)

| Dimension | 1 (fail) | 5 (excellent) |
|-----------|----------|---------------|
| **Persona recognition** | Any team / any user | Primary persona would say "this is for me" |
| **Job alignment** | Wrong primary action | Primary job doable in ≤ expected clicks |
| **Trust (brand routes)** | Template / scam vibes | Credible for persona's buying context |
| **Tone** | Lorem / wrong register | Matches voice & tone; no jargon mismatch |
| **Differentiation** | Clone of competitor | Clear why us vs competitors table |
| **Anti-audience** | Appeals to wrong user | Would not confuse excluded segment |

**Ship bar:** no dimension below **3** on flagship routes; average **≥ 4**.

## Report section (append to critique)

```markdown
## Audience fit

**Primary persona:** …  
**Route:** …

| Dimension | Score | Evidence | Fix |
|-----------|-------|----------|-----|
| Persona recognition | /5 | … | … |
| Job alignment | /5 | … | … |
| Trust | /5 | … | … |
| Tone | /5 | … | … |
| Differentiation | /5 | … | … |
| Anti-audience | /5 | … | … |

**Verdict:** PASS / REVISE  
**Recommended:** polish | shape | product.md update
```

## Verdict rules

- **PASS** — all ≥ 3, avg ≥ 4 → `@heyeddi-design polish` for P1 visual issues only
- **REVISE** — any ≤ 2 → `shape` or persona update in `@heyeddi-intake`; do not polish over wrong IA/tone

## Eval / integration

Harness may check Decision log cites persona. Audience-fit is agent-judged unless extended with rubric automation later.
