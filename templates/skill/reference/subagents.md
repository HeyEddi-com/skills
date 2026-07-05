# Subagent delegation — `<skill-name>`

**Default in Cursor:** delegate rows below via the **Task** tool unless the user asks for a single-thread run.

Read hub spec: [subagent-delegation.md](https://github.com/heyeddi/skills/blob/main/docs/subagent-delegation.md) (or `docs/subagent-delegation.md` in the skills hub).

## Global types

| Type | Use |
|------|-----|
| `explore` | Read-only repo search |
| `shell` | Scripts, npm, gh, verify |
| `generalPurpose` | One focused phase (brief, critique, single view) |

## This skill

| Phase / step | Subagent | Readonly | Prompt must include |
|--------------|----------|----------|---------------------|
| _(fill per skill)_ | | | `@skill-name`, `--project-root`, stop rules |

Orchestrator verifies artifacts exist before launching the next row.
