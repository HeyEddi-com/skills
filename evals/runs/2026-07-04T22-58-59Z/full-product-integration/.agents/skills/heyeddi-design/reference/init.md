# Init — product and design context setup

**Scope:** Strategic project context before design work. Writes `PRODUCT.md`; offers `DESIGN.md` via `document`.

**When:** Empty project, missing `PRODUCT.md`, or user invokes `@heyeddi-design init`.

## Step 1 — Load current state

Run `load_context.py`. Check for `PRODUCT.md` and `DESIGN.md` at paths returned in `search_paths`.

| State | Action |
|-------|--------|
| Neither file | Steps 2–4, then offer `document` |
| PRODUCT only | Offer `document` for DESIGN |
| Both exist | Ask what to refresh; never overwrite silently |
| PRODUCT missing Register | Add `## Register` (`product` or `brand`) |

## Step 2 — Explore codebase

Before asking questions, scan:

- README, docs, package.json (stack, PrimeVue, OpenProps usage)
- Existing Vue components, layouts, routes
- CSS variables / tokens already in use
- Brand assets (logo, favicon)

Form a **register hypothesis:**

- **Brand:** marketing pages, hero sections, campaign surfaces
- **Product:** `/app`, dashboard, settings, auth, data tables, app shell

## Step 3 — Strategic interview

If the repo or brief is sparse, interview before writing — see `discover.md` cadence (2–3 questions per round).

Minimum for PRODUCT.md:

- Register confirmation (brand vs product)
- Users and purpose
- Brand personality (3 words)
- Named references and anti-references
- Accessibility needs

**Do not ask about colors, fonts, or radii here** — those belong in `DESIGN.md` via `document`.

Write PRODUCT.md only after user confirms strategic answers.

## Step 4 — Write PRODUCT.md

```markdown
# Product

## Register

product

## Users
[Who, context, job to be done]

## Product Purpose
[What, why, success metrics]

## Brand Personality
[Voice, tone, 3-word personality]

## Anti-references
[What this must NOT look like]

## Design Principles
[3–5 strategic principles — not token-level rules]

## Accessibility & Inclusion
[WCAG level, known needs]
```

Register value is bare `product` or `brand`.

## Step 5 — DESIGN.md

Offer `@heyeddi-design document`:

- **Code exists:** scan tokens and components into DESIGN.md
- **Greenfield:** seed DESIGN.md from quick visual questions (color strategy, type direction, density)

If user skips, note they can run `document` later — **craft requires DESIGN.md** for full workflow.

## Step 6 — Wrap up

Summarize what was written and recommend next command:

- Net-new surface → `@heyeddi-design shape <brief>`
- Existing UI, no DESIGN.md → `@heyeddi-design document`
- Ready to build with brief → `@heyeddi-design craft`

If init was a blocker for another command, resume that command after init completes.
