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
5. **Design talk:** `@heyeddi-design` and `@design-handoff` must append to **Decision log** in `.heyeddi/design.md` — conversational rationale (we chose / we rejected). Fail if UI shipped with no new Decision log entry for that feature.
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

## Eval case: heyeddi-design-polish-existing
## Turn: single
## Skills invoked: @heyeddi-design, @primevue-openprops-architect

## User goal (worker prompt)
@heyeddi-design @primevue-openprops-architect

**Goal:** The `/login` screen **already exists** but looks bad (black native inputs, hex colors, cramped layout). **Critique first, then polish** — not greenfield `shape` + `craft`.

## Mandatory order

1. `load_context` — read `.heyeddi/product.md` and `.heyeddi/design.md`.
2. **Critique** (`reference/critique.md`) — study `LoginView.vue`; write `.heyeddi/docs/login-critique.md` (P0/P1 issues, token drift, fix directions).
3. **Document** — update `.heyeddi/design.md` where drift vs intended tokens/components.
4. **Polish** (`reference/polish.md`) — fix P0/P1 from your critique: PrimeVue + OpenProps, no hex, spacing/hierarchy.
5. Validate with `@primevue-openprops-architect`.
6. **Append** Decision log — reference critique findings + what you fixed.

**Scope / stop rules:**
- Finish when `npm test` and `npm run build` pass.
- Do **not** run Playwright, `@visual-auditor`, or `npm run dev` — harness runs visual QA after your turn.

No designer mockups — judge critique quality + implementation improvements.

## Success criteria for this turn
Independent **@heyeddi-design** eval — **existing UI**, not greenfield.

## Pipeline (required)

- `load_context` run
- **Critique first** — `.heyeddi/docs/login-critique.md` exists with P0/P1 issues (native inputs, hex, cramped layout, etc.)
- **Then polish** — not full greenfield `shape`
- `.heyeddi/design.md` updated for drift; Decision log cites critique + fixes
- Login uses PrimeVue + OpenProps after polish — no black inputs, no inline hex
- **FAIL if:** skipped critique, no critique file, polish without addressing documented P0s
- Playwright captures in `.heyeddi/audits/eval-capture/` — fail if still looks like broken baseline
- Tests/build clean

Do not require @design-handoff or mockup PNGs.

## Worker agent output
I'll follow the heyeddi-design workflow: load context, critique the login screen, then polish it. Reading the skill, product/design docs, and `LoginView.vue` first.
Creating the critique document, then polishing the login screen. Fixing `App.vue` so tests pass.
Updating the LoginView test to mount PrimeVue.
Appending the decision log and finishing up.
## Critique summary

The login screen read as a debug stub: **native `<input>` / `<button>`**, **six inline hex colors**, **8px padding**, and a **280px** column — none of it using OpenProps or PrimeVue despite what `design.md` specified.

Full report: `.heyeddi/docs/login-critique.md`

| Priority | Issues |
|----------|--------|
| **P0** | Native controls, inline hex, no Card, full token/component drift |
| **P1** | Cramped spacing, weak hierarchy, missing forgot-password, no label/`for` pairing |
| **P2** | Remember-me, SSO, validation states (deferred) |

**Audience fit:** REVISE — trust/persona scores were low; fixable via polish, not a full reshape.

---

## What changed

**`LoginView.vue`** — PrimeVue `Card`, `InputText`, `Password`, `Button`; centered 28rem auth panel; OpenProps spacing/surface tokens; “Sign in to SecureVault” copy; forgot-password link.

**`design.md`** — Token table, auth layout rules, component catalog (including `Password`), drift marked resolved, decision log appended.

**Supporting fixes**
- `App.vue` — semantic `<main>` wrapper (tests + a11y)
- `ForgotPasswordView.vue` + route — placeholder for the forgot-password affordance
- `tests/unit/setup.ts` — PrimeVue plugin for component tests

---

## Validation

| Check | Result |
|-------|--------|
| `@primevue-openprops-architect` (`validate_vue.py`) | vue-tsc pass |
| `npm test` | 2/2 pass |
| `npm run build` | pass |

No Playwright/dev server run per scope. Harness can run visual QA next.

## Git diff stat
.heyeddi/design.md      |  80 ++++++++++++++++++++++++----
 src/App.vue             |  12 ++++-
 src/router/index.ts     |   5 ++
 src/views/LoginView.vue | 135 ++++++++++++++++++++++++++++++++++++++++--------
 tests/unit/setup.ts     |  35 +++++++++++++
 5 files changed, 232 insertions(+), 35 deletions(-)

