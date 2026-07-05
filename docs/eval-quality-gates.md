# Eval quality gates

**Date:** 2026-07-02

Agent evals use **three assertion layers** — not just `file_exists`.

## Layers

| Layer | What it proves | Example assertion types |
|-------|----------------|-------------------------|
| **Feature** | Skill delivered the right artifact | `file_exists`, `file_contains` |
| **Quality** | Code is real software | `npm_build`, `npm_test`, `pytest`, `feature_test_exists` |
| **Deps** | Dependencies managed | `ensure_deps`, `audit_dependencies` |
| **Visual** | Page loads, styled UI, resembles design | `page_loads`, `ui_rendered`, `page_not_blank`, `visual_similarity` |

## Assertion types (quality)

```yaml
- name: frontend-builds
  type: npm_build

- name: frontend-tests-pass
  type: npm_test
```

`npm_test` fails on exit code **and** on Vue runtime warnings in test output (e.g. `Failed to resolve component: router-view`). Vitest can report green while the app shell test is broken.

```yaml
- name: page-loads-settings
  type: page_loads
  route: /settings
  must_contain: ["Settings", "Save"]
  allow_skip: true      # skip if Playwright not installed

- name: primevue-ui-visible
  type: ui_rendered
  route: /settings
  primevue_selectors: [".p-card", ".p-button"]
  min_width: 120

- name: visual-vs-handoff
  type: visual_similarity
  route: /settings
  reference: designs/settings/desktop.png
  min_similarity: 0.20
  ref_content_fraction: 0.35   # screenshot must have ≥35% of mockup's ink density
```

`ui_rendered` fails when PrimeVue components exist in DOM but are unstyled (tiny layout boxes). `visual_similarity` also rejects sparse white pages that falsely match mostly-white mockups.

## Optional deps for full quality gate

```bash
./scripts/setup-evals.sh
# or: uv sync --group evals --group evals-quality && uv run playwright install chromium
```

Without Playwright, visual assertions with `allow_skip: true` pass as skipped.

## Cases with quality gates

| Case | Quality checks |
|------|----------------|
| `project-engineering-scaffold-vue` | build, test, deps, scaffold files |
| `design-handoff-only` | + feature test, page load, visual similarity |
| `backend-type-bridger-users` | build, test, pytest |

Quality phase runs `npm install` if needed — slower but proves robust delivery.
