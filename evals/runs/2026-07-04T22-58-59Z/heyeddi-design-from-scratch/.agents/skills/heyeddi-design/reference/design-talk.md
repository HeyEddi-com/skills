# Design talk in `.heyeddi/design.md`

Both **@heyeddi-design** and **@design-handoff** document in **one file**: `.heyeddi/design.md`.

## Format reference

Study the [Superhuman DESIGN.md](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/superhuman/DESIGN.md):

- Rich YAML frontmatter + long `description` paragraph
- Body sections that **reference tokens in prose** (`{colors.ink}`, `{typography.display-lg}`)
- Named component tokens with variants (`button-primary`, `button-primary-hover`)
- **Key Characteristics** bullets in Overview
- Do's and Don'ts as prescriptive guardrails

That voice is the target. HeyEddi adds **`## Decision log`** at the end for per-route appendices.

## What goes where

| Content | Location |
|---------|----------|
| Tokens, typography scale, component definitions | YAML frontmatter + sections 1–9 |
| Living system rules, PrimeVue catalog | **Components**, **Do's and Don'ts** |
| One feature's handoff mapping, polish before/after | **Decision log** only |

## When to update

| Skill | Update sections 1–9 | Append Decision log |
|-------|-------------------|---------------------|
| `document` | Yes | Optional on seed |
| `shape` | Overview if north star set | After brief confirmed |
| `craft` | Components if new primitives | **Required** |
| `critique` | No | No (report in `.heyeddi/docs/`) |
| `polish` | Fix drift in Colors/Components | **Required** — cite critique |
| `@design-handoff` | Components/layout if new patterns | **Required** |

## Decision log entry

```markdown
### YYYY-MM-DD — <feature or route> (@heyeddi-design craft | @design-handoff)

**Context:** …

**We chose:**
- …

**Component strategy:**
- Sidebar → `AppSidebar` (custom — PrimeVue has no app shell)
- Profile section → PrimeVue `Card` + `InputText` (sufficient)
- …

**We rejected:**
- …

**Mockup → UI:** _(handoff)_ desktop/mobile **regions** → components + build path (reuse / PrimeVue / wrapper / custom). Layout only; colors from `{colors.primary}`.

**Open questions:** none
```

## Voice examples

Good (Superhuman-style):

> We went with `{colors.canvas-soft}` cards and `{rounded.md}` because the settings mockup stacks two raised panels — not full-bleed white bands. Mockup blue buttons were ignored; primary uses `{colors.primary}` from the design system.

Bad:

> Updated design.md. Used PrimeVue Card.

## What not to do

- Create a separate decision file.
- Put only hex tables in the body without role prose.
- Let Decision log replace updating **Components** when you add a new pattern.

See `document.md` for full section order.
