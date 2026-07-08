# Delegation matrix — heyeddi-product

**Date:** 2026-07-06

The PM **commissions** specialists and **synthesizes**. Never duplicate their tools inline.

## When to delegate

| PM question | Skill | Tool / mode | You extract |
|-------------|-------|-------------|-------------|
| Can users complete the task? | `@ux-flow-auditor` | `trace_flow --task-id` | Click depth, friction, fail steps |
| Does UI fit persona & job? | `@heyeddi-design` | `critique` | Hierarchy, voice, missing states |
| Is text readable + layout matches spec? | `@visual-auditor` | full fix loop — capture, review, **fix**, `append_fix_log` | fix-log.md + review doc |
| Is code right-sized? | `@engineering-excellence` | `audit_engineering` | KISS/YAGNI findings |
| Duplicate UI waste? | `@no-duplicate-ui` | `find_duplicate_ui` | Merge candidates |
| Tokens / theme coherent? | `@primevue-openprops-architect` | `verify_tokens` | Brand violations |

## Synthesis rules

1. **One recommendation per finding** — link to delegated report path
2. **Prioritize by persona pain** — Jordan blocked > Riley polish
3. **Propose alternatives** — "cut dashboard stats, ship roster table only" with rationale
4. **Assign owner skill** — who implements the change

## Task subagent pattern

```
Task shell → ux-flow-auditor trace_flow
Task generalPurpose → heyeddi-design critique (read critique.md)
Task shell → visual-auditor audit_contrast --check
Task shell → engineering-excellence audit_engineering
Main chat → update review-plan synthesis + backlog
```
