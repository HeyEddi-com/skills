<template>
  <div class="login-page">
    <Card class="login-card">
      <template #title>
        <h1 class="login-card__title">SecureVault</h1>
      </template>
      <template #subtitle>
        <p class="login-card__subtitle">Sign in to your team vault</p>
      </template>
      <template #content>
        <form class="login-form" novalidate @submit.prevent="handleSubmit">
          <Message
            v-if="authError"
            severity="error"
            :closable="false"
            class="login-form__banner"
            role="alert"
          >
            {{ authError }}
          </Message>

          <div class="login-form__field">
            <label class="login-form__label" for="login-email">Email</label>
            <InputText
              id="login-email"
              v-model="email"
              type="email"
              autocomplete="email"
              inputmode="email"
              :invalid="Boolean(fieldErrors.email)"
              :disabled="isLoading"
              aria-describedby="login-email-error"
              class="login-form__input"
              fluid
            />
            <small
              v-if="fieldErrors.email"
              id="login-email-error"
              class="login-form__error"
              role="alert"
            >
              {{ fieldErrors.email }}
            </small>
          </div>

          <div class="login-form__field">
            <label class="login-form__label" for="login-password">Password</label>
            <Password
              id="login-password"
              v-model="password"
              :feedback="false"
              toggle-mask
              :invalid="Boolean(fieldErrors.password)"
              :disabled="isLoading"
              autocomplete="current-password"
              aria-describedby="login-password-error"
              input-class="login-form__input"
              fluid
            />
            <small
              v-if="fieldErrors.password"
              id="login-password-error"
              class="login-form__error"
              role="alert"
            >
              {{ fieldErrors.password }}
            </small>
          </div>

          <div class="login-form__utility">
            <div class="login-form__remember">
              <Checkbox
                v-model="rememberMe"
                input-id="login-remember"
                :binary="true"
                :disabled="isLoading"
              />
              <label for="login-remember" class="login-form__remember-label">
                Remember me on this device
              </label>
            </div>
            <RouterLink to="/forgot-password" class="login-form__link">
              Forgot password?
            </RouterLink>
          </div>

          <Button
            type="submit"
            label="Sign in"
            class="login-form__submit"
            :loading="isLoading"
            fluid
          />
        </form>
      </template>
      <template #footer>
        <p class="login-card__footer">
          Don't have an account?
          <RouterLink to="/signup" class="login-form__link login-form__link--emphasis">
            Sign up
          </RouterLink>
        </p>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";

const REMEMBER_KEY = "sv_remember_me";
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const email = ref("");
const password = ref("");
const rememberMe = ref(false);
const isLoading = ref(false);
const authError = ref("");
const fieldErrors = reactive<{ email: string; password: string }>({
  email: "",
  password: "",
});

onMounted(() => {
  rememberMe.value = localStorage.getItem(REMEMBER_KEY) === "true";
});

function clearFieldErrors() {
  fieldErrors.email = "";
  fieldErrors.password = "";
}

function validate(): boolean {
  clearFieldErrors();
  let valid = true;

  const trimmedEmail = email.value.trim();
  if (!trimmedEmail) {
    fieldErrors.email = "Enter a valid email address";
    valid = false;
  } else if (!EMAIL_PATTERN.test(trimmedEmail)) {
    fieldErrors.email = "Enter a valid email address";
    valid = false;
  }

  if (!password.value) {
    fieldErrors.password = "Password is required";
    valid = false;
  }

  return valid;
}

async function handleSubmit() {
  authError.value = "";
  if (!validate()) return;

  isLoading.value = true;
  localStorage.setItem(REMEMBER_KEY, String(rememberMe.value));

  try {
    await new Promise((resolve) => setTimeout(resolve, 800));
    authError.value = "Invalid email or password. Please try again.";
  } finally {
    isLoading.value = false;
  }
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
  width: 100%;
  max-width: 24rem;
  border: 1px solid var(--border-1);
  border-radius: var(--radius-3);
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.04);
  background: var(--surface-2);
}

.login-card :deep(.p-card-body) {
  padding: var(--size-5);
}

.login-card :deep(.p-card-title) {
  margin-bottom: var(--size-2);
}

.login-card :deep(.p-card-subtitle) {
  margin-bottom: 0;
}

.login-card__title {
  margin: 0;
  font-size: var(--font-size-5);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-1);
}

.login-card__subtitle {
  margin: 0;
  font-size: var(--font-size-2);
  color: var(--text-2);
  line-height: var(--font-lineheight-3);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
  margin-top: var(--size-5);
}

.login-form__banner {
  margin: 0;
}

.login-form__field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.login-form__label {
  font-size: var(--font-size-1);
  font-weight: 600;
  color: var(--text-1);
}

.login-form__error {
  color: var(--red-9);
  font-size: var(--font-size-0);
}

.login-form__utility {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--size-3);
  margin-top: var(--size-1);
}

.login-form__remember {
  display: flex;
  align-items: center;
  gap: var(--size-2);
}

.login-form__remember-label {
  font-size: var(--font-size-1);
  color: var(--text-2);
  cursor: pointer;
  user-select: none;
}

.login-form__link {
  font-size: var(--font-size-1);
  color: var(--indigo-9);
  text-decoration: none;
}

.login-form__link:hover {
  text-decoration: underline;
}

.login-form__link:focus-visible {
  outline: 2px solid var(--indigo-7);
  outline-offset: 2px;
  border-radius: var(--radius-1);
}

.login-form__link--emphasis {
  font-weight: 600;
}

.login-form__submit {
  margin-top: var(--size-2);
}

.login-card__footer {
  margin: 0;
  text-align: center;
  font-size: var(--font-size-1);
  color: var(--text-2);
}

@media (prefers-reduced-motion: reduce) {
  .login-form__link {
    transition: none;
  }
}
</style>
