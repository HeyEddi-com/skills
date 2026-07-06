
#!/usr/bin/env python3
"""Capture responsive screenshots with Playwright (optional)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Visual audit screenshots")
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--widths", default="375,768,1440")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    base_url = os.environ.get(
        "DEV_SERVER_URL",
        os.environ.get("FLUTTER_WEB_URL", "http://localhost:5173"),
    )
    out_dir = root / ".visual-audit"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        emit(
            "[skip] Playwright not installed.\n"
            "Install: pip install playwright && playwright install chromium\n"
            "Fallback: python scripts/layout_tree.py --route "
            + args.route
            + " --project-root "
            + str(root)
        )
        return

    artifacts: list[str] = []
    url = base_url.rstrip("/") + args.route
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for w in widths:
            page = browser.new_page(viewport={"width": w, "height": 900})
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as exc:
                emit(f"[warn] navigation failed for {url}: {exc}")
                browser.close()
                return
            slug = args.route.strip("/").replace("/", "_") or "home"
            path = out_dir / f"{slug}_{w}px.png"
            page.screenshot(path=str(path), full_page=True)
            artifacts.append(str(path))
            page.close()
        browser.close()

    emit(json.dumps({"route": args.route, "artifacts": artifacts}, indent=2))


if __name__ == "__main__":
    main()
