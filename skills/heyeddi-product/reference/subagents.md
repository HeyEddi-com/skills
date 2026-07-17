# Subagents: heyeddi-product

| Phase | Subagent | Script / delegate |
|-------|----------|-------------------|
| Init docs | `shell` | `init_product_docs.py` |
| Context | `shell` | `load_product_context.py` |
| Audit / check | `shell` | `audit_product.py`, `check_features.py` |
| UX research | `shell` | `@ux-flow-auditor` `trace_flow` |
| Design research | `generalPurpose` | `@heyeddi-design` `critique` |
| Visual research | `shell` | `@visual-auditor` `audit_contrast --check` |
| Engineering research | `shell` | `@engineering-excellence` `audit_engineering` |
| Synthesis | **main chat** | Fill `review-plan-*.md`, update `backlog.md` |

Main chat owns PM judgment: specialists supply evidence.
