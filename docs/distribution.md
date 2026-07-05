# Skill distribution with git subtrees

**Date:** 2026-07-02

## Model

```
┌─────────────────────────┐     git subtree add/pull/push     ┌──────────────────────────┐
│  skills (this hub)      │ ◄──────────────────────────────► │  my-skill-name (remote)  │
│  skills/name/           │                                   │  SKILL.md at repo root   │
└─────────────────────────┘                                   └──────────────────────────┘
                                      │
                                      │ npx skills add heyeddi/name
                                      ▼
                            ┌─────────────────────────┐
                            │  consumer Vue project   │
                            │  .agents/skills/name/   │
                            │  or ~/.cursor/skills/   │
                            └─────────────────────────┘
```

- **Standalone skill repo** — `SKILL.md` at repository root (not under `.cursor/`).
- **Collection hub** — aggregates under `skills/<name>/`.
- **Consumer project** — install via `scripts/install-skills.sh` or `npx skills add`.

## Prefix

```
skills/<skill-name>
```

## Commands

### Add a skill from a remote repository

```bash
./scripts/add-skill-subtree.sh <skill-name> <remote-url> [branch]
```

### Install into a project

```bash
./scripts/install-skills.sh <skill-name> --project /path/to/app
./scripts/install-skills.sh --all --global
```

### Push hub changes to standalone repo

```bash
./scripts/push-skill-subtree.sh <skill-name> [remote-url] [branch]
```

## Standalone repo shape (after push)

```
visual-auditor/          # GitHub repo root = skill root
├── SKILL.md
├── manifest.json
├── context/
└── scripts/
```

Compatible with `npx skills add heyeddi/visual-auditor -a cursor`.

## Registry

`skills-registry.json` lists each skill's name, remote URL, and description.
