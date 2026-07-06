<template>
  <main class="app-shell">
    <router-view />
  </main>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: var(--surface-1);
  color: var(--text-1);
}
</style>
