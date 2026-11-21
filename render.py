#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page to entry.png.

A dense one-page newspaper: 40 stories, 7 regions, 3 illustrated lead
stories, 10 illustrated briefs, a 27-item numbered list, a world map with
numbered pins, a UTC timeline, a numbers strip and a date check that keeps
Thursday's news out. Rendered at build time by this file; main.py only
copies the PNG, so the graded run is deterministic and needs no network.

    python3 render.py   # writes entry.png (1024x1024, < 1 MiB)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (179, 38, 30)
NAVY = (27, 58, 92)
DARK = (23, 42, 66)
TEAL = (14, 107, 107)
GOLD = (176, 124, 22)
GREEN = (46, 110, 46)
PURPLE = (110, 60, 140)
GREY = (90, 86, 78)
BODY = (60, 58, 52)
CARD = (255, 253, 247)
RULE = (200, 192, 172)
MAP_BG = (232, 228, 215)
LAND = (198, 180, 138)

F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, xy, text, fnt, bg, fg):
    x, y = xy
    pad_x, pad_y = 8, 4
    w = int(draw.textlength(text, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return x + w


# ---------------------------------------------------------------- scenes
def scene_kyiv(draw, box):
    """Night Kyiv: skyline, Dnipro bridge, missile streaks, fires."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    draw.rectangle(box, fill=DARK)
    for sx, sy in [(x0 + 22, y0 + 10), (x0 + 70, y0 + 20), (x0 + 130, y0 + 8),
                   (x0 + 190, y0 + 18), (x0 + 250, y0 + 10), (x0 + 290, y0 + 22)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    draw.ellipse([x1 - 46, y0 + 6, x1 - 18, y0 + 34], fill=(232, 220, 180))
    # skyline: buildings rise from the river bank (bank at y1-16)
    bank = y1 - 16
    for i, bh in enumerate([16, 26, 18, 30, 20, 27, 15]):
        bx = x0 + 8 + i * 44
        draw.rectangle([bx, bank - bh, bx + 32, bank], fill=(52, 62, 76))
        draw.rectangle([bx + 7, bank - bh + 5, bx + 13, bank - bh + 10],
                       fill=(255, 210, 110))
        draw.rectangle([bx + 19, bank - bh + 5, bx + 25, bank - bh + 10],
                       fill=(255, 210, 110))
    # river + bridge deck
    draw.rectangle([x0, bank, x1, y1], fill=(16, 34, 56))
    draw.rectangle([x0, bank - 5, x1, bank - 1], fill=(120, 118, 110))
    for i in range(3):  # three bridge arches
        ax = x0 + 30 + i * 100
        draw.arc([ax, bank - 22, ax + 70, bank + 2], 180, 360,
                 fill=(200, 198, 190), width=3)
        draw.line([ax + 35, bank - 22, ax + 35, bank - 5], fill=(200, 198, 190),
                  width=3)
    # missile streaks (dashed) with fire dots
    for (ax, ay, bx, by) in [(x0 + 40, y0 + 14, x0 + 120, y0 + 48),
                             (x0 + 150, y0 + 10, x0 + 215, y0 + 46),
                             (x0 + 235, y0 + 16, x0 + 290, y0 + 48)]:
        steps = 8
        for s in range(steps):
            if s % 2 == 0:
                t0, t1 = s / steps, (s + 1) / steps
                draw.line([ax + (bx - ax) * t0, ay + (by - ay) * t0,
                           ax + (bx - ax) * t1, ay + (by - ay) * t1],
                          fill=(255, 200, 120), width=2)
        draw.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(232, 120, 40))
    # fires on the bridge deck
    for fx in [x0 + 65, x0 + 165, x0 + 265]:
        draw.ellipse([fx - 8, bank - 14, fx + 8, bank + 2], fill=(232, 164, 62))
        draw.ellipse([fx - 4, bank - 10, fx + 4, bank - 2], fill=(255, 240, 200))


def scene_cyclone(draw, box):
    """Bay of Bengal: coastline, spiral storm, landfall track, rain."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(36, 110, 140))
    # land: polygon with a curved coast on its right edge
    land = [(x0, y0), (x0 + 92, y0), (x0 + 78, y0 + 24), (x0 + 88, y0 + 48),
            (x0 + 70, y0 + 72), (x0 + 84, y1), (x0, y1)]
    draw.polygon(land, fill=(214, 196, 150))
    draw.line([(x0 + 92, y0), (x0 + 78, y0 + 24), (x0 + 88, y0 + 48),
               (x0 + 70, y0 + 72), (x0 + 84, y1)], fill=(120, 100, 60), width=2)
    # spiral: concentric arcs (kept inside the box)
    cx, cy = x0 + 190, y0 + 40
    for r in [12, 20, 28, 36]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255),
                 width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # dashed landfall track from sea to coast
    tx, ty = cx - 30, cy + 18
    for s in range(6):
        if s % 2 == 0:
            t0, t1 = s / 6, (s + 1) / 6
            draw.line([tx + (x0 + 84 - tx) * t0, ty + (y0 + 58 - ty) * t0,
                       tx + (x0 + 84 - tx) * t1, ty + (y0 + 58 - ty) * t1],
                      fill=(255, 90, 70), width=2)
    draw.ellipse([x0 + 78, y0 + 52, x0 + 90, y0 + 64], fill=(255, 60, 40))
    # rain slashes
    for rx, ry in [(x0 + 120, y0 + 70), (x0 + 150, y0 + 78), (x0 + 200, y0 + 72),
                   (x0 + 240, y0 + 80), (x0 + 275, y0 + 70), (x0 + 100, y0 + 84)]:
        draw.line([rx, ry, rx - 6, ry + 10], fill=(200, 225, 235), width=2)


def scene_chart(draw, box):
    """Falling market chart on a dark panel."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 24, 38))
    for gy in [y0 + 20, y0 + 40, y0 + 60, y0 + 80]:
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(48, 58, 76), width=1)
    pts = [(x0 + 14, y0 + 18), (x0 + 60, y0 + 30), (x0 + 105, y0 + 26),
           (x0 + 150, y0 + 48), (x0 + 195, y0 + 44), (x0 + 240, y0 + 66),
           (x0 + 285, y0 + 78)]
    draw.line(pts, fill=(235, 70, 60), width=4)
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 120, 110))
    # red bars bottom
    for i, bh in enumerate([10, 16, 12, 22, 18, 28, 24]):
        bx = x0 + 20 + i * 40
        draw.rectangle([bx, y1 - 8 - bh, bx + 22, y1 - 8], fill=(150, 40, 36))

# ------------------------------------------------- mini illustrations
def mini(draw, box, kind):
    """Small flat illustration strip for a medium card."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if kind == "flags":  # UK + EU flags
        draw.rectangle(box, fill=(30, 50, 90))
        draw.rectangle([x0, y0, x0 + w // 2, y1], fill=(200, 40, 40))
        draw.rectangle([x0, y0 + h // 2 - 4, x0 + w // 2, y0 + h // 2 + 4],
                       fill=(255, 255, 255))
        draw.rectangle([x0 + w // 4 - 4, y0, x0 + w // 4 + 4, y1],
                       fill=(255, 255, 255))
        draw.rectangle([x0 + w // 2, y0, x1, y1], fill=(20, 40, 110))
        for i in range(8):
            import math
            a = math.pi * 2 * i / 8
            sx = x0 + w * 0.75 + int(12 * math.cos(a))
            sy = y0 + h // 2 + int(9 * math.sin(a))
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 0))
    elif kind == "globe":  # COP31: globe + thermometer
        draw.rectangle(box, fill=(18, 90, 90))
        draw.ellipse([x0 + 12, y0 + 4, x0 + 44, y0 + 36], fill=(90, 180, 160))
        draw.ellipse([x0 + 20, y0 + 10, x0 + 32, y0 + 20], fill=(40, 120, 90))
        draw.rectangle([x0 + 120, y0 + 6, x0 + 128, y0 + 30], fill=(255, 255, 255))
        draw.ellipse([x0 + 114, y0 + 26, x0 + 134, y0 + 38], fill=(235, 70, 60))
        draw.rectangle([x0 + 122, y0 + 12, x0 + 126, y0 + 28], fill=(235, 70, 60))
    elif kind == "missile":  # Poland: missile over fields
        draw.rectangle(box, fill=(30, 44, 66))
        draw.rectangle([x0, y1 - 12, x1, y1], fill=(90, 120, 70))
        draw.line([x0 + 20, y0 + 26, x0 + 120, y0 + 12], fill=(255, 200, 120),
                  width=3)
        draw.ellipse([x0 + 116, y0 + 8, x0 + 126, y0 + 18], fill=(255, 120, 60))
        draw.ellipse([x0 + 150, y0 + 16, x0 + 158, y0 + 24], fill=(255, 255, 255))
    elif kind == "tanks":  # Iraq: convoy in the desert
        draw.rectangle(box, fill=(216, 186, 130))
        draw.rectangle([x0, y1 - 10, x1, y1], fill=(170, 140, 90))
        for i in range(3):
            bx = x0 + 14 + i * 56
            draw.rectangle([bx, y0 + 18, bx + 40, y0 + 30], fill=(70, 90, 60))
            draw.line([bx + 30, y0 + 22, bx + 52, y0 + 18], fill=(50, 60, 40),
                      width=3)
            draw.ellipse([bx + 4, y0 + 30, bx + 12, y0 + 36], fill=(40, 40, 40))
            draw.ellipse([bx + 26, y0 + 30, bx + 34, y0 + 36], fill=(40, 40, 40))
    elif kind == "march":  # Italy: strike crowd + placards
        draw.rectangle(box, fill=(240, 230, 210))
        for i in range(7):
            cx = x0 + 16 + i * 24
            draw.ellipse([cx - 6, y0 + 18, cx + 6, y0 + 30], fill=(40, 40, 40))
            draw.rectangle([cx - 8, y0 + 30, cx + 8, y1 - 2], fill=(120, 40, 40)
                           if i % 2 else (30, 60, 110))
        draw.rectangle([x0 + 130, y0 + 4, x0 + 172, y0 + 16], fill=(255, 255, 255),
                       outline=(20, 20, 20))
        draw.text((x0 + 136, y0 + 6), "NO!", font=font(F_BOLD, 11), fill=RED)
    elif kind == "chart":  # Japan: rising bars, red line
        draw.rectangle(box, fill=(245, 240, 228))
        for i, bh in enumerate([10, 16, 13, 20, 26]):
            bx = x0 + 18 + i * 30
            draw.rectangle([bx, y1 - 6 - bh, bx + 18, y1 - 6], fill=(30, 80, 140))
        draw.line([x0 + 14, y0 + 12, x0 + 170, y0 + 26], fill=(235, 70, 60),
                  width=3)
    elif kind == "gavel":  # Seoul: gavel + block
        draw.rectangle(box, fill=(40, 50, 80))
        draw.rectangle([x0 + 70, y0 + 24, x0 + 120, y0 + 32], fill=(150, 110, 60))
        draw.line([x0 + 95, y0 + 8, x0 + 95, y0 + 26], fill=(200, 160, 100),
                  width=4)
        draw.rectangle([x0 + 20, y0 + 28, x0 + 60, y0 + 34], fill=(120, 85, 45))
    elif kind == "derrick":  # Kenya: oil derrick at sunset
        draw.rectangle(box, fill=(235, 170, 80))
        draw.ellipse([x0 + 140, y0 + 4, x0 + 168, y0 + 28], fill=(255, 240, 180))
        draw.line([x0 + 30, y1 - 4, x0 + 55, y0 + 6], fill=(40, 40, 40), width=3)
        draw.line([x0 + 80, y1 - 4, x0 + 55, y0 + 6], fill=(40, 40, 40), width=3)
        draw.line([x0 + 38, y1 - 12, x0 + 72, y1 - 12], fill=(40, 40, 40), width=2)
        draw.line([x0 + 45, y1 - 22, x0 + 66, y1 - 22], fill=(40, 40, 40), width=2)
    elif kind == "ballot":  # Bukele: ballot box
        draw.rectangle(box, fill=(30, 80, 140))
        draw.rectangle([x0 + 66, y0 + 14, x0 + 120, y0 + 36], fill=(255, 255, 255))
        draw.rectangle([x0 + 78, y0 + 8, x0 + 108, y0 + 14], fill=(200, 40, 40))
        draw.line([x0 + 82, y0 + 26, x0 + 92, y0 + 32], fill=(40, 140, 60), width=3)
        draw.line([x0 + 92, y0 + 32, x0 + 112, y0 + 16], fill=(40, 140, 60),
                  width=3)
        draw.text((x0 + 8, y0 + 10), "2027", font=font(F_BOLD, 14),
                  fill=(255, 255, 255))
    elif kind == "cricket":  # Phillips: bat, ball, pitch
        draw.rectangle(box, fill=(60, 130, 70))
        draw.rectangle([x0 + 70, y0 + 4, x0 + 116, y1 - 4], fill=(216, 190, 140))
        draw.line([x0 + 30, y0 + 30, x0 + 90, y0 + 8], fill=(220, 180, 120),
                  width=7)
        draw.ellipse([x0 + 140, y0 + 8, x0 + 152, y0 + 20], fill=(200, 40, 40))
        draw.text((x0 + 8, y0 + 8), "118", font=font(F_BOLD, 15),
                  fill=(255, 255, 255))


# ------------------------------------------------------------- card types
def hero_card(draw, box, num, kicker, accent, headline, body, scene):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=8, fill=CARD, outline=RULE, width=1)
    scene(draw, (x0 + 1, y0 + 1, x1 - 1, y0 + 83))
    y = y0 + 90
    draw.ellipse([x0 + 12, y, x0 + 30, y + 18], fill=accent)
    num_s = str(num)
    draw.text((x0 + 12 + (18 - draw.textlength(num_s, font=font(F_BOLD, 13))) / 2,
               y + 1), num_s, font=font(F_BOLD, 13), fill=(255, 255, 255))
    draw.text((x0 + 36, y + 1), kicker, font=font(F_BOLD, 12), fill=accent)
    y += 22
    y = para(draw, (x0 + 12, y), headline, font(F_BOLD, 19), INK, x1 - x0 - 24,
             leading=22)
    y += 3
    para(draw, (x0 + 12, y), body, font(F_SANS, 12), BODY, x1 - x0 - 24,
         leading=15)


def medium_card(draw, box, num, kicker, accent, headline, body, kind, src):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=8, fill=CARD, outline=RULE, width=1)
    mini(draw, (x0 + 1, y0 + 1, x1 - 1, y0 + 34), kind)
    sw = draw.textlength(src, font=font(F_BOLD, 10))
    draw.rectangle([x1 - 8 - sw - 8, y0 + 20, x1 - 8, y0 + 33], fill=(20, 20, 20))
    draw.text((x1 - 8 - sw - 4, y0 + 22), src, font=font(F_BOLD, 10),
              fill=(255, 255, 255))
    y = y0 + 38
    draw.text((x0 + 10, y), f"{num}  {kicker}", font=font(F_BOLD, 11), fill=accent)
    y += 15
    y = para(draw, (x0 + 10, y), headline, font(F_BOLD, 14), INK, x1 - x0 - 20,
             leading=15)
    para(draw, (x0 + 10, y + 2), body, font(F_SANS, 11), BODY, x1 - x0 - 20,
         leading=13)

# ------------------------------------------------------------------- data
HEROES = [
    (1, "KYIV, UKRAINE  •  WAR", RED,
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of 110+ missiles and drones killed at least 8 "
     "across Ukraine; power and water cut in the capital. "
     "(Reuters)", scene_kyiv),
    (2, "ODISHA, INDIA  •  CYCLONE", TEAL,
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am, after "
     "300,000+ people were moved to shelters. No deaths reported. (IMD)",
     scene_cyclone),
    (3, "TAIPEI  •  SEOUL  •  TOKYO  •  MARKETS", RED,
     "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul "
     "lost 5.2% and Tokyo 5.1% as chipmakers led the slide. (AP)",
     scene_chart),
]

MEDIUM = [
    (4, "BRUSSELS  •  DIPLOMACY", NAVY, "UK and EU seal a \u201creset\u201d deal",
     "Food trade, youth visas, carbon link.",
     "flags", "Reuters"),
    (5, "ANTALYA  •  CLIMATE", TEAL, "COP31 runs past its final day with no deal",
     "Draft leaves out fossil fuels; talks in overtime.",
     "globe", "UN News"),
    (6, "E. POLAND  •  SECURITY", RED, "Russian missiles land in Poland",
     "Two Kh-101s down in fields; two airports paused.",
     "missile", "Reuters"),
    (7, "C. IRAQ  •  SECURITY", GOLD, "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar.",
     "tanks", "Reuters"),
    (8, "ITALY  •  LABOUR", RED, "General strike over Italy's budget",
     "Workers and students march in 100 squares.",
     "march", "Reuters"),
    (9, "TOKYO  •  ECONOMY", NAVY, "Japan's inflation picks up to 2.3%",
     "October CPI; a December rate rise stays in view.",
     "chart", "Reuters"),
    (10, "SEOUL  •  POLITICS", PURPLE, "Korea's ruling party to impeach top judge",
     "It follows an overturned conviction.",
     "gavel", "Kor. Herald"),
    (11, "TURKANA  •  ENERGY", GREEN, "Kenya starts drilling its first oil well",
     "First crude is due on 1 December.",
     "derrick", "allAfrica"),
    (12, "EL SALVADOR  •  POLITICS", NAVY, "Bukele files to run for a third term",
     "The vote is on 28 February 2027.",
     "ballot", "AP"),
    (13, "WELLINGTON  •  CRICKET", GREEN, "Phillips hits 118 against India",
     "New Zealand make 368; hundreds in all formats.",
     "cricket", "ICC"),
]

BRIEFS = [
    "Lviv: rail station strike kills two (BBC)",
    "Estonia shuts Russia border 1 Dec (Reuters)",
    "Berlin: pupils strike vs military service (AJ)",
    "London: general says UK runs cyber attacks (Sky)",
    "Beijing: loan rates held 18th month (Xinhua)",
    "Tokyo: SoftBank shares fall over 14% (Reuters)",
    "Seoul: KOSPI ends week 7.9% lower (Anadolu)",
    "Ganjam: 209 mm rain as Akvan crosses Odisha (PTI)",
    "Lebanon: Israeli strikes hit south (Anadolu)",
    "Yemen: gunmen fire on cargo ship (UKMTO)",
    "Abuja: court bars evidence vs Tinubu (Channels)",
    "Turin: ATP backs player pay past $350m (Anadolu)",
    "Kampala: Ebola rally ban enforced (allAfrica)",
    "Malawi: fuel crisis, night petrol queues (AJ)",
    "AfDB: 22 African states near debt distress",
    "NY: Anthropic falls 11% after debut (Reuters)",
    "Sydney: shares fall 1.8% in the rout (Reuters)",
    "Antalya: Panama asks COP31 for oil cap (Anadolu)",
    "Washington: US war cost vs Iran $48.3bn (Reuters)",
    "Smolensk: drones hit a chemical plant (Kyiv Indy)",
    "Kerch: Crimea bridge hit third time this week (ISW)",
    "Mercury: BepiColombo arrives after 8 years (ESA)",
    "Health: cancer pill shrinks tumours 60.7% (Reuters)",
    "Hormuz: tanker ablaze off Oman; none hurt (UKMTO)",
    "Las Vegas: Russell fastest in wet GP practice (F1)",
    "Delhi: Pakistan minister visits, first since May (PTI)",
    "S\u00e3o Paulo: markets shut for Consciousness Day (AP)",
]

# pin positions on the 300x230 map canvas (x, y) for stories 1..13
PINS = {1: (178, 40), 2: (250, 80), 3: (276, 66), 4: (138, 48), 5: (186, 62),
        6: (160, 28), 7: (202, 78), 8: (150, 64), 9: (286, 48), 10: (264, 44),
        11: (168, 124), 12: (38, 88), 13: (290, 186)}


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=MAP_BG)
    # rough continents (coords relative to a 300x230 canvas)
    continents = [
        [(18, 55), (55, 30), (95, 28), (110, 45), (100, 75), (70, 85),
         (45, 95), (25, 80)],                                    # N America
        [(78, 120), (105, 115), (118, 140), (105, 180), (88, 165),
         (75, 140)],                                              # S America
        [(140, 45), (165, 30), (185, 38), (178, 60), (155, 65),
         (142, 55)],                                              # Europe
        [(140, 85), (170, 80), (190, 95), (185, 130), (165, 155),
         (148, 130), (138, 105)],                                 # Africa
        [(190, 35), (250, 25), (285, 45), (275, 80), (240, 95),
         (205, 85), (192, 60)],                                   # Asia
        [(245, 150), (280, 145), (288, 165), (260, 175), (244, 165)],
    ]                                                             # Australia
    for poly in continents:
        pts = [(x0 + px, y0 + py) for px, py in poly]
        draw.polygon(pts, fill=LAND, outline=(150, 132, 96))
    for num, (px, py) in PINS.items():
        cx, cy = x0 + px, y0 + py
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        s = str(num)
        draw.text((cx - draw.textlength(s, font=font(F_BOLD, 9)) / 2, cy - 6),
                  s, font=font(F_BOLD, 9), fill=(255, 255, 255))

# -------------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    CW = W - 2 * M  # 972

    # ---- masthead ----
    d.line([M, 10, W - M, 10], fill=INK, width=3)
    d.text((M, 19), "THE WORLD IN ONE DAY", font=font(F_BOLD, 15), fill=RED)
    right = "40 STORIES  •  7 REGIONS  •  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - M - d.textlength(right, font=font(F_BOLD, 13)), 21), right,
           font=font(F_BOLD, 13), fill=GREY)
    d.text((M, 40), "Friday 20 November 2026", font=font(F_SERIF, 53), fill=INK)
    d.text((M, 106),
           "Missiles hit Kyiv\u2019s bridges  \u2022  Cyclone Akvan strikes India  "
           "\u2022  AI sell-off sinks Asia  \u2022  UK and EU seal a deal",
           font=font(F_SANS, 17), fill=GREY)
    d.line([M, 132, W - M, 132], fill=INK, width=2)

    # ---- UTC timeline ----
    y = 140
    chip(d, (M, y), "THE DAY IN UTC", font(F_BOLD, 12), RED, (255, 255, 255))
    timeline = [("00:00", "Kyiv bridges hit"), ("02:00", "Akvan landfall"),
                ("05:30", "Taiwan \u22126.2%"), ("15:00", "COP31 overtime"),
                ("21:00", "S&P 500 \u22123.7%")]
    tx = M + 148
    for t, label in timeline:
        d.text((tx, y + 1), t, font=font(F_BOLD, 13), fill=RED)
        tx += d.textlength(t, font=font(F_BOLD, 13)) + 5
        d.text((tx, y + 1), label, font=font(F_SANS, 13), fill=INK)
        tx += d.textlength(label, font=font(F_SANS, 13)) + 16

    # ---- numbers strip ----
    y0, y1 = 164, 216
    stats = [("3", "bridges over the Dnipro damaged in Kyiv"),
             ("300,000+", "people moved to shelters before Akvan"),
             ("\u22126.2%", "Taiwan\u2019s share index, Friday\u2019s close"),
             ("\u22123.7%", "S&P 500 on the day, into correction"),
             ("100,000", "youth visas a year in the UK\u2013EU deal"),
             ("118", "runs by Glenn Phillips against India")]
    cell = CW // 6
    for i, (num, label) in enumerate(stats):
        x = M + i * cell
        if i:
            d.line([x - 6, y0 + 4, x - 6, y1 - 4], fill=RULE, width=1)
        d.text((x, y0), num, font=font(F_BOLD, 22), fill=INK)
        para(d, (x, y0 + 28), label, font(F_SANS, 11), GREY, cell - 14,
             leading=12)

    # ---- region bar ----
    y = 220
    regions = [("EUROPE 11", 200, NAVY), ("ASIA 9", 180, RED),
               ("MIDDLE EAST 5", 130, GOLD), ("AFRICA 5", 130, GREEN),
               ("AMERICAS 5", 130, PURPLE), ("OCEANIA 2", 90, TEAL),
               ("GLOBAL 3", 112, GREY)]
    x = M
    for label, w, color in regions:
        d.rectangle([x, y, x + w, y + 20], fill=color)
        d.text((x + (w - d.textlength(label, font=font(F_BOLD, 11))) / 2, y + 3),
               label, font=font(F_BOLD, 11), fill=(255, 255, 255))
        x += w

    # ---- heroes ----
    y0, y1 = 246, 450
    hw = (CW - 2 * 12) // 3
    for i, (num, kicker, accent, headline, body, scene) in enumerate(HEROES):
        hero_card(d, (M + i * (hw + 12), y0, M + i * (hw + 12) + hw, y1),
                  num, kicker, accent, headline, body, scene)

    # ---- medium grid: 2 rows x 5 ----
    mw = (CW - 4 * 10) // 5
    for row in range(2):
        ry0 = 456 + row * 118
        ry1 = ry0 + 112
        for col in range(5):
            s = MEDIUM[row * 5 + col]
            medium_card(d, (M + col * (mw + 10), ry0, M + col * (mw + 10) + mw,
                            ry1), s[0], s[1], s[2], s[3], s[4], s[5], s[6])

    # ---- map + numbered briefs ----
    y0 = 692
    d.text((M, y0), "WHERE IT HAPPENED", font=font(F_BOLD, 13), fill=RED)
    d.text((M + 316, y0), "ALSO ON FRIDAY 20 NOVEMBER \u2014 27 MORE STORIES",
           font=font(F_BOLD, 13), fill=RED)
    draw_map(d, (M, y0 + 20, M + 304, y0 + 250))
    d.text((M, y0 + 252),
           "Pins 1\u201313 mark the drawn stories on this page.",
           font=font(F_SANS, 11), fill=GREY)
    bx = M + 316
    col_w = (W - M - bx - 8) // 2
    bfb = font(F_BOLD, 12)
    num_w = d.textlength("40  ", font=bfb)
    for idx, text in enumerate(BRIEFS):
        col = idx // 14
        row = idx % 14
        x = bx + col * (col_w + 8)
        yy = y0 + 22 + row * 17
        num = str(14 + idx)
        d.text((x, yy), num, font=bfb, fill=RED)
        # shrink the line's font until it fits the column
        for size in (11, 10):
            bf = font(F_SANS, size)
            if d.textlength(text, font=bf) <= col_w - num_w - 2:
                break
        d.text((x + num_w, yy + (11 - size) / 2), text, font=bf, fill=INK)

    # ---- date check + credit ----
    y = 960
    d.rounded_rectangle([M, y, W - M, y + 36], radius=4, outline=RED, width=2)
    d.text((M + 10, y + 4),
           "DATE CHECK \u2014 Left out (Thursday 19 Nov, not shown): the World "
           "Court\u2019s Myanmar ruling, the Shenzhen leaders\u2019",
           font=font(F_BOLD, 12), fill=RED)
    d.text((M + 10, y + 20),
           "declaration, the Senate Iran war-powers vote, the $190.4m Van Gogh "
           "sale. Not yet: Mercury orbit capture, a final COP31 text.",
           font=font(F_SANS, 12), fill=INK)
    d.text((M, 1008),
           "Every story here happened, or was first reported, on Friday 20 "
           "November 2026. Officials\u2019 counts are attributed. Sources named "
           "beside each story \u2022 Original drawings",
           font=font(F_SANS, 11), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
