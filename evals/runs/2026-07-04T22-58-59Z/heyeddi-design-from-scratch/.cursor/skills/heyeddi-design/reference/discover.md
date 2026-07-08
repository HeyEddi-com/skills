# Discover — discovery interview

**Scope:** Understand the request deeply. No code, no wireframes, no `DESIGN.md` writes.

**Trigger:** Vague brief, first message with no sub-command, or `@heyeddi-design discover`.

## Rules

- **Do NOT** write code or make visual decisions during discovery.
- **Do NOT** dump all questions at once — natural dialogue, **2–3 questions per round**, then wait.
- Use the structured question tool when available; otherwise ask in chat and stop.
- Treat `PRODUCT.md` and `DESIGN.md` as anchors; skip questions they already answer.
- **Assert-then-confirm:** when one answer is obvious from context, state it and ask to confirm or override — don't offer four-option menus for settled choices.
- At least **one user-answer round** unless repo docs fully answer purpose, audience, personas, and scope.
- If `product.md` lacks **Personas** or **Per-route intent**, cover those in this interview (or route to `@heyeddi-intake`).

## Translate plain language

Users won't say "information architecture" or "Restrained color strategy." Map their words:

| User says | You clarify |
|-----------|-------------|
| "enterprise view" | B2B admin? density? data tables? sidebar nav? roles/permissions? |
| "clean / modern" | Anchor products/brands, not adjectives — ask for 2–3 named references |
| "like Notion / Linear / Salesforce" | What specifically — nav, density, typography, settings IA? |
| "login" / "sign in" | Apply **sign-in** archetype in `surface-completeness.md` — recovery links, remember me, SSO?, invite-only? |
| "professional" | Register (product vs brand), scene sentence (who, where, lighting, mood) |

## Interview areas

Cover what's missing from `PRODUCT.md` / `DESIGN.md` / the user's prompt:

### Purpose & context
- What is this for? What problem does it solve?
- Who uses it specifically? (role, frequency, context — not "users")
- User's state of mind when they arrive (rushed, exploring, anxious, focused)
- What does success look like?

### Content & data
- What data or content appears on this surface?
- Realistic ranges (empty, typical, max — e.g. 0 / 5 / 500 rows)
- Edge cases: empty, error, first-time, power user
- Dynamic content and update frequency

### Design direction (skip if DESIGN.md answers)
- **Color strategy:** Restrained / Committed / Full palette / Drenched
- **Theme scene sentence:** one sentence — who, where, ambient light, mood (forces light vs dark)
- **2–3 named anchor references** (specific products/brands, not "minimal")

### Scope
- **Fidelity:** sketch / mid-fi / high-fi / production-ready
- **Breadth:** one screen / flow / whole surface
- **Interactivity:** static / prototype / shipped-quality
- **Time intent:** quick exploration vs ship-ready

### Constraints & anti-goals
- Mobile/responsive requirements
- Accessibility beyond WCAG AA?
- What should this **NOT** be? Biggest risk if wrong?

## Exit

When discovery gaps are filled, either:

- User invoked **`discover` only** → summarize findings in 5–8 bullets and ask whether to continue to **`shape`** (research + explore + brief).
- User is in **`shape`** → proceed to `reference/research.md` automatically.

Do not write the final design brief until research and explore phases complete (unless user explicitly skips with "no research" / "skip images").
