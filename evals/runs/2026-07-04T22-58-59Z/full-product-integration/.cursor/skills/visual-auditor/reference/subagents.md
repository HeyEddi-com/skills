# Subagent delegation — visual-auditor

This skill is **usually invoked as a subagent**, not run inline in a long design turn.

| Step | Subagent | Readonly | Notes |
|------|----------|----------|-------|
| Start preview + Playwright capture | `shell` | yes | `audit_ui.py` or harness equivalent |
| Layout tree fallback | `shell` | yes | `layout_tree.py` when no Playwright |
| Compare to reference PNGs | `generalPurpose` | yes | Read captures + mockups; layout hierarchy only |

Parent skill (`heyeddi-handoff`, `heyeddi-design`) launches this via Task with route, widths, artifact paths.
