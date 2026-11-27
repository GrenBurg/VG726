#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haalt de hoogtepunten (spot heights) uit het kaartbeeld met OCR, bouwt daar
een geinterpoleerd hoogtevlak van, en bepaalt waar hoogtelijnen de kaartrand
snijden. Die waarden gaan in de randband, zoals op het origineel.

Waarom deze omweg: het origineel zet bij elke hoogtelijn die de bladrand
snijdt de waarde in de band. De moderne bronkaart tekent hoogtelijnen wel,
maar labelt ze nauwelijks -- de bruine cijfers zijn hoogtepunten met een
decimaal, geen hoogtelijnwaarden. Directe overname kan dus niet; via de
hoogtepunten wel, zij het als benadering.
"""
import re
import numpy as np
from PIL import Image
import pytesseract
from scipy.interpolate import Rbf

Image.MAX_IMAGE_PIXELS = None

SRC = "map_utm.png"
E0, E1 = 340.60, 352.25
N0, N1 = 5779.305, 5790.400
PXKM = 472.441

im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.array(im).astype(int)
print("beeld", W, H)

# --------------------------------------------------- hoogtecijfers vinden --
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (r < 110) & (g < 105) & (b < 105)
bw = ((~dark) * 255).astype("uint8")

TILE = 700
OVER = 150
SCALE = 2
pat = re.compile(r"^(\d{1,2})[.,](\d)$")
pts = []

for ty in range(0, H, TILE - OVER):
    for tx in range(0, W, TILE - OVER):
        x1, y1 = min(tx + TILE, W), min(ty + TILE, H)
        if x1 - tx < 200 or y1 - ty < 200:
            continue
        tl = bw[ty:y1, tx:x1]
        tile = Image.fromarray(tl).resize(((x1-tx)*SCALE, (y1-ty)*SCALE), Image.LANCZOS)
        try:
            d = pytesseract.image_to_data(
                tile, config="--psm 11 -c tessedit_char_whitelist=0123456789.,",
                output_type=pytesseract.Output.DICT)
        except Exception:
            continue
        for i, t in enumerate(d["text"]):
            t = t.strip()
            m = pat.match(t)
            if not m:
                continue
            try:
                conf = float(d["conf"][i])
            except Exception:
                conf = -1
            if conf < 40:
                continue
            val = float(f"{m.group(1)}.{m.group(2)}")
            if not (8.0 <= val <= 55.0):
                continue
            cx = tx + (d["left"][i] + d["width"][i] / 2) / SCALE
            cy = ty + (d["top"][i] + d["height"][i] / 2) / SCALE
            pts.append((cx, cy, val))

# ontdubbelen (tiles overlappen)
uniq = []
for cx, cy, v in pts:
    if not any(abs(cx - ux) < 40 and abs(cy - uy) < 40 for ux, uy, _ in uniq):
        uniq.append((cx, cy, v))
print("hoogtepunten gevonden:", len(uniq))
vals = [p[2] for p in uniq]
if vals:
    print("bereik", round(min(vals), 1), "-", round(max(vals), 1),
          " mediaan", round(float(np.median(vals)), 1))

np.save("spotheights.npy", np.array(uniq))
