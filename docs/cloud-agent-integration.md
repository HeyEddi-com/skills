# Cloud Agent Integration (Pydantic AI / LangChain)

**Date:** 2026-07-02  
**Status:** Phase 0 — specification  
**Runtime:** Google Cloud Run + Pydantic AI (primary) + LangChain (secondary)

HeyEddi skills must behave identically whether the agent runs in **Cursor** (local shell) or on **Cloud Run** (containerized). This doc defines the integration contract.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Cloud Run service                                          │
│  ┌─────────────┐    ┌──────────────────┐    ┌───────────┐ │
│  │ Skill       │───►│ Tool registry    │───►│ Script    │ │
│  │ loader      │    │ (manifest.json)  │    │ invoker   │ │
│  └─────────────┘    └──────────────────┘    └─────┬─────┘ │
│         │                    ▲                     │        │
│         ▼                    │                     ▼        │
│  ┌─────────────┐    ┌────────┴─────────┐    ┌───────────┐ │
│  │ SKILL.md +  │    │ Pydantic AI      │    │ scripts/  │ │
│  │ context/    │    │ @agent.tool      │    │ *.py      │ │
│  └─────────────┘    │ LangChain Tool   │    └───────────┘ │
│                     └──────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
         ▲
         │ skills-registry.json + cloned workspace
         │
