import { ref } from "vue";
import type { User } from "@/types/api";

export function useUsers() {
  const users = ref<User[]>([]);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  async function fetch(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const res = await globalThis.fetch("/api/users");
      if (!res.ok) {
        throw new Error(`Failed to fetch users: ${res.status}`);
      }
      users.value = (await res.json()) as User[];
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return { users, loading, error, fetch, fetchUsers: fetch };
}
