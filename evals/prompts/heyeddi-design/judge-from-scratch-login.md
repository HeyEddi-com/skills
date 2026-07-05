Independent **@heyeddi-design** eval — no mockup PNGs.

## Brief & design thinking

- Brief follows **`surface-completeness.md`** (full regions + **Deferred wiring**) — not minimal email/password only
- Brief includes **`## Deferred wiring`** (forgot password, remember me, SSO, etc. — what is UI-only vs API later)
- Decision log in `.heyeddi/design.md`

## Login UI (fail if sparse)

- `/login`: PrimeVue + OpenProps; **no black unstyled inputs**
- **Spacing:** card padding, gaps between fields, subtitle→form, utilities→CTA — not cramped/stacked-flat inputs
- **Forgot password?** link present (stub route or `#` OK)
- **Remember me** checkbox present (persistence can be deferred — UI required)
- Error + loading states
- **FAIL if:** only email + password + button with no utility row; no deferred wiring doc; ugly/cramped captures in `.heyeddi/audits/eval-capture/`
- Tests/build clean

Do not require @design-handoff.
