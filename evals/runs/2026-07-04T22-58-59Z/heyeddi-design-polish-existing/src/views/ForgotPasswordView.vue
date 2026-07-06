<template>
  <div class="forgot-page">
    <Card class="forgot-card">
      <template #title>Reset password</template>
      <template #subtitle>Password reset is not wired yet — placeholder route for login affordance.</template>
      <template #content>
        <router-link to="/login" class="forgot-page__link">Back to sign in</router-link>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from "primevue/card";
</script>

<style scoped>
.forgot-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--size-5);
  background: var(--surface-1);
}

.forgot-card {
  width: min(100%, 28rem);
  background: var(--surface-2);
}

.forgot-page__link {
  color: var(--text-2);
  font-size: var(--font-size-2);
}
</style>
