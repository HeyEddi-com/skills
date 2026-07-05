#!/usr/bin/env bash
# Push local subtree changes to a skill's standalone repository.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

usage() {
  echo "Usage: $0 <skill-name> [remote-url] [branch]" >&2
  echo "If remote-url is omitted, reads from skills-registry.json." >&2
  echo "Example: $0 visual-auditor git@github.com:heyeddi/visual-auditor.git main" >&2
  exit 1
}

[[ $# -lt 1 || $# -gt 3 ]] && usage

NAME="$1"
REMOTE="${2:-}"
BRANCH="${3:-main}"

validate_skill_name "$NAME"
require_git_repo

if [[ -z "$REMOTE" ]]; then
  REMOTE="$(lookup_remote "$NAME")"
fi

if [[ -z "$REMOTE" ]]; then
  echo "Error: remote URL required (not in skills-registry.json for '${NAME}')" >&2
  exit 1
fi

PREFIX="$(skill_prefix "$NAME")"
DEST="$(skill_path "$NAME")"

if [[ ! -d "$DEST" ]]; then
  echo "Error: skill not found at ${DEST}" >&2
  exit 1
fi

register_skill "$NAME" "$REMOTE"

echo "Pushing ${PREFIX} to ${REMOTE} (${BRANCH})..."

if git -C "$REPO_ROOT" subtree push --prefix="${PREFIX}" "$REMOTE" "$BRANCH" 2>/dev/null; then
  echo "Done."
  exit 0
fi

# First push to a new empty remote: split and push the branch.
SPLIT_BRANCH="subtree-split-${NAME}"
echo "Subtree push failed or remote is new — splitting branch ${SPLIT_BRANCH}..."

git -C "$REPO_ROOT" branch -D "$SPLIT_BRANCH" 2>/dev/null || true
git -C "$REPO_ROOT" subtree split --prefix="${PREFIX}" -b "$SPLIT_BRANCH"
git -C "$REPO_ROOT" push "$REMOTE" "${SPLIT_BRANCH}:${BRANCH}"
git -C "$REPO_ROOT" branch -D "$SPLIT_BRANCH"

echo "Done (initial split push)."
