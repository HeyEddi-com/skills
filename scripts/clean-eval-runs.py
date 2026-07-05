#!/usr/bin/env python3
"""Remove kept agent-eval sandboxes under evals/runs/."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "evals" / "runs"

sys.path.insert(0, str(REPO_ROOT))
from evals.lib.fs_utils import robust_rmtree


def list_run_dirs() -> list[Path]:
    if not RUNS_DIR.is_dir():
        return []
    return sorted(
        (p for p in RUNS_DIR.iterdir() if p.is_dir()),
        key=lambda p: p.name,
    )


def dir_size(path: Path) -> int:
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                pass
    return total


def human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.1f} {unit}" if unit != "B" else f"{num} B"
        num /= 1024
    return f"{num:.1f} GB"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete old eval sandboxes from evals/runs/<timestamp>/",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=0,
        metavar="N",
        help="Keep the N most recent run folders (default: delete all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be removed without deleting",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Do not prompt for confirmation",
    )
    while "--" in sys.argv:
        sys.argv.remove("--")
    args = parser.parse_args()

    runs = list_run_dirs()
    if not runs:
        print(f"No eval runs under {RUNS_DIR}")
        return 0

    if args.keep < 0:
        print("--keep must be >= 0", file=sys.stderr)
        return 1

    to_remove = runs[: max(0, len(runs) - args.keep)]
    if not to_remove:
        print(f"Nothing to remove ({len(runs)} run(s); keeping all with --keep {args.keep})")
        return 0

    total_bytes = sum(dir_size(p) for p in to_remove)
    print(f"Eval runs dir: {RUNS_DIR}")
    print(f"Found {len(runs)} run(s); removing {len(to_remove)} (~{human_size(total_bytes)})")
    for path in to_remove:
        cases = [c.name for c in path.iterdir() if c.is_dir()] if path.is_dir() else []
        label = ", ".join(cases) if cases else "(empty)"
        print(f"  {'[dry-run] ' if args.dry_run else ''}{path.name}  ({label})")

    if args.dry_run:
        return 0

    if not args.yes:
        answer = input("\nDelete these folders? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Cancelled.")
            return 0

    removed = 0
    for path in to_remove:
        try:
            robust_rmtree(path)
        except OSError as exc:
            print(
                f"\nFailed to remove {path}: {exc}",
                file=sys.stderr,
            )
            print(
                "Stop any Vite/dev servers using eval sandboxes under evals/runs/ and retry.",
                file=sys.stderr,
            )
            return 1
        removed += 1
    print(f"\nRemoved {removed} run folder(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
