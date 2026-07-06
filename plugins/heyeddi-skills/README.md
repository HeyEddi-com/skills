# HeyEddi Skills (Cursor plugin)

Cursor Marketplace bundle for all 21 HeyEddi agent skills. Skill sources are symlinked from `skills/` at the repo root (single source of truth).

## Install via CLI (consumers)

```bash
npx skills add HeyEddi-com/skills -a cursor -y --skill '*'
```

## Install via Cursor

- **Team Marketplace:** Settings → Plugins → Team Marketplaces → Import `https://github.com/HeyEddi-com/skills`
- **Public Marketplace:** [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish)

## Components

21 skills under `skills/` — see [skills-registry.json](../../skills-registry.json) and the [hub README](../../README.md).
