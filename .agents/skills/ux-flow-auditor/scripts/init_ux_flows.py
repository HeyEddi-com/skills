#!/usr/bin/env python3
"""Scaffold `.heyeddi/docs/ux-flows.md` and example flow definition."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from _heyeddi_paths import skill_docs_dir, ux_flows_dir, ux_flows_index
from _skill_cli import emit, resolve_project_root

TODAY = date.today().isoformat()

INDEX = """# UX flows index

**Last updated:** {today}

Task-oriented flow audits — click depth, friction, ease of use. Maintained by `@ux-flow-auditor`.

| Task ID | Goal | Route | Max clicks | Last run | Report |
|---------|------|-------|------------|----------|--------|
| update-profile | Change display name and save | /settings | 4 | — | [update-profile.md](ux-flows/update-profile.md) |

## How to add a flow

1. Add a row above
2. Create `ux-flows/<task-id>.flow.json` (see `update-profile.flow.json`)
3. Run `trace_flow.py --task-id <task-id> --check`

## Metrics

- **Click depth** — interactions from landing to success
- **Friction** — failed steps, hidden controls, extra navigation
- **Pass** — within `max_clicks` and all steps succeed
"""

EXAMPLE_FLOW = {
    "task_id": "update-profile",
    "goal": "User updates display name and saves profile",
    "start_route": "/settings",
    "max_clicks": 4,
    "viewport_width": 1440,
    "steps": [
        {"action": "expect", "selector": ".settings input, .settings .p-inputtext", "label": "Profile form visible"},
        {"action": "fill", "selector": ".settings input, .settings .p-inputtext >> nth=0", "value": "Alex Rivera", "label": "Edit display name"},
        {"action": "click", "selector": ".settings__save button, .settings button:has-text('Save')", "label": "Save changes"},
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Init .heyeddi/docs/ux-flows/")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    skill_docs_dir(root).mkdir(parents=True, exist_ok=True)
    flows = ux_flows_dir(root)
    flows.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    index = ux_flows_index(root)
    if not index.is_file():
        index.write_text(INDEX.format(today=TODAY), encoding="utf-8")
        created.append(str(index.relative_to(root)))

    example = flows / "update-profile.flow.json"
    if not example.is_file():
        example.write_text(json.dumps(EXAMPLE_FLOW, indent=2) + "\n", encoding="utf-8")
        created.append(str(example.relative_to(root)))

    stub = flows / "update-profile.md"
    if not stub.is_file():
        stub.write_text(
            "# Flow: update-profile\n\nRun `trace_flow.py --task-id update-profile` to generate this report.\n",
            encoding="utf-8",
        )
        created.append(str(stub.relative_to(root)))

    emit({"ok": True, "created": created})


if __name__ == "__main__":
    main()
