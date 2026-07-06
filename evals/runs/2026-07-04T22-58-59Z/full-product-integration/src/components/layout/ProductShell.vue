<template>
  <div class="product-shell">
    <a class="skip-link" href="#main-content">{{ t.brand.skipToMain }}</a>
    <ProductNav />
    <main id="main-content" class="product-shell__main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import ProductNav from "@/components/layout/ProductNav.vue";
import { useLocale } from "@/composables/useLocale";

const { t } = useLocale();
</script>

<style scoped>
.product-shell {
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

.product-shell__main {
  flex: 1;
}
</style>
