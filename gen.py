"""Draw the world news of Thursday 26 November 2026 as one image.

Program-drawn with PIL only: no network, no AI images, deterministic.
All 43 stories happened or were first reported on 26 November 2026
(verified against Reuters / SCMP / AP / PANA / One Turn roundups).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


# ---------------------------------------------------------------- palette
NAVY = (15, 30, 58)
NAVY2 = (23, 48, 88)
INK = (18, 24, 38)
PAPER = (247, 246, 242)
CARD = (255, 255, 255)
MUTED = (90, 98, 116)
LINE = (214, 218, 226)
GOLD = (212, 160, 32)
SKY = (148, 196, 232)

REGION_COLORS = {
    "North America": (37, 99, 235),
    "Europe": (124, 58, 237),
    "Middle East": (220, 38, 38),
    "Africa": (234, 88, 12),
    "Asia-Pacific": (8, 145, 178),
    "South Asia": (101, 163, 13),
    "Latin America": (219, 39, 119),
    "Markets & Tech": (15, 118, 110),
    "Science & Health": (79, 70, 229),
}

# ---------------------------------------------------------------- stories
# (title, detail, region, icon kind, is_drawn_scene)
LEADS = [
    ("US proposes new tariffs on 14 partners",
     "Rates of 20-40% floated",
     "North America", "tariff"),
    ("Cairo tanker fire kills 31, 21 hurt",
     "Tanker overturns on Ring Road",
     "Africa", "fire"),
    ("Gaza strikes kill 9, incl. Hamas minister",
     "Third straight night of air attacks",
     "Middle East", "war"),
]

GRID = [
    ("Kyiv hit by ballistic missiles, 7 hurt", "Shopping centre struck overnight", "Europe", "missile", True),
    ("Ukraine hits Russian air base", "5 jets damaged in strike", "Europe", "plane", False),
    ("Houthis hit Saudi ports", "Refinery damaged in attack", "Middle East", "oil", True),
    ("Iran: two tankers hit mines", "Blasts in the Strait of Hormuz", "Middle East", "mine", False),
    ("Trump & NATO: Russia must not widen war", "Joint statement after Florida talks", "Europe", "handshake", False),
    ("N. Korea vows more nuclear weapons", "Kim ignores Trump's overture", "Asia-Pacific", "nuclear", True),
    ("China probes Shanghai party chief", "Chen Jining under investigation", "Asia-Pacific", "court", False),
    ("Pakistan astronaut reaches Tiangong", "First Pakistani on China's station", "Asia-Pacific", "space", True),
    ("FCC OKs SpaceX StarMind", "Up to 1m satellites for AI in orbit", "North America", "satellite", True),
    ("Nvidia halts AI server sales to Asia", "Four markets hit by US curbs", "Markets & Tech", "chip", False),
    ("UK net migration 77,000", "Lowest in nearly 30 years", "Europe", "migration", True),
    ("Depardieu to face rape trial", "Appeal lost; trial ordered", "Europe", "court", False),
    ("Duran Duran guitarist dies at 65", "Andy Taylor helped define the 80s", "Europe", "music", False),
    ("Jolie & Pitt settle winery fight", "Decade-long dispute ends", "North America", "star", False),
    ("Macy's 100th parade postponed", "Storm forces delay in New York", "North America", "parade", True),
    ("FedEx jet overshoots Miami runway", "Delays on a peak travel day", "North America", "plane", True),
    ("US Army blows up toxic explosives", "Iowa detonation 'a success'", "North America", "explosion", False),
    ("Court blocks Trump birthright order", "Federal judge halts the order", "North America", "court", False),
    ("Bovespa +1.6% as LatAm rallies", "Brazil leads regional gains", "Latin America", "chart", False),
    ("Hernandez de Cos to lead ECB", "Succeeds Lagarde as chief", "Europe", "chart", False),
    ("Pig-kidney patient: 1 yr off dialysis", "Milestone for xenotransplant", "Science & Health", "health", False),
    ("Colombian fighter jailed 20 yrs", "Russian court over Ukraine role", "Europe", "court", False),
    ("8 French IS members jailed for life", "Iraq sentences over IS links", "Middle East", "court", False),
    ("China-Mongolia-Russia rail restarts", "Service back after 6-year halt", "Asia-Pacific", "rail", False),
    ("Singapore rebuts US tariff logic", "SE Asia hits back at Washington", "Asia-Pacific", "chart", False),
    ("London Tube strikes begin", "First of 8 winter strike days", "Europe", "strike", False),
    ("DRC Ebola tops 12,000 cases", "5,904 deaths in worst outbreak", "Africa", "virus", True),
    ("S. Africa court backs Ramaphosa", "Farmgate report thrown out", "Africa", "court", False),
    ("Serbia election set for 27 Dec", "Presidential vote announced", "Europe", "vote", False),
    ("Bangladesh garment workers gassed", "Police use tear gas at protest", "South Asia", "strike", False),
    ("China warns Japan on S. China Sea", "Urges halt to 'escalation'", "Asia-Pacific", "wave", False),
    ("Indonesia mine rescue slowed by rain", "13 trapped in illegal mine", "Asia-Pacific", "mine", True),
    ("UK sends convicted refugees to Eswatini", "Migration deal in action", "Africa", "migration", False),
    ("Lukoil overseas deal struck", "US-backed group buys assets", "Markets & Tech", "oil", False),
    ("Stocks rebound on tariff calm", "Euro Stoxx +1.9%, Sensex +2.3%", "Markets & Tech", "chart", True),
    ("King tides flood California coast", "Storm waves swamp roads, homes", "North America", "wave", True),
    ("Bangkok refinery fire injures 7", "Blaze at oil refinery", "Asia-Pacific", "fire", False),
    ("1Password breach: data stolen", "Attacker took customer info", "Markets & Tech", "chip", False),
    ("Judge blocks FCC review of ABC", "Free-speech ruling for stations", "North America", "court", False),
    ("NY bans AI chatbots posing as human", "New law protects children", "North America", "chip", False),
]

TIMELINE = [
    ("00 UTC", "Gaza strikes kill 9 overnight"),
    ("04 UTC", "Kyiv hit by missiles; 7 hurt"),
    ("08 UTC", "Cairo fire toll reaches 31"),
    ("12 UTC", "EU budget talks open"),
    ("16 UTC", "Tariff backlash in Asia"),
    ("20 UTC", "Thanksgiving night in the US"),
]

REGIONS = ["North America", "Europe", "Middle East", "Africa",
           "Asia-Pacific", "South Asia", "Latin America",
           "Markets & Tech", "Science & Health"]


# ---------------------------------------------------------------- helpers
def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, box, color):
    """Small vector pictogram inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = min(x1 - x0, y1 - y0)
    u = s / 40.0  # unit

    if kind == "tariff":  # rising bars + %
        for i, h in enumerate((10, 18, 26)):
            bx = x0 + 6 * u + i * 11 * u
            d.rectangle([bx, y1 - 6 * u - h * u, bx + 8 * u, y1 - 6 * u], fill=color)
        d.text((x0 + 26 * u, y0 + 2 * u), "%", font=int(14 * u), fill=color)
    elif kind == "fire":  # flame
        d.polygon([(cx, y0 + 4 * u), (cx + 12 * u, y0 + 20 * u),
                   (cx + 6 * u, y0 + 18 * u), (cx + 10 * u, y1 - 5 * u),
                   (cx - 10 * u, y1 - 5 * u), (cx - 6 * u, y0 + 18 * u),
                   (cx - 12 * u, y0 + 20 * u)], fill=(234, 88, 12))
        d.polygon([(cx, y0 + 18 * u), (cx + 5 * u, y0 + 26 * u),
                   (cx, y1 - 5 * u), (cx - 5 * u, y0 + 26 * u)], fill=(250, 204, 21))
    elif kind == "war":  # explosion burst
        for ang in range(0, 360, 30):
            import math
            a = math.radians(ang)
            r1, r2 = 6 * u, 17 * u
            d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                    cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                   fill=color, width=max(2, int(3 * u)))
        d.ellipse([cx - 6 * u, cy - 6 * u, cx + 6 * u, cy + 6 * u], fill=(234, 88, 12))
    elif kind == "missile":  # rocket + trail
        d.polygon([(cx, y0 + 3 * u), (cx + 6 * u, y0 + 14 * u),
                   (cx - 6 * u, y0 + 14 * u)], fill=color)
        d.rectangle([cx - 5 * u, y0 + 14 * u, cx + 5 * u, y0 + 28 * u], fill=color)
        d.polygon([(cx - 5 * u, y0 + 28 * u), (cx - 11 * u, y0 + 34 * u),
                   (cx - 5 * u, y0 + 30 * u)], fill=color)
        d.polygon([(cx + 5 * u, y0 + 28 * u), (cx + 11 * u, y0 + 34 * u),
                   (cx + 5 * u, y0 + 30 * u)], fill=color)
        d.polygon([(cx, y1 - 3 * u), (cx + 3 * u, y0 + 30 * u),
                   (cx - 3 * u, y0 + 30 * u)], fill=(234, 88, 12))
    elif kind == "plane":
        d.ellipse([x0 + 4 * u, cy - 4 * u, x1 - 4 * u, cy + 4 * u], fill=color)
        d.polygon([(cx - 2 * u, cy - 4 * u), (cx + 8 * u, cy - 14 * u),
                   (cx + 12 * u, cy - 14 * u), (cx + 4 * u, cy - 4 * u)], fill=color)
        d.polygon([(cx - 6 * u, cy + 4 * u), (cx + 2 * u, cy + 12 * u),
                   (cx + 6 * u, cy + 12 * u), (cx, cy + 4 * u)], fill=color)
        d.polygon([(cx + 12 * u, cy - 3 * u), (cx + 18 * u, cy - 10 * u),
                   (cx + 18 * u, cy - 6 * u), (cx + 13 * u, cy + 1 * u)], fill=color)
    elif kind == "oil":  # barrel
        d.rectangle([cx - 9 * u, y0 + 8 * u, cx + 9 * u, y1 - 6 * u], fill=color)
        d.rectangle([cx - 9 * u, y0 + 13 * u, cx + 9 * u, y0 + 16 * u], fill=(255, 255, 255))
        d.rectangle([cx - 9 * u, y0 + 25 * u, cx + 9 * u, y0 + 28 * u], fill=(255, 255, 255))
        d.ellipse([cx - 9 * u, y0 + 5 * u, cx + 9 * u, y0 + 11 * u], fill=(255, 255, 255))
    elif kind == "nuclear":  # trefoil
        d.ellipse([cx - 5 * u, cy - 5 * u, cx + 5 * u, cy + 5 * u], fill=color)
        import math
        for base in (90, 210, 330):
            a = math.radians(base)
            px, py = cx + 12 * u * math.cos(a), cy + 12 * u * math.sin(a)
            d.pieslice([px - 8 * u, py - 8 * u, px + 8 * u, py + 8 * u],
                       base - 30, base + 30, fill=color)
        d.ellipse([cx - 16 * u, cy - 16 * u, cx + 16 * u, cy + 16 * u], outline=color, width=max(2, int(2 * u)))
    elif kind == "space":  # station
        d.rectangle([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], fill=color)
        d.rectangle([x0 + 3 * u, cy - 6 * u, cx - 5 * u, cy + 6 * u], fill=color)
        d.rectangle([cx + 5 * u, cy - 6 * u, x1 - 3 * u, cy + 6 * u], fill=color)
        for sx, sy in ((x0 + 6 * u, y0 + 5 * u), (x1 - 6 * u, y0 + 8 * u), (x0 + 9 * u, y1 - 6 * u)):
            d.ellipse([sx - 1.5 * u, sy - 1.5 * u, sx + 1.5 * u, sy + 1.5 * u], fill=GOLD)
    elif kind == "satellite":
        d.rectangle([cx - 6 * u, cy - 4 * u, cx + 6 * u, cy + 4 * u], fill=color)
        d.line([cx - 6 * u, cy, x0 + 3 * u, y0 + 8 * u], fill=color, width=max(2, int(2 * u)))
        d.line([cx + 6 * u, cy, x1 - 3 * u, y1 - 8 * u], fill=color, width=max(2, int(2 * u)))
        d.arc([x0 + 2 * u, y0 + 2 * u, x0 + 16 * u, y0 + 16 * u], 180, 360, fill=GOLD, width=max(2, int(2 * u)))
        d.ellipse([cx - 16 * u, cy - 16 * u, cx + 16 * u, cy + 16 * u], outline=(180, 190, 205), width=1)
    elif kind == "chip":
        d.rectangle([cx - 9 * u, cy - 9 * u, cx + 9 * u, cy + 9 * u], fill=color)
        d.rectangle([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], fill=(255, 255, 255))
        for i in range(3):
            d.line([cx - 9 * u + i * 9 * u, y0 + 2 * u, cx - 9 * u + i * 9 * u, cy - 9 * u], fill=color, width=max(2, int(2 * u)))
            d.line([cx - 9 * u + i * 9 * u, cy + 9 * u, cx - 9 * u + i * 9 * u, y1 - 2 * u], fill=color, width=max(2, int(2 * u)))
    elif kind == "migration":  # arrows
        d.polygon([(x0 + 4 * u, cy - 8 * u), (x1 - 10 * u, cy - 8 * u),
                   (x1 - 10 * u, cy - 13 * u), (x1 - 3 * u, cy - 3 * u),
                   (x1 - 10 * u, cy + 7 * u), (x1 - 10 * u, cy + 2 * u),
                   (x0 + 4 * u, cy + 2 * u)], fill=color)
        d.ellipse([x0 + 4 * u, cy + 9 * u, x0 + 12 * u, cy + 17 * u], fill=GOLD)
        d.ellipse([x0 + 16 * u, cy + 9 * u, x0 + 24 * u, cy + 17 * u], fill=GOLD)
    elif kind == "court":  # scales
        d.line([cx, y0 + 4 * u, cx, y1 - 6 * u], fill=color, width=max(2, int(2 * u)))
        d.line([x0 + 6 * u, y0 + 8 * u, x1 - 6 * u, y0 + 8 * u], fill=color, width=max(2, int(2 * u)))
        d.polygon([(x0 + 4 * u, y0 + 18 * u), (x0 + 12 * u, y0 + 18 * u), (x0 + 8 * u, y0 + 8 * u)], outline=color, width=max(2, int(2 * u)))
        d.polygon([(x1 - 12 * u, y0 + 18 * u), (x1 - 4 * u, y0 + 18 * u), (x1 - 8 * u, y0 + 8 * u)], outline=color, width=max(2, int(2 * u)))
        d.rectangle([x0 + 10 * u, y1 - 6 * u, x1 - 10 * u, y1 - 3 * u], fill=color)
    elif kind == "music":
        d.ellipse([cx - 10 * u, cy + 4 * u, cx - 2 * u, cy + 12 * u], fill=color)
        d.ellipse([cx + 4 * u, cy + 8 * u, cx + 12 * u, cy + 16 * u], fill=color)
        d.line([cx - 3 * u, cy + 8 * u, cx - 3 * u, y0 + 4 * u], fill=color, width=max(2, int(2 * u)))
        d.line([cx + 11 * u, cy + 12 * u, cx + 11 * u, y0 + 8 * u], fill=color, width=max(2, int(2 * u)))
        d.line([cx - 3 * u, y0 + 4 * u, cx + 11 * u, y0 + 8 * u], fill=color, width=max(2, int(2 * u)))
    elif kind == "star":
        import math
        pts = []
        for i in range(10):
            r = 16 * u if i % 2 == 0 else 7 * u
            a = math.radians(-90 + i * 36)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=GOLD)
    elif kind == "parade":  # balloon
        d.ellipse([cx - 12 * u, y0 + 2 * u, cx + 12 * u, y0 + 22 * u], fill=color)
        d.ellipse([cx - 5 * u, y0 + 5 * u, cx + 1 * u, y0 + 11 * u], fill=(255, 255, 255))
        d.polygon([(cx - 3 * u, y0 + 22 * u), (cx + 3 * u, y0 + 22 * u), (cx, y0 + 27 * u)], fill=color)
        d.line([cx, y0 + 27 * u, cx + 3 * u, y1 - 4 * u], fill=MUTED, width=max(1, int(2 * u)))
    elif kind == "explosion":
        import math
        pts = []
        for i in range(16):
            r = 17 * u if i % 2 == 0 else 8 * u
            a = math.radians(i * 22.5)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=(234, 88, 12))
        d.ellipse([cx - 5 * u, cy - 5 * u, cx + 5 * u, cy + 5 * u], fill=(250, 204, 21))
    elif kind == "chart":
        pts = [(x0 + 4 * u, y1 - 12 * u), (x0 + 13 * u, y1 - 20 * u),
               (x0 + 20 * u, y1 - 14 * u), (x0 + 28 * u, y1 - 24 * u),
               (x1 - 5 * u, y1 - 30 * u)]
        d.line(pts, fill=color, width=max(2, int(3 * u)), joint="curve")
        d.polygon([(x1 - 10 * u, y1 - 30 * u), (x1 - 3 * u, y1 - 30 * u), (x1 - 6 * u, y1 - 23 * u)], fill=color)
        d.line([x0 + 4 * u, y1 - 6 * u, x1 - 4 * u, y1 - 6 * u], fill=MUTED, width=max(1, int(2 * u)))
    elif kind == "health":  # cross
        d.rectangle([cx - 4 * u, y0 + 4 * u, cx + 4 * u, y1 - 4 * u], fill=color)
        d.rectangle([x0 + 4 * u, cy - 4 * u, x1 - 4 * u, cy + 4 * u], fill=color)
    elif kind == "virus":
        d.ellipse([cx - 11 * u, cy - 11 * u, cx + 11 * u, cy + 11 * u], fill=color)
        import math
        for i in range(8):
            a = math.radians(i * 45)
            d.line([cx + 11 * u * math.cos(a), cy + 11 * u * math.sin(a),
                    cx + 16 * u * math.cos(a), cy + 16 * u * math.sin(a)],
                   fill=color, width=max(2, int(3 * u)))
        d.ellipse([cx - 4 * u, cy - 4 * u, cx + 1 * u, cy + 1 * u], fill=(255, 255, 255))
    elif kind == "rail":  # train front
        d.rounded_rectangle([cx - 12 * u, y0 + 6 * u, cx + 12 * u, y1 - 8 * u], radius=4 * u, fill=color)
        d.rectangle([cx - 8 * u, y0 + 10 * u, cx + 8 * u, y0 + 18 * u], fill=SKY)
        d.line([cx - 8 * u, y1 - 8 * u, cx - 14 * u, y1 - 3 * u], fill=MUTED, width=max(2, int(2 * u)))
        d.line([cx + 8 * u, y1 - 8 * u, cx + 14 * u, y1 - 3 * u], fill=MUTED, width=max(2, int(2 * u)))
    elif kind == "strike":  # picket sign
        d.rectangle([x0 + 6 * u, y0 + 4 * u, x1 - 6 * u, y0 + 20 * u], fill=color)
        d.line([cx, y0 + 20 * u, cx, y1 - 4 * u], fill=(90, 98, 116), width=max(2, int(3 * u)))
        d.line([x0 + 10 * u, y0 + 10 * u, x1 - 10 * u, y0 + 10 * u], fill=(255, 255, 255), width=max(2, int(2 * u)))
        d.line([x0 + 10 * u, y0 + 15 * u, x1 - 10 * u, y0 + 15 * u], fill=(255, 255, 255), width=max(2, int(2 * u)))
    elif kind == "vote":  # ballot box
        d.rectangle([cx - 12 * u, y0 + 12 * u, cx + 12 * u, y1 - 6 * u], fill=color)
        d.rectangle([cx - 5 * u, y0 + 8 * u, cx + 5 * u, y0 + 12 * u], fill=(255, 255, 255))
        d.polygon([(cx - 2 * u, y0 + 2 * u), (cx + 8 * u, y0 + 2 * u),
                   (cx + 2 * u, y0 + 10 * u), (cx - 6 * u, y0 + 10 * u)], fill=(255, 255, 255))
    elif kind == "wave":
        for j, yy in enumerate((cy - 8 * u, cy, cy + 8 * u)):
            pts = []
            for i in range(9):
                xx = x0 + 4 * u + i * 4 * u
                yv = yy + (3 * u if i % 2 == 0 else -3 * u)
                pts.append((xx, yv))
            d.line(pts, fill=color if j != 1 else GOLD, width=max(2, int(3 * u)), joint="curve")
    elif kind == "mine":  # helmet
        d.pieslice([cx - 14 * u, y0 + 6 * u, cx + 14 * u, y0 + 30 * u], 180, 360, fill=color)
        d.rectangle([cx - 16 * u, y0 + 18 * u, cx + 16 * u, y0 + 22 * u], fill=color)
        d.rectangle([cx - 3 * u, y0 + 4 * u, cx + 3 * u, y0 + 12 * u], fill=GOLD)
        d.line([x0 + 4 * u, y1 - 5 * u, x1 - 4 * u, y1 - 5 * u], fill=MUTED, width=max(2, int(2 * u)))
    elif kind == "handshake":
        d.polygon([(x0 + 4 * u, cy - 2 * u), (cx, cy - 10 * u),
                   (x1 - 4 * u, cy - 2 * u), (cx, cy + 8 * u)], outline=color, width=max(2, int(2 * u)))
        d.line([x0 + 4 * u, cy - 2 * u, cx, cy + 8 * u], fill=color, width=max(2, int(2 * u)))
    else:  # fallback dot
        d.ellipse([cx - 8 * u, cy - 8 * u, cx + 8 * u, cy + 8 * u], fill=color)


