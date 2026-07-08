#!/usr/bin/env bash
# Install Python eval deps with uv (PyYAML, Playwright, Pillow, optional backends).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv not found. Install: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

DEP_GROUPS=(evals evals-quality dev)
PYDANTIC=false
CURSOR=false
HUB_TOOLS=false

usage() {
  cat >&2 <<'EOF'
Usage: setup-evals.sh [options]

Options:
  --all           evals + evals-quality + hub-tools
  --pydantic      Also sync evals-pydantic (Pydantic AI backend)
  --cursor        Also sync evals-cursor (cursor-sdk backend)
  --hub-tools     Pillow for generate-handoff-mockups.py
  --no-browsers   Skip playwright install chromium
  -h, --help

Default: uv sync --group evals --group evals-quality && playwright install chromium
EOF
  exit 1
}

INSTALL_BROWSERS=true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) DEP_GROUPS=(evals evals-quality hub-tools); HUB_TOOLS=true ;;
    --pydantic) PYDANTIC=true ;;
    --cursor) CURSOR=true ;;
    --hub-tools) HUB_TOOLS=true ;;
    --no-browsers) INSTALL_BROWSERS=false ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
  shift
done

SYNC_ARGS=()
for g in "${DEP_GROUPS[@]}"; do
  SYNC_ARGS+=(--group "$g")
done
$PYDANTIC && SYNC_ARGS+=(--group evals-pydantic)
$CURSOR && SYNC_ARGS+=(--group evals-cursor)
$HUB_TOOLS && SYNC_ARGS+=(--group hub-tools)

echo "uv sync ${SYNC_ARGS[*]}"
uv sync "${SYNC_ARGS[@]}"

if $INSTALL_BROWSERS; then
  echo "uv run playwright install chromium"
  uv run playwright install chromium
fi

echo ""
echo "Ready:"
echo "  uv run poe test              # smoke tests"
echo "  uv run poe eval-heyeddi-handoff   # agent eval"
echo "  uv run poe eval-list"
