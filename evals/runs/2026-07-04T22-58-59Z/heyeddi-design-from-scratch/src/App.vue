<template>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <main id="main-content">
    <router-view />
  </main>
</template>

<script setup lang="ts">
</script>

<style scoped>
.skip-link {
  position: absolute;
  left: var(--size-3);
  top: var(--size-3);
  z-index: 100;
  padding: var(--size-2) var(--size-3);
  background: var(--surface-2);
  color: var(--text-1);
  border: 1px solid var(--border-1);
  border-radius: var(--radius-2);
  font-size: var(--font-size-1);
  text-decoration: none;
  transform: translateY(-200%);
  transition: transform 0.2s ease;
}

.skip-link:focus {
  transform: translateY(0);
  outline: 2px solid var(--indigo-7);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .skip-link {
    transition: none;
  }
}
</style>
