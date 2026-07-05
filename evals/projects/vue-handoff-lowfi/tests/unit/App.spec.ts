import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createWebHistory } from "vue-router";
import App from "@/App.vue";

describe("App", () => {
  it("renders shell with router", async () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [{ path: "/", component: { template: "<div class='route-stub' />" } }],
    });
    const wrapper = mount(App, { global: { plugins: [router] } });
    await router.isReady();
    expect(wrapper.find("main").exists()).toBe(true);
    expect(wrapper.find(".router-view-stub, .route-stub").exists()).toBe(true);
  });
});
