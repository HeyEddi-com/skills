# Design brief — SecureVault login

**Feature:** `securevault-login`  
**Route:** `/login` → `LoginView.vue`  
**Register:** product (app UI)  
**Date:** 2026-07-04

## Feature summary

SecureVault is a team password manager. The login screen is the first product touchpoint for small teams who need a fast, trustworthy sign-in before reaching the vault. The surface must feel calm and professional — not a generic admin template — with every sign-in affordance visible even when backend auth is stubbed.

## Audience

- **Primary persona:** SMB team lead / ops person signing in before daily work (inferred from product.md audience)
- **Route intent:** Task-focused entry — understand "sign in to SecureVault" in under 5 seconds, complete credentials, recover if forgotten
- **Direction row:** Warm, approachable (Notion marketing / Superhuman settings) — avoid cold gray enterprise admin
- **Differentiation:** Generous spacing and plain-language errors vs cramped competitor login modals

## Primary user action

Sign in with email and password.

## Design direction

- Centered card on `--surface-1` canvas; elevated `--surface-2` panel with border + subtle shadow
- Indigo primary (Aura preset) for Sign in CTA
- Display title + muted subtitle; max form width ~24rem
- Mobile-first: full-width card padding on 375px; centered column on 768+

## Scope

- **In:** `/login` complete sign-in archetype; `/forgot-password` placeholder view
- **Out:** SSO buttons, sign-up flow implementation, dashboard post-auth (stub redirect only)

## Layout regions

```
┌─────────────────────────────────────────────┐
│  [page canvas — surface-1, min-height 100vh]│
│         ┌─────────────────────────┐         │
│         │ BRAND: SecureVault      │         │
│         │ subtitle                │         │
│         ├─────────────────────────┤         │
│         │ [error banner if any]   │         │
│         │ Email label + input     │         │
│         │ Password label + input  │         │
│         │ [Remember me] [Forgot?] │  ← utility row
│         │ [ Sign in — primary ]   │         │
│         ├─────────────────────────┤         │
│         │ footer: Sign up link    │         │
│         └─────────────────────────┘         │
└─────────────────────────────────────────────┘
```

| Region | Content |
|--------|---------|
| Header | Product name, subtitle "Sign in to your team vault" |
| Alert | Inline `Message` for auth / network errors |
| Form | Email (`InputText`), Password (`Password` with toggle) |
| Utility row | `Checkbox` Remember me + text link Forgot password? |
| Primary CTA | Full-width `Button` Sign in |
| Footer | "Don't have an account?" + Sign up link (placeholder) |

## Component map

| Region | PrimeVue |
|--------|----------|
| Card shell | `Card` (#title, #subtitle, #content, #footer) |
| Email | `InputText` + `<label>` |
| Password | `Password` (toggle mask) |
| Remember me | `Checkbox` |
| Forgot password | `RouterLink` |
| Sign in | `Button` (loading prop) |
| Errors | `Message` severity="error" |
| Footer sign-up | `RouterLink` |

## Key states

| State | Behavior |
|-------|----------|
| Default | Empty fields, Sign in enabled |
| Validation | Inline field errors on blur/submit; email format check |
| Loading | Button `loading`, inputs disabled |
| Error | Page-level Message: "Invalid email or password" (stub) |
| Success | Stub: brief loading then error OR toast + redirect note in deferred wiring |

## Copy

| Element | Text |
|---------|------|
| Title | SecureVault |
| Subtitle | Sign in to your team vault |
| Email label | Email |
| Password label | Password |
| Remember me | Remember me on this device |
| Forgot | Forgot password? |
| CTA | Sign in |
| Footer | Don't have an account? **Sign up** |
| Validation email | Enter a valid email address |
| Validation password | Password is required |
| Auth error | Invalid email or password. Please try again. |

## Surface completeness audit (sign-in archetype)

| Check | Status |
|-------|--------|
| Page title + subtitle | ✓ Header in card |
| Primary CTA (Sign in) | ✓ |
| Email + password fields | ✓ |
| Forgot password link | ✓ → `/forgot-password` |
| Remember me | ✓ Checkbox |
| Sign-up / invite path | ✓ Footer link (placeholder route) |
| SSO row | Deferred — documented below |
| Legal footer (terms/privacy) | Deferred — team app, not public marketing |
| Loading state | ✓ Button loading |
| Error state | ✓ Message banner |
| Validation state | ✓ Field-level |
| Spacing: card padding `--size-5` | ✓ |
| Spacing: section gaps `--size-4`–`--size-5` | ✓ |
| Spacing: CTA separation from fields | ✓ `--size-4`+ |
| Max-width form constraint | ✓ ~24rem card |

## Deferred wiring

| UI element | Shipped as | Wire later |
|------------|------------|------------|
| Sign in button | Client validation + 800ms stub; shows auth error Message | `POST /api/auth/login` → session/JWT, redirect `/dashboard` |
| Remember me | Persists checkbox to `localStorage` key `sv_remember_me` | Secure refresh token / extended session server-side |
| Forgot password link | `/forgot-password` placeholder view with back link | Reset API + email template + token flow |
| Sign up footer link | `/signup` placeholder or disabled toast "Contact your admin" | Registration / invite API |
| SSO buttons (Google, Microsoft) | **Omitted UI** — not shipped this eval | OAuth providers + callback routes |
| Post-login redirect | Stays on login with stub error | Router guard + `/dashboard` |
| i18n (`es`) | English copy only | `vue-i18n` locale files per foundations |
| Rate limiting / lockout UI | Not shown | Backend 429 handling + inline copy |

## Open questions

None — eval scope is single login surface with stubbed auth.
