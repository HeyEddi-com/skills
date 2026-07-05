@heyeddi-design must deliver the dashboard:

- DashboardView at `/dashboard` using `useUsers()` composable (wired; live API optional for eval)
- **Primary UI:** user table/list with demo/offline data when API unavailable — not a 3-tile KPI wireframe
- Optional 1–2 summary stat cards OK; DESIGN.md updated if dashboard patterns were missing
- Loading/empty/demo states; styled beyond default PrimeVue admin look — see `modern-reference.md`
- Tests stub present

**Do not require** live FastAPI on `:8090` for pass — UI must still render in preview.

Read all changed files. Dashboard must be styled and substantive in preview (not empty shell).

**Process proof:** Screenshot in `.heyeddi/audits/eval-process/dashboard/` — judge opens PNG and confirms **table rows + heading**, not necessarily 3 stat cards.
