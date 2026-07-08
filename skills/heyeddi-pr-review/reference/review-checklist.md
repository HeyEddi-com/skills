# Review checklist — PR submission review

**Date:** 2026-07-07

Use this rubric when reviewing a **submitted** PR. Scope = committed diff only.

## 1. Context

- [ ] `fetch_pr_context` run — file list and categories recorded
- [ ] PR title/body explain **why** and **how to verify**
- [ ] Changed files match PR description (no surprise files)

## 2. Product fit (`@heyeddi-product`)

- [ ] `load_product_context` + `check_features` for `routes_touched`
- [ ] Acceptance criteria met for affected routes
- [ ] Change is **useful** for primary persona — not scope creep
- [ ] PM judgment written in report (not just tool JSON)

## 3. Documentation

- [ ] `check_doc_drift` — no warn-level findings unresolved
- [ ] `product.md` route intent matches behavior change
- [ ] `design.md` Decision log updated when UI changes
- [ ] `docs/engineering/` updated when API/modules change

## 4. Engineering (`audit_pr_changes` + delegates)

- [ ] No warn-level KISS/YAGNI/SOLID on **changed** files
- [ ] New behavior has tests in PR or existing suite references
- [ ] `@composable-patterns` when composables change
- [ ] `@engineering-excellence` when audit flags fat handlers

## 5. UI (when `categories.ui` non-empty)

- [ ] `@no-duplicate-ui` — no forked components
- [ ] `@primevue-openprops-architect` — tokens, no raw hex
- [ ] `@visual-auditor` on touched routes (contrast + layout)

## 6. Hard gate

- [ ] `@pre-merge-gate` — Overall OK (or documented SKIP with reason)
- [ ] Gate markdown pasted in **Gate results** section

## 7. Verdict

| Verdict | Criteria |
|---------|----------|
| **Approve** | All above satisfied |
| **Request changes** | Fixable gaps (docs, tests, gate) |
| **Block** | Breaks product intent, security, or flagship route |

Default output: `.heyeddi/docs/pr-<N>-review.md`. Post `gh pr review` only when user asks.
