"""Load and validate eval case YAML."""
from __future__ import annotations

from pathlib import Path

MAX_STEPS = 7


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "Install eval deps with uv: ./scripts/setup-evals.sh"
        ) from exc
    return yaml.safe_load(path.read_text())


def _read_prompt(evals_dir: Path, prompt_file: str) -> str:
    return (evals_dir / prompt_file).read_text().strip()


def _resolve_step_prompts(evals_dir: Path, steps: list[dict]) -> None:
    for i, step in enumerate(steps):
        name = step.get("name", f"step-{i + 1}")
        if step.get("prompt_file"):
            step["prompt"] = _read_prompt(evals_dir, step["prompt_file"])
        if step.get("judge_file"):
            step["judge"] = _read_prompt(evals_dir, step["judge_file"])
        if "prompt" not in step:
            raise ValueError(f"Step {name!r} needs prompt or prompt_file")
        if not step.get("skills"):
            raise ValueError(f"Step {name!r} needs skills: [one or more skill names]")


def load_case(case_path: Path, evals_dir: Path) -> dict:
    data = load_yaml(case_path)
    data["_path"] = str(case_path)

    steps = data.get("steps") or []
    if steps:
        if len(steps) > MAX_STEPS:
            raise ValueError(
                f"Case {data.get('id', case_path.stem)} has {len(steps)} steps; max is {MAX_STEPS}"
            )
        _resolve_step_prompts(evals_dir, steps)
        data["skills"] = data.get("skills") or _union_step_skills(steps)
        return data

    prompt_file = data.get("prompt_file")
    if prompt_file:
        data["prompt"] = _read_prompt(evals_dir, prompt_file)
    elif "prompt" not in data:
        raise ValueError(f"Case {case_path} needs prompt_file, prompt, or steps")
    if data.get("judge_file"):
        data["judge"] = _read_prompt(evals_dir, data["judge_file"])
    return data


def _union_step_skills(steps: list[dict]) -> list[str]:
    seen: list[str] = []
    for step in steps:
        for name in step.get("skills", []):
            if name not in seen:
                seen.append(name)
    return seen


def case_skill_names(case: dict) -> list[str]:
    """All skills to install in sandbox (union of case + steps)."""
    names = list(case.get("skills") or [])
    for step in case.get("steps") or []:
        for name in step.get("skills", []):
            if name not in names:
                names.append(name)
    return names


def is_stepped(case: dict) -> bool:
    return bool(case.get("steps"))


def iter_turns(case: dict) -> list[dict]:
    """Each agent turn: skills, prompt, judge criteria, optional verify_commands."""
    if steps := case.get("steps"):
        return [
            {
                "name": s.get("name", f"step-{i + 1}"),
                "skills": s["skills"],
                "prompt": s["prompt"],
                "judge": s.get("judge"),
                "verify_commands": s.get("verify_commands"),
                "visual_audit": s.get("visual_audit"),
                "assertions": s.get("assertions", []),
                "agent_timeout": s.get("agent_timeout"),
            }
            for i, s in enumerate(steps)
        ]
    return [
        {
            "name": "single",
            "skills": case["skills"],
            "prompt": case["prompt"],
            "judge": case.get("judge"),
            "verify_commands": case.get("verify_commands"),
            "visual_audit": case.get("visual_audit"),
            "assertions": case.get("assertions", []),
            "agent_timeout": case.get("agent_timeout"),
        }
    ]
