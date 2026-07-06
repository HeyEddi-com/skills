# Critique — /login (2026-07-04)

## First impression

The login screen reads as an unfinished prototype: a narrow 280px column with inline styles, microscopic type, and stark black inputs on an otherwise light page. It does not feel like SecureVault — a product register app where trust and clarity matter at the front door. Nothing signals PrimeVue, OpenProps, or the design system documented in `design.md`.

## What's working

- Route and view exist; email/password/sign-in IA is correct for a minimal auth surface.
- Form fields are wired with `v-model`; sign-in handler stub is in place for later auth integration.
- Project stack (PrimeVue, OpenProps tokens in `tokens.css`, Aura preset in `main.ts`) is ready — the view simply does not use it.

## Issues (priority)

### P0 — ship blockers

| Issue | Evidence | Fix direction |
|-------|----------|---------------|
| Native inputs bypass PrimeVue theme | `<input>` with inline `background: #000` | Replace with PrimeVue `InputText` and `Password`; inherit Aura styling |
| Raw hex colors throughout | `#999`, `#aaa`, `#000`, `#fff`, `#3dd68c` on every element | Remove all inline styles; use semantic tokens (`--surface-*`, `--text-*`) and PrimeVue primary |
| Inline `style=""` on all nodes | Entire template is inline-styled | Scoped CSS classes + token-based spacing/typography |
| No Card / layout shell | Flat `div` with `padding: 8px` | Wrap in PrimeVue `Card` with `#title`, `#subtitle`, `#content`; center on viewport |
| Token drift vs `design.md` | Doc specifies OpenProps + PrimeVue; code uses none | Align implementation to component catalog |

### P1 — hierarchy / polish

| Issue | Evidence | Fix direction |
|-------|----------|---------------|
| Cramped spacing | 8px padding, 4px input padding, 8px button margin | Use OpenProps scale: `--size-4`–`--size-6` for gaps and card padding |
| Weak typographic hierarchy | H1 at 14px `#999`; labels at 10px | Page title via Card `#title`; labels at `--font-size-1` / `--text-2` |
| Form too narrow | `max-width: 280px` | Constrain form at ~24–28rem, center in viewport with min-height shell |
| Missing auth affordances | No forgot-password, remember-me, or product context | Add forgot-password link (stub route or `#`); subtitle naming SecureVault |
| No field association / a11y | Labels not linked via `for`/`id` | Pair labels with inputs; ensure focus order and visible focus rings (PrimeVue default) |
| App shell missing `<main>` | `App.vue` is bare `router-view`; unit test expects `main` | Add semantic `main` wrapper for router outlet |

### P2 — nice-to-have

- Remember-me checkbox (deferred wiring until auth API exists).
- Sign-up / invite alternate path copy.
- Inline validation and error Message on failed sign-in.
- SSO row if product.md later defines team/enterprise persona.

## Token & component drift

| `design.md` (intended) | Code (actual) |
|------------------------|---------------|
| OpenProps semantic tokens (`--surface-1`, `--text-1`) | Hardcoded hex only |
| PrimeVue `InputText` for email/password | Native `<input>` |
| PrimeVue `Button` for sign in | Native `<button>` with custom green hex |
| PrimeVue `Card` for panel | Unstyled `div` |
| No raw hex in Vue/CSS | Six hex values in inline styles |

`tokens.css` correctly aliases OpenProps grays and sets body typography; `LoginView.vue` ignores the entire token layer.

## Audience fit

**Primary persona:** Not defined in `product.md` (eval scaffold). Inferred: security-conscious product user signing into SecureVault.  
**Route:** `/login` — product register, trust-sensitive entry point.

| Dimension | Score | Evidence | Fix |
|-----------|-------|----------|-----|
| Persona recognition | 2/5 | Generic "Login" heading; no product name or trust cues | Card title "Sign in to SecureVault"; supportive subtitle |
| Job alignment | 4/5 | Email, password, sign-in present | Keep IA; improve CTA prominence via PrimeVue Button |
| Trust | 1/5 | Black inputs and neon green button feel broken/untrustworthy | System tokens + consistent primary color |
| Tone | 2/5 | Cramped, debug-like styling | Calm spacing, readable type, professional card layout |
| Differentiation | 2/5 | Could be any thrown-together form | Apply HeyEddi stack consistently |
| Anti-audience | 4/5 | Nothing actively misleading | — |

**Verdict:** REVISE (Trust and Persona recognition ≤ 2) — address via **polish** (visual/system alignment), not full **shape**; IA is acceptable.

## Recommended next step

- [x] `polish` — spacing, PrimeVue, tokens (primary path)
- [ ] `document` — sync `design.md` Colors/Layout after polish
- [ ] `shape` — only if personas/SSO requirements expand scope
