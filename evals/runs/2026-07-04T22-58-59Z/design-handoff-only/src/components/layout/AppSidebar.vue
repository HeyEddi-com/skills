<template>
  <aside class="app-sidebar" :class="{ 'app-sidebar--open': open }">
    <header class="app-sidebar__brand">
      <span class="app-sidebar__title">SecureVault</span>
      <span class="app-sidebar__subtitle">Workspace</span>
    </header>

    <nav class="app-sidebar__nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="nav-link"
        :class="{ 'nav-link--active': isActive(item.to) }"
        @click="emit('close')"
      >
        {{ item.label }}
      </RouterLink>
    </nav>

    <div class="app-sidebar__user">
      <div class="app-sidebar__avatar" aria-hidden="true">A</div>
      <div class="app-sidebar__user-info">
        <span class="app-sidebar__user-name">Alex Rivera</span>
        <span class="app-sidebar__user-email">alex@example.com</span>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

defineProps<{ open?: boolean }>();
const emit = defineEmits<{ close: [] }>();

const navItems = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Documents", to: "/documents" },
  { label: "Team", to: "/team" },
  { label: "Settings", to: "/settings" },
];

const route = useRoute();

function isActive(path: string): boolean {
  return route.path === path;
}
</script>

<style scoped>
.app-sidebar {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  width: var(--sidebar-width);
  flex-shrink: 0;
  padding: var(--size-4) var(--size-3);
  background: var(--surface-2);
  border-right: 1px solid var(--surface-3);
}

.app-sidebar__brand {
  display: flex;
  flex-direction: column;
  gap: var(--size-1);
  padding: var(--size-2) var(--size-3);
  margin-bottom: var(--size-4);
}

.app-sidebar__title {
  font-size: var(--font-size-3);
  font-weight: var(--font-weight-7);
  color: var(--text-1);
}

.app-sidebar__subtitle {
  font-size: var(--font-size-1);
  color: var(--text-2);
}

.app-sidebar__nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--size-1);
  padding-inline: var(--size-2);
}

.nav-link {
  display: flex;
  align-items: center;
  min-height: 2.75rem;
  padding: var(--size-2) var(--size-3);
  padding-inline: var(--size-3);
  border-radius: var(--radius-2);
  color: var(--text-2);
  text-decoration: none;
  font-size: var(--font-size-2);
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-link:hover {
  color: var(--text-1);
  background: var(--surface-1);
}

.nav-link--active {
  background: var(--brand-subtle);
  color: var(--brand);
  font-weight: var(--font-weight-6);
}

.app-sidebar__user {
  display: flex;
  align-items: center;
  gap: var(--size-3);
  margin-top: auto;
  padding: var(--size-3);
  border: 1px solid var(--surface-3);
  border-radius: var(--radius-2);
  background: var(--surface-0);
}

.app-sidebar__avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--size-7);
  height: var(--size-7);
  border-radius: var(--radius-round);
  background: var(--brand);
  color: var(--gray-0);
  font-size: var(--font-size-2);
  font-weight: var(--font-weight-7);
  flex-shrink: 0;
}

.app-sidebar__user-info {
  display: flex;
  flex-direction: column;
  gap: var(--size-1);
  min-width: 0;
}

.app-sidebar__user-name {
  font-size: var(--font-size-2);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.app-sidebar__user-email {
  font-size: var(--font-size-1);
  color: var(--text-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 48rem) {
  .app-sidebar {
    position: fixed;
    inset-block: 0;
    inset-inline-start: 0;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform 0.2s ease;
    min-height: 100vh;
  }

  .app-sidebar--open {
    transform: translateX(0);
  }
}
</style>
