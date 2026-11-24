#!/usr/bin/env python3
"""Render the v2 news-image entry: THE WORLD IN PICTURES, 24 November 2026.

Fresh code, written in-session. Reads stories.json (same dir), draws a
1024x1024 illustrated news poster with PIL, writes entry.png.
All graphics are procedural (bars, map polygons, pictogram icons).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024

NAVY = (19, 41, 75)
PAPER = (251, 246, 236)
INK = (26, 26, 26)
GREY = (90, 90, 90)
RED = (180, 35, 24)
TEAL = (14, 124, 123)
GOLD = (201, 138, 27)
BLUE = (46, 111, 183)
GREEN = (30, 122, 52)
CARD = (255, 255, 255)
SEA = (215, 229, 238)
LAND = (169, 191, 203)
LAND_LINE = (110, 135, 150)
RULE = (200, 190, 170)

DJ = "/usr/share/fonts/truetype/dejavu"
LB = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font(f"{DJ}/DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font(f"{DJ}/DejaVuSans-Bold.ttf", s)
SANS = lambda s: font(f"{DJ}/DejaVuSans.ttf", s)


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


def rrect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


# ---------------------------------------------------------------- icons
def draw_icon(d, kind, x, y, s, color):
    """Draw a white pictogram of size s inside a coloured chip at (x, y)."""
    d.rectangle([x, y, x + s, y + s], fill=color)
    c = (255, 255, 255)
    p = s / 34.0  # scale unit
    ox, oy = x, y
    if kind == "chart":  # three bars
        for i, h in enumerate((14, 22, 30)):
            d.rectangle([ox + (5 + i * 10) * p, oy + (30 - h) * p,
                         ox + (11 + i * 10) * p, oy + 30 * p], fill=c)
    elif kind == "line":  # rising polyline
        pts = [(ox + 4 * p, oy + 28 * p), (ox + 12 * p, oy + 20 * p),
               (ox + 20 * p, oy + 22 * p), (ox + 30 * p, oy + 8 * p)]
        d.line(pts, fill=c, width=max(2, int(2.5 * p)))
        d.polygon([(ox + 30 * p, oy + 4 * p), (ox + 30 * p, oy + 12 * p),
                   (ox + 24 * p, oy + 8 * p)], fill=c)
    elif kind == "alert":  # triangle + !
        d.polygon([(ox + 17 * p, oy + 4 * p), (ox + 31 * p, oy + 29 * p),
                   (ox + 3 * p, oy + 29 * p)], fill=c)
        d.rectangle([ox + 15.5 * p, oy + 13 * p, ox + 18.5 * p, oy + 22 * p],
                    fill=color)
        d.ellipse([ox + 15.5 * p, oy + 24 * p, ox + 18.5 * p, oy + 27 * p],
                  fill=color)
    elif kind == "ban":  # circle + slash
        d.ellipse([ox + 4 * p, oy + 4 * p, ox + 30 * p, oy + 30 * p],
                  outline=c, width=max(2, int(3 * p)))
        d.line([(ox + 8 * p, oy + 26 * p), (ox + 26 * p, oy + 8 * p)],
               fill=c, width=max(2, int(3 * p)))
    elif kind == "court":  # columns + roof
        d.polygon([(ox + 3 * p, oy + 10 * p), (ox + 17 * p, oy + 3 * p),
                   (ox + 31 * p, oy + 10 * p)], fill=c)
        for i in range(3):
            d.rectangle([ox + (7 + i * 9) * p, oy + 13 * p,
                         ox + (11 + i * 9) * p, oy + 27 * p], fill=c)
        d.rectangle([ox + 4 * p, oy + 28 * p, ox + 30 * p, oy + 31 * p], fill=c)
    elif kind == "note":  # music note
        d.ellipse([ox + 7 * p, oy + 21 * p, ox + 15 * p, oy + 29 * p], fill=c)
        d.rectangle([ox + 13.5 * p, oy + 6 * p, ox + 15.5 * p, oy + 24 * p],
                    fill=c)
        d.polygon([(ox + 15 * p, oy + 6 * p), (ox + 27 * p, oy + 11 * p),
                   (ox + 15 * p, oy + 13 * p)], fill=c)
    elif kind == "soccer":  # ball
        d.ellipse([ox + 4 * p, oy + 4 * p, ox + 30 * p, oy + 30 * p],
                  outline=c, width=max(2, int(2.5 * p)))
        d.polygon([(ox + 17 * p, oy + 12 * p), (ox + 23 * p, oy + 16 * p),
                   (ox + 21 * p, oy + 23 * p), (ox + 13 * p, oy + 23 * p),
                   (ox + 11 * p, oy + 16 * p)], fill=c)
        for (ax, ay, bx, by) in ((17, 12, 17, 5), (23, 16, 29, 14),
                                 (21, 23, 26, 28), (13, 23, 8, 28),
                                 (11, 16, 5, 14)):
            d.line([(ox + ax * p, oy + ay * p), (ox + bx * p, oy + by * p)],
                   fill=c, width=max(1, int(2 * p)))
    elif kind == "basket":  # basketball
        d.ellipse([ox + 4 * p, oy + 4 * p, ox + 30 * p, oy + 30 * p],
                  outline=c, width=max(2, int(2.5 * p)))
        d.line([(ox + 4 * p, oy + 17 * p), (ox + 30 * p, oy + 17 * p)],
               fill=c, width=max(1, int(2 * p)))
        d.line([(ox + 17 * p, oy + 4 * p), (ox + 17 * p, oy + 30 * p)],
               fill=c, width=max(1, int(2 * p)))
        d.arc([ox + 4 * p, oy + 4 * p, ox + 30 * p, oy + 30 * p], 300, 60,
              fill=c, width=max(1, int(2 * p)))
    elif kind == "football":  # american football
        d.ellipse([ox + 3 * p, oy + 11 * p, ox + 31 * p, oy + 23 * p], fill=c)
        d.line([(ox + 13 * p, oy + 17 * p), (ox + 21 * p, oy + 17 * p)],
               fill=color, width=max(1, int(2 * p)))
        for lx in (14, 17, 20):
            d.line([(ox + lx * p, oy + 14 * p), (ox + lx * p, oy + 20 * p)],
                   fill=color, width=max(1, int(1.5 * p)))
    elif kind == "chip":  # microchip
        d.rectangle([ox + 10 * p, oy + 10 * p, ox + 24 * p, oy + 24 * p],
                    outline=c, width=max(2, int(2.5 * p)))
        d.rectangle([ox + 14 * p, oy + 14 * p, ox + 20 * p, oy + 20 * p],
                    fill=c)
        for i in range(3):
            for (ax, ay, bx, by) in (
                    (12 + i * 5, 5, 12 + i * 5, 10),
                    (12 + i * 5, 24, 12 + i * 5, 29),
                    (5, 12 + i * 5, 10, 12 + i * 5),
                    (24, 12 + i * 5, 29, 12 + i * 5)):
                d.line([(ox + ax * p, oy + ay * p), (ox + bx * p, oy + by * p)],
                       fill=c, width=max(1, int(2 * p)))
    elif kind == "scales":  # balance
        d.line([(ox + 17 * p, oy + 5 * p), (ox + 17 * p, oy + 28 * p)],
               fill=c, width=max(2, int(2.5 * p)))
        d.line([(ox + 6 * p, oy + 9 * p), (ox + 28 * p, oy + 9 * p)],
               fill=c, width=max(2, int(2.5 * p)))
        d.polygon([(ox + 3 * p, oy + 17 * p), (ox + 9 * p, oy + 17 * p),
                   (ox + 6 * p, oy + 10 * p)], fill=c)
        d.polygon([(ox + 25 * p, oy + 17 * p), (ox + 31 * p, oy + 17 * p),
                   (ox + 28 * p, oy + 10 * p)], fill=c)
        d.rectangle([ox + 11 * p, oy + 28 * p, ox + 23 * p, oy + 31 * p],
                    fill=c)
    elif kind == "globe":  # earth
        d.ellipse([ox + 4 * p, oy + 4 * p, ox + 30 * p, oy + 30 * p],
                  outline=c, width=max(2, int(2.5 * p)))
        d.ellipse([ox + 12 * p, oy + 4 * p, ox + 22 * p, oy + 30 * p],
                  outline=c, width=max(1, int(1.5 * p)))
        d.line([(ox + 4 * p, oy + 17 * p), (ox + 30 * p, oy + 17 * p)],
               fill=c, width=max(1, int(1.5 * p)))
    elif kind == "mountain":
        d.polygon([(ox + 3 * p, oy + 29 * p), (ox + 13 * p, oy + 9 * p),
                   (ox + 19 * p, oy + 20 * p), (ox + 24 * p, oy + 12 * p),
                   (ox + 31 * p, oy + 29 * p)], fill=c)
        d.polygon([(ox + 11 * p, oy + 12 * p), (ox + 15 * p, oy + 12 * p),
                   (ox + 13 * p, oy + 9 * p)], fill=color)
    elif kind == "ship":
        d.polygon([(ox + 4 * p, oy + 19 * p), (ox + 30 * p, oy + 19 * p),
                   (ox + 26 * p, oy + 27 * p), (ox + 8 * p, oy + 27 * p)],
                  fill=c)
        d.rectangle([ox + 8 * p, oy + 12 * p, ox + 14 * p, oy + 18 * p],
                    fill=c)
        d.rectangle([ox + 17 * p, oy + 9 * p, ox + 24 * p, oy + 18 * p],
                    fill=c)
        d.line([(ox + 21 * p, oy + 4 * p), (ox + 21 * p, oy + 9 * p)],
               fill=c, width=max(1, int(2 * p)))
    elif kind == "dome":  # capitol dome
        d.pieslice([ox + 8 * p, oy + 4 * p, ox + 26 * p, oy + 20 * p], 180, 360,
                   fill=c)
        d.rectangle([ox + 5 * p, oy + 20 * p, ox + 29 * p, oy + 23 * p], fill=c)
        for i in range(4):
            d.rectangle([ox + (7 + i * 6) * p, oy + 24 * p,
                         ox + (10 + i * 6) * p, oy + 30 * p], fill=c)
    elif kind == "bus":
        rrect(d, [ox + 3 * p, oy + 8 * p, ox + 31 * p, oy + 25 * p], 2, fill=c)
        for i in range(3):
            d.rectangle([ox + (7 + i * 8) * p, oy + 12 * p,
                         ox + (12 + i * 8) * p, oy + 18 * p], fill=color)
        for wx in (9, 25):
            d.ellipse([ox + wx * p, oy + 24 * p, ox + (wx + 5) * p,
                       oy + 29 * p], fill=c)

# ---------------------------------------------------------------- world map
# Rough continent outlines in (lon, lat); drawn equirectangular.
CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 70), (-80, 73), (-65, 60), (-55, 52), (-60, 47),
                 (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
                 (-95, 19), (-100, 16), (-105, 20), (-110, 23), (-115, 30),
                 (-125, 40), (-125, 48), (-135, 58), (-150, 60), (-165, 60)],
    "greenland": [(-55, 60), (-45, 60), (-40, 70), (-50, 76), (-60, 74),
                  (-58, 64)],
    "samerica": [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-52, 5),
                 (-50, 0), (-45, -5), (-35, -8), (-40, -20), (-48, -28),
                 (-55, -35), (-65, -41), (-70, -50), (-73, -53), (-70, -40),
                 (-73, -30), (-75, -20), (-80, -10), (-81, 0), (-80, 8)],
    "africa": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (12, -18), (9, -2), (9, 4),
               (-8, 5), (-15, 12)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53),
               (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60),
               (30, 62), (25, 65), (20, 70), (15, 70), (10, 68), (5, 62),
               (0, 58), (-5, 55), (-10, 50)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52),
           (-1, 51)],
    "asia": [(30, 62), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73),
             (140, 72), (160, 70), (178, 66), (170, 60), (162, 56),
             (158, 52), (142, 50), (140, 40), (130, 33), (127, 35),
             (122, 38), (120, 30), (115, 23), (108, 18), (105, 10),
             (100, 8), (98, 12), (95, 16), (92, 21), (88, 22), (85, 19),
             (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25),
             (62, 25), (57, 26), (53, 27), (50, 29), (48, 30), (44, 29),
             (40, 31), (36, 36), (33, 36), (30, 36), (28, 38)],
    "australia": [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
                  (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
                  (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
                  (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
                  (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
}


def lonlat_to_xy(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (83.0 - lat) / 139.0 * (y1 - y0)
    return x, y


def draw_map(d, box, pins):
    d.rectangle(box, fill=SEA)
    # graticule
    for lon in range(-150, 181, 30):
        x, _ = lonlat_to_xy(lon, 75, box)
        d.line([(x, box[1]), (x, box[3])], fill=(255, 255, 255), width=1)
    for lat in range(-30, 76, 30):
        _, y = lonlat_to_xy(0, lat, box)
        d.line([(box[0], y), (box[2], y)], fill=(255, 255, 255), width=1)
    for pts in CONTINENTS.values():
        xy = [lonlat_to_xy(lon, lat, box) for lon, lat in pts]
        d.polygon(xy, fill=LAND, outline=LAND_LINE)
    # region labels
    f = SANS_B(15)
    for label, lon, lat in (("AMERICAS", -100, 35), ("EUROPE", -8, 38),
                            ("AFRICA", 20, -25), ("ASIA", 105, 55),
                            ("PACIFIC", 165, -35)):
        x, y = lonlat_to_xy(lon, lat, box)
        d.text((x, y), label, font=f, fill=(70, 95, 115))
    # pins (clamped inside the map box so edge pins stay visible)
    nf = SANS_B(13)
    for pin in pins:
        x, y = lonlat_to_xy(pin["lon"], pin["lat"], box)
        x = min(max(x, box[0] + 13), box[2] - 13)
        y = min(max(y, box[1] + 13), box[3] - 13)
        r = 11
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        tw = d.textlength(str(pin["n"]), font=nf)
        d.text((x - tw / 2, y - 8), str(pin["n"]), font=nf,
               fill=(255, 255, 255))


def hexcol(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        S = json.load(fh)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 92], fill=NAVY)
    d.rectangle([0, 92, W, 96], fill=RED)
    d.text((28, 14), S["title"], font=SERIF_B(52), fill=(255, 255, 255))
    d.text((28, 70), S["date_line"], font=SANS_B(17), fill=(233, 196, 90))
    tag = S["tagline"]
    tw = d.textlength(tag, font=SANS(15))
    d.text((W - 28 - tw, 72), tag, font=SANS(15), fill=(200, 210, 225))

    # ---------------------------------------------------------------- lead
    lead = S["lead"]
    d.text((28, 106), lead["kicker"], font=SANS_B(15), fill=RED)
    d.text((28, 126), lead["headline"], font=SERIF_B(35), fill=NAVY)
    d.text((28, 168), lead["subline"], font=SANS(17), fill=INK)
    # stat tiles 2x2 (left) + bar chart (right)
    tile_x, tile_y = 28, 200
    tw_, th_ = 268, 56
    for i, st in enumerate(lead["stats"]):
        x = tile_x + (i % 2) * (tw_ + 12)
        y = tile_y + (i // 2) * (th_ + 10)
        d.rectangle([x, y, x + tw_, y + th_], fill=CARD, outline=RULE, width=1)
        d.rectangle([x, y, x + 5, y + th_], fill=TEAL if i < 3 else GOLD)
        d.text((x + 14, y + 5), st["label"], font=SANS_B(13), fill=GREY)
        d.text((x + 14, y + 22), st["change"] + "  " + st["value"],
               font=SANS_B(21), fill=NAVY if i < 3 else (150, 100, 10))
    # bar chart
    cx0, cy0, cx1, cy1 = 620, 196, 996, 322
    d.rectangle([cx0, cy0, cx1, cy1], fill=CARD, outline=RULE, width=1)
    d.text((cx0 + 12, cy0 + 8), lead["chart_title"], font=SANS_B(14),
           fill=GREY)
    bars = lead["chart"]
    base = cy1 - 30
    top = cy0 + 34
    bw = 74
    gap = 26
    x = cx0 + 34
    for b in bars:
        hgt = int((b["pct"] / 7.0) * (base - top))
        col = GREEN if b["label"] == "Nasdaq" else (BLUE if b["label"] == "S&P 500" else NAVY)
        d.rectangle([x, base - hgt, x + bw, base], fill=col)
        vl = "+%.2f%%" % b["pct"]
        vw = d.textlength(vl, font=SANS_B(15))
        d.text((x + (bw - vw) / 2, base - hgt + 6), vl, font=SANS_B(15),
               fill=(255, 255, 255))
        lw = d.textlength(b["label"], font=SANS_B(14))
        d.text((x + (bw - lw) / 2, base + 6), b["label"], font=SANS_B(14),
               fill=GREY)
        x += bw + gap
    d.line([(cx0 + 14, base), (cx1 - 14, base)], fill=GREY, width=1)

    # ---------------------------------------------------------------- map
    d.text((28, 338), S["map"]["title"], font=SANS_B(17), fill=NAVY)
    d.rectangle([28, 360, 996, 516], outline=RULE, width=1)
    draw_map(d, (28, 360, 996, 516), S["map"]["pins"])
    # key strip: 2 rows x 4 cols
    kf = SANS_B(14)
    pins = S["map"]["pins"]
    for i, pin in enumerate(pins):
        col, row = i % 4, i // 4
        x = 28 + col * 244
        y = 526 + row * 22
        label = "%d  %s" % (pin["n"], pin["label"])
        d.text((x, y), label, font=kf, fill=INK)

    # ---------------------------------------------------------------- grid
    d.text((28, 578), S["grid_title"], font=SANS_B(16), fill=NAVY)
    d.line([(28, 600), (996, 600)], fill=RED, width=2)
    gx, gy = 28, 610
    cw, chh, cgap = 236, 70, 6
    for i, card in enumerate(S["grid"]):
        col, row = i % 4, i // 4
        x = gx + col * (cw + cgap)
        y = gy + row * (chh + cgap)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=RULE, width=1)
        draw_icon(d, card["icon"], x + 8, y + 8, 34, hexcol(card["color"]))
        tx = x + 50
        twd = cw - 58
        hl = wrap(d, card["head"], SANS_B(14), twd)[:2]
        yy = y + 6
        for ln in hl:
            d.text((tx, yy), ln, font=SANS_B(14), fill=INK)
            yy += 17
        bl = wrap(d, card["body"], SANS(11), twd)[:2]
        for ln in bl:
            d.text((tx, yy), ln, font=SANS(11), fill=GREY)
            yy += 13

    # ---------------------------------------------------------------- date check
    dy0 = 914
    d.rectangle([28, dy0, 996, 996], outline=RED, width=3)
    d.rectangle([28, dy0, 996, dy0 + 20], fill=RED)
    d.text((40, dy0 + 2), S["date_check"]["title"], font=SANS_B(14),
           fill=(255, 255, 255))
    items = S["date_check"]["items"]
    itf = SANS(11)
    for i, it in enumerate(items):
        col, row = i % 3, i // 3
        x = 40 + col * 320
        y = dy0 + 24 + row * 11.5
        d.text((x, y), "×  " + it, font=itf, fill=(120, 20, 12))

    # ---------------------------------------------------------------- footer
    fsize = 12
    ff = SANS(fsize)
    fw = d.textlength(S["footer"], font=ff)
    while fw > 980 and fsize > 9:
        fsize -= 1
        ff = SANS(fsize)
        fw = d.textlength(S["footer"], font=ff)
    d.text(((W - fw) / 2, 1002), S["footer"], font=ff, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
