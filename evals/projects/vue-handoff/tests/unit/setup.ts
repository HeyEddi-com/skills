import { config } from "@vue/test-utils";

config.global.stubs = {
  RouterView: { template: "<div class='router-view-stub' />" },
  RouterLink: { template: "<a><slot /></a>", props: ["to"] },
};
