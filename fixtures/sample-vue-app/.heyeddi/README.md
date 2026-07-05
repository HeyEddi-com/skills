# HeyEddi

**HeyEddi** is a product studio and agency: we design and ship SaaS applications for clients — Vue frontends, FastAPI or Firebase backends, and a consistent design system (OpenProps + PrimeVue).

This folder is the **HeyEddi workspace** in your repository. Skills read and write here so product context, design artifacts, and reports stay in one place.

## Skills (free to use)

Our [Cursor Agent Skills](https://github.com/heyeddi/skills) are **free and open**. Install into any project:

```bash
npx skills add heyeddi/project-engineering -a cursor
./scripts/install-skills.sh --all --project .
```

Skills are invoked with `@skill-name` in Cursor or wired into our Cloud Run agent. They automate engineering scaffold, design, handoff, API types, QA gates, and PR workflows — the same steps our team runs on client work.

**You own your code.** Skills suggest and generate; you review and merge like any other contributor.

## How we use this folder

| Path | Purpose |
|------|---------|
| `stack.json` | Declared stacks: Vue, FastAPI, Firebase |
| `product.md` | Product brief — users, routes, acceptance criteria |
| `design.md` | Design system — tokens, PrimeVue catalog, layout rules |
| `designs/<feature>/` | Per-feature artifacts: handoff PNGs, briefs, wireframes, research |
| `docs/` | Skill-generated reports (ship checklist, PR tracking, drift audits, gate output) |
| `audits/` | Visual audit summaries, pre-merge snapshots (optional) |

**Convention:** When a skill creates documentation, save it under `.heyeddi/docs/` or the relevant subfolder above — not scattered at repo root. Root `PRODUCT.md` / `DESIGN.md` / `designs/` are legacy fallbacks; prefer this folder for new work.

## Typical flow

1. `@project-engineering` — audit scaffold, install deps, declare `stack.json`
2. `@heyeddi-design` or `@design-handoff` — product + design docs, then UI
3. `@backend-type-bridger` + `@composable-patterns` — API types and composables
4. `@verify-build` + `@visual-auditor` + `@pre-merge-gate` — ship checklist

See [HeyEddi skills hub](https://github.com/heyeddi/skills) for the full cheat sheet.

---
*Last updated: 2026-07-02 — maintained by project-engineering scaffold*
