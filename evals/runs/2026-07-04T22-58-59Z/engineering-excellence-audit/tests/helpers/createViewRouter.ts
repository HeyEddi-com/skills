import { createRouter, createMemoryHistory, type RouteRecordRaw } from "vue-router";
import type { Component } from "vue";

const stubRoute = { template: "<div />" };

const STUB_PATHS = ["/", "/login", "/dashboard", "/settings"] as const;

/**
 * Isolated view tests must use memory history — createWebHistory() resolves the
 * browser URL (often "/") and emits Vue Router warnings when routes are missing.
 */
export function createViewRouter(path: string, component: Component) {
  const routes: RouteRecordRaw[] = STUB_PATHS.filter((p) => p !== path).map((p) => ({
    path: p,
    component: stubRoute,
  }));
  routes.push({ path, component });
  return createRouter({
    history: createMemoryHistory(path),
    routes,
  });
}
