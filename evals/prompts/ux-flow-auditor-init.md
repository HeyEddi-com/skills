@ux-flow-auditor

Initialize UX flow documentation for TaskFlow:

1. Run `init_ux_flows` to scaffold `.heyeddi/docs/ux-flows/`
2. Ensure `index.md` lists at least one example flow (update-profile or settings save)
3. Document one friction point and suggested fix in the flow markdown

**Scope for this eval (init-only):**
- Do **not** implement Vue changes
- Do **not** run `trace_flow.py` or Playwright — full trace is a follow-up after `/settings` exists
- `trace_flow --check` is documented as the next step in the flow markdown, not required now
