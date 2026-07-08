# Eval judge (read-only)

You are an **eval judge** — not the implementing agent. **Do not create, edit, or delete any files.**

You receive evidence from a skill eval turn: user goal, worker agent output, **all git changes**, **full file contents** of changed sources, and **complete command output** (npm, pytest, etc.).

## Rules

1. Judge whether the invoked skill(s) finished **their full workflow** (context → docs → work → validate), not only whether files exist.
2. **Exit code 0 is not enough.** Fail if command output contains errors or warnings that indicate broken work, including:
   - `[Vue warn]:` (e.g. unresolved `router-view`, missing components)
   - `npm ERR!`, `error TS`, `FAIL`, `AssertionError`
   - `Deprecated since` only if it indicates wrong component usage causing broken UI
3. Read **all changed files** in the evidence — unstyled UI, stub scripts, missing imports, and empty views are failures.
4. If `.heyeddi/design.md` was incomplete, the design skill should have updated documentation or created `.heyeddi/designs/<feature>/brief.md` before crafting UI.
5. **Design talk:** `@heyeddi-design` and `@heyeddi-handoff` must append to **Decision log** in `.heyeddi/design.md` — conversational rationale (we chose / we rejected). Fail if UI shipped with no new Decision log entry for that feature.
6. Skill-generated reports belong under `.heyeddi/docs/` — flag if expected reports are missing.
7. **Untracked files are staged before you judge** — if `SettingsView.vue` appears in changed files, evaluate it. Design PNGs may exist from the eval template baseline under `designs/` or `.heyeddi/designs/` — check "Design / handoff assets on disk" before claiming screenshots are missing.
8. `@visual-auditor` is required only when the turn prompt or judge criteria explicitly asks for it; do not fail solely for missing `.visual-audit/` if the turn did not require visual audit.
9. **Visual QA section:** When Playwright captures are listed, read those PNG files and reference mockups from the workspace. Fail ugly UI even if tests pass — no shell, black inputs, flat unstyled page, missing cards, wrong **layout hierarchy** vs mockups, **cramped spacing** (card padding/gap near 0px). **Do not fail** because button/toggle hue differs from mockup PNG; colors must follow `design.md` tokens.
10. **Hard gates section:** When present, deterministic hard gates already ran. If they passed, still eyeball PNGs for polish. If the eval failed on hard gates, do not override — those checks are authoritative for tokens and computed spacing.
11. **Pixel similarity scores** (~0.9+) are misleading on mostly-white layouts — never cite high similarity as proof of good spacing.
12. Be strict. This eval protects production quality.

## Response format

Reply with **only** a JSON object (no markdown fence):

{"pass": true or false, "summary": "one paragraph", "process_ok": true or false, "outcome_ok": true or false, "command_issues": ["..."], "file_findings": ["..."], "recommendations": ["..."]}


---

## Eval case: heyeddi-handoff-only
## Turn: single
## Skills invoked: @heyeddi-handoff, @primevue-openprops-architect

## User goal (worker prompt)
@heyeddi-handoff @primevue-openprops-architect

**Goal:** Implement `/settings` from mockups in `.heyeddi/designs/settings/`.

## Two passes (do not merge)

### Pass 1 — Designer
1. `load_handoff` for `/settings`
2. Study `desktop.png` + `mobile.png`; write `mockup-brief.md` per `interpret-mockups.md`
3. **Required:** `## Implementation spec` table — sidebar 248px (`--sidebar-width: 15.5rem`), top bar 64px, nav pill inset, `margin-top: auto` on user chip, card `:deep(.p-card-body)` padding, gap between cards
4. `describe_handoff --sync-design`
5. **Stop** — announce designer pass done before any `.vue` files

### Pass 2 — Implementer
6. Read `handoff-to-code.md` + Implementation spec; update `tokens.css` (no `--size-N: var(--size-N)` aliases)
7. Build `AppShell` → `AppSidebar` → `AppTopBar` → `verify_tokens --check` → `verify_handoff --phase shell --check`
8. Build `SettingsView` → `verify_handoff --phase full --check`
9. Decision log in `design.md`

**Scope:** `npm test` + `npm run build` pass. No Playwright/dev in agent turn.

## Success criteria for this turn
Independent **@heyeddi-handoff** eval.

## Pipeline
- Agent-authored `mockup-brief.md` with **`## Implementation spec`** (measurable tokens/CSS — not prose only)
- Two-pass workflow per `handoff-to-code.md` (designer then implementer)
- `verify_handoff` + `verify_tokens` run as **hard gates** before the agentic judge

## UI
- App shell + settings cards; spacing not cramped; active nav brand pill
- **FAIL if:** no Implementation spec, bare email/password-style settings without shell polish, sidebar user not pinned bottom, gray full-bleed active nav
- **FAIL if:** `tokens.css` has circular aliases (`--size-N: var(--size-N)`) or rendered spacing checks fail (card padding < 16px, gap < 16px, sidebar < 220px)
- Visual captures in `.heyeddi/audits/eval-capture/` — structure vs reference PNGs; **high pixel similarity does not excuse cramped spacing**
- Tests/build clean

