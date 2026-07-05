<template>
  <div class="card"><span>{{ name }}</span></div>
</template>

<script setup>
defineProps({ name: { type: String, default: 'User' } })
</script>

<style scoped>
.card { padding: var(--size-2); color: #333; }
</style>
