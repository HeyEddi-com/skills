import { describe, it, expect } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { definePreset } from "@primeuix/themes";
import Aura from "@primevue/themes/aura";
import SettingsView from "@/views/SettingsView.vue";
import { createViewRouter } from "../helpers/createViewRouter";

const HeyEddiAura = definePreset(Aura, {
  semantic: {
    primary: {
      500: "{indigo.500}",
      600: "{indigo.600}",
    },
  },
});

function mountSettings() {
  const router = createViewRouter("/settings", SettingsView);
  return mount(SettingsView, {
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

describe("SettingsView", () => {
  it("renders profile and notification cards with save action", async () => {
    const wrapper = mountSettings();
    await flushPromises();

    expect(wrapper.text()).toContain("Settings");
    expect(wrapper.text()).toContain("Profile");
    expect(wrapper.text()).toContain("Notifications");
    expect(wrapper.find("#display-name").exists()).toBe(true);
    expect(wrapper.find("#email").exists()).toBe(true);
    expect(wrapper.text()).toContain("Save changes");
  });

  it("shows saved confirmation after save click", async () => {
    const wrapper = mountSettings();
    await flushPromises();

    await wrapper.find(".settings__save button").trigger("click");
    await flushPromises();

    expect(wrapper.text()).toContain("Your settings were saved.");
  });
});
