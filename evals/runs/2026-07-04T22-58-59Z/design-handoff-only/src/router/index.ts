import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/settings" },
    {
      path: "/settings",
      name: "settings",
      component: () => import("@/views/SettingsView.vue"),
    },
    { path: "/dashboard", name: "dashboard", redirect: "/settings" },
    { path: "/documents", name: "documents", redirect: "/settings" },
    { path: "/team", name: "team", redirect: "/settings" },
  ],
});

export default router;
