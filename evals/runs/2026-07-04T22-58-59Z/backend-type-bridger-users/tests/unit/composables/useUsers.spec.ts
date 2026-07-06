import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { useUsers } from "@/composables/useUsers";

describe("useUsers", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => [{ id: "1", email: "demo@example.com" }],
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetchUsers loads users from /api/users", async () => {
    const { users, loading, error, fetchUsers } = useUsers();

    expect(loading.value).toBe(false);
    await fetchUsers();

    expect(fetch).toHaveBeenCalledWith("/api/users");
    expect(users.value).toEqual([{ id: "1", email: "demo@example.com" }]);
    expect(error.value).toBeNull();
    expect(loading.value).toBe(false);
  });
});
