#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preußisches Meßtischblatt (4 cm-Karte, 1:25000) -- overlay/template
v0.4  -- geometrie exact opgemeten aan Meßtischblatt 2656 "Arnsberg Süd"
        (Neue Nr. 4614, Preuß. Landesaufnahme 1894, Nachträge 1927).

MEETMETHODE (voor reproduceerbaarheid):
  - scan rechtgezet met +0,178° (verticale kaderlijnen loodrecht gemaakt;
    resterende helling 0,00004 -- verwaarloosbaar)
  - schaal bepaald via twee onafhankelijke wegen die 0,3% overeenkwamen:
      * km-rasterafstand langs de randverdeling: 471,8 px/km
      * de schaalbalk (-1000..+2000 m): 11,875 px/mm
    aangehouden: 11,795 px/mm  (= 471,8 px/km)
  - controle: kaartvlak komt uit op 11,61 x 11,06 km, wat overeenkomt met de
    theoretische Meßtischblatt-uitsnede van 10' lengte x 6' breedte op 51,4°N
    (11,58 x 11,11 km). Meting daarmee bevestigd.

LET OP: het blad is licht scheefgetrokken (papiervervorming). Horizontale en
verticale km-afstanden verschillen 0,7% (473,4 vs 470,3 px/km). Er is met het
gemiddelde gerekend; het sjabloon zelf is wél zuiver haaks.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import fontpad

MM = 72.0 / 25.4


def mm(v):
    return v * MM


# ======================================================== GEMETEN GEOMETRIE ==
# Alle waarden in mm, gemeten aan het origineel (zie kop).

# Meetreferentie (rechtgezette scan, px):
#   links   buitenlijn 985  | zware band 997-1009 | binnenlijn 1020 | neat line 1099
#   rechts  neat line 6596  | binnenlijn 6673,5   | zware band 6684-6697 | buitenlijn 6709
#   boven   buitenlijn 360,5| zware band 373-385  | binnenlijn 395  | neat line 473,5
#   onder   neat line 5708,5| binnenlijn 5786,5   | zware band 5797-5810 | buitenlijn 5821,5
#   papier  x 92..7808, y 104..6579
PAPER_W = 654.2
PAPER_H = 549.0

MAP_W = 466.0          # kaartvlak binnen de neat line (5497 px)
MAP_H = 443.8          # (5235 px)

MARGIN_L = 85.4        # papierrand -> neat line
MARGIN_R = 102.8
MARGIN_T = 31.3
MARGIN_B = 73.8

# kaderopbouw, afstanden naar BUITEN gemeten vanaf de neat line
GRAD_BAND = 6.634      # graduated band (78,25 px)
GAP_INNER = 0.911      # wit tussen binnenlijn en zware band (10,75 px)
HEAVY_W = 1.145        # zware zwarte band (13,5 px)
GAP_OUTER = 1.017      # wit tussen zware band en buitenlijn (12 px)
LW_THIN = 0.18
LW_HAIR = 0.30

# afgeleid: neat line -> buitenlijn = 9,71 mm (114 px, gemeten 1099-985 = 114) OK
OFF_INNER_LINE = GRAD_BAND
OFF_HEAVY_IN = GRAD_BAND + GAP_INNER
OFF_HEAVY_OUT = OFF_HEAVY_IN + HEAVY_W
OFF_OUTER_LINE = OFF_HEAVY_OUT + GAP_OUTER

# --- legendakolom (gemeten aan het origineel, mm vanaf papier-linkerrand) ---
LEG_HEAD_X = 576.5      # 'Zeichenerklärung:' begint hier
LEG_HEAD_Y = 7.2        # basislijn van de kop
LEG_SYM_X = 569.5       # linkerkant symboolkolom
LEG_SYM_W = 9.2         # breedte symboolkolom
LEG_TXT_X = 580.0       # linkerkant tekst/labels én categoriekoppen
LEG_ABK_X1 = 569.9      # afkortingen: kolom 1 afkorting
LEG_ABK_T1 = 578.4      #              kolom 1 uitleg
LEG_ABK_X2 = 595.3      #              kolom 2 afkorting
LEG_ABK_T2 = 601.1      #              kolom 2 uitleg
LEG_PITCH = 2.90        # regelafstand items
LEG_PITCH2 = 5.38       # regelafstand tweeregelige items
LEG_CAT_GAP = 3.75      # extra ruimte vóór een categoriekop
LEG_FS_ITEM = 6.4       # corpsgrootte items
LEG_FS_CAT = 7.4        # corpsgrootte categoriekoppen

# km-raster (1 km = 40 mm bij 1:25000)
KM_MM = 40.0
GRID_OFF_X = 16.0       # neat line links -> rasterlijn 341
GRID_OFF_Y = 36.0       # neat line boven -> rasterlijn 5790
GRID_N_X = 12           # rasterlijnen 341..352
GRID_N_Y = 11           # rasterlijnen 5790..5780

# ============================================================== PARAMETERS ===
SHEET_NAME = "Wilp"
SHEET_SUB = "Nord."
NEUE_NR = "3312"
MTB_NR = "1041"
GRID_X_START = 300               # rasterwaarden links -> rechts (UTM 32U east, km)
GRID_X_PREFIX = "32U"            # zone-aanduiding
GRID_Y_START = 5792              # rasterwaarden boven -> onder (aflopend, UTM north km)
SCALE_DENOM_STR = "25000"
LON_LABEL = "6\u00b005' \u00f6.L.v.Greenwich."
LAT_TOP = "52\u00b015,0'"
LAT_BOT = "52\u00b009,0'"
LON_RIGHT = "6\u00b014'"
AUFNAHME = "Nach niederl\u00e4ndischer Landesaufnahme."
NACHTRAG = "Reichsamt f\u00fcr Landesaufnahme, einzelne Nachtr\u00e4ge 1943."
KREIS_A_NR, KREIS_A = "17", "Gem. Voorst,"
KREIS_B_NR, KREIS_B = "18", "\u201e   Deventer,"
REG_BEZ = "Prov. Gelderland."

