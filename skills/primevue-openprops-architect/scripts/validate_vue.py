
#!/usr/bin/env python3
"""Run vue-tsc and stylelint if available."""
from __future__ import annotations

import argparse
import shutil

from _skill_cli import emit, resolve_project_root, run_command


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Vue + CSS")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    sections: list[str] = []

    if shutil.which("npx"):
        sections.append("## vue-tsc")
        sections.append(
            run_command(["npx", "vue-tsc", "--noEmit"], root)
            if (root / "node_modules").is_dir()
            else "[skip] node_modules not found: run npm install first"
        )
        if shutil.which("stylelint") or (root / "node_modules" / ".bin" / "stylelint").exists():
            sections.append("## stylelint")
            cmd = (
                ["npx", "stylelint", "**/*.{css,vue,scss}"]
                if (root / "node_modules").is_dir()
                else ["stylelint", "**/*.{css,vue,scss}"]
            )
            sections.append(run_command(cmd, root))
        else:
            sections.append("## stylelint\n[skip] stylelint not installed")
    else:
        sections.append("[skip] npx not found: install Node.js to run vue-tsc/stylelint")

    emit("\n\n".join(sections))


if __name__ == "__main__":
    main()
