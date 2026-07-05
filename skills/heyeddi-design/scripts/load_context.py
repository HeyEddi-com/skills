#!/usr/bin/env python3
"""Load PRODUCT.md and DESIGN.md for design sessions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _heyeddi_paths import design_md, designs_dir, product_md, skill_docs_dir
from _skill_cli import emit, resolve_project_root


def audience_readiness(product_text: str | None) -> dict[str, bool]:
    if not product_text:
        return {
            "has_personas": False,
            "has_route_intent": False,
            "has_voice_tone": False,
            "audience_ready": False,
        }
    lower = product_text.lower()
    has_personas = "## personas" in lower
    has_route = "## per-route intent" in lower or "## route intent" in lower
    has_voice = "## voice & tone" in lower or "## voice and tone" in lower
    return {
        "has_personas": has_personas,
        "has_route_intent": has_route,
        "has_voice_tone": has_voice,
        "audience_ready": has_personas and has_route,
    }


def read_md(path: Path | None, max_chars: int = 8000) -> str | None:
    if path is None or not path.is_file():
        return None
    text = path.read_text(errors="replace")
    return text[:max_chars] + ("…" if len(text) > max_chars else "")


def list_design_features(root: Path) -> list[str]:
    designs = designs_dir(root)
    if not designs.is_dir():
        return []
    return sorted(
        p.name
        for p in designs.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


def suggest_next(product_exists: bool, design_exists: bool, features: list[str], audience_ready: bool) -> str:
    if not product_exists:
        return "Run @heyeddi-design init — .heyeddi/product.md missing"
    if not audience_ready:
        return "Run @product-translator or discover — add Personas + Per-route intent to product.md"
    if not design_exists:
        return "Run @heyeddi-design document — .heyeddi/design.md missing"
    if features:
        return f"Existing design folders: {', '.join(features)} — use shape/craft with confirmed brief"
    return "Run @heyeddi-design shape <brief> for new surface planning"


def main() -> None:
    parser = argparse.ArgumentParser(description="Load design context")
    parser.add_argument("--project-root", default=None)
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    design_path = design_md(root)
    product_path = product_md(root)
    design_exists = design_path is not None
    product_exists = product_path is not None
    product_text = read_md(product_path)
    audience = audience_readiness(product_text)
    features = list_design_features(root)
    docs_dir = skill_docs_dir(root)
    emit(
        json.dumps(
            {
                "project_root": str(root),
                "heyeddi_dir": str(root / ".heyeddi"),
                "skill_docs_dir": str(docs_dir),
                "design_md_path": str(design_path) if design_path else None,
                "product_md_path": str(product_path) if product_path else None,
                "designs_dir": str(designs_dir(root)),
                "design_md": read_md(design_path),
                "product_md": product_text,
                "design_exists": design_exists,
                "product_exists": product_exists,
                "audience": audience,
                "audience_blocker": (
                    "Run @product-translator or @heyeddi-design discover — product.md needs Personas + Per-route intent"
                    if product_exists and not audience["audience_ready"]
                    else None
                ),
                "design_features": features,
                "suggested_next": suggest_next(product_exists, design_exists, features, audience["audience_ready"]),
                "convention": "Write skill artifacts to .heyeddi/docs/ and designs to .heyeddi/designs/",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
