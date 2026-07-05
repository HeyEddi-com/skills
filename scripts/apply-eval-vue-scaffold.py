#!/usr/bin/env python3
"""Apply HeyEddi Vue scaffold to eval project templates."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "project-engineering"
SCAFFOLD = SKILL / "scaffold" / "vue"
EVAL_PROJECTS = REPO / "evals" / "projects"


def apply(project_dir: Path, *, force_package: bool = False) -> None:
    subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "scaffold_vue.py"), "--project-root", str(project_dir)],
        check=True,
    )
    if force_package:
        shutil.copy2(SCAFFOLD / "package.json", project_dir / "package.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Vue scaffold to eval templates")
    parser.add_argument("project", nargs="?", help="Project dir name under evals/projects/")
    parser.add_argument("--all-vue", action="store_true", help="Upgrade all vue-* eval templates")
    args = parser.parse_args()

    targets: list[Path] = []
    if args.all_vue:
        targets = [p for p in EVAL_PROJECTS.iterdir() if p.is_dir() and p.name.startswith("vue")]
    elif args.project:
        targets = [EVAL_PROJECTS / args.project]
    else:
        parser.error("Provide project name or --all-vue")

    for t in targets:
        if not t.is_dir():
            raise SystemExit(f"Not found: {t}")
        print(f"Scaffolding {t.name}...")
        apply(t, force_package=True)
        print(f"  done: {t}")


if __name__ == "__main__":
    main()
