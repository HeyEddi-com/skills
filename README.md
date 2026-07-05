# HeyEddi Skills

Curated [Cursor Agent Skills](https://cursor.com/docs/context/skills) for HeyEddi product workflows — from intake and design through engineering, QA, and merge. Each skill is an **independent installable package**; this repo is the **hub** that vendors them with git subtrees and runs the agent eval suite.

**Status:** 20 skills · agent eval suite **15/15 pass** (2026-07-04) · public hub for [HeyEddi-com](https://github.com/HeyEddi-com)

## Skills catalog

| Skill | Role |
|-------|------|
| `skill-orchestrator` | Discover @skills and suggest pipelines from `skill-routing.json` |
| `product-translator` | User prompt → `product.md`, mockups, intake JSON, routing |
| `heyeddi-design` | Design from scratch — briefs, wireframes, craft (Vue) |
| `design-handoff` | Screenshot-first Vue implementation (PrimeVue + tokens) |
| `design-handoff-flutter` | Screenshot-first Flutter / Material 3 implementation |
| `primevue-openprops-architect` | PrimeVue + OpenProps guardrails for Vue/CSS edits |
| `project-engineering` | Vue + FastAPI + Firebase scaffold, deps, dev servers |
| `flutter-engineering` | Flutter + FastAPI scaffold, analyze/test, dev servers |
| `backend-type-bridger` | OpenAPI / Firestore → TypeScript types |
| `dart-type-bridger` | OpenAPI / Firestore → Dart model stubs |
| `composable-patterns` | Vue composables for FastAPI / Firebase access |
| `flutter-patterns` | Riverpod repositories — Dio + Firebase patterns |
| `engineering-excellence` | KISS/YAGNI/DRY/SOLID audits + `.heyeddi/docs/engineering/` |
| `ux-flow-auditor` | Task-flow traces — friction, click depth — `.heyeddi/docs/ux-flows/` |
| `visual-auditor` | Responsive screenshot audit (Vue or Flutter web) |
| `verify-build` | Vite static build validator |
| `pre-merge-gate` | QA merge-readiness checklist |
| `pr-review-responder` | PR review comment workflow |
| `design-system-generalizer` | Spread golden-page patterns across routes |
| `no-duplicate-ui` | Detect duplicate Vue UI |

Install any skill into your app:

```bash
npx skills add heyeddi/visual-auditor -a cursor
# or from this clone:
./scripts/install-skills.sh visual-auditor --project /path/to/your-app
./scripts/install-skills.sh --all --global
```

## Quick start (this hub)

**Requirements:** Python 3.11+, [uv](https://docs.astral.sh/uv/), Node.js 20+ (for Vue eval templates), [Cursor agent CLI](https://cursor.com) for agent evals.

```bash
git clone git@github.com:HeyEddi-com/skills.git
cd skills
uv sync --group dev --group evals

# Smoke tests (no agent API)
uv run poe test

# List agent eval cases
uv run poe eval-list

# Run one eval (keeps sandbox under evals/runs/)
uv run poe eval-design-handoff

# Full suite (~50 min; use --model auto if on usage limits)
uv run python scripts/run-evals.py --all --keep-sandbox --timeout 1500 --model auto
```

See [docs/agent-evals.md](docs/agent-evals.md) and [docs/agent-eval-results.md](docs/agent-eval-results.md) for harness details and latest results.

## Repository layout

```
.
├── skills/<name>/          # Standalone skill packages (subtree mount point)
│   ├── SKILL.md
│   ├── manifest.json
│   ├── context/
│   └── scripts/
├── evals/                  # Agent eval cases, prompts, project templates
├── docs/                   # Architecture, distribution, eval philosophy
├── scripts/                # install, test, eval, subtree push/pull
├── fixtures/               # sample-vue-app for script smoke tests
└── skills-registry.json    # Catalog metadata
```

Skills **do not** live under `.cursor/` here — that keeps them compatible with `npx skills add heyeddi/<name>` in consumer projects.

## Authoring & distribution

Each skill has its own GitHub repo; this hub syncs via **git subtrees** (not submodules):

```bash
./scripts/new-skill.sh my-skill-name
# edit skills/my-skill-name/
./scripts/push-skill-subtree.sh my-skill-name git@github.com:heyeddi/my-skill-name.git
```

| | Subtrees | Submodules |
|---|----------|------------|
| Clone | One clone, all skills in `skills/` | Requires `submodule update` |
| Publish | `push-skill-subtree.sh` → standalone repo | Push in submodule + bump ref |
| Install | `npx skills add heyeddi/name` | Same |

Details: [docs/distribution.md](docs/distribution.md)

## `.heyeddi/` in app projects

Consumer apps store product context, design assets, and skill-generated docs under `.heyeddi/`. See [docs/heyeddi-folder.md](docs/heyeddi-folder.md).

## Eval philosophy

Evals give the agent a **goal**, not a script. Each skill must run its real workflow (context → docs → assumptions → work → validate). See [docs/eval-philosophy.md](docs/eval-philosophy.md).

## Documentation

| Doc | Topic |
|-----|--------|
| [docs/skills-roadmap.md](docs/skills-roadmap.md) | Build plan |
| [docs/team-cheat-sheet.md](docs/team-cheat-sheet.md) | Designer + QA reference |
| [docs/cloud-agent-integration.md](docs/cloud-agent-integration.md) | Pydantic AI / LangChain |
| [docs/testing-skills.md](docs/testing-skills.md) | Script smoke tests |
| [docs/subagent-delegation.md](docs/subagent-delegation.md) | Task tool + cloud delegation |

## Contributing

1. Branch from `main`, keep changes focused.
2. Run `uv run poe test` before opening a PR.
3. For skill behavior changes, run the relevant `uv run poe eval-*` case or the full suite.

---

**HeyEddi-com** · Last updated: 2026-07-04
