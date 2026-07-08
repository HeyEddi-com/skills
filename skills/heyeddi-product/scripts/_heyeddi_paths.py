"""HeyEddi `.heyeddi/` path helpers — product docs under `.heyeddi/docs/product/`."""
from __future__ import annotations

from pathlib import Path


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def skill_docs_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "docs"


def product_docs_dir(root: Path) -> Path:
    return skill_docs_dir(root) / "product"


def features_dir(root: Path) -> Path:
    return product_docs_dir(root) / "features"


def intake_dir(root: Path) -> Path:
    return skill_docs_dir(root) / "intake"


def product_md(root: Path) -> Path | None:
    for rel in (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md"):
        p = root / rel
        if p.is_file():
            return p
    return None


def product_json(root: Path) -> Path | None:
    p = intake_dir(root) / "product-translation.json"
    return p if p.is_file() else None


def routing_json(root: Path) -> Path | None:
    p = intake_dir(root) / "skill-routing.json"
    return p if p.is_file() else None
