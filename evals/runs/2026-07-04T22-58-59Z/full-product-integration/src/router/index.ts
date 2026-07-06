import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/login/login-view.vue";
import DashboardView from "@/views/dashboard/dashboard-view.vue";
import SettingsView from "@/views/SettingsView.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { layout: "brand", showFeaturesLink: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { layout: "brand" },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { layout: "app" },
  },
  {
    path: "/settings",
    name: "settings",
    component: SettingsView,
    meta: { layout: "app" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
