#!/usr/bin/env python3
"""Generate settings handoff mockup PNGs — layout references for evals.

Hub tooling only: writes PNGs + minimal handoff.json. The **@design-handoff skill**
must read those images and **author** `mockup-brief.md` (see reference/interpret-mockups.md).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit("Install Pillow: uv sync --group hub-tools") from exc

# Palette — calm SaaS (OpenProps-adjacent)
CANVAS = (241, 245, 249)       # page bg
SIDEBAR = (255, 255, 255)      # shell sidebar
SURFACE = (255, 255, 255)      # cards
BORDER = (226, 232, 240)
BORDER_INPUT = (203, 213, 225)
TEXT = (15, 23, 42)
TEXT_SEC = (51, 65, 85)
MUTED = (100, 116, 139)
ACCENT = (37, 99, 235)
ACCENT_HOVER = (29, 78, 216)
NAV_MUTED = (71, 85, 105)
NAV_ACTIVE_BG = (239, 246, 255)
NAV_ACTIVE = (37, 99, 235)
SHADOW = (148, 163, 184, 40)

APP_NAME = "SecureVault"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/TTF",
        "/usr/share/fonts/dejavu",
    ):
        path = Path(base) / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, ...],
    outline: tuple[int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _shadow_card(img: Image.Image, box: tuple[int, int, int, int], radius: int = 12) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = box
    for i, alpha in enumerate((18, 12, 6)):
        od.rounded_rectangle(
            (x0 + i, y0 + i + 2, x1 + i, y1 + i + 2),
            radius=radius,
            fill=(15, 23, 42, alpha),
        )
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))


def _draw_input(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    font: ImageFont.ImageFont,
) -> None:
    _rounded_rect(draw, box, 8, SURFACE, BORDER_INPUT)
    draw.text((box[0] + 14, box[1] + 11), value, fill=TEXT, font=font)


def _draw_toggle(draw: ImageDraw.ImageDraw, x: int, y: int, on: bool = True) -> None:
    w, h = 44, 24
    track = ACCENT if on else (203, 213, 225)
    _rounded_rect(draw, (x, y, x + w, y + h), 12, track)
    knob_x = x + w - 20 if on else x + 4
    draw.ellipse((knob_x, y + 4, knob_x + 16, y + 20), fill=(255, 255, 255))


def _draw_sidebar(draw: ImageDraw.ImageDraw, height: int) -> None:
    _rounded_rect(draw, (0, 0, 248, height), 0, SIDEBAR, BORDER)
    draw.line((248, 0, 248, height), fill=BORDER, width=1)
    logo = _font(20, bold=True)
    draw.text((28, 28), APP_NAME, fill=TEXT, font=logo)
    draw.text((28, 54), "Workspace", fill=MUTED, font=_font(11))

    nav = [
        ("Dashboard", False),
        ("Documents", False),
        ("Team", False),
        ("Settings", True),
    ]
    y = 100
    nav_font = _font(15)
    for label, active in nav:
        if active:
            _rounded_rect(draw, (12, y - 6, 236, y + 30), 8, NAV_ACTIVE_BG)
            draw.text((40, y), label, fill=NAV_ACTIVE, font=nav_font)
        else:
            draw.text((40, y), label, fill=NAV_MUTED, font=nav_font)
        y += 44

    # User chip bottom
    _rounded_rect(draw, (16, height - 72, 232, height - 20), 10, (248, 250, 252), BORDER)
    draw.ellipse((28, height - 60, 52, height - 36), fill=ACCENT)
    draw.text((36, height - 54), "A", fill=(255, 255, 255), font=_font(12, bold=True))
    draw.text((60, height - 58), "Alex Rivera", fill=TEXT, font=_font(13))
    draw.text((60, height - 40), "alex@example.com", fill=MUTED, font=_font(11))


def _draw_topbar(draw: ImageDraw.ImageDraw, width: int) -> None:
    draw.rectangle((248, 0, width, 64), fill=SURFACE)
    draw.line((248, 64, width, 64), fill=BORDER, width=1)
    draw.text((280, 20), "Settings", fill=TEXT, font=_font(18, bold=True))
    # Search + bell + avatar
    _rounded_rect(draw, (width - 200, 16, width - 48, 48), 8, CANVAS, BORDER)
    draw.text((width - 188, 26), "Search…", fill=MUTED, font=_font(13))
    draw.ellipse((width - 36, 20, width - 12, 44), fill=ACCENT)


def _draw_settings_content_desktop(draw: ImageDraw.ImageDraw, content_x: int, content_y: int, content_w: int) -> None:
    title = _font(32, bold=True)
    subtitle = _font(15)
    section = _font(17, bold=True)
    label = _font(13)
    body = _font(15)

    draw.text((content_x, content_y), "Settings", fill=TEXT, font=title)
    draw.text(
        (content_x, content_y + 44),
        "Manage your profile and how we reach you.",
        fill=MUTED,
        font=subtitle,
    )

    # Profile card
    cy = content_y + 100
    card_h = 220
    card = (content_x, cy, content_x + content_w, cy + card_h)
    _rounded_rect(draw, card, 12, SURFACE, BORDER)
    draw.text((content_x + 24, cy + 20), "Profile", fill=TEXT, font=section)
    draw.text((content_x + 24, cy + 48), "Your name and sign-in email.", fill=MUTED, font=label)

    draw.text((content_x + 24, cy + 82), "Display name", fill=TEXT_SEC, font=label)
    _draw_input(draw, (content_x + 24, cy + 102, content_x + content_w - 24, cy + 146), "Alex Rivera", body)

    draw.text((content_x + 24, cy + 158), "Email", fill=TEXT_SEC, font=label)
    _draw_input(draw, (content_x + 24, cy + 178, content_x + content_w - 24, cy + 222), "alex@example.com", body)

    # Notifications card
    cy2 = cy + card_h + 24
    card2_h = 120
    card2 = (content_x, cy2, content_x + content_w, cy2 + card2_h)
    _rounded_rect(draw, card2, 12, SURFACE, BORDER)
    draw.text((content_x + 24, cy2 + 20), "Notifications", fill=TEXT, font=section)
    draw.text((content_x + 24, cy2 + 48), "Choose how you hear about account activity.", fill=MUTED, font=label)
    draw.text((content_x + 24, cy2 + 82), "Email updates", fill=TEXT_SEC, font=body)
    _draw_toggle(draw, content_x + content_w - 68, cy2 + 76, on=True)

    # Save
    btn = (content_x + content_w - 140, cy2 + card2_h + 32, content_x + content_w, cy2 + card2_h + 80)
    _rounded_rect(draw, btn, 8, ACCENT)
    tw = draw.textlength("Save changes", font=body)
    draw.text((btn[0] + (btn[2] - btn[0] - tw) / 2, btn[1] + 12), "Save changes", fill=(255, 255, 255), font=body)


def draw_desktop() -> Image.Image:
    w, h = 1440, 900
    img = Image.new("RGB", (w, h), CANVAS)
    draw = ImageDraw.Draw(img)
    _draw_sidebar(draw, h)
    _draw_topbar(draw, w)
    _draw_settings_content_desktop(draw, 280, 96, 720)
    return img


def _draw_mobile_topbar(draw: ImageDraw.ImageDraw, w: int) -> None:
    draw.rectangle((0, 0, w, 56), fill=SURFACE)
    draw.line((0, 56, w, 56), fill=BORDER, width=1)
    # hamburger
    for i, yy in enumerate((22, 28, 34)):
        draw.rounded_rectangle((20, yy, 36, yy + 2), radius=1, fill=TEXT)
    draw.text((52, 16), APP_NAME, fill=TEXT, font=_font(17, bold=True))
    draw.ellipse((w - 44, 14, w - 20, 38), fill=ACCENT)


def draw_mobile() -> Image.Image:
    w, h = 390, 844
    img = Image.new("RGB", (w, h), CANVAS)
    draw = ImageDraw.Draw(img)
    _draw_mobile_topbar(draw, w)

    title = _font(26, bold=True)
    subtitle = _font(13)
    section = _font(16, bold=True)
    label = _font(12)
    body = _font(14)

    draw.text((20, 72), "Settings", fill=TEXT, font=title)
    draw.text((20, 108), "Profile and notifications", fill=MUTED, font=subtitle)

    cy = 148
    _rounded_rect(draw, (16, cy, w - 16, cy + 200), 12, SURFACE, BORDER)
    draw.text((32, cy + 16), "Profile", fill=TEXT, font=section)
    draw.text((32, 42 + cy), "Display name", fill=TEXT_SEC, font=label)
    _draw_input(draw, (32, cy + 60, w - 32, cy + 100), "Alex Rivera", body)
    draw.text((32, cy + 112), "Email", fill=TEXT_SEC, font=label)
    _draw_input(draw, (32, cy + 130, w - 32, cy + 170), "alex@example.com", body)

    cy2 = cy + 216
    _rounded_rect(draw, (16, cy2, w - 16, cy2 + 140), 12, SURFACE, BORDER)
    draw.text((32, cy2 + 16), "Notifications", fill=TEXT, font=section)
    draw.text((32, cy2 + 52), "No channels configured", fill=TEXT_SEC, font=body)
    draw.text((32, cy2 + 76), "Add email or push when you connect integrations.", fill=MUTED, font=label)

    _rounded_rect(draw, (16, h - 88, w - 16, h - 32), 10, ACCENT)
    tw = draw.textlength("Save changes", font=body)
    draw.text(((w - tw) / 2, h - 68), "Save changes", fill=(255, 255, 255), font=body)

    # Bottom nav
    draw.rectangle((0, h - 28, w, h), fill=SURFACE)
    draw.line((0, h - 28, w, h - 28), fill=BORDER, width=1)
    return img


HANDOFF_JSON = {
    "route": "/settings",
    "app": APP_NAME,
    "mockup_contract": "layout_only",
    "notes": [
        "PNG colors are illustrative — implement colors from .heyeddi/design.md tokens",
        "mockup-brief.md is NOT shipped — @design-handoff must write it from these PNGs before coding",
        "See skills/design-handoff/reference/interpret-mockups.md",
    ],
}


def write_handoff_json(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "handoff.json").write_text(json.dumps(HANDOFF_JSON, indent=2) + "\n")
    print(f"Wrote {out_dir / 'handoff.json'}")


def write_pair(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    draw_desktop().save(out_dir / "desktop.png", "PNG")
    draw_mobile().save(out_dir / "mobile.png", "PNG")
    write_handoff_json(out_dir)
    print(f"Wrote {out_dir / 'desktop.png'}")
    print(f"Wrote {out_dir / 'mobile.png'}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Generate handoff mockup PNGs")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Regenerate eval template + fixture mockups",
    )
    parser.add_argument("out_dir", nargs="?", type=Path, help=".heyeddi/designs/<feature> directory")
    args = parser.parse_args()

    targets = [
        root / "evals/projects/vue-handoff/.heyeddi/designs/settings",
        root / "evals/projects/product-app/.heyeddi/designs/settings",
        root / "fixtures/sample-vue-app/.heyeddi/designs/settings",
    ]

    if args.all:
        for t in targets:
            if t.parent.parent.parent.exists():
                write_pair(t)
        return

    if not args.out_dir:
        parser.error("Provide out_dir or use --all")
    write_pair(args.out_dir)


if __name__ == "__main__":
    main()
