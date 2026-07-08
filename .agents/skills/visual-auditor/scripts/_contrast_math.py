"""WCAG 2.x contrast math — shared by audit_contrast and unit tests."""
from __future__ import annotations

import math
import re
from typing import TypedDict


class Rgba(TypedDict):
    r: float
    g: float
    b: float
    a: float


def parse_css_color(value: str | None) -> Rgba | None:
    if not value or value.strip().lower() in {"transparent", "none"}:
        return None
    value = value.strip()
    m = re.match(
        r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)",
        value,
        re.I,
    )
    if m:
        return {
            "r": float(m.group(1)),
            "g": float(m.group(2)),
            "b": float(m.group(3)),
            "a": float(m.group(4)) if m.group(4) is not None else 1.0,
        }
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return {
                "r": int(h[0:2], 16),
                "g": int(h[2:4], 16),
                "b": int(h[4:6], 16),
                "a": 1.0,
            }
    return None


def relative_luminance(color: Rgba) -> float:
    def channel(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(color["r"]) + 0.7152 * channel(color["g"]) + 0.0722 * channel(color["b"])


def contrast_ratio(fg: Rgba, bg: Rgba) -> float:
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def rgb_to_hsl(color: Rgba) -> tuple[float, float, float]:
    r, g, b = color["r"] / 255.0, color["g"] / 255.0, color["b"] / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d + (6 if g < b else 0)) / 6.0
    elif mx == g:
        h = ((b - r) / d + 2) / 6.0
    else:
        h = ((r - g) / d + 4) / 6.0
    return h * 360.0, s, l


def hue_distance(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def is_large_text(font_size_px: float, font_weight: int | float) -> bool:
    weight = int(font_weight) if not isinstance(font_weight, str) else 700 if str(font_weight).isdigit() and int(font_weight) >= 700 else 400
    if "bold" in str(font_weight).lower():
        weight = 700
    return font_size_px >= 18.0 or (font_size_px >= 14.0 and weight >= 700)


def required_ratio(font_size_px: float, font_weight: int | float, level: str = "AA") -> float:
    large = is_large_text(font_size_px, font_weight)
    if level == "AAA":
        return 4.5 if large else 7.0
    return 3.0 if large else 4.5


def composite_over(fg: Rgba, bg: Rgba) -> Rgba:
    a = fg["a"] + bg["a"] * (1.0 - fg["a"])
    if a <= 0:
        return {"r": 0.0, "g": 0.0, "b": 0.0, "a": 0.0}
    return {
        "r": (fg["r"] * fg["a"] + bg["r"] * bg["a"] * (1.0 - fg["a"])) / a,
        "g": (fg["g"] * fg["a"] + bg["g"] * bg["a"] * (1.0 - fg["a"])) / a,
        "b": (fg["b"] * fg["a"] + bg["b"] * bg["a"] * (1.0 - fg["a"])) / a,
        "a": a,
    }


def round_ratio(value: float) -> float:
    return math.floor(value * 100.0) / 100.0
