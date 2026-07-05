#!/usr/bin/env bash
# Add a skill repository as a git subtree under skills/<name>/.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

usage() {
  echo "Usage: $0 <skill-name> <remote-url> [branch]" >&2
  echo "Example: $0 visual-auditor git@github.com:heyeddi/visual-auditor.git main" >&2
  exit 1
}

[[ $# -lt 2 || $# -gt 3 ]] && usage

NAME="$1"
REMOTE="$2"
BRANCH="${3:-main}"

validate_skill_name "$NAME"
require_git_repo

DEST="$(skill_path "$NAME")"
PREFIX="$(skill_prefix "$NAME")"

if [[ -d "$DEST" && "$(ls -A "$DEST" 2>/dev/null)" ]]; then
  echo "Error: ${DEST} already exists and is not empty." >&2
  echo "Remove it first or use a different name." >&2
  exit 1
fi

echo "Adding subtree ${PREFIX} from ${REMOTE} (${BRANCH})..."
git -C "$REPO_ROOT" subtree add --prefix="${PREFIX}" "$REMOTE" "$BRANCH" --squash

register_skill "$NAME" "$REMOTE"
echo "Registered ${NAME} in skills-registry.json"
echo "Done."
