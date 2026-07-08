Independent **@heyeddi-design** eval — **existing UI**, not greenfield.

## Pipeline (required)

- `load_context` run
- **Critique first** — `.heyeddi/docs/login-critique.md` exists with P0/P1 issues (native inputs, hex, cramped layout, etc.)
- **Then polish** — not full greenfield `shape`
- `.heyeddi/design.md` updated for drift; Decision log cites critique + fixes
- Login uses PrimeVue + OpenProps after polish — no black inputs, no inline hex
- **FAIL if:** skipped critique, no critique file, polish without addressing documented P0s
- Playwright captures in `.heyeddi/audits/eval-capture/` — fail if still looks like broken baseline
- Tests/build clean

Do not require @heyeddi-handoff or mockup PNGs.
