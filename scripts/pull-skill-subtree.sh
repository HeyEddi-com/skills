#!/usr/bin/env bash
# Pull upstream changes for a skill subtree from its remote repository.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

usage() {
  echo "Usage: $0 <skill-name> [branch]" >&2
  echo "Remote is read from skills-registry.json." >&2
  exit 1
}

[[ $# -lt 1 || $# -gt 2 ]] && usage

NAME="$1"
BRANCH="${2:-main}"

validate_skill_name "$NAME"
require_git_repo

REMOTE="$(lookup_remote "$NAME")"
if [[ -z "$REMOTE" ]]; then
  echo "Error: no remote found for '${NAME}' in skills-registry.json" >&2
  exit 1
fi

PREFIX="$(skill_prefix "$NAME")"

echo "Pulling ${PREFIX} from ${REMOTE} (${BRANCH})..."
git -C "$REPO_ROOT" subtree pull --prefix="${PREFIX}" "$REMOTE" "$BRANCH" --squash
echo "Done."
