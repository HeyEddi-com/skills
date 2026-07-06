<template>
  <BrandShell v-if="layout === 'brand'" :show-features-link="showFeaturesLink">
    <router-view />
  </BrandShell>
  <AppShell v-else>
    <router-view />
  </AppShell>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import BrandShell from "@/components/layout/BrandShell.vue";
import AppShell from "@/components/layout/AppShell.vue";

const route = useRoute();
const layout = computed(() => (route.meta.layout as string) ?? "app");
const showFeaturesLink = computed(() => Boolean(route.meta.showFeaturesLink));
</script>

