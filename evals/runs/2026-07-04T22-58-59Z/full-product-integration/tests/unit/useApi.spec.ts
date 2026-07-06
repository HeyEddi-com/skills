import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { useApi } from "@/composables/useApi";

describe("useApi", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fetchApi calls /api-prefixed path and returns JSON", async () => {
    const payload = [{ id: "1", email: "demo@example.com" }];
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(payload),
    } as Response);

    const { fetchApi } = useApi();
    const result = await fetchApi<typeof payload>("/users");

    expect(fetch).toHaveBeenCalledWith("/api/users", {
      headers: { "Content-Type": "application/json" },
    });
    expect(result).toEqual(payload);
  });

  it("fetchApi throws when response is not ok", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      text: () => Promise.resolve("Server error"),
    } as Response);

    const { fetchApi } = useApi();
    await expect(fetchApi("/users")).rejects.toThrow("Server error");
  });
});
