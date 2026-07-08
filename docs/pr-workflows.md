# PR workflows

**Date:** 2026-07-07

HeyEddi splits pull request work into **two skills** with distinct roles. Use the right one — they are not interchangeable.

## Overview

| Workflow | Skill | Who | When |
|----------|-------|-----|------|
| **1. Review submitted PR** | `@heyeddi-pr-review` | Reviewer, QA, or author self-check | Before approval / before requesting review |
| **2. Respond to PR review** | `@heyeddi-pr-respond` | PR author | After human reviewers leave comments |

```
                    ┌─────────────────────────┐
                    │   Feature branch PR     │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
   @heyeddi-pr-review              (reviewers comment)
   committed diff only                          │
   product + docs + eng + gate                   ▼
              │                      @heyeddi-pr-respond
              │                      fix / decline + re-gate
              └─────────────────┬─────────────────┘
                                ▼
                         merge to main
```

## Workflow 1 — Review submitted PR

**Invoke:** `@heyeddi-pr-review` + PR number

**Scope rule:** Only committed changes (`base...head`). Ignore uncommitted files.

### Pipeline

1. `fetch_pr_context` — diff, changed files, categories, routes touched
2. `check_doc_drift` — product.md, design.md, engineering docs vs changes
3. `audit_pr_changes` — KISS/test signals on changed files only
4. `@heyeddi-product` — `load_product_context`, `check_features` for touched routes
5. Conditional delegates when UI/API files change (visual-auditor, composable-patterns, etc.)
6. `@pre-merge-gate` — tests, build, types
7. `write_pr_review` → `.heyeddi/docs/pr-<N>-review.md`
8. Agent sets **Verdict:** Approve | Request changes | Block
9. `verify_pr_review --check`

### Output

Default: markdown report at `.heyeddi/docs/pr-<N>-review.md`. Post `gh pr review` only when the user asks.

### Example prompt

```
@heyeddi-pr-review Review PR #42 — committed changes only.
Check product fit, doc drift, engineering quality, and run pre-merge gate.
```

## Workflow 2 — Respond to PR review

**Invoke:** `@heyeddi-pr-respond` + PR number

**Scope rule:** Address **every** reviewer comment with fix-vs-decline reasoning.

### Pipeline

1. `fetch_pr_comments` — inline, review, discussion
2. Tracking table → `.heyeddi/docs/pr-<N>-tracking.md`
3. Per comment: fix | decline | partial | out-of-scope
4. Apply fixes in code/docs
5. `@pre-merge-gate` after fixes
6. Threaded replies (`gh api .../comments/ID/replies`)
7. `verify_response --check`
8. Summary comment on PR (after all individual replies)

### vs `/babysit`

| Tool | Use when |
|------|----------|
| `/babysit` | Fast merge-ready loop |
| `@heyeddi-pr-respond` | Team rules — every comment, fix matrix, documented tracking |

### Example prompt

```
@heyeddi-pr-respond Handle review feedback on PR #42.
Reply to every comment; fix what's correct; re-run pre-merge gate.
```

## Delegation map

| Concern | Workflow 1 | Workflow 2 |
|---------|------------|------------|
| Product / AC | `@heyeddi-product` | fix-vs-decline uses PR goals |
| Engineering | `audit_pr_changes`, `@engineering-excellence` | fixes + re-audit if needed |
| Visual / UX | `@visual-auditor` (if UI in diff) | only if comment is visual |
| CI / tests | `@pre-merge-gate` | `@pre-merge-gate` after fixes |
| GitHub | optional review | **required** threaded replies |

## Artifacts (`.heyeddi/docs/`)

| File | Workflow |
|------|----------|
| `pr-<N>-review.md` | Submission review report |
| `pr-<N>-context.json` | Cached fetch_pr_context (optional) |
| `pr-<N>-tracking.md` | Comment tracking table |
| `pr-<N>-replies.md` | Drafted replies (eval / offline) |

## Eval cases

```bash
uv run poe eval-pr-submission   # workflow 1 — fixture diff
uv run poe eval-pr              # workflow 2 — fixture comments
```

## Related docs

- [team-cheat-sheet.md](./team-cheat-sheet.md) — quick invoke table
- [heyeddi-folder.md](./heyeddi-folder.md) — `.heyeddi/docs/` layout
- [subagent-delegation.md](./subagent-delegation.md) — Task tool patterns
