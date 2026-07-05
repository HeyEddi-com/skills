#!/usr/bin/env bash
# Verify local Cursor Agent CLI is on PATH and can run headless evals.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

AGENT_BIN="${AGENT_BIN:-${EVAL_AGENT_BIN:-agent}}"

if ! command -v "${AGENT_BIN}" >/dev/null 2>&1; then
  echo "ERROR: '${AGENT_BIN}' not on PATH. Set AGENT_BIN to your agent binary path." >&2
  exit 1
fi

RESOLVED="$(command -v "${AGENT_BIN}")"
VERSION="$("${AGENT_BIN}" --version 2>&1 || true)"
echo "OK  agent: ${RESOLVED} (${VERSION})"

TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

OUT="$("${AGENT_BIN}" -p --trust --workspace "${TMP}" --output-format text "Reply with exactly: EVAL_OK" 2>&1)" || {
  if echo "${OUT}" | grep -q "Authentication required"; then
    echo "Please log in: agent login" >&2
    exit 1
  fi
  echo "${OUT}" >&2
  exit 1
}

echo "OK  logged in"
echo ""
echo "Run evals:"
echo "  uv run poe eval-design-handoff"
