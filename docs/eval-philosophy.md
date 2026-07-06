# Eval philosophy — skills finish their job

**Date:** 2026-07-02

Agent evals exist to answer one question: **did the skill do what it is supposed to do — including discovery, documentation, and process — not just dump files?**

## How a human uses a skill

1. State a **goal** (plan, feature, route, problem).
2. The skill **checks context** — existing docs, design system, stack, patterns.
3. The skill **fills gaps** — update `PRODUCT.md` / `DESIGN.md`, run audits, ask questions (or document assumptions when headless).
4. The skill **executes** — implement, wire, test, validate.
5. The skill **chains** guardrails (`@primevue-openprops-architect`, `@visual-auditor`, tests).

Evals must mirror that order. Micro-managing tool names in the prompt is an anti-pattern.

## Prompt style

**Bad (micromanagement):**
```
Run audit_scaffold. Run scaffold_stack. Create HomeView.vue with 3 bullets…
```

**Good (goal + trust the skill):**
```
@heyeddi-design

We need a public marketing homepage for TaskFlow (see PRODUCT.md).
Follow your full workflow: load context, check DESIGN.md and the design system,
update documentation if anything is missing, then build home and login.
```

## Per-skill expectations

| Skill | Process eval checks | Outcome eval checks |
|-------|---------------------|---------------------|
| **heyeddi-design** | `load_context`; `DESIGN.md` present/updated; `designs/<feature>/brief.md` or research for new surfaces | Views exist, styled UI, tokens, tests |
| **design-handoff** | `load_handoff`; read `DESIGN.md` + mockups | Layout regions match handoff (shell, cards, CTA); PrimeVue + tokens; visual gate — **not** mockup pixel colors |
| **project-engineering** | `audit_scaffold` run; gaps addressed | vite/vitest, deps, build, tests |
| **backend-type-bridger** | `sync_openapi` | `src/types/api.ts` matches schema |
| **composable-patterns** | context docs followed | `useApi` / composable patterns, tests |
| **primevue-openprops-architect** | (auto on Vue edits) | no hex, validate_vue if available |

## Headless evals and “asking questions”

The local `agent` CLI runs **one turn at a time** without a human in the loop. For evals:

- Templates may ship **partial** `DESIGN.md` so the skill must run `document` / `shape` before `craft`.
- Prompts say: **document assumptions in `DESIGN.md` or `designs/<feature>/brief.md`** when something would normally be a user question.
- We do **not** assert chat questions; we assert **artifacts** (updated docs, briefs, audit JSON, built UI).

## Agentic judge (default)

After each worker turn, a **second agent call** (judge) receives:

- Full **git diff** and **contents of all changed source files**
- **Complete stdout/stderr** from `npm test`, `npm run build`, `pytest`, etc.
- Worker agent output and per-turn **judge criteria**

The judge decides pass/fail — including **npm/Vue warnings with exit code 0**. No `file_exists` regex gate by default.

Use `--deterministic` on `run-evals.py` only for legacy CI-style assertions.

Env: `EVAL_JUDGE_TIMEOUT` (default 300s), `EVAL_JUDGE_MODEL` (optional).

## Visual QA (Playwright + agentic judge)

Design/handoff turns may declare `visual_audit` in the case YAML. After `npm test` / `build`, the harness:

1. Starts `npm run preview` and captures `/route` at 375 / 768 / 1440 via Playwright
2. Saves PNGs to `.heyeddi/audits/eval-capture/` (and mirrors `.heyeddi/audits/visual/screenshots/`)
3. Compares captures to reference mockup PNGs (similarity hint — layout only; colors from design system)
4. Passes paths + instructions to the **agentic judge**, which must **open and read the PNGs** and fail missing shell, black inputs, flat unstyled layout — **not** button hue vs mockup PNG

Requires `./scripts/setup-evals.sh` (Playwright + Chromium). Missing captures = hard fail before judge.

## Multi-turn cases (max 6)

Each turn = one realistic `@skill` invocation + agentic judge before the next:

```
Turn 1 @project-engineering  → audit/scaffold
Turn 2 @backend-type-bridger → types/composables
Turn 3 @heyeddi-design       → home/login + visual-auditor
Turn 4 @heyeddi-design       → dashboard
Turn 5 @design-handoff       → settings + visual-auditor
Turn 6 @verify-build …       → QA ship pipeline (pre-merge-gate, etc.)
```

Failure on turn *N* stops the case — the skill did not finish its job before moving on.

## Skill coverage (all 12)

| Layer | Coverage |
|-------|----------|
| Smoke (`poe test`) | All 12 skills — structure + CLI |
| Agent eval | All 12 — chained in integration/design cases + dedicated `pr-review-responder-workflow` |

Pipeline skills (`verify-build`, `visual-auditor`, `pre-merge-gate`, `no-duplicate-ui`, `design-system-generalizer`) are invoked in **turn 6** of `full-product-integration` and chained in design evals — not isolated one-off cases.

## Independent design skill evals

| Case | Skill | Scenario |
|------|-------|----------|
| `design-handoff-only` | `@design-handoff` | Mockups → implement `/settings` |
| `heyeddi-design-from-scratch` | `@heyeddi-design` | No UI yet — shape/document → craft `/login` |
| `heyeddi-design-polish-existing` | `@heyeddi-design` | **Ugly existing** `/login` — visual audit, document drift, polish |

All use agentic judge + Playwright. Handoff compares to PNGs; heyeddi-design judges captures for production quality.

```bash
uv run poe eval-design-handoff
uv run poe eval-heyeddi-design-scratch
uv run poe eval-heyeddi-design-polish
```

## Adding a new eval

1. Pick a **user goal**, not a file checklist.
2. Choose **turns** (which skills, in what order).
3. Per turn: **process assertions** first, **outcome assertions** second.
4. Run `--dry-run` and confirm prompts read like cheat-sheet invocations.

See [agent-evals.md](./agent-evals.md) and [eval-quality-gates.md](./eval-quality-gates.md).
