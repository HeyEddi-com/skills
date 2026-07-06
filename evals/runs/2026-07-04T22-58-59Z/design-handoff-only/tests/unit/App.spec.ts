import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createMemoryHistory } from "vue-router";
import PrimeVue from "primevue/config";
import App from "@/App.vue";

describe("App", () => {
  it("renders shell with router", async () => {
    const router = createRouter({
      history: createMemoryHistory("/settings"),
      routes: [
        { path: "/", redirect: "/settings" },
        { path: "/settings", component: { template: "<div class='route-stub' />" } },
        { path: "/dashboard", redirect: "/settings" },
      ],
    });
    const wrapper = mount(App, {
      global: {
        plugins: [router, PrimeVue],
        stubs: {
          RouterView: false,
        },
      },
    });
    await router.isReady();
    expect(wrapper.find(".app-shell").exists()).toBe(true);
    expect(wrapper.find(".route-stub").exists()).toBe(true);
  });
});
