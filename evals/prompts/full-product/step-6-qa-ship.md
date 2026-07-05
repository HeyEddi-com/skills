@verify-build @pre-merge-gate @no-duplicate-ui @design-system-generalizer @project-engineering

## QA ship (scripts only — fast turn)

TaskFlow routes: `/`, `/login`, `/dashboard`, `/settings`.

**Do not** start `npm run dev`, Playwright, or `audit_ui.py`. The eval harness runs full-route screenshots **after** this turn.

Your job:

1. Run (or fix until green):
   - `bash .agents/skills/verify-build/scripts/verify_build.sh --project-root .`
   - `python .agents/skills/no-duplicate-ui/scripts/find_duplicate_ui.py --project-root .`
   - `python .agents/skills/design-system-generalizer/scripts/scan_patterns.py --route /settings --project-root .`
   - `python .agents/skills/design-system-generalizer/scripts/diff_violations.py --golden /settings --target /dashboard --project-root .`
   - `python .agents/skills/design-system-generalizer/scripts/diff_violations.py --golden /settings --target /login --project-root .`
   - **`python .agents/skills/pre-merge-gate/scripts/pre_merge_gate.py --project-root . --skip-visual-audit`** — required; harness owns visual proof
   - `npm test`, `npm run build`, `cd backend && poetry run pytest -q`
2. Write `.heyeddi/docs/ship-report.md` — paste **actual** gate output (pre-merge must show **Overall: OK**, not BLOCKED on visual-audit).
3. Optional: `@engineering-excellence` init/audit if `.heyeddi/docs/engineering/` missing.

**Finish when verify commands pass.** Do not re-implement features or run visual capture in this turn.
