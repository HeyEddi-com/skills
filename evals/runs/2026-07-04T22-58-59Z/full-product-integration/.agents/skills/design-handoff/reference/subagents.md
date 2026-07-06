# Subagent delegation — design-handoff

**Default:** two-pass handoff uses subagents per phase. Main chat orchestrates Pass 1 → verify → Pass 2 → verify → audit.

## Pass 1 — Designer (interpret)

| Step | Subagent | Readonly | Worker prompt |
|------|----------|----------|---------------|
| Study PNGs + write `mockup-brief.md` + Implementation spec | `generalPurpose` | yes* | `@design-handoff` Pass 1 only. Route + paths to PNGs. Follow `interpret-mockups.md`. No `.vue` edits. |
| `describe_handoff.py --sync-design` | `shell` | no | Run script; return stdout |

\*Interpret may write under `.heyeddi/designs/` and `.heyeddi/design.md` only.

**Gate:** `describe_handoff.py --check` passes before Pass 2.

## Pass 2 — Implementer (build)

| Step | Subagent | Readonly | Worker prompt |
|------|----------|----------|---------------|
| Find existing layout/catalog components | `explore` | yes | Search `@/components/`, `design.md` Components, prior AppShell patterns |
| Fix `tokens.css` + `verify_tokens.py` | `shell` | no | Per Implementation spec; run verify |
| Build shell (`AppShell`, sidebar, top bar) | `generalPurpose` | no | `@design-handoff` Pass 2 shell only. Run `verify_handoff --phase shell` before done |
| Build route view | `generalPurpose` | no | `@design-handoff` Pass 2 route only. `verify_handoff --phase full` |
| `validate_vue` + `npm test` + `npm run build` | `shell` | no | Full command output |
| Visual capture | `shell` | yes | `@visual-auditor` or `audit_ui.py` at 375/768/1440 |

## Optional

| Step | Subagent | When |
|------|----------|------|
| Diff review | `bugbot` | User or eval requests review before merge |
| Auth/settings security | `security-review` | Route handles credentials or PII |

Main chat **merges** subagent summaries, appends Decision log, and confirms gates passed.
