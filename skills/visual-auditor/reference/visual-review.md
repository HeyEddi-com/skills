# Visual review: screenshots vs specification

**Date:** 2026-07-06

You **see** the UI through captures. Compare against **two** specs:

| Spec | Source | Check |
|------|--------|-------|
| **Product** | `.heyeddi/product.md`: route intent, page purpose, persona success feeling | Does this screen deliver the job? |
| **Design** | `.heyeddi/design.md` + `designs/<feature>/mockup-brief.md` | Hierarchy, spacing, tokens, components |

Mockup PNG colors are **layout only**: implementation colors come from `design.md` tokens.

## Review steps

1. `load_visual_context --route /path --write-review`
2. `capture_screenshots --route /path`
3. `audit_contrast --route /path` (automated legibility)
4. **Open each PNG** in `.heyeddi/audits/visual/screenshots/`
5. Fill **vs product.md** and **vs design.md** sections in the review doc
6. Merge contrast violations into issues table

## Issue severity

| Severity | Examples |
|----------|----------|
| **error** | Contrast fail, wrong IA vs brief, blocks persona job |
| **warn** | Spacing drift, weak hierarchy, motion-over-text risk |
| **info** | Polish opportunity within spec |

## Do not stop at notes

Every **error** and actionable **warn** gets a code fix in the same session unless user explicitly waives in review doc.
