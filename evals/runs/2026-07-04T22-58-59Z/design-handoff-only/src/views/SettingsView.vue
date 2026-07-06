<template>
  <section class="settings">
    <header class="settings__header">
      <h1 class="settings__title">Settings</h1>
      <p class="settings__subtitle settings__subtitle--desktop">
        Manage your profile and how we reach you.
      </p>
      <p class="settings__subtitle settings__subtitle--mobile">Profile and notifications</p>
    </header>

    <div class="settings__cards">
      <Card class="settings__card">
        <template #title>Profile</template>
        <template #subtitle>Your name and sign-in email.</template>
        <template #content>
          <div class="settings__fields">
            <label class="settings__field">
              <span class="settings__label">Display name</span>
              <InputText v-model="displayName" class="settings__input" />
            </label>
            <label class="settings__field">
              <span class="settings__label">Email</span>
              <InputText v-model="email" type="email" class="settings__input" />
            </label>
          </div>
        </template>
      </Card>

      <Card class="settings__card">
        <template #title>Notifications</template>
        <template #subtitle>Choose how you hear about account activity.</template>
        <template #content>
          <div class="settings__toggle-row settings__toggle-row--desktop">
            <span class="settings__toggle-label">Email updates</span>
            <ToggleSwitch v-model="emailUpdates" />
          </div>
          <div class="settings__empty settings__empty--mobile">
            <p class="settings__empty-title">No channels configured</p>
            <p class="settings__empty-hint">Add email or push when you connect integrations.</p>
          </div>
        </template>
      </Card>
    </div>

    <div class="settings__save">
      <Button label="Save changes" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import ToggleSwitch from "primevue/toggleswitch";

const displayName = ref("Alex Rivera");
const email = ref("alex@example.com");
const emailUpdates = ref(true);
</script>

<style scoped>
.settings {
  padding: var(--size-6) var(--size-5);
  max-width: var(--content-max-width);
}

.settings__header {
  margin-bottom: var(--size-6);
}

.settings__title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-7);
  color: var(--text-1);
}

.settings__subtitle {
  margin: 0;
  font-size: var(--font-size-2);
  color: var(--text-2);
}

.settings__subtitle--mobile {
  display: none;
}

.settings__cards {
  display: flex;
  flex-direction: column;
  gap: var(--size-6);
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
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-5);
  color: var(--text-2);
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
  font-size: var(--font-size-2);
  color: var(--text-1);
}

.settings__empty {
  display: none;
}

.settings__empty-title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-2);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.settings__empty-hint {
  margin: 0;
  font-size: var(--font-size-1);
  color: var(--text-2);
}

.settings__save {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--size-6);
}

@media (max-width: 48rem) {
  .settings__subtitle--desktop {
    display: none;
  }

  .settings__subtitle--mobile {
    display: block;
  }

  .settings__toggle-row--desktop {
    display: none;
  }

  .settings__empty--mobile {
    display: block;
  }

  .settings__save {
    justify-content: stretch;
  }

  .settings__save :deep(.p-button) {
    width: 100%;
  }
}
</style>