## Git diff patch
```
diff --git a/.heyeddi/design.md b/.heyeddi/design.md
index f3f33f9..fa92adb 100644
--- a/.heyeddi/design.md
+++ b/.heyeddi/design.md
@@ -1,19 +1,77 @@
-# Design — SecureVault (out of sync with code)
+# Design — SecureVault
 
-> **Eval:** Documents OpenProps + PrimeVue, but `LoginView.vue` **violates** this file. `@heyeddi-design` must **audit existing UI**, update this doc from code (scan mode), then **polish**.
+> Product register UI: OpenProps semantic tokens + PrimeVue Aura (indigo primary). See `.heyeddi/docs/login-critique.md` for brownfield audit (2026-07-04).
 
-## System (intended)
+## Token source
 
-- OpenProps tokens + PrimeVue InputText, Button, Card
-- No raw hex in Vue/CSS
+OpenProps via `src/styles/tokens.css` — semantic aliases only in components:
+
+| Token | Maps to | Use |
+|-------|---------|-----|
+| `--surface-0` | `--gray-0` | Elevated panels on dark contexts |
+| `--surface-1` | `--gray-1` | Page background |
+| `--surface-2` | `--gray-2` | Cards, raised panels |
+| `--text-1` | `--gray-12` | Headings, primary copy |
+| `--text-2` | `--gray-9` | Labels, hints, secondary copy |
+| `--font-size-1` | `--font-size-0` | Labels, hints |
+| `--font-size-2` | `--font-size-1` | Body |
+| `--font-size-5` | `--font-size-4` | Card titles |
+
+Spacing: OpenProps `--size-*` directly in scoped CSS (no circular aliases).
+
+Primary actions: PrimeVue Aura preset in `main.ts` (`HeyEddiAura`, indigo scale) — not custom hex buttons.
+
+## Layout — auth surfaces
+
+- Full-viewport centered column; max form width ~28rem (`--size-content-2` / 24–28rem).
+- Card internal padding: `--size-5`–`--size-6`.
+- Field stack gap: `--size-3`; section gap (title → fields): `--size-5`.
+- CTA separation above primary button: `--size-4` minimum.
 
 ## Component catalog
 
-| UI | PrimeVue |
-|----|----------|
-| Sign in | Button |
-| Email / password | InputText |
+| UI | PrimeVue | Notes |
+|----|----------|-------|
+| Auth panel | `Card` | `#title`, `#subtitle`, `#content` slots required |
+| Sign in | `Button` | `severity="primary"`, full width on auth forms |
+| Email | `InputText` | `type="email"`, paired `<label for>` |
+| Password | `Password` | Mask toggle; paired `<label for>` |
+| Forgot password | `router-link` or text link | Styled with `--text-2`, token spacing |
+
+## Do's and Don'ts
+
+- **Do** use semantic CSS variables and PrimeVue components from this catalog.
+- **Do** use scoped CSS classes for layout; keep templates free of inline `style=""`.
+- **Don't** use raw hex in `.vue` or component CSS.
+- **Don't** use native `<input>` / `<button>` when a catalog component exists.
+
+## Known drift (resolved 2026-07-04)
+
+- ~~Login route used native inputs and hex colors~~ — polished in `LoginView.vue`.
+
+## Decision log
+
+### 2026-07-04 — /login (@heyeddi-design polish)
+
+**Context:** Brownfield critique (`.heyeddi/docs/login-critique.md`) found P0 token/component drift — native inputs, inline hex, cramped 280px layout. SecureVault product register; personas not yet in `product.md`.
+
+**We chose:**
+- Centered auth card at 28rem max-width with OpenProps spacing (`--size-2`–`--size-6`) and semantic surfaces (`--surface-1`, `--surface-2`, `--text-1`, `--text-2`).
+- Product-facing copy: “Sign in to SecureVault” title + supportive subtitle for trust (critique P1 persona/trust scores).
+- Forgot-password link → placeholder `/forgot-password` route (surface-completeness affordance; API deferred).
+
+**Component strategy:**
+- Auth panel → PrimeVue `Card` (`#title`, `#subtitle`, `#content`)
+- Email → `InputText` with `for`/`id` labels
+- Password → `Password` (toggle mask; catalog updated from generic InputText)
+- Sign in → `Button` primary, full width, form submit
+- App shell → semantic `<main>` in `App.vue` (a11y + existing unit test)
+
+**We rejected:**
+- Keeping inline hex / native controls — direct P0 critique blockers.
+- Greenfield `shape` — IA (email, password, sign-in) was already correct.
+- Remember-me / SSO in this pass — P2; deferred until product personas defined.
 
