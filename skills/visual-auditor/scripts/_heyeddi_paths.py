"""HeyEddi path helpers: visual audit artifacts under `.heyeddi/audits/visual/`."""
from __future__ import annotations

from pathlib import Path


def heyeddi_dir(root: Path) -> Path:
    return root / ".heyeddi"


def visual_audit_dir(root: Path) -> Path:
    """Contrast reports, JSON, and screenshots subdirectory."""
    return heyeddi_dir(root) / "audits" / "visual"


def screenshot_dir(root: Path) -> Path:
    return visual_audit_dir(root) / "screenshots"


def legacy_screenshot_dir(root: Path) -> Path:
    """Deprecated repo-root path: do not write here."""
    return root / ".visual-audit"
