"""Run eval via locally installed Cursor Agent CLI (`agent` binary).

Uses the headless agent already on your machine — not cursor-sdk or cloud VMs.

  agent -p --trust --force --workspace <sandbox> "<prompt>"

Streaming uses ``--output-format stream-json`` so the terminal shows tool calls and
progress while the agent works (``text`` format buffers until the run finishes).
"""
from __future__ import annotations

import json
import os
import select
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

from evals.backends.results import AgentRunResult, AgentTransientError

DEFAULT_TIMEOUT_S = 600
HEARTBEAT_INTERVAL_S = 30
# Linux ARG_MAX ~2MB but agent expands argv; keep prompt off CLI when large.
DEFAULT_PROMPT_ARG_MAX = 24_000
PROMPT_FILE_REL = ".heyeddi/_eval_agent_prompt.md"
PROMPT_FILE_INSTRUCTION = (
    "Your full instructions are in `.heyeddi/_eval_agent_prompt.md` in this workspace. "
    "Read that file first, then follow it exactly."
)
TRANSIENT_MARKERS = (
    "resource_exhausted",
    "retriableerror",
    "rate limit",
    "rate_limit",
    "too many requests",
    "429",
    "503",
    "connection",
    "reconnecting",
    "unavailable",
)


def is_transient_agent_error(message: str) -> bool:
    hay = message.lower()
    return any(marker in hay for marker in TRANSIENT_MARKERS)


def _agent_failure_message(returncode: int, stdout: str) -> str:
    tail = stdout.strip()[-1200:]
    if is_transient_agent_error(tail):
        return (
            f"Cursor agent API temporary failure (exit {returncode}): "
            "resource_exhausted / rate limit. Wait a few minutes and retry, "
            "or set EVAL_AGENT_MODEL to a different model. "
            f"Detail: {tail[-300:]}"
        )
    return f"Agent exited {returncode}" + (f": {tail[-800:]}" if tail else "")


def resolve_agent_bin() -> str:
    for candidate in (
        os.environ.get("AGENT_BIN"),
        os.environ.get("EVAL_AGENT_BIN"),
        "agent",
        "cursor-agent",
    ):
        if not candidate:
            continue
        path = shutil.which(candidate)
        if path:
            return path
    raise RuntimeError(
        f"Cursor Agent CLI not found on PATH (tried: agent, cursor-agent, AGENT_BIN). "
        "Set AGENT_BIN to the full path of your `agent` binary."
    )


def _auth_hint(stderr: str, stdout: str) -> str | None:
    combined = f"{stderr}\n{stdout}"
    if "Authentication required" in combined or "agent login" in combined:
        return "Please log in: agent login"
    return None


def _shell_command(tool_call: dict[str, Any]) -> str | None:
    shell = tool_call.get("shellToolCall")
    if not shell:
        return None
    args = shell.get("args") or {}
    cmd = args.get("command")
    if cmd:
        return str(cmd)
    return shell.get("description")


def _tool_label(tool_call: dict[str, Any]) -> str:
    if cmd := _shell_command(tool_call):
        return f"shell: {cmd}"
    for key in (
        "readToolCall",
        "editToolCall",
        "writeToolCall",
        "grepToolCall",
        "globToolCall",
        "listToolCall",
        "deleteToolCall",
    ):
        if key not in tool_call:
            continue
        inner = tool_call[key] or {}
        args = inner.get("args") or {}
        for field in ("path", "pattern", "globPattern", "command"):
            if args.get(field):
                return f"{key.replace('ToolCall', '')}: {args[field]}"
        desc = inner.get("description")
        if desc:
            return str(desc)
        return key.replace("ToolCall", "")
    return "tool"


def _tool_result_summary(tool_call: dict[str, Any]) -> str | None:
    for key, inner in tool_call.items():
        if not key.endswith("ToolCall") or not isinstance(inner, dict):
            continue
        result = inner.get("result")
        if not isinstance(result, dict):
            continue
        if success := result.get("success"):
            if isinstance(success, dict):
                exit_code = success.get("exitCode")
                if exit_code is not None:
                    return f"exit {exit_code}"
                stdout = (success.get("stdout") or "").strip()
                if stdout:
                    first = stdout.splitlines()[0]
                    return first[:120] + ("…" if len(first) > 120 else "")
            return "ok"
        if result.get("error"):
            err = result["error"]
            if isinstance(err, dict):
                return str(err.get("message") or err)[:120]
            return str(err)[:120]
    return None


