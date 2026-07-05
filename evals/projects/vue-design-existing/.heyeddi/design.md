# Design — SecureVault (out of sync with code)

> **Eval:** Documents OpenProps + PrimeVue, but `LoginView.vue` **violates** this file. `@heyeddi-design` must **audit existing UI**, update this doc from code (scan mode), then **polish**.

## System (intended)

- OpenProps tokens + PrimeVue InputText, Button, Card
- No raw hex in Vue/CSS

## Component catalog

| UI | PrimeVue |
|----|----------|
| Sign in | Button |
| Email / password | InputText |

## Known drift

- Login route uses native `<input>` and hex colors — fix via `polish` workflow