-## Known drift
+**Critique → fixes:** P0 hex/PrimeVue drift, inline styles, missing Card → resolved. P1 spacing, hierarchy, forgot-password, a11y labels → resolved.
 
-- Login route uses native `<input>` and hex colors — fix via `polish` workflow
+**Open questions:** Wire auth API and forgot-password flow when backend ready.
diff --git a/src/App.vue b/src/App.vue
index d372e96..39d0eb9 100644
--- a/src/App.vue
+++ b/src/App.vue
@@ -1,6 +1,14 @@
 <template>
-  <router-view />
+  <main class="app-shell">
+    <router-view />
+  </main>
 </template>
 
-<script setup>
+<script setup lang="ts">
 </script>
+
+<style scoped>
+.app-shell {
+  min-height: 100vh;
+}
+</style>
diff --git a/src/router/index.ts b/src/router/index.ts
index d5f712b..0935ac8 100644
--- a/src/router/index.ts
+++ b/src/router/index.ts
@@ -9,6 +9,11 @@ const router = createRouter({
       name: "login",
       component: () => import("@/views/LoginView.vue"),
     },
+    {
+      path: "/forgot-password",
+      name: "forgot-password",
+      component: () => import("@/views/ForgotPasswordView.vue"),
+    },
   ],
 });
 
diff --git a/src/views/LoginView.vue b/src/views/LoginView.vue
index 122ed26..2385eb1 100644
--- a/src/views/LoginView.vue
+++ b/src/views/LoginView.vue
@@ -1,35 +1,126 @@
 <template>
-  <div style="padding: 8px; max-width: 280px">
-    <h1 style="font-size: 14px; color: #999">Login</h1>
-    <label style="font-size: 10px; color: #aaa">Email</label>
-    <input
-      v-model="email"
-      type="email"
-      style="display: block; width: 100%; background: #000; color: #fff; border: none; padding: 4px"
-    />
-    <label style="font-size: 10px; color: #aaa">Password</label>
-    <input
-      v-model="password"
-      type="password"
-      style="display: block; width: 100%; background: #000; color: #fff; border: none; padding: 4px"
-    />
-    <button
-      type="button"
-      style="margin-top: 8px; width: 100%; background: #3dd68c; border: none; padding: 12px"
-      @click="signIn"
-    >
-      Sign in
-    </button>
+  <div class="login-page">
+    <Card class="login-card">
+      <template #title>Sign in to SecureVault</template>
+      <template #subtitle>Enter your credentials to access your vault.</template>
+      <template #content>
+        <form class="login-form" @submit.prevent="signIn">
+          <div class="login-field">
+            <label class="login-field__label" for="login-email">Email</label>
+            <InputText
+              id="login-email"
+              v-model="email"
+              type="email"
+              autocomplete="email"
+              class="login-field__input"
+              fluid
+            />
+          </div>
+          <div class="login-field">
+            <label class="login-field__label" for="login-password">Password</label>
+            <Password
+              id="login-password"
+              v-model="password"
+              :feedback="false"
+              toggle-mask
+              autocomplete="current-password"
+              class="login-field__input"
+              fluid
+            />
+          </div>
+          <div class="login-form__actions">
+            <Button type="submit" label="Sign in" fluid />
+          </div>
+          <p class="login-form__footer">
+            <router-link to="/forgot-password" class="login-form__link">
+              Forgot password?
+            </router-link>
+          </p>
+        </form>
+      </template>
+    </Card>
   </div>
 </template>
 
 <script setup lang="ts">
 import { ref } from "vue";
+import Button from "primevue/button";
+import Card from "primevue/card";
+import InputText from "primevue/inputtext";
+import Password from "primevue/password";
 
 const email = ref("user@example.com");
 const password = ref("");
 
 function signIn(): void {
-  // stub
+  // stub — wire auth API later
 }
 </script>
