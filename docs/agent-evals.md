# Agent-based skill evals

**Date:** 2026-07-15

Skill **instructions** are only validated when a real agent follows them on a fresh project. This doc complements [testing-skills.md](./testing-skills.md) (script smoke tests).

**Read [eval-philosophy.md](./eval-philosophy.md) first** — goals, per-skill process, and why prompts trust skills instead of micromanaging tools.

## Two test layers

```
scripts/test-skills.py     →  "Does the package run?"     (no agent)
scripts/run-evals.py       →  "Does the agent obey?"      (real agent)
scripts/release-gate.sh    →  "Ship-ready?" (pytest + smoke + evals)
```

## Running agent evals (local PC)

Uses your installed `agent` CLI — default backend, no SDK, no cloud VM.

Always use `set -o pipefail` and `PYTHONUNBUFFERED=1` when piping logs (so timeouts are not masked by `tee`).

```bash
./scripts/verify-agent-cli.sh
./scripts/setup-evals.sh              # uv: pyyaml + playwright + pillow + chromium
uv run python scripts/run-evals.py --dry-run --all
uv run python scripts/run-evals.py heyeddi-handoff-only

# Full suite — continues on case errors by default; judge timeout 900s
PYTHONUNBUFFERED=1 uv run poe eval-all

# Pre-release gate (required before tagging)
./scripts/release-gate.sh             # full
./scripts/release-gate.sh --quick     # pytest + smoke + orchestrator only
```

Default judge timeout is **900s** (`EVAL_JUDGE_TIMEOUT`). Use `--fail-fast` to abort the suite on the first case crash.

See [evals/README.md](../evals/README.md) for case format, backends, and adding new evals.

## CI recommendation

| Job | Command | When |
|-----|---------|------|
| smoke | `uv run poe test` + `uv run pytest tests/ -q` | Every PR |
| release gate | `./scripts/release-gate.sh` | Before every release tag |
| agent eval | `PYTHONUNBUFFERED=1 uv run poe eval-all` | Manual / nightly on your PC |
| agent eval (CI) | `python3 scripts/run-evals.py --backend cursor --all` | Optional; needs `CURSOR_API_KEY` + cursor-sdk |
| cloud parity | `python3 scripts/run-evals.py --backend pydantic --all` | Before Cloud Run deploy |

## Adding an eval for a new skill

1. Create `evals/projects/<template>/` — minimal **fresh** project (what a new repo looks like before the skill runs).
2. Write `evals/prompts/<skill-task>.md` — **specific** instruction (not vague).
3. Add `evals/cases/<skill>.yaml` with skills, template, prompt, assertions.
4. Run `python3 scripts/run-evals.py <case-id>` until assertions pass reliably.

Assertions must be **objective** — for default evals the **agentic judge** reads all changes and command output. Legacy `--deterministic` mode uses file/build checks. See [eval-quality-gates.md](./eval-quality-gates.md).

## Integration eval (full product)

`full-product-integration` runs **5 sequential turns** — how a user actually chains skills:

| Turn | User invokes | Verifies |
|------|----------------|----------|
| 1 | `@project-engineering` | scaffold, deps, theme wired |
| 2 | `@backend-type-bridger` `@composable-patterns` | types, composables, pytest |
| 3 | `@heyeddi-design` | marketing home + login + nav |
| 4 | `@heyeddi-design` | dashboard wired to API |
| 5 | `@heyeddi-handoff` `@project-engineering` | settings + build/test ship check |

Each turn must pass its gate before the next agent run starts.

```bash
uv run poe eval-integration    # 20+ min; --timeout 1200
```

`heyeddi-handoff-only` is the dedicated `@heyeddi-handoff` case (pre-scaffolded template). Combined scaffold+handoff lives in `eval-integration`.

Single-shot cases remain for narrow skills (e.g. `primevue-fix-violations`).
