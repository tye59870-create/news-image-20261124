#!/usr/bin/env python3
"""Render the 24 November 2026 front page for make.fun news-image-20261124.

A fresh Pillow renderer for the daily news-image bounty: it draws a
newspaper front page for Tuesday 24 November 2026 -- masthead, lead story,
four-item grid and a news ticker -- at 1024 by 1024 pixels. No network
access, no randomness, no input files: the same run always draws the
same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
BACKGROUND = (251, 247, 238)
FOREGROUND = (20, 20, 20)
ACCENT = (176, 30, 40)
DEEP = (22, 35, 63)
MUTED = (90, 88, 82)
BODY_INK = (52, 50, 46)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GUTTER = 46            # side margin
FRAME_OUT = 18         # outer frame inset
FRAME_IN = 26          # inner frame inset
CONTENT_W = PAGE_W - 2 * GUTTER
GRID_ROW_H = 186       # height of one grid row
TICKER_H = 84          # height of the navy ticker bar

LEAD = {
    "kicker": "MARKETS  ·  NVIDIA",
    "headline": "HUANG IS BACK",
    "deck": ("Nvidia reinstates Jensen Huang as chief executive 12 days after "
             "his exit; shares soar 31% \u2014 adding nearly $1 trillion in "
             "value \u2014 as the Nasdaq jumps 6.5% in its best day since April."),
}

GRID = [
    {
        "kicker": "LIBYA",
        "headline": "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
        "body": ("Seven sea drones sink the corvette Merkury at Benghazi; "
                 "Zelenskyy claims the strike \u2014 and a hit on the cargo "
                 "ship MV Angara."),
    },
    {
        "kicker": "IRAN",
        "headline": "IRAN PUTS EUROPE IN MISSILE RANGE",
        "body": ("Tehran claims its missiles now reach 4,500 km, more than "
                 "double the old limit; three tankers hit mines in the "
                 "Strait of Hormuz."),
    },
    {
        "kicker": "MANCHESTER",
        "headline": "12,000 FLEE CONCERT IN GAS SCARE",
        "body": ("An unknown substance, first feared to be tear gas, clears "
                 "Don Toliver\u2019s show at Co-op Live; 89 treated, one in "
                 "hospital."),
    },
    {
        "kicker": "NORTH KOREA",
        "headline": "KIM SNUBS TRUMP\u2019S OVERTURES",
        "body": ("Trump\u2019s bids to revive talks with Kim Jong Un have been "
                 "ignored, the WSJ reports, as Pyongyang expands its "
                 "arsenal."),
    },
]

TICKER = ("ALSO IN THE NEWS:   O\u2019Hare ground stop snarls Thanksgiving "
          "travel   \u2022   Iranian singer gets 74 lashes for hijab-free "
          "concert   \u2022   Oxfam: Gaza soil and water toxic for decades"
          "   \u2022   30+ missing after Indonesia factory fire   \u2022   "
          "COP31 fallout: first full collapse since 2009")

FOOTER = "Compiled from the day\u2019s reporting  ·  24 November 2026"


def load(path, size):
    """Load a TrueType font at the requested size."""
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, font, width):
    """Split text into as many lines as needed to fit inside width."""
    done = []
    current = ""
    for word in text.split(" "):
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                done.append(current)
            current = word
    if current:
        done.append(current)
    return done


def put_centred(draw, cx, y, text, font, fill=FOREGROUND):
    """Draw one centred line; return the y just below it."""
    wide = draw.textlength(text, font=font)
    draw.text((cx - wide / 2, y), text, font=font, fill=fill)
    return y + font.size


def hrule(draw, y, x0=GUTTER, x1=PAGE_W - GUTTER, weight=1, fill=FOREGROUND):
    """Draw a horizontal rule of the given weight."""
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)
    return y + weight


def draw_globe(draw, cx, cy, radius):
    """A small line-art globe for the masthead."""
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 outline=FOREGROUND, width=3)
    draw.ellipse([cx - 10, cy - radius, cx + 10, cy + radius],
                 outline=FOREGROUND, width=2)
    draw.line([cx - radius, cy, cx + radius, cy], fill=FOREGROUND, width=2)
    draw.arc([cx - radius, cy - 14, cx + radius, cy + 14], 200, 340,
             fill=FOREGROUND, width=2)
    draw.arc([cx - radius, cy - 14, cx + radius, cy + 14], 20, 160,
             fill=FOREGROUND, width=2)


def draw_masthead(draw):
    """Globe, title and date; returns the y below the double rule."""
    cx = PAGE_W // 2
    draw_globe(draw, cx, 74, 24)
    y = put_centred(draw, cx, 112, "THE WORLD IN ONE IMAGE",
                    load(SERIF_BOLD, 46))
    y += 12
    y = put_centred(draw, cx, y, "T U E S D A Y ,  2 4  N O V E M B E R  2 0 2 6",
                    load(SANS_BOLD, 19), fill=ACCENT)
    y += 16
    y = hrule(draw, y, weight=4)
    y += 12
    y = hrule(draw, y, weight=1)
    return y + 20


def draw_lead(draw, y):
    """The lead story: kicker, headline and deck; returns the y below it."""
    draw.text((GUTTER, y), LEAD["kicker"], font=load(SANS_BOLD, 21),
              fill=ACCENT)
    y += 34
    draw.text((GUTTER, y), LEAD["headline"], font=load(SERIF_BOLD, 76),
              fill=FOREGROUND)
    y += 96
    deck_font = load(SERIF, 26)
    for line in fit_lines(draw, LEAD["deck"], deck_font, CONTENT_W):
        draw.text((GUTTER, y), line, font=deck_font, fill=FOREGROUND)
        y += 32
    y += 14
    y = hrule(draw, y)
    return y + 20


def draw_grid(draw, y):
    """The four supporting stories in two columns and two rows."""
    col_w = (CONTENT_W - 26) // 2
    left_x = [GUTTER, GUTTER + col_w + 26]
    row_h = GRID_ROW_H
    for idx, story in enumerate(GRID):
        x = left_x[idx % 2]
        yy = y + (idx // 2) * row_h
        draw.text((x, yy), story["kicker"], font=load(SANS_BOLD, 19),
                  fill=ACCENT)
        yy += 28
        head_font = load(SANS_BOLD, 29)
        for line in fit_lines(draw, story["headline"], head_font, col_w)[:2]:
            draw.text((x, yy), line, font=head_font, fill=FOREGROUND)
            yy += 34
        yy += 4
        body_font = load(SANS, 19)
        for line in fit_lines(draw, story["body"], body_font, col_w)[:3]:
            draw.text((x, yy), line, font=body_font, fill=BODY_INK)
            yy += 24
    y = y + 2 * row_h - 8
    y = hrule(draw, y)
    return y + 16


def draw_ticker(draw, y):
    """The navy ticker bar; returns the y below it."""
    bar_h = TICKER_H
    draw.rectangle([GUTTER, y, PAGE_W - GUTTER, y + bar_h], fill=DEEP)
    ticker_font = load(SANS, 19)
    ty = y + 10
    for line in fit_lines(draw, TICKER, ticker_font, CONTENT_W - 32):
        draw.text((GUTTER + 16, ty), line, font=ticker_font, fill=WHITE)
        ty += 24
    return y + bar_h + 10


def render():
    """Compose the whole front page and return the image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), BACKGROUND)
    draw = ImageDraw.Draw(page)
    draw.rectangle([FRAME_OUT, FRAME_OUT, PAGE_W - FRAME_OUT - 1,
                    PAGE_H - FRAME_OUT - 1], outline=FOREGROUND, width=2)
    draw.rectangle([FRAME_IN, FRAME_IN, PAGE_W - FRAME_IN - 1,
                    PAGE_H - FRAME_IN - 1], outline=FOREGROUND, width=1)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_grid(draw, y)
    y = draw_ticker(draw, y)
    put_centred(draw, PAGE_W // 2, y, FOOTER, load(SANS, 16), fill=MUTED)
    return page


def main():
    image = render()
    image.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", image.size)


if __name__ == "__main__":
    main()
