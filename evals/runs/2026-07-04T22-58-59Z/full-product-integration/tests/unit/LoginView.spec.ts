import { describe, it, expect, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { definePreset } from "@primeuix/themes";
import Aura from "@primevue/themes/aura";
import LoginView from "@/views/login/login-view.vue";
import { createViewRouter } from "../helpers/createViewRouter";

const HeyEddiAura = definePreset(Aura, {
  semantic: {
    primary: {
      500: "{indigo.500}",
      600: "{indigo.600}",
    },
  },
});

function mountLogin() {
  const router = createViewRouter("/login", LoginView);
  return mount(LoginView, {
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

describe("LoginView", () => {
  it("renders sign-in form fields and submit button", async () => {
    const wrapper = mountLogin();
    await flushPromises();

    expect(wrapper.find("#email").exists()).toBe(true);
    expect(wrapper.find("#password").exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
    expect(wrapper.text()).toContain("Sign in to TaskFlow");
  });

  it("shows validation message when submitting empty form", async () => {
    const wrapper = mountLogin();
    await flushPromises();

    await wrapper.find("form").trigger("submit.prevent");
    await flushPromises();

    expect(wrapper.text()).toContain("Enter your email and password");
  });

  it("navigates to dashboard after valid submit", async () => {
    const router = createViewRouter("/login", LoginView);
    const push = vi.spyOn(router, "push");

    const wrapper = mount(LoginView, {
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
    await flushPromises();

    await wrapper.find("#email").setValue("sam@team.co");
    await wrapper.find("#password input").setValue("secret");
    await wrapper.find("form").trigger("submit.prevent");
    await flushPromises();

    expect(push).toHaveBeenCalledWith("/dashboard");
  });
});
