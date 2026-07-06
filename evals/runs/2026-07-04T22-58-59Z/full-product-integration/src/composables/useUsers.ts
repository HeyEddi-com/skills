import { ref } from "vue";
import type { User } from "@/types/api";
import { useApi } from "@/composables/useApi";

/**
 * Team roster from `GET /api/users`.
 *
 * OpenAPI assumes the 200 response is a bare `User[]` (not paginated or wrapped).
 * Required fields per schema: `id`, `email` (both strings).
 */
export function useUsers() {
  const users = ref<User[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const { fetchApi } = useApi();

  async function fetchUsers(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      users.value = await fetchApi<User[]>("/users");
    } catch (e) {
      error.value = e instanceof Error ? e.message : String(e);
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return { users, loading, error, fetchUsers };
}
