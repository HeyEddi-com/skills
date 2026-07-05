#!/usr/bin/env bash
# Install skills from this hub into a Cursor project or globally via npx skills.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

usage() {
  cat >&2 <<'EOF'
Usage:
  install-skills.sh --all [--global] [--project <path>]
  install-skills.sh <skill-name> [--global] [--project <path>]

Installs from skills/<name>/ in this hub using: npx skills add <path> -a cursor

Options:
  --global          Install to ~/.cursor/skills/ (all projects)
  --project <path>  Target project directory (default: current directory)
  --copy            Pass --copy to skills CLI (no symlinks)
  -y                Skip confirmation prompts

Examples:
  ./scripts/install-skills.sh visual-auditor --global
  ./scripts/install-skills.sh --all --project ~/Projects/my-vue-app
EOF
  exit 1
}

GLOBAL=false
PROJECT="."
COPY_FLAG=()
YES_FLAG=()
SKILLS=()
ALL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) ALL=true; shift ;;
    --global) GLOBAL=true; shift ;;
    --project) PROJECT="$2"; shift 2 ;;
    --copy) COPY_FLAG=(--copy); shift ;;
    -y) YES_FLAG=(-y); shift ;;
    -h|--help) usage ;;
    *)
      validate_skill_name "$1"
      SKILLS+=("$1")
      shift
      ;;
  esac
done

if $ALL; then
  for dir in "${REPO_ROOT}/skills"/*/; do
    [[ -d "$dir" ]] || continue
    name="$(basename "$dir")"
    [[ "$name" == .* ]] && continue
    SKILLS+=("$name")
  done
fi

[[ ${#SKILLS[@]} -eq 0 ]] && usage

PROJECT="$(cd "$PROJECT" && pwd)"
GLOBAL_FLAG=()
$GLOBAL && GLOBAL_FLAG=(-g)

for name in "${SKILLS[@]}"; do
  src="${REPO_ROOT}/skills/${name}"
  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "Error: missing ${src}/SKILL.md" >&2
    exit 1
  fi
  echo "Installing ${name} from ${src} → ${PROJECT} ($($GLOBAL && echo global || echo project))..."
  (
    cd "$PROJECT"
    npx skills add "$src" -a cursor "${GLOBAL_FLAG[@]}" "${COPY_FLAG[@]}" "${YES_FLAG[@]}"
  )
done

echo "Done."