+
+<style scoped>
+.login-page {
+  display: flex;
+  align-items: center;
+  justify-content: center;
+  min-height: 100vh;
+  padding: var(--size-5);
+  background: var(--surface-1);
+}
+
+.login-card {
+  width: min(100%, 28rem);
+  background: var(--surface-2);
+}
+
+.login-card :deep(.p-card-title) {
+  font-size: var(--font-size-5);
+  color: var(--text-1);
+}
+
+.login-card :deep(.p-card-subtitle) {
+  color: var(--text-2);
+  font-size: var(--font-size-2);
+}
+
+.login-form {
+  display: flex;
+  flex-direction: column;
+  gap: var(--size-4);
+}
+
+.login-field {
+  display: flex;
+  flex-direction: column;
+  gap: var(--size-2);
+}
+
+.login-field__label {
+  font-size: var(--font-size-1);
+  font-weight: var(--font-weight-5);
+  color: var(--text-2);
+}
+
+.login-field__input {
+  width: 100%;
+}
+
+.login-form__actions {
+  margin-top: var(--size-2);
+}
+
+.login-form__footer {
+  margin: 0;
+  text-align: center;
+}
+
+.login-form__link {
+  font-size: var(--font-size-1);
+  color: var(--text-2);
+  text-decoration: none;
+}
+
+.login-form__link:hover {
+  color: var(--text-1);
+  text-decoration: underline;
+}
+</style>
diff --git a/tests/unit/setup.ts b/tests/unit/setup.ts
index dd8b02d..c70a689 100644
--- a/tests/unit/setup.ts
+++ b/tests/unit/setup.ts
@@ -1,4 +1,39 @@
 import { config } from "@vue/test-utils";
+import PrimeVue from "primevue/config";
+import { definePreset } from "@primeuix/themes";
+import Aura from "@primevue/themes/aura";
+
+const HeyEddiAura = definePreset(Aura, {
+  semantic: {
+    primary: {
+      50: "{indigo.50}",
+      100: "{indigo.100}",
+      200: "{indigo.200}",
+      300: "{indigo.300}",
+      400: "{indigo.400}",
+      500: "{indigo.500}",
+      600: "{indigo.600}",
+      700: "{indigo.700}",
+      800: "{indigo.800}",
+      900: "{indigo.900}",
+      950: "{indigo.950}",
+    },
+  },
+});
+
+config.global.plugins = [
+  [
+    PrimeVue,
+    {
+      theme: {
+        preset: HeyEddiAura,
+        options: {
+          darkModeSelector: "system",
+        },
+      },
+    },
+  ],
+];
 
 config.global.stubs = {
   RouterView: { template: "<div class='router-view-stub' />" },
```

## Design / handoff assets on disk (baseline + new)
(no design assets under .heyeddi/designs/ or designs/)

## Changed file contents (full sources)

### .heyeddi/design.md
```
# Design — SecureVault

> Product register UI: OpenProps semantic tokens + PrimeVue Aura (indigo primary). See `.heyeddi/docs/login-critique.md` for brownfield audit (2026-07-04).

## Token source

OpenProps via `src/styles/tokens.css` — semantic aliases only in components:

| Token | Maps to | Use |
|-------|---------|-----|
| `--surface-0` | `--gray-0` | Elevated panels on dark contexts |
| `--surface-1` | `--gray-1` | Page background |
| `--surface-2` | `--gray-2` | Cards, raised panels |
| `--text-1` | `--gray-12` | Headings, primary copy |
| `--text-2` | `--gray-9` | Labels, hints, secondary copy |
| `--font-size-1` | `--font-size-0` | Labels, hints |
| `--font-size-2` | `--font-size-1` | Body |
| `--font-size-5` | `--font-size-4` | Card titles |

Spacing: OpenProps `--size-*` directly in scoped CSS (no circular aliases).

Primary actions: PrimeVue Aura preset in `main.ts` (`HeyEddiAura`, indigo scale) — not custom hex buttons.

## Layout — auth surfaces

- Full-viewport centered column; max form width ~28rem (`--size-content-2` / 24–28rem).
- Card internal padding: `--size-5`–`--size-6`.
- Field stack gap: `--size-3`; section gap (title → fields): `--size-5`.
- CTA separation above primary button: `--size-4` minimum.

## Component catalog

| UI | PrimeVue | Notes |
|----|----------|-------|
| Auth panel | `Card` | `#title`, `#subtitle`, `#content` slots required |
| Sign in | `Button` | `severity="primary"`, full width on auth forms |
| Email | `InputText` | `type="email"`, paired `<label for>` |
| Password | `Password` | Mask toggle; paired `<label for>` |
| Forgot password | `router-link` or text link | Styled with `--text-2`, token spacing |

## Do's and Don'ts

- **Do** use semantic CSS variables and PrimeVue components from this catalog.
- **Do** use scoped CSS classes for layout; keep templates free of inline `style=""`.
- **Don't** use raw hex in `.vue` or component CSS.
- **Don't** use native `<input>` / `<button>` when a catalog component exists.

## Known drift (resolved 2026-07-04)

- ~~Login route used native inputs and hex colors~~ — polished in `LoginView.vue`.

## Decision log

### 2026-07-04 — /login (@heyeddi-design polish)

**Context:** Brownfield critique (`.heyeddi/docs/login-critique.md`) found P0 token/component drift — native inputs, inline hex, cramped 280px layout. SecureVault product register; personas not yet in `product.md`.

**We chose:**
- Centered auth card at 28rem max-width with OpenProps spacing (`--size-2`–`--size-6`) and semantic surfaces (`--surface-1`, `--surface-2`, `--text-1`, `--text-2`).
- Product-facing copy: “Sign in to SecureVault” title + supportive subtitle for trust (critique P1 persona/trust scores).
- Forgot-password link → placeholder `/forgot-password` route (surface-completeness affordance; API deferred).

**Component strategy:**
- Auth panel → PrimeVue `Card` (`#title`, `#subtitle`, `#content`)
- Email → `InputText` with `for`/`id` labels
- Password → `Password` (toggle mask; catalog updated from generic InputText)
- Sign in → `Button` primary, full width, form submit
- App shell → semantic `<main>` in `App.vue` (a11y + existing unit test)

**We rejected:**
- Keeping inline hex / native controls — direct P0 critique blockers.
- Greenfield `shape` — IA (email, password, sign-in) was already correct.
- Remember-me / SSO in this pass — P2; deferred until product personas defined.

**Critique → fixes:** P0 hex/PrimeVue drift, inline styles, missing Card → resolved. P1 spacing, hierarchy, forgot-password, a11y labels → resolved.

**Open questions:** Wire auth API and forgot-password flow when backend ready.

```

### src/App.vue
```
<template>
  <main class="app-shell">
    <router-view />
  </main>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}
