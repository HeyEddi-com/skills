
#!/usr/bin/env python3
"""Fallback layout extractor when Playwright or vision is unavailable."""
from __future__ import annotations

import argparse
import json
import os

from _skill_cli import emit, resolve_project_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Layout tree fallback")
    parser.add_argument("--route", required=True)
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    base_url = os.environ.get("DEV_SERVER_URL", "http://localhost:5173")

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        emit(
            json.dumps(
                {
                    "route": args.route,
                    "mode": "stub",
                    "message": "Playwright not installed — returning placeholder layout tree",
                    "elements": [
                        {"tag": "body", "width": 375, "height": 800, "note": "install playwright for real data"}
                    ],
                },
                indent=2,
            )
        )
        return

    url = base_url.rstrip("/") + args.route
    tree: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 375, "height": 900})
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
            for sel in ["main", "header", "nav", "footer", "h1", "form"]:
                loc = page.locator(sel).first
                if loc.count():
                    box = loc.bounding_box()
                    if box:
                        tree.append({"selector": sel, **{k: round(v) for k, v in box.items()}})
        except Exception as exc:
            emit(f"[warn] layout extraction failed: {exc}")
        finally:
            browser.close()

    emit(json.dumps({"route": args.route, "project_root": str(root), "elements": tree}, indent=2))


if __name__ == "__main__":
    main()
