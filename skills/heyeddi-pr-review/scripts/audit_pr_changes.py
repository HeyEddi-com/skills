#!/usr/bin/env python3
"""Engineering and test-coverage signals scoped to PR changed files."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _pr_context import TEST_MARKERS, load_context
from _skill_cli import emit, resolve_project_root

MAX_FILE_LINES = 400
ABSTRACTION_HINTS = re.compile(
    r"(Factory|Manager|Orchestrator|Abstract|Base[A-Z]\w+Service)",
    re.MULTILINE,
)


def is_test_path(path: str) -> bool:
    lower = path.lower()
    return any(marker in lower for marker in TEST_MARKERS)


def is_source_path(path: str) -> bool:
    lower = path.lower()
    if is_test_path(lower):
        return False
    return lower.endswith((".vue", ".ts", ".tsx", ".js", ".py"))


def collect_tests(root: Path) -> str:
    chunks: list[str] = []
    for pattern in ("tests/**/*.spec.ts", "tests/**/*.spec.js", "tests/**/*.test.ts", "backend/**/test_*.py"):
        for path in root.glob(pattern):
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
    return "\n".join(chunks)


def audit_file(root: Path, rel: str) -> list[dict]:
    path = root / rel
    if not path.is_file():
        return []
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    lines = text.splitlines()
    if len(lines) > MAX_FILE_LINES:
        findings.append(
            {
                "principle": "KISS",
                "severity": "warn",
                "file": rel,
                "message": f"Changed file has {len(lines)} lines (>{MAX_FILE_LINES}): consider splitting",
            }
        )
    if ABSTRACTION_HINTS.search(text):
        findings.append(
            {
                "principle": "YAGNI",
                "severity": "info",
                "file": rel,
                "message": "Abstraction naming in changed file: confirm reuse justifies it",
            }
        )
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit PR changed files for engineering signals")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--context", default=None)
    parser.add_argument("--fixture", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)

    ctx = load_context(root, args.pr, args.context, args.fixture)
    changed: list[str] = ctx.get("changed_files") or []

    source_files = [p for p in changed if is_source_path(p)]
    test_files = [p for p in changed if is_test_path(p)]

    findings: list[dict] = []
    for rel in source_files:
        findings.extend(audit_file(root, rel))

    test_corpus = collect_tests(root)
    untested: list[str] = []
    for rel in source_files:
        stem = Path(rel).stem
        if stem in {"index", "main", "App"}:
            continue
        if stem not in test_corpus and rel not in test_files:
            if rel.endswith(".vue") or "composables" in rel or "routers" in rel:
                untested.append(rel)

    if untested:
        for rel in untested:
            findings.append(
                {
                    "principle": "Testable",
                    "severity": "warn",
                    "file": rel,
                    "message": "Changed behavior file has no matching test reference in test suite",
                }
            )

    status = "fail" if any(f["severity"] == "warn" for f in findings) else "ok"
    payload = {
        "pr": args.pr,
        "status": status,
        "source_files_changed": source_files,
        "test_files_changed": test_files,
        "untested_changed": untested,
        "findings": findings,
    }
    emit(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
