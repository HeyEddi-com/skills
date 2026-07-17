# Subagent delegation: project-engineering

| Step | Subagent | Readonly | Worker prompt |
|------|----------|----------|---------------|
| `audit_scaffold` | `shell` | yes | JSON output; no edits |
| `scaffold_stack` / `scaffold_vue` / Firebase scaffold | `shell` | no | Stack from `stack.json` or `--stack auto` |
| `npm ci` / `npm install` | `shell` | no | After scaffold |
| `npm test` / `npm run build` / `pytest` | `shell` | yes | Return full output |
| Find existing backend layout | `explore` | yes | Before choosing stack |

Orchestrator reads audit JSON and decides which scaffold subagents to run.
