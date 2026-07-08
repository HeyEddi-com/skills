# Testing skills in this hub

**Date:** 2026-07-02

Skills are **installable packages** in `skills/` — they are tested here against a **fixture project**, not by opening this repo as a Cursor app.

## Quick start

```bash
# All skills: structure + smoke + cloud invoker
./scripts/test-skills.py

# One skill
./scripts/test-skills.py heyeddi-handoff

# Structure only (no script execution)
./scripts/test-skills.py --structure-only

# List skill names
./scripts/test-skills.py --list
```

## What gets tested

| Layer | Checks |
|-------|--------|
| **structure** | `SKILL.md` frontmatter `name` matches folder; `manifest.json` valid; each tool's `script` file exists; `context/VOCABULARY.md` + `_skill_cli.py` present |
| **smoke** | Run each manifest tool against `fixtures/sample-vue-app/` with default args; output non-empty, no Python traceback |
| **cloud** | Same invocation via `scripts/cloud/invoke_skill_tool.py` (Pydantic AI / LangChain path) |

Graceful skips are **OK** — e.g. `[skip] Playwright not installed`, `gh CLI not found`. Tests fail on empty output, tracebacks, or syntax errors.

## Fixture project

`fixtures/sample-vue-app/` is a minimal workspace:

- `DESIGN.md`, `PRODUCT.md`
- `package.json` with `test` / `build` echo scripts (no `npm install` required)
- `openapi.json`, `firestore.rules`
- `designs/settings/` with `handoff.json` + PNG screenshots
- `src/views/SettingsView.vue`, duplicate-ish `UserCard` / `ProfileCard`
- `src/composables/useApi.ts`

Extend the fixture when a skill needs new file types.

## Per-skill manual checks

Some behaviour needs a **real app** or **live services** — run these in a Vue project after `install-skills.sh`:

| Skill | Manual test |
|-------|-------------|
| `primevue-openprops-architect` | `python skills/.../validate_vue.py --project-root .` after `npm install` |
| `verify-build` | Real `npm run build` on a Vite app |
| `visual-auditor` | Dev server running + `pip install playwright && playwright install chromium` |
| `heyeddi-handoff` | Attach real screenshots in Cursor `@heyeddi-handoff` |
| `heyeddi-pr-respond` | `gh auth login` + open PR number |
| `pre-merge-gate` | Full CI project with passing tests |

## Adding tests for a new skill

1. Scaffold: `./scripts/new-skill.sh my-skill`
2. Add `manifest.json` tools
3. If new fixture files needed, extend `fixtures/sample-vue-app/`
4. If default args are non-obvious, add cases in `default_args_for_tool()` in `scripts/test-skills.py`
5. Run `./scripts/test-skills.py my-skill`

## CI (suggested)

```yaml
- run: python3 scripts/test-skills.py --structure-only   # always
- run: python3 scripts/test-skills.py                   # smoke + cloud
```

Smoke tests do not require Node, Playwright, or `gh` — skips are accepted.

| Layer | Command | Agent? |
|-------|---------|--------|
| **Smoke** | `scripts/test-skills.py` | No — scripts only |
| **Agent eval** | `scripts/run-evals.py` | **Yes** — real agent on fresh project |

See [agent-evals.md](./agent-evals.md), [eval-quality-gates.md](./eval-quality-gates.md), and [evals/README.md](../evals/README.md).
- [skills/README.md](../skills/README.md)
