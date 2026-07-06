<template>
  <div class="auth-placeholder">
    <Card class="auth-placeholder__card">
      <template #title>
        <h1 class="auth-placeholder__title">Reset your password</h1>
      </template>
      <template #subtitle>
        <p class="auth-placeholder__subtitle">
          Password reset is not wired yet. Your team admin can help you regain access.
        </p>
      </template>
      <template #content>
        <RouterLink to="/login" class="auth-placeholder__link">
          ← Back to sign in
        </RouterLink>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from "primevue/card";
</script>

<style scoped>
.auth-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--size-5);
  background: var(--surface-1);
}

.auth-placeholder__card {
  width: 100%;
  max-width: 24rem;
  border: 1px solid var(--border-1);
  border-radius: var(--radius-3);
  background: var(--surface-2);
}

.auth-placeholder__card :deep(.p-card-body) {
  padding: var(--size-5);
}

.auth-placeholder__title {
  margin: 0;
  font-size: var(--font-size-4);
  font-weight: 700;
  color: var(--text-1);
}

.auth-placeholder__subtitle {
  margin: 0;
  font-size: var(--font-size-2);
  color: var(--text-2);
  line-height: var(--font-lineheight-3);
}

.auth-placeholder__link {
  display: inline-block;
  margin-top: var(--size-4);
  font-size: var(--font-size-1);
  color: var(--indigo-9);
  text-decoration: none;
}

.auth-placeholder__link:hover {
  text-decoration: underline;
}

.auth-placeholder__link:focus-visible {
  outline: 2px solid var(--indigo-7);
  outline-offset: 2px;
  border-radius: var(--radius-1);
}
</style>
