#!/usr/bin/env python3
"""Compose the news poster for Saturday 21 November 2026.

Draws a front-page style poster with Pillow primitives only and saves it
as entry.png beside this file. Deterministic: same pixels every run.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 234)
INK = (20, 22, 26)
RED = (179, 32, 44)
BLUE = (29, 78, 137)
GOLD = (176, 132, 26)
GREEN = (34, 110, 62)
GREY = (96, 96, 96)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_chart(draw, x, y, w, h):
    for i in range(4):
        gy = y + h * i // 3
        draw.line([(x, gy), (x + w, gy)], fill=(200, 194, 178), width=2)
    pts = [(x + 6, y + 16), (x + w * 0.24, y + 26), (x + w * 0.42, y + 19),
           (x + w * 0.58, y + h * 0.52), (x + w * 0.76, y + h * 0.60),
           (x + w - 8, y + h - 10)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED)
    ex, ey = pts[-1]
    draw.polygon([(ex - 26, ey - 20), (ex + 4, ey - 16), (ex - 8, ey + 12)], fill=RED)


def icon_burst(draw, cx, cy):
    draw.rectangle([cx - 30, cy + 10, cx - 12, cy + 30], fill=INK)
    draw.rectangle([cx - 4, cy + 2, cx + 14, cy + 30], fill=INK)
    draw.rectangle([cx + 18, cy + 14, cx + 30, cy + 30], fill=INK)
    star(draw, cx, cy - 14, 20, 8, 8, RED)
    star(draw, cx, cy - 14, 9, 4, 8, GOLD)


def icon_badge(draw, cx, cy):
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=GOLD, width=4)
    star(draw, cx, cy, 17, 7, 5, GOLD)


def icon_scales(draw, cx, cy):
    draw.line([(cx, cy - 26), (cx, cy + 22)], fill=BLUE, width=4)
    draw.line([(cx - 26, cy - 20), (cx + 26, cy - 20)], fill=BLUE, width=4)
    for sx in (-26, 26):
        draw.line([(cx + sx, cy - 20), (cx + sx - 8, cy + 0)], fill=BLUE, width=3)
        draw.line([(cx + sx, cy - 20), (cx + sx + 8, cy + 0)], fill=BLUE, width=3)
        draw.arc([cx + sx - 10, cy - 4, cx + sx + 10, cy + 12], 0, 180, fill=BLUE, width=3)
    draw.rectangle([cx - 14, cy + 24, cx + 14, cy + 29], fill=BLUE)


def icon_sun(draw, cx, cy):
    for i in range(8):
        a = i * math.pi / 4
        draw.line([(cx - 6 + 21 * math.cos(a), cy + 21 * math.sin(a)),
                   (cx - 6 + 30 * math.cos(a), cy + 30 * math.sin(a))], fill=GOLD, width=4)
    draw.ellipse([cx - 22, cy - 16, cx + 10, cy + 16], fill=GOLD)
    draw.rectangle([cx + 18, cy - 22, cx + 25, cy + 16], outline=RED, width=3)
    draw.ellipse([cx + 16, cy + 14, cx + 27, cy + 27], fill=RED)


def icon_robot(draw, cx, cy):
    draw.line([(cx, cy - 30), (cx, cy - 20)], fill=INK, width=4)
    draw.ellipse([cx - 4, cy - 36, cx + 4, cy - 28], fill=RED)
    draw.rounded_rectangle([cx - 28, cy - 20, cx + 28, cy + 24], 9, outline=INK, width=4)
    draw.ellipse([cx - 17, cy - 8, cx - 7, cy + 2], fill=BLUE)
    draw.ellipse([cx + 7, cy - 8, cx + 17, cy + 2], fill=BLUE)
    draw.line([(cx - 13, cy + 12), (cx + 13, cy + 12)], fill=INK, width=4)


def icon_mosquito(draw, cx, cy):
    draw.ellipse([cx - 7, cy - 16, cx + 7, cy + 20], fill=GREEN)
    draw.ellipse([cx - 5, cy - 27, cx + 5, cy - 14], fill=GREEN)
    draw.polygon([(cx - 5, cy - 12), (cx - 32, cy - 27), (cx - 24, cy - 1)],
                 outline=GREY, fill=(212, 222, 206))
    draw.polygon([(cx + 5, cy - 12), (cx + 32, cy - 27), (cx + 24, cy - 1)],
                 outline=GREY, fill=(212, 222, 206))
    for dx, dy in ((-1, -4), (-1, 6), (-1, 15), (1, -4), (1, 6), (1, 15)):
        draw.line([(cx + dx * 5, cy + dy), (cx + dx * 27, cy + dy + 11)], fill=INK, width=3)
    draw.line([(cx, cy - 27), (cx - 3, cy - 38)], fill=INK, width=3)


def panel(draw, x, y, w, h, place, color, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], fill=(253, 251, 245), outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=color)
    icon(draw, x + 38, y + 48)
    draw.text((x + 82, y + 28), place, font=font(SANS_B, 19), fill=color)
    hy = y + 78
    for line in wrap(draw, headline, font(SERIF_B, 23), w - 24):
        draw.text((x + 12, hy), line, font=font(SERIF_B, 23), fill=INK)
        hy += 28
    draw.line([(x + 12, hy + 1), (x + w - 12, hy + 1)], fill=(190, 182, 164), width=2)
    by = hy + 9
    for line in wrap(draw, body, font(SANS, 16), w - 24):
        draw.text((x + 12, by), line, font=font(SANS, 16), fill=(52, 54, 58))
        by += 21


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.line([(36, 26), (988, 26)], fill=INK, width=3)
    centered(d, 512, 38, "THE WORLD IN A DAY", font(SERIF_B, 62))
    d.line([(36, 116), (988, 116)], fill=INK, width=3)
    d.rectangle([36, 126, 988, 168], fill=INK)
    centered(d, 512, 133, "SATURDAY · 21 NOVEMBER 2026", font(SANS_B, 30), fill=(255, 255, 255))

    # Hero: markets sell-off
    hx, hy, hw, hh = 36, 184, 952, 308
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(253, 251, 245), outline=INK, width=3)
    d.rectangle([hx, hy, hx + hw, hy + 10], fill=RED)
    d.text((hx + 20, hy + 22), "GLOBAL MARKETS", font=font(SANS_B, 20), fill=RED)
    d.text((hx + 20, hy + 48), "AI SELL-OFF SHAKES", font=font(SERIF_B, 47), fill=INK)
    d.text((hx + 20, hy + 102), "WORLD MARKETS", font=font(SERIF_B, 47), fill=INK)
    icon_chart(d, hx + 24, hy + 166, 470, 106)
    sx = hx + 540
    stats = [("S&P 500", "-3.7%"), ("NIKKEI (JAPAN)", "-5.1%"), ("HANG SENG", "-3.8%")]
    sy = hy + 160
    for name, val in stats:
        d.text((sx, sy), name, font=font(SANS_B, 21), fill=INK)
        d.text((sx + 268, sy), val, font=font(SANS_B, 21), fill=RED)
        sy += 30
    for line in wrap(d, "Fears AI spending will not pay off spark a global rout; Wall Street enters correction.",
                     font(SANS, 17), 400):
        d.text((sx, sy + 8), line, font=font(SANS, 17), fill=(52, 54, 58))
        sy += 23

    # Panel rows
    pw, gap = 309, 12
    xs = [36, 36 + pw + gap, 36 + 2 * (pw + gap)]
    row1 = [
        ("UKRAINE", RED, "MISSILE STRIKES ZELENSKY'S HOMETOWN",
         "Russian strike on Kryvyi Rih kills two and wounds 60.", icon_burst),
        ("MEXICO", GOLD, "MOST-WANTED CARTEL BOSS CAPTURED",
         "'El Chapo Isidro' seized in a Sinaloa raid; violence follows.", icon_badge),
        ("THE HAGUE", BLUE, "UN COURT RULES MYANMAR GENOCIDE",
         "World court finds Myanmar responsible for genocide of the Rohingya.", icon_scales),
    ]
    row2 = [
        ("CLIMATE", GOLD, "COP31 TALKS RUN INTO OVERTIME",
         "Antalya summit deadlocked over fossil fuels.", icon_sun),
        ("GENEVA", BLUE, "'KILLER ROBOT' RULES BY 2028",
         "UN talks agree to draft limits on AI weapons.", icon_robot),
        ("HEALTH", GREEN, "MOSQUITOES CUT DENGUE BY 69%",
         "Bacteria-carrying mosquitoes slash cases in Brazil.", icon_mosquito),
    ]
    for x, (place, color, head, body, icon) in zip(xs, row1):
        panel(d, x, 504, pw, 216, place, color, head, body, icon)
    for x, (place, color, head, body, icon) in zip(xs, row2):
        panel(d, x, 732, pw, 216, place, color, head, body, icon)

    # Footer ticker
    d.rectangle([36, 964, 988, 1000], fill=INK)
    centered(d, 512, 973,
             "ALSO: FBI database breach reported  ·  82,500 march in France  ·  Ireland 20-17 South Africa",
             font(SANS_B, 17), fill=(255, 255, 255))

    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
