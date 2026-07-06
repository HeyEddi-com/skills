# Design — SecureVault

> Product register UI: OpenProps semantic tokens + PrimeVue Aura (indigo primary). See `.heyeddi/docs/login-critique.md` for brownfield audit (2026-07-04).

## Token source

OpenProps via `src/styles/tokens.css` — semantic aliases only in components:

| Token | Maps to | Use |
|-------|---------|-----|
| `--surface-0` | `--gray-0` | Elevated panels on dark contexts |
| `--surface-1` | `--gray-1` | Page background |
| `--surface-2` | `--gray-2` | Cards, raised panels |
| `--text-1` | `--gray-12` | Headings, primary copy |
| `--text-2` | `--gray-9` | Labels, hints, secondary copy |
| `--font-size-1` | `--font-size-0` | Labels, hints |
| `--font-size-2` | `--font-size-1` | Body |
| `--font-size-5` | `--font-size-4` | Card titles |

Spacing: OpenProps `--size-*` directly in scoped CSS (no circular aliases).

Primary actions: PrimeVue Aura preset in `main.ts` (`HeyEddiAura`, indigo scale) — not custom hex buttons.

## Layout — auth surfaces

- Full-viewport centered column; max form width ~28rem (`--size-content-2` / 24–28rem).
- Card internal padding: `--size-5`–`--size-6`.
- Field stack gap: `--size-3`; section gap (title → fields): `--size-5`.
- CTA separation above primary button: `--size-4` minimum.

## Component catalog

| UI | PrimeVue | Notes |
|----|----------|-------|
| Auth panel | `Card` | `#title`, `#subtitle`, `#content` slots required |
| Sign in | `Button` | `severity="primary"`, full width on auth forms |
| Email | `InputText` | `type="email"`, paired `<label for>` |
| Password | `Password` | Mask toggle; paired `<label for>` |
| Forgot password | `router-link` or text link | Styled with `--text-2`, token spacing |

## Do's and Don'ts

- **Do** use semantic CSS variables and PrimeVue components from this catalog.
- **Do** use scoped CSS classes for layout; keep templates free of inline `style=""`.
- **Don't** use raw hex in `.vue` or component CSS.
- **Don't** use native `<input>` / `<button>` when a catalog component exists.

## Known drift (resolved 2026-07-04)

- ~~Login route used native inputs and hex colors~~ — polished in `LoginView.vue`.

## Decision log

### 2026-07-04 — /login (@heyeddi-design polish)

**Context:** Brownfield critique (`.heyeddi/docs/login-critique.md`) found P0 token/component drift — native inputs, inline hex, cramped 280px layout. SecureVault product register; personas not yet in `product.md`.

**We chose:**
- Centered auth card at 28rem max-width with OpenProps spacing (`--size-2`–`--size-6`) and semantic surfaces (`--surface-1`, `--surface-2`, `--text-1`, `--text-2`).
- Product-facing copy: “Sign in to SecureVault” title + supportive subtitle for trust (critique P1 persona/trust scores).
- Forgot-password link → placeholder `/forgot-password` route (surface-completeness affordance; API deferred).

**Component strategy:**
- Auth panel → PrimeVue `Card` (`#title`, `#subtitle`, `#content`)
- Email → `InputText` with `for`/`id` labels
- Password → `Password` (toggle mask; catalog updated from generic InputText)
- Sign in → `Button` primary, full width, form submit
- App shell → semantic `<main>` in `App.vue` (a11y + existing unit test)

**We rejected:**
- Keeping inline hex / native controls — direct P0 critique blockers.
- Greenfield `shape` — IA (email, password, sign-in) was already correct.
- Remember-me / SSO in this pass — P2; deferred until product personas defined.

**Critique → fixes:** P0 hex/PrimeVue drift, inline styles, missing Card → resolved. P1 spacing, hierarchy, forgot-password, a11y labels → resolved.

**Open questions:** Wire auth API and forgot-password flow when backend ready.
