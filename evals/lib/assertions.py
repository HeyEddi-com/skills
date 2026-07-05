"""Post-agent assertions on eval sandboxes."""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.lib import quality_gate as qg


@dataclass
class AssertionResult:
    name: str
    ok: bool
    detail: str


def _resolve_path(project_root: Path, rel: str) -> Path:
    return (project_root / rel).resolve()


def _allow_skip(spec: dict[str, Any], detail: str) -> bool:
    return bool(spec.get("allow_skip")) and ("[skip]" in detail or detail.startswith("skip:"))


def check_assertion(
    project_root: Path,
    hub_root: Path,
    spec: dict[str, Any],
    index: int,
) -> AssertionResult:
    atype = spec.get("type", "")
    name = spec.get("name", f"assertion-{index}")

    if atype == "file_exists":
        path = _resolve_path(project_root, spec["path"])
        ok = path.is_file()
        return AssertionResult(name, ok, f"{'found' if ok else 'missing'}: {path}")

    if atype == "any_file_exists":
        candidates = spec.get("paths", [])
        for rel in candidates:
            path = _resolve_path(project_root, rel)
            if path.is_file():
                return AssertionResult(name, True, f"found: {path.relative_to(project_root)}")
        return AssertionResult(name, False, f"none found: {candidates}")

    if atype == "file_not_exists":
        path = _resolve_path(project_root, spec["path"])
        ok = not path.is_file()
        return AssertionResult(name, ok, f"{'absent' if ok else 'still exists'}: {path}")

    if atype == "file_contains":
        path = _resolve_path(project_root, spec["path"])
        if not path.is_file():
            return AssertionResult(name, False, f"missing file: {path}")
        text = path.read_text(errors="replace")
        pattern = spec["pattern"]
        found = re.search(pattern, text, re.MULTILINE) is not None
        negate = spec.get("negate", False)
        ok = (not found) if negate else found
        return AssertionResult(name, ok, f"pattern={pattern!r} in {spec['path']}")

    if atype == "json_stdout":
        cmd = [
            str(c).replace("{project_root}", str(project_root)).replace("{hub_root}", str(hub_root))
            for c in spec["cmd"]
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        output = (result.stdout or "") + (result.stderr or "")
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return AssertionResult(name, False, f"stdout not JSON: {output[:200]}")
        for key, expected in spec.get("json_equals", {}).items():
            if data.get(key) != expected:
                return AssertionResult(name, False, f"{key}={data.get(key)!r} want {expected!r}")
        return AssertionResult(name, True, "json checks passed")

    if atype == "command":
        cmd = [
            str(c).replace("{project_root}", str(project_root))
            .replace("{hub_root}", str(hub_root))
            for c in spec["cmd"]
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        output = (result.stdout or "") + (result.stderr or "")
        if spec.get("expect_exit_zero", True) and result.returncode != 0:
            if spec.get("allow_skip") and "[skip]" in output:
                return AssertionResult(name, True, "skipped (allowed)")
            return AssertionResult(name, False, f"exit {result.returncode}: {output[:200]}")
        for fragment in spec.get("expect_stdout_contains", []):
            if fragment not in output:
                return AssertionResult(name, False, f"missing fragment {fragment!r} in output")
        return AssertionResult(name, True, output.splitlines()[0][:120] if output else "ok")

    # --- Quality gate assertions (build, test, deps, visual) ---

    if atype == "ensure_deps":
        ok, detail = qg.ensure_node_deps(project_root)
        if not ok:
            return AssertionResult(name, False, detail)
        return AssertionResult(name, True, detail)

    if atype == "npm_build":
        ok, detail = qg.npm_build(project_root)
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "npm_test":
        ok, detail = qg.npm_test(project_root)
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "pytest":
        ok, detail = qg.pytest_backend(project_root)
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "audit_dependencies":
        ok, detail = qg.audit_dependencies(
            project_root,
            max_major_behind=int(spec.get("max_major_behind", 1)),
        )
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "feature_test_exists":
        ok, detail = qg.feature_test_exists(project_root, spec["vue_path"])
        return AssertionResult(name, ok, detail)

    if atype == "page_loads":
        ok, detail = qg.page_loads(
            project_root,
            spec["route"],
            must_contain=spec.get("must_contain"),
            selectors=spec.get("selectors"),
        )
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "ui_rendered":
        ok, detail = qg.ui_rendered(
            project_root,
            spec["route"],
            primevue_selectors=spec.get("primevue_selectors"),
            min_width=int(spec.get("min_width", 120)),
            min_height=int(spec.get("min_height", 24)),
        )
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "page_not_blank":
        ok, detail = qg.screenshot_not_blank(project_root, spec["route"])
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    if atype == "visual_similarity":
        ref = _resolve_path(project_root, spec["reference"])
        if not ref.is_file():
            ref = hub_root / spec["reference"]
        ok, detail = qg.visual_similarity(
            project_root,
            spec["route"],
            ref,
            min_similarity=float(spec.get("min_similarity", 0.12)),
            min_content_ratio=spec.get("min_content_ratio"),
            ref_content_fraction=float(spec.get("ref_content_fraction", 0.35)),
        )
        if not ok and _allow_skip(spec, detail):
            return AssertionResult(name, True, f"skipped: {detail}")
        return AssertionResult(name, ok, detail)

    return AssertionResult(name, False, f"unknown assertion type: {atype}")


def run_assertions(
    project_root: Path,
    hub_root: Path,
    specs: list[dict[str, Any]],
    *,
    verbose: bool = True,
) -> list[AssertionResult]:
    results: list[AssertionResult] = []
    for i, spec in enumerate(specs):
        name = spec.get("name", f"assertion-{i}")
        atype = spec.get("type", "")
        if verbose:
            print(f"  check: {name} ({atype})...", flush=True)
        ar = check_assertion(project_root, hub_root, spec, i)
        results.append(ar)
        if verbose:
            mark = "PASS" if ar.ok else "FAIL"
            print(f"  [{mark}] {ar.name}: {ar.detail}", flush=True)
    return results
