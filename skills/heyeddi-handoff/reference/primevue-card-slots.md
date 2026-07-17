# PrimeVue Card slots

**PrimeVue `Card` does not render default-slot children.** Body content must use `<template #content>`.

## Correct

```vue
<Card class="settings__card">
  <template #title>Profile</template>
  <template #subtitle>Your name and sign-in email.</template>
  <template #content>
    <div class="settings__fields">
      <InputText v-model="displayName" />
    </div>
  </template>
</Card>
```

## Wrong (renders empty card body in browser)

```vue
<Card class="settings__card">
  <template #title>Profile</template>
  <div class="settings__fields">
    <InputText v-model="displayName" />
  </div>
</Card>
```

Symptom: Playwright/screenshots show title + subtitle only: no inputs, toggles, or stat values.

## Named slots

| Slot | Use |
|------|-----|
| `#title` | Card heading |
| `#subtitle` | Muted hint under title |
| `#content` | **All body UI**: fields, toggles, stat values, tables |
| `#footer` | Optional actions row |

## Verification

- `verify_handoff.py --check`: fails when any `<Card>` has loose elements outside named slots
- Playwright content gates: `/settings` requires ≥2 inputs in `.settings`; `/dashboard` requires stat values

See also `handoff-to-code.md` common failures.