</style>

```

### src/router/index.ts
```
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/login" },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      path: "/forgot-password",
      name: "forgot-password",
      component: () => import("@/views/ForgotPasswordView.vue"),
    },
  ],
});

export default router;

```

### src/views/LoginView.vue
```
<template>
  <div class="login-page">
    <Card class="login-card">
      <template #title>Sign in to SecureVault</template>
      <template #subtitle>Enter your credentials to access your vault.</template>
      <template #content>
        <form class="login-form" @submit.prevent="signIn">
          <div class="login-field">
            <label class="login-field__label" for="login-email">Email</label>
            <InputText
              id="login-email"
              v-model="email"
              type="email"
              autocomplete="email"
              class="login-field__input"
              fluid
            />
          </div>
          <div class="login-field">
            <label class="login-field__label" for="login-password">Password</label>
            <Password
              id="login-password"
              v-model="password"
              :feedback="false"
              toggle-mask
              autocomplete="current-password"
              class="login-field__input"
              fluid
            />
          </div>
          <div class="login-form__actions">
            <Button type="submit" label="Sign in" fluid />
          </div>
          <p class="login-form__footer">
            <router-link to="/forgot-password" class="login-form__link">
              Forgot password?
            </router-link>
          </p>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

const email = ref("user@example.com");
const password = ref("");

function signIn(): void {
  // stub — wire auth API later
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--size-5);
  background: var(--surface-1);
}

.login-card {
  width: min(100%, 28rem);
  background: var(--surface-2);
}

.login-card :deep(.p-card-title) {
  font-size: var(--font-size-5);
  color: var(--text-1);
}

.login-card :deep(.p-card-subtitle) {
  color: var(--text-2);
  font-size: var(--font-size-2);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--size-4);
}

.login-field {
  display: flex;
  flex-direction: column;
  gap: var(--size-2);
}

.login-field__label {
  font-size: var(--font-size-1);
  font-weight: var(--font-weight-5);
  color: var(--text-2);
}

.login-field__input {
  width: 100%;
}

