#!/usr/bin/env bash
# Static skill security scan for CI / release gate.
#
# Tooling choice (no duplication):
#   1. skill-trust lint  — primary gate (schema + static security; no LLM keys)
#   2. skills-check audit — secondary gate, fail only on high/critical
#      (injection/command patterns). Skip skills-check lint (noisy metadata)
#      and --include-registry-audits (skills.sh API needs published coords;
#      platform audits refresh after release, not local hub folders).
#
# Usage:
#   ./scripts/skill-security-scan.sh
#   ./scripts/skill-security-scan.sh --trust-only
#   npm run skill-security
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

TRUST_ONLY=false
for arg in "$@"; do
  case "$arg" in
    --trust-only) TRUST_ONLY=true ;;
    -h|--help)
      sed -n '2,16p' "$0"
      exit 0
      ;;
  esac
done

resolve_bin() {
  local name="$1"
  if [[ -x "${REPO_ROOT}/node_modules/.bin/${name}" ]]; then
    echo "${REPO_ROOT}/node_modules/.bin/${name}"
    return
  fi
  if command -v "$name" >/dev/null 2>&1; then
    command -v "$name"
    return
  fi
  return 1
}

ensure_deps() {
  if [[ ! -x "${REPO_ROOT}/node_modules/.bin/skill-trust" ]]; then
    echo "==> npm install (skill-trust / skills-check)"
    npm install --no-fund --no-audit
  fi
}

ensure_deps

SKILL_TRUST="$(resolve_bin skill-trust)"
SKILLS_CHECK="$(resolve_bin skills-check || true)"

echo "==> skill-trust lint (primary)"
failed=0
shopt -s nullglob
for skill_dir in "${REPO_ROOT}/skills"/*/; do
  name="$(basename "$skill_dir")"
  if [[ ! -f "${skill_dir}/SKILL.md" ]]; then
    continue
  fi
  if ! "${SKILL_TRUST}" lint "$skill_dir" --format pretty; then
    echo "FAIL skill-trust: ${name}"
    failed=$((failed + 1))
  fi
done
shopt -u nullglob

if [[ "$failed" -gt 0 ]]; then
  echo "skill-trust lint failed for ${failed} skill(s)"
  exit 1
fi
echo "skill-trust lint: all skills passed"

if $TRUST_ONLY; then
  echo "Skipping skills-check (--trust-only)"
  exit 0
fi

if [[ -z "${SKILLS_CHECK}" ]]; then
  echo "WARN: skills-check not installed — skip secondary audit"
  exit 0
fi

echo "==> skills-check audit (secondary; fail-on high)"
# --skip-urls: avoid flaky network. --no-isolation: CI runners vary.
# Registry audits intentionally omitted — see script header.
"${SKILLS_CHECK}" audit "${REPO_ROOT}/skills" \
  --no-isolation \
  --skip-urls \
  --fail-on high \
  --format terminal

echo
echo "Skill security scan PASSED."
