#!/usr/bin/env python3
"""Render entry.png: a pixel-style newspaper front page for Monday 23 Nov 2026.

Build-time only (uses PIL). The submitted program main.py is stdlib-only and
just copies the committed entry.png.

Art is drawn on a 512x512 logical canvas where 1 logical pixel = 2x2 final
pixels, then upscaled with NEAREST to 1024x1024 so every pixel stays crisp.
All text uses Fusion Pixel Font 12px (proportional, latin) by TakWolf,
SIL OFL 1.1 — https://github.com/TakWolf/fusion-pixel-font — rendered only at
whole multiples of its 12px design size (12/24/36) so glyphs stay pixel-true.
Text layers are alpha-thresholded to kill any anti-aliasing softness.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = os.environ.get(
    "FUSION_FONT",
    "/tmp/fusionfont/fusion-pixel-12px-proportional-latin.ttf",
)
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

S = 512  # logical canvas size; final image is S*2

PAPER = (246, 241, 226)
INK = (22, 22, 34)
RED = (178, 34, 52)
NAVY = (18, 30, 58)
OCEAN = (43, 92, 168)
LAND = (80, 148, 82)
WHITE = (250, 248, 240)
GREY = (110, 106, 96)
GREEN = (34, 139, 76)
ORANGE = (232, 126, 32)
YELLOW = (244, 190, 40)

_f = {}


def font(size):
    if size not in _f:
        _f[size] = ImageFont.truetype(FONT_PATH, size)
    return _f[size]


def text_layer(size, draw_fn):
    """Draw text on a transparent layer, threshold alpha, return layer."""
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d)
    a = layer.getchannel("A").point(lambda v: 255 if v >= 110 else 0)
    layer.putalpha(a)
    return layer


def wrap(text, fnt, width):
    """Greedy word wrap by measured pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_body(d, text, x, y, width, pitch=15, fill=INK):
    fnt = font(12)
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += pitch
    return y


# ---------------------------------------------------------------- sprites

def px(d, x, y, c):
    d.point((x, y), fill=c)


