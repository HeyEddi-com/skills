# Agent Skills Architecture & Blueprint

This document outlines the standard guidelines for creating model-agnostic AI Agent Skills, followed by a specific blueprint for a Vue SPA + PrimeVue/OpenProps + FastAPI/Firebase stack.

## Part 1: General Guidelines for Creating Custom Skills

A robust, portable Agent Skill is not just a prompt; it is a mini-software package. To ensure it works well with both massive models (Gemini) and smaller, strict self-hosted models, follow these core principles:

### 1. The Triad Structure

Every skill should be housed in its own directory and contain three distinct layers:

- **The Interface** (`manifest.json` / Tool Schema): Tells the model what the tool is, what arguments it takes, and what it returns. Keep schemas flat and simple. Local models struggle with deeply nested JSON.

- **The Context** (`context/`): The markdown files containing your rules.
  - `VOCABULARY.md`: Positive instructions (e.g., "Use OpenProps variables like `var(--size-fluid-3)`").
  - `ANTI_PATTERNS.md`: Negative constraints (e.g., "NEVER use standard Tailwind classes, NEVER write raw CSS hex codes").
  - `EXAMPLES.md`: One or two perfect "Before/After" code blocks.

- **The Execution** (`scripts/`): The actual code (Node.js/Python) that runs when the model calls the tool.

### 2. Design Principles for Autonomous Execution

- **Return Errors as Text, Don't Crash**: If a script fails (e.g., a linter finds an error), the script should catch the error and return the terminal output as a string to the agent. This triggers the agent's "Critic" persona to fix the code. If the script just crashes, the agent stops.

- **Idempotency**: The agent might call a tool multiple times. Ensure your scripts don't corrupt files if run repeatedly.

- **Read-Only vs. Read-Write Tools**: Clearly separate tools that gather context (like taking a screenshot) from tools that mutate state (like running a formatter).

## Part 2: Essential Skills for Your Vue / PrimeVue / Backend Stack

Based on your preferred stack (Static Sites, Vue SPA, PrimeVue or OpenProps, FastAPI/Firebase), here are 4 specific Skills you should build.

### Skill 1: The Headless Visual Auditor (Playwright)

Solves the "Cursor Mobile View" problem and enables visual autonomy.

**Goal:** Allows the agent to visually inspect desktop, tablet, and mobile views of the Vue SPA without relying on the IDE pane.

**Context/Rules:** `VISUAL_HIERARCHY.md` (Defines what good spacing and alignment look like).

**Execution Script** (`audit-ui.ts`):

1. Uses Playwright to load `localhost:5173` (Vite dev server).
2. Takes screenshots at 375px, 768px, and 1440px widths.
3. If the agent has vision (Gemini), it returns the images. If not, it runs a script to extract the computed dimensions of key elements and returns them as a JSON layout tree.

### Skill 2: The Vue/PrimeVue Strict Scaffolder

LLMs hallucinate UI components constantly. This skill forces strict adherence to your styling system.

**Goal:** Prevent the agent from mixing arbitrary CSS with PrimeVue, or hallucinating PrimeVue props that don't exist.

**Context/Rules:**

- `PRIMEVUE_API.md`: A condensed cheat sheet of the PrimeVue components you actually use (e.g., DataTable, Dialog, Button) and their exact Vue 3 `<script setup>` syntax.
- `OPENPROPS_STRICT.md`: Banning raw CSS values and forcing the use of OpenProps (`var(--surface-1)`, `var(--font-sans)`).

**Execution Script** (`validate-vue.js`): A script that runs `vue-tsc --noEmit` and stylelint specifically configured to flag any hardcoded hex colors or padding values, returning the warnings to the agent to fix.

### Skill 3: The Backend Type Bridger

Bridging the gap between FastAPI/Firebase and the Vue SPA.

**Goal:** Ensure the frontend agent never guesses what the backend payload looks like.

**Execution Script** (FastAPI version — `sync-openapi.py`):

1. Fetches the `openapi.json` from your local FastAPI server.
2. Automatically generates/updates a `types.ts` file in the Vue project so the agent has perfect autocomplete context.

**Execution Script** (Firebase version — `fetch-firestore-schema.js`):

- Reads your Firestore rules or a predefined schema file and returns the exact data structure to the agent before it writes a Vue composable for data fetching.

### Skill 4: The Vite Static Build Validator

Because a Vue SPA that looks good in dev might fail to build statically.

**Goal:** Ensure the agent doesn't introduce SSR/Static generation bugs or unresolved imports.

**Execution Script** (`verify-build.sh`):

- Runs `npm run build` headlessly.
- If it succeeds, the agent gets a "Build Successful" message.
- If it fails, the script pipes the exact Rollup/Vite error stack trace back to the agent so it can autonomously patch the import or typing error.

## Directory Structure Example

When you assemble this, your project (or a global `.agent-skills` folder) will look like this:

```
.agent-skills/
  ├── visual-auditor/
  │   ├── manifest.json       (Tool: take_screenshots)
  │   └── scripts/
  │       └── playwright-audit.ts
  │
  ├── primevue-architect/
  │   ├── context/
  │   │   ├── PRIMEVUE_API.md
  │   │   ├── OPENPROPS_STRICT.md
  │   │   └── ANTI_PATTERNS.md
  │   └── scripts/
  │       └── lint-styles.js
  │
  └── backend-bridger/
      ├── manifest.json       (Tool: fetch_api_types)
      └── scripts/
          └── generate-types.py
```
