---
name: skill-orchestrator
description: Discover HeyEddi skills, sync product/UX/design cross-pillar opinions, and suggest which @skills to invoke. Use at session start, multi-skill pipelines, or when connecting product-manager, ux-flow-auditor, and heyeddi-design on a route.
version: 1.2.0
---

# Skill Orchestrator

Routes work to the right HeyEddi skill — and **keeps product, UX, and design pillars in sync**.

## When to use

- Session start on a HeyEddi project (`.heyeddi/` present or greenfield app request)
- User asks "what skills do we have?" or "which skill should handle this?"
- Before a multi-step pipeline (intake → scaffold → design → handoff → QA)
- **Any time one pillar runs** — bookend with `load_workflow_context` / `append_pillar_opinion`
- After `@product-translator` — confirm `skill-routing.json` before downstream work

## Cross-pillar sync (mandatory for product · UX · design)

Read **`reference/cross-pillar-workflow.md`**.

```
init_workflow_sync                    (once per project)
load_workflow_context --route /path   (start of pillar session)
… @product-manager | @ux-flow-auditor | @heyeddi-design work …
append_pillar_opinion --pillar …      (end — triggers sibling opinions)
```

## Skill discovery pipeline

```
write_skills_index        → .heyeddi/skills-index.{json,md}
load_catalog / suggest_skills
read one SKILL.md         → follow that skill's pipeline
```

If `.heyeddi/docs/intake/skill-routing.json` exists, **follow route order**.

## Tools

| Script | Purpose |
|--------|---------|
| `write_skills_index.py` | Scan → `.heyeddi/skills-index.*` |
| `load_catalog.py` | Read cached index |
| `suggest_skills.py` | Rank skills for a prompt |
| `init_workflow_sync.py` | Scaffold `.heyeddi/docs/workflow/` |
| `load_workflow_context.py` | Sibling opinions + checklist for route |
| `append_pillar_opinion.py` | Log opinion; request UX/design/product response |

## Related

- `@product-manager` · `@ux-flow-auditor` · `@heyeddi-design` — three pillars
- `@product-translator` — upstream intake
- `docs/cross-pillar-workflow.md` — hub summary
