---
name: pr-review-responder
description: Addresses PR review feedback — fetch all comment types, fix-vs-decline decisions, apply fixes, re-run pre-merge gate, threaded replies. Use when responding to human review comments as the PR author. For reviewing a submitted PR use pr-submission-review.
disable-model-invocation: true
---

# PR Review Responder

## Subagents (default)

Fetch + reply via **Task** — `shell` for `gh`/`fetch_pr_comments`/`verify_response`; `generalPurpose` for fix-vs-decline analysis. Main chat owns tracking table. See `reference/subagents.md`.

## When to use

- Human reviewers left comments — you are the **author** responding
- Need flat JSON of all comment types for tracking table
- Team rules: reply to every comment, fix-vs-decline matrix, re-gate after fixes

**Not this skill:** initial review of submitted PR → `@pr-submission-review`.

## Mandatory pipeline

Read **`reference/workflow.md`**.

```
fetch_pr_comments --pr <N>
→ tracking table in .heyeddi/docs/pr-<N>-tracking.md (every comment)
for each comment:
  analyze vs PR goals → fix | decline | partial | out-of-scope
  apply code/docs fixes when fix
  reply in thread (gh api .../comments/ID/replies)
pre_merge_gate                    → after all fixes
verify_response --pr <N> --check   → tracking complete + gate OK
→ summary comment on PR (only after all individual replies)
```

## Requires

- `gh` CLI authenticated (`GH_TOKEN` in cloud)

## vs `/babysit`

| Tool | Use when |
|------|----------|
| `/babysit` | Fast merge-ready loop, minimal ceremony |
| `@pr-review-responder` | Team rules — every comment, fix matrix, threaded replies, documented tracking |
