# Design — SecureVault

> [DESIGN.md format](https://getdesign.md/what-is-design-md): semantic tokens + PrimeVue catalog + Decision log.

## System

- **Token source:** OpenProps via `src/styles/tokens.css` (semantic aliases on `--surface-*`, `--text-*`, `--border-*`, `--size-*`, `--radius-*`)
- **Component library:** PrimeVue 4 + Aura preset (indigo primary in `main.ts`)
- **Register:** product — focused app UI, generous spacing on auth surfaces

## Foundations (always on)

- Responsive mobile-first (375 / 768 / 1440)
- System light/dark via `color-scheme: light dark` + OpenProps grays
- WCAG 2.2 AA target — skip link, labels, focus-visible, error `role="alert"`
- i18n: `en` shipped; `es` deferred (see securevault-login brief)

## Component catalog

| Pattern | PrimeVue | Notes |
|---------|----------|-------|
| Auth card shell | `Card` | Use `#title`, `#subtitle`, `#content`, `#footer` slots |
| Text field | `InputText` | Explicit `<label>`, `fluid` |
| Password field | `Password` | `toggle-mask`, `:feedback="false"` |
| Remember me | `Checkbox` | `:binary="true"` |
| Primary CTA | `Button` | `type="submit"`, `loading`, `fluid` on auth |
| Auth errors | `Message` | `severity="error"`, `:closable="false"` |

## Layout / density rules

- Auth cards: max-width `24rem`, padding `--size-5` internal
- Field stacks: gap `--size-4`; utility row between fields and CTA
- CTA separation: `--size-2`+ margin above Sign in
- Surfaces: `--surface-2` card on `--surface-1` canvas, `--border-1` + subtle shadow

## Exceptions

- No raw hex in Vue/CSS unless listed here.

---

## Decision log

### 2026-07-04 — securevault-login (`@heyeddi-design` shape + craft)

**Context:** First product route for SecureVault eval — complete sign-in archetype with stubbed auth, no designer mockups.

**We chose:**
- Centered elevated card (Superhuman-style single-column focus) for SMB team lead persona — warm, approachable, not cold admin template
- Full sign-in affordances: email, password, remember me, forgot password, sign-up footer
- Stub auth: client validation + 800ms delay → inline error Message (deferred: real API)
- Placeholder views for `/forgot-password` and `/signup` instead of omitting links

**Component strategy:**
- Auth shell → PrimeVue `Card` with all four slots (ANTI_PATTERN: never empty card body)
- Credentials → `InputText` + `Password` with explicit labels for a11y
- Utility row → `Checkbox` + `RouterLink` (forgot password)
- Errors → `Message` banner + field-level `<small role="alert">`
- App shell → skip link + `<main>` in `App.vue`

**We rejected:**
- SSO button row (deferred — no OAuth backend)
- Cramped default PrimeVue card padding (overridden with `--size-5`)
- Inline styles or hex colors (semantic tokens only)

**Pattern borrowed:** Superhuman settings / Notion warmth — generous spacing, plain-language errors, single primary CTA

**Deferred wiring:** See `.heyeddi/designs/securevault-login/brief.md` § Deferred wiring

**Open questions:** none