def _assistant_text(message: dict[str, Any]) -> str:
    parts: list[str] = []
    for block in message.get("content") or []:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if text:
                parts.append(str(text))
    return "".join(parts)


def format_stream_event(event: dict[str, Any], *, prefix: str) -> str | None:
    """Human-readable one-liner for a stream-json event (or None to skip)."""
    kind = event.get("type")

    if kind == "system" and event.get("subtype") == "init":
        model = event.get("model") or "default"
        return f"{prefix}▶ agent started (model: {model})"

    if kind == "thinking" and event.get("subtype") == "delta":
        if os.environ.get("EVAL_AGENT_SHOW_THINKING", "").strip() not in ("1", "true", "yes"):
            return None
        text = (event.get("text") or "").strip()
        if not text:
            return None
        one_line = " ".join(text.split())
        return f"{prefix}… {one_line[:100]}{'…' if len(one_line) > 100 else ''}"

    if kind == "assistant":
        text = _assistant_text(event.get("message") or {})
        text = text.strip()
        if not text:
            return None
        one_line = " ".join(text.split())
        return f"{prefix}💬 {one_line[:200]}{'…' if len(one_line) > 200 else ''}"

    if kind == "tool_call":
        tc = event.get("tool_call") or {}
        label = _tool_label(tc)
        if event.get("subtype") == "started":
            return f"{prefix}⚙ {label}"
        if event.get("subtype") == "completed":
            summary = _tool_result_summary(tc)
            if summary:
                return f"{prefix}✓ {label} → {summary}"
            return f"{prefix}✓ {label}"
        return None

    if kind == "result":
        if event.get("is_error"):
            return f"{prefix}✗ agent error"
        secs = (event.get("duration_ms") or 0) / 1000
        return f"{prefix}■ done ({secs:.0f}s)"

    if kind == "connection":
        subtype = event.get("subtype") or "event"
        return f"{prefix}↻ connection {subtype}"

    if kind == "retry":
        attempt = event.get("attempt")
        subtype = event.get("subtype") or "event"
        if attempt is not None:
            return f"{prefix}↻ retry {subtype} (attempt {attempt})"
        return f"{prefix}↻ retry {subtype}"

    return None


def _emit(line: str, *, stream: bool) -> None:
    if stream:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()


def _parse_stream_line(
    line: str,
    *,
    prefix: str,
    stream: bool,
    chunks: list[str],
    final_result: list[str],
) -> None:
    line = line.strip()
    if not line:
        return
    chunks.append(line + "\n")
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        if stream and line:
            _emit(f"{prefix}⚠ {line}", stream=True)
        if is_transient_agent_error(line):
            chunks.append(f"TRANSIENT:{line}\n")
        return
    if not isinstance(event, dict):
        return
    if event.get("type") == "result" and event.get("result"):
        final_result[:] = [str(event["result"])]
    formatted = format_stream_event(event, prefix=prefix)
    if formatted:
        _emit(formatted, stream=stream)


def _heartbeat_loop(stop: threading.Event, start: float, prefix: str, stream: bool) -> None:
    while not stop.wait(HEARTBEAT_INTERVAL_S):
        elapsed = int(time.monotonic() - start)
        _emit(f"{prefix}… still running ({elapsed}s)", stream=stream)


def _prompt_arg_max() -> int:
    raw = os.environ.get("EVAL_AGENT_PROMPT_ARG_MAX", "").strip()
    if raw:
        try:
            return max(1024, int(raw))
        except ValueError:
            pass
    return DEFAULT_PROMPT_ARG_MAX


def _argv_prompt(prompt: str, sandbox: Path) -> list[str]:
    """Pass prompt on argv when small; otherwise write to workspace file (avoids E2BIG)."""
    encoded_len = len(prompt.encode("utf-8"))
    if encoded_len <= _prompt_arg_max():
        return [prompt]

    prompt_path = sandbox / PROMPT_FILE_REL
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")
    if os.environ.get("EVAL_AGENT_VERBOSE", "").strip() in ("1", "true", "yes"):
        sys.stderr.write(
            f"  agent: prompt {encoded_len} bytes → {PROMPT_FILE_REL} (CLI limit {_prompt_arg_max()})\n"
        )
        sys.stderr.flush()
    return [PROMPT_FILE_INSTRUCTION]


