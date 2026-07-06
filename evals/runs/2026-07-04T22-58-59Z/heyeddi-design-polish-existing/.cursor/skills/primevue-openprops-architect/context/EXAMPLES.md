
# Examples — PrimeVue + OpenProps

## Good — token-based card

```vue
<template>
  <Card class="settings-card">
    <template #title>Profile</template>
    <p class="settings-card__hint">Update your display name.</p>
  </Card>
</template>

<style scoped>
.settings-card {
  background: var(--surface-2);
  padding: var(--size-fluid-3);
}
.settings-card__hint {
  color: var(--text-2);
  font-size: var(--font-size-2);
}
</style>
```

## Bad — hardcoded styles

```vue
<template>
  <div style="background: #fff; padding: 16px;">
    <Button label="Save" color="blue" />
  </div>
</template>
```
