#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tekent de terreindata uit terrain.json als een Meßtischblatt-kaartje.

Alles is vector: geen bitmap, dus scherp op elke vergroting en klein van
bestand. Het kader, de randverdeling en de typografie volgen de maten die
aan het origineel (Arnsberg Süd, 1894/1927) zijn opgemeten; de symbolen
komen uit mtb_symbols.py.

Dit is het kleine blad voor de game: een zestiende Meßtischblatt,
2,9 x 2,8 km, op 1:25 000 dus 116 x 112 mm kaartvlak.
"""
import json
import math
import os
import sys

import numpy as np
from skimage import measure
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import fontpad

import terrain_field as field

MM = 72.0 / 25.4


def mm(v):
    return v * MM


D = json.load(open("terrain.json"))
W_M = D["meta"]["width_m"]
H_M = D["meta"]["height_m"]
IV = D["meta"]["contour_interval_m"]
NAMES = D["meta"]["names"]
field.init(D["meta"]["seed"], W_M, H_M)

SCALE = 25000.0
MAP_W = W_M * 1000.0 / SCALE        # 116.0 mm
MAP_H = H_M * 1000.0 / SCALE        # 112.0 mm

# randopmaak: smaller dan het volle blad, maar dezelfde opbouw en maten
GRAD_BAND = 6.634
GAP_INNER = 0.911
HEAVY_W = 1.145
GAP_OUTER = 1.017
LW_THIN = 0.18
LW_HAIR = 0.30
OFF_INNER = GRAD_BAND
OFF_HEAVY_IN = GRAD_BAND + GAP_INNER
OFF_HEAVY_OUT = OFF_HEAVY_IN + HEAVY_W
OFF_OUTER = OFF_HEAVY_OUT + GAP_OUTER

MARGIN_L = 17.0
MARGIN_R = 17.0
MARGIN_T = 30.0
MARGIN_B = 36.0
PAPER_W = MARGIN_L + MAP_W + MARGIN_R
PAPER_H = MARGIN_T + MAP_H + MARGIN_B

SHEET_NAME = NAMES["village"]
SHEET_NR = "4312"
GRID_KM = 1.0                        # kilometerraster

INK = Color(0.13, 0.12, 0.10)
WATER = Color(0.33, 0.47, 0.52)
VEG = Color(0.40, 0.46, 0.30)
CONTOUR = Color(0.52, 0.38, 0.22)
ROADFILL = Color(0.78, 0.60, 0.34)

pdfmetrics.registerFont(TTFont("Didone", fontpad.pad("PlayfairDisplay[wght].ttf")))
SER, SERI, SERB = "Ser", "SerI", "SerB"
pdfmetrics.registerFont(TTFont(SER, fontpad.pad("DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont(SERI, fontpad.pad("DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont(SERB, fontpad.pad("DejaVuSerif-Bold.ttf")))

c = canvas.Canvas("messtischblatt_game.pdf", pagesize=(mm(PAPER_W), mm(PAPER_H)))

NX0 = mm(MARGIN_L)
NY0 = mm(MARGIN_B)
NX1 = mm(MARGIN_L + MAP_W)
NY1 = mm(MARGIN_B + MAP_H)


def X(xm):
    """meter -> PDF-x"""
    return NX0 + xm / W_M * (NX1 - NX0)


def Y(ym):
    """meter -> PDF-y (y loopt naar boven, net als in de data)"""
    return NY0 + ym / H_M * (NY1 - NY0)


def clip_map():
    p = c.beginPath()
    p.rect(NX0, NY0, NX1 - NX0, NY1 - NY0)
    c.clipPath(p, stroke=0, fill=0)


# =============================================================== vlakken ===
def poly_path(pts, close=True):
    p = c.beginPath()
    p.moveTo(X(pts[0][0]), Y(pts[0][1]))
    for x, y in pts[1:]:
        p.lineTo(X(x), Y(y))
    if close:
        p.close()
    return p


def fill_area(pts, rgb, alpha):
    c.saveState()
    c.setFillColor(Color(*rgb, alpha=alpha))
    c.drawPath(poly_path(pts), stroke=0, fill=1)
    c.restoreState()


def _inside(pts, x, y):
    n = len(pts)
    j = n - 1
    hit = False
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi:
            hit = not hit
        j = i
    return hit


def scatter_in(pts, step, fn, jitter=0.35, seed=0):
    """Strooit een symbool over een vlak, in een verspringend rooster."""
    import random
    r = random.Random(seed)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    y = min(ys)
    row = 0
    while y <= max(ys):
        off = (step * 0.5) if row % 2 else 0.0
        x = min(xs) + off
        while x <= max(xs):
            jx = x + r.uniform(-jitter, jitter) * step
            jy = y + r.uniform(-jitter, jitter) * step
            if _inside(pts, jx, jy):
                fn(jx, jy, r)
            x += step
        y += step * 0.86
        row += 1


def sym_conifer(xm, ym, r):
    s = mm(0.62)
    x, y = X(xm), Y(ym)
    c.setLineWidth(0.26)
    c.line(x, y - s * 0.7, x, y + s * 0.9)
    c.line(x - s * 0.62, y - s * 0.1, x, y + s * 0.9)
    c.line(x + s * 0.62, y - s * 0.1, x, y + s * 0.9)


def sym_decid(xm, ym, r):
    x, y = X(xm), Y(ym)
    c.setLineWidth(0.26)
    c.circle(x, y, mm(0.52), stroke=1, fill=0)


def sym_marsh(xm, ym, r):
    x, y = X(xm), Y(ym)
    c.setLineWidth(0.24)
    w = mm(1.1)
    c.line(x - w, y, x + w, y)
    c.line(x - w * 0.5, y + mm(0.45), x + w * 0.5, y + mm(0.45))


def sym_meadow(xm, ym, r):
    x, y = X(xm), Y(ym)
    c.setLineWidth(0.22)
    c.line(x - mm(0.5), y, x + mm(0.5), y)
    c.line(x, y - mm(0.35), x, y + mm(0.35))


def sym_heath(xm, ym, r):
    x, y = X(xm), Y(ym)
    c.setLineWidth(0.24)
    c.line(x, y - mm(0.3), x, y + mm(0.5))
    c.line(x - mm(0.3), y + mm(0.1), x, y + mm(0.5))
    c.line(x + mm(0.3), y + mm(0.1), x, y + mm(0.5))


AREA_STYLE = {
    "nadelwald": ((0.62, 0.70, 0.56), 0.42, 46, sym_conifer),
    "laubwald": ((0.64, 0.72, 0.55), 0.42, 46, sym_decid),
    "mischwald": ((0.63, 0.71, 0.56), 0.42, 46, sym_conifer),
    "bruch": ((0.70, 0.76, 0.72), 0.34, 52, sym_marsh),
    "wiese": ((0.78, 0.81, 0.66), 0.30, 58, sym_meadow),
    "heide": ((0.80, 0.77, 0.63), 0.30, 56, sym_heath),
}


def draw_areas():
    c.saveState()
    clip_map()
    for a in D["areas"]:
        rgb, alpha, step, sym = AREA_STYLE[a["kind"]]
        fill_area(a["poly"], rgb, alpha)
        c.setStrokeColor(Color(*VEG.rgb(), alpha=0.75))
        c.setLineWidth(0.3)
        c.drawPath(poly_path(a["poly"]), stroke=1, fill=0)
        c.setStrokeColor(Color(*VEG.rgb(), alpha=0.95))
        scatter_in(a["poly"], step, sym, seed=hash(a["kind"]) & 0xFFFF)
    c.restoreState()


# ========================================================== hoogtelijnen ===
def draw_contours():
    n = 420
    xs = np.linspace(0, W_M, n)
    ys = np.linspace(0, H_M, n)
    Z = np.empty((n, n))
    for j, yy in enumerate(ys):
        for i, xx in enumerate(xs):
            Z[j, i] = field.elevation(xx, yy)
    lo, hi = Z.min(), Z.max()
    c.saveState()
    clip_map()
    c.setStrokeColor(CONTOUR)
    lev = math.ceil(lo / IV) * IV
    idx = 0
    while lev < hi:
        for seg in measure.find_contours(Z, lev):
            if len(seg) < 6:
                continue
            thick = (round(lev / IV) % 4 == 0)
            c.setLineWidth(0.42 if thick else 0.2)
            p = c.beginPath()
            x0 = seg[0][1] / (n - 1) * W_M
            y0 = seg[0][0] / (n - 1) * H_M
            p.moveTo(X(x0), Y(y0))
            for yy, xx in seg[1:]:
                p.lineTo(X(xx / (n - 1) * W_M), Y(yy / (n - 1) * H_M))
            c.drawPath(p, stroke=1, fill=0)
        lev += IV
        idx += 1
    c.restoreState()
    return lo, hi


# ================================================================ water ====
def draw_stream():
    c.saveState()
    clip_map()
    path = D["stream"]["path"]
    c.setStrokeColor(WATER)
    c.setLineWidth(1.05)
    c.setLineCap(1)
    p = c.beginPath()
    p.moveTo(X(path[0][0]), Y(path[0][1]))
    for x, y in path[1:]:
        p.lineTo(X(x), Y(y))
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


# ================================================================ wegen ====
ROAD_W = {"IIA": (1.55, 0.42), "III": (0.95, 0.30), "track": (0.0, 0.26)}


def draw_roads():
    c.saveState()
    clip_map()
    for r in D["roads"]:
        pts = r["path"]
        body, edge = ROAD_W[r["cls"]]
        p = c.beginPath()
        p.moveTo(X(pts[0][0]), Y(pts[0][1]))
        for x, y in pts[1:]:
            p.lineTo(X(x), Y(y))
        c.setLineCap(1)
        c.setLineJoin(1)
        if body > 0:
            c.setStrokeColor(ROADFILL)
            c.setLineWidth(body)
            c.drawPath(p, stroke=1, fill=0)
            c.setStrokeColor(INK)
            c.setLineWidth(edge)
            c.setDash()
            c.drawPath(p, stroke=1, fill=0)
        else:
            c.setStrokeColor(INK)
            c.setLineWidth(edge)
            c.setDash(1.4, 1.2)
            c.drawPath(p, stroke=1, fill=0)
            c.setDash()
    c.restoreState()


# =========================================================== bebouwing =====
def draw_buildings():
    c.saveState()
    clip_map()
    c.setFillColor(INK)
    c.setStrokeColor(INK)
    for grp in (D["buildings"], D["hamlet_buildings"]):
        for b in grp:
            c.saveState()
            c.translate(X(b["x"]), Y(b["y"]))
            c.rotate(b["rot"])
            w = b["w"] / W_M * (NX1 - NX0)
            h = b["h"] / H_M * (NY1 - NY0)
            c.rect(-w / 2, -h / 2, w, h, stroke=0, fill=1)
            c.restoreState()

    # begraafplaats
    c.setFillColor(Color(1, 1, 1))
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    c.drawPath(poly_path(D["cemetery"]), stroke=1, fill=1)
    cx = sum(p[0] for p in D["cemetery"]) / len(D["cemetery"])
    cy = sum(p[1] for p in D["cemetery"]) / len(D["cemetery"])
    for dx, dy in ((-18, 8), (6, -6), (20, 10)):
        x, y = X(cx + dx), Y(cy + dy)
        c.line(x, y - mm(0.4), x, y + mm(0.5))
        c.line(x - mm(0.25), y + mm(0.18), x + mm(0.25), y + mm(0.18))

    # kerk met toren
    ch = D["church"]
    x, y = X(ch["x"]), Y(ch["y"])
    c.setFillColor(Color(1, 1, 1))
    c.setLineWidth(0.4)
    c.circle(x, y, mm(0.8), stroke=1, fill=1)
    c.setFillColor(INK)
    c.circle(x, y, mm(0.3), stroke=0, fill=1)
    c.line(x, y + mm(0.8), x, y + mm(2.0))
    c.line(x - mm(0.45), y + mm(1.6), x + mm(0.45), y + mm(1.6))

    # windmolen
    wm = D["windmill"]
    x, y = X(wm["x"]), Y(wm["y"])
    c.setLineWidth(0.34)
    d = mm(0.95)
    c.line(x - d, y - d, x + d, y + d)
    c.line(x - d, y + d, x + d, y - d)
    c.line(x, y - d, x, y - mm(1.7))
    c.restoreState()


# ============================================================== punten =====
def draw_points():
    c.saveState()
    clip_map()
    c.setFillColor(INK)
    c.setStrokeColor(INK)
    for s in D["spot_heights"]:
        x, y = X(s["x"]), Y(s["y"])
        c.circle(x, y, mm(0.17), stroke=0, fill=1)
        c.setFont(SERI, 3.6)
        c.drawString(x + mm(0.6), y - mm(0.5), f"{s['h']:.1f}".replace(".", ","))
    for t in D["trig"]:
        x, y = X(t["x"]), Y(t["y"])
        c.setLineWidth(0.34)
        d = mm(0.78)
        p = c.beginPath()
        p.moveTo(x, y + d)
        p.lineTo(x - d * 0.87, y - d * 0.5)
        p.lineTo(x + d * 0.87, y - d * 0.5)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.circle(x, y, mm(0.14), stroke=0, fill=1)
        c.setFont(SERI, 3.8)
        c.drawString(x + mm(1.1), y - mm(0.4), f"{t['h']:.1f}".replace(".", ","))
    c.restoreState()


# ============================================================== namen ======
def _spaced(txt, x, y, font, size, extra=1.1, centre=True):
    total = sum(pdfmetrics.stringWidth(ch, font, size) + extra for ch in txt) - extra
    cx = x - total / 2 if centre else x
    c.setFont(font, size)
    for ch in txt:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + extra


def draw_labels():
    c.saveState()
    clip_map()
    c.setFillColor(INK)
    for L in D["labels"]:
        if L["kind"] == "village":
            _spaced(L["text"].upper(), X(L["x"]), Y(L["y"]), SERB, 7.0, 1.5)
        elif L["kind"] == "hamlet":
            _spaced(L["text"], X(L["x"]), Y(L["y"]), SER, 5.0, 0.8)
        else:
            c.saveState()
            c.setFillColor(Color(*VEG.rgb(), alpha=0.95))
            c.translate(X(L["x"]), Y(L["y"]))
            c.rotate(-11)
            _spaced(L["text"], 0, 0, SERI, 5.4, 1.2)
            c.restoreState()
    # beeknaam, schuin langs de loop
    st = D["stream"]["path"]
    k = int(len(st) * 0.33)
    x0, y0 = st[k]
    x1, y1 = st[min(k + 4, len(st) - 1)]
    c.saveState()
    c.setFillColor(WATER)
    c.translate(X(x0), Y(y0) + mm(1.0))
    c.rotate(math.degrees(math.atan2(Y(y1) - Y(y0), X(x1) - X(x0))))
    _spaced(NAMES["stream"], 0, 0, SERI, 4.6, 0.9, centre=False)
    c.restoreState()
    c.restoreState()


# =============================================================== kader =====
def rect_out(off, lw):
    o = mm(off)
    c.setLineWidth(lw)
    c.rect(NX0 - o, NY0 - o, (NX1 - NX0) + 2 * o, (NY1 - NY0) + 2 * o,
           stroke=1, fill=0)


def draw_frame():
    c.saveState()
    c.setStrokeColor(INK)
    rect_out(0, LW_THIN)
    rect_out(OFF_INNER, LW_THIN)
    rect_out((OFF_HEAVY_IN + OFF_HEAVY_OUT) / 2.0, mm(HEAVY_W))
    rect_out(OFF_OUTER, LW_HAIR)
    c.restoreState()


def draw_grid_band():
    """Kilometerraster: streepjes in de band plus kruisjes in het kaartvlak."""
    c.saveState()
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    b = mm(GRAD_BAND)
    nx = int(W_M // (GRID_KM * 1000))
    ny = int(H_M // (GRID_KM * 1000))
    c.setLineWidth(LW_THIN)
    for i in range(1, nx + 1):
        x = X(i * GRID_KM * 1000)
        c.line(x, NY1, x, NY1 + b)
        c.line(x, NY0, x, NY0 - b)
        c.setFont(SER, 6.2)
        c.drawString(x + mm(0.8), NY1 + mm(2.1), str(10 + i))
        c.drawString(x + mm(0.8), NY0 - mm(4.4), str(10 + i))
    for j in range(1, ny + 1):
        y = Y(j * GRID_KM * 1000)
        c.line(NX0, y, NX0 - b, y)
        c.line(NX1, y, NX1 + b, y)
        c.setFont(SER, 6.2)
        c.drawRightString(NX0 - mm(1.2), y + mm(1.0), str(40 + j))
        c.drawString(NX1 + mm(1.2), y + mm(1.0), str(40 + j))
    # rasterkruisjes
    c.saveState()
    clip_map()
    c.setLineWidth(0.26)
    for i in range(1, nx + 1):
        for j in range(1, ny + 1):
            x, y = X(i * GRID_KM * 1000), Y(j * GRID_KM * 1000)
            c.line(x - mm(0.8), y, x + mm(0.8), y)
            c.line(x, y - mm(0.8), x, y + mm(0.8))
    c.restoreState()
    c.restoreState()


def draw_title():
    c.saveState()
    c.setFillColor(INK)
    cx = (NX0 + NX1) / 2
    c.setFont("Didone", 15)
    for dx in (0, 0.25):
        c.drawCentredString(cx + dx, mm(PAPER_H - 13.0), f"{SHEET_NAME}.")
    c.setFont(SERI, 5.4)
    c.drawCentredString(cx, mm(PAPER_H - 18.2), "Truppenkarte  ·  Ostfront")
    c.setFont(SER, 6.0)
    c.drawRightString(NX1, mm(PAPER_H - 13.0), f"Blatt {SHEET_NR}")
    c.setFont(SERI, 5.2)
    c.drawString(NX0, mm(PAPER_H - 13.0), "Nur für den Dienstgebrauch")
    c.restoreState()


def draw_scalebar():
    c.saveState()
    c.setFillColor(INK)
    c.setStrokeColor(INK)
    cx = (NX0 + NX1) / 2
    ytxt = mm(21.5)
    c.setFont(SER, 6.4)
    c.drawCentredString(cx, ytxt, "1:25 000   (4 cm der Karte = 1 km der Natur)")
    total_m = 2000.0
    L = mm(total_m / 1000.0 * 40.0)
    x0 = cx - L / 2
    ybar = ytxt - mm(5.0)
    h = mm(1.3)
    c.setLineWidth(0.3)
    c.rect(x0, ybar, L, h, stroke=1, fill=0)
    seg = L / 4
    for i in range(4):
        if i % 2 == 0:
            c.rect(x0 + i * seg, ybar, seg, h, stroke=0, fill=1)
    c.setFont(SERI, 4.6)
    for i, lab in enumerate(("0", "500", "1000", "1500", "2000")):
        c.drawCentredString(x0 + i * seg, ybar - mm(2.6), lab)
    c.drawString(x0 + L + mm(1.4), ybar - mm(0.2), "Meter")
    c.restoreState()


def draw_credit():
    c.saveState()
    c.setFillColor(Color(0.35, 0.34, 0.30))
    c.setFont(SERI, 4.0)
    c.drawCentredString((NX0 + NX1) / 2, mm(3.4),
                        f"Fiktives Gelände · Seed {D['meta']['seed']} · "
                        f"{W_M/1000:.1f} × {H_M/1000:.1f} km")
    c.restoreState()


# ================================================================= run =====
c.setFillColor(Color(0.955, 0.945, 0.905))
c.rect(0, 0, mm(PAPER_W), mm(PAPER_H), stroke=0, fill=1)

draw_areas()
lo, hi = draw_contours()
draw_stream()
draw_roads()
draw_buildings()
draw_points()
draw_labels()
draw_grid_band()
draw_frame()
draw_title()
draw_scalebar()
draw_credit()
c.showPage()
c.save()

print(f"blad {PAPER_W:.0f} x {PAPER_H:.0f} mm, kaartvlak {MAP_W:.0f} x {MAP_H:.0f} mm")
print(f"terrein {W_M/1000:.1f} x {H_M/1000:.1f} km, hoogte {lo:.1f}..{hi:.1f} m")
print("geschreven: messtischblatt_game.pdf")
