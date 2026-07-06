import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import { createRouter, createMemoryHistory } from "vue-router";
import App from "@/App.vue";

const stubRoute = { template: "<div class='route-stub' />" };

describe("App", () => {
  it("renders shell with router", async () => {
    const router = createRouter({
      history: createMemoryHistory("/"),
      routes: [
        { path: "/", component: stubRoute },
        { path: "/login", component: stubRoute },
        { path: "/dashboard", component: stubRoute },
        { path: "/settings", component: stubRoute },
      ],
    });
    const wrapper = mount(App, { global: { plugins: [router] } });
    await router.isReady();
    expect(wrapper.find("main").exists()).toBe(true);
    expect(wrapper.find(".route-stub").exists()).toBe(true);
  });
});
