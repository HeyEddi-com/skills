#!/usr/bin/env bash
# Test one or all skills. Wrapper for scripts/test-skills.py
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/test-skills.py" "$@"
