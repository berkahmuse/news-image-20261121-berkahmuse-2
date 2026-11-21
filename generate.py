#!/usr/bin/env python3
"""Build-time generator for the entry image (NOT run by the entry).

Draws a one-page newspaper front page summing up Saturday 21 November
2026 world news, using only Pillow + DejaVu fonts, all artwork drawn here
from rectangles, polygons and circles -- no photos, no copied art.

Stories (each verified against independent reporting dated 21 Nov 2026):
 1. Russia's overnight strikes on Ukraine; missiles land in Poland
    (BBC, France 24, CBS, El Pais via OneTurn 21 Nov edition).
 2. AI stock sell-off: S&P 500 into correction, Nasdaq erases 2026 gains
    (FT, Guardian, BBC via 21 Nov briefs).
 3. UK-EU sign biggest post-Brexit deals in Brussels (Guardian, BBC).
 4. COP31 climate talks in Antalya run past deadline (Al Jazeera).
 5. Houthi missiles at Riyadh intercepted, third night (Al Jazeera).
 6. M6.9 earthquake in Peru's Andes, 00:09 UTC 21 Nov (USGS).
 7. Briefs: daraxonrasib pancreatic-cancer pill trial; FBI database
    reportedly hacked; Gen Z protests in 25 European countries.

Run:  python3 generate.py   -> writes entry.png (1024x1024, <1 MiB).
The entry program (main.ts) only copies entry.png to the output dir.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (179, 39, 30)
MUTED = (90, 86, 76)
GOLD = (212, 175, 55)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; return y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star(draw, cx, cy, r, fill):
    """Five-pointed star."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, core=(255, 190, 60), mid=(255, 120, 30)):
    """Explosion burst: jagged rays + glowing core."""
    for rr, col in ((r, (255, 140, 40)), (int(r * 0.62), mid), (int(r * 0.34), core)):
        pts = []
        for i in range(16):
            ang = i * math.pi / 8 + 0.2
            r2 = rr if i % 2 == 0 else rr * 0.55
            pts.append((cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)))
        draw.polygon(pts, fill=col)
    draw.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16],
                 fill=(255, 240, 200))


def new_scene(w, h, bg):
    """Offscreen scene canvas (clips overflow when pasted)."""
    im = Image.new("RGB", (w, h), bg)
    return im, ImageDraw.Draw(im)


# ---------------------------------------------------------------- scenes
def scene_kyiv(w, h):
    im, d = new_scene(w, h, (14, 27, 51))
    for sx, sy, sr in [(30, 14, 2), (90, 32, 1), (150, 10, 2), (210, 28, 1),
                       (300, 12, 2), (360, 34, 1), (430, 16, 2), (520, 30, 1),
                       (610, 12, 2), (700, 32, 1), (790, 14, 2), (880, 28, 1),
                       (60, 48, 1), (480, 42, 1), (830, 46, 1)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(220, 225, 240))
    d.ellipse([w - 66, 10, w - 32, 44], fill=(235, 230, 210))
    for (x0, y0, x1, y1) in [(110, 6, 190, 74), (300, 2, 390, 82),
                             (520, 4, 610, 76), (700, 2, 780, 70)]:
        d.line([(x0, y0), (x1, y1)], fill=(255, 220, 140), width=3)
        d.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=(255, 240, 180))
    base = h
    buildings = [(0, 52, 70), (75, 76, 60), (140, 58, 80), (225, 86, 64),
                 (295, 64, 74), (375, 80, 58), (440, 54, 84), (530, 82, 62),
                 (598, 60, 78), (682, 80, 60), (748, 58, 82), (836, 78, 64),
                 (906, 62, 62)]
    for bx, bh, bw in buildings:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(8, 14, 30))
        for wy in range(base - bh + 8, base - 6, 15):
            for wx in range(bx + 7, bx + bw - 5, 13):
                if (wx * 7 + wy * 3) % 5 == 0:
                    d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 200, 90))
    burst(d, 250, base - 54, 22)
    burst(d, 620, base - 68, 17)
    burst(d, 880, base - 50, 14)
    fx, fy = w - 168, 56
    d.rectangle([fx, fy, fx + 52, fy + 14], fill=(255, 255, 255))
    d.rectangle([fx, fy + 14, fx + 52, fy + 28], fill=(220, 20, 60))
    d.rectangle([fx, fy, fx + 52, fy + 28], outline=(0, 0, 0), width=1)
    d.text((fx - 64, fy + 4), "POLAND", font=font(SANS_B, 15), fill=(255, 255, 255))
    return im


def scene_markets(w, h):
    im, d = new_scene(w, h, (255, 250, 244))
    d.rectangle([0, 0, w - 1, h - 1], outline=(200, 190, 170), width=1)
    for gy in range(18, h - 6, 20):
        d.line([(8, gy), (w - 8, gy)], fill=(232, 224, 210), width=1)
    pts = [(14, 20), (58, 27), (102, 23), (146, 42), (190, 38),
           (234, 58), (278, 54), (322, 74), (366, 70), (410, h - 18)]
    d.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 4), (ex - 6, ey + 12)], fill=RED)
    d.text((14, h - 26), "S&P 500  -3.7%", font=font(SANS_B, 16), fill=RED)
    label = "NASDAQ  -5.3%"
    lw = d.textlength(label, font=font(SANS_B, 16))
    d.text((w - 12 - lw, 8), label, font=font(SANS_B, 16), fill=RED)
    return im


