# Skills index

**Generated:** 2026-07-04T00:54:43Z · **Maintained by:** `@heyeddi-orchestrator`

Cached catalog — read this instead of every `SKILL.md` at session start. Refresh after installing skills: `write_skills_index --project-root .`

**Installed:** 22 / 22 skills

| Skill | Invoke | Installed | Description |
|-------|--------|-----------|-------------|
| backend-type-bridger | @backend-type-bridger | yes | Syncs FastAPI OpenAPI schema to TypeScript types and reads Firestore schema hints. Use when writing Vue composables a... |
| composable-patterns | @composable-patterns | yes | Provides FastAPI JWT and Firebase client composable patterns for consistent auth and data layers. Context-first skill... |
| dart-type-bridger | @dart-type-bridger | yes | Syncs FastAPI OpenAPI schema to Dart model stubs and reads Firestore schema hints for Flutter projects. Use when writ... |
| heyeddi-handoff | @heyeddi-handoff | yes | Implements screens from designer screenshots and handoff notes. Two-pass workflow — designer writes mockup-brief with... |
| design-handoff-flutter | @design-handoff-flutter | yes | Implements Flutter screens from designer screenshots and handoff notes using Material 3. Two-pass workflow — mockup-b... |
| design-system-generalizer | @design-system-generalizer | yes | Scans token and component usage patterns from a golden reference page and diffs violations on other routes. Use when ... |
| engineering-excellence | @engineering-excellence | yes | Audits code for KISS, YAGNI, DRY, SOLID, and testability; maintains living engineering notes under .heyeddi/docs/engi... |
| flutter-engineering | @flutter-engineering | yes | Ensures HeyEddi Flutter projects have the right engineering stack — Flutter (Riverpod, go_router, Material 3), FastAP... |
| flutter-patterns | @flutter-patterns | yes | Provides FastAPI Dio and Firebase client patterns for Flutter — repositories, Riverpod providers, auth. Context-first... |
| heyeddi-design | @heyeddi-design | yes | End-to-end UI design for HeyEddi stack (PrimeVue, DESIGN.md, semantic tokens — OpenProps on scaffold default). Use wh... |
| impeccable | @impeccable | yes | Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adap... |
| no-duplicate-ui | @no-duplicate-ui | yes | Scans Vue files for duplicate component names and similar template overlap. Use during PR review or when refactoring ... |
| heyeddi-pr-respond | @heyeddi-pr-respond | yes | Fetches all PR comment types (inline, review, discussion) via gh api for team review workflow. Use when addressing PR... |
| pre-merge-gate | @pre-merge-gate | yes | Runs pre-merge checks (tests, build, types, optional UI audit) and returns a markdown pass/fail report. Use when QA a... |
| primevue-openprops-architect | @primevue-openprops-architect | yes | Enforces PrimeVue + project design tokens when editing Vue or CSS. OpenProps rules apply only when the project alread... |
| heyeddi-intake | @heyeddi-intake | yes | Translates vague user prompts into HeyEddi product docs, professional layout mockups, mockup briefs, and skill-routin... |
| project-engineering | @project-engineering | yes | Ensures HeyEddi projects have the right engineering stack — Vue (Vite/Vitest), FastAPI backend, or Firebase tooling. ... |
| heyeddi-orchestrator | @heyeddi-orchestrator | yes | Discover HeyEddi skills, load the catalog, and suggest which @skills to invoke for the current task. Use at session s... |
| update-pitches | @update-pitches | yes | Audits backend pitch stories in docs/_pitches/ against app/{models,routers,services}/ and syncs Summary.md and priori... |
| ux-flow-auditor | @ux-flow-auditor | yes | Traces user task flows with Playwright — click depth, step success, friction — and writes reports to .heyeddi/docs/ux... |
| verify-build | @verify-build | yes | Runs npm run build to catch Vite/Rollup failures before merge. Use when validating frontend changes or in CI pre-merg... |
| visual-auditor | @visual-auditor | yes | Captures responsive screenshots via Playwright when available, or extracts a layout JSON tree as fallback. Use when c... |

## Quick use

1. `suggest_skills --user-prompt "..."` — rank skills for the task
2. Read **one** chosen skill's `SKILL.md` (path in JSON index)
3. Follow `docs/intake/skill-routing.json` when present
