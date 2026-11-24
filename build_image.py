#!/usr/bin/env python3
"""Draw the front page for Tuesday 24 November 2026.

A newspaper front page, drawn entirely with Pillow: masthead, one lead
story and six smaller stories, each with a flat vector-style
illustration, plus a ticker of the day's other news. Output is a
1024x1024 PNG, deterministic: same input, same bytes.

Sources (verified against live news on 24 Nov 2026, ~00:15 UTC):
- COP31 climate talks in Antalya end without any deal on fossil fuels
  (Jagran Josh / Studmentor / Observer Voice school headlines, 24 Nov).
- Indonesia candy-factory fire in Cikande, Banten: at least 24 dead,
  around 30 missing, rescue ongoing (Education Times / Studmentor).
- Russian cargo ship Sparta II still burning in the Gulf of Finland
  after a drone strike (Education Times / Jagran Josh).
- Russian drone and missile strikes hit the Kyiv region; several
  killed and missing (Jagran Josh / Studmentor / Education Times).
- Nvidia reinstates Jensen Huang as CEO, less than two weeks after
  his resignation (People, 23 Nov).
- India and Nepal: Modi and PM Balendra Shah flag off the
  Saryu-Kamala Express; $1.5bn aid package and 8 MoUs (OneWorld
  SouthAsia / Jagran Josh).
- Oxfam/CEOBS report: Gaza's air, soil and water poisoned by
  explosive and incendiary weapons (Disclosure News, 24 Nov);
  Australia, Canada, Italy and UK call for aid access to flooded
  Gaza (The Paris Eye, 23 Nov).
- Ticker: Lisbon cost-of-living protests; World Chess Championship
  Gukesh vs Sindarov begins in Geneva; Verstappen wins the Las Vegas
  GP; Alcaraz wins the ATP Finals; India-New Zealand Test drawn,
  Pant 128; Trump blames Democrats for a Wall Street sell-off;
  Russian corvette reported destroyed at Benghazi, Libya.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (178, 34, 27)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)
SEA = (46, 110, 138)
SAND = (214, 196, 150)
ORANGE = (214, 92, 20)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A cracked globe: blue disc, meridian lines, red crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 124, 165),
                 outline=INK, width=3)
    for k in (-0.55, 0.0, 0.55):
        x0 = cx + int(r * k)
        draw.arc([x0 - int(r * 0.45), cy - r, x0 + int(r * 0.45), cy + r],
                 start=270, end=90, fill=(210, 230, 240), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(210, 230, 240), width=2)
    draw.ellipse([cx - r + 12, cy - r + 18, cx - 8, cy - 6], fill=(74, 140, 90))
    draw.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16], fill=(74, 140, 90))
    pts = [(cx + 6, cy - r + 4), (cx - 12, cy - r // 2), (cx + 10, cy - 4),
           (cx - 8, cy + r // 3), (cx + 4, cy + r - 8)]
    draw.line(pts, fill=RED, width=5, joint="curve")


def draw_factory_fire(draw, x, y, w, h):
    """Factory shed with flames and smoke, contained in its box."""
    base = y + h - 20
    draw.rectangle([x, base, x + w, y + h], fill=(120, 116, 104))
    draw.rectangle([x + 10, base - 52, x + w - 10, base], fill=(150, 52, 40))
    draw.polygon([(x + 10, base - 52), (x + w // 2, base - 78),
                  (x + w - 10, base - 52)], fill=(84, 80, 70))
    draw.rectangle([x + w - 30, base - 92, x + w - 18, base - 52],
                   fill=(120, 116, 104))
    for i in range(3):
        wx = x + 24 + i * 34
        draw.rectangle([wx, base - 34, wx + 18, base - 12], fill=(52, 52, 52))
    fx = x + w // 2
    for dx, fh, col in ((-18, 30, (255, 140, 0)), (0, 42, (255, 90, 0)),
                        (18, 28, (255, 170, 40))):
        draw.polygon([(fx + dx - 11, base - 52), (fx + dx, base - 52 - fh),
                      (fx + dx + 11, base - 52)], fill=col)
    for i, rr in enumerate((9, 12)):
        cy = y + 24 - i * 10
        draw.ellipse([fx - rr + 14, cy - rr, fx + rr + 14, cy + rr],
                     fill=(150, 148, 140))


def draw_ship_fire(draw, x, y, w, h):
    """Cargo ship burning on the sea, contained in its box."""
    sea_y = y + h - 24
    draw.rectangle([x, sea_y, x + w, y + h], fill=(38, 90, 120))
    draw.rectangle([x + 10, sea_y - 26, x + w - 10, sea_y], fill=(60, 60, 62))
    draw.rectangle([x + w // 2 - 8, sea_y - 44, x + w // 2 + 22, sea_y - 26],
                   fill=(200, 200, 190))
    draw.rectangle([x + 16, sea_y - 38, x + 44, sea_y - 26], fill=(140, 140, 130))
    fx = x + w // 2 + 4
    for dx, fh, col in ((-16, 26, (255, 140, 0)), (0, 36, (255, 90, 0)),
                        (16, 24, (255, 170, 40))):
        draw.polygon([(fx + dx - 10, sea_y - 38), (fx + dx, sea_y - 38 - fh),
                      (fx + dx + 10, sea_y - 38)], fill=col)
    for i, rr in enumerate((9, 12)):
        cy = y + 22 - i * 10
        draw.ellipse([fx - rr + 8, cy - rr, fx + rr + 8, cy + rr],
                     fill=(120, 118, 110))


def draw_flats(draw, x, y, w, h):
    """Apartment block with a smoke column, contained in its box."""
    top = y + 34
    draw.rectangle([x, top, x + w, y + h], fill=(120, 116, 104))
    draw.rectangle([x, top, x + w, top + 12], fill=(84, 80, 70))
    for r in range(2):
        for c in range(4):
            wx = x + 12 + c * (w // 4)
            wy = top + 22 + r * 26
            lit = (r + c) % 3 == 0
            draw.rectangle([wx, wy, wx + w // 6, wy + 16],
                           fill=(255, 214, 130) if lit else (52, 52, 52))
    draw.polygon([(x + w - 26, top), (x + w, top), (x + w, top + 26),
                  (x + w - 40, top + 16)], fill=(40, 38, 34))
    sx = x + w - 14
    for i, rr in enumerate((9, 12, 14)):
        cy = y + 26 - i * 9
        draw.ellipse([sx - rr, cy - rr, sx + rr, cy + rr],
                     fill=(150, 148, 140))


def draw_chip(draw, x, y, s):
    """A computer chip, for the Nvidia story."""
    draw.rectangle([x, y, x + s, y + s], fill=TEAL, outline=INK, width=2)
    draw.rectangle([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                   fill=(20, 60, 56), outline=(255, 255, 255), width=2)
    for i in range(4):
        px = x + s // 4 + i * (s // 8)
        draw.line([(px, y - 8), (px, y)], fill=INK, width=2)
        draw.line([(px, y + s), (px, y + s + 8)], fill=INK, width=2)
        py = y + s // 4 + i * (s // 8)
        draw.line([(x - 8, py), (x, py)], fill=INK, width=2)
        draw.line([(x + s, py), (x + s + 8, py)], fill=INK, width=2)


def draw_train(draw, x, y, w, h):
    """A small train front, for the India-Nepal story."""
    draw.rectangle([x + 8, y + 10, x + w - 8, y + h - 14], fill=BLUE,
                   outline=INK, width=2)
    draw.rectangle([x + 20, y + 22, x + w - 20, y + h // 2], fill=(210, 230, 240),
                   outline=INK, width=2)
    draw.line([(x + w // 2, y + 22), (x + w // 2, y + h // 2)], fill=INK, width=2)
    for cx in (x + w // 3, x + 2 * w // 3):
        draw.ellipse([cx - 9, y + h - 32, cx + 9, y + h - 14], fill=(255, 220, 100),
                     outline=INK, width=2)
    draw.line([(x, y + h - 6), (x + w, y + h - 6)], fill=INK, width=3)


def draw_drop(draw, cx, cy, r):
    """A water drop with a warning mark, for the Gaza story."""
    draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r], fill=(58, 124, 165),
                 outline=INK, width=2)
    draw.polygon([(cx, cy - r - 14), (cx - r, cy - r // 2 + 4),
                  (cx + r, cy - r // 2 + 4)], fill=(58, 124, 165))
    draw.text((cx, cy - 6), "!", font=F_SANS_B(28), fill=(255, 255, 255),
              anchor="ma")


def panel_head(draw, x, y, w, kicker, title, tsize=27):
    draw.text((x, y), kicker, font=F_SANS_B(15), fill=RED)
    y = para(draw, x, y + 22, title, F_SANS_B(tsize), w, leading=tsize + 4)
    return y + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---------- masthead ----------
    rule(d, M, 30, W - M, 3)
    d.text((W // 2, 44), "THE WORLD IN ONE PAGE",
           font=F_SERIF_B(56), fill=INK, anchor="mt")
    rule(d, M, 116, W - M, 2)
    d.text((M, 126), "TUESDAY, 24 NOVEMBER 2026", font=F_SANS_B(19), fill=INK)
    d.text((W - M, 126), "ONE DAY  ·  ONE PAGE", font=F_SANS_B(19),
           fill=INK, anchor="rt")
    rule(d, M, 154, W - M, 3)

    # ---------- lead: COP31 ----------
    ly = 168
    d.text((M, ly), "CLIMATE  ·  ANTALYA, TÜRKIYE", font=F_SANS_B(16), fill=RED)
    d.text((M, ly + 26), "COP31 COLLAPSES", font=F_SERIF_B(66), fill=INK)
    d.text((M, ly + 100),
           "Climate talks end with no deal at all",
           font=F_SERIF(26), fill=INK)
    body = ("Nearly 200 countries leave Antalya without an agreement after "
            "the final draft drops every mention of fossil fuels. The "
            "summit closes empty-handed, two days late.")
    para(d, M, ly + 140, body, F_SANS(19), 560, leading=25)
    draw_globe(d, 862, ly + 122, 78)
    d.text((862, ly + 216), "No deal on fossil fuels,",
           font=F_SANS(15), fill=GREY, anchor="mt")
    d.text((862, ly + 236), "no deal on climate finance.",
           font=F_SANS(15), fill=GREY, anchor="mt")
    rule(d, M, 452, W - M, 2)

    # ---------- row 2: three stories ----------
    ry = 470
    cols = [(M, 300), (M + 312, 300), (M + 624, 300)]
    # A: Indonesia factory fire
    x, w = cols[0]
    y = panel_head(d, x, ry, w, "DISASTER  ·  CIKANDE, BANTEN",
                   "Factory fire: 24 dead, 30 missing")
    draw_factory_fire(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "A blaze at a candy factory kills at least 24 workers. Rescuers "
         "keep searching for around 30 still missing.",
         F_SANS(16), w, leading=21)
    # B: Baltic ship
    x, w = cols[1]
    y = panel_head(d, x, ry, w, "THE BALTIC  ·  GULF OF FINLAND",
                   "Russian ship still burning")
    draw_ship_fire(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "The cargo ship Sparta II burns after a drone strike Finland "
         "says was likely Ukraine's.",
         F_SANS(16), w, leading=21)
    # C: Kyiv
    x, w = cols[2]
    y = panel_head(d, x, ry, w, "UKRAINE  ·  KYIV REGION",
                   "Drone hits homes; several missing")
    draw_flats(d, x, y + 8, w, 108)
    para(d, x, y + 128,
         "Russian drone and missile strikes hit the Kyiv region, killing "
         "several people and leaving others missing.",
         F_SANS(16), w, leading=21)
    rule(d, M, 752, W - M, 2)

    # ---------- row 3: three short stories ----------
    ry = 770
    x, w = cols[0]
    y = panel_head(d, x, ry, w, "TECH  ·  NVIDIA",
                   "Huang is back as CEO", 24)
    draw_chip(d, x + 8, y + 6, 52)
    d.text((x + 78, y + 10), "Back as CEO less than two",
           font=F_SANS(16), fill=INK)
    d.text((x + 78, y + 32), "weeks after quitting.",
           font=F_SANS(16), fill=INK)
    x, w = cols[1]
    y = panel_head(d, x, ry, w, "SOUTH ASIA  ·  INDIA–NEPAL",
                   "A new train, a $1.5bn package", 24)
    draw_train(d, x + 8, y + 4, 70, 60)
    d.text((x + 92, y + 10), "Modi and Shah flag off",
           font=F_SANS(16), fill=INK)
    d.text((x + 92, y + 32), "the Saryu-Kamala Express.",
           font=F_SANS(16), fill=INK)
    x, w = cols[2]
    y = panel_head(d, x, ry, w, "GAZA  ·  THE POISONED LAND",
                   "Toxic legacy of the war", 24)
    draw_drop(d, x + 40, y + 40, 24)
    d.text((x + 86, y + 10), "Oxfam: air, soil, water",
           font=F_SANS(16), fill=INK)
    d.text((x + 86, y + 32), "poisoned for decades.",
           font=F_SANS(16), fill=INK)
    rule(d, M, 914, W - M, 2)

    # ---------- ticker ----------
    ty = 924
    d.text((M, ty), "ALSO ON 24 NOVEMBER", font=F_SANS_B(15), fill=RED)
    ticker = ("Lisbon marches against the cost of living  ·  Gukesh defends "
              "his chess crown vs Sindarov in Geneva  ·  Verstappen wins "
              "the Las Vegas GP  ·  Alcaraz takes the ATP Finals  ·  "
              "India–New Zealand Test drawn, Pant 128")
    para(d, M, ty + 24, ticker, F_SANS(15), W - 2 * M, leading=20)
    rule(d, M, 990, W - M, 2)
    d.text((W // 2, 998),
           "All stories as reported on Tuesday 24 November 2026",
           font=F_SANS(13), fill=GREY, anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
