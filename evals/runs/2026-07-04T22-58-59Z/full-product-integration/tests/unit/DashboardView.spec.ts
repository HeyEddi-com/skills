import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { definePreset } from "@primeuix/themes";
import Aura from "@primevue/themes/aura";
import DashboardView from "@/views/dashboard/dashboard-view.vue";
import { DEMO_USERS } from "@/data/demoUsers";
import { createViewRouter } from "../helpers/createViewRouter";

const HeyEddiAura = definePreset(Aura, {
  semantic: {
    primary: {
      500: "{indigo.500}",
      600: "{indigo.600}",
    },
  },
});

function mountDashboard() {
  const router = createViewRouter("/dashboard", DashboardView);
  return mount(DashboardView, {
    global: {
      plugins: [
        router,
        [PrimeVue, { theme: { preset: HeyEddiAura, options: { darkModeSelector: "system" } } }],
      ],
      stubs: {
        RouterLink: { template: "<a><slot /></a>", props: ["to"] },
      },
    },
  });
}

describe("DashboardView", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders team roster heading and refresh action", async () => {
    vi.mocked(fetch).mockRejectedValue(new Error("Network error"));

    const wrapper = mountDashboard();
    await flushPromises();

    expect(wrapper.text()).toContain("Team roster");
    expect(wrapper.text()).toContain("Refresh");
  });

  it("shows demo roster rows when API is unavailable", async () => {
    vi.mocked(fetch).mockRejectedValue(new Error("Failed to fetch"));

    const wrapper = mountDashboard();
    await flushPromises();

    expect(wrapper.text()).toContain("API unavailable");
    for (const user of DEMO_USERS) {
      expect(wrapper.text()).toContain(user.email);
    }
    expect(wrapper.text()).toContain("Demo data");
  });

  it("shows live API users when fetch succeeds", async () => {
    const roster = [{ id: "live-1", email: "live@team.co" }];
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(roster),
    } as Response);

    const wrapper = mountDashboard();
    await flushPromises();

    expect(wrapper.text()).toContain("live@team.co");
    expect(wrapper.text()).toContain("Live API");
    expect(wrapper.text()).not.toContain("API unavailable");
  });

  it("shows empty state when API returns no users", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    } as Response);

    const wrapper = mountDashboard();
    await flushPromises();

    expect(wrapper.text()).toContain("No team members yet");
  });

  it("re-fetches on refresh click", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([{ id: "1", email: "a@team.co" }]),
    } as Response);

    const wrapper = mountDashboard();
    await flushPromises();

    vi.mocked(fetch).mockClear();
    await wrapper.find("button").trigger("click");
    await flushPromises();

    expect(fetch).toHaveBeenCalledWith("/api/users", {
      headers: { "Content-Type": "application/json" },
    });
  });
});
