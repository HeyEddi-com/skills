# Subagent delegation — pre-merge-gate

| Step | Subagent | Readonly |
|------|----------|----------|
| `pre_merge_gate.py` | `shell` | yes |
| Fix failures from report | `generalPurpose` or main | no |
| Re-run gate | `shell` | yes |

Optional: `ci-watcher` if gate runs in CI and orchestrator waits for checks.
