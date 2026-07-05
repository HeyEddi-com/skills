<template>
  <div style="padding: 8px; max-width: 280px">
    <h1 style="font-size: 14px; color: #999">Login</h1>
    <label style="font-size: 10px; color: #aaa">Email</label>
    <input
      v-model="email"
      type="email"
      style="display: block; width: 100%; background: #000; color: #fff; border: none; padding: 4px"
    />
    <label style="font-size: 10px; color: #aaa">Password</label>
    <input
      v-model="password"
      type="password"
      style="display: block; width: 100%; background: #000; color: #fff; border: none; padding: 4px"
    />
    <button
      type="button"
      style="margin-top: 8px; width: 100%; background: #3dd68c; border: none; padding: 12px"
      @click="signIn"
    >
      Sign in
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const email = ref("user@example.com");
const password = ref("");

function signIn(): void {
  // stub
}
</script>
