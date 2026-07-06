"""HeyEddi `.heyeddi/` paths."""
from __future__ import annotations

from pathlib import Path

PRODUCT_CANDIDATES = (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md", "docs/PRODUCT.md")
DESIGN_CANDIDATES = (".heyeddi/design.md", ".heyeddi/DESIGN.md", "DESIGN.md")
DESIGNS_CANDIDATES = (".heyeddi/designs", "designs")


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def intake_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "docs" / "intake"


def resolve_existing(root: Path, candidates: tuple[str, ...]) -> Path | None:
    for rel in candidates:
        p = root / rel
        if p.is_file():
            return p
    return None


def product_md(root: Path) -> Path | None:
    return resolve_existing(root, PRODUCT_CANDIDATES)


def design_md(root: Path) -> Path | None:
    return resolve_existing(root, DESIGN_CANDIDATES)


def designs_dir(root: Path) -> Path:
    for rel in DESIGNS_CANDIDATES:
        p = root / rel
        if p.is_dir():
            return p
    d = heyeddi_dir(root) / "designs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def canonical_product_path(root: Path) -> Path:
    return heyeddi_dir(root) / "product.md"