def draw_hero_scene(d, kind, box):
    """Bigger pictorial scene for the three lead cards."""
    x0, y0, x1, y1 = box
    if kind == "tariff":
        d.rectangle(box, fill=(23, 48, 88))
        d.text((x0 + 12, y0 + 6), "20-40%  NEW TARIFFS", font=font(20, True), fill=(255, 255, 255))
        d.text((x0 + 12, y0 + 32), "14 trading partners", font=font(13), fill=(148, 196, 232))
        for i, h in enumerate((18, 26, 34, 42)):
            bx = x0 + 24 + i * 68
            d.rectangle([bx, y1 - 14 - h, bx + 44, y1 - 14], fill=(148, 196, 232) if i < 3 else GOLD)
        d.line([x0 + 10, y1 - 14, x1 - 10, y1 - 14], fill=(255, 255, 255), width=2)
    elif kind == "fire":
        d.rectangle(box, fill=(43, 20, 12))
        d.rectangle([x0, y1 - 26, x1, y1], fill=(30, 30, 34))  # road
        d.rectangle([x0 + 60, y1 - 52, x0 + 190, y1 - 26], fill=(120, 120, 128))  # tanker
        d.ellipse([x0 + 74, y1 - 30, x0 + 92, y1 - 12], fill=(20, 20, 22))
        d.ellipse([x0 + 158, y1 - 30, x0 + 176, y1 - 12], fill=(20, 20, 22))
        for fx, fh in ((110, 66), (140, 84), (170, 60)):
            d.polygon([(x0 + fx, y1 - 52 - fh), (x0 + fx + 26, y1 - 52 - fh // 2),
                       (x0 + fx + 14, y1 - 52), (x0 + fx - 14, y1 - 52),
                       (x0 + fx - 26, y1 - 52 - fh // 2)], fill=(234, 88, 12))
        d.polygon([(x0 + 140, y1 - 52 - 52), (x0 + 156, y1 - 52 - 26),
                   (x0 + 148, y1 - 52), (x0 + 132, y1 - 52),
                   (x0 + 124, y1 - 52 - 26)], fill=(250, 204, 21))
        d.text((x0 + 210, y0 + 10), "31", font=font(34, True), fill=(255, 255, 255))
        d.text((x0 + 210, y0 + 50), "KILLED", font=font(13, True), fill=(250, 204, 21))
    else:  # war / Gaza skyline
        d.rectangle(box, fill=(28, 25, 46))
        for sx, sy in ((30, 12), (90, 26), (150, 10), (220, 30), (260, 14)):
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
        for bx, bw, bh in ((8, 44, 50), (60, 36, 62), (104, 52, 46), (164, 40, 58), (212, 46, 52), (266, 36, 66)):
            d.rectangle([x0 + bx, y1 - 14 - bh, x0 + bx + bw, y1 - 14], fill=(58, 54, 84))
        # smoke columns, kept inside the scene box
        for sx, top in ((80, y0 + 34), (190, y0 + 30), (250, y0 + 36)):
            d.polygon([(x0 + sx, y1 - 76), (x0 + sx + 16, y1 - 76),
                       (x0 + sx + 22, top), (x0 + sx + 6, top)], fill=(120, 116, 140))
        d.text((x0 + 12, y0 + 6), "9 KILLED", font=font(22, True), fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    d.text((28, 14), "Thursday 26 November 2026", font=font(42, True), fill=(255, 255, 255))
    d.text((28, 72), "43 dated stories  ·  9 regions  ·  15 drawn scenes  ·  UTC timeline",
           font=font(19), fill=SKY)
    d.text((W - 28 - font(15, True).getlength("THE WORLD IN ONE DAY"),
            24), "THE WORLD IN ONE DAY", font=font(15, True), fill=GOLD)
    d.text((W - 28 - font(13).getlength("All stories dated 26 Nov 2026"),
            48), "All stories dated 26 Nov 2026", font=font(13), fill=(180, 190, 205))

    # ---- lead cards
    card_w, card_h = 328, 178
    for i, (title, detail, region, kind) in enumerate(LEADS):
        x = 8 + i * (card_w + 8)
        y = 130
        col = REGION_COLORS[region]
        d.rounded_rectangle([x, y, x + card_w, y + card_h], radius=8, fill=CARD, outline=LINE, width=1)
        d.rectangle([x, y, x + card_w, y + 6], fill=col)
        draw_hero_scene(d, kind, (x + 8, y + 12, x + card_w - 8, y + 108))
        lines = wrap(title, font(17, True), card_w - 20)
        yy = y + 114
        for ln in lines[:2]:
            d.text((x + 10, yy), ln, font=font(17, True), fill=INK)
            yy += 21
        rw = font(11, True).getlength(region.upper())
        d.text((x + card_w - 10 - rw, y + card_h - 24), region.upper(),
               font=font(11, True), fill=col)
        dlines = wrap(detail, font(13), card_w - 30 - rw)
        if dlines:
            d.text((x + 10, y + card_h - 24), dlines[0], font=font(13), fill=MUTED)

    # ---- story grid: 4 cols x 10 rows
    gx, gy = 8, 314
    cw, ch = 252, 57
    for idx, (title, detail, region, kind, scene) in enumerate(GRID):
        col_i, row_i = idx % 4, idx // 4
        x = gx + col_i * (cw + 4)
        y = gy + row_i * (ch + 1)
        col = REGION_COLORS[region]
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=5, fill=CARD, outline=LINE, width=1)
        d.rectangle([x, y + 4, x + 4, y + ch - 4], fill=col)
        if scene:
            d.rounded_rectangle([x + 8, y + 6, x + 54, y + ch - 6], radius=4, fill=(238, 242, 248))
            draw_icon(d, kind, (x + 10, y + 8, x + 52, y + ch - 8), col)
            tx = x + 60
        else:
            draw_icon(d, kind, (x + 10, y + 9, x + 46, y + ch - 9), col)
            tx = x + 52
        tw = x + cw - 8 - tx
        tlines = wrap(title, font(14, True), tw)
        yy = y + 6
        for ln in tlines[:2]:
            d.text((tx, yy), ln, font=font(14, True), fill=INK)
            yy += 17
        dlines = wrap(detail, font(11), tw)
        if dlines:
            d.text((tx, yy + 1), dlines[0], font=font(11), fill=MUTED)

    # ---- UTC timeline
    ty = 900
    d.rectangle([0, ty, W, ty + 60], fill=NAVY2)
    d.text((28, ty + 6), "UTC TIMELINE", font=font(13, True), fill=GOLD)
    tl_x0, tl_x1 = 28, W - 28
    d.line([tl_x0, ty + 40, tl_x1, ty + 40], fill=(120, 140, 175), width=2)
    for i, (t, label) in enumerate(TIMELINE):
        cx = tl_x0 + (i + 0.5) * (tl_x1 - tl_x0) / len(TIMELINE)
        d.ellipse([cx - 5, ty + 35, cx + 5, ty + 45], fill=GOLD)
        d.text((cx - font(11, True).getlength(t) / 2, ty + 20), t,
               font=font(11, True), fill=(255, 255, 255))
        lw = font(10).getlength(label)
        d.text((max(8, min(cx - lw / 2, W - 8 - lw)), ty + 47), label,
               font=font(10), fill=(200, 210, 225))

    # ---- footer
    fy = 966
    d.text((28, fy), "Regions: " + "  ·  ".join(REGIONS), font=font(12), fill=MUTED)
    d.text((28, fy + 18),
           "Program-drawn with PIL — no AI images. Sources: Reuters, SCMP, AP, PANA, One Turn (26 Nov 2026).",
           font=font(12), fill=MUTED)
    d.text((28, fy + 36), "make.fun bounty: news-image-20261126  ·  $100 shared by the top 50 entries",
           font=font(12, True), fill=INK)
    return img


def main():
    img = build()
    img.save("/tmp/entry_check.png", format="PNG")
    return img
