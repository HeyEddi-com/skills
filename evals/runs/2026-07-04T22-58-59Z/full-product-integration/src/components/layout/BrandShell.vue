<template>
  <div class="brand-shell">
    <a class="skip-link" href="#main-content">{{ t.brand.skipToMain }}</a>
    <BrandNav :show-features-link="showFeaturesLink" />
    <main id="main-content" class="brand-shell__main">
      <slot />
    </main>
    <footer class="brand-shell__footer">
      <p>{{ t.brand.footer }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import BrandNav from "@/components/layout/BrandNav.vue";
import { useLocale } from "@/composables/useLocale";

defineProps<{
  showFeaturesLink?: boolean;
}>();

const { t } = useLocale();
</script>

<style scoped>
.brand-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--surface-1);
  color: var(--text-1);
}

.skip-link {
  position: absolute;
  left: var(--size-3);
  top: -100%;
  z-index: 100;
  padding: var(--size-2) var(--size-3);
  background: var(--surface-2);
  color: var(--text-1);
  border-radius: var(--radius-2);
  text-decoration: none;
}

.skip-link:focus {
  top: var(--size-3);
}

.brand-shell__main {
  flex: 1;
}

.brand-shell__footer {
  border-top: 1px solid var(--border-1);
  padding: var(--size-4);
  text-align: center;
  color: var(--text-2);
  font-size: var(--font-size-0);
}
</style>
