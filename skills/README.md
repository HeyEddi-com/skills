# Installable skills

Each subdirectory here is a **standalone, distributable skill** — the same layout as an independent GitHub repo after `git subtree push`.

```
skills/
  visual-auditor/
    SKILL.md
    manifest.json
    context/
    scripts/
```

## Install into a Vue / Cursor project

From this hub:

```bash
# One skill
./scripts/install-skills.sh visual-auditor --project /path/to/your-app

# All skills
./scripts/install-skills.sh --all --project /path/to/your-app

# Global (every project)
./scripts/install-skills.sh design-handoff --global
```

Or directly with the skills CLI:

```bash
npx skills add /path/to/heyeddi/skills/visual-auditor -a cursor
npx skills add heyeddi/visual-auditor -a cursor   # after subtree push to GitHub
```

Skills install to `.agents/skills/` or `~/.cursor/skills/` — Cursor loads both.

## Publish a skill to its own repo

```bash
./scripts/push-skill-subtree.sh visual-auditor git@github.com:heyeddi/visual-auditor.git
```

The standalone repo root **is** the skill folder (not nested under `.cursor/`).

## Authoring

- New skill: `./scripts/new-skill.sh my-skill`
- Regenerate all: `python3 scripts/bootstrap-all-skills.py`
- Hub rules only: `.cursor/rules/` (not skill content)
