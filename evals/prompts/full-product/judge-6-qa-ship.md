QA pipeline — agent runs **scripts only** (no Playwright in agent turn):

- @verify-build: production build succeeded
- @design-system-generalizer: `scan_patterns` on `/settings`; `diff_violations` golden `/settings` vs `/dashboard` and `/login`
- @no-duplicate-ui: duplicate scan run
- @pre-merge-gate: **`pre_merge_gate.py --skip-visual-audit`** — report must show **Overall: OK** (visual proof is harness-only; FAIL if BLOCKED on visual-audit rows)
- `.heyeddi/docs/ship-report.md` exists and matches executed command output (not aspirational)
- `.heyeddi/audits/eval-process/manifest.json` + `qa-ship/` captures from **harness** (not agent)

**Process proof:** Open `.heyeddi/audits/eval-process/qa-ship/` — harness screenshots, not agent-run Playwright.

**FAIL if:** agent ran `pre_merge_gate.py` without `--skip-visual-audit`, or ship-report claims OK while gate output shows BLOCKED.
