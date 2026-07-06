"""HeyEddi `.heyeddi/` path helpers — UX flow docs live under `.heyeddi/docs/ux-flows/`."""
from __future__ import annotations

from pathlib import Path


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def skill_docs_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "docs"


def ux_flows_dir(root: Path) -> Path:
    return skill_docs_dir(root) / "ux-flows"


def ux_flows_index(root: Path) -> Path:
    return skill_docs_dir(root) / "ux-flows.md"


def audits_dir(root: Path) -> Path:
    return heyeddi_dir(root) / "audits"


def product_md(root: Path) -> Path | None:
    for rel in (".heyeddi/product.md", ".heyeddi/PRODUCT.md", "PRODUCT.md"):
        p = root / rel
        if p.is_file():
            return p
    return None
