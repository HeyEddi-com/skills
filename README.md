# HeyEddi Skills

A curated collection of [Cursor Agent Skills](https://cursor.com/docs/context/skills), distributed as **independent installable packages** and assembled in this hub with **git subtrees**.

## Layout philosophy

| Location | Purpose |
|----------|---------|
| `skills/<name>/` | **Source of truth** — each folder is a standalone skill (same as its own GitHub repo) |
| `.cursor/rules/` | Hub authoring rules only — not skill content |
| Your app project | Skills **installed** via `npx skills add` → `.agents/skills/` or `~/.cursor/skills/` |

Skills do **not** live under `.cursor/` in this repo. That keeps them installable and matches `npx skills add heyeddi/visual-auditor`.

## Repository layout

```
.
├── skills/                     # Installable skills (subtree mount point)
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── manifest.json
│       ├── context/
│       └── scripts/
├── .cursor/rules/              # Authoring rules for this hub
├── docs/
├── scripts/
│   ├── install-skills.sh       # Install into a project or globally
│   ├── new-skill.sh
│   ├── push-skill-subtree.sh
│   └── ...
└── skills-registry.json
```

## Install skills (consumers)

```bash
# From this hub into your Vue app
./scripts/install-skills.sh visual-auditor --project /path/to/your-app

# All skills
./scripts/install-skills.sh --all --global

# Or directly
npx skills add ./skills/visual-auditor -a cursor
npx skills add heyeddi/visual-auditor -a cursor   # after published to GitHub
```

## Authoring (this hub)

```bash
./scripts/new-skill.sh my-skill-name
# edit skills/my-skill-name/
./scripts/push-skill-subtree.sh my-skill-name git@github.com:heyeddi/my-skill-name.git
```

Subtree prefix is `skills/<name>` — the standalone repo root **is** the skill folder.

## Test skills (this hub)

```bash
./scripts/test-skills.py                    # all: structure + smoke + cloud invoker
./scripts/test-skills.py design-handoff     # one skill
./scripts/test-skills.py --structure-only   # manifests only
```

Uses `fixtures/sample-vue-app/` as a fake Vue project. See [docs/testing-skills.md](docs/testing-skills.md).

## Agent evals (instructions)

```bash
./scripts/verify-agent-cli.sh
./scripts/setup-evals.sh
uv run poe test                              # smoke (no agent)
uv run poe eval-design-handoff              # agent eval + quality gate
```

See [docs/agent-evals.md](docs/agent-evals.md).

## Eval philosophy

Evals give the agent a **goal**, not a script. Each skill must run its real workflow (context → docs → questions/assumptions → work). See [docs/eval-philosophy.md](docs/eval-philosophy.md).

## `.heyeddi/` in app projects

Consumer apps keep product, design, and skill-generated docs under `.heyeddi/`. See [docs/heyeddi-folder.md](docs/heyeddi-folder.md).

## Why subtrees (not submodules)

| | Subtrees | Submodules |
|---|----------|------------|
| Clone | One clone, all skills in `skills/` | `submodule update --init` |
| Publish | `push-skill-subtree.sh` → standalone repo | Push in submodule + bump ref |
| Install | `npx skills add heyeddi/name` | Same |

## Docs

- [docs/skills-roadmap.md](docs/skills-roadmap.md) — build plan
- [docs/distribution.md](docs/distribution.md) — subtree workflow
- [docs/team-cheat-sheet.md](docs/team-cheat-sheet.md) — Designer + QA reference
- [docs/subagent-delegation.md](docs/subagent-delegation.md) — Task tool + cloud `delegate_to_skill`
- [docs/cloud-agent-integration.md](docs/cloud-agent-integration.md) — Pydantic AI / LangChain
- [docs/testing-skills.md](docs/testing-skills.md) — smoke tests (scripts)
- [docs/agent-evals.md](docs/agent-evals.md) — agent-based evals (instructions)

## Date

Last updated: 2026-07-02
