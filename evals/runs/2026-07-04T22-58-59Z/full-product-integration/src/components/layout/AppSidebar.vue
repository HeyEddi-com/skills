<template>
  <aside class="app-sidebar" :aria-label="t.product.navLabel">
    <div class="app-sidebar__brand">
      <RouterLink to="/dashboard" class="app-sidebar__logo">{{ t.brand.name }}</RouterLink>
      <p class="app-sidebar__workspace">{{ t.product.workspace }}</p>
    </div>

    <nav class="app-sidebar__nav">
      <RouterLink
        to="/dashboard"
        class="app-sidebar__nav-link"
        :class="{ 'app-sidebar__nav-link--active': isDashboardRoute }"
      >
        {{ t.product.team }}
      </RouterLink>
      <RouterLink
        to="/settings"
        class="app-sidebar__nav-link"
        :class="{ 'app-sidebar__nav-link--active': isSettingsRoute }"
      >
        {{ t.product.settings }}
      </RouterLink>
    </nav>

    <div class="app-sidebar__user">
      <span class="app-sidebar__avatar" aria-hidden="true">{{ userInitial }}</span>
      <div class="app-sidebar__user-text">
        <p class="app-sidebar__user-name">{{ t.settings.demoName }}</p>
        <p class="app-sidebar__user-email">{{ t.settings.demoEmail }}</p>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useLocale } from "@/composables/useLocale";

const route = useRoute();
const { t } = useLocale();

const isDashboardRoute = computed(() => route.path === "/dashboard");
const isSettingsRoute = computed(() => route.path === "/settings");
const userInitial = computed(() => t.value.settings.demoName.charAt(0).toUpperCase());
</script>

<style scoped>
.app-sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  min-height: 100%;
  padding: var(--size-4);
  border-right: 1px solid var(--border-1);
  background: light-dark(var(--surface-0), var(--surface-2));
}

.app-sidebar__brand {
  margin-bottom: var(--size-5);
}

.app-sidebar__logo {
  display: block;
  font-weight: var(--font-weight-7);
  font-size: var(--font-size-2);
  color: var(--text-1);
  text-decoration: none;
  letter-spacing: var(--font-letterspacing-0);
}

.app-sidebar__workspace {
  margin: var(--size-1) 0 0;
  font-size: var(--font-size-0);
  color: var(--text-2);
}

.app-sidebar__nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--size-1);
}

.app-sidebar__nav-link {
  display: flex;
  align-items: center;
  min-height: 2.75rem;
  padding: var(--size-2) var(--size-3);
  border-radius: var(--radius-2);
  color: var(--text-2);
  text-decoration: none;
  font-size: var(--font-size-1);
  transition: background 150ms ease, color 150ms ease;
}

.app-sidebar__nav-link:hover,
.app-sidebar__nav-link:focus-visible {
  color: var(--text-1);
  background: var(--surface-2);
}

.app-sidebar__nav-link--active {
  color: var(--brand);
  background: var(--brand-subtle);
}

.app-sidebar__user {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: var(--size-3);
  padding: var(--size-3);
  border: 1px solid var(--border-1);
  border-radius: var(--radius-2);
  background: var(--surface-1);
}

.app-sidebar__avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-round);
  background: var(--brand);
  color: var(--gray-0);
  font-weight: var(--font-weight-6);
  font-size: var(--font-size-1);
  flex-shrink: 0;
}

.app-sidebar__user-text {
  min-width: 0;
}

.app-sidebar__user-name {
  margin: 0;
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.app-sidebar__user-email {
  margin: var(--size-1) 0 0;
  font-size: var(--font-size-0);
  color: var(--text-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .app-sidebar {
    min-height: 100vh;
  }
}
</style>
