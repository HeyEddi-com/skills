<template>
  <div class="dashboard">
    <header class="dashboard__header">
      <div class="dashboard__intro">
        <h1 class="dashboard__title">{{ t.dashboard.title }}</h1>
        <p class="dashboard__subtitle">{{ t.dashboard.subtitle }}</p>
      </div>
      <Button
        type="button"
        :label="t.dashboard.refresh"
        icon="pi pi-refresh"
        severity="secondary"
        outlined
        :loading="loading"
        @click="refresh"
      />
    </header>

    <Message v-if="offlineDemo" severity="warn" :closable="false" class="dashboard__banner">
      {{ t.dashboard.offlineBanner }}
    </Message>

    <div class="dashboard__stats">
      <Card class="dashboard__stat-card">
        <template #content>
          <p class="dashboard__stat-label">{{ t.dashboard.statMembers }}</p>
          <p class="dashboard__stat-value">{{ users.length }}</p>
        </template>
      </Card>
      <Card class="dashboard__stat-card">
        <template #content>
          <p class="dashboard__stat-label">{{ t.dashboard.statSource }}</p>
          <p class="dashboard__stat-value">{{ dataSourceLabel }}</p>
        </template>
      </Card>
    </div>

    <Card class="dashboard__table-card">
      <template #content>
        <DataTable
          :value="users"
          :loading="loading"
          striped-rows
          data-key="id"
          class="dashboard__table"
        >
          <Column field="email" :header="t.dashboard.columnEmail" sortable />
          <Column field="id" :header="t.dashboard.columnId" sortable />
          <template #empty>
            <div class="dashboard__empty">
              <p>{{ t.dashboard.empty }}</p>
            </div>
          </template>
        </DataTable>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Message from "primevue/message";
import { useLocale } from "@/composables/useLocale";
import { useUsers } from "@/composables/useUsers";
import { DEMO_USERS } from "@/data/demoUsers";

const { t } = useLocale();
const { users, loading, fetchUsers } = useUsers();

const offlineDemo = ref(false);

const dataSourceLabel = computed(() =>
  offlineDemo.value ? t.value.dashboard.sourceDemo : t.value.dashboard.sourceLive,
);

async function refresh(): Promise<void> {
  offlineDemo.value = false;
  try {
    await fetchUsers();
  } catch {
    users.value = [...DEMO_USERS];
    offlineDemo.value = true;
  }
}

onMounted(() => {
  void refresh();
});
</script>

<style scoped>
.dashboard {
  max-width: var(--content-max);
  margin: 0 auto;
  padding: var(--size-5) var(--size-4) var(--size-6);
  display: flex;
  flex-direction: column;
  gap: var(--size-5);
}

.dashboard__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--size-4);
  flex-wrap: wrap;
}

.dashboard__title {
  margin: 0;
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-7);
  letter-spacing: var(--font-letterspacing-0);
}

.dashboard__subtitle {
  margin: var(--size-2) 0 0;
  color: var(--text-2);
  font-size: var(--font-size-1);
  max-width: 36rem;
}

.dashboard__banner {
  width: 100%;
}

.dashboard__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--size-4);
}

@media (max-width: 480px) {
  .dashboard__stats {
    grid-template-columns: 1fr;
  }
}

.dashboard__stat-card :deep(.p-card-body) {
  padding: var(--size-4);
}

.dashboard__stat-card {
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.04);
}

.dashboard__stat-label {
  margin: 0;
  font-size: var(--font-size-0);
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.dashboard__stat-value {
  margin: var(--size-2) 0 0;
  font-size: var(--font-size-4);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.dashboard__table-card {
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.04);
}

.dashboard__table-card :deep(.p-card-body) {
  padding: 0;
}

.dashboard__table :deep(.p-datatable-thead > tr > th) {
  background: var(--surface-1);
  color: var(--text-2);
  font-size: var(--font-size-0);
  font-weight: var(--font-weight-6);
  border-color: var(--border-1);
}

.dashboard__table :deep(.p-datatable-tbody > tr > td) {
  border-color: var(--border-1);
}

.dashboard__empty {
  padding: var(--size-6);
  text-align: center;
  color: var(--text-2);
}

.dashboard__empty p {
  margin: 0;
}
</style>
