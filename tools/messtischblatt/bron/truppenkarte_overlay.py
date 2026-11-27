#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truppenkarte-overlay generator -- v1.0

Genereert een transparante Wehrmacht 'Truppenkarte'-stijl overlay (A3 liggend,
420x297mm) die met pypdf over een map.army-PDF-export gelegd wordt, voor
reenactment-doeleinden (project: Unternehmen Bauernhof e.a.).

Layout gemodelleerd naar een origineel exemplaar (Truppenkarte 39 West Rhenen,
Ausgabe Nr.3, Stand 1942).

------------------------------------------------------------------------
CHANGELOG
v1.0  Eerste vastgezette versie. Bevat:
      - Titelblok (Truppenkarte / sheet-naam / operatienaam), vette schreef-
        loze koppen (Helvetica-Bold) + schreef-cursieve editieregel, exact
        nagebouwd op close-ups van een origineel exemplaar
      - Wit kader (geen vergeling), dunne dubbele kaderlijn, hoofd- en
        subrastertikjes (200 m-onderverdeling) + kleine X/Y-asaanduiding
        linksboven
        Rasternummers zwart (niet rood) nagetekend op hun echte positie --
        positie wordt PER EXPORT gemeten (rasterlijn-detectie via kolom-/
        rijprojectie op een pixelrender, zie top_grid_x/side_grid_y_from_top);
        offset en rotatie verschillen per map.army-export en moeten dus bij
        een nieuwe export opnieuw bepaald worden
      - Zeichenerklärung, blad-overzicht, gegradueerde schaalbalk (dynamisch
        op SCALE_DENOM), uitgevers-/declinatieblok, edition-box
      - Volledig zwart-wit (geen kleuraccenten), passend bij grijswaarden-
        exports uit map.army
------------------------------------------------------------------------
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MM = 72.0 / 25.4


def mm(v):
    return v * MM


PAGE_W = mm(420)
PAGE_H = mm(297)

