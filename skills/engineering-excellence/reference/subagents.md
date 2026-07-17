# Subagents: engineering-excellence

| Phase | Subagent | Script |
|-------|----------|--------|
| Init docs | `shell` | `init_engineering_docs.py` |
| Audit | `shell` | `audit_engineering.py --check` |
| ADR | main chat + `append_decision.py` | short write |

Main chat reads audit JSON, updates `architecture.md` / `reuse-catalog.md`, delegates re-audit to `shell`.
