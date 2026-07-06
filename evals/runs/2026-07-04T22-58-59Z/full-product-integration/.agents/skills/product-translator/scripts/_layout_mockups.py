"""Professional layout mockup drawing — settings app shell preset."""
from __future__ import annotations

from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None  # type: ignore[misc, assignment]
    ImageDraw = None  # type: ignore[misc, assignment]
    ImageFont = None  # type: ignore[misc, assignment]

CANVAS = (241, 245, 249)
SIDEBAR = (255, 255, 255)
SURFACE = (255, 255, 255)
BORDER = (226, 232, 240)
BORDER_INPUT = (203, 213, 225)
TEXT = (15, 23, 42)
TEXT_SEC = (51, 65, 85)
MUTED = (100, 116, 139)
ACCENT = (37, 99, 235)
NAV_MUTED = (71, 85, 105)
NAV_ACTIVE_BG = (239, 246, 255)
NAV_ACTIVE = (37, 99, 235)


@dataclass
class MockupSpec:
    app_name: str = "HeyEddi App"
    route: str = "/settings"
    feature: str = "settings"
    page_title: str = "Settings"
    page_subtitle: str = "Profile and notifications"
    display_name: str = "Alex Rivera"
    email: str = "alex@example.com"


def pillow_available() -> bool:
    return Image is not None


def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    from pathlib import Path

    for base in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/TTF", "/usr/share/fonts/dejavu"):
        path = Path(base) / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _rounded_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _draw_input(draw, box, value: str, font):
    _rounded_rect(draw, box, 8, SURFACE, BORDER_INPUT)
    draw.text((box[0] + 14, box[1] + 11), value, fill=TEXT, font=font)


def _draw_sidebar(draw, height: int, spec: MockupSpec, active: str = "Settings"):
    _rounded_rect(draw, (0, 0, 248, height), 0, SIDEBAR, BORDER)
    draw.line((248, 0, 248, height), fill=BORDER, width=1)
    draw.text((28, 28), spec.app_name, fill=TEXT, font=_font(20, bold=True))
    draw.text((28, 54), "Workspace", fill=MUTED, font=_font(11))
    nav = [("Dashboard", False), ("Settings", True), ("Team", False)]
    y = 100
    for label, is_active in nav:
        is_active = label == active or is_active
        if is_active:
            _rounded_rect(draw, (12, y, 236, y + 40), 8, NAV_ACTIVE_BG)
            draw.text((28, y + 10), label, fill=NAV_ACTIVE, font=_font(14, bold=True))
        else:
            draw.text((28, y + 10), label, fill=NAV_MUTED, font=_font(14))
        y += 48
    draw.text((28, height - 56), spec.display_name, fill=TEXT_SEC, font=_font(12, bold=True))
    draw.text((28, height - 36), spec.email, fill=MUTED, font=_font(11))


def draw_settings_desktop(spec: MockupSpec):
    w, h = 1440, 900
    img = Image.new("RGB", (w, h), CANVAS)
    draw = ImageDraw.Draw(img)
    _draw_sidebar(draw, h, spec)
    cx = 248
    title = _font(32, bold=True)
    subtitle = _font(15)
    section = _font(18, bold=True)
    label = _font(13)
    body = _font(15)
    draw.text((cx + 48, 48), spec.page_title, fill=TEXT, font=title)
    draw.text((cx + 48, 92), spec.page_subtitle, fill=MUTED, font=subtitle)
    card_w = min(720, w - cx - 96)
    cy = 140
    _rounded_rect(draw, (cx + 48, cy, cx + 48 + card_w, cy + 200), 12, SURFACE, BORDER)
    draw.text((cx + 72, cy + 20), "Profile", fill=TEXT, font=section)
    draw.text((cx + 72, cy + 56), "Display name", fill=TEXT_SEC, font=label)
    _draw_input(draw, (cx + 72, cy + 78, cx + 48 + card_w - 24, cy + 118), spec.display_name, body)
    draw.text((cx + 72, cy + 130), "Email", fill=TEXT_SEC, font=label)
    _draw_input(draw, (cx + 72, cy + 152, cx + 48 + card_w - 24, cy + 192), spec.email, body)
    cy2 = cy + 220
    _rounded_rect(draw, (cx + 48, cy2, cx + 48 + card_w, cy2 + 120), 12, SURFACE, BORDER)
    draw.text((cx + 72, cy2 + 20), "Notifications", fill=TEXT, font=section)
    draw.text((cx + 72, cy2 + 56), "Email notifications", fill=TEXT_SEC, font=body)
    _rounded_rect(draw, (cx + 48 + card_w - 68, cy2 + 52, cx + 48 + card_w - 24, cy2 + 76), 12, ACCENT)
    draw.ellipse((cx + 48 + card_w - 48, cy2 + 56, cx + 48 + card_w - 32, cy2 + 72), fill=(255, 255, 255))
    btn_x1 = cx + 48 + card_w - 160
    _rounded_rect(draw, (btn_x1, cy2 + 160, cx + 48 + card_w, cy2 + 204), 10, ACCENT)
    tw = draw.textlength("Save changes", font=body)
    draw.text((btn_x1 + (160 - tw) / 2, cy2 + 176), "Save changes", fill=(255, 255, 255), font=body)
    return img


def draw_settings_mobile(spec: MockupSpec):
    w, h = 390, 844
    img = Image.new("RGB", (w, h), CANVAS)
    draw = ImageDraw.Draw(img)
    _rounded_rect(draw, (0, 0, w, 56), 0, SIDEBAR, BORDER)
    draw.text((20, 16), spec.app_name, fill=TEXT, font=_font(16, bold=True))
    title = _font(26, bold=True)
    subtitle = _font(13)
    section = _font(16, bold=True)
    label = _font(12)
    body = _font(14)
    draw.text((20, 72), spec.page_title, fill=TEXT, font=title)
    draw.text((20, 108), spec.page_subtitle, fill=MUTED, font=subtitle)
    cy = 148
    _rounded_rect(draw, (16, cy, w - 16, cy + 200), 12, SURFACE, BORDER)
    draw.text((32, cy + 16), "Profile", fill=TEXT, font=section)
    draw.text((32, 42 + cy), "Display name", fill=TEXT_SEC, font=label)
    _draw_input(draw, (32, cy + 60, w - 32, cy + 100), spec.display_name, body)
    draw.text((32, cy + 112), "Email", fill=TEXT_SEC, font=label)
    _draw_input(draw, (32, cy + 130, w - 32, cy + 170), spec.email, body)
    cy2 = cy + 216
    _rounded_rect(draw, (16, cy2, w - 16, cy2 + 100), 12, SURFACE, BORDER)
    draw.text((32, cy2 + 16), "Notifications", fill=TEXT, font=section)
    draw.text((32, cy2 + 52), "Email notifications", fill=TEXT_SEC, font=body)
    _rounded_rect(draw, (16, h - 88, w - 16, h - 32), 10, ACCENT)
    tw = draw.textlength("Save changes", font=body)
    draw.text(((w - tw) / 2, h - 68), "Save changes", fill=(255, 255, 255), font=body)
    return img
