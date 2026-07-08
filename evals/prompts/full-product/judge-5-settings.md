@heyeddi-handoff implemented /settings from .heyeddi/designs/settings/ per handoff workflow:

- load_handoff used; DESIGN.md consulted/updated
- mockup-brief + Implementation spec; AppShell before route
- SettingsView matches mockups; PrimeVue Card body in `<template #content>`
- Tests pass with **zero Vue Router warnings** in full `npm test` output (fix `LoginView.spec.ts` with `createViewRouter` if needed)

**Process proof:** Open screenshots in `.heyeddi/audits/eval-process/settings/`. FAIL if cards are empty (title only), inputs/toggle missing, or captures absent.

Read all changed files and full npm/pytest output.