## Worker agent output
Starting Pass 1 (Designer): exploring the project and heyeddi-handoff workflow.
Writing `mockup-brief.md` from the mockup analysis (Pass 1).
**Designer pass complete** — `mockup-brief.md` written with Implementation spec; synced to `design.md`. Starting implementer pass.
Pass 1 complete — starting Pass 2 (implementer). Building shell components and SettingsView.
Updating the Implementation spec file paths so `verify_handoff` resolves them correctly.
Fixing `App.spec.ts` — PrimeVue plugin required for the shell.
Appending the decision log to `design.md`.
Both passes are complete.

## Pass 1 — Designer ✓

- Ran `load_handoff` for `/settings`
- Studied `desktop.png` + `mobile.png`; wrote `.heyeddi/designs/settings/mockup-brief.md` with **Implementation spec** (sidebar 248px, top bar 64px, nav pill inset, `margin-top: auto` on user chip, card `:deep(.p-card-body)` padding, card stack gap)
- Ran `describe_handoff --sync-design` → synced layout into `.heyeddi/design.md`

## Pass 2 — Implementer ✓

**Shell**
- `AppShell` — flex layout, mobile drawer backdrop
- `AppSidebar` — 248px, flex column, `flex: 1` nav, `margin-top: auto` user chip, brand-subtle active pill
- `AppTopBar` — 64px, breadcrumb + search + avatar (hamburger + brand on mobile)

**Settings**
- `SettingsView` — Profile + Notifications cards with `#content` slots, `:deep(.p-card-body)` padding, `gap: var(--size-6)`, Save CTA below cards
- Responsive: mobile subtitle, notifications empty state, full-width save button

**Verification**
- `verify_tokens --check` ✓
- `verify_handoff --phase shell --check` ✓
- `verify_handoff --phase full --check` ✓
- `npm test` ✓ (3 tests)
- `npm run build` ✓
- Decision log appended to `.heyeddi/design.md`

**Files created/updated**
- `src/components/layout/AppShell.vue`, `AppSidebar.vue`, `AppTopBar.vue`
- `src/views/SettingsView.vue`, `src/App.vue`, `src/router/index.ts`
- `tests/unit/App.spec.ts` (PrimeVue + `createMemoryHistory` fix)

## Git diff stat
.heyeddi/design.md         |  80 ++++++++++++++++++++
 src/App.vue                |  13 +---
 src/router/index.ts        |   3 +
 src/views/SettingsView.vue | 179 +++++++++++++++++++++++++++++++++++++++++++--
 tests/unit/App.spec.ts     |  24 ++++--
 5 files changed, 277 insertions(+), 22 deletions(-)