def run_local_agent_eval(
    prompt: str,
    sandbox: Path,
    *,
    model: str | None = None,
    timeout_s: int | None = None,
    stream: bool | None = None,
) -> AgentRunResult:
    agent_bin = resolve_agent_bin()
    sandbox = sandbox.resolve()
    if not sandbox.is_dir():
        raise FileNotFoundError(f"Sandbox not found: {sandbox}")

    timeout = timeout_s or int(os.environ.get("EVAL_AGENT_TIMEOUT", DEFAULT_TIMEOUT_S))
    model = model or os.environ.get("EVAL_AGENT_MODEL")

    output_format = os.environ.get("EVAL_AGENT_OUTPUT_FORMAT", "stream-json").strip().lower()
    if output_format not in ("stream-json", "text"):
        output_format = "stream-json"

    args = [
        agent_bin,
        "-p",
        "--trust",
        "--force",
        "--workspace",
        str(sandbox),
        "--output-format",
        output_format,
    ]
    if output_format == "stream-json":
        # Tool events stream; assistant messages arrive whole without this flag.
        if os.environ.get("EVAL_AGENT_PARTIAL_OUTPUT", "").strip() in ("1", "true", "yes"):
            args.append("--stream-partial-output")
    if model:
        args.extend(["--model", model])
    args.extend(_argv_prompt(prompt, sandbox))

    if stream is None:
        stream = sys.stdout.isatty() and not os.environ.get("EVAL_AGENT_QUIET")

    prefix = "  | " if stream else ""

    if stream:
        print(
            f"  agent: running (timeout {timeout}s) — streaming {output_format} below",
            flush=True,
        )

    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(sandbox),
            bufsize=1,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to start agent: {exc}") from exc

    chunks: list[str] = []
    final_result: list[str] = []
    start = time.monotonic()
    stop_heartbeat = threading.Event()
    heartbeat = None
    if stream and output_format == "stream-json":
        heartbeat = threading.Thread(
            target=_heartbeat_loop,
            args=(stop_heartbeat, start, prefix, stream),
            daemon=True,
        )
        heartbeat.start()

    try:
        assert proc.stdout is not None
        deadline = start + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                proc.kill()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                raise RuntimeError(f"Agent timed out after {timeout}s")

            ready, _, _ = select.select([proc.stdout], [], [], min(remaining, 1.0))
            if ready:
                line = proc.stdout.readline()
                if not line:
                    break
                if output_format == "stream-json":
                    _parse_stream_line(
                        line,
                        prefix=prefix,
                        stream=stream,
                        chunks=chunks,
                        final_result=final_result,
                    )
                else:
                    chunks.append(line)
                    if stream:
                        sys.stdout.write(f"{prefix}{line}")
                        sys.stdout.flush()
            elif proc.poll() is not None:
                break

        proc.wait(timeout=10)
    except subprocess.TimeoutExpired as exc:
        proc.kill()
        raise RuntimeError(f"Agent timed out after {timeout}s") from exc
    finally:
        stop_heartbeat.set()
        if heartbeat:
            heartbeat.join(timeout=1)

    stdout = "".join(chunks)
    stderr = ""
    auth = _auth_hint(stderr, stdout)
    if auth:
        raise RuntimeError(auth)

    if proc.returncode != 0:
        msg = _agent_failure_message(proc.returncode, stdout)
        if is_transient_agent_error(stdout):
            raise AgentTransientError(msg)
        raise RuntimeError(msg)

    status = "finished"
    output = (final_result[0] if final_result else stdout).strip()

    if output_format == "text" and output.startswith("{"):
        try:
            parsed = json.loads(output)
            if isinstance(parsed, dict):
                if parsed.get("is_error"):
                    raise RuntimeError(parsed.get("result") or parsed.get("error") or "Agent error")
                output = str(parsed.get("result") or parsed.get("text") or output)
                status = str(parsed.get("status") or status)
        except json.JSONDecodeError:
            pass

    return AgentRunResult(
        backend="local",
        status=status,
        output=output,
        raw={"returncode": proc.returncode, "stderr": stderr, "output_format": output_format},
    )
