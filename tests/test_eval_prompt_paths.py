"""Validate eval case YAML prompt/judge file paths exist."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALS_DIR = REPO_ROOT / "evals"
CASES_DIR = EVALS_DIR / "cases"


def _collect_prompt_paths(data: dict) -> list[str]:
    paths: list[str] = []
    for key in ("prompt_file", "judge_file"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            paths.append(value.strip())
    for step in data.get("steps") or []:
        if not isinstance(step, dict):
            continue
        for key in ("prompt_file", "judge_file"):
            value = step.get(key)
            if isinstance(value, str) and value.strip():
                paths.append(value.strip())
    return paths


def test_eval_case_prompt_files_exist() -> None:
    missing: list[str] = []
    for case_path in sorted(CASES_DIR.glob("*.yaml")):
        data = yaml.safe_load(case_path.read_text(encoding="utf-8")) or {}
        for rel in _collect_prompt_paths(data):
            full = EVALS_DIR / rel
            if not full.is_file():
                missing.append(f"{case_path.name}: {rel}")
    assert not missing, "Missing eval prompt/judge files:\n" + "\n".join(missing)
