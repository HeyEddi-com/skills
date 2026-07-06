# Polish — refine existing screen

**Scope:** Improve an implemented route without changing core IA.

**Prerequisite:** Run **`critique`** first (`reference/critique.md`) and write `.heyeddi/docs/<feature>-critique.md` — unless you already critiqued this route in the current session. Polish addresses the P0/P1 items from that critique.

## Steps

1. Run `load_context.py` — DESIGN.md + PRODUCT.md (check `audience_ready`).
2. **Read the critique** — `.heyeddi/docs/<feature>-critique.md`. If missing, run **critique** before changing code.
3. Re-check `reference/audience-fit.md` — tone and persona alignment, not just spacing.
4. Run `@visual-auditor` on the target route at 375/768/1440 (when available).
5. Fix issues in priority order: P0 → P1 → P2 from critique; align tokens/components with `design.md`.
6. Re-run `@primevue-openprops-architect` validation.
7. Re-run `@visual-auditor` to confirm improvement (when available).
8. **Append** to **Decision log** in `.heyeddi/design.md` — reference critique findings + what you fixed (`reference/design-talk.md`).

## Boundaries

- **Polish** does not replace **shape** — if critique flags IA problems, recommend `shape` + brief update first.
- Do not introduce new PrimeVue components without updating DESIGN.md component table.
