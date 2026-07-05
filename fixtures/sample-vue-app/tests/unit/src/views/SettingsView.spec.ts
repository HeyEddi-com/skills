import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import SettingsView from "../../../../src/views/SettingsView";

describe("SettingsView", () => {
  it("renders", () => {
    const wrapper = mount(SettingsView);
    expect(wrapper.exists()).toBe(true);
  });
});
