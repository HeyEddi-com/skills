"""Run eval via Cursor SDK (optional — for CI with CURSOR_API_KEY).

Prefer evals.backends.local_agent for day-to-day evals on a PC with `agent` installed.
"""
from __future__ import annotations

import os
from pathlib import Path

from evals.backends.results import AgentRunResult


def run_cursor_eval(prompt: str, sandbox: Path, model: str = "composer-2.5") -> AgentRunResult:
    api_key = os.environ.get("CURSOR_API_KEY")
    if not api_key:
        raise RuntimeError("CURSOR_API_KEY required for cursor backend")

    try:
        from cursor_sdk import Agent, AgentOptions, LocalAgentOptions
    except ImportError as exc:
        raise RuntimeError("Install cursor-sdk: pip install cursor-sdk") from exc

    result = Agent.prompt(
        prompt,
        AgentOptions(
            api_key=api_key,
            model=model,
            local=LocalAgentOptions(cwd=str(sandbox.resolve())),
        ),
    )
    text = getattr(result, "result", None) or str(result)
    status = getattr(result, "status", "unknown")
    return AgentRunResult(backend="cursor", status=str(status), output=str(text), raw=result)
