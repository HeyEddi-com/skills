
#!/usr/bin/env python3
"""Find duplicate or similar Vue UI files."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _skill_cli import emit, resolve_project_root

TEMPLATE_RE = re.compile(r"<template>(.*?)</template>", re.DOTALL | re.IGNORECASE)


def template_tokens(path: Path) -> set[str]:
    m = TEMPLATE_RE.search(path.read_text(errors="replace"))
    if not m:
        return set()
    return set(re.findall(r"[A-Za-z][A-Za-z0-9-]*", m.group(1)))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b) if (a | b) else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Find duplicate UI")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--min-score", type=float, default=0.55)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    vue_files = list(root.rglob("*.vue"))
    if not vue_files:
        emit(json.dumps({"duplicates": [], "hint": "no .vue files found"}, indent=2))
        return
    by_name: dict[str, list[str]] = {}
    tokens: dict[str, set[str]] = {}
    for f in vue_files:
        if "node_modules" in f.parts:
            continue
        rel = str(f.relative_to(root))
        by_name.setdefault(f.stem.lower(), []).append(rel)
        tokens[rel] = template_tokens(f)
    pairs: list[dict] = []
    for stem, paths in by_name.items():
        if len(paths) > 1:
            pairs.append({"type": "same_filename", "stem": stem, "paths": paths})
    paths_list = list(tokens.keys())
    for i, a in enumerate(paths_list):
        for b in paths_list[i + 1 :]:
            score = jaccard(tokens[a], tokens[b])
            if score >= args.min_score:
                pairs.append({"type": "template_overlap", "a": a, "b": b, "score": round(score, 2)})
    emit(json.dumps({"duplicate_count": len(pairs), "pairs": pairs[:50]}, indent=2))


if __name__ == "__main__":
    main()
