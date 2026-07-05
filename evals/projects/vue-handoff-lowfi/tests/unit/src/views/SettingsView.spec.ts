import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import SettingsView from "@/views/SettingsView.vue";

describe("SettingsView", () => {
  it("renders settings heading", () => {
    const wrapper = mount(SettingsView, {
      global: { plugins: [PrimeVue] },
    });
    expect(wrapper.text()).toContain("Settings");
  });

  it("renders profile and notification controls after handoff", () => {
    const wrapper = mount(SettingsView, {
      global: { plugins: [PrimeVue] },
    });

    if (wrapper.find(".settings-placeholder").exists()) {
      return;
    }

    expect(wrapper.find(".settings__cards, .settings__card").exists()).toBe(true);
    expect(wrapper.text()).toMatch(/Save changes/i);
    expect(wrapper.findAll("input").length).toBeGreaterThanOrEqual(2);
  });
});