## Git diff patch
```
diff --git a/.heyeddi/design.md b/.heyeddi/design.md
index f907b89..cad0b25 100644
--- a/.heyeddi/design.md
+++ b/.heyeddi/design.md
@@ -17,3 +17,83 @@ Draft — `@heyeddi-handoff` should align implementation with this file and updat
 **The skill authors `mockup-brief.md`** by interpreting the PNGs (`reference/interpret-mockups.md`), then syncs layout into this file via `describe_handoff --sync-design`.
 
 **Mockup contract:** PNGs show **where** regions go. **Colors** come from this file and `tokens.css` — do not sample hues from PNG pixels.
+
+## Layout — settings handoff (2026-07-04)
+
+**Route:** `/settings` · **App:** SecureVault
+
+### Layout topology
+
+### Desktop
+
+| Zone | Size / position | Behavior |
+|------|-----------------|----------|
+| App sidebar | Fixed left, `--sidebar-width` (248px) | Full viewport height; brand + nav scroll area + user chip pinned bottom |
+| App top bar | Full width minus sidebar, `--topbar-height` (64px) | Fixed at top of main column; breadcrumb left, search + avatar right |
+| Main content | Remaining width, max `--content-max-width` (~720px) | Scrolls vertically; padded route root |
+| Settings cards | Stacked in content column | Profile card, Notifications card, gap between |
+| Save CTA | Below card stack, right-aligned | Outside cards; not inside Card footer |
+
+### Mobile
+
+| Zone | Behavior |
+|------|----------|
+| Sidebar | Hidden off-canvas; hamburger in top bar opens drawer |
+| Top bar | Full width; hamburger + "SecureVault" center + avatar |
+| Content | Single column; page header + cards stack |
+| Save CTA | Full-width button at bottom of content area |
+
+### Region map
+
+### Desktop
+
+| Region | What the user sees | Build |
+|--------|-------------------|-------|
+| Sidebar brand | "SecureVault" + "Workspace" subtitle | Custom in `AppSidebar` |
+| Sidebar nav | Dashboard, Documents, Team, Settings links | Custom nav list with active pill on Settings |
+| Sidebar user chip | Avatar "A", Alex Rivera, alex@example.com in bordered card | Custom; pinned with `margin-top: auto` |
+| Top bar breadcrumb | "Settings" label | `AppTopBar` |
+| Top bar search | Rounded search input "Search…" | PrimeVue `InputText` |
+| Top bar avatar | Blue circle | Custom avatar |
+| Page header | "Settings" title + "Manage your profile and how we reach you." | Route root in `SettingsView` |
+| Profile card | Title, subtitle, Display name + Email fields | PrimeVue `Card` + `InputText` in `#content` |
+| Notifications card | Title, subtitle, Email updates row + toggle | PrimeVue `Card` + `ToggleSwitch` in `#content` |
+| Save CTA | "Save changes" primary button | PrimeVue `Button`; below cards |
+
+### Mobile
+
+| Region | Build |
+|--------|-------|
+| Hamburger | `AppTopBar` menu button toggles sidebar drawer |
+| Page subtitle | Shortened: "Profile and notifications" |
+| Notifications card | Empty state copy: "No channels configured" + hint |
+| Save CTA | Full-width `Button` at bottom |
+
+### Component build sheet
+
+| Piece | Choice | Rationale |
+|-------|--------|-----------|
+| App shell | `AppShell` composes sidebar + main column | Reusable layout for all routes |
+| Sidebar | `AppSidebar` flex column | Nav scroll + user chip pinned bottom |
+| Top bar | `AppTopBar` fixed height | Consistent chrome across routes |
+| Settings cards | PrimeVue `Card` with `#title`, `#subtitle`, `#content` | Card slots required — body in `#content` only |
+| Form fields | PrimeVue `InputText` | Catalog component; token-backed borders |
+| Toggle | PrimeVue `ToggleSwitch` | Notifications preference |
+| Save action | PrimeVue `Button` severity primary | Detached below card stack |
+
+**Source:** `.heyeddi/designs/settings/mockup-brief.md` — implement from this brief; PNGs are spatial checks only.
+
+## Decision log (2026-07-04)
+
+| Region | Component | Rationale |
+|--------|-----------|-----------|
+| App layout | `AppShell` | Composes sidebar + main column; mobile backdrop for drawer |
+| Sidebar brand + nav | `AppSidebar` | Flex column with `flex: 1` nav and `margin-top: auto` user chip per spec |
+| Active nav | `.nav-link--active` pill | `brand-subtle` background with horizontal inset — not full-bleed gray |
+| User chip | Custom bordered block in sidebar | Avatar + name/email; pinned bottom with border on `surface-3` |
+| Top bar | `AppTopBar` | 64px height; breadcrumb/search/avatar desktop; hamburger + brand mobile |
+| Settings page | `SettingsView` | Max-width content column; page header outside cards |
+| Profile fields | PrimeVue `Card` + `InputText` in `#content` | Card slots required; fields inside `#content` slot |
+| Notifications | PrimeVue `Card` + `ToggleSwitch` | Desktop toggle row; mobile empty-state copy per responsive delta |
+| Save action | PrimeVue `Button` in `.settings__save` | Detached below card stack; right-aligned desktop, full-width mobile |
+| Layout tokens | `tokens.css` | `--sidebar-width: 15.5rem`, `--topbar-height: 4rem`, `--content-max-width: 45rem` |
diff --git a/src/App.vue b/src/App.vue
index 4f32238..ef6771d 100644
--- a/src/App.vue
+++ b/src/App.vue
@@ -1,16 +1,9 @@
 <template>
-  <main class="app-shell">
+  <AppShell>
     <router-view />
-  </main>
+  </AppShell>
 </template>
 
 <script setup lang="ts">
+import AppShell from "@/components/layout/AppShell.vue";
 </script>
-
-<style scoped>
-.app-shell {
-  min-height: 100vh;
-  background: var(--surface-1);
-  color: var(--text-1);
-}
-</style>
diff --git a/src/router/index.ts b/src/router/index.ts
index 106b91d..e0d3400 100644
--- a/src/router/index.ts
+++ b/src/router/index.ts
@@ -9,6 +9,9 @@ const router = createRouter({
       name: "settings",
       component: () => import("@/views/SettingsView.vue"),
     },
+    { path: "/dashboard", name: "dashboard", redirect: "/settings" },
+    { path: "/documents", name: "documents", redirect: "/settings" },
+    { path: "/team", name: "team", redirect: "/settings" },
   ],
 });
 
diff --git a/src/views/SettingsView.vue b/src/views/SettingsView.vue
index 87856b0..a4e7315 100644
--- a/src/views/SettingsView.vue
+++ b/src/views/SettingsView.vue
@@ -1,15 +1,182 @@
 <template>
-  <section class="settings-placeholder">
-    <h1>Settings</h1>
-    <p>Placeholder — @heyeddi-handoff implements from mockups.</p>
+  <section class="settings">
+    <header class="settings__header">
+      <h1 class="settings__title">Settings</h1>
+      <p class="settings__subtitle settings__subtitle--desktop">
+        Manage your profile and how we reach you.
+      </p>
+      <p class="settings__subtitle settings__subtitle--mobile">Profile and notifications</p>
+    </header>
+
+    <div class="settings__cards">
+      <Card class="settings__card">
+        <template #title>Profile</template>
+        <template #subtitle>Your name and sign-in email.</template>
+        <template #content>
+          <div class="settings__fields">
+            <label class="settings__field">
+              <span class="settings__label">Display name</span>
+              <InputText v-model="displayName" class="settings__input" />
+            </label>
+            <label class="settings__field">
+              <span class="settings__label">Email</span>
+              <InputText v-model="email" type="email" class="settings__input" />
+            </label>
+          </div>
+        </template>
+      </Card>
+
+      <Card class="settings__card">
+        <template #title>Notifications</template>
+        <template #subtitle>Choose how you hear about account activity.</template>
+        <template #content>
+          <div class="settings__toggle-row settings__toggle-row--desktop">
+            <span class="settings__toggle-label">Email updates</span>
+            <ToggleSwitch v-model="emailUpdates" />
+          </div>
+          <div class="settings__empty settings__empty--mobile">
+            <p class="settings__empty-title">No channels configured</p>
+            <p class="settings__empty-hint">Add email or push when you connect integrations.</p>
+          </div>
+        </template>
+      </Card>
+    </div>
+
+    <div class="settings__save">
+      <Button label="Save changes" />
+    </div>
   </section>
 </template>
 
