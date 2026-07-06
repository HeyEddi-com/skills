<template>
  <div class="login-page">
    <Card class="login-card">
      <template #title>Sign in to SecureVault</template>
      <template #subtitle>Enter your credentials to access your vault.</template>
      <template #content>
        <form class="login-form" @submit.prevent="signIn">
          <div class="login-field">
            <label class="login-field__label" for="login-email">Email</label>
            <InputText
              id="login-email"
              v-model="email"
              type="email"
              autocomplete="email"
              class="login-field__input"
              fluid
            />
          </div>
          <div class="login-field">
            <label class="login-field__label" for="login-password">Password</label>
            <Password
              id="login-password"
              v-model="password"
              :feedback="false"
              toggle-mask
              autocomplete="current-password"
              class="login-field__input"
              fluid
            />
          </div>
          <div class="login-form__actions">
            <Button type="submit" label="Sign in" fluid />
          </div>
          <p class="login-form__footer">
            <router-link to="/forgot-password" class="login-form__link">
              Forgot password?
            </router-link>
          </p>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

const email = ref("user@example.com");
const password = ref("");

function signIn(): void {
  // stub — wire auth API later
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--size-5);
  background: var(--surface-1);
}

.login-card {
  width: min(100%, 28rem);
  background: var(--surface-2);
}

.login-card :deep(.p-card-title) {
  font-size: var(--font-size-5);
  color: var(--text-1);
}

.login-card :deep(.p-card-subtitle) {
  color: var(--text-2);
  font-size: var(--font-size-2);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
}

.login-field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.login-field__label {
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-5);
  color: var(--text-2);
}

.login-field__input {
  width: 100%;
}

.login-form__actions {
  margin-top: var(--size-2);
}

.login-form__footer {
  margin: 0;
  text-align: center;
}

.login-form__link {
  font-size: var(--font-size-1);
  color: var(--text-2);
  text-decoration: none;
}

.login-form__link:hover {
  color: var(--text-1);
  text-decoration: underline;
}
</style>
