<template>
  <header class="app-topbar">
    <button
      type="button"
      class="app-topbar__menu"
      :aria-label="t.product.openMenu"
      @click="emit('toggle-sidebar')"
    >
      <i class="pi pi-bars" aria-hidden="true" />
    </button>

    <p class="app-topbar__title">{{ pageTitle }}</p>

    <div class="app-topbar__locale" role="group" :aria-label="t.brand.localeEn">
      <button
        type="button"
        class="app-topbar__locale-btn"
        :class="{ 'app-topbar__locale-btn--active': locale === 'en' }"
        :aria-pressed="locale === 'en'"
        @click="setLocale('en')"
      >
        EN
      </button>
      <button
        type="button"
        class="app-topbar__locale-btn"
        :class="{ 'app-topbar__locale-btn--active': locale === 'es' }"
        :aria-pressed="locale === 'es'"
        @click="setLocale('es')"
      >
        ES
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useLocale } from "@/composables/useLocale";

const emit = defineEmits<{ "toggle-sidebar": [] }>();

const route = useRoute();
const { locale, t, setLocale } = useLocale();

const pageTitle = computed(() => {
  if (route.path === "/settings") return t.value.product.settings;
  if (route.path === "/dashboard") return t.value.product.team;
  return t.value.brand.name;
});
</script>

<style scoped>
.app-topbar {
  display: flex;
  align-items: center;
  gap: var(--size-3);
  height: var(--topbar-height);
  padding: 0 var(--size-4);
  border-bottom: 1px solid var(--border-1);
  background: light-dark(var(--surface-0), var(--surface-2));
}

.app-topbar__menu {
  display: none;
  align-items: center;
  justify-content: center;
  width: 2.75rem;
  height: 2.75rem;
  border: 1px solid var(--border-1);
  border-radius: var(--radius-2);
  background: var(--surface-1);
  color: var(--text-1);
  cursor: pointer;
}

.app-topbar__title {
  margin: 0;
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.app-topbar__locale {
  display: flex;
  gap: var(--size-1);
  margin-left: auto;
}

.app-topbar__locale-btn {
  border: 1px solid var(--border-1);
  background: var(--surface-1);
  color: var(--text-2);
  font-size: var(--font-size-0);
  padding: var(--size-1) var(--size-2);
  border-radius: var(--radius-2);
  cursor: pointer;
  min-width: 2.75rem;
  min-height: 2.75rem;
}

.app-topbar__locale-btn--active {
  color: var(--brand);
  border-color: var(--brand);
  background: var(--brand-subtle);
}

@media (max-width: 768px) {
  .app-topbar__menu {
    display: inline-flex;
  }
}
</style>
