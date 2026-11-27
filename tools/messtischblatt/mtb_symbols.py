# -*- coding: utf-8 -*-
"""
Symboolbibliotheek voor het Meßtischblatt-sjabloon.
Alle symbolen zijn natekeningen in de stijl van het origineel (Arnsberg Süd
1894/1927), programmatisch opgebouwd zodat ze schaalbaar en schoon blijven.

Elke tekenfunctie krijgt (c, x, y, w, mm, INK) waarbij:
  x,y = linkerkant / hartlijn van het symboolvak (PDF-punten)
  w   = beschikbare breedte (PDF-punten)
"""


def _dash(c, x, y, w, pattern, lw=0.45):
    """pattern: lijst van (aan, uit) in mm-fracties van w."""
    c.setLineWidth(lw)
    pos = 0.0
    total = sum(a + b for a, b in pattern)
    n = int(w / (total + 0.001)) + 2
    xx = x
    for _ in range(n):
        for on, off in pattern:
            if xx >= x + w:
                break
            x2 = min(xx + on, x + w)
            c.line(xx, y, x2, y)
            xx = x2 + off
    return


# ------------------------------------------------------------- GRENZEN -----
def sym_reichsgrenze(c, x, y, w, mm, INK):
    """Zware streep-blok grens met dwarsstreepjes."""
    c.setStrokeColor(INK)
    seg = w / 6.0
    for i in range(6):
        x0 = x + i * seg
        c.setLineWidth(1.5)
        c.line(x0 + seg * 0.12, y, x0 + seg * 0.78, y)
        c.setLineWidth(0.5)
        c.line(x0 + seg * 0.06, y - mm(0.55), x0 + seg * 0.06, y + mm(0.55))
        c.line(x0 + seg * 0.84, y - mm(0.55), x0 + seg * 0.84, y + mm(0.55))


