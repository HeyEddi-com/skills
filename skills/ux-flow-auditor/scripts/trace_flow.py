#!/usr/bin/env python3
"""Trace a user task flow with Playwright; write report to `.heyeddi/docs/ux-flows/`."""
from __future__ import annotations

import argparse
import json
import os
from datetime import date
from pathlib import Path

from _heyeddi_paths import audits_dir, ux_flows_dir, ux_flows_index
from _skill_cli import emit, fail, resolve_project_root


def _load_flow(root: Path, task_id: str) -> dict:
    path = ux_flows_dir(root) / f"{task_id}.flow.json"
    if not path.is_file():
        fail(f"Flow definition missing: {path.relative_to(root)}: run init_ux_flows.py")
    return json.loads(path.read_text(encoding="utf-8"))


def _run_playwright(flow: dict, root: Path) -> dict:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        return {
            "ok": False,
            "skipped": True,
            "error": "Playwright not installed: pip install playwright && playwright install chromium",
            "click_count": 0,
            "steps": [],
        }

    base = os.environ.get("DEV_SERVER_URL", "http://localhost:5173").rstrip("/")
    route = flow.get("start_route", "/")
    url = base + route
    width = int(flow.get("viewport_width", 1440))
    steps_log: list[dict] = []
    click_count = 0
    ok = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": 900})
        try:
            page.goto(url, wait_until="networkidle", timeout=25000)
        except Exception as exc:
            browser.close()
            return {"ok": False, "error": str(exc), "click_count": 0, "steps": []}

        for index, step in enumerate(flow.get("steps") or [], start=1):
            action = step.get("action", "click")
            selector = step.get("selector", "")
            label = step.get("label") or f"Step {index}"
            row: dict = {"index": index, "label": label, "action": action, "ok": True}

            try:
                if action == "expect":
                    loc = page.locator(selector).first
                    row["ok"] = loc.count() > 0 and loc.is_visible()
                    if not row["ok"]:
                        ok = False
                elif action == "fill":
                    page.locator(selector).first.fill(step.get("value", ""))
                    click_count += 1
                elif action == "click":
                    page.locator(selector).first.click()
                    click_count += 1
                else:
                    row["ok"] = False
                    row["error"] = f"unknown action: {action}"
                    ok = False
            except Exception as exc:
                row["ok"] = False
                row["error"] = str(exc)
                ok = False

            steps_log.append(row)
            if not row["ok"]:
                break

        # Screenshot at end
        audit = audits_dir(root) / "ux-flow"
        audit.mkdir(parents=True, exist_ok=True)
        shot = audit / f"{flow.get('task_id', 'flow')}_{width}px.png"
        page.screenshot(path=str(shot), full_page=True)
        browser.close()

    max_clicks = int(flow.get("max_clicks", 99))
    within_budget = click_count <= max_clicks
    return {
        "ok": ok and within_budget,
        "click_count": click_count,
        "max_clicks": max_clicks,
        "within_budget": within_budget,
        "steps": steps_log,
        "screenshot": str(shot.relative_to(root)),
    }


def _write_report(root: Path, flow: dict, result: dict) -> Path:
    flows = ux_flows_dir(root)
    flows.mkdir(parents=True, exist_ok=True)
    task_id = flow.get("task_id", "flow")
    path = flows / f"{task_id}.md"
    today = date.today().isoformat()
    status = "PASS" if result.get("ok") else "FAIL"
    lines = [
        f"# UX flow: {task_id}",
        "",
        f"**Date:** {today}  ",
        f"**Goal:** {flow.get('goal', '')}  ",
        f"**Route:** `{flow.get('start_route', '/')}`  ",
        f"**Status:** {status}",
        "",
        "## Metrics",
        "",
        f"- **Clicks:** {result.get('click_count', 0)} / max {result.get('max_clicks', '?')}",
        f"- **Within budget:** {'yes' if result.get('within_budget') else 'no'}",
        "",
        "## Steps",
        "",
        "| # | Label | Action | OK |",
        "|---|-------|--------|-----|",
    ]
    for row in result.get("steps") or []:
        mark = "yes" if row.get("ok") else "no"
        err = f" ({row['error']})" if row.get("error") else ""
        lines.append(f"| {row['index']} | {row['label']} | {row['action']} | {mark}{err} |")

    if result.get("screenshot"):
        lines.extend(["", f"Screenshot: `{result['screenshot']}`", ""])
    if result.get("error"):
        lines.extend(["## Error", "", result["error"], ""])
    lines.extend(
        [
            "## Friction notes",
            "",
            "*(Agent fills: dead ends, extra navigation, mobile regressions.)*",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def trace_flow(root: Path, task_id: str) -> dict:
    flow = _load_flow(root, task_id)
    flow["task_id"] = task_id
    result = _run_playwright(flow, root)
    if result.get("skipped"):
        return result
    report = _write_report(root, flow, result)
    return {
        **result,
        "task_id": task_id,
        "report": str(report.relative_to(root)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Trace UX task flow")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--check", action="store_true", help="Exit 1 if flow fails budget or steps")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    result = trace_flow(root, args.task_id)
    emit(json.dumps(result, indent=2))
    if args.check and not result.get("ok"):
        fail(f"UX flow {args.task_id} failed: see {result.get('report', 'report')}")


if __name__ == "__main__":
    main()