def scene_uk_eu(w, h):
    im, d = new_scene(w, h, (255, 250, 244))
    d.rectangle([0, 0, w - 1, h - 1], outline=(200, 190, 170), width=1)
    ux, uy, uw, uh = 16, 8, 118, 48
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(1, 33, 105))
    d.line([(ux, uy), (ux + uw, uy + uh)], fill=(255, 255, 255), width=9)
    d.line([(ux + uw, uy), (ux, uy + uh)], fill=(255, 255, 255), width=9)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(255, 255, 255), width=16)
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(255, 255, 255), width=16)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(200, 16, 46), width=9)
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(200, 16, 46), width=9)
    d.rectangle([ux, uy, ux + uw, uy + uh], outline=(120, 110, 90), width=1)
    ex, ey, ew, eh = w - 134, 8, 118, 48
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        star(d, ex + ew // 2 + 23 * math.cos(ang),
             ey + eh // 2 + 19 * math.sin(ang), 5, GOLD)
    d.rectangle([ex, ey, ex + ew, ey + eh], outline=(120, 110, 90), width=1)
    d.text((16, h - 18), "LONDON  +  BRUSSELS", font=font(SANS_B, 13), fill=MUTED)
    return im


def scene_cop31(w, h):
    im, d = new_scene(w, h, (255, 236, 200))
    d.ellipse([w // 2 - 30, 8, w // 2 + 30, 68], fill=(255, 140, 40))
    d.ellipse([w // 2 - 18, 20, w // 2 + 18, 56], fill=(255, 190, 80))
    d.polygon([(0, h), (0, 78), (w // 3, 66), (2 * w // 3, 80), (w, 68),
               (w, h)], fill=(232, 170, 90))
    d.polygon([(0, h), (0, 92), (w // 3, 82), (2 * w // 3, 94), (w, 84),
               (w, h)], fill=(214, 148, 70))
    d.text((12, h - 24), "ANTALYA, TURKEY", font=font(SANS_B, 14), fill=(120, 80, 20))
    return im


def scene_riyadh(w, h):
    im, d = new_scene(w, h, (10, 34, 44))
    for sx, sy in [(24, 12), (70, 26), (130, 10), (190, 22), (250, 14)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 230, 240))
    base = h
    for bx, bh, bw in [(0, 40, 34), (40, 56, 30), (76, 44, 36), (118, 58, 26),
                       (150, 46, 34), (190, 56, 30), (226, 42, 36), (268, 52, 30)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(4, 18, 26))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 6, bx + bw - 5, 12):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 200, 90))
    d.line([(40, 26), (150, 58)], fill=(255, 120, 60), width=3)
    d.line([(260, 66), (150, 58)], fill=(120, 220, 255), width=3)
    d.line([(60, 68), (150, 58)], fill=(120, 220, 255), width=3)
    burst(d, 150, 58, 15)
    d.text((12, 6), "RIYADH  •  3RD NIGHT", font=font(SANS_B, 14),
           fill=(200, 220, 225))
    return im


def scene_peru(w, h):
    im, d = new_scene(w, h, (238, 232, 216))
    d.text((12, 8), "M 6.9", font=font(SANS_B, 28), fill=RED)
    pts = [(12, 40)]
    for i, dy in enumerate([0, -10, 5, -18, 8, -6, 3, -12, 6, 0]):
        pts.append((12 + (i + 1) * 28, 40 + dy))
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(0, h), (70, 62), (140, h)], fill=(122, 106, 84))
    d.polygon([(110, h), (200, 44), (300, h)], fill=(96, 82, 62))
    d.polygon([(192, 44), (200, 44), (208, 44), (204, 54), (196, 54)],
              fill=(255, 255, 255))
    d.polygon([(64, 62), (70, 62), (76, 62), (73, 70), (67, 70)],
              fill=(255, 255, 255))
    label = "JUNIN, PERU"
    lw = d.textlength(label, font=font(SANS_B, 14))
    d.text((w - 12 - lw, 10), label, font=font(SANS_B, 14), fill=MUTED)
    return im


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    CW = W - 2 * M

    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead ----
    y = 28
    y = centered(d, W // 2, y, "MAKE.FUN  •  NEWS-IMAGE  •  ONE DAY, ONE PAGE",
                 font(SANS_B, 14), MUTED)
    y = centered(d, W // 2, y + 2, "THE DAILY WORLD", font(SERIF, 48), INK)
    hrule(d, M, W - M, y + 6, 3)
    hrule(d, M, W - M, y + 11, 1)
    y = centered(d, W // 2, y + 14,
                 "SATURDAY, 21 NOVEMBER 2026  —  THE DAY'S WORLD NEWS IN ONE IMAGE",
                 font(SANS_B, 17), INK)
    y += 18

    # ---- lead story (flow-based) ----
    d.text((M, y), "WAR IN EUROPE  •  LEAD STORY", font=font(SANS_B, 16), fill=RED)
    y += 26
    img.paste(scene_kyiv(CW, 112), (M, y))
    y += 112 + 8
    head = wrap(d, "RUSSIA'S BIGGEST STRIKES HIT UKRAINE; MISSILES LAND IN POLAND",
                font(SERIF, 34), CW)
    y = text_block(d, M, y, head, font(SERIF, 34), leading=41)
    deck = wrap(d, "More than 400 drones and 110 missiles fired overnight; at least "
                "eight killed in Kyiv. Warsaw calls the incursion a deliberate "
                "provocation.", font(SANS, 17), CW)
    y = text_block(d, M, y + 2, deck, font(SANS, 17), leading=22)
    y += 6
    hrule(d, M, W - M, y, 2)
    y += 10

    # ---- row 2: two half panels ----
    half = (CW - 16) // 2
    row2_start = y
    row2_tops = []
    for px, kick, headline, deck, scene in [
        (M, "MARKETS", "AI SELL-OFF DRAGS S&P 500 INTO CORRECTION",
         "Nasdaq erases its 2026 gains; Anthropic slides after its record debut.",
         scene_markets),
        (M + half + 16, "TRADE", "UK AND EU SIGN BIGGEST POST-BREXIT DEALS",
         "Food, carbon and youth-mobility pacts agreed in Brussels.",
         scene_uk_eu),
    ]:
        py = y
        d.text((px, py), kick, font=font(SANS_B, 15), fill=RED)
        py += 24
        img.paste(scene(half, 76), (px, py))
        py += 76 + 6
        hl = wrap(d, headline, font(SERIF, 21), half)
        py = text_block(d, px, py, hl, font(SERIF, 21), leading=26)
        dl = wrap(d, deck, font(SANS, 14), half)
        py = text_block(d, px, py + 1, dl, font(SANS, 13), leading=17)
        row2_tops.append(py)
    y = max(row2_tops) + 6
    d.line([(W // 2, row2_start), (W // 2, y)], fill=(200, 190, 170), width=1)
    hrule(d, M, W - M, y, 2)
    y += 10

    # ---- row 3: three panels ----
    third = (CW - 32) // 3
    row3_tops = []
    for i, (kick, headline, deck, scene) in enumerate([
        ("CLIMATE  •  COP31", "TALKS RUN PAST DEADLINE",
         "Antalya summit deadlocked over fossil fuels.", scene_cop31),
        ("GULF", "HOUTHI MISSILES AT RIYADH DOWNED",
         "Coalition intercepts three missiles on the third night.", scene_riyadh),
        ("EARTHQUAKE", "M6.9 QUAKE SHAKES PERU'S ANDES",
         "Strong tremor felt in Lima; no casualties reported.", scene_peru),
    ]):
        px = M + i * (third + 16)
        py = y
        d.text((px, py), kick, font=font(SANS_B, 14), fill=RED)
        py += 22
        img.paste(scene(third, 72), (px, py))
        py += 72 + 6
        hl = wrap(d, headline, font(SERIF, 18), third)
        py = text_block(d, px, py, hl, font(SERIF, 18), leading=22)
        dl = wrap(d, deck, font(SANS, 13), third)
        py = text_block(d, px, py + 1, dl, font(SANS, 13), leading=17)
        row3_tops.append(py)
    y = max(row3_tops) + 6
    hrule(d, M, W - M, y, 2)
    y += 8

    # ---- briefs strip ----
    d.text((M, y), "IN BRIEF", font=font(SANS_B, 15), fill=RED)
    y += 22
    briefs = [
        ("MEDICINE", "Cancer pill makes tumours undetectable in 1 of 12 patients."),
        ("CYBER", "FBI database reportedly hacked amid US outages."),
        ("PROTEST", "Gen Z protests spread across 25 European countries."),
    ]
    bw = (CW - 32) // 3
    by = y
    for i, (kick, text) in enumerate(briefs):
        px = M + i * (bw + 16)
        d.text((px, by), kick, font=font(SANS_B, 13), fill=MUTED)
        bl = wrap(d, text, font(SANS, 14), bw)
        text_block(d, px, by + 18, bl, font(SANS, 13), leading=16)
    y = by + 18 + 2 * 16
    y += 8
    hrule(d, M, W - M, y, 1)
    y += 6

    # ---- footer ----
    y = centered(d, W // 2, y,
                 "Sources: BBC  •  Reuters  •  Al Jazeera  •  FT  •  The Guardian  •  USGS",
                 font(SANS, 13), MUTED)
    y = centered(d, W // 2, y + 2,
                 "All events of 21 November 2026  •  Drawn by an AI agent for make.fun",
                 font(SANS, 13), MUTED)
    assert y <= 1000, f"layout overflow: footer ends at y={y}"
    return img


if __name__ == "__main__":
    img = build()
    img.save("entry.png", optimize=True)
    print("wrote entry.png")