-<script setup lang="ts"></script>
+<script setup lang="ts">
+import { ref } from "vue";
+import Card from "primevue/card";
+import InputText from "primevue/inputtext";
+import Button from "primevue/button";
+import ToggleSwitch from "primevue/toggleswitch";
+
+const displayName = ref("Alex Rivera");
+const email = ref("alex@example.com");
+const emailUpdates = ref(true);
+</script>
 
 <style scoped>
-.settings-placeholder {
-  padding: var(--size-5);
+.settings {
+  padding: var(--size-6) var(--size-5);
+  max-width: var(--content-max-width);
+}
+
+.settings__header {
+  margin-bottom: var(--size-6);
+}
+
+.settings__title {
+  margin: 0 0 var(--size-2);
+  font-size: var(--font-size-5);
+  font-weight: var(--font-weight-7);
+  color: var(--text-1);
+}
+
+.settings__subtitle {
+  margin: 0;
+  font-size: var(--font-size-2);
+  color: var(--text-2);
+}
+
+.settings__subtitle--mobile {
+  display: none;
+}
+
+.settings__cards {
+  display: flex;
+  flex-direction: column;
+  gap: var(--size-6);
+}
+
+.settings__card :deep(.p-card-body) {
+  padding: var(--size-6);
+}
+
+.settings__fields {
+  display: flex;
+  flex-direction: column;
+  gap: var(--size-4);
+}
+
+.settings__field {
+  display: flex;
+  flex-direction: column;
+  gap: var(--size-2);
+}
+
+.settings__label {
+  font-size: var(--font-size-1);
+  font-weight: var(--font-weight-5);
   color: var(--text-2);
 }
+
+.settings__input {
+  width: 100%;
+}
+
+.settings__toggle-row {
+  display: flex;
+  align-items: center;
+  justify-content: space-between;
+  gap: var(--size-4);
+}
+
+.settings__toggle-label {
+  font-size: var(--font-size-2);
+  color: var(--text-1);
+}
+
+.settings__empty {
+  display: none;
+}
+
+.settings__empty-title {
+  margin: 0 0 var(--size-2);
+  font-size: var(--font-size-2);
+  font-weight: var(--font-weight-6);
+  color: var(--text-1);
+}
+
+.settings__empty-hint {
+  margin: 0;
+  font-size: var(--font-size-1);
+  color: var(--text-2);
+}
+
+.settings__save {
+  display: flex;
+  justify-content: flex-end;
+  margin-top: var(--size-6);
+}
+
+@media (max-width: 48rem) {
+  .settings__subtitle--desktop {
+    display: none;
+  }
+
+  .settings__subtitle--mobile {
+    display: block;
+  }
+
+  .settings__toggle-row--desktop {
+    display: none;
+  }
+
+  .settings__empty--mobile {
+    display: block;
+  }
+
+  .settings__save {
+    justify-content: stretch;
+  }
+
+  .settings__save :deep(.p-button) {
+    width: 100%;
+  }
+}
 </style>
diff --git a/tests/unit/App.spec.ts b/tests/unit/App.spec.ts
index d917aa4..b06de80 100644
--- a/tests/unit/App.spec.ts
+++ b/tests/unit/App.spec.ts
@@ -1,17 +1,29 @@
 import { describe, it, expect } from "vitest";
 import { mount } from "@vue/test-utils";
-import { createRouter, createWebHistory } from "vue-router";
+import { createRouter, createMemoryHistory } from "vue-router";
+import PrimeVue from "primevue/config";
 import App from "@/App.vue";
 
 describe("App", () => {
   it("renders shell with router", async () => {
     const router = createRouter({
-      history: createWebHistory(),
-      routes: [{ path: "/", component: { template: "<div class='route-stub' />" } }],
+      history: createMemoryHistory("/settings"),
+      routes: [
+        { path: "/", redirect: "/settings" },
+        { path: "/settings", component: { template: "<div class='route-stub' />" } },
+        { path: "/dashboard", redirect: "/settings" },
+      ],
+    });
+    const wrapper = mount(App, {
+      global: {
+        plugins: [router, PrimeVue],
+        stubs: {
+          RouterView: false,
+        },
+      },
     });
-    const wrapper = mount(App, { global: { plugins: [router] } });
     await router.isReady();
-    expect(wrapper.find("main").exists()).toBe(true);
-    expect(wrapper.find(".router-view-stub, .route-stub").exists()).toBe(true);
+    expect(wrapper.find(".app-shell").exists()).toBe(true);
+    expect(wrapper.find(".route-stub").exists()).toBe(true);
   });
 });
```

## Design / handoff assets on disk (baseline + new)
- .heyeddi/designs/settings/desktop.png (42229 bytes)
- .heyeddi/designs/settings/handoff.json (363 bytes)
- .heyeddi/designs/settings/mobile.png (22676 bytes)
- .heyeddi/designs/settings/mockup-brief.md (7941 bytes)

## Changed file contents (full sources)

### .heyeddi/design.md
```
# Design (eval handoff)

Draft — `@heyeddi-handoff` should align implementation with this file and update component/layout notes.

## System

- Semantic tokens in `src/styles/tokens.css` — **OpenProps** on HeyEddi scaffold (`open-props` in `package.json`); custom `:root` vars OK on brownfield. See `heyeddi-design/reference/token-strategy.md`.
- PrimeVue for UI primitives — wire Aura preset to project brand token (not mockup PNG colors).
- **Component catalog:** `AppShell`, `AppSidebar`, `AppTopBar`, `Card`, `InputText`, `Button`, `ToggleSwitch`

## Settings mockups

`.heyeddi/designs/settings/` — designer attachments for SecureVault:
- `desktop.png` / `mobile.png` — layout references (regenerate: `uv run poe mockups`)
- `handoff.json` — route + contract notes only

**The skill authors `mockup-brief.md`** by interpreting the PNGs (`reference/interpret-mockups.md`), then syncs layout into this file via `describe_handoff --sync-design`.

**Mockup contract:** PNGs show **where** regions go. **Colors** come from this file and `tokens.css` — do not sample hues from PNG pixels.

## Layout — settings handoff (2026-07-04)

**Route:** `/settings` · **App:** SecureVault

### Layout topology

### Desktop

| Zone | Size / position | Behavior |
|------|-----------------|----------|
| App sidebar | Fixed left, `--sidebar-width` (248px) | Full viewport height; brand + nav scroll area + user chip pinned bottom |
| App top bar | Full width minus sidebar, `--topbar-height` (64px) | Fixed at top of main column; breadcrumb left, search + avatar right |
| Main content | Remaining width, max `--content-max-width` (~720px) | Scrolls vertically; padded route root |
| Settings cards | Stacked in content column | Profile card, Notifications card, gap between |
| Save CTA | Below card stack, right-aligned | Outside cards; not inside Card footer |

### Mobile

| Zone | Behavior |
|------|----------|
| Sidebar | Hidden off-canvas; hamburger in top bar opens drawer |
| Top bar | Full width; hamburger + "SecureVault" center + avatar |
| Content | Single column; page header + cards stack |
| Save CTA | Full-width button at bottom of content area |

### Region map

### Desktop

| Region | What the user sees | Build |
|--------|-------------------|-------|
| Sidebar brand | "SecureVault" + "Workspace" subtitle | Custom in `AppSidebar` |
| Sidebar nav | Dashboard, Documents, Team, Settings links | Custom nav list with active pill on Settings |
| Sidebar user chip | Avatar "A", Alex Rivera, alex@example.com in bordered card | Custom; pinned with `margin-top: auto` |
| Top bar breadcrumb | "Settings" label | `AppTopBar` |
| Top bar search | Rounded search input "Search…" | PrimeVue `InputText` |
| Top bar avatar | Blue circle | Custom avatar |
| Page header | "Settings" title + "Manage your profile and how we reach you." | Route root in `SettingsView` |
| Profile card | Title, subtitle, Display name + Email fields | PrimeVue `Card` + `InputText` in `#content` |
| Notifications card | Title, subtitle, Email updates row + toggle | PrimeVue `Card` + `ToggleSwitch` in `#content` |
| Save CTA | "Save changes" primary button | PrimeVue `Button`; below cards |

### Mobile

| Region | Build |
|--------|-------|
| Hamburger | `AppTopBar` menu button toggles sidebar drawer |
| Page subtitle | Shortened: "Profile and notifications" |
| Notifications card | Empty state copy: "No channels configured" + hint |
| Save CTA | Full-width `Button` at bottom |

### Component build sheet

| Piece | Choice | Rationale |
|-------|--------|-----------|
| App shell | `AppShell` composes sidebar + main column | Reusable layout for all routes |
| Sidebar | `AppSidebar` flex column | Nav scroll + user chip pinned bottom |
| Top bar | `AppTopBar` fixed height | Consistent chrome across routes |
| Settings cards | PrimeVue `Card` with `#title`, `#subtitle`, `#content` | Card slots required — body in `#content` only |
| Form fields | PrimeVue `InputText` | Catalog component; token-backed borders |
| Toggle | PrimeVue `ToggleSwitch` | Notifications preference |
| Save action | PrimeVue `Button` severity primary | Detached below card stack |

**Source:** `.heyeddi/designs/settings/mockup-brief.md` — implement from this brief; PNGs are spatial checks only.

## Decision log (2026-07-04)

| Region | Component | Rationale |
|--------|-----------|-----------|
| App layout | `AppShell` | Composes sidebar + main column; mobile backdrop for drawer |
| Sidebar brand + nav | `AppSidebar` | Flex column with `flex: 1` nav and `margin-top: auto` user chip per spec |
| Active nav | `.nav-link--active` pill | `brand-subtle` background with horizontal inset — not full-bleed gray |
| User chip | Custom bordered block in sidebar | Avatar + name/email; pinned bottom with border on `surface-3` |
| Top bar | `AppTopBar` | 64px height; breadcrumb/search/avatar desktop; hamburger + brand mobile |
| Settings page | `SettingsView` | Max-width content column; page header outside cards |
| Profile fields | PrimeVue `Card` + `InputText` in `#content` | Card slots required; fields inside `#content` slot |
| Notifications | PrimeVue `Card` + `ToggleSwitch` | Desktop toggle row; mobile empty-state copy per responsive delta |
| Save action | PrimeVue `Button` in `.settings__save` | Detached below card stack; right-aligned desktop, full-width mobile |
| Layout tokens | `tokens.css` | `--sidebar-width: 15.5rem`, `--topbar-height: 4rem`, `--content-max-width: 45rem` |

```

### src/App.vue
```
<template>
  <AppShell>
    <router-view />
  </AppShell>
</template>

<script setup lang="ts">
import AppShell from "@/components/layout/AppShell.vue";
</script>

```

### src/router/index.ts
```
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

```

### src/views/SettingsView.vue
```
<template>
  <section class="settings">
    <header class="settings__header">
      <h1 class="settings__title">Settings</h1>
      <p class="settings__subtitle settings__subtitle--desktop">
        Manage your profile and how we reach you.
      </p>
      <p class="settings__subtitle settings__subtitle--mobile">Profile and notifications</p>
    </header>

    <div class="settings__cards">
      <Card class="settings__card">
        <template #title>Profile</template>
        <template #subtitle>Your name and sign-in email.</template>
        <template #content>
          <div class="settings__fields">
            <label class="settings__field">
              <span class="settings__label">Display name</span>
              <InputText v-model="displayName" class="settings__input" />
            </label>
            <label class="settings__field">
              <span class="settings__label">Email</span>
              <InputText v-model="email" type="email" class="settings__input" />
            </label>
          </div>
        </template>
      </Card>

      <Card class="settings__card">
        <template #title>Notifications</template>
        <template #subtitle>Choose how you hear about account activity.</template>
        <template #content>
          <div class="settings__toggle-row settings__toggle-row--desktop">
            <span class="settings__toggle-label">Email updates</span>
            <ToggleSwitch v-model="emailUpdates" />
          </div>
          <div class="settings__empty settings__empty--mobile">
            <p class="settings__empty-title">No channels configured</p>
            <p class="settings__empty-hint">Add email or push when you connect integrations.</p>
          </div>
        </template>
      </Card>
    </div>

    <div class="settings__save">
      <Button label="Save changes" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import ToggleSwitch from "primevue/toggleswitch";

const displayName = ref("Alex Rivera");
const email = ref("alex@example.com");
const emailUpdates = ref(true);
</script>

<style scoped>
.settings {
  padding: var(--size-6) var(--size-5);
  max-width: var(--content-max-width);
}

.settings__header {
  margin-bottom: var(--size-6);
}

.settings__title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-7);
  color: var(--text-1);
}