def sym_provinzgrenze(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    seg = w / 5.0
    for i in range(5):
        x0 = x + i * seg
        c.setLineWidth(1.3)
        c.line(x0 + seg * 0.30, y, x0 + seg * 0.80, y)
        c.setLineWidth(0.4)
        c.circle(x0 + seg * 0.12, y, mm(0.35), stroke=1, fill=0)


def sym_kreisgrenze(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    seg = w / 4.0
    for i in range(4):
        x0 = x + i * seg
        c.setLineWidth(0.9)
        c.line(x0, y, x0 + seg * 0.55, y)
        c.circle(x0 + seg * 0.78, y, mm(0.22), stroke=0, fill=1)


def sym_gemeindegrenze(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    seg = w / 4.0
    for i in range(4):
        x0 = x + i * seg
        c.setLineWidth(0.5)
        c.line(x0, y, x0 + seg * 0.50, y)
        c.circle(x0 + seg * 0.72, y, mm(0.16), stroke=0, fill=1)


# --------------------------------------------------------- EISENBAHNEN -----
def _rail(c, x, y, w, mm, INK, lw, ties, tie_h):
    c.setStrokeColor(INK)
    c.setLineWidth(lw)
    c.line(x, y, x + w, y)
    c.setLineWidth(0.4)
    step = w / ties
    for i in range(ties + 1):
        xx = x + i * step
        c.line(xx, y - mm(tie_h), xx, y + mm(tie_h))


def sym_bahn_mehrgleisig(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(1.9)
    c.line(x, y, x + w, y)
    c.setStrokeColor(INK)
    c.setLineWidth(0.45)
    step = w / 5.0
    for i in range(5):
        c.line(x + i * step + step * 0.35, y - mm(0.62),
               x + i * step + step * 0.35, y + mm(0.62))
    c.setLineWidth(0.5)
    c.line(x, y - mm(0.62), x + w, y - mm(0.62))
    c.line(x, y + mm(0.62), x + w, y + mm(0.62))


def sym_bahn_eingleisig(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(x, y - mm(0.6), x + w, y - mm(0.6))
    c.line(x, y + mm(0.6), x + w, y + mm(0.6))
    step = w / 5.0
    for i in range(6):
        c.line(x + i * step, y - mm(0.6), x + i * step, y + mm(0.6))


def sym_kleinbahn(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.45)
    c.line(x, y - mm(0.45), x + w, y - mm(0.45))
    c.line(x, y + mm(0.45), x + w, y + mm(0.45))
    step = w / 4.0
    for i in range(5):
        c.line(x + i * step, y - mm(0.45), x + i * step, y + mm(0.45))


def sym_schmalspur(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.4)
    c.line(x, y - mm(0.32), x + w, y - mm(0.32))
    c.line(x, y + mm(0.32), x + w, y + mm(0.32))
    step = w / 3.0
    for i in range(4):
        c.line(x + i * step, y - mm(0.32), x + i * step, y + mm(0.32))


def sym_schmalspur_klein(c, x, y, w, mm, INK):
    sym_schmalspur(c, x, y, w, mm, INK)
    c.setLineWidth(0.3)
    c.line(x, y, x + w, y)


def sym_wirtschaftsbahn(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.45)
    seg = w / 8.0
    for i in range(8):
        if i % 2 == 0:
            c.line(x + i * seg, y, x + (i + 1) * seg, y)
    for i in (1, 4, 7):
        c.line(x + i * seg, y - mm(0.4), x + i * seg, y + mm(0.4))


def sym_seilbahn(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(0.45)
    c.line(x, y, x + w, y)
    for f in (0.08, 0.5, 0.92):
        cx = x + w * f
        d = mm(0.55)
        p = c.beginPath()
        p.moveTo(cx - d, y)
        p.lineTo(cx, y + d)
        p.lineTo(cx + d, y)
        p.lineTo(cx, y - d)
        p.close()
        c.drawPath(p, stroke=1, fill=0)


# ------------------------------------------------------------- STRASSEN ----
def sym_kraftfahrbahn(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.55)
    for dy in (-0.75, -0.25, 0.25, 0.75):
        c.line(x, y + mm(dy), x + w, y + mm(dy))


def sym_reichsstrasse(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(x, y - mm(0.5), x + w, y - mm(0.5))
    c.line(x, y + mm(0.5), x + w, y + mm(0.5))


def sym_strasse_IA(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.45)
    c.line(x, y - mm(0.42), x + w, y - mm(0.42))
    c.line(x, y + mm(0.42), x + w, y + mm(0.42))


def sym_strasse_IB(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    c.line(x, y - mm(0.35), x + w, y - mm(0.35))
    c.line(x, y + mm(0.35), x + w, y + mm(0.35))


def sym_weg_IIA(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    c.line(x, y + mm(0.28), x + w, y + mm(0.28))
    seg = w / 9.0
    for i in range(9):
        if i % 2 == 0:
            c.line(x + i * seg, y - mm(0.28), x + (i + 1) * seg, y - mm(0.28))


def sym_weg_IIB(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    seg = w / 9.0
    for i in range(9):
        if i % 2 == 0:
            c.line(x + i * seg, y + mm(0.24), x + (i + 1) * seg, y + mm(0.24))
            c.line(x + i * seg, y - mm(0.24), x + (i + 1) * seg, y - mm(0.24))


def sym_feldweg(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    seg = w / 7.0
    for i in range(7):
        if i % 2 == 0:
            c.line(x + i * seg, y, x + (i + 0.75) * seg, y)


def sym_fussweg(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    seg = w / 12.0
    for i in range(12):
        if i % 2 == 0:
            c.line(x + i * seg, y, x + (i + 0.6) * seg, y)


# ------------------------------------------------- BODENBEDECKING (vlak) ---
def _blob(c, x, y, w, h, mm, INK):
    """Onregelmatig 'wolkje' zoals de vlaksymbolen op het origineel."""
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    p = c.beginPath()
    p.moveTo(x + w * 0.10, y - h * 0.35)
    p.curveTo(x - w * 0.02, y + h * 0.05, x + w * 0.18, y + h * 0.52, x + w * 0.42, y + h * 0.40)
    p.curveTo(x + w * 0.62, y + h * 0.58, x + w * 0.96, y + h * 0.30, x + w * 0.90, y - h * 0.05)
    p.curveTo(x + w * 1.02, y - h * 0.40, x + w * 0.70, y - h * 0.58, x + w * 0.45, y - h * 0.46)
    p.curveTo(x + w * 0.26, y - h * 0.60, x + w * 0.06, y - h * 0.58, x + w * 0.10, y - h * 0.35)
    c.drawPath(p, stroke=1, fill=0)


def _laub(c, cx, cy, mm, INK):
    c.setLineWidth(0.3)
    c.circle(cx, cy, mm(0.42), stroke=1, fill=0)


def _nadel(c, cx, cy, mm, INK):
    c.setLineWidth(0.3)
    c.line(cx, cy - mm(0.45), cx, cy + mm(0.55))
    c.line(cx - mm(0.38), cy - mm(0.05), cx, cy + mm(0.55))
    c.line(cx + mm(0.38), cy - mm(0.05), cx, cy + mm(0.55))


def sym_laubwald(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    for dx, dy in [(0.28, 0.18), (0.55, -0.10), (0.36, -0.30), (0.70, 0.24)]:
        _laub(c, x + w * dx, y + h * dy, mm, INK)


def sym_nadelwald(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    for dx, dy in [(0.26, 0.14), (0.52, -0.14), (0.72, 0.20), (0.40, -0.34)]:
        _nadel(c, x + w * dx, y + h * dy, mm, INK)


def sym_mischwald(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    _laub(c, x + w * 0.28, y + h * 0.16, mm, INK)
    _laub(c, x + w * 0.36, y - h * 0.30, mm, INK)
    _nadel(c, x + w * 0.60, y - h * 0.06, mm, INK)
    _nadel(c, x + w * 0.76, y + h * 0.22, mm, INK)


def sym_buschwerk(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    c.setFillColor(INK)
    for dx, dy in [(0.26, 0.10), (0.46, -0.22), (0.66, 0.16), (0.80, -0.10)]:
        c.circle(x + w * dx, y + h * dy, mm(0.22), stroke=0, fill=1)
    _nadel(c, x + w * 0.56, y + h * 0.30, mm, INK)


def sym_heide(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    c.setLineWidth(0.28)
    for dx in (0.26, 0.44, 0.62, 0.78):
        bx = x + w * dx
        by = y - h * 0.18
        c.line(bx, by, bx, by + mm(0.7))
        c.line(bx - mm(0.28), by + mm(0.28), bx, by + mm(0.7))
        c.line(bx + mm(0.28), by + mm(0.28), bx, by + mm(0.7))


def sym_sand(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setFillColor(INK)
    import random
    rnd = random.Random(7)
    for _ in range(46):
        px = x + w * rnd.uniform(0.06, 0.94)
        py = y + h * rnd.uniform(-0.45, 0.45)
        c.circle(px, py, mm(0.13), stroke=0, fill=1)


def sym_wiese(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    c.setLineWidth(0.26)
    for dy in (-0.28, 0.02, 0.30):
        for dx in (0.24, 0.46, 0.68):
            bx = x + w * dx
            by = y + h * dy
            c.line(bx - mm(0.5), by, bx + mm(0.5), by)


def sym_bruch(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    c.setLineWidth(0.26)
    for dy in (-0.26, 0.06, 0.32):
        c.line(x + w * 0.20, y + h * dy, x + w * 0.80, y + h * dy)
    for dx in (0.34, 0.58):
        c.line(x + w * dx, y - h * 0.42, x + w * dx, y + h * 0.42)


def sym_weingarten(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    c.rect(x + w * 0.06, y - h * 0.45, w * 0.88, h * 0.9, stroke=1, fill=0)
    for i in range(6):
        xx = x + w * (0.14 + i * 0.13)
        c.line(xx, y - h * 0.36, xx, y + h * 0.36)


def sym_hopfen(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    for r in range(3):
        for col in range(5):
            cx = x + w * (0.14 + col * 0.18)
            cy = y + h * (-0.32 + r * 0.32)
            d = mm(0.30)
            c.line(cx - d, cy - d, cx + d, cy + d)
            c.line(cx - d, cy + d, cx + d, cy - d)


def sym_park(c, x, y, w, mm, INK):
    h = mm(3.2)
    _blob(c, x, y, w, h, mm, INK)
    _laub(c, x + w * 0.30, y + h * 0.20, mm, INK)
    _laub(c, x + w * 0.62, y - h * 0.22, mm, INK)
    c.setLineWidth(0.24)
    c.line(x + w * 0.14, y - h * 0.36, x + w * 0.86, y + h * 0.34)


def sym_baumschule(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    c.rect(x + w * 0.06, y - h * 0.45, w * 0.88, h * 0.9, stroke=1, fill=0)
    for col in range(4):
        cx = x + w * (0.18 + col * 0.21)
        _laub(c, cx, y + h * 0.20, mm, INK)
        _nadel(c, cx, y - h * 0.24, mm, INK)


def sym_friedhof(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.rect(x + w * 0.10, y - h * 0.45, w * 0.80, h * 0.9, stroke=1, fill=0)
    for col in range(3):
        for r in range(2):
            cx = x + w * (0.24 + col * 0.24)
            cy = y + h * (-0.22 + r * 0.42)
            c.line(cx, cy - mm(0.30), cx, cy + mm(0.30))
            c.line(cx - mm(0.18), cy + mm(0.12), cx + mm(0.18), cy + mm(0.12))
    c.setFillColor(INK)
    c.circle(x + w * 0.50, y, mm(0.28), stroke=0, fill=1)


def sym_bruchfeld(c, x, y, w, mm, INK):
    h = mm(3.2)
    c.setStrokeColor(INK)
    c.setLineWidth(0.45)
    for i in range(7):
        xx = x + w * (0.10 + i * 0.13)
        c.line(xx, y - h * 0.42, xx, y + h * 0.42)


# ------------------------------------------------------ LIJN-OBJECTEN ------
def sym_damm(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.5)
    c.line(x, y, x + w, y)
    c.setLineWidth(0.28)
    n = 16
    for i in range(n):
        xx = x + w * i / n
        c.line(xx, y, xx, y - mm(0.55))


def sym_drahtzaun(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.line(x, y, x + w, y)
    for i in range(7):
        xx = x + w * (0.05 + i * 0.15)
        c.line(xx, y - mm(0.45), xx, y + mm(0.45))
        c.line(xx - mm(0.25), y - mm(0.25), xx + mm(0.25), y + mm(0.25))


def sym_fels(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    import random
    rnd = random.Random(3)
    for i in range(22):
        xx = x + w * rnd.uniform(0.02, 0.98)
        yy = y + mm(rnd.uniform(-0.5, 0.5))
        c.line(xx, yy, xx + mm(rnd.uniform(0.2, 0.6)), yy + mm(rnd.uniform(-0.4, 0.4)))


def sym_hecke(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    n = 9
    for i in range(n):
        cx = x + w * (i + 0.5) / n
        c.circle(cx, y, mm(0.30), stroke=1, fill=0)


def sym_knick(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    c.line(x, y - mm(0.25), x + w, y - mm(0.25))
    n = 8
    for i in range(n):
        cx = x + w * (i + 0.5) / n
        c.circle(cx, y + mm(0.28), mm(0.24), stroke=1, fill=0)


def sym_mauer(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.85)
    c.line(x, y, x + w, y)


def sym_trockengraben(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.line(x, y + mm(0.22), x + w, y + mm(0.22))
    c.line(x, y - mm(0.22), x + w, y - mm(0.22))


def sym_wall(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.4)
    c.line(x, y, x + w, y)
    c.setLineWidth(0.25)
    n = 14
    for i in range(n):
        xx = x + w * i / n
        c.line(xx, y, xx + mm(0.18), y + mm(0.42))


def sym_zaun(c, x, y, w, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(0.28)
    c.line(x, y, x + w, y)
    n = 10
    for i in range(n):
        xx = x + w * (i + 0.5) / n
        c.circle(xx, y, mm(0.16), stroke=0, fill=1)


# -------------------------------------------------------- PUNTSYMBOLEN -----
def pt_kirche_turm(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.setLineWidth(0.35)
    c.circle(cx, cy, mm(0.42), stroke=1, fill=0)
    c.line(cx, cy + mm(0.42), cx, cy + mm(1.25))
    c.line(cx - mm(0.28), cy + mm(0.95), cx + mm(0.28), cy + mm(0.95))


def pt_kirche_ohne(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    c.circle(cx, cy, mm(0.42), stroke=1, fill=0)


def pt_kapelle(c, cx, cy, mm, INK):
    c.setFillColor(INK)
    c.circle(cx, cy, mm(0.34), stroke=0, fill=1)


def pt_trig(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    d = mm(0.62)
    p = c.beginPath()
    p.moveTo(cx, cy + d)
    p.lineTo(cx - d, cy - d * 0.7)
    p.lineTo(cx + d, cy - d * 0.7)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def pt_turm(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.circle(cx, cy, mm(0.20), stroke=0, fill=1)
    c.setLineWidth(0.3)
    c.circle(cx, cy, mm(0.55), stroke=1, fill=0)


def pt_windmuehle(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    d = mm(0.62)
    c.line(cx - d, cy - d, cx + d, cy + d)
    c.line(cx - d, cy + d, cx + d, cy - d)
    c.line(cx, cy - d, cx, cy - mm(1.0))


def pt_windmotor(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    c.line(cx, cy - mm(0.7), cx, cy + mm(0.7))
    c.line(cx - mm(0.45), cy + mm(0.35), cx + mm(0.45), cy + mm(0.35))
    c.line(cx - mm(0.30), cy - mm(0.7), cx + mm(0.30), cy - mm(0.7))


def pt_wassermuehle(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    d = mm(0.55)
    c.line(cx - d, cy, cx + d, cy)
    c.line(cx, cy - d, cx, cy + d)
    c.line(cx - d * 0.7, cy - d * 0.7, cx + d * 0.7, cy + d * 0.7)
    c.line(cx - d * 0.7, cy + d * 0.7, cx + d * 0.7, cy - d * 0.7)


def pt_denkmal(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.rect(cx - mm(0.22), cy - mm(0.5), mm(0.44), mm(1.0), stroke=0, fill=1)


def pt_einzelgrab(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    c.line(cx, cy - mm(0.5), cx, cy + mm(0.62))
    c.line(cx - mm(0.32), cy + mm(0.28), cx + mm(0.32), cy + mm(0.28))


def pt_block(c, cx, cy, mm, INK):
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(cx - mm(0.5), cy - mm(0.3))
    p.lineTo(cx - mm(0.2), cy + mm(0.45))
    p.lineTo(cx + mm(0.45), cy + mm(0.2))
    p.lineTo(cx + mm(0.3), cy - mm(0.42))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def pt_grube(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.28)
    for i in range(3):
        c.line(cx - mm(0.7), cy - mm(0.4) + i * mm(0.4),
               cx + mm(0.7), cy - mm(0.4) + i * mm(0.4))
    c.circle(cx, cy, mm(0.75), stroke=1, fill=0)


def pt_bergwerk(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.35)
    d = mm(0.6)
    c.line(cx - d, cy - d, cx + d, cy + d)
    c.line(cx - d, cy + d, cx + d, cy - d)


def pt_schornstein(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.rect(cx - mm(0.18), cy - mm(0.5), mm(0.36), mm(1.05), stroke=0, fill=1)
    c.setLineWidth(0.25)
    c.circle(cx, cy - mm(0.62), mm(0.18), stroke=1, fill=0)


def pt_hoehenpunkt(c, cx, cy, mm, INK):
    c.setFillColor(INK)
    c.circle(cx, cy, mm(0.18), stroke=0, fill=1)


def pt_funkturm(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.line(cx - mm(0.5), cy - mm(0.6), cx, cy + mm(0.75))
    c.line(cx + mm(0.5), cy - mm(0.6), cx, cy + mm(0.75))
    c.line(cx - mm(0.30), cy, cx + mm(0.30), cy)


def pt_wasserturm(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.rect(cx - mm(0.42), cy + mm(0.1), mm(0.84), mm(0.55), stroke=1, fill=0)
    c.line(cx, cy + mm(0.1), cx, cy - mm(0.65))


def pt_wegweiser(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.line(cx, cy - mm(0.6), cx, cy + mm(0.7))
    c.line(cx, cy + mm(0.55), cx + mm(0.55), cy + mm(0.4))


def pt_pegel(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.circle(cx, cy, mm(0.40), stroke=1, fill=0)
    c.line(cx, cy - mm(0.4), cx, cy - mm(0.85))


def pt_ruine(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    c.line(cx - mm(0.5), cy - mm(0.45), cx - mm(0.5), cy + mm(0.3))
    c.line(cx - mm(0.5), cy + mm(0.3), cx - mm(0.1), cy + mm(0.05))
    c.line(cx + mm(0.15), cy - mm(0.45), cx + mm(0.15), cy + mm(0.5))
    c.line(cx - mm(0.6), cy - mm(0.45), cx + mm(0.55), cy - mm(0.45))


def pt_grenzzeichen(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.circle(cx, cy, mm(0.34), stroke=1, fill=0)


def pt_baum(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.circle(cx, cy + mm(0.25), mm(0.42), stroke=1, fill=0)
    c.line(cx, cy - mm(0.15), cx, cy - mm(0.7))


def pt_huenenstein(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.circle(cx, cy, mm(0.30), stroke=1, fill=0)
    c.circle(cx, cy, mm(0.62), stroke=1, fill=0)


def pt_kilometerstein(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    d = mm(0.48)
    p = c.beginPath()
    p.moveTo(cx, cy + d)
    p.lineTo(cx - d, cy - d * 0.7)
    p.lineTo(cx + d, cy - d * 0.7)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def pt_funkstelle(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.circle(cx, cy - mm(0.35), mm(0.22), stroke=0, fill=1)
    c.setLineWidth(0.28)
    c.line(cx, cy - mm(0.2), cx, cy + mm(0.65))
    c.line(cx - mm(0.35), cy + mm(0.4), cx, cy + mm(0.65))
    c.line(cx + mm(0.35), cy + mm(0.4), cx, cy + mm(0.65))


def pt_foersterei(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setFillColor(INK)
    c.rect(cx - mm(0.3), cy - mm(0.3), mm(0.6), mm(0.6), stroke=0, fill=1)
    _nadel(c, cx + mm(0.75), cy, mm, INK)


def pt_schlachtfeld(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.32)
    c.line(cx - mm(0.55), cy - mm(0.5), cx + mm(0.55), cy + mm(0.5))
    c.line(cx + mm(0.55), cy - mm(0.5), cx - mm(0.55), cy + mm(0.5))
    c.line(cx - mm(0.55), cy + mm(0.5), cx - mm(0.3), cy + mm(0.72))


def pt_heiligenbild(c, cx, cy, mm, INK):
    c.setStrokeColor(INK)
    c.setLineWidth(0.3)
    c.line(cx, cy - mm(0.5), cx, cy + mm(0.6))
    c.line(cx - mm(0.3), cy + mm(0.3), cx + mm(0.3), cy + mm(0.3))
