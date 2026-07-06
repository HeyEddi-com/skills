<template>
  <header class="brand-nav">
    <RouterLink to="/" class="brand-nav__logo">{{ t.brand.name }}</RouterLink>

    <nav class="brand-nav__links" :aria-label="t.brand.features">
      <RouterLink v-if="showFeaturesLink" to="/#features" class="brand-nav__link">
        {{ t.brand.features }}
      </RouterLink>
      <RouterLink
        to="/login"
        class="brand-nav__link"
        :class="{ 'brand-nav__link--active': isLoginRoute }"
      >
        {{ t.brand.signIn }}
      </RouterLink>
    </nav>

    <div class="brand-nav__locale" role="group" :aria-label="t.brand.localeEn">
      <button
        type="button"
        class="brand-nav__locale-btn"
        :class="{ 'brand-nav__locale-btn--active': locale === 'en' }"
        :aria-pressed="locale === 'en'"
        @click="setLocale('en')"
      >
        EN
      </button>
      <button
        type="button"
        class="brand-nav__locale-btn"
        :class="{ 'brand-nav__locale-btn--active': locale === 'es' }"
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

defineProps<{
  showFeaturesLink?: boolean;
}>();

const route = useRoute();
const { locale, t, setLocale } = useLocale();

const isLoginRoute = computed(() => route.path === "/login");
</script>

<style scoped>
.brand-nav {
  display: flex;
  align-items: center;
  gap: var(--size-3);
  padding: var(--size-3) var(--size-4);
  max-width: var(--content-max);
  margin: 0 auto;
  border-bottom: 1px solid var(--border-1);
  background: light-dark(var(--surface-0), var(--surface-2));
}

.brand-nav__logo {
  font-weight: var(--font-weight-7);
  font-size: var(--font-size-2);
  color: var(--text-1);
  text-decoration: none;
  letter-spacing: var(--font-letterspacing-0);
}

.brand-nav__links {
  display: flex;
  align-items: center;
  gap: var(--size-3);
  margin-left: auto;
}

.brand-nav__link {
  color: var(--text-2);
  text-decoration: none;
  font-size: var(--font-size-1);
  padding: var(--size-2) var(--size-3);
  border-radius: var(--radius-2);
  transition: background 150ms ease, color 150ms ease;
}

.brand-nav__link:hover,
.brand-nav__link:focus-visible {
  color: var(--text-1);
  background: var(--surface-2);
}

.brand-nav__link--active {
  color: var(--brand);
  background: var(--brand-subtle);
}

.brand-nav__locale {
  display: flex;
  gap: var(--size-1);
  margin-left: var(--size-2);
}

.brand-nav__locale-btn {
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

.brand-nav__locale-btn--active {
  color: var(--brand);
  border-color: var(--brand);
  background: var(--brand-subtle);
}

@media (max-width: 640px) {
  .brand-nav {
    flex-wrap: wrap;
  }

  .brand-nav__links {
    order: 3;
    width: 100%;
    margin-left: 0;
    justify-content: flex-start;
  }
}
</style>