.settings__subtitle {
  margin: 0;
  font-size: var(--font-size-2);
  color: var(--text-2);
}

.settings__subtitle--mobile {
  display: none;
}

.settings__cards {
  display: flex;
  flex-direction: column;
  gap: var(--size-6);
}

.settings__card :deep(.p-card-body) {
  padding: var(--size-6);
}

.settings__fields {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
}

.settings__field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.settings__label {
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-5);
  color: var(--text-2);
}

.settings__input {
  width: 100%;
}

.settings__toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--size-4);
}

.settings__toggle-label {
  font-size: var(--font-size-2);
  color: var(--text-1);
}

.settings__empty {
  display: none;
}

.settings__empty-title {
  margin: 0 0 var(--size-2);
  font-size: var(--font-size-2);
  font-weight: var(--font-weight-6);
  color: var(--text-1);
}

.settings__empty-hint {
  margin: 0;
  font-size: var(--font-size-1);
  color: var(--text-2);
}

.settings__save {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--size-6);
}

@media (max-width: 48rem) {
  .settings__subtitle--desktop {
    display: none;
  }

  .settings__subtitle--mobile {
    display: block;
  }

  .settings__toggle-row--desktop {
    display: none;
  }

  .settings__empty--mobile {
    display: block;
  }

  .settings__save {
    justify-content: stretch;
  }

  .settings__save :deep(.p-button) {
    width: 100%;
  }
}
</style>