.login-form__actions {
  margin-top: var(--size-2);
}

.login-form__footer {
  margin: 0;
  text-align: center;
}

.login-form__link {
  font-size: var(--font-size-1);
  color: var(--text-2);
  text-decoration: none;
}

.login-form__link:hover {
  color: var(--text-1);
  text-decoration: underline;
}
</style>

```

### tests/unit/setup.ts
```
import { config } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { definePreset } from "@primeuix/themes";
import Aura from "@primevue/themes/aura";

const HeyEddiAura = definePreset(Aura, {
  semantic: {
    primary: {
      50: "{indigo.50}",
      100: "{indigo.100}",
      200: "{indigo.200}",
      300: "{indigo.300}",
      400: "{indigo.400}",
      500: "{indigo.500}",
      600: "{indigo.600}",
      700: "{indigo.700}",
      800: "{indigo.800}",
      900: "{indigo.900}",
      950: "{indigo.950}",
    },
  },
});

config.global.plugins = [
  [
    PrimeVue,
    {
      theme: {
        preset: HeyEddiAura,
        options: {
          darkModeSelector: "system",
        },
      },
    },
  ],
];

config.global.stubs = {
  RouterView: { template: "<div class='router-view-stub' />" },
  RouterLink: { template: "<a><slot /></a>", props: ["to"] },
};

```


## Command runs (complete output — check warnings/errors)
### $ npm test
exit_code: 0
```

> test
> vitest run


 RUN  v3.2.6 /home/eddi/Projects/heyeddi/skills/evals/runs/2026-07-04T22-58-59Z/heyeddi-design-polish-existing

 ✓ tests/unit/App.spec.ts (1 test) 168ms
 ✓ tests/unit/src/views/LoginView.spec.ts (1 test) 302ms
   ✓ LoginView > renders sign in  300ms

 Test Files  2 passed (2)
      Tests  2 passed (2)
   Start at  17:45:12
   Duration  2.36s (transform 296ms, setup 616ms, collect 434ms, tests 471ms, environment 1.64s, prepare 432ms)


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
dist/index.html                                0.40 kB │ gzip:  0.27 kB
dist/assets/ForgotPasswordView-Dj1hpdil.css    0.32 kB │ gzip:  0.21 kB
dist/assets/LoginView-FS5j98jY.css             1.07 kB │ gzip:  0.37 kB
dist/assets/index-CYKRDnkO.css                29.71 kB │ gzip:  7.85 kB
dist/assets/ForgotPasswordView-BY7KJvvD.js     0.67 kB │ gzip:  0.43 kB
dist/assets/index-DtdFObL5.js                 17.41 kB │ gzip:  4.88 kB
dist/assets/LoginView-pIpM17WV.js             89.04 kB │ gzip: 20.08 kB
dist/assets/index-DfDL_T9A.js                250.33 kB │ gzip: 68.49 kB
✓ built in 1.88s

```


## Hard gates

All deterministic checks passed.

## Visual QA captures (Playwright)

Route: `/login`

**Captured screenshots** (read these PNG files in the workspace — compare to references):
- `.heyeddi/audits/eval-process/single/login_375px.png` (19657 bytes)
- `.heyeddi/audits/eval-process/single/login_768px.png` (21625 bytes)
- `.heyeddi/audits/eval-process/single/login_1440px.png` (23866 bytes)

**No reference mockups** (from-scratch design) — judge captures only. Fail unstyled UI, black inputs, empty/sparse pages.

**Rendered spacing checks** (computed CSS — AUTO-FAIL if any fail):
- [ok] card body padding-top: 20.0px (expect >= 16px)
- [ok] card body padding-top: 20.0px (expect >= 16px)

**Your job:** Open the captured screenshots and reference mockups. Fail if:
- No app shell when mockup shows sidebar/top bar (flat page on gray background)
- Inputs look like solid black boxes or unstyled native fields
- No card/panel layout / wrong region hierarchy vs mockups
- Page is sparse, cramped in a corner, or missing key regions (Profile, Notifications, Save CTA)
- **Empty PrimeVue Cards** — title/subtitle only with no fields, toggles, or stat values in card body
- **Cramped spacing** — card body padding < 16px, card stack gap < 16px, or sidebar < 220px at desktop
- Captures are missing or capture errors occurred

**Do not fail** solely because primary button/toggle color differs from mockup PNG — judge colors against design.md tokens.

