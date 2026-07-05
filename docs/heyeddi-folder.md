# The `.heyeddi/` folder

**Date:** 2026-07-03

Every HeyEddi client or internal app uses a **`.heyeddi/`** directory at the project root. It is the single place for product context, design artifacts, and documents that skills generate — so nothing important gets lost at repo root.

## What is HeyEddi?

**HeyEddi** is a product studio and agency: we design and ship SaaS applications (Vue or **Flutter** + FastAPI or Firebase, OpenProps + PrimeVue for web). We also publish **free, open [Cursor Agent Skills](https://github.com/heyeddi/skills)** so anyone can run the same workflows we use on client work.

Skills are installed with `npx skills add heyeddi/<name>` or `./scripts/install-skills.sh`. Invoke with `@skill-name` in Cursor.

## Folder layout

```
.heyeddi/
├── README.md          # Agency intro, free skills, how we use this folder
├── stack.json         # { "frontend": "vue"|"flutter", "backends": ["fastapi"], "api_port": 8090, "web_port": 8085 }
├── product.md         # Users, routes, acceptance criteria
├── skills-index.json  # Cached skill catalog (@skill-orchestrator)
├── skills-index.md    # Human-readable catalog table
├── design.md          # DESIGN.md format — tokens + rationale + Decision log
├── designs/
│   └── <feature>/     # Handoff PNGs, briefs, wireframes, research
├── docs/              # Skill-generated reports (ship, PR, drift, gates)
│   ├── intake/        # @product-translator — translation-*.md, skill-routing.json
│   ├── ux-flows.md    # Index of traced user tasks (@ux-flow-auditor)
│   ├── engineering/   # architecture, reuse-catalog, decisions (@engineering-excellence)
│   └── ux-flows/      # Per-task .flow.json + reports (@ux-flow-auditor)
└── audits/            # Optional visual / merge / ux-flow snapshots
    └── eval-process/  # Multi-turn eval proof (integration): manifest.json + per-step PNGs
```

## Conventions

1. **`scaffold_stack`** (via `@project-engineering` for Vue or `@flutter-engineering` for Flutter) creates `.heyeddi/` if missing, including `README.md`.
2. **`@product-translator`** (greenfield) writes `product.md`, optional mockups/briefs, and `docs/intake/skill-routing.json` before other skills.
3. **Design skills** write to `.heyeddi/design.md` and `.heyeddi/designs/` (product.md often from translator first).
4. **QA / PR skills** write reports to `.heyeddi/docs/` (e.g. `ship-report.md`, `pr-42-tracking.md`).
5. **Engineering excellence** maintains `.heyeddi/docs/engineering/` and audit reports (`engineering-audit-<date>.md`).
6. **UX flow auditor** maintains `.heyeddi/docs/ux-flows/` and index `ux-flows.md`.
7. **Skill orchestrator** writes `.heyeddi/skills-index.json` + `skills-index.md` — read these instead of every SKILL.md at session start. Refresh after skill installs.
8. **Audience-driven design** — `product.md` Personas + Per-route intent drive `@heyeddi-design`; see `docs/design-excellence.md`.
9. **Legacy paths** at repo root (`PRODUCT.md`, `DESIGN.md`, `designs/`) still work — `load_context` and `load_handoff` check `.heyeddi/` first.

## Path resolution

Shared helper: `skills/project-engineering/scripts/_heyeddi_paths.py` (copied into design skills). Scripts resolve canonical paths before falling back to legacy locations.

## Related

- [design-excellence.md](./design-excellence.md) — audience-driven design layers
- [clarify-before-act.md](./clarify-before-act.md) — when skills ask vs read `.heyeddi/`
- [team-cheat-sheet.md](./team-cheat-sheet.md)
- [eval-philosophy.md](./eval-philosophy.md)
- `skills/project-engineering/scaffold/heyeddi/README.md` — template copied into new projects