```

### tests/unit/App.spec.ts
```
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

```


## Command runs (complete output — check warnings/errors)
### $ npm test
exit_code: 0
```

> test
> vitest run


 RUN  v3.2.6 /home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only

 ✓ tests/unit/App.spec.ts (1 test) 154ms
 ✓ tests/unit/src/views/SettingsView.spec.ts (2 tests) 224ms

 Test Files  2 passed (2)
      Tests  3 passed (3)
   Start at  17:59:02
   Duration  2.61s (transform 465ms, setup 353ms, collect 740ms, tests 377ms, environment 1.87s, prepare 509ms)


```

### $ npm run build
exit_code: 0
```

> build
> vue-tsc -b && vite build

vite v6.4.3 building for production...
transforming...
✓ 264 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                          0.40 kB │ gzip:  0.27 kB
dist/assets/SettingsView-08NwJ-yK.css    1.91 kB │ gzip:  0.46 kB
dist/assets/index-BIq8P9X2.css          34.94 kB │ gzip:  8.95 kB
dist/assets/SettingsView-5DTtdwc0.js    64.95 kB │ gzip: 12.98 kB
dist/assets/index-CCrGvbnS.js          263.89 kB │ gzip: 70.01 kB
✓ built in 2.06s

```

### $ python3 .agents/skills/heyeddi-handoff/scripts/verify_handoff.py --route /settings --check
exit_code: 0
```
{
  "ok": true,
  "phase": "full",
  "has_implementation_spec": true,
  "checks": [
    {
      "name": "Sidebar width",
      "ok": true,
      "requirement": "`--sidebar-width: 15.5rem` (248px)",
      "target": "`src/styles/tokens.css`, `src/components/layout/AppSidebar.vue`",
      "patterns": [
        "\\-\\-sidebar\\-width"
      ]
    },
    {
      "name": "Sidebar column",
      "ok": true,
      "requirement": "`display: flex; flex-direction: column; min-height: 100%`",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "display"
      ]
    },
    {
      "name": "Nav scroll area",
      "ok": true,
      "requirement": "`flex: 1` on nav wrapper",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "flex:\\s*1"
      ]
    },
    {
      "name": "User chip pin",
      "ok": true,
      "requirement": "`margin-top: auto` on user block",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "margin\\-top:\\s*auto"
      ]
    },
    {
      "name": "Nav row height",
      "ok": true,
      "requirement": "`min-height: 2.75rem` (44px)",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "min\\-height"
      ]
    },
    {
      "name": "Nav active pill",
      "ok": true,
      "requirement": "`background: var(--brand-subtle); color: var(--brand); border-radius: var(--radius-2); padding: var(--size-2) var(--size-3); padding-inline: var(--size-3)` with horizontal inset",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "\\-\\-brand\\-subtle",
        "\\-\\-brand",
        "\\-\\-radius\\-2",
        "\\-\\-size\\-2",
        "\\-\\-size\\-3",
        "\\-\\-size\\-3",
        "brand\\-subtle"
      ]
    },
    {
      "name": "Top bar height",
      "ok": true,
      "requirement": "`--topbar-height: 4rem` (64px); `height: var(--topbar-height)`",
      "target": "`src/styles/tokens.css`, `src/components/layout/AppTopBar.vue`",
      "patterns": [
        "\\-\\-topbar\\-height",
        "\\-\\-topbar\\-height"
      ]
    },
    {
      "name": "Content max-width",
      "ok": true,
      "requirement": "`--content-max-width: 45rem` (~720px)",
      "target": "`src/styles/tokens.css`, `src/views/SettingsView.vue`",
      "patterns": [
        "\\-\\-content\\-max\\-width"
      ]
    },
    {
      "name": "Content padding",
      "ok": true,
      "requirement": "`padding: var(--size-6) var(--size-5)` on route root",
      "target": "`src/views/SettingsView.vue`",
      "patterns": [
        "\\-\\-size\\-6",
        "\\-\\-size\\-5"
      ]
    },
    {
      "name": "Card stack gap",
      "ok": true,
      "requirement": "`gap: var(--size-6)` on `.settings__cards`",
      "target": "`src/views/SettingsView.vue`",
      "patterns": [
        "\\-\\-size\\-6",
        "gap:\\s*var\\(\\-\\-size\\-"
      ]
    },
    {
      "name": "Card body padding",
      "ok": true,
      "requirement": "`:deep(.p-card-body) { padding: var(--size-6) }`",
      "target": "`src/views/SettingsView.vue`",
      "patterns": [
        "\\-\\-size\\-6",
        "p-card-body|\\.p-card"
      ]
    },
    {
      "name": "Save CTA",
      "ok": true,
      "requirement": "below cards; desktop `justify-content: flex-end`; `margin-top: var(--size-6)` on `.settings__save`",
      "target": "`src/views/SettingsView.vue`",
      "patterns": [
        "\\-\\-size\\-6",
        "justify\\-content:\\s*flex\\-end"
      ]
    },
    {
      "name": "User chip",
      "ok": true,
      "requirement": "bordered card (`border: 1px solid var(--surface-3)`), avatar circle, pinned bottom",
      "target": "`src/components/layout/AppSidebar.vue`",
      "patterns": [
        "\\-\\-surface\\-3"
      ]
    },
    {
      "name": "Sidebar width token",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/styles/tokens.css"
      ],
      "patterns": [
        "--sidebar-width"
      ]
    },
    {
      "name": "Sidebar flex column + user pinned",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/components/layout/AppSidebar.vue"
      ],
      "patterns": [
        "flex-direction:\\s*column",
        "margin-top:\\s*auto"
      ]
    },
    {
      "name": "Nav active brand pill",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/components/layout/AppSidebar.vue"
      ],
      "patterns": [
        "brand-subtle",
        "nav-link--active|active"
      ]
    },
    {
      "name": "App shell layout",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/components/layout/AppShell.vue"
      ],
      "patterns": [
        "AppSidebar",
        "app-shell"
      ]
    },
    {
      "name": "Top bar height token",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/styles/tokens.css",
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/components/layout/AppTopBar.vue"
      ],
      "patterns": [
        "--topbar-height"
      ]
    },
    {
      "name": "Settings cards use Card",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/views/SettingsView.vue"
      ],
      "patterns": [
        "Card",
        "settings__cards|settings__card"
      ]
    },
    {
      "name": "Settings Card body uses #content slot",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/views/SettingsView.vue"
      ],
      "patterns": [
        "<template\\s+#content>",
        "Card"
      ]
    },
    {
      "name": "Card stack gap",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/views/SettingsView.vue"
      ],
      "patterns": [
        "gap:\\s*var\\(--size-"
      ]
    },
    {
      "name": "Save CTA outside cards",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/views/SettingsView.vue"
      ],
      "patterns": [
        "Save changes",
        "settings__save"
      ]
    },
    {
      "name": "Content max-width",
      "ok": true,
      "files": [
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/styles/tokens.css",
        "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/views/SettingsView.vue"
      ],
      "patterns": [
        "--content-max-width|max-width"
      ]
    },
    {
      "name": "PrimeVue Card #content slots",
      "ok": true,
      "issues": []
    }
  ],
  "failed": [],
  "route": "/settings",
  "feature": "settings"
}

