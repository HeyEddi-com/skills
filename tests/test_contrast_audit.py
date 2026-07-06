"""Tests for visual-auditor contrast math and fixture probe."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_contrast_math_green_on_green_fails_aa() -> None:
    sys.path.insert(0, str(REPO / "skills" / "visual-auditor" / "scripts"))
    from _contrast_math import contrast_ratio, parse_css_color, required_ratio  # type: ignore

    fg = parse_css_color("#16a34a")
    bg = parse_css_color("#22c55e")
    assert fg and bg
    ratio = contrast_ratio(fg, bg)
    assert ratio < required_ratio(16, 400)


def test_contrast_math_black_on_white_passes() -> None:
    sys.path.insert(0, str(REPO / "skills" / "visual-auditor" / "scripts"))
    from _contrast_math import contrast_ratio, parse_css_color, required_ratio  # type: ignore

    fg = parse_css_color("#111827")
    bg = parse_css_color("#ffffff")
    assert fg and bg
    assert contrast_ratio(fg, bg) >= required_ratio(16, 400)


def test_fixture_html_reports_contrast_errors() -> None:
    fixture = REPO / "skills" / "visual-auditor" / "fixtures" / "contrast-violations.html"
    script = REPO / "skills" / "visual-auditor" / "scripts" / "audit_contrast.py"
    if not fixture.is_file():
        return
    try:
        import playwright  # noqa: F401
    except ImportError:
        return

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--fixture",
            str(fixture),
            "--route",
            "/",
            "--widths",
            "375",
            "--project-root",
            str(REPO / "fixtures" / "sample-vue-app"),
        ],
        capture_output=True,
        text=True,
        cwd=script.parent,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["errors"] >= 1
    assert any(v.get("code") == "same-hue-low-contrast" for v in payload.get("violations", []))


def test_fixture_check_exits_nonzero() -> None:
    fixture = REPO / "skills" / "visual-auditor" / "fixtures" / "contrast-violations.html"
    script = REPO / "skills" / "visual-auditor" / "scripts" / "audit_contrast.py"
    try:
        import playwright  # noqa: F401
    except ImportError:
        return
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--fixture",
            str(fixture),
            "--route",
            "/",
            "--widths",
            "375",
            "--check",
            "--project-root",
            str(REPO / "fixtures" / "sample-vue-app"),
        ],
        cwd=script.parent,
    )
    assert result.returncode == 1
