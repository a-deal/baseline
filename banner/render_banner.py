#!/usr/bin/env python3
"""Render X/Twitter header banner (1500x500) for Baseline.

X header safe zones:
- Profile pic covers bottom-left (~0,300 to ~200,500 on desktop, larger on mobile)
- Name/bio overlaps bottom-center on mobile
- Keep key content in right half + upper area
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1500, 500
OUT = os.path.join(os.path.dirname(__file__), "x_header_baseline.png")

# Colors
BLACK = (0, 0, 0)
OFF_WHITE = (245, 245, 245)
LIGHT_GRAY = (180, 180, 180)
MID_GRAY = (120, 120, 120)
DIM_GRAY = (80, 80, 80)
ACCENT = (200, 60, 60)

img = Image.new("RGB", (W, H), BLACK)
draw = ImageDraw.Draw(img)

RIGHT_MARGIN = 100


def get_font(size, bold=False):
    if bold:
        paths = [
            "/Library/Fonts/SF-Pro-Display-Black.otf",
            "/Library/Fonts/SF-Pro-Display-Heavy.otf",
            "/Library/Fonts/SF-Pro-Display-Bold.otf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:
        paths = [
            "/Library/Fonts/SF-Pro-Display-Regular.otf",
            "/Library/Fonts/SF-Pro-Display-Light.otf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)


def text_width(text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_height(text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


font_big = get_font(130, bold=True)
font_med = get_font(130, bold=False)
font_sub = get_font(18, bold=False)
font_logo_text = get_font(38, bold=True)

# =====================================================================
# LOGO — top right
# Concept: "baseline" with a horizontal line through it representing
# the baseline/threshold. A dot sits above the line = "where you stand"
# =====================================================================

logo_text = "baseline"
logo_w = text_width(logo_text, font_logo_text)
logo_h = text_height(logo_text, font_logo_text)
logo_x = W - RIGHT_MARGIN - logo_w - 50  # leave room for the dot element
logo_y = 42

# The dot — sits to the right of the text, above the baseline
dot_radius = 8
dot_x = logo_x + logo_w + 22
dot_y = logo_y + 8  # above the baseline
draw.ellipse(
    [(dot_x - dot_radius, dot_y - dot_radius),
     (dot_x + dot_radius, dot_y + dot_radius)],
    fill=ACCENT
)

# Horizontal "baseline" line — runs through/under the dot and extends right
line_y = logo_y + logo_h // 2 + 12  # sits at the baseline of the text
draw.line([(logo_x + logo_w + 8, line_y), (dot_x + 30, line_y)], fill=MID_GRAY, width=3)

# The text itself
draw.text((logo_x, logo_y), logo_text, fill=OFF_WHITE, font=font_logo_text)

# Small thin line under the full logo for separation
underline_y = logo_y + logo_h + 18
draw.line(
    [(logo_x, underline_y), (dot_x + 30, underline_y)],
    fill=DIM_GRAY, width=1
)

# =====================================================================
# TAGLINE — "Average is not healthy."
# =====================================================================

# "Average" — right-aligned
avg_text = "Average"
avg_w = text_width(avg_text, font_big)
avg_x = W - RIGHT_MARGIN - avg_w
draw.text((avg_x, 135), avg_text, fill=OFF_WHITE, font=font_big)

# "is not healthy." — right-aligned
y2 = 275

is_text = "is "
not_text = "not"
healthy_text = " healthy."

is_w = text_width(is_text, font_med)
not_w = text_width(not_text, font_big)
healthy_w = text_width(healthy_text, font_big)
total_w = is_w + not_w + healthy_w

line2_x = W - RIGHT_MARGIN - total_w

draw.text((line2_x, y2), is_text, fill=MID_GRAY, font=font_med)
draw.text((line2_x + is_w, y2), not_text, fill=ACCENT, font=font_big)
draw.text((line2_x + is_w + not_w, y2), healthy_text, fill=OFF_WHITE, font=font_big)

# =====================================================================
# SUBTITLE — right-aligned, bottom
# =====================================================================
sub_text = "Your health data, scored against the population."
sub_w = text_width(sub_text, font_sub)
draw.text((W - RIGHT_MARGIN - sub_w, 430), sub_text, fill=MID_GRAY, font=font_sub)

img.save(OUT, "PNG", quality=95)
print(f"Saved: {OUT} ({W}x{H})")
