<template>
  <div class="app-shell">
    <AppSidebar :open="sidebarOpen" @close="sidebarOpen = false" />
    <div v-if="sidebarOpen" class="app-shell__backdrop" @click="sidebarOpen = false" />
    <div class="app-shell__main">
      <AppTopBar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="app-shell__content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import AppSidebar from "./AppSidebar.vue";
import AppTopBar from "./AppTopBar.vue";

const sidebarOpen = ref(false);
</script>

<style scoped>
.app-shell {
  display: flex;
  min-height: 100vh;
  background: var(--surface-1);
  color: var(--text-1);
}

.app-shell__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.app-shell__content {
  flex: 1;
  overflow-y: auto;
}

.app-shell__backdrop {
  display: none;
}

@media (max-width: 48rem) {
  .app-shell__backdrop {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 90;
    background: light-dark(rgb(0 0 0 / 0.35), rgb(0 0 0 / 0.55));
  }
}
</style>
