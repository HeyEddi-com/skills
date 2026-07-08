"""HeyEddi `.heyeddi/` path helpers for PR submission review."""
from __future__ import annotations

from pathlib import Path


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def skill_docs_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "docs"


def product_md(root: Path) -> Path | None:
    for rel in (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md"):
        path = root / rel
        if path.is_file():
            return path
    return None


def design_md(root: Path) -> Path | None:
    for rel in (".heyeddi/design.md", ".heyeddi/DESIGN.md", "DESIGN.md"):
        path = root / rel
        if path.is_file():
            return path
    return None


def engineering_docs_dir(root: Path) -> Path:
    return skill_docs_dir(root) / "engineering"


def pr_review_path(root: Path, pr: int) -> Path:
    return skill_docs_dir(root) / f"pr-{pr}-review.md"


def pr_context_cache(root: Path, pr: int) -> Path:
    return skill_docs_dir(root) / f"pr-{pr}-context.json"
