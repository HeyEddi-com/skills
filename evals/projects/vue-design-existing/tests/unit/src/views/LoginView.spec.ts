import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import LoginView from "@/views/LoginView.vue";

describe("LoginView", () => {
  it("renders sign in", () => {
    const wrapper = mount(LoginView);
    expect(wrapper.text()).toContain("Sign in");
  });
});
