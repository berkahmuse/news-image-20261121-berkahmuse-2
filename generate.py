#!/usr/bin/env python3
"""Build-time generator for the entry image (NOT run by the entry).

Draws a one-page newspaper front page summing up Saturday 21 November
2026 world news, using only Pillow + DejaVu fonts, all artwork drawn here
from rectangles, polygons and circles -- no photos, no copied art.

Stories (each verified against independent reporting dated 21 Nov 2026):
 1. Houthi missiles at Riyadh intercepted before dawn, third night
    (Reuters, Al Jazeera, AFP).
 2. Bitcoin crashes below $60,000, lowest since September 2024
    (CoinGecko, Bloomberg via BigGo, 21 Nov).
 3. Tanker hit by unknown projectile off Oman's Khasab, Strait of Hormuz
    (Reuters / UKMTO, Saturday 21 Nov).
 4. COP31 climate talks in Antalya run past deadline into Saturday
    (AP, Reuters, theclimatewatch).
 5. Fire at Hartha power plant near Basra: 4 killed, 30 injured (Reuters).
 6. M6.9 earthquake in Peru's Andes, 00:09 UTC 21 Nov (USGS).
 7. Briefs: FBI database reportedly hacked (Reuters, 21 Nov); Vietnam
    passes land law on Saturday (Reuters); NATO chief Rutte due in
    Warsaw today (BBC, ISW).

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
def scene_riyadh(w, h):
    """Riyadh skyline at night, missile intercepts overhead (lead scene)."""
    im, d = new_scene(w, h, (10, 34, 44))
    for i in range(60):
        sx = (i * 53 + 17) % w
        sy = (i * 29 + 7) % 34 + 4
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 230, 240))
    d.ellipse([w - 66, 10, w - 32, 44], fill=(235, 230, 210))
    base = h
    x, i = 0, 0
    while x < w:
        bw = 26 + (i * 13) % 22
        bh = 34 + (i * 17) % 34
        d.rectangle([x, base - bh, x + bw, base], fill=(4, 18, 26))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(x + 6, x + bw - 5, 12):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 200, 90))
        x += bw + 6
        i += 1
    cx, cy = w // 2, 52
    d.line([(cx - 110, 24), (cx, cy)], fill=(255, 120, 60), width=3)
    d.line([(cx + 110, 66), (cx, cy)], fill=(120, 220, 255), width=3)
    d.line([(cx - 90, 68), (cx, cy)], fill=(120, 220, 255), width=3)
    burst(d, cx, cy, 15)
    d.text((12, 6), "RIYADH  •  3RD NIGHT", font=font(SANS_B, 14),
           fill=(200, 220, 225))
    return im


def scene_bitcoin(w, h):
    im, d = new_scene(w, h, (255, 250, 244))
    d.rectangle([0, 0, w - 1, h - 1], outline=(200, 190, 170), width=1)
    for gy in range(18, h - 6, 20):
        d.line([(8, gy), (w - 8, gy)], fill=(232, 224, 210), width=1)
    pts = [(14, 26), (58, 22), (102, 30), (146, 28), (190, 40),
           (234, 44), (278, 58), (322, 56), (366, 72), (410, h - 16)]
    d.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 4), (ex - 6, ey + 12)], fill=RED)
    d.ellipse([w - 58, 8, w - 14, 52], fill=(247, 147, 26))
    d.text((w - 45, 16), "B", font=font(SANS_B, 26), fill=(255, 255, 255))
    d.text((14, h - 26), "BTC  -10%", font=font(SANS_B, 16), fill=RED)
    return im


def scene_tanker(w, h):
    im, d = new_scene(w, h, (16, 52, 74))
    d.ellipse([w - 70, 8, w - 40, 38], fill=(235, 230, 210))
    for sx, sy in [(24, 12), (70, 26), (130, 10), (190, 22), (250, 14),
                   (300, 24), (360, 12), (420, 26)]:
        if sx < w:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 230, 240))
    sea = h - 22
    d.rectangle([0, sea, w, h], fill=(10, 38, 58))
    for wx in range(0, w, 34):
        d.line([(wx, sea + 6), (wx + 16, sea + 6)], fill=(90, 140, 170), width=2)
    hx, hy = 60, sea - 26
    d.rectangle([hx, hy, hx + 300, sea], fill=(30, 30, 34))
    d.rectangle([hx, hy - 14, hx + 300, hy], fill=(200, 60, 40))
    for cx in range(hx + 16, hx + 290, 34):
        d.rectangle([cx, hy - 12, cx + 22, hy - 2], fill=(240, 200, 90))
    d.rectangle([hx + 310, sea - 44, hx + 336, sea], fill=(60, 60, 66))
    burst(d, hx + 300, sea - 8, 13)
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


def scene_basra(w, h):
    im, d = new_scene(w, h, (64, 32, 24))
    d.ellipse([w // 2 - 24, 6, w // 2 + 24, 54], fill=(255, 120, 40))
    for sx, sy, sr in [(20, 12, 6), (60, 20, 8), (120, 10, 7), (200, 18, 6),
                       (260, 12, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 80, 60))
    base = h
    for tx in (30, 110, 190):
        d.polygon([(tx, base), (tx + 18, 26), (tx + 52, 26), (tx + 70, base)],
                  fill=(40, 22, 16))
        d.ellipse([tx + 18, 20, tx + 52, 32], fill=(90, 50, 30))
    burst(d, 150, base - 12, 16)
    d.text((12, h - 22), "HARTHA, IRAQ", font=font(SANS_B, 13),
           fill=(255, 200, 150))
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
    d.text((M, y), "GULF  •  LEAD STORY", font=font(SANS_B, 16), fill=RED)
    y += 26
    img.paste(scene_riyadh(CW, 112), (M, y))
    y += 112 + 8
    head = wrap(d, "HOUTHI MISSILES AT RIYADH DOWNED ON THIRD NIGHT",
                font(SERIF, 34), CW)
    y = text_block(d, M, y, head, font(SERIF, 34), leading=41)
    deck = wrap(d, "Three ballistic missiles intercepted before dawn on Saturday; "
                "Houthis threaten ports and a power station.", font(SANS, 17), CW)
    y = text_block(d, M, y + 2, deck, font(SANS, 17), leading=22)
    y += 6
    hrule(d, M, W - M, y, 2)
    y += 10

    # ---- row 2: two half panels ----
    half = (CW - 16) // 2
    row2_start = y
    row2_tops = []
    for px, kick, headline, deck, scene in [
        (M, "MARKETS", "BITCOIN CRASHES BELOW $60,000",
         "Lowest since September 2024; about $2bn in leveraged bets wiped out in a day.",
         scene_bitcoin),
        (M + half + 16, "SHIPPING", "TANKER HIT IN STRAIT OF HORMUZ",
         "Unknown projectile strikes vessel off Oman; no injuries reported.",
         scene_tanker),
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
        ("DISASTER  •  IRAQ", "FIRE AT BASRA POWER PLANT KILLS FOUR",
         "At least four dead, 30 injured at Hartha station.", scene_basra),
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
        ("CYBER", "FBI database reportedly hacked amid US outages."),
        ("POLITICS", "Vietnam passes land-seizure fast-track."),
        ("NATO", "NATO chief due in Warsaw today."),
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
                 "Sources: Reuters  •  Al Jazeera  •  BBC  •  USGS  •  CoinGecko",
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
