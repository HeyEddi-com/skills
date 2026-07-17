# Subagent delegation: heyeddi-pr-review

| Step | Subagent | Readonly | Worker prompt |
|------|----------|----------|---------------|
| `fetch_pr_context` | `shell` | yes | PR number; `--fixture` in evals |
| `check_doc_drift` | `shell` | yes | Same PR context |
| `audit_pr_changes` | `shell` | yes | Same PR context |
| `load_product_context` / `check_features` | `shell` | yes | Scope to `routes_touched` |
| UI delegates (`visual-auditor`, etc.) | `shell` / `generalPurpose` | mixed | Only when UI files in diff |
| `pre_merge_gate` | `shell` | yes | Full gate before verdict |
| Verdict + report prose | main |: | Fill Summary, Product fit, Verdict |

Main chat owns the **verdict** and ensures scope stays on committed diff.