┌────────┴────────┐
│ GitHub repos    │
│ (per-skill +    │
│  app projects)  │
└─────────────────┘
```

---

## Skill loader

At container startup (or per-request with cache):

1. Read `skills-registry.json` (or env `ENABLED_SKILLS=visual-auditor,design-handoff`).
2. For each skill, load:
   - `SKILL.md` body → system / skill context block
   - `context/*.md` → on-demand via skill instructions
   - `manifest.json` → register tools

**Skill selection (mirrors Cursor “Agent Decides”):**

- Include all skill `name` + `description` in a routing preamble.
- Pydantic AI: optional classifier step or tool-less turn that picks skills before execution.
- Skills with `disable-model-invocation: true` in frontmatter → **never** auto-load; only when user/session explicitly requests.

---

## manifest.json contract

Keep schemas **flat** (single level of properties). Local and smaller models parse these more reliably.

```json
{
  "skill": "visual-auditor",
  "version": "1.0.0",
  "tools": [
    {
      "name": "capture_screenshots",
      "description": "Capture responsive screenshots of a Vue app route.",
      "readonly": true,
      "script": "scripts/audit_ui.py",
      "parameters": {
        "type": "object",
        "properties": {
          "route": { "type": "string" },
          "project_root": { "type": "string" },
          "dev_server_url": { "type": "string" },
          "widths": { "type": "array", "items": { "type": "integer" } }
        },
        "required": ["route", "project_root"]
      }
    }
  ]
}
```

| Field | Purpose |
|-------|---------|
| `readonly` | `true` = audit/context tools; `false` = may mutate workspace (use sparingly on cloud) |
| `script` | Path relative to skill root |
| `parameters` | JSON Schema object — maps to Pydantic model / LangChain args |

---

## Script invoker (shared)

All tools call one invoker:

```python
# Pseudocode — implement in scripts/cloud/invoke_skill_tool.py

def invoke_skill_tool(
    skill_dir: Path,
    script: str,
    args: dict[str, Any],
    *,
    project_root: Path,
    timeout: int = 300,
) -> str:
    """Run script; return stdout+stderr as text. Never raise on non-zero exit."""
    cmd = build_cli_command(skill_dir / script, args, project_root)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        output = f"[exit {result.returncode}]\n{output}"
    return output.strip() or "(no output)"
```

**Rules:**

- Scripts accept `--key value` or JSON via stdin — pick one convention per skill, document in `scripts/README.md`.
- Exit `0` on success; non-zero with human-readable errors otherwise.
- **Idempotent** — same args → same result.

---

## Pydantic AI registration

```python
# Pseudocode

from pydantic_ai import Agent

def register_skill_tools(agent: Agent, skills: list[SkillPackage]) -> None:
    for skill in skills:
        for tool_def in skill.manifest["tools"]:
            fn = make_tool_fn(skill.path, tool_def)
            agent.tool(name=tool_def["name"], description=tool_def["description"])(fn)
```

Each `fn` validates args with a Pydantic model generated from `parameters`, then calls `invoke_skill_tool`.

**Context injection:** Prepend loaded `SKILL.md` (minus frontmatter) to agent instructions when that skill is active for the session.

---

## LangChain registration

```python
# Pseudocode

from langchain_core.tools import StructuredTool

def to_langchain_tools(skill: SkillPackage) -> list[StructuredTool]:
    tools = []
    for tool_def in skill.manifest["tools"]:
        tools.append(StructuredTool.from_function(
            coroutine=make_async_invoker(skill, tool_def),
            name=tool_def["name"],
            description=tool_def["description"],
            args_schema=pydantic_model_from_schema(tool_def["parameters"]),
        ))
    return tools
```

Use the **same** `invoke_skill_tool` underneath — one script, two frameworks.

---

## Environment variables (Cloud Run)

| Variable | Purpose |
|----------|---------|
| `PROJECT_ROOT` | Mounted workspace or clone path |
| `DEV_SERVER_URL` | e.g. `http://127.0.0.1:5173` (sidecar or pre-started) |
| `ARTIFACT_BUCKET` | GCS bucket for screenshots / reports |
| `GH_TOKEN` | PR review skill (Secret Manager) |
| `ENABLED_SKILLS` | Comma-separated skill names |
| `OPENAPI_URL` | FastAPI schema URL for type bridger |
| `FIREBASE_SCHEMA_PATH` | Path to Firestore rules/schema export |

---

## Workspace model

Cloud Run jobs typically:

1. Clone app repo (or receive tarball) into `/workspace`.
2. Optionally start Vite dev server sidecar for `visual-auditor` / `design-handoff`.
3. Run agent with `PROJECT_ROOT=/workspace`.
4. Upload artifacts to GCS; return signed URLs in tool responses.

**Read-only tools** preferred on cloud — agent edits files via separate git/PR flow, not blind shell on production mounts.

---

## Python vs Node scripts

| Prefer Python when | Keep Node when |
|--------------------|----------------|
| Skill runs on Cloud Run | Tool is Vue/npm-specific and no Python equivalent |
| Playwright audit | `vue-tsc` / stylelint via subprocess wrapper OK |

Pattern: thin Python wrapper shells to `npm run` / `npx` when needed:

```python
subprocess.run(["npm", "run", "build"], cwd=project_root, ...)
```

---

## Normalized handoff brief

`design-handoff` and future Penpot adapter produce the same JSON shape:

```json
{
  "screen": "settings",
  "route": "/settings",
  "mode": "screenshot",
  "frames": [
    { "name": "desktop", "path": "designs/settings/desktop.png", "width": 1440 },
    { "name": "mobile", "path": "designs/settings/mobile.png", "width": 375 }
  ],
  "notes": ["Reuse SettingsSection"],
  "design_context": { "design_md": "...", "product_md": "..." }
}
```

Future `mode: "penpot"` adds `penpot_file_id`, `frame_id` — workflow after `load_handoff` unchanged.

---

## Subagent delegation (mirrors Cursor Task)

Skills define default delegation in `reference/subagents.md`. Cursor uses the **Task** tool today; Cloud Run uses the same prompt shape:

```python
async def delegate_to_skill(
    skill: str,
    phase: str,
    subagent_type: str,  # explore | shell | generalPurpose | …
    prompt: str,
    project_root: Path,
    *,
    readonly: bool = False,
) -> str:
    """Child agent run: scoped SKILL.md slice + phase tools only."""
    ...
```

Orchestrator parent agent calls this between phases (e.g. design-handoff interpret → verify gate → implement). See [subagent-delegation.md](./subagent-delegation.md).

---

## Phase 0 deliverables

- [ ] `scripts/cloud/invoke_skill_tool.py`
- [ ] `scripts/cloud/register_tools.py`
- [ ] `scripts/cloud/load_skills.py`
- [ ] Example Pydantic AI agent snippet in this doc (append when implemented)
- [ ] Integration test: one skill, one tool, mock workspace

---

## Related

- [subagent-delegation.md](./subagent-delegation.md) — Task tool + cloud delegation
- [skills-roadmap.md](./skills-roadmap.md) — full build plan
- [skill-guides.md](./skill-guides.md) — triad structure
