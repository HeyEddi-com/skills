<template>
  <header class="app-topbar">
    <div class="app-topbar__left">
      <button
        type="button"
        class="app-topbar__menu"
        aria-label="Open navigation menu"
        @click="emit('toggle-sidebar')"
      >
        <span class="app-topbar__menu-icon" aria-hidden="true" />
      </button>
      <span class="app-topbar__breadcrumb">{{ pageTitle }}</span>
      <span class="app-topbar__brand-mobile">SecureVault</span>
    </div>

    <div class="app-topbar__right">
      <InputText
        v-model="searchQuery"
        class="app-topbar__search"
        placeholder="Search…"
        aria-label="Search"
      />
      <div class="app-topbar__avatar" aria-hidden="true" />
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import InputText from "primevue/inputtext";

const emit = defineEmits<{ "toggle-sidebar": [] }>();

const route = useRoute();
const searchQuery = ref("");

const pageTitle = computed(() => {
  const name = route.name?.toString() ?? "";
  if (name === "settings") return "Settings";
  return name.charAt(0).toUpperCase() + name.slice(1);
});
</script>

<style scoped>
.app-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--topbar-height);
  padding-inline: var(--size-5);
  background: var(--surface-2);
  border-bottom: 1px solid var(--surface-3);
  flex-shrink: 0;
}

.app-topbar__left {
  display: flex;
  align-items: center;
  gap: var(--size-3);
}

.app-topbar__menu {
  display: none;
  align-items: center;
  justify-content: center;
  width: var(--size-7);
  height: var(--size-7);
  padding: 0;
  border: none;
  border-radius: var(--radius-2);
  background: transparent;
  cursor: pointer;
}

.app-topbar__menu-icon,
.app-topbar__menu-icon::before,
.app-topbar__menu-icon::after {
  display: block;
  width: var(--size-5);
  height: 2px;
  background: var(--text-1);
  border-radius: var(--radius-1);
}

.app-topbar__menu-icon {
  position: relative;
}

.app-topbar__menu-icon::before,
.app-topbar__menu-icon::after {
  content: "";
  position: absolute;
  left: 0;
}

.app-topbar__menu-icon::before {
  top: calc(-1 * var(--size-2));
}

.app-topbar__menu-icon::after {
  top: var(--size-2);
}

.app-topbar__breadcrumb {
  font-size: var(--font-size-2);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.app-topbar__brand-mobile {
  display: none;
  font-size: var(--font-size-3);
  font-weight: var(--font-weight-7);
  color: var(--text-1);
}

.app-topbar__right {
  display: flex;
  align-items: center;
  gap: var(--size-3);
}

.app-topbar__search {
  width: 12rem;
}

.app-topbar__avatar {
  width: var(--size-7);
  height: var(--size-7);
  border-radius: var(--radius-round);
  background: var(--brand);
  flex-shrink: 0;
}

@media (max-width: 48rem) {
  .app-topbar__menu {
    display: flex;
  }

  .app-topbar__breadcrumb {
    display: none;
  }

  .app-topbar__brand-mobile {
    display: block;
  }

  .app-topbar__search {
    display: none;
  }
}
</style>
