<template>
  <div class="login">
    <div class="login__intro">
      <h1 class="login__title">{{ t.login.title }}</h1>
      <p class="login__subtitle">{{ t.login.subtitle }}</p>
    </div>

    <Card class="login__card">
      <template #content>
        <Message v-if="errorMessage" severity="error" :closable="false" class="login__error">
          {{ errorMessage }}
        </Message>

        <form class="login__form" @submit.prevent="handleSubmit">
          <div class="login__field">
            <label for="email">{{ t.login.emailLabel }}</label>
            <InputText
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              :placeholder="t.login.emailPlaceholder"
              :invalid="showFieldErrors && !email.trim()"
              aria-describedby="email-error"
            />
            <small v-if="showFieldErrors && !email.trim()" id="email-error" class="login__hint">
              {{ t.login.errorRequired }}
            </small>
          </div>

          <div class="login__field">
            <label for="password">{{ t.login.passwordLabel }}</label>
            <Password
              id="password"
              v-model="password"
              :feedback="false"
              toggle-mask
              autocomplete="current-password"
              :placeholder="t.login.passwordPlaceholder"
              :invalid="showFieldErrors && !password"
              aria-describedby="password-error"
              input-class="w-full"
            />
            <small v-if="showFieldErrors && !password" id="password-error" class="login__hint">
              {{ t.login.errorRequired }}
            </small>
          </div>

          <div class="login__row">
            <div class="login__remember">
              <Checkbox v-model="rememberMe" input-id="remember" binary />
              <label for="remember">{{ t.login.rememberMe }}</label>
            </div>
            <a class="login__forgot" href="#" @click.prevent>{{ t.login.forgotPassword }}</a>
          </div>

          <Button
            type="submit"
            :label="t.login.submit"
            class="login__submit"
            :loading="submitting"
          />
        </form>
      </template>
    </Card>

    <p class="login__footer">
      {{ t.login.newTeam }}
      <RouterLink to="/">{{ t.login.startTrial }}</RouterLink>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import Card from "primevue/card";
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";
import { useLocale } from "@/composables/useLocale";

const router = useRouter();
const { t } = useLocale();

const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const showFieldErrors = ref(false);
const errorMessage = ref("");
const submitting = ref(false);

async function handleSubmit() {
  showFieldErrors.value = true;
  errorMessage.value = "";

  if (!email.value.trim() || !password.value) {
    errorMessage.value = t.value.login.errorRequired;
    return;
  }

  submitting.value = true;
  try {
    await router.push("/dashboard");
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.login {
  max-width: var(--content-narrow);
  margin: 0 auto;
  padding: var(--size-7) var(--size-4) var(--size-8);
}

.login__intro {
  margin-bottom: var(--size-5);
  text-align: center;
}

.login__title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-7);
}

.login__subtitle {
  margin: 0;
  color: var(--text-2);
}

.login__card {
  border: 1px solid var(--border-1);
  border-radius: var(--radius-card);
  overflow: hidden;
}

.login__card :deep(.p-card-body) {
  padding: var(--size-5);
}

.login__error {
  margin-bottom: var(--size-4);
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
}

.login__field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.login__field label {
  font-weight: var(--font-weight-6);
  font-size: var(--font-size-1);
}

.login__field :deep(.p-inputtext),
.login__field :deep(.p-password),
.login__field :deep(.p-password-input) {
  width: 100%;
}

.login__hint {
  color: var(--red-7);
}

.login__row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--size-3);
}

.login__remember {
  display: flex;
  align-items: center;
  gap: var(--size-2);
}

.login__remember label {
  font-size: var(--font-size-1);
  color: var(--text-2);
}

.login__forgot {
  color: var(--brand);
  font-size: var(--font-size-1);
  text-decoration: none;
}

.login__forgot:hover,
.login__forgot:focus-visible {
  text-decoration: underline;
}

.login__submit {
  width: 100%;
  margin-top: var(--size-2);
}

.login__footer {
  margin-top: var(--size-5);
  text-align: center;
  color: var(--text-2);
  font-size: var(--font-size-1);
}

.login__footer a {
  color: var(--brand);
  font-weight: var(--font-weight-6);
}
</style>
