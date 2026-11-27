#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bepaalt de hoogtecijfers voor de randband.

Werkwijze:
  1. de POSITIES komen uit de kaart zelf: waar snijdt een getekende bruine
     hoogtelijn de neat line?
  2. de WAARDEN komen uit een hoogtevlak dat is geinterpoleerd over de met
     OCR gevonden hoogtepunten, afgerond op het hoogtelijn-interval.

Positie is dus echt, waarde is een benadering. Dat is de eerlijkste
combinatie die uit deze bron te halen is: de moderne kaart labelt haar
hoogtelijnen niet, dus de waarde valt niet direct af te lezen.
"""
import numpy as np
from PIL import Image
# geen RBF: die extrapoleert buiten de meetpunten naar onmogelijke hoogtes
# (leverde 47,5 en 50 m op terwijl Twente hier niet boven ~40 m komt).
# Inverse-afstandsweging blijft per definitie binnen het bereik van de data.

Image.MAX_IMAGE_PIXELS = None

E0, E1 = 340.60, 352.25
N0, N1 = 5779.305, 5790.400
PXKM = 472.441
INTERVAL = 2.5                      # aangenomen hoogtelijn-interval (m)

a = np.array(Image.open("map_utm.png").convert("RGB")).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
brown = (r > 110) & (r < 205) & (g > 55) & (g < 135) & (b < 95) & ((r - b) > 50)

pts = np.load("spotheights.npy")
print("hoogtepunten:", len(pts))
px, py, pv = pts[:, 0], pts[:, 1], pts[:, 2]

POW = 2.2


def surface(xs, ys):
    xs = np.asarray(xs, float)[:, None]
    ys = np.asarray(ys, float)[:, None]
    d2 = (xs - px[None, :]) ** 2 + (ys - py[None, :]) ** 2
    d2 = np.maximum(d2, 1.0)
    w = 1.0 / d2 ** (POW / 2.0)
    return (w * pv[None, :]).sum(axis=1) / w.sum(axis=1)


def crossings(kind, band_px=26, minrun=2):
    """Vindt clusters bruine pixels in een strook langs een rand."""
    if kind == "top":
        strip = brown[2:2 + band_px, :]
        prof = strip.sum(axis=0)
    elif kind == "bottom":
        strip = brown[H - 2 - band_px:H - 2, :]
        prof = strip.sum(axis=0)
    elif kind == "left":
        strip = brown[:, 2:2 + band_px]
        prof = strip.sum(axis=1)
    else:
        strip = brown[:, W - 2 - band_px:W - 2]
        prof = strip.sum(axis=1)
    on = prof >= minrun
    out = []
    i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            if 2 <= (j - i) <= 60:
                out.append((i + j - 1) / 2.0)
            i = j
        else:
            i += 1
    return out


result = {}
for kind in ("top", "bottom", "left", "right"):
    cs = crossings(kind)
    items = []
    for c in cs:
        if kind == "top":
            x, y = c, 14.0
        elif kind == "bottom":
            x, y = c, H - 14.0
        elif kind == "left":
            x, y = 14.0, c
        else:
            x, y = W - 14.0, c
        h = float(surface([x], [y])[0])
        if not (10.0 <= h <= 45.0):
            continue
        hq = round(h / INTERVAL) * INTERVAL
        items.append((c, hq))
    # te dicht op elkaar of zelfde waarde naast elkaar: dunnen
    thin = []
    for c, hq in items:
        if thin and abs(c - thin[-1][0]) < 34:
            continue
        thin.append((c, hq))
    result[kind] = thin
    print(f"{kind:7s} {len(thin):3d} kruisingen  "
          f"waarden {sorted({v for _, v in thin})}")

np.save("edge_heights.npy", np.array(
    [(k, c, v) for k, lst in result.items() for c, v in lst],
    dtype=object), allow_pickle=True)
print("opgeslagen: edge_heights.npy")
