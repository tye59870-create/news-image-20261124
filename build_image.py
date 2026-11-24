#!/usr/bin/env python3
"""Build the entry image for make.fun bounty news-image-20261124.

Draws a 1024x1024 newspaper front page summing up the world news of
Tuesday 24 November 2026. Pure Pillow, deterministic, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (20, 20, 20)
RED = (176, 30, 40)
NAVY = (22, 35, 63)
GRAY = (90, 88, 82)
RULE = (20, 20, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


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


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 46  # side margin
    CW = W - 2 * M  # content width

    # ---- frame ----
    d.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=2)
    d.rectangle([26, 26, W - 27, H - 27], outline=RULE, width=1)

    # ---- masthead ----
    cx = W // 2
    # small globe
    gx, gy, r = cx, 74, 24
    d.ellipse([gx - r, gy - r, gx + r, gy + r], outline=INK, width=3)
    d.ellipse([gx - 10, gy - r, gx + 10, gy + r], outline=INK, width=2)
    d.line([gx - r, gy, gx + r, gy], fill=INK, width=2)
    d.arc([gx - r, gy - 14, gx + r, gy + 14], 200, 340, fill=INK, width=2)
    d.arc([gx - r, gy - 14, gx + r, gy + 14], 20, 160, fill=INK, width=2)

    y = 112
    y = draw_centered(d, cx, y, "THE WORLD IN ONE IMAGE", font(SERIF_B, 46))
    y += 12
    y = draw_centered(d, cx, y, "T U E S D A Y ,  2 4  N O V E M B E R  2 0 2 6",
                      font(SANS_B, 19), fill=RED)
    y += 16
    d.rectangle([M, y, W - M, y + 4], fill=RULE)
    y += 12
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 20

    # ---- lead story: Nvidia / Huang ----
    d.text((M, y), "MARKETS  ·  NVIDIA", font=font(SANS_B, 21), fill=RED)
    y += 34
    d.text((M, y), "HUANG IS BACK", font=font(SERIF_B, 76), fill=INK)
    y += 96
    deck = ("Nvidia reinstates Jensen Huang as chief executive 12 days after "
            "his exit; shares soar 31% \u2014 adding nearly $1 trillion in "
            "value \u2014 as the Nasdaq jumps 6.5% in its best day since April.")
    for line in wrap(d, deck, font(SERIF, 26), CW):
        d.text((M, y), line, font=font(SERIF, 26), fill=INK)
        y += 32
    y += 14
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 20

    # ---- 2x2 grid ----
    stories = [
        ("LIBYA",
         "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
         "Seven sea drones sink the corvette Merkury at Benghazi; Zelenskyy "
         "claims the strike \u2014 and a hit on the cargo ship MV Angara."),
        ("IRAN",
         "IRAN PUTS EUROPE IN MISSILE RANGE",
         "Tehran claims its missiles now reach 4,500 km, more than double "
         "the old limit; three tankers hit mines in the Strait of Hormuz."),
        ("MANCHESTER",
         "12,000 FLEE CONCERT IN GAS SCARE",
         "An unknown substance, first feared to be tear gas, clears Don "
         "Toliver\u2019s show at Co-op Live; 89 treated, one in hospital."),
        ("NORTH KOREA",
         "KIM SNUBS TRUMP\u2019S OVERTURES",
         "Trump\u2019s bids to revive talks with Kim Jong Un have been "
         "ignored, the WSJ reports, as Pyongyang expands its arsenal."),
    ]
    col_w = (CW - 26) // 2
    row_h = 186
    gx0 = [M, M + col_w + 26]
    gy0 = y
    for i, (kicker, head, body) in enumerate(stories):
        x = gx0[i % 2]
        yy = gy0 + (i // 2) * row_h
        d.text((x, yy), kicker, font=font(SANS_B, 19), fill=RED)
        yy += 28
        for line in wrap(d, head, font(SANS_B, 29), col_w)[:2]:
            d.text((x, yy), line, font=font(SANS_B, 29), fill=INK)
            yy += 34
        yy += 4
        for line in wrap(d, body, font(SANS, 19), col_w)[:3]:
            d.text((x, yy), line, font=font(SANS, 19), fill=(52, 50, 46))
            yy += 24
    y = gy0 + 2 * row_h - 8
    d.rectangle([M, y, W - M, y + 1], fill=RULE)
    y += 16

    # ---- ticker bar ----
    bar_h = 84
    d.rectangle([M, y, W - M, y + bar_h], fill=NAVY)
    ticker = ("ALSO IN THE NEWS:   O\u2019Hare ground stop snarls Thanksgiving "
              "travel   \u2022   Iranian singer gets 74 lashes for hijab-free "
              "concert   \u2022   Oxfam: Gaza soil and water toxic for decades"
              "   \u2022   30+ missing after Indonesia factory fire   \u2022   "
              "COP31 fallout: first full collapse since 2009")
    ty = y + 10
    for line in wrap(d, ticker, font(SANS, 19), CW - 32):
        d.text((M + 16, ty), line, font=font(SANS, 19), fill=(255, 255, 255))
        ty += 24
    y += bar_h + 10

    # ---- footer ----
    draw_centered(d, cx, y, "Compiled from the day\u2019s reporting  ·  24 November 2026",
                  font(SANS, 16), fill=GRAY)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