def draw_globe(d, cx, cy, r):
    """Pixel globe with land blobs and a jagged red crack."""
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            dx, dy = xx - cx, yy - cy
            if dx * dx + dy * dy <= r * r:
                px(d, xx, yy, OCEAN)
    # crude continents: blobs of land pixels
    blobs = [(-0.45, -0.35, 0.30), (0.05, -0.55, 0.24), (0.45, -0.15, 0.28),
             (-0.15, 0.25, 0.26), (0.35, 0.45, 0.20), (-0.55, 0.45, 0.16)]
    for bx, by, br in blobs:
        gx, gy, gr = cx + int(bx * r), cy + int(by * r), int(br * r)
        for yy in range(gy - gr, gy + gr + 1):
            for xx in range(gx - gr, gx + gr + 1):
                dx, dy = xx - cx, yy - cy
                if dx * dx + dy * dy <= r * r and (xx - gx) ** 2 + (yy - gy) ** 2 <= gr * gr:
                    px(d, xx, yy, LAND)
    # outline
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            dx, dy = xx - cx, yy - cy
            if r * r < dx * dx + dy * dy <= (r + 1.6) ** 2:
                px(d, xx, yy, INK)
    # the crack: jagged vertical split, 2px wide, red with dark edge
    x = cx - 2
    for yy in range(cy - r + 6, cy + r - 4):
        x += [1, 0, -1, 1, 1, -1, 0, 1][(yy // 3) % 8]
        for wdt in (0, 1):
            px(d, x + wdt, yy, RED)
        px(d, x + 2, yy, INK)


def draw_ship(d, x, y, scale=1):
    """Tiny warship silhouette (hull, tower, mast) in ink."""
    d.rectangle([x, y + 10, x + 42, y + 14], fill=INK)          # hull deck
    d.polygon([(x + 2, y + 14), (x + 40, y + 14), (x + 34, y + 19), (x + 8, y + 19)], fill=INK)
    d.rectangle([x + 16, y + 4, x + 26, y + 10], fill=INK)        # superstructure
    d.rectangle([x + 20, y, x + 22, y + 4], fill=INK)             # mast
    d.rectangle([x + 30, y + 7, x + 36, y + 10], fill=INK)        # gun block


def draw_drone(d, x, y):
    """Quadcopter drone: X arms, rotors, body."""
    d.rectangle([x + 6, y + 5, x + 11, y + 9], fill=INK)
    for cx, cy in [(x, y), (x + 14, y), (x, y + 10), (x + 14, y + 10)]:
        d.rectangle([cx, cy, cx + 4, cy + 2], fill=INK)
    d.line([x + 3, y + 3, x + 7, y + 6], fill=INK)
    d.line([x + 15, y + 3, x + 11, y + 6], fill=INK)
    d.line([x + 3, y + 11, x + 7, y + 8], fill=INK)
    d.line([x + 15, y + 11, x + 11, y + 8], fill=INK)
    px(d, x + 8, y + 7, RED)


def draw_chart(d, x, y):
    """Rising market chart: axes + green zigzag arrow."""
    d.line([x, y, x, y + 22], fill=GREY)
    d.line([x, y + 22, x + 38, y + 22], fill=GREY)
    pts = [(x + 3, y + 18), (x + 12, y + 13), (x + 19, y + 16), (x + 28, y + 7), (x + 35, y + 3)]
    d.line(pts, fill=GREEN, width=2)
    d.polygon([(x + 35, y + 3), (x + 29, y + 3), (x + 35, y + 9)], fill=GREEN)


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(img)
    M = 14                      # margin
    R = S - M                   # right edge (498)

    # top rules
    d.rectangle([M, 6, R, 8], fill=INK)
    d.rectangle([M, 11, R, 12], fill=INK)

    # cracked-globe sprites flanking the masthead
    draw_globe(d, 30, 36, 13)
    draw_globe(d, S - 30, 36, 13)

    # ---- text layer (thresholded for crispness) ----
    def texts(t):
        # masthead
        t.text((S // 2, 14), "THE WORLD IN ONE DAY", font=font(36), fill=INK, anchor="ma")
        # date band text (drawn later over band; white on ink)
        # lead story
        t.text((140, 96), "CLIMATE · ANTALYA, TÜRKIYE", font=font(12), fill=RED)
        t.text((140, 112), "COP31 TALKS COLLAPSE", font=font(24), fill=INK)
        t.text((140, 142), "NO DEAL IN ANTALYA", font=font(24), fill=INK)
        draw_body(t, "Longest COP ever ends in failure: EU and 130+ nations reject "
                     "an 'Antalya Pact' that never mentions fossil fuels. First "
                     "collapse since Copenhagen 2009.", 140, 178, 358)
        # row 2, col A: Ukraine
        t.text((M, 232), "WAR · BENGHAZI, LIBYA", font=font(12), fill=RED)
        t.text((M, 248), "UKRAINE SINKS", font=font(24), fill=INK)
        t.text((M, 278), "RUSSIAN WARSHIP", font=font(24), fill=INK)
        draw_body(t, "Seven naval drones sink corvette Merkury in Benghazi port; "
                     "a Ka-27 helicopter destroyed, arms ship Angara hit. "
                     "Kyiv confirms.", M, 314, 236)
        # row 2, col B: Nvidia
        t.text((262, 232), "TECH · WALL STREET", font=font(12), fill=RED)
        t.text((262, 248), "HUANG RETURNS", font=font(24), fill=INK)
        t.text((262, 278), "AS NVIDIA CEO", font=font(24), fill=INK)
        draw_body(t, "Jensen Huang is reinstated as CEO, 11 days after resigning. "
                     "Shares leap 30% and the Nasdaq jumps 6%.", 262, 314, 236)
        # row 3 headlines
        t.text((M, 388), "INDONESIA", font=font(12), fill=RED)
        t.text((M, 403), "FACTORY FIRE", font=font(12), fill=INK)
        t.text((180, 388), "DEMOCRATS", font=font(12), fill=RED)
        t.text((180, 403), "TAKE THE HOUSE", font=font(12), fill=INK)
        t.text((346, 388), "IRAN DEFIES", font=font(12), fill=RED)
        t.text((346, 403), "US BLOCKADE", font=font(12), fill=INK)
        draw_body(t, "Candy-factory fire in Cikande, Banten: "
                     "24 dead, 30 missing.", M, 424, 152)
        draw_body(t, "258 seats: biggest House majority since "
                     "1992. Senate falls too.", 180, 424, 152)
        draw_body(t, "Tehran vows to defy Hormuz blockade. "
                     "Houthis claim refinery hit.", 346, 424, 152)

    img.paste(Image.alpha_composite(img.convert("RGBA"), text_layer(0, texts)).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # date band (over the blank strip between masthead and lead)
    d.rectangle([M, 58, R, 94], fill=INK)
    band = text_layer(0, lambda t: t.text((S // 2, 77), "MONDAY · 23 NOVEMBER 2026",
                                          font=font(24), fill=WHITE, anchor="mm"))
    img.paste(Image.alpha_composite(img.convert("RGBA"), band).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    # lead globe
    draw_globe(d, 70, 158, 52)

    # rules between sections
    d.rectangle([M, 222, R, 223], fill=INK)
    d.rectangle([M, 382, R, 383], fill=INK)

    # row-2 sprites
    draw_ship(d, 196, 226)
    draw_drone(d, 168, 224)
    draw_chart(d, 452, 226)

    # ticker band
    d.rectangle([M, 472, R, 506], fill=NAVY)
    tick = text_layer(0, lambda t: (
        t.text((S // 2, 476), "BTC REBOUNDS OFF 2-YEAR LOW · BELGIUM STRIKE GROUNDS FLIGHTS",
               font=font(12), fill=YELLOW, anchor="ma"),
        t.text((S // 2, 490), "2031 WOMEN'S WORLD CUP: USA · MEXICO · COSTA RICA · JAMAICA",
               font=font(12), fill=WHITE, anchor="ma"),
    ))
    img.paste(Image.alpha_composite(img.convert("RGBA"), tick).convert("RGB"), (0, 0))

    big = img.resize((1024, 1024), Image.NEAREST)
    big.save(OUT_PATH, optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    build()
