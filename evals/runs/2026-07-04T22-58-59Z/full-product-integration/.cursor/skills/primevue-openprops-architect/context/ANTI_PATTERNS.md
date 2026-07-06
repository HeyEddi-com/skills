
# Anti-patterns — PrimeVue + OpenProps

- NEVER use inline `style=""` attributes or hardcoded hex colors (`#fff`, `#333`).
- NEVER invent PrimeVue props — check component API before use.
- NEVER put body content as direct children of PrimeVue `Card` — use `<template #content>` or the card body is empty in the browser.
- NEVER duplicate Button/Input wrappers when a shared component exists.
- NEVER use Tailwind utility classes if the project uses semantic CSS tokens / OpenProps (check `design.md`).
- NEVER add `open-props` dependency unless scaffold or user requests it.
- NEVER add raw `<style>` blocks with magic numbers — use design tokens.
- NEVER import PrimeVue components globally when the project uses on-demand registration.
