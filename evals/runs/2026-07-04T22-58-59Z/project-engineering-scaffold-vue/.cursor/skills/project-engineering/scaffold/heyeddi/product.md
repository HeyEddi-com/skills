# Product

Describe users, routes, and acceptance criteria here.

Skills read this file from `.heyeddi/product.md` (canonical). Legacy root `PRODUCT.md` is still supported.

## Locales (default)

| Code | Language | Status | Notes |
|------|----------|--------|-------|
| `en` | English | shipped | fallback locale |
| `es` | Spanish | shipped | default HeyEddi pair |

- **Detection:** browser language on first visit; fallback `en`.
- **Override:** user language picker (Settings or shell).
- Add rows when scoping new languages; note RTL in Notes column if applicable.

## Foundations waivers

_List only if explicitly out of scope for this product — each needs a one-line reason._

| Foundation | Waived? | Reason |
|------------|---------|--------|
| Responsive | no | |
| System light/dark | no | |
| en + es i18n | no | |
| WCAG 2.2 AA | no | |
| Dyslexia reading mode | no | |

See `heyeddi-design/reference/foundations.md`.
