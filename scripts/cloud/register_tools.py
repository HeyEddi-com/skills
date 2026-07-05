#!/usr/bin/env python3
"""List all tools from skill manifests for Pydantic AI / LangChain registration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_skills import load_all_skills


def register_tools(hub_root: Path) -> list[dict]:
    tools: list[dict] = []
    for skill in load_all_skills(hub_root):
        skill_dir = skill["path"]
        for tool in skill["manifest"].get("tools", []):
            tools.append(
                {
                    "skill": skill["name"],
                    "skill_dir": skill_dir,
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "readonly": tool.get("readonly", True),
                    "script": tool.get("script", ""),
                    "parameters": tool.get("parameters", {}),
                }
            )
    return tools


if __name__ == "__main__":
    hub = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(json.dumps(register_tools(hub), indent=2))
