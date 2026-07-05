"""Run eval via Pydantic AI (mirrors Cloud Run agent shape)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INVOKE = REPO_ROOT / "scripts" / "cloud" / "invoke_skill_tool.py"


@dataclass
class AgentRunResult:
    backend: str
    status: str
    output: str
    raw: object | None = None


def _make_tools(hub_root: Path, sandbox: Path, skill_names: list[str]):
    """Build pydantic-ai tools: skill scripts + file write."""
    from pydantic_ai import RunContext, Tool

    def run_skill_tool(
        ctx: RunContext[None],
        skill_name: str,
        tool_name: str,
        args_json: str = "{}",
    ) -> str:
        skill_dir = hub_root / "skills" / skill_name
        manifest = json.loads((skill_dir / "manifest.json").read_text())
        tool_def = next((t for t in manifest.get("tools", []) if t["name"] == tool_name), None)
        if not tool_def:
            return f"[error] tool {tool_name} not in {skill_name}"
        args = json.loads(args_json)
        args.setdefault("project_root", str(sandbox))
        cmd = [
            sys.executable,
            str(INVOKE),
            "--skill-dir",
            str(skill_dir),
            "--script",
            tool_def["script"],
            "--project-root",
            str(sandbox),
            "--args-json",
            json.dumps(args),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or "") + (r.stderr or "")

    def write_file(ctx: RunContext[None], relative_path: str, content: str) -> str:
        path = (sandbox / relative_path).resolve()
        if not str(path).startswith(str(sandbox.resolve())):
            return "[error] path escapes sandbox"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return f"wrote {relative_path} ({len(content)} bytes)"

    def read_file(ctx: RunContext[None], relative_path: str) -> str:
        path = sandbox / relative_path
        if not path.is_file():
            return f"[error] not found: {relative_path}"
        return path.read_text(errors="replace")[:12000]

    def list_files(ctx: RunContext[None], relative_dir: str = ".") -> str:
        base = sandbox / relative_dir
        if not base.is_dir():
            return f"[error] not a directory: {relative_dir}"
        files = [str(p.relative_to(sandbox)) for p in sorted(base.rglob("*")) if p.is_file()][:80]
        return "\n".join(files) or "(empty)"

    return [run_skill_tool, write_file, read_file, list_files]


def run_pydantic_eval(
    system_prompt: str,
    user_prompt: str,
    hub_root: Path,
    sandbox: Path,
    skill_names: list[str],
    model: str | None = None,
) -> AgentRunResult:
    try:
        from pydantic_ai import Agent
    except ImportError as exc:
        raise RuntimeError("Install pydantic-ai: pip install pydantic-ai") from exc

    model_name = model or os.environ.get("EVAL_MODEL", "openai:gpt-4o-mini")
    tools = _make_tools(hub_root, sandbox, skill_names)
    agent = Agent(model_name, system_prompt=system_prompt, tools=tools)
    result = agent.run_sync(user_prompt)
    return AgentRunResult(
        backend="pydantic",
        status="completed",
        output=str(result.output),
        raw=result,
    )