```

### $ python3 .agents/skills/heyeddi-handoff/scripts/verify_tokens.py --check
exit_code: 0
```
{
  "ok": true,
  "circular_aliases": [],
  "path": "/home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-handoff-only/src/styles/tokens.css"
}

```

### $ python3 .agents/skills/heyeddi-handoff/scripts/verify_theme.py --check
exit_code: 0
```
Theme verification OK — semantic light/dark tokens and PrimeVue surfaces aligned.

```


## Hard gates

All deterministic checks passed.

## Visual QA captures (Playwright)

Route: `/settings`

**Captured screenshots** (read these PNG files in the workspace — compare to references):
- `.heyeddi/audits/eval-process/single/settings_375px.png` (36036 bytes)
- `.heyeddi/audits/eval-process/single/settings_768px.png` (38331 bytes)
- `.heyeddi/audits/eval-process/single/settings_1440px.png` (51024 bytes)
- `.heyeddi/audits/eval-process/single/settings_1440px_dark.png` (50627 bytes)

**Reference mockups** (layout/hierarchy only — colors come from design.md, not PNG pixels):
- `.heyeddi/designs/settings/desktop.png`
- `.heyeddi/designs/settings/mobile.png`

**Automated pixel similarity** (coarse — high score does NOT mean good spacing; mostly white/gray layouts score ~0.9+ even when cramped):
- [ok] capture `.heyeddi/audits/eval-process/single/settings_1440px.png` vs ref `.heyeddi/designs/settings/desktop.png`: similarity=0.97 (min 0.12)
- [ok] capture `.heyeddi/audits/eval-process/single/settings_375px.png` vs ref `.heyeddi/designs/settings/mobile.png`: similarity=0.92 (min 0.12)

**Rendered spacing checks** (computed CSS — AUTO-FAIL if any fail):
- [ok] sidebar width @ desktop: 248.0px (expect 220–290px)
- [ok] settings card stack gap: 28.0px (expect >= 16px)
- [ok] card body padding-top: 28.0px (expect >= 16px)
- [ok] sidebar width @ desktop: 248.0px (expect 220–290px)
- [ok] settings card stack gap: 28.0px (expect >= 16px)
- [ok] card body padding-top: 28.0px (expect >= 16px)

**Rendered content checks** (DOM — AUTO-FAIL if any fail):
- [ok] settings form inputs: 2 visible (expect >= 2 (Display name + Email))
- [ok] settings notification toggle: 2 visible (expect >= 1 ToggleSwitch)
- [ok] settings save CTA: 1 visible (expect Save changes button)
- [ok] settings form inputs: 2 visible (expect >= 2 (Display name + Email))
- [ok] settings notification toggle: 2 visible (expect >= 1 ToggleSwitch)
- [ok] settings save CTA: 1 visible (expect Save changes button)
- [ok] settings form inputs @ dark: 2 visible (expect >= 2 (Display name + Email))
- [ok] settings notification toggle @ dark: 2 visible (expect >= 1 ToggleSwitch)
- [ok] settings save CTA @ dark: 1 visible (expect Save changes button)
- [ok] dark mode card surface: rgb(24, 24, 27) (expect non-transparent card background)

**Your job:** Open the captured screenshots and reference mockups. Fail if:
- No app shell when mockup shows sidebar/top bar (flat page on gray background)
- Inputs look like solid black boxes or unstyled native fields
- No card/panel layout / wrong region hierarchy vs mockups
- Page is sparse, cramped in a corner, or missing key regions (Profile, Notifications, Save CTA)
- **Empty PrimeVue Cards** — title/subtitle only with no fields, toggles, or stat values in card body
- **Cramped spacing** — card body padding < 16px, card stack gap < 16px, or sidebar < 220px at desktop
- Captures are missing or capture errors occurred

**Do not fail** solely because primary button/toggle color differs from mockup PNG — judge colors against design.md tokens.

