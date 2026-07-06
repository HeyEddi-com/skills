---
name: visual-auditor
description: Captures responsive screenshots via Playwright when available, or extracts a layout JSON tree as fallback. Use when checking mobile/desktop layout, spacing, or comparing UI to a reference image.
disable-model-invocation: true
---


# Visual Auditor

**Designed to run as a delegated subagent** — parent skills launch via Task (`shell`). See `reference/subagents.md`.

## When to use

- Designer or QA needs proof of responsive layout (375/768/1440)
- Comparing implemented route against reference screenshots
- Playwright unavailable → use layout tree fallback

## Instructions

1. Start dev server or set `DEV_SERVER_URL` (Vue default `http://localhost:5173`) or `FLUTTER_WEB_URL` (Flutter web default `http://127.0.0.1:8085`).
2. Run `python scripts/audit_ui.py --route /path --project-root <root>`.
3. If Playwright missing, run `python scripts/layout_tree.py` for dimension JSON.
4. Review artifacts under `.visual-audit/` or returned paths.

## Env

- `DEV_SERVER_URL` — base URL for Vue/Vite SPA
- `FLUTTER_WEB_URL` — base URL for Flutter web (`flutter run -d web-server`)
- `ARTIFACT_BUCKET` — cloud: GCS upload target