pdfmetrics.registerFont(TTFont("Cond", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("CondB", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"))

INK = Color(0.08, 0.08, 0.08, alpha=1)
PAPER = Color(1, 1, 1, alpha=1)             # witte marge i.p.v. vergeeld papier
PAPER_EDGE = Color(0.55, 0.45, 0.30, alpha=1)

SHEET_NAME = "HAAKSBERGEN"
SHEET_CODE = "34 Oost \u00b7 Blatt 3907"
OPERATION_NAME = "Unternehmen Bauernhof"
EDITION = "Ausgabe Nr. 1, Stand: 2026"
DECLINATION = "3,3\u00b0"
SCALE_DENOM = 25000  # 1 : 25 000, zoals ingesteld bij export (A3)

TOP_BAND = mm(30)
BOTTOM_BAND = mm(62)
SIDE_BAND = mm(25)

# Empirisch gemeten rasterposities in de huidige map.army-export (grijswaarden-versie),
# via detectie van de doorlopende rasterlijnen zelf (kolom-/rijprojectie), niet de
# (soms verschoven) tekstlabels. Bij een nieuwe export: opnieuw meten met hetzelfde
# recept, want extent/rotatie kan per export verschillen.
TOP_GRID_VALUES = list(range(42, 52))          # bovenkant/onderkant, links -> rechts
SIDE_GRID_VALUES = list(range(86, 79, -1))     # linker-/rechterkant, boven -> onder


def top_grid_x(v):
    return mm(39.9168 * v - 1644.5096)


def side_grid_y_from_top(v):
    return mm(-40.0031 * v + 3487.1508)

c = canvas.Canvas("overlay_v2.pdf", pagesize=(PAGE_W, PAGE_H))


# ------------------------------------------------------------------ paper --
def paper_age():
    # bewust leeg gelaten: geen sepia/vergelingseffect meer, kaart blijft wit/fris
    pass


def margin_bands():
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, PAGE_H - TOP_BAND, PAGE_W, TOP_BAND, stroke=0, fill=1)
    c.rect(0, 0, PAGE_W, BOTTOM_BAND, stroke=0, fill=1)
    c.rect(0, 0, SIDE_BAND, PAGE_H, stroke=0, fill=1)
    c.rect(PAGE_W - SIDE_BAND, 0, SIDE_BAND, PAGE_H, stroke=0, fill=1)
    c.restoreState()


def ruled_lines():
    c.saveState()
    c.setStrokeColor(INK)
    for y in (PAGE_H - TOP_BAND, BOTTOM_BAND):
        c.setLineWidth(1.3)
        c.line(0, y, PAGE_W, y)
        c.setLineWidth(0.4)
        c.line(0, y - mm(1.3), PAGE_W, y - mm(1.3))
    for x in (SIDE_BAND, PAGE_W - SIDE_BAND):
        c.setLineWidth(1.3)
        c.line(x, 0, x, PAGE_H)
    # outer sheet edge
    c.setLineWidth(0.8)
    c.rect(mm(1.5), mm(1.5), PAGE_W - mm(3), PAGE_H - mm(3), stroke=1, fill=0)
    c.restoreState()


def graticule_labels():
    c.saveState()
    c.setFillColor(INK)
    c.setFont("Cond", 6.3)
    top_labels = ["6\u00b040'", "6\u00b050'", "6\u00b055'"]
    xs = [mm(70), mm(210), mm(350)]
    for lbl, x in zip(top_labels, xs):
        c.drawCentredString(x, PAGE_H - TOP_BAND + mm(3), lbl)
    c.saveState()
    c.translate(mm(4.2), mm(150))
    c.rotate(90)
    c.drawCentredString(0, 0, "52\u00b015'")
    c.restoreState()
    c.saveState()
    c.translate(mm(4.2), mm(70))
    c.rotate(90)
    c.drawCentredString(0, 0, "52\u00b010'")
    c.restoreState()
    c.restoreState()


# --------------------------------------------------------------- top band --
def top_band_text():
    c.saveState()
    y_base = PAGE_H - mm(9)
    # left caption
    c.setFillColor(INK)
    c.setFont("Helvetica", 9.5)
    c.drawString(SIDE_BAND + mm(4), y_base, "Topografische kaart van Nederland")
    c.setFont("Helvetica", 9.5)
    c.drawString(SIDE_BAND + mm(4), y_base - mm(6.5), f"schaal 1 : {SCALE_DENOM:,}".replace(",", " "))

    # centre title block
    cx = PAGE_W / 2
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(cx, y_base + mm(1), "Truppenkarte")
    c.setFont("Times-Italic", 8.5)
    c.drawCentredString(cx, y_base - mm(6), EDITION)
    c.setFont("Helvetica-Bold", 9)
    txt = "Nicht f\u00fcr die \u00d6ffentlichkeit bestimmt !"
    c.drawCentredString(cx, y_base - mm(13.5), txt)

    # right sheet name
    rx = PAGE_W - SIDE_BAND - mm(4)
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(rx, y_base, SHEET_NAME)
    c.setFont("Times-Roman", 8.5)
    c.drawRightString(rx, y_base - mm(6.5), SHEET_CODE)
    c.setFont("Times-Italic", 7.5)
    c.drawRightString(rx, y_base - mm(12), OPERATION_NAME)
    c.restoreState()


# ------------------------------------------------------------ legend -------
LINE_SYMBOLS = [
    ("rail2", "Eisenbahn zweigleisig"),
    ("rail1", "Eisenbahn eingleisig"),
    ("road_thick", "Autostra\u00dfe"),
    ("road_med", "Hauptstra\u00dfe im Stadtgebiet"),
    ("road_thin", "Nebenstra\u00dfe"),
    ("track", "Unterhaltener Fahrweg"),
    ("path", "Fu\u00dfweg"),
]
AREA_SYMBOLS = [
    ("wood", "Laubwald"),
    ("water", "Gew\u00e4sser"),
    ("church", "Kirche mit Turm"),
    ("chapel", "Kapelle"),
    ("trig", "Trigonometrischer Punkt"),
    ("height", "H\u00f6he in m \u00fcb. N.A.P."),
]


def sym_line(kind, x, y):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    w = mm(9)
    if kind == "rail2":
        c.setLineWidth(0.5)
        c.line(x, y - mm(0.7), x + w, y - mm(0.7))
        c.line(x, y + mm(0.7), x + w, y + mm(0.7))
        for t in range(6):
            tx = x + t * mm(1.6)
            c.line(tx, y - mm(1.1), tx, y + mm(1.1))
    elif kind == "rail1":
        c.setLineWidth(0.5)
        c.line(x, y, x + w, y)
        for t in range(6):
            tx = x + t * mm(1.6)
            c.line(tx, y - mm(1.1), tx, y + mm(1.1))
    elif kind == "road_thick":
        c.setLineWidth(2.4)
        c.line(x, y, x + w, y)
    elif kind == "road_med":
        c.setLineWidth(1.4)
        c.line(x, y, x + w, y)
    elif kind == "road_thin":
        c.setLineWidth(0.7)
        c.line(x, y, x + w, y)
    elif kind == "track":
        c.setLineWidth(0.5)
        c.line(x, y, x + w, y)
    elif kind == "path":
        c.setLineWidth(0.4)
        dash = 1.6
        xx = x
        while xx < x + w:
            c.line(xx, y, min(xx + mm(dash), x + w), y)
            xx += mm(dash * 2)


def sym_area(kind, x, y):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    if kind == "wood":
        for i in range(3):
            cxp = x + mm(1.2) + i * mm(2.4)
            c.setLineWidth(0.5)
            c.circle(cxp, y, mm(1.0), stroke=1, fill=0)
    elif kind == "water":
        c.setLineWidth(0.5)
        for i in range(3):
            yy = y - mm(1.0) + i * mm(1.0)
            c.line(x, yy, x + mm(8), yy)
    elif kind == "church":
        c.setLineWidth(0.6)
        c.circle(x + mm(1.2), y, mm(0.9), stroke=1, fill=0)
        c.line(x + mm(1.2), y + mm(0.9), x + mm(1.2), y + mm(2.6))
    elif kind == "chapel":
        c.setLineWidth(0.6)
        c.circle(x + mm(1.2), y, mm(0.7), stroke=1, fill=1)
    elif kind == "trig":
        c.setLineWidth(0.6)
        c.circle(x + mm(1.2), y, mm(1.0), stroke=1, fill=0)
        c.line(x + mm(1.2), y, x + mm(1.2) + mm(0.1), y + mm(0.1))
    elif kind == "height":
        c.setFont("Cond", 6)
        c.drawString(x, y - mm(1), "128,4")


def legend():
    x0 = SIDE_BAND + mm(4)
    y_top = BOTTOM_BAND - mm(15)
    c.setFillColor(INK)
    c.setFont("CondB", 7)
    c.drawString(x0, y_top, "ZEICHENERKL\u00c4RUNG")
    c.setLineWidth(0.3)
    c.line(x0, y_top - mm(1.6), x0 + mm(100), y_top - mm(1.6))

    row_h = mm(6.0)
    yy = y_top - mm(6.5)
    for kind, label in LINE_SYMBOLS:
        sym_line(kind, x0, yy)
        c.setFont("Cond", 6.4)
        c.setFillColor(INK)
        c.drawString(x0 + mm(11), yy - mm(1.0), label)
        yy -= row_h

    x1 = x0 + mm(56)
    yy = y_top - mm(6.5)
    for kind, label in AREA_SYMBOLS:
        sym_area(kind, x1, yy)
        c.setFont("Cond", 6.4)
        c.setFillColor(INK)
        c.drawString(x1 + mm(11), yy - mm(1.0), label)
        yy -= row_h


# ---------------------------------------------------------- blad-overzicht -
def sheet_overview(x0, top_y):
    """top_y = y-coordinate of the header baseline; grid hangs below it."""
    c.saveState()
    c.setFont("CondB", 6.5)
    c.setFillColor(INK)
    c.drawString(x0, top_y, "\u00dcBERSICHT DER BL\u00c4TTER 1:25000")
    labels = [["3906", "3907", "3908"],
              ["3906v", "3907v", "3908v"],
              ["3905", "3907.", "3909"]]
    cell = mm(8.0)
    gx = x0
    gy = top_y - mm(5) - cell * 3
    c.setLineWidth(0.4)
    for r in range(3):
        for col in range(3):
            cx0 = gx + col * cell
            cy0 = gy + (2 - r) * cell
            c.rect(cx0, cy0, cell, cell, stroke=1, fill=0)
            bold = (r == 2 and col == 1)
            c.setFont("CondB" if bold else "Cond", 5.8 if bold else 5.4)
            c.drawCentredString(cx0 + cell / 2, cy0 + cell / 2 - mm(0.9), labels[r][col])
    c.restoreState()


# ---------------------------------------------------------------- scale ----
def scale_bar(x0, top_y):
    """top_y = baseline of the 'Ma\u00dfstab' heading; bar and labels hang below it."""
    c.saveState()
    c.setFillColor(INK)
    c.setFont("Helvetica", 13)
    scale_txt = f"{SCALE_DENOM:,}".replace(",", " ")
    c.drawString(x0, top_y, f"Ma\u00dfstab 1 : {scale_txt}")

    # mm on paper per km in reality, derived from the actual export scale
    km_mm = mm(1_000_000 / SCALE_DENOM)
    n_full_km = 1  # how many extra whole-km segments to draw after the subdivided first km
    y0 = top_y - mm(10)
    seg1 = km_mm / 5  # 200 m per block within the first kilometre
    y = y0
    x = x0
    c.setLineWidth(0.3)
    c.setStrokeColor(INK)
    # subdivided first kilometre (200 m alternating blocks)
    for i in range(5):
        if i % 2 == 0:
            c.setFillColor(INK)
        else:
            c.setFillColor(Color(1, 1, 1, alpha=1))
        c.rect(x + i * seg1, y, seg1, mm(2.6), stroke=1, fill=1)
    x += km_mm
    # remaining whole kilometres, alternating solid bar
    for i in range(n_full_km):
        if i % 2 == 0:
            c.setFillColor(INK)
        else:
            c.setFillColor(Color(1, 1, 1, alpha=1))
        c.rect(x + i * km_mm, y, km_mm, mm(2.6), stroke=1, fill=1)
    total = km_mm * (1 + n_full_km)
    c.setFillColor(INK)
    c.setFont("Cond", 6)
    for k in range(2 + n_full_km):
        xx = x0 + k * km_mm if k > 0 else x0
        c.drawCentredString(xx, y - mm(3), "0" if k == 0 else str(k))
    c.drawCentredString(x0 + total / 2, y - mm(7), "km")
    cm_per_km = 100000 / SCALE_DENOM
    cm_txt = f"{cm_per_km:g}".replace(".", ",")
    c.setFont("Cond", 6.3)
    c.drawString(x0, y - mm(11.5), f"({cm_txt} cm der Karte = 1 km der Natur)")
    c.restoreState()


# ----------------------------------------------------------- publisher -----
def publisher_block(x0, top_y, w):
    c.saveState()
    c.setFillColor(INK)
    c.setFont("Cond", 6.6)
    lines = [
        "Herausgegeben im Auftrage des",
        "Wehrmachtsbefehlshabers in den Niederlanden,",
        "Abt. I / Mess.",
    ]
    yy = top_y
    for ln in lines:
        c.drawString(x0, yy, ln)
        yy -= mm(3.4)
    yy -= mm(2)
    c.setFont("Cond", 6.6)
    c.drawString(x0, yy, f"Nadelabweichung: {DECLINATION} westlich")
    yy -= mm(3.4)
    c.drawString(x0, yy, "(siehe Missweisungszeichen op de kaart)")

    box_w = mm(30)
    box_h = mm(15)
    bx = x0 + w - box_w
    by = mm(9)
    c.setLineWidth(0.6)
    c.rect(bx, by, box_w, box_h, stroke=1, fill=0)
    c.setLineWidth(0.2)
    c.line(bx, by + box_h / 2, bx + box_w, by + box_h / 2)
    c.line(bx + box_w / 2, by, bx + box_w / 2, by + box_h)
    c.setFont("CondB", 6.5)
    c.drawCentredString(bx + box_w / 4, by + box_h * 0.75 - mm(1), "Enl")
    c.drawCentredString(bx + box_w * 0.75, by + box_h * 0.75 - mm(1), "50")
    c.setFont("Cond", 5.6)
    c.drawCentredString(bx + box_w / 4, by + box_h * 0.25 - mm(1), SHEET_CODE.split("\u00b7")[0].strip())
    c.drawCentredString(bx + box_w * 0.75, by + box_h * 0.25 - mm(1), "Ausg. Nr.1")
    c.restoreState()


def credit_line():
    c.saveState()
    c.setFillColor(Color(0.25, 0.25, 0.25, alpha=0.9))
    c.setFont("Cond", 5.6)
    c.drawCentredString(PAGE_W / 2, mm(2.6),
                         "Reenactment-hulpmiddel \u2014 kaartbeeld: map.army / OpenTopoMap \u2014 stijloverlay ter illustratie, geen historisch document")
    c.restoreState()


def redraw_grid_numbers():
    """Tekent de originele rasternummers na (die nu onder de witte marges
    verdwenen zijn) vlak buiten de kaderlijn, op hun echte rasterpositie.
    Cijfers in zwart (zoals de rand-index op het origineel); het rode raster
    zelf blijft zichtbaar op de kaart. Kleine tussentikjes elke 200 m erbij,
    net als de fijnere onderverdeling op het origineel."""
    c.saveState()
    top_rule = PAGE_H - TOP_BAND
    bot_rule = BOTTOM_BAND
    left_rule = SIDE_BAND
    right_rule = PAGE_W - SIDE_BAND

    # fijne tussentikjes (elke 1/5 rastercel = 200 m) zonder cijfer
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    for v10 in range(TOP_GRID_VALUES[0] * 5, TOP_GRID_VALUES[-1] * 5 + 1):
        v = v10 / 5
        if v == int(v):
            continue
        x = top_grid_x(v)
        if x < SIDE_BAND or x > PAGE_W - SIDE_BAND:
            continue
        c.line(x, top_rule, x, top_rule + mm(1.1))
        c.line(x, bot_rule, x, bot_rule - mm(1.1))
    for v10 in range(SIDE_GRID_VALUES[-1] * 5, SIDE_GRID_VALUES[0] * 5 + 1):
        v = v10 / 5
        if v == int(v):
            continue
        y_pdf = PAGE_H - side_grid_y_from_top(v)
        if y_pdf < BOTTOM_BAND or y_pdf > PAGE_H - TOP_BAND:
            continue
        c.line(left_rule, y_pdf, left_rule - mm(1.1), y_pdf)
        c.line(right_rule, y_pdf, right_rule + mm(1.1), y_pdf)

    # hoofdtikjes + cijfers
    c.setFont("CondB", 7.5)
    c.setFillColor(INK)
    c.setLineWidth(0.5)
    for v in TOP_GRID_VALUES:
        x = top_grid_x(v)
        if x < SIDE_BAND or x > PAGE_W - SIDE_BAND:
            continue
        c.line(x, top_rule, x, top_rule + mm(2.2))
        c.drawCentredString(x, top_rule + mm(3.0), str(v))
        c.line(x, bot_rule, x, bot_rule - mm(2.2))
        c.drawCentredString(x, bot_rule - mm(6.0), str(v))

    for v in SIDE_GRID_VALUES:
        y = side_grid_y_from_top(v)
        y_pdf = PAGE_H - y
        if y_pdf < BOTTOM_BAND or y_pdf > PAGE_H - TOP_BAND:
            continue
        c.line(left_rule, y_pdf, left_rule - mm(2.2), y_pdf)
        c.drawCentredString(left_rule - mm(6.5), y_pdf - mm(1.3), str(v))
        c.line(right_rule, y_pdf, right_rule + mm(2.2), y_pdf)
        c.drawCentredString(right_rule + mm(6.5), y_pdf - mm(1.3), str(v))

    # kleine assen-aanduiding in de linkerbovenhoek, zoals op het origineel
    c.setFont("Cond", 5.8)
    c.drawString(mm(4), top_rule + mm(3.2), "X \u2192")
    c.saveState()
    c.translate(mm(6), top_rule - mm(3))
    c.rotate(90)
    c.drawString(0, 0, "Y \u2192")
    c.restoreState()
    c.restoreState()


# ------------------------------------------------------------------- run ---
paper_age()
margin_bands()
ruled_lines()
redraw_grid_numbers()
top_band_text()
legend()
sheet_overview(SIDE_BAND + mm(114), mm(50))
scale_bar(SIDE_BAND + mm(150), mm(40))
publisher_block(SIDE_BAND + mm(234), mm(50), mm(130))
credit_line()
c.showPage()
c.save()
print("done")
