# Holistic product review

**Date:** 2026-07-06

PM work is **not** backlog hygiene only. Each review answers:

| Question | Evidence sources |
|----------|------------------|
| **Does it work?** | `check_features`, `@ux-flow-auditor` traces, acceptance criteria |
| **Is it useful?** | Persona jobs, competitor frame in `product.md`, UX critique |
| **Would something else be better?** | Synthesis across UX + design + engineering findings |

## Review types

### Intake review (post-`@heyeddi-intake`)

```
audit_product --check
write_feature_spec (per route)
```

Block `@heyeddi-design craft` on flagship routes until feature specs exist.

### Build review (mid-implementation)

```
check_features
write_review_plan
delegate critique + trace_flow + audit_contrast
update recommendations table
```

### Release review (pre-ship)

```
verify_product --check
confirm review plan P0 rows resolved or waived in backlog
```

## Waiver

If shipping with known gaps, document in `backlog.md` under **Out of scope** with persona impact: not silent debt.
