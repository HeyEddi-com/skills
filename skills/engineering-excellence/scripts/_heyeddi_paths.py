"""HeyEddi `.heyeddi/` path helpers: engineering docs live under `.heyeddi/docs/`."""
from __future__ import annotations

from pathlib import Path


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def skill_docs_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "docs"


def engineering_docs_dir(root: Path) -> Path:
    return skill_docs_dir(root) / "engineering"


def audits_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "audits"


def product_md(root: Path) -> Path | None:
    for rel in (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md"):
        p = root / rel
        if p.is_file():
            return p
    return None
