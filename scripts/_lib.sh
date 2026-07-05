#!/usr/bin/env bash
# Shared helpers for skill subtree scripts.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_PREFIX="skills"
REGISTRY="${REPO_ROOT}/skills-registry.json"

skill_path() {
  local name="$1"
  echo "${REPO_ROOT}/${SKILLS_PREFIX}/${name}"
}

skill_prefix() {
  local name="$1"
  echo "${SKILLS_PREFIX}/${name}"
}

validate_skill_name() {
  local name="$1"
  if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "Error: skill name must be lowercase kebab-case (e.g. my-skill-name)" >&2
    exit 1
  fi
}

require_git_repo() {
  if ! git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    echo "Error: not a git repository. Run: git init" >&2
    exit 1
  fi
}

lookup_remote() {
  local name="$1"
  if [[ ! -f "$REGISTRY" ]]; then
    echo ""
    return
  fi
  python3 - "$name" "$REGISTRY" <<'PY' 2>/dev/null || true
import json, sys
name, path = sys.argv[1], sys.argv[2]
with open(path) as f:
    data = json.load(f)
for skill in data.get("skills", []):
    if skill.get("name") == name:
        print(skill.get("remote", ""))
        break
PY
}

register_skill() {
  local name="$1"
  local remote="$2"
  local description="${3:-}"
  python3 - "$name" "$remote" "$description" "$REGISTRY" <<'PY'
import json, sys
from pathlib import Path

name, remote, description, path = sys.argv[1:5]
p = Path(path)
data = {"skills": []}
if p.exists():
    data = json.loads(p.read_text())
skills = data.setdefault("skills", [])
for s in skills:
    if s.get("name") == name:
        s["remote"] = remote
        if description:
            s["description"] = description
        break
else:
    entry = {"name": name, "remote": remote}
    if description:
        entry["description"] = description
    skills.append(entry)
p.write_text(json.dumps(data, indent=2) + "\n")
PY
}
