#!/usr/bin/env bash
# Scaffold a new skill under skills/<name>/ from templates/skill/ (full triad).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

usage() {
  echo "Usage: $0 <skill-name> [description]" >&2
  exit 1
}

[[ $# -lt 1 || $# -gt 2 ]] && usage

NAME="$1"
DESCRIPTION="${2:-}"

validate_skill_name "$NAME"

DEST="$(skill_path "$NAME")"
TEMPLATE="${REPO_ROOT}/templates/skill"

if [[ -d "$DEST" ]] && [[ -n "$(ls -A "$DEST" 2>/dev/null)" ]]; then
  echo "Error: skill already exists at ${DEST}" >&2
  exit 1
fi

if [[ ! -d "$TEMPLATE" ]]; then
  echo "Error: template not found at ${TEMPLATE}" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -r "${TEMPLATE}/context" "${DEST}/"
cp -r "${TEMPLATE}/scripts" "${DEST}/"
cp "${TEMPLATE}/manifest.json" "${DEST}/manifest.json"
cp "${TEMPLATE}/SKILL.md" "${DEST}/SKILL.md"
[[ -f "${TEMPLATE}/reference.md" ]] && cp "${TEMPLATE}/reference.md" "${DEST}/reference.md"

python3 - "$NAME" "$DESCRIPTION" "${DEST}" <<'PY'
import re, sys
from pathlib import Path

name, desc, dest = sys.argv[1], sys.argv[2], Path(sys.argv[3])
title = name.replace("-", " ").title()

skill_md = (dest / "SKILL.md").read_text()
skill_md = re.sub(r"^name: .*$", f"name: {name}", skill_md, count=1, flags=re.M)
if desc:
    skill_md = re.sub(r"^description: .*$", f"description: {desc}", skill_md, count=1, flags=re.M)
skill_md = re.sub(r"^# Skill Name$", f"# {title}", skill_md, count=1, flags=re.M)
(dest / "SKILL.md").write_text(skill_md)

manifest = (dest / "manifest.json").read_text()
manifest = manifest.replace('"skill-name"', f'"{name}"')
(dest / "manifest.json").write_text(manifest)
PY

echo "Created skill triad at ${SKILLS_PREFIX}/${NAME}/"
echo "Next: edit SKILL.md, manifest.json tools, and scripts/."
