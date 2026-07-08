# Cross-pillar workflow (hub)

**Date:** 2026-07-07

Canonical spec: `skills/skill-orchestrator/reference/cross-pillar-workflow.md`

Product (`@product-manager`), UX (`@ux-flow-auditor`), and design (`@heyeddi-design`) share `.heyeddi/docs/workflow/`. Whenever one pillar runs on a route, siblings **opine and maintain their docs** before the route is done.

Tools live on `@skill-orchestrator`: `init_workflow_sync`, `load_workflow_context`, `append_pillar_opinion`.
