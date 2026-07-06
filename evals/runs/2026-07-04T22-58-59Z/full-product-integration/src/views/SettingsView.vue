<template>
  <div class="settings">
    <header class="settings__header">
      <h1 class="settings__title">{{ t.settings.title }}</h1>
      <p class="settings__subtitle">{{ t.settings.subtitle }}</p>
    </header>

    <div class="settings__cards">
      <Card class="settings__card">
        <template #title>{{ t.settings.profileTitle }}</template>
        <template #subtitle>{{ t.settings.profileSubtitle }}</template>
        <template #content>
          <div class="settings__fields">
            <div class="settings__field">
              <label class="settings__label" for="display-name">{{ t.settings.displayNameLabel }}</label>
              <InputText
                id="display-name"
                v-model="displayName"
                class="settings__input"
                autocomplete="name"
              />
            </div>
            <div class="settings__field">
              <label class="settings__label" for="email">{{ t.settings.emailLabel }}</label>
              <InputText
                id="email"
                v-model="email"
                type="email"
                class="settings__input"
                autocomplete="email"
              />
            </div>
          </div>
        </template>
      </Card>

      <Card class="settings__card">
        <template #title>{{ t.settings.notificationsTitle }}</template>
        <template #subtitle>{{ t.settings.notificationsSubtitle }}</template>
        <template #content>
          <div class="settings__toggle-row">
            <label class="settings__toggle-label" for="email-updates">{{ t.settings.emailUpdatesLabel }}</label>
            <ToggleSwitch v-model="emailUpdates" input-id="email-updates" />
          </div>
        </template>
      </Card>
    </div>

    <div class="settings__save">
      <!-- Save changes — primary CTA outside card stack -->
      <Button type="button" :label="t.settings.save" @click="save" />
    </div>

    <Message v-if="saved" severity="success" :closable="false" class="settings__banner">
      {{ t.settings.savedMessage }}
    </Message>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import ToggleSwitch from "primevue/toggleswitch";
import { useLocale } from "@/composables/useLocale";

const { t } = useLocale();

const displayName = ref(t.value.settings.demoName);
const email = ref(t.value.settings.demoEmail);
const emailUpdates = ref(true);
const saved = ref(false);

function save(): void {
  saved.value = true;
}
</script>

<style scoped>
.settings {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--size-6) var(--size-5);
}

.settings__header {
  margin-bottom: var(--size-5);
}

.settings__title {
  margin: 0;
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-7);
  letter-spacing: var(--font-letterspacing-0);
}

.settings__subtitle {
  margin: var(--size-2) 0 0;
  color: var(--text-2);
  font-size: var(--font-size-1);
}

.settings__cards {
  display: flex;
  flex-direction: column;
  gap: var(--size-6);
}

.settings__card {
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.04);
}

.settings__card :deep(.p-card-body) {
  padding: var(--size-6);
}

.settings__fields {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
}

.settings__field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.settings__label {
  font-size: var(--font-size-0);
  color: var(--text-2);
  font-weight: var(--font-weight-5);
}

.settings__input {
  width: 100%;
}

.settings__toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--size-4);
}

.settings__toggle-label {
  font-size: var(--font-size-1);
  color: var(--text-1);
}

.settings__save {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--size-6);
}

.settings__banner {
  margin-top: var(--size-4);
}

@media (max-width: 640px) {
  .settings__save {
    justify-content: stretch;
  }

  .settings__save :deep(.p-button) {
    width: 100%;
  }
}
</style>
