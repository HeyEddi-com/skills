@heyeddi-design @primevue-openprops-architect

**Goal:** Design and build a **production-quality login screen** for SecureVault (see `.heyeddi/product.md`).

No designer mockups — **heyeddi-design from scratch**, not `@design-handoff`.

Read **`reference/surface-completeness.md`** — design a **complete** sign-in surface (sign-in archetype); stub unwired backend; document **Deferred wiring**.

## Mandatory order

1. `load_context` — `.heyeddi/product.md`, `.heyeddi/design.md`
2. `shape` / `document` for **`securevault-login`** → `.heyeddi/designs/securevault-login/brief.md` including:
   - **Surface completeness** audit + sign-in archetype (forgot password, remember me, spacing, footer links)
   - **`## Deferred wiring`** table — UI you ship vs API work later
3. `craft` → `LoginView.vue` at `/login` implementing the brief (generous spacing, card padding, utility row)
4. Validate with `@primevue-openprops-architect`
5. **Append** Decision log in `.heyeddi/design.md`

**Minimum UI chrome (even if stubbed):** email, password, **Forgot password?** link, **Remember me** checkbox, **Sign in** button, error/loading states. Optional: sign-up footer, SSO buttons — document in deferred wiring if omitted.

**Scope / stop rules:**
- Finish when `npm test` and `npm run build` pass.
- Do **not** run Playwright, `@visual-auditor`, or `npm run dev` — harness captures after your turn.
