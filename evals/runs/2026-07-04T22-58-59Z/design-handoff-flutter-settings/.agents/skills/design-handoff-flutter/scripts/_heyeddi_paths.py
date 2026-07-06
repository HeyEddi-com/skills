"""HeyEddi `.heyeddi/` paths — shared with design-handoff."""
from __future__ import annotations

from pathlib import Path

PRODUCT_CANDIDATES = (
    ".heyeddi/product.md",
    ".heyeddi/PRODUCT.md",
    "PRODUCT.md",
)

DESIGN_CANDIDATES = (
    ".heyeddi/design.md",
    ".heyeddi/DESIGN.md",
    "DESIGN.md",
)

DESIGNS_CANDIDATES = (".heyeddi/designs", "designs")


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def resolve_existing(root: Path, candidates: tuple[str, ...]) -> Path | None:
    for rel in candidates:
        p = root / rel
        if p.is_file():
            return p
    return None


def resolve_dir(root: Path, candidates: tuple[str, ...], *, mkdir_name: str) -> Path:
    for rel in candidates:
        p = root / rel
        if p.is_dir():
            return p
    return heyeddi_dir(root) / mkdir_name


def product_md(root: Path) -> Path | None:
    return resolve_existing(root, PRODUCT_CANDIDATES)


def design_md(root: Path) -> Path | None:
    return resolve_existing(root, DESIGN_CANDIDATES)


def designs_dir(root: Path) -> Path:
    return resolve_dir(root, DESIGNS_CANDIDATES, mkdir_name="designs")


def canonical_design_path(root: Path) -> Path:
    return heyeddi_dir(root) / "design.md"
