<template>
  <header class="product-nav">
    <RouterLink to="/dashboard" class="product-nav__logo">{{ t.brand.name }}</RouterLink>

    <nav class="product-nav__links" :aria-label="t.product.navLabel">
      <RouterLink
        to="/dashboard"
        class="product-nav__link"
        :class="{ 'product-nav__link--active': isDashboardRoute }"
      >
        {{ t.product.team }}
      </RouterLink>
      <RouterLink
        to="/settings"
        class="product-nav__link"
        :class="{ 'product-nav__link--active': isSettingsRoute }"
      >
        {{ t.product.settings }}
      </RouterLink>
    </nav>

    <div class="product-nav__locale" role="group" :aria-label="t.brand.localeEn">
      <button
        type="button"
        class="product-nav__locale-btn"
        :class="{ 'product-nav__locale-btn--active': locale === 'en' }"
        :aria-pressed="locale === 'en'"
        @click="setLocale('en')"
      >
        EN
      </button>
      <button
        type="button"
        class="product-nav__locale-btn"
        :class="{ 'product-nav__locale-btn--active': locale === 'es' }"
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

const route = useRoute();
const { locale, t, setLocale } = useLocale();

const isDashboardRoute = computed(() => route.path === "/dashboard");
const isSettingsRoute = computed(() => route.path === "/settings");
</script>

<style scoped>
.product-nav {
  display: flex;
  align-items: center;
  gap: var(--size-3);
  padding: var(--size-3) var(--size-4);
  border-bottom: 1px solid var(--border-1);
  background: light-dark(var(--surface-0), var(--surface-2));
}

.product-nav__logo {
  font-weight: var(--font-weight-7);
  font-size: var(--font-size-2);
  color: var(--text-1);
  text-decoration: none;
  letter-spacing: var(--font-letterspacing-0);
}

.product-nav__links {
  display: flex;
  align-items: center;
  gap: var(--size-1);
  margin-left: var(--size-4);
}

.product-nav__link {
  color: var(--text-2);
  text-decoration: none;
  font-size: var(--font-size-1);
  padding: var(--size-2) var(--size-3);
  border-radius: var(--radius-2);
  transition: background 150ms ease, color 150ms ease;
}

.product-nav__link:hover,
.product-nav__link:focus-visible {
  color: var(--text-1);
  background: var(--surface-2);
}

.product-nav__link--active {
  color: var(--brand);
  background: var(--brand-subtle);
}

.product-nav__locale {
  display: flex;
  gap: var(--size-1);
  margin-left: auto;
}

.product-nav__locale-btn {
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

.product-nav__locale-btn--active {
  color: var(--brand);
  border-color: var(--brand);
  background: var(--brand-subtle);
}

@media (max-width: 640px) {
  .product-nav {
    flex-wrap: wrap;
  }

  .product-nav__links {
    order: 3;
    width: 100%;
    margin-left: 0;
  }
}
</style>
