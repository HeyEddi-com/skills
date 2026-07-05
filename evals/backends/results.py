"""Shared eval backend result types."""
from __future__ import annotations

from dataclasses import dataclass


class AgentTransientError(RuntimeError):
    """Cursor agent hit a temporary API limit or connection error — safe to retry."""


@dataclass
class AgentRunResult:
    backend: str
    status: str
    output: str
    raw: object | None = None
