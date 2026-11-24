#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026.

Everything is drawn from scratch with Pillow: a masthead, one lead
story, three mid-page stories and three short stories, each with a
small flat illustration, plus a ticker of the day's other news. The
output is a 1024 by 1024 PNG, deterministic, so running the script
twice gives byte-identical files.

The stories are the headlines as reported on 24 November 2026:
COP31 in Antalya ends with no deal on fossil fuels; a candy-factory
fire in Cikande, Banten, kills at least 24 with around 30 missing;
the Russian cargo ship Sparta II keeps burning in the Gulf of
Finland after a drone strike; Russian drones hit the Kyiv region;
Nvidia brings Jensen Huang back as chief executive; India and Nepal
open the Saryu-Kamala Express with a $1.5bn package; an Oxfam
report says Gaza's air, soil and water are poisoned for decades.
The ticker adds the Lisbon protests, the Gukesh-Sindarov chess
championship, the Las Vegas Grand Prix, the ATP Finals and the
India-New Zealand Test draw.
"""
import os  # filesystem paths
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

SIDE = 1024
MARGIN = 36
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PALETTE = {
    "paper": (246, 241, 229),
    "ink": (20, 20, 20),
    "red": (178, 34, 27),
    "blue": (31, 78, 121),
    "teal": (15, 118, 110),
    "grey": (90, 86, 76),
    "sea": (46, 110, 138),
    "wall": (120, 116, 104),
    "roof": (84, 80, 70),
    "dark": (52, 52, 52),
    "lit": (255, 214, 130),
    "brick": (150, 52, 40),
    "smoke": (150, 148, 140),
    "soot": (120, 118, 110),
    "water": (38, 90, 120),
    "hull": (60, 60, 62),
    "deck": (200, 200, 190),
    "crate": (140, 140, 130),
    "pale": (210, 230, 240),
    "land": (74, 140, 90),
    "ocean": (58, 124, 165),
    "flame_a": (255, 140, 0),
    "flame_b": (255, 90, 0),
    "flame_c": (255, 170, 40),
    "gold": (255, 220, 100),
    "navy": (20, 60, 56),
}


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def serif_bold(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_font("DejaVuSerif.ttf", size)


def sans_bold(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def split_words(dr, text, fnt, width):
    """Greedy word wrap: lines that fit inside width."""
    out = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if dr.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(dr, x, y, text, fnt, width, color, gap):
    """Draw wrapped text, return the y just below the last line."""
    for ln in split_words(dr, text, fnt, width):
        dr.text((x, y), ln, font=fnt, fill=color)
        y += gap
    return y


def hline(dr, x0, y, x1, width=2):
    dr.line([(x0, y), (x1, y)], fill=PALETTE["ink"], width=width)


def card_title(dr, x, y, width, kicker, title, tsize):
    """Kicker + wrapped title; returns y below the title block."""
    dr.text((x, y), kicker, font=sans_bold(15), fill=PALETTE["red"])
    end = draw_lines(dr, x, y + 22, title, sans_bold(tsize), width,
                     PALETTE["ink"], tsize + 4)
    return end + 4


def flame_row(dr, cx, base_y, specs, half=10):
    """A row of triangular flames centred on cx, sitting on base_y."""
    for dx, height, colour in specs:
        dr.polygon([(cx + dx - half, base_y), (cx + dx, base_y - height),
                    (cx + dx + half, base_y)], fill=colour)


def smoke_puffs(dr, cx, top_y, radii, step, colour):
    """Grey puffs rising from top_y, each step pixels higher."""
    for i, rr in enumerate(radii):
        cy = top_y - i * step
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=colour)


def globe_art(dr, cx, cy, r):
    """A cracked globe: blue disc, meridians, red crack."""
    ink = PALETTE["ink"]
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PALETTE["ocean"],
               outline=ink, width=3)
    for k in (-0.55, 0.0, 0.55):
        x0 = cx + int(r * k)
        dr.arc([x0 - int(r * 0.45), cy - r, x0 + int(r * 0.45), cy + r],
               start=270, end=90, fill=PALETTE["pale"], width=2)
    dr.line([(cx - r, cy), (cx + r, cy)], fill=PALETTE["pale"], width=2)
    dr.ellipse([cx - r + 12, cy - r + 18, cx - 8, cy - 6],
               fill=PALETTE["land"])
    dr.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16],
               fill=PALETTE["land"])
    crack = [(cx + 6, cy - r + 4), (cx - 12, cy - r // 2), (cx + 10, cy - 4),
             (cx - 8, cy + r // 3), (cx + 4, cy + r - 8)]
    dr.line(crack, fill=PALETTE["red"], width=5, joint="curve")


def factory_art(dr, x, y, w, h):
    """Factory shed with flames and smoke, inside its box."""
    base = y + h - 20
    dr.rectangle([x, base, x + w, y + h], fill=PALETTE["wall"])
    dr.rectangle([x + 10, base - 52, x + w - 10, base],
                 fill=PALETTE["brick"])
    dr.polygon([(x + 10, base - 52), (x + w // 2, base - 78),
                (x + w - 10, base - 52)], fill=PALETTE["roof"])
    dr.rectangle([x + w - 30, base - 92, x + w - 18, base - 52],
                 fill=PALETTE["wall"])
    for i in range(3):
        wx = x + 24 + i * 34
        dr.rectangle([wx, base - 34, wx + 18, base - 12],
                     fill=PALETTE["dark"])
    fx = x + w // 2
    flame_row(dr, fx, base - 52,
              [(-18, 30, PALETTE["flame_a"]), (0, 42, PALETTE["flame_b"]),
               (18, 28, PALETTE["flame_c"])], half=11)
    smoke_puffs(dr, fx + 14, y + 24, (9, 12), 10, PALETTE["smoke"])


def ship_art(dr, x, y, w, h):
    """Cargo ship burning on the sea, inside its box."""
    sea_y = y + h - 24
    dr.rectangle([x, sea_y, x + w, y + h], fill=PALETTE["water"])
    dr.rectangle([x + 10, sea_y - 26, x + w - 10, sea_y],
                 fill=PALETTE["hull"])
    dr.rectangle([x + w // 2 - 8, sea_y - 44, x + w // 2 + 22, sea_y - 26],
                 fill=PALETTE["deck"])
    dr.rectangle([x + 16, sea_y - 38, x + 44, sea_y - 26],
                 fill=PALETTE["crate"])
    fx = x + w // 2 + 4
    flame_row(dr, fx, sea_y - 38,
              [(-16, 26, PALETTE["flame_a"]), (0, 36, PALETTE["flame_b"]),
               (16, 24, PALETTE["flame_c"])])
    smoke_puffs(dr, fx + 8, y + 22, (9, 12), 10, PALETTE["soot"])


def flats_art(dr, x, y, w, h):
    """Apartment block with a smoke column, inside its box."""
    top = y + 34
    dr.rectangle([x, top, x + w, y + h], fill=PALETTE["wall"])
    dr.rectangle([x, top, x + w, top + 12], fill=PALETTE["roof"])
    for r in range(2):
        for c in range(4):
            wx = x + 12 + c * (w // 4)
            wy = top + 22 + r * 26
            lit = (r + c) % 3 == 0
            dr.rectangle([wx, wy, wx + w // 6, wy + 16],
                         fill=PALETTE["lit"] if lit else PALETTE["dark"])
    dr.polygon([(x + w - 26, top), (x + w, top), (x + w, top + 26),
                (x + w - 40, top + 16)], fill=(40, 38, 34))
    smoke_puffs(dr, x + w - 14, y + 26, (9, 12, 14), 9, PALETTE["smoke"])


def chip_art(dr, x, y, s):
    """A computer chip, for the Nvidia story."""
    ink = PALETTE["ink"]
    dr.rectangle([x, y, x + s, y + s], fill=PALETTE["teal"],
                 outline=ink, width=2)
    dr.rectangle([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                 fill=PALETTE["navy"], outline=(255, 255, 255), width=2)
    for i in range(4):
        px = x + s // 4 + i * (s // 8)
        dr.line([(px, y - 8), (px, y)], fill=ink, width=2)
        dr.line([(px, y + s), (px, y + s + 8)], fill=ink, width=2)
        py = y + s // 4 + i * (s // 8)
        dr.line([(x - 8, py), (x, py)], fill=ink, width=2)
        dr.line([(x + s, py), (x + s + 8, py)], fill=ink, width=2)


def train_art(dr, x, y, w, h):
    """A small train front, for the India-Nepal story."""
    ink = PALETTE["ink"]
    dr.rectangle([x + 8, y + 10, x + w - 8, y + h - 14],
                 fill=PALETTE["blue"], outline=ink, width=2)
    dr.rectangle([x + 20, y + 22, x + w - 20, y + h // 2],
                 fill=PALETTE["pale"], outline=ink, width=2)
    dr.line([(x + w // 2, y + 22), (x + w // 2, y + h // 2)],
            fill=ink, width=2)
    for cx in (x + w // 3, x + 2 * w // 3):
        dr.ellipse([cx - 9, y + h - 32, cx + 9, y + h - 14],
                   fill=PALETTE["gold"], outline=ink, width=2)
    dr.line([(x, y + h - 6), (x + w, y + h - 6)], fill=ink, width=3)


def drop_art(dr, cx, cy, r):
    """A water drop with a warning mark, for the Gaza story."""
    dr.ellipse([cx - r, cy - r // 2, cx + r, cy + r],
               fill=PALETTE["ocean"], outline=PALETTE["ink"], width=2)
    dr.polygon([(cx, cy - r - 14), (cx - r, cy - r // 2 + 4),
                (cx + r, cy - r // 2 + 4)], fill=PALETTE["ocean"])
    dr.text((cx, cy - 6), "!", font=sans_bold(28), fill=(255, 255, 255),
            anchor="ma")


def render_front_page():
    page = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
    dr = ImageDraw.Draw(page)
    m = MARGIN

    # ---------- masthead ----------
    hline(dr, m, 30, SIDE - m, 3)
    dr.text((SIDE // 2, 44), "THE WORLD IN ONE PAGE",
            font=serif_bold(56), fill=PALETTE["ink"], anchor="mt")
    hline(dr, m, 116, SIDE - m, 2)
    dr.text((m, 126), "TUESDAY, 24 NOVEMBER 2026",
            font=sans_bold(19), fill=PALETTE["ink"])
    dr.text((SIDE - m, 126), "ONE DAY  ·  ONE PAGE",
            font=sans_bold(19), fill=PALETTE["ink"], anchor="rt")
    hline(dr, m, 154, SIDE - m, 3)

    # ---------- lead: COP31 ----------
    ly = 168
    dr.text((m, ly), "CLIMATE  ·  ANTALYA, TÜRKIYE",
            font=sans_bold(16), fill=PALETTE["red"])
    dr.text((m, ly + 26), "COP31 COLLAPSES",
            font=serif_bold(66), fill=PALETTE["ink"])
    dr.text((m, ly + 100), "Climate talks end with no deal at all",
            font=serif(26), fill=PALETTE["ink"])
    lead_body = ("Nearly 200 countries leave Antalya without an agreement "
                 "after the final draft drops every mention of fossil "
                 "fuels. The summit closes empty-handed, two days late.")
    draw_lines(dr, m, ly + 140, lead_body, sans(19), 560,
               PALETTE["ink"], 25)
    globe_art(dr, 862, ly + 122, 78)
    dr.text((862, ly + 216), "No deal on fossil fuels,",
            font=sans(15), fill=PALETTE["grey"], anchor="mt")
    dr.text((862, ly + 236), "no deal on climate finance.",
            font=sans(15), fill=PALETTE["grey"], anchor="mt")
    hline(dr, m, 452, SIDE - m, 2)

    # ---------- row 2: three stories ----------
    ry = 470
    stories = [
        (factory_art, "DISASTER  ·  CIKANDE, BANTEN",
         "Factory fire: 24 dead, 30 missing",
         "A blaze at a candy factory kills at least 24 workers. "
         "Rescuers keep searching for around 30 still missing."),
        (ship_art, "THE BALTIC  ·  GULF OF FINLAND",
         "Russian ship still burning",
         "The cargo ship Sparta II burns after a drone strike Finland "
         "says was likely Ukraine's."),
        (flats_art, "UKRAINE  ·  KYIV REGION",
         "Drone hits homes; several missing",
         "Russian drone and missile strikes hit the Kyiv region, "
         "killing several people and leaving others missing."),
    ]
    for idx, (art, kick, head, body) in enumerate(stories):
        cx = m + idx * 312
        after = card_title(dr, cx, ry, 300, kick, head, 27)
        art(dr, cx, after + 8, 300, 108)
        draw_lines(dr, cx, after + 128, body, sans(16), 300,
                   PALETTE["ink"], 21)
    hline(dr, m, 752, SIDE - m, 2)

    # ---------- row 3: three short stories ----------
    ry = 770
    shorts = [
        ("chip", 78, "TECH  ·  NVIDIA", "Huang is back as CEO",
         "Back as CEO less than two", "weeks after quitting."),
        ("train", 92, "SOUTH ASIA  ·  INDIA–NEPAL",
         "A new train, a $1.5bn package",
         "Modi and Shah flag off", "the Saryu-Kamala Express."),
        ("drop", 86, "GAZA  ·  THE POISONED LAND",
         "Toxic legacy of the war",
         "Oxfam: air, soil, water", "poisoned for decades."),
    ]
    for idx, (kind, tx, kick, head, line1, line2) in enumerate(shorts):
        cx = m + idx * 312
        after = card_title(dr, cx, ry, 300, kick, head, 24)
        if kind == "chip":
            chip_art(dr, cx + 8, after + 6, 52)
        elif kind == "train":
            train_art(dr, cx + 8, after + 4, 70, 60)
        else:
            drop_art(dr, cx + 40, after + 40, 24)
        dr.text((cx + tx, after + 10), line1, font=sans(16),
                fill=PALETTE["ink"])
        dr.text((cx + tx, after + 32), line2, font=sans(16),
                fill=PALETTE["ink"])
    hline(dr, m, 914, SIDE - m, 2)

    # ---------- ticker ----------
    ty = 924
    dr.text((m, ty), "ALSO ON 24 NOVEMBER",
            font=sans_bold(15), fill=PALETTE["red"])
    ticker = ("Lisbon marches against the cost of living  ·  Gukesh "
              "defends his chess crown vs Sindarov in Geneva  ·  "
              "Verstappen wins the Las Vegas GP  ·  Alcaraz takes the "
              "ATP Finals  ·  India–New Zealand Test drawn, Pant 128")
    draw_lines(dr, m, ty + 24, ticker, sans(15), SIDE - 2 * m,
               PALETTE["ink"], 20)
    hline(dr, m, 990, SIDE - m, 2)
    dr.text((SIDE // 2, 998),
            "All stories as reported on Tuesday 24 November 2026",
            font=sans(13), fill=PALETTE["grey"], anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    render_front_page()
