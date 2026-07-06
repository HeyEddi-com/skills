import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { useUsers } from "@/composables/useUsers";

describe("useUsers", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetchUsers loads users from GET /api/users", async () => {
    const roster = [{ id: "1", email: "demo@example.com" }];
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(roster),
    } as Response);

    const { users, loading, error, fetchUsers } = useUsers();
    expect(loading.value).toBe(false);

    const pending = fetchUsers();
    expect(loading.value).toBe(true);

    await pending;

    expect(loading.value).toBe(false);
    expect(error.value).toBeNull();
    expect(users.value).toEqual(roster);
    expect(fetch).toHaveBeenCalledWith("/api/users", {
      headers: { "Content-Type": "application/json" },
    });
  });

  it("fetchUsers sets error ref on failure", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      text: () => Promise.resolve("Not found"),
    } as Response);

    const { users, error, fetchUsers } = useUsers();

    await expect(fetchUsers()).rejects.toThrow("Not found");
    expect(error.value).toBe("Not found");
    expect(users.value).toEqual([]);
  });
});
