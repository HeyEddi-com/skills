<template>
  <div class="app-shell">
    <a class="skip-link" href="#main-content">{{ t.brand.skipToMain }}</a>
    <AppSidebar
      class="app-shell__sidebar"
      :class="{ 'app-shell__sidebar--open': sidebarOpen }"
    />
    <div
      v-if="sidebarOpen"
      class="app-shell__backdrop"
      aria-hidden="true"
      @click="sidebarOpen = false"
    />
    <div class="app-shell__main-column">
      <AppTopBar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main id="main-content" class="app-shell__main">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import AppSidebar from "@/components/layout/AppSidebar.vue";
import AppTopBar from "@/components/layout/AppTopBar.vue";
import { useLocale } from "@/composables/useLocale";

const { t } = useLocale();
const sidebarOpen = ref(false);
</script>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
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

.app-shell__main-column {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.app-shell__main {
  flex: 1;
}

.app-shell__backdrop {
  display: none;
}

@media (max-width: 768px) {
  .app-shell__sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 200ms ease;
  }

  .app-shell__sidebar--open {
    transform: translateX(0);
  }

  .app-shell__backdrop {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 40;
    background: rgb(0 0 0 / 0.4);
  }
}
</style>