# ================================================================== FONTS ====
pdfmetrics.registerFont(TTFont("Didone", fontpad.pad("fonts/PlayfairDisplay[wght].ttf")))
pdfmetrics.registerFont(TTFont("DidoneI", fontpad.pad("fonts/PlayfairDisplay-Italic[wght].ttf")))
SER = "Ser"
SERI = "SerI"
SERB = "SerB"
SERCI = "SerCI"
pdfmetrics.registerFont(TTFont(SER, fontpad.pad("DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont(SERI, fontpad.pad("DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont(SERB, fontpad.pad("DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont(SERCI, fontpad.pad("DejaVuSerifCondensed-Italic.ttf")))

INK = Color(0.13, 0.12, 0.10, alpha=1)

c = canvas.Canvas("mtb_template.pdf", pagesize=(mm(PAPER_W), mm(PAPER_H)))

# neat-line rechthoek in PDF-coördinaten (oorsprong linksonder)
NX0 = mm(MARGIN_L)
NX1 = mm(MARGIN_L + MAP_W)
NY1 = mm(PAPER_H - MARGIN_T)
NY0 = mm(PAPER_H - MARGIN_T - MAP_H)


def rect_out(off, lw):
    """Rechthoek op afstand `off` mm buiten de neat line."""
    o = mm(off)
    c.setLineWidth(lw)
    c.rect(NX0 - o, NY0 - o, (NX1 - NX0) + 2 * o, (NY1 - NY0) + 2 * o, stroke=1, fill=0)


# =================================================================== KADER ===
def draw_frame():
    c.saveState()
    c.setStrokeColor(INK)
    # neat line
    rect_out(0, LW_THIN)
    # binnenlijn van de graduated band
    rect_out(OFF_INNER_LINE, LW_THIN)
    # zware band: als dikke lijn op het midden van de band
    mid = (OFF_HEAVY_IN + OFF_HEAVY_OUT) / 2.0
    rect_out(mid, mm(HEAVY_W))
    # buitenlijn
    rect_out(OFF_OUTER_LINE, LW_HAIR)
    c.restoreState()


def grid_positions():
    xs = [NX0 + mm(GRID_OFF_X + i * KM_MM) for i in range(GRID_N_X)]
    ys = [NY1 - mm(GRID_OFF_Y + i * KM_MM) for i in range(GRID_N_Y)]
    return xs, ys


def draw_graduated_band():
    """Rasternummers in de band, met scheidingsstreepjes over de bandbreedte."""
    c.saveState()
    # de band zelf wit maken (het kaartbeeld loopt tot de neat line)
    b = mm(GRAD_BAND)
    c.setFillColor(Color(1, 1, 1, alpha=1))
    c.rect(NX0 - b, NY0 - b, (NX1 - NX0) + 2 * b, b, stroke=0, fill=1)
    c.rect(NX0 - b, NY1, (NX1 - NX0) + 2 * b, b, stroke=0, fill=1)
    c.rect(NX0 - b, NY0, b, NY1 - NY0, stroke=0, fill=1)
    c.rect(NX1, NY0, b, NY1 - NY0, stroke=0, fill=1)
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    xs, ys = grid_positions()
    b = mm(GRAD_BAND)

    c.setLineWidth(LW_THIN)
    for i, x in enumerate(xs):
        for yb, sgn in ((NY1, 1), (NY0, -1)):
            c.line(x, yb, x, yb + sgn * b)
        full = GRID_X_START + i
        val = str(full)[-2:]
        c.setFont(SER, 9)
        c.drawString(x + mm(1.2), NY1 + mm(2.4), val)
        c.drawString(x + mm(1.2), NY0 - mm(5.2), val)
    for j, y in enumerate(ys):
        for xb, sgn in ((NX0, -1), (NX1, 1)):
            c.line(xb, y, xb + sgn * b, y)
        val = str(GRID_Y_START - j)
        short = val[-2:]
        c.setFont(SER, 9)
        c.drawRightString(NX0 - mm(1.4), y + mm(1.6), short)
        c.drawString(NX1 + mm(1.4), y + mm(1.6), short)

    # volledige waarde met voorloopcijfers in de hoeken
    # volledige waarde bij de eerste rasterlijn, als klein voorloopcijfer
    c.setFont(SER, 6.0)
    pre_x = str(GRID_X_START)[:-2]
    pre_y = str(GRID_Y_START)[:-2]
    wx = pdfmetrics.stringWidth(pre_x, SER, 6.0)
    c.drawString(xs[0] + mm(1.2) - wx - 0.6, NY1 + mm(2.4), pre_x)
    c.drawString(xs[0] + mm(1.2) - wx - 0.6, NY0 - mm(5.2), pre_x)
    wy = pdfmetrics.stringWidth(pre_y, SER, 6.0)
    c.drawString(NX0 - mm(1.4) - pdfmetrics.stringWidth("90", SER, 9) - wy - 0.6,
                 ys[0] + mm(1.6), pre_y)
    c.drawString(NX1 + mm(1.4) - wy - 0.6, ys[0] + mm(1.6), pre_y)
    c.restoreState()


def draw_fine_ticks():
    """NIET GEBRUIKT. Het origineel heeft geen fijne verdeling in de band --
    de band is daar gevuld met de hoogtecijfers van de hoogtelijnen die de
    kaartrand snijden. Functie blijft staan voor het geval je 'm toch wilt."""
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(0.12)
    t = mm(1.5)
    step = mm(KM_MM / 10.0)
    xs, ys = grid_positions()
    x = xs[0]
    while x <= xs[-1] + 1:
        c.line(x, NY1, x, NY1 + t)
        c.line(x, NY0, x, NY0 - t)
        x += step
    y = ys[0]
    while y >= ys[-1] - 1:
        c.line(NX0, y, NX0 - t, y)
        c.line(NX1, y, NX1 + t, y)
        y -= step
    c.restoreState()


def draw_geo_labels():
    """Lengte-/breedtegraden. Op het origineel staan die in de vrije marge
    net buiten het kader; het kaartbeeld loopt hier tot de neat line, dus
    binnen het kaartvlak zetten zou onleesbaar zijn."""
    c.saveState()
    c.setFillColor(INK)
    o = mm(OFF_OUTER_LINE)
    c.setFont(SER, 8)
    # lengtegraad: boven het kader links, onder het kader rechts
    c.drawString(NX0 + mm(46), NY1 + o + mm(2.0), LON_LABEL)
    c.drawRightString(NX1 - mm(6), NY0 - o - mm(3.0), LON_RIGHT)
    # breedtegraad: gekanteld in de linkermarge, bij de boven- en onderrand
    for lbl, yy in ((LAT_TOP, NY1 - mm(6)), (LAT_BOT, NY0 + mm(6))):
        c.saveState()
        c.translate(NX0 - o - mm(2.2), yy)
        c.rotate(90)
        c.setFont(SER, 8)
        c.drawString(0, 0, lbl)
        c.restoreState()
    c.restoreState()


# ================================================================== TITEL ====
def draw_title():
    """Alle posities in mm vanaf de papier-linkerbovenhoek, gemeten aan het origineel:
       sectorbox   x 85,5..103,3   y 4,1..24,9
       'Aufgenommen' tekst x 109,2..123,7  y 9,2..17,0
       titel 'Arnsberg.'  x 296,1..341,8 (midden 319,0)  y 8,2..18,2 (kaphoogte 10,0)
       blok rechtsboven   x 467,2..549,4  y 2,0..15,3
    """
    c.saveState()
    c.setFillColor(INK)

    def PX(v):      # mm vanaf linkerpapierrand -> PDF x
        return mm(v)

    def PY(v):      # mm vanaf bovenpapierrand -> PDF y
        return mm(PAPER_H - v)

    # --- sectordiagram: gesloten vierkant met trapvormige scheidslijn ---
    # Gemeten aan het origineel (mm vanaf papier-linkerbovenhoek):
    #   omtrek   x 85,50 .. 103,22   y 4,11 .. 21,92
    #   trapjes  verticaal x 94,32 en 99,53 ; horizontaal y 7,33 en 10,47
    L, R = 85.50, 103.22
    T, B = 4.11, 21.92
    S1, S2 = 94.32, 99.53          # verticale trapjes
    H1, H2 = 7.33, 10.47           # horizontale trapjes
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.rect(PX(L), PY(B), mm(R - L), mm(B - T), stroke=1, fill=0)
    # de trap die sector 1 (rechtsboven) van sector 2 scheidt
    c.setLineWidth(0.45)
    c.line(PX(S1), PY(T), PX(S1), PY(H1))
    c.line(PX(S1), PY(H1), PX(S2), PY(H1))
    c.line(PX(S2), PY(H1), PX(S2), PY(H2))
    c.line(PX(S2), PY(H2), PX(R), PY(H2))
    c.setFont(SER, 6.2)
    c.setFillColor(INK)
    c.drawCentredString(PX(100.6), PY(6.6), "1")
    c.drawCentredString(PX(91.6), PY(14.6), "2")

    # --- 'Aufgenommen:' + namen ---
    tx = PX(109.2)
    c.setFont(SERI, 7.4)
    c.drawString(tx, PY(11.0), "Aufgenommen:")
    c.setFont(SERI, 6.2)
    c.drawString(tx, PY(14.3), "1  Prlt. N.N.")
    c.drawString(tx, PY(16.9), "2  Top. N.N.")

    # --- titel, gecentreerd op x = 319,0 mm, kaphoogte 10 mm ---
    c.setFont("Didone", 29.0)
    for dx in (0, 0.3):
        c.drawCentredString(PX(319.0) + dx, PY(15.9), f"{SHEET_NAME}.")
    if SHEET_SUB:
        c.setFont(SER, 8.5)
        c.drawCentredString(PX(319.0), PY(19.3), SHEET_SUB)

    # --- blok rechtsboven ---
    rx = PX(549.4)
    c.setFont(SER, 8.5)
    c.drawRightString(PX(521.0), PY(7.2), "Neue Nr.")
    c.setFont("Helvetica-Bold", 20)
    c.drawRightString(rx, PY(8.0), NEUE_NR)
    c.setFont(SER, 11)
    c.drawRightString(PX(497.0), PY(19.0), "(4 cm-Karte)")
    c.setFont(SER, 13)
    c.drawRightString(rx, PY(19.0), f"Me\u00dftischblatt {MTB_NR}")
    c.restoreState()


# ================================================================= ONDER =====
def draw_bottom_left():
    """Gemeten aan het origineel (mm vanaf papier-linkerbovenhoek):
         'Preußische Landesaufnahme 1894.'  x 85,8..161,2   y 488,0..491,7
         Kreis-blok met accolade            x 85,4..193,5   y 496,0..504,9
         'Reichsamt für Landesaufnahme...'  x 84,9..157,4   y 507,2..510,2
    """
    c.saveState()
    c.setFillColor(INK)
    c.setStrokeColor(INK)

    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    c.setFont(SERI, 7.6)
    c.drawString(PX(85.8), PY(491.7), AUFNAHME)

    # twee Kreis-regels met omcirkeld nummer
    c.setFont(SERI, 10.5)
    rows = ((KREIS_A_NR, KREIS_A, 500.0), (KREIS_B_NR, KREIS_B, 504.9))
    for nr, txt, yy in rows:
        c.setLineWidth(0.45)
        c.ellipse(PX(85.4), PY(yy) - mm(0.9), PX(91.6), PY(yy) + mm(2.8),
                  stroke=1, fill=0)
        c.setFont(SER, 6.2)
        c.drawCentredString(PX(88.5), PY(yy), nr)
        c.setFont(SERI, 10.5)
        c.drawString(PX(93.5), PY(yy), txt)

    # accolade tussen de twee regels en de Reg.Bez.-regel
    bx = PX(137.0)
    c.setLineWidth(0.55)
    c.line(bx, PY(505.6), bx, PY(497.2))
    c.line(bx, PY(505.6), bx + mm(1.0), PY(505.6))
    c.line(bx, PY(497.2), bx + mm(1.0), PY(497.2))
    c.setFont(SERI, 10.5)
    c.drawString(PX(139.5), PY(502.0), REG_BEZ)

    c.setFont(SERI, 7.0)
    c.drawString(PX(84.9), PY(510.2), NACHTRAG)
    c.restoreState()


def draw_scalebar():
    """Gemeten aan het origineel:
         titelregel   x 288,9..368,7   y 488,9..491,6
         hoofdbalk    x 249,2..370,0   y 495,4..496,0   (= 120,8 mm = 3000 m)
         Schritt-schaal                y 497,8..498,4
       De balk loopt van -1000 m tot +2000 m; het nulpunt ligt op x 289,2.
       De Schritt-verdeling deelt dezelfde balk (2500 Schritt = 2000 m).
    """
    c.saveState()
    c.setFillColor(INK)
    c.setStrokeColor(INK)

    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    scale_txt = f"{SCALE_DENOM_STR}"
    c.setFont(SER, 9.5)
    c.drawCentredString(PX(328.8), PY(490.6),
                        f"1:{scale_txt}  (4 cm der Karte = 1 km der Natur)")

    X0, X1 = 249.2, 370.0            # -1000 m .. +2000 m
    XZERO = 289.2                    # 0 m
    MMPM = (X1 - X0) / 3000.0        # mm per meter

    def mx(meters):
        return PX(XZERO + meters * MMPM)

    ytop, ybot = 495.4, 496.0
    h = mm(ybot - ytop)

    # ---- Meter-schaal ----
    c.setLineWidth(0.35)
    c.rect(PX(X0), PY(ybot), PX(X1) - PX(X0), h, stroke=1, fill=0)
    # linkerdeel -1000..0 fijn verdeeld per 100 m, afwisselend gevuld
    for i in range(10):
        if i % 2 == 0:
            c.setFillColor(INK)
            c.rect(mx(-1000 + i * 100), PY(ybot), 100 * MMPM * MM, h,
                   stroke=0, fill=1)
    # rechterdeel per 500 m afwisselend
    for k, s in enumerate(range(0, 2000, 500)):
        if k % 2 == 0:
            c.setFillColor(INK)
            c.rect(mx(s), PY(ybot), 500 * MMPM * MM, h, stroke=0, fill=1)

    c.setFillColor(INK)
    c.setFont(SERCI, 5.6)
    for v in (-1000, -500, 0, 500, 1000, 1500):
        c.drawCentredString(mx(v), PY(493.4), str(abs(v)))
    c.drawString(mx(2000) + mm(1.6), PY(493.4), "2000 Meter = 2 Kilometer")

    # ---- Schritt-schaal (zelfde balk, 2500 Schritt = 2000 m) ----
    M_PER_SCHRITT = 0.8
    sy = 498.4
    c.setLineWidth(0.3)
    c.line(PX(X0), PY(sy), mx(2000), PY(sy))
    for s in range(-1000, 2501, 500):
        xx = mx(s * M_PER_SCHRITT)
        c.line(xx, PY(sy), xx, PY(sy - 1.3))
    c.setFont(SERCI, 5.6)
    for s in (-1000, -500, 0, 500, 1000, 1500, 2000):
        c.drawCentredString(mx(s * M_PER_SCHRITT), PY(501.0), str(abs(s)))
    c.drawString(mx(2500 * M_PER_SCHRITT) + mm(1.6), PY(501.0), "2500 Schritt")
    c.restoreState()


def draw_copyright():
    """Gemeten aan het origineel: blok x 459,8..550,8  y 488,1..496,1
       (drie regels, rechts uitgevuld tegen x 550,8)."""
    c.saveState()
    c.setFillColor(INK)

    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    c.setFont(SERI, 6.8)
    lines = [
        "Nachdruck und Vervielf\u00e4ltigung jeder Art, auch einzelner Teile, sowie",
        "die Anfertigung von Vergr\u00f6\u00dferungen oder Verkleinerungen sind verboten",
        "und werden gerichtlich auf Grund des Urheberschutzgesetzes verfolgt.",
    ]
    y = 491.0
    for ln in lines:
        c.drawRightString(PX(550.8), PY(y), ln)
        y += 2.7
    c.restoreState()


ADJ_TOP = ("Olst", "1021")        # aangrenzend blad boven
ADJ_BOTTOM = ("Zutphen", "1061")    # onder
ADJ_LEFT = ("Apeldoorn", "1040")       # links
ADJ_RIGHT = ("Lochem", "1042")      # rechts


EDGE_HEIGHTS_FILE = "edge_heights.json"


def draw_edge_heights():
    """Hoogtecijfers in de graduated band, bij elke hoogtelijn die de
    kaartrand snijdt -- zoals het origineel dat doet.

    De POSITIE komt uit de kaart zelf (gedetecteerde bruine hoogtelijn op
    de neat line); de WAARDE is geinterpoleerd uit de hoogtepunten die met
    OCR uit het kaartbeeld zijn gehaald, afgerond op 2,5 m. De waarde is
    dus een benadering: de bronkaart labelt haar hoogtelijnen niet."""
    import json
    import os
    if not os.path.exists(EDGE_HEIGHTS_FILE):
        return
    items = json.load(open(EDGE_HEIGHTS_FILE))

    # Opeenvolgende gelijke waarden langs dezelfde rand uitdunnen. In vlak
    # rivierland levert het gladde hoogtevlak anders rijtjes van vijf keer
    # hetzelfde getal op; een kaartmaker labelt een hoogtelijn ook maar een
    # keer per kruising. Minimale onderlinge afstand: 7% van de randlengte.
    byedge = {}
    for kind, frac, val in items:
        byedge.setdefault(kind, []).append((frac, val))
    items = []
    for kind, lst in byedge.items():
        lst.sort()
        last_val, last_frac = None, -9.0
        for frac, val in lst:
            if val == last_val and (frac - last_frac) < 0.07:
                continue
            items.append([kind, frac, val])
            last_val, last_frac = val, frac

    c.saveState()
    c.setFillColor(INK)
    b = mm(GRAD_BAND)
    fs = 4.6
    for kind, frac, val in items:
        lbl = f"{val:g}".replace(".", ",")
        if kind in ("top", "bottom"):
            x = NX0 + (NX1 - NX0) * frac
            if x < NX0 + mm(3) or x > NX1 - mm(3):
                continue
            # rasternummers staan direct rechts van hun lijn: ruimte laten
            if any(-mm(2.0) < (x - gx) < mm(8.5) for gx in grid_positions()[0]):
                continue
            # rechts in de band staan de aangrenzende bladnamen
            if x > NX1 - mm(46):
                continue
            yb = (NY1 + mm(1.0)) if kind == "top" else (NY0 - b + mm(1.0))
            c.saveState()
            c.translate(x, yb)
            c.rotate(90)
            c.setFont(SERCI, fs)
            c.drawString(0, 0, lbl)
            c.restoreState()
        else:
            y = NY1 - (NY1 - NY0) * frac
            if y < NY0 + mm(3) or y > NY1 - mm(3):
                continue
            if any(abs(y - gy) < mm(4.6) for gy in grid_positions()[1]):
                continue
            # zone van de gekantelde aangrenzende-bladnaam vrijhouden
            gys = grid_positions()[1]
            if len(gys) >= 7:
                ymid = (gys[5] + gys[6]) / 2.0
                if abs(y - ymid) < mm(13):
                    continue
            c.setFont(SERCI, fs)
            if kind == "left":
                c.drawRightString(NX0 - mm(1.2), y - mm(0.7), lbl)
            else:
                c.drawString(NX1 + mm(1.2), y - mm(0.7), lbl)
    c.restoreState()


def draw_adjacent_sheets():
    """Namen en nummers van de aangrenzende bladen, in de graduated band --
    zoals het origineel 'Arnsberg Nord. 2582', 'Olpe', 'Meschede.',
    'Balve. 2855' en 'Endorf 2726' in de randband zet."""
    c.saveState()
    c.setFillColor(INK)
    xs, ys = grid_positions()

    # boven: rechts in de band, cursief
    nm, nr = ADJ_TOP
    c.setFont(SERI, 7.0)
    c.drawRightString(NX1 - mm(14), NY1 + mm(4.6), nm + ".")
    c.setFont(SERI, 5.2)
    c.drawRightString(NX1 - mm(14), NY1 + mm(1.8), nr + ".")

    # onder
    nm, nr = ADJ_BOTTOM
    c.setFont(SERI, 7.0)
    c.drawRightString(NX1 - mm(14), NY0 - mm(2.4), nm + ".")
    c.setFont(SERI, 5.2)
    c.drawRightString(NX1 - mm(14), NY0 - mm(5.0), nr + ".")

    # links en rechts: gekanteld in de band, midden TUSSEN twee rasterlijnen
    # (op de hartlijn van het blad valt een rasternummer, dat botst)
    if len(ys) >= 7:
        y_mid = (ys[5] + ys[6]) / 2.0
    else:
        y_mid = (NY0 + NY1) / 2
    for nm_nr, xb, ang in ((ADJ_LEFT, NX0 - mm(GRAD_BAND) + mm(1.6), 90),
                           (ADJ_RIGHT, NX1 + mm(GRAD_BAND) - mm(1.6), -90)):
        nm, nr = nm_nr
        c.saveState()
        c.translate(xb, y_mid)
        c.rotate(ang)
        c.setFont(SERI, 7.0)
        c.drawCentredString(0, 0, nm + ".")
        c.restoreState()
    c.restoreState()


def draw_greiferkante():
    """Grijperrand-aanduiding, verticaal in de linkermarge.
    Gemeten op het origineel: x 66,1..79,9  y 180,0..299,9 (gekanteld)."""
    c.saveState()
    c.setFillColor(INK)
    c.translate(mm(74.0), mm(PAPER_H - 300.0))
    c.rotate(90)
    c.setFont("Helvetica", 8)
    txt = "Greiferkante"
    x = 0
    for ch in txt:
        c.drawString(x, 0, ch)
        x += pdfmetrics.stringWidth(ch, "Helvetica", 8) + 1.9
    c.restoreState()


def draw_ziehkante():
    """Gemeten: x 397,2..411,3  y 511,4..514,8 -- schreefloze letter,
       ruim gespatieerd (snijaanduiding voor de drukkerij)."""
    c.saveState()
    c.setFillColor(INK)
    c.setFont("Helvetica", 7)
    txt = "Ziehkante"
    x = mm(397.2)
    for ch in txt:
        c.drawString(x, mm(PAPER_H - 514.8), ch)
        x += pdfmetrics.stringWidth(ch, "Helvetica", 7) + 0.55
    c.restoreState()


import mtb_symbols as S

# ============================================== LEGENDA-INHOUD (origineel) ==
# ('cat', tekst) | ('item', symboolfunctie, label) | ('item2', fn, r1, r2)
# ('pair', fn1, lbl1, fn2, lbl2) voor de twee-koloms vlaksymbolen
LEGEND = [
    ("cat", "Grenzen:"),
    ("item", S.sym_reichsgrenze, "Reichs-oder Landesgrenze"),
    ("item", S.sym_provinzgrenze, "Provinz-oder Regierungsbezirksgrenze"),
    ("item", S.sym_kreisgrenze, "Kreisgrenze"),
    ("item", S.sym_gemeindegrenze, "Gemeindegrenze"),
    ("cat", "Eisenbahnen:"),
    ("item2", S.sym_bahn_mehrgleisig, "mehrgleisige Haupt-u. vollspurige", "Nebenbahn"),
    ("item2", S.sym_bahn_eingleisig, "eingleisige Haupt-u. vollspurige", "Nebenbahn"),
    ("item", S.sym_kleinbahn, "Vollspurige nebenbahn\u00e4hnliche Kleinbahn"),
    ("item", S.sym_schmalspur, "Schmalspurige Nebenbahn"),
    ("item", S.sym_schmalspur_klein, "Schmalspurige nebenbahn\u00e4hnliche Kleinb."),
    ("item", S.sym_wirtschaftsbahn, "Stra\u00dfen-u. Wirtschaftsbahn"),
    ("item", S.sym_seilbahn, "Seil-und Schwebebahn"),
    ("cat", "Kraftfahrbahnen:"),
    ("note", "im Bau"),
    ("item", S.sym_kraftfahrbahn, ""),
    ("cat", "Stra\u00dfen:"),
    ("item", S.sym_reichsstrasse, "Reichsstra\u00dfe"),
    ("item3", S.sym_strasse_IA,
     "I A  etwa 5,5 m Mindestnutzbreite mit gutem Unter-",
     "bau, f\u00fcr Lastkraftwagen zu jeder Jahreszeit",
     "unbedingt brauchbar"),
    ("item2", S.sym_strasse_IB,
     "I B  weniger fest, etwa 4 m Mindestnutzbreite,",
     "f\u00fcr Lastkraftwagen nur bedingt brauchbar"),
    ("cat", "Wege:"),
    ("item3", S.sym_weg_IIA,
     "II A  Unterhaltener Fahrweg, f\u00fcr einzelne Kraft-",
     "wagen zu jeder Zeit brauchbar, abgesehen von",
     "au\u00dfergew\u00f6hnlichen Witterungsverh\u00e4ltnissen"),
    ("item", S.sym_weg_IIB, "II B  Unterhaltener Fahrweg"),
    ("item", S.sym_feldweg, "III  Feld-und Waldwege"),
    ("item", S.sym_fussweg, "Fu\u00dfweg"),
    ("gap", 3.0),
    ("pair", S.sym_laubwald, "Laubwald", S.sym_nadelwald, "Nadelwald"),
    ("pair", S.sym_mischwald, "Mischwald", S.sym_buschwerk, "Buschwerk u.|Weidenanpflanzg."),
    ("pair", S.sym_heide, "Heide u.|\u00d6dland", S.sym_sand, "Sand|oder Kies"),
    ("pair", S.sym_wiese, "Wiese|(nasse Wiese)", S.sym_bruch, "Bruch mit|Torfstich"),
    ("pair", S.sym_weingarten, "Weingarten", S.sym_hopfen, "Hopfenan-|pflanzung"),
    ("pair", S.sym_park, "Park", S.sym_baumschule, "Baumschule"),
    ("gap", 1.5),
    ("wide", S.sym_friedhof, "Friedhof f. Christen u. Nichtchristen"),
    ("gap", 1.5),
    ("wide", S.sym_bruchfeld, "Bruchfeld (durch Bergbau unterh\u00f6hlt)"),
    ("gap", 3.0),
    ("item", S.sym_damm, "Damm"),
    ("item", S.sym_drahtzaun, "Drahtzaun"),
    ("item", S.sym_fels, "Fels"),
    ("item", S.sym_hecke, "Hecke"),
    ("item", S.sym_knick, "Knick (kleiner Wall mit Hecke)"),
    ("item", S.sym_mauer, "Mauer"),
    ("item", S.sym_trockengraben, "Trockener Graben"),
    ("item", S.sym_wall, "Wall (Feldeinfriedigung)"),
    ("item", S.sym_zaun, "Zaun"),
    ("anchor", 182.0),
    ("pt", S.pt_denkmal, "Denkm.", "Denkmal"),
    ("pt", S.pt_einzelgrab, "+", "Einzelgrab"),
    ("pt", S.pt_block, "Err. Block", "Erratischer Block"),
    ("pt", S.pt_foersterei, "F., W.W.", "F\u00f6rsterei, Waldw\u00e4rter"),
    ("pt", S.pt_funkstelle, "F. St.", "Funkstelle"),
    ("pt", S.pt_funkturm, "F. T.", "Funkturm (\u00fcber 60 m hoch)"),
    ("pt", S.pt_grenzzeichen, "", "Grenzzeichen"),
    ("pt", S.pt_grube, "", "Grube, Steinbruch"),
    ("pt", S.pt_heiligenbild, "Kp.", "Heiligenbild, Kapelle"),
    ("pt", S.pt_baum, "", "Hervorragender Baum"),
    ("pt", S.pt_hoehenpunkt, "113,5", "H\u00f6henpunkt"),
    ("pt", S.pt_huenenstein, "", "H\u00fcnenstein, H\u00fcnengrab"),
    ("pt", S.pt_kilometerstein, "120", "Kilometerstein"),
    ("pt", S.pt_kirche_turm, "", "Kirche"),
    ("pt", S.pt_denkmal, "Mlst.", "Meilenstein"),
    ("pt", S.pt_hoehenpunkt, "322,71", "Niv.-Punkt"),
    ("pt", S.pt_pegel, "P.", "Pegel"),
    ("pt", S.pt_ruine, "R.", "Ruine"),
    ("pt", S.pt_bergwerk, "", "Bergwerk, im Betrieb u. verlassen"),
    ("pt", S.pt_schlachtfeld, "20.8.14.", "Schlacht-, Gefechtsfeld"),
    ("pt", S.pt_schornstein, "", "Schornstein, frei u. im Haus"),
    ("pt", S.pt_trig, "416,5", "Trig. Punkt"),
    ("pt", S.pt_turm, "T., W.", "Turm, Warte"),
    ("pt", S.pt_wasserturm, "W.T.", "Wasserturm"),
    ("pt", S.pt_wassermuehle, "", "Wasserm\u00fchle"),
    ("pt", S.pt_wegweiser, "", "Wegweiser"),
    ("pt", S.pt_windmotor, "", "Windmotor"),
    ("pt", S.pt_windmuehle, "", "Windm\u00fchle"),
]

ABK = [
    ("Abl.", "Ablage", "Kol.", "Kolonie"),
    ("Anl.St.", "Anlegestelle", "K.D.", "Kulturgeschichtl. Denkm."),
    ("Bf.", "Bahnhof", "(M.)", "M\u00fchle, weithin sichtbar"),
    ("BW.", "Bahnw\u00e4rter", "N.D.", "Naturdenkmal"),
    ("Cha.", "Chausseehaus", "N.S.G.", "Naturschutzgebiet"),
    ("D.M.", "Dampfm\u00fchle", "\u00d6.M.", "\u00d6lm\u00fchle"),
    ("Dom.", "Dom\u00e4ne", "Pav.", "Pavillon"),
    ("Ehr.Fdhf.", "Ehrenfriedhof|f\u00fcr Krieger", "Sch.", "Scheune"),
    ("Fbr.", "Fabrik", "Schp.", "Schuppen"),
    ("H.", "H\u00fctte", "St.", "Stall"),
    ("Hp.", "Haltepunkt", "S.W.", "S\u00e4gewerk"),
    ("Jg.Hb.", "Jugendherberge", "T.O.", "Teerofen"),
    ("K.O.", "Kalkofen", "Vw.", "Vorwerk"),
    ("Kas.", "Kaserne", "Wbh.", "Wasserbeh\u00e4lter"),
    ("(K.)", "Kirche, weithin|sichtbar", "Whs.", "Wirtshaus"),
    ("Kr.", "Krug", "Zgl.", "Ziegelei"),
]


def draw_legend():
    """Rendert de rechterkolom. Posities/afstanden zijn de gemeten waarden."""
    c.saveState()
    c.setFillColor(INK)
    c.setStrokeColor(INK)

    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    # kop
    c.setFont("Didone", 15)
    c.drawString(PX(LEG_HEAD_X), PY(LEG_HEAD_Y), "Zeichenerkl\u00e4rung:")

    y = 12.0                      # loopt naar beneden in mm vanaf papierbovenrand
    symw = mm(LEG_SYM_W)
    symx = PX(LEG_SYM_X)
    txtx = PX(LEG_TXT_X)

    for entry in LEGEND:
        kind = entry[0]

        if kind == "gap":
            y += entry[1]
            continue

        if kind == "anchor":
            y = max(y, entry[1])
            continue

        if kind == "cat":
            y += LEG_CAT_GAP
            c.setFont(SERI, LEG_FS_CAT)
            c.setFillColor(INK)
            c.drawString(txtx, PY(y), entry[1])
            y += LEG_PITCH
            continue

        if kind == "note":
            c.setFont(SERI, LEG_FS_ITEM)
            c.drawString(PX(LEG_TXT_X + 14), PY(y), entry[1])
            y += LEG_PITCH * 0.8
            continue

        if kind == "item":
            fn, label = entry[1], entry[2]
            fn(c, symx, PY(y - 0.9), symw, mm, INK)
            if label:
                c.setFont(SERI, LEG_FS_ITEM)
                c.setFillColor(INK)
                c.drawString(txtx, PY(y), label)
            y += LEG_PITCH
            continue

        if kind == "item2":
            fn, l1, l2 = entry[1], entry[2], entry[3]
            fn(c, symx, PY(y - 0.9), symw, mm, INK)
            c.setFont(SERI, LEG_FS_ITEM)
            c.setFillColor(INK)
            c.drawString(txtx, PY(y), l1)
            c.drawString(txtx, PY(y + 2.5), l2)
            y += LEG_PITCH2
            continue

        if kind == "item3":
            fn = entry[1]
            fn(c, symx, PY(y - 0.9), symw, mm, INK)
            c.setFont(SERI, LEG_FS_ITEM)
            c.setFillColor(INK)
            for k, ln in enumerate(entry[2:5]):
                c.drawString(txtx, PY(y + k * 2.5), ln)
            y += LEG_PITCH2 + 2.5
            continue

        if kind == "pair":
            fn1, l1, fn2, l2 = entry[1], entry[2], entry[3], entry[4]
            h = 4.6
            fn1(c, symx, PY(y + 1.0), mm(7.2), mm, INK)
            fn2(c, PX(LEG_TXT_X + 20.0), PY(y + 1.0), mm(7.2), mm, INK)
            c.setFont(SERI, LEG_FS_ITEM)
            c.setFillColor(INK)
            for col_x, lbl in ((LEG_TXT_X, l1), (LEG_TXT_X + 29.5, l2)):
                parts = lbl.split("|")
                for k, p in enumerate(parts):
                    c.drawString(PX(col_x), PY(y + 0.6 + k * 2.5), p)
            y += h + (2.5 if ("|" in l1 or "|" in l2) else 0.6)
            continue

        if kind == "wide":
            fn, label = entry[1], entry[2]
            fn(c, symx, PY(y + 0.8), mm(7.2), mm, INK)
            c.setFont(SERI, LEG_FS_ITEM)
            c.setFillColor(INK)
            c.drawString(PX(LEG_TXT_X), PY(y + 1.2), label)
            y += 5.4
            continue

        if kind == "pt":
            fn, abk, label = entry[1], entry[2], entry[3]
            fn(c, symx + symw * 0.72, PY(y - 0.8), mm, INK)
            c.setFont(SERCI, LEG_FS_ITEM - 0.6)
            c.setFillColor(INK)
            if abk:
                c.drawRightString(symx + symw * 0.45, PY(y), abk)
            c.setFont(SERI, LEG_FS_ITEM)
            c.drawString(txtx, PY(y), label)
            y += 3.42
            continue

    # ---- Abkürzungen ----  (gemeten blok 293,9..344,4)
    y = max(y + 3.0, 293.9)
    c.setFont(SERI, LEG_FS_CAT)
    c.drawString(PX(LEG_TXT_X), PY(y), "Abk\u00fcrzungen:")
    y += 3.4
    c.setFont(SERCI, 5.0)
    for a1, t1, a2, t2 in ABK:
        c.setFont(SERCI, 5.0)
        c.drawString(PX(LEG_ABK_X1), PY(y), a1)
        c.drawString(PX(LEG_ABK_X2), PY(y), a2)
        lines1 = t1.split("|")
        lines2 = t2.split("|")
        for k, ln in enumerate(lines1):
            c.drawString(PX(LEG_ABK_T1), PY(y + k * 2.3), ln)
        for k, ln in enumerate(lines2):
            c.drawString(PX(LEG_ABK_T2), PY(y + k * 2.3), ln)
        y += 2.62 + 2.3 * (max(len(lines1), len(lines2)) - 1)

    # ---------------------------------------------------- Gewässer ---------
    y = max(y + 3.2, 350.4)
    c.setFont(SERI, LEG_FS_CAT)
    c.drawString(PX(LEG_TXT_X), PY(y), "Gew\u00e4sser:")
    y += 2.6
    y = draw_gewasser(y)

    # ---------------------------------------------------- Höhenlinien ------
    y = max(y + 2.0, 406.7)
    c.setFont(SERI, LEG_FS_CAT)
    c.drawString(PX(LEG_TXT_X), PY(y), "H\u00f6henlinien:")
    y += 3.0
    y = draw_hoehenlinien(y)

    # ---------------------------------------------------- Planzeiger -------
    y = max(y + 3.0, 428.0)
    y = draw_planzeiger(y)
    c.restoreState()
    return y


def draw_gewasser(y):
    """Illustratief watervignet in de stijl van het origineel.
    Gemeten blok op het origineel: y 350,4 .. 400,1 (49,7 mm hoog)."""
    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    x0 = LEG_SYM_X
    top = y
    c.saveState()
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    LBL = SERCI

    # ---- hoofdstroom: brede rivier, links breed -> rechts smal ----
    c.setLineWidth(2.0)
    p = c.beginPath()
    p.moveTo(PX(x0 + 1), PY(top + 20.0))
    p.curveTo(PX(x0 + 16), PY(top + 21.5), PX(x0 + 30), PY(top + 17.5),
              PX(x0 + 46), PY(top + 19.5))
    c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(0.9)
    p = c.beginPath()
    p.moveTo(PX(x0 + 46), PY(top + 19.5))
    p.curveTo(PX(x0 + 60), PY(top + 21.0), PX(x0 + 70), PY(top + 26.0),
              PX(x0 + 80), PY(top + 30.0))
    c.drawPath(p, stroke=1, fill=0)
    c.setFont(LBL, 5.2)
    c.drawString(PX(x0 + 1), PY(top + 15.6), "Schiffbarer Flu\u00df")
    c.drawString(PX(x0 + 57), PY(top + 31.6), "Nicht schiffbarer Fl.")

    # ---- bovenrij: bron en bach ----
    c.setLineWidth(0.4)
    p = c.beginPath()
    p.moveTo(PX(x0 + 64), PY(top + 4.0))
    p.curveTo(PX(x0 + 56), PY(top + 6.0), PX(x0 + 50), PY(top + 9.0),
              PX(x0 + 44), PY(top + 12.5))
    c.drawPath(p, stroke=1, fill=0)
    c.circle(PX(x0 + 64.6), PY(top + 3.8), mm(0.6), stroke=1, fill=0)
    c.setFont(LBL, 5.2)
    c.drawString(PX(x0 + 66), PY(top + 4.4), "Quelle")
    c.drawString(PX(x0 + 49), PY(top + 7.4), "Bach")

    # ---- meer met eiland (links onder de rivier) ----
    c.setLineWidth(0.5)
    c.ellipse(PX(x0 + 20), PY(top + 34.0), PX(x0 + 38), PY(top + 26.0),
              stroke=1, fill=0)
    c.setFont(LBL, 5.2)
    c.drawString(PX(x0 + 27), PY(top + 29.4), "See")
    c.setLineWidth(0.35)
    c.ellipse(PX(x0 + 25), PY(top + 32.0), PX(x0 + 30), PY(top + 30.0),
              stroke=1, fill=0)
    c.setFont(LBL, 4.4)
    c.drawString(PX(x0 + 25.3), PY(top + 31.4), "Insel")

    # ---- kanaal + sluis (rechts) ----
    c.setLineWidth(0.7)
    c.line(PX(x0 + 50), PY(top + 24.0), PX(x0 + 66), PY(top + 21.0))
    c.setFont(LBL, 5.2)
    c.drawString(PX(x0 + 51), PY(top + 26.0), "Kanal")
    c.setLineWidth(0.6)
    c.line(PX(x0 + 63.5), PY(top + 22.6), PX(x0 + 63.5), PY(top + 20.4))
    c.drawString(PX(x0 + 65), PY(top + 19.4), "Schlse.")

    # ---- bruggen over de hoofdstroom ----
    def brug(xx, ytop, ybot, lw):
        c.setLineWidth(lw)
        c.line(PX(xx), PY(ytop), PX(xx), PY(ybot))

    brug(x0 + 9, top + 22.4, top + 18.0, 0.9)
    c.setFont(LBL, 4.8)
    c.drawString(PX(x0 + 2.0), PY(top + 25.0), "Holz-Br.")
    brug(x0 + 22, top + 22.6, top + 17.8, 1.3)
    c.drawString(PX(x0 + 19.5), PY(top + 25.2), "Steinbr\u00fccke")
    brug(x0 + 41, top + 22.4, top + 17.6, 1.3)
    c.drawString(PX(x0 + 37), PY(top + 25.0), "Eiserne Br.")

    # ---- wehr, furt, steg ----
    c.setLineWidth(0.45)
    for i in range(5):
        xx = x0 + 14.5 + i * 0.7
        c.line(PX(xx), PY(top + 22.2), PX(xx), PY(top + 18.2))
    c.setFont(LBL, 4.8)
    c.drawString(PX(x0 + 11.0), PY(top + 25.0), "Wehr")
    c.setLineWidth(0.3)
    c.line(PX(x0 + 31), PY(top + 21.8), PX(x0 + 31), PY(top + 18.4))
    c.drawString(PX(x0 + 28.5), PY(top + 16.4), "Steg")
    c.setLineWidth(0.35)
    for i in range(4):
        xx = x0 + 35 + i * 0.55
        c.line(PX(xx), PY(top + 21.6), PX(xx), PY(top + 18.6))
    c.drawString(PX(x0 + 33.5), PY(top + 24.0) if False else PY(top + 15.0), "Furt")

    # ---- schilf / nasse oever links onder ----
    c.setLineWidth(0.3)
    for i in range(6):
        xx = x0 + 2 + i * 1.4
        c.line(PX(xx), PY(top + 28.6), PX(xx), PY(top + 27.2))
        c.line(PX(xx - 0.45), PY(top + 28.6), PX(xx + 0.45), PY(top + 28.6))
    c.setFont(LBL, 4.8)
    c.drawString(PX(x0 + 2), PY(top + 31.0), "Schilf")

    # ---- stroom-onderloop met molen en stuw ----
    c.setLineWidth(0.4)
    c.line(PX(x0 + 8), PY(top + 36.0), PX(x0 + 18), PY(top + 39.5))
    c.setFont(LBL, 4.8)
    c.drawString(PX(x0 + 4), PY(top + 35.0), "Nasser Graben")
    c.setLineWidth(0.6)
    c.rect(PX(x0 + 44), PY(top + 38.0), mm(3.2), mm(2.4), stroke=1, fill=0)
    c.drawString(PX(x0 + 48), PY(top + 36.6), "Stauschleuse")
    c.setLineWidth(0.4)
    c.line(PX(x0 + 40), PY(top + 36.2), PX(x0 + 44), PY(top + 36.8))

    # ---- trockenes Flu\u00dfbett ----
    c.setLineWidth(0.3)
    seg = 1.2
    xx = x0 + 4
    while xx < x0 + 26:
        c.line(PX(xx), PY(top + 43.0), PX(xx + seg * 0.6), PY(top + 43.0))
        xx += seg
    c.setFont(LBL, 4.8)
    c.drawString(PX(x0 + 4), PY(top + 45.2), "Trockenes Flu\u00dfbett")

    c.restoreState()
    return top + 49.7


def draw_hoehenlinien(y):
    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    c.saveState()
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    x0 = LEG_SYM_X
    vals = [("15", "15 m"), ("12,5", "12,5 \u00b7"), ("10", "10 \u00b7"), ("7,5", "7,5 \u00b7"), ("5", "5 \u00b7")]
    for i, (v, lbl) in enumerate(vals):
        yy = y + i * 2.2
        c.setLineWidth(0.55 if i == 0 else 0.3)
        p = c.beginPath()
        p.moveTo(PX(x0), PY(yy))
        p.curveTo(PX(x0 + 12), PY(yy - 0.7), PX(x0 + 26), PY(yy + 0.7),
                  PX(x0 + 40), PY(yy))
        c.drawPath(p, stroke=1, fill=0)
        c.setFont(SERCI, 5.4)
        c.drawString(PX(x0 + 42), PY(yy + 0.6), lbl)
    yy = y + len(vals) * 2.2
    c.setFont(SERCI, 4.6)
    c.drawString(PX(x0 + 26), PY(yy - 2.0), "8,75")
    c.drawString(PX(x0 + 26), PY(yy - 0.2), "6,25")
    c.setFont(SERI, LEG_FS_ITEM - 0.4)
    c.drawString(PX(LEG_TXT_X - 2), PY(yy + 3.0), "Die H\u00f6hen sind in Metern \u00fcber Normal-Null")
    c.drawString(PX(LEG_TXT_X + 4), PY(yy + 5.4), "angegeben.")
    c.restoreState()
    return yy + 7.0


PLANZ_TEXT = [
    "Zum Ablesen ist die waagerechte Teilung so",
    "an eine waagerechte Gitterlinie zu legen, da\u00df",
    "die senkrechte Teilung den zu bezeichnenden",
    "Kartenpunkt ber\u00fchrt. Dann ist an der waage-",
    "rechten Teilung bei der n\u00e4chsten linken senk-",
    "rechten Gitterlinie der \u201eRechts\u201c-Wert, und an",
    "der senkrechten Teilung der \u201eHoch\u201c-Wert ab-",
    "zulesen.",
    "",
    "Der Rechtswert ist stets zuerst zu nennen.",
    "Die Punktangabe erfolgt in Metern. Nicht ab-",
    "lesbare Werte sind bis zur Angabe des vollen",
    "Meters durch Nullen zu ersetzen.",
]


def draw_planzeiger(y):
    def PX(v):
        return mm(v)

    def PY(v):
        return mm(PAPER_H - v)

    c.saveState()
    c.setFillColor(INK)
    c.setStrokeColor(INK)
    # kop in schreefloos, zoals op het origineel
    c.setFont("Helvetica", 11)
    c.drawString(PX(LEG_TXT_X + 2), PY(y), "P l a n z e i g e r .")
    y += 4.2
    c.setFont("Helvetica", 5.4)
    for ln in PLANZ_TEXT:
        if ln:
            c.drawString(PX(LEG_SYM_X), PY(y), ln)
        y += 2.35
    y += 1.0
    c.setFont("Helvetica-Oblique", 5.6)
    c.drawString(PX(LEG_SYM_X), PY(y), "Beispiel: Punkt p liegt in Metern:")
    y += 3.2
    c.setFont("Helvetica", 5.4)
    c.drawString(PX(LEG_SYM_X + 2), PY(y), "\u201eRechts\u201c  32 05000 + 200 = 32 05200 = (kurz:) 05200")
    y += 2.6
    c.drawString(PX(LEG_SYM_X + 2), PY(y), "\u201eHoch\u201c    57 89000 + 450 = 57 89450 = (kurz:) 89450")
    y += 3.4
    c.setFont("Helvetica-Oblique", 5.0)
    c.drawString(PX(LEG_SYM_X + 2), PY(y), "* Kennziffer des Meridianstreifens")
    # --- Planzeiger-instrument, op de gemeten maten van het origineel ---
    # De twee armen zijn elk exact 40,0 mm = 1 km op 1:25000, dus precies
    # één rastervierkant van de kaart. Op het origineel gemeten: 50 deel-
    # streepjes van 0,80 mm (= 20 m per streepje), met een cijfer om de
    # vijf streepjes (= 100 m).
    ARM = 40.0                 # armlengte in mm (1 km op 1:25000)
    NDIV = 50                  # aantal deelstreepjes per arm
    STEP = ARM / NDIV          # 0,80 mm
    ARM_W = 4.0                # breedte van de arm

    # gemeten hoekpunt van de L (binnenhoek, rechtsonder)
    CX = 609.45                # x van de binnenhoek
    CY = 530.70                # y van de binnenhoek

    c.setStrokeColor(INK)
    c.setFillColor(INK)

    # ---- verticale arm: loopt van de hoek 40 mm omhoog ----
    vx0, vx1 = CX, CX + ARM_W
    vy0, vy1 = CY - ARM, CY
    c.setLineWidth(0.45)
    c.rect(PX(vx0), PY(vy1), mm(ARM_W), mm(ARM), stroke=1, fill=0)
    c.setLineWidth(0.18)
    for i in range(1, NDIV):
        yy = CY - i * STEP
        long = (i % 5 == 0)
        c.line(PX(vx0), PY(yy), PX(vx0 + (ARM_W if long else ARM_W * 0.55)), PY(yy))
    c.setFont("Helvetica", 4.4)
    for k in range(1, 10):
        yy = CY - k * 5 * STEP
        c.drawRightString(PX(vx0) - mm(0.8), PY(yy) + mm(0.5), str(k))

    # ---- horizontale arm: loopt van de hoek 40 mm naar links ----
    hx0, hx1 = CX - ARM, CX
    hy0, hy1 = CY, CY + ARM_W
    c.setLineWidth(0.45)
    c.rect(PX(hx0), PY(hy1), mm(ARM), mm(ARM_W), stroke=1, fill=0)
    c.setLineWidth(0.18)
    for i in range(1, NDIV):
        xx = CX - i * STEP
        long = (i % 5 == 0)
        c.line(PX(xx), PY(hy0), PX(xx), PY(hy0 + (ARM_W if long else ARM_W * 0.55)))
    c.setFont("Helvetica", 4.4)
    for k in range(1, 10):
        xx = CX - k * 5 * STEP
        c.drawCentredString(PX(xx), PY(hy1) - mm(1.2), str(k))

    # ---- voorbeelddiagram linksboven (schematisch, gemeten posities) ----
    c.setLineWidth(0.4)
    # rastervierkant van het voorbeeld
    c.line(PX(575.41), PY(490.63), PX(600.00), PY(490.63))
    c.line(PX(575.41), PY(490.63), PX(575.41), PY(521.0))
    c.line(PX(575.41), PY(495.34), PX(600.00), PY(495.34))
    c.line(PX(600.00), PY(490.63), PX(600.00), PY(521.0))
    c.line(PX(575.41), PY(515.52), PX(600.00), PY(515.52))
    c.line(PX(586.43), PY(495.34), PX(586.43), PY(521.0))
    c.setFont("Helvetica", 5.6)
    c.drawString(PX(580.6), PY(494.4), "05")
    c.setFont("Helvetica", 3.8)
    c.drawString(PX(578.9), PY(493.9), "32")
    c.setFont("Helvetica", 5.6)
    c.drawString(PX(601.6), PY(494.4), "06")
    c.setFont("Helvetica", 5.6)
    c.drawRightString(PX(575.0), PY(514.8), "89")
    c.setFont("Helvetica", 3.8)
    c.drawRightString(PX(575.0) - pdfmetrics.stringWidth("89", "Helvetica", 5.6),
                      PY(514.8), "57")
    # deelschaal binnen het voorbeeld
    c.setLineWidth(0.15)
    for i in range(1, 10):
        yy = 515.52 - i * (515.52 - 496.0) / 10.0
        c.line(PX(583.89), PY(yy), PX(586.43), PY(yy))
        c.setFont("Helvetica", 3.4)
        c.drawRightString(PX(583.5), PY(yy) + mm(0.4), str(i))
    for i in range(1, 10):
        xx = 583.89 - i * (583.89 - 566.5) / 10.0
        c.line(PX(xx), PY(515.52), PX(xx), PY(517.4))
        c.setFont("Helvetica", 3.4)
        c.drawCentredString(PX(xx), PY(519.0), str(i))
    c.setFont("Helvetica", 4.6)
    c.drawString(PX(581.0), PY(507.5), "p")
    c.setFont("Helvetica", 3.8)
    c.drawString(PX(579.3), PY(511.5), "05")
    c.drawString(PX(579.3), PY(514.6), "20")

    y = CY + ARM_W + 6.0
    c.setFont("Helvetica", 8)
    c.drawString(PX(569.5), PY(y), "Planzeiger 1:25000")
    c.restoreState()
    return y + 3.0


MAP_IMAGE = "maparea.png"


def draw_placeholder():
    """Plaatst het kaartbeeld exact binnen de neat line."""
    import os
    if os.path.exists(MAP_IMAGE):
        c.drawImage(MAP_IMAGE, NX0, NY0, width=NX1 - NX0, height=NY1 - NY0,
                    preserveAspectRatio=False, anchor='sw', mask=None)
    else:
        c.saveState()
        c.setFillColor(Color(0.62, 0.62, 0.62, alpha=1))
        c.setFont(SERI, 12)
        c.drawCentredString((NX0 + NX1) / 2, (NY0 + NY1) / 2,
                            f"[ kaartvlak {MAP_W} \u00d7 {MAP_H} mm ]")
        c.restoreState()


draw_placeholder()
draw_frame()
draw_graduated_band()
draw_geo_labels()
draw_title()
draw_bottom_left()
draw_scalebar()
draw_copyright()
draw_ziehkante()
draw_greiferkante()
draw_adjacent_sheets()
draw_edge_heights()
draw_legend()
c.showPage()
c.save()
print(f"done  paper {PAPER_W} x {PAPER_H} mm   map {MAP_W} x {MAP_H} mm")
