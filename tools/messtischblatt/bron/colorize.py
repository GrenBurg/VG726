#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zet het moderne stafkaartbeeld om naar het gedempte kleurpalet van een
Duitse legerkaart (referentie: Truppenkarte 39 West Rhenen, 1942).

Uitgangspunt: de kaart is voor ons NIEUW. Er wordt dus niets vergeeld of
bevlekt -- het papier blijft wit en de druk blijft scherp. Alleen het
kleurgebruik wordt teruggebracht naar het periodepalet:
  - verzadiging fors omlaag (moderne kaart ~0,40 -> doel ~0,13)
  - lichte warme verschuiving (minder blauw)
  - hue-correcties per kleurgroep: fel groen -> olijf, hard blauw -> grijsblauw,
    signaalrood/oranje -> baksteenrood, geel -> bleek oker
"""
import numpy as np
from PIL import Image
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "map600-1.png"
DST = sys.argv[2] if len(sys.argv) > 2 else "map600_period.png"

SAT_FACTOR = 0.34          # globale verzadigingsdemping
WARM_B = 0.975             # blauwkanaal iets terug -> warmere druk
WHITE_KEEP = 0.93          # boven deze helderheid blijft het papierwit


def rgb_to_hsv(a):
    a = a.astype(np.float32) / 255.0
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    df = mx - mn
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    h = np.zeros_like(mx)
    m = (df > 1e-6)
    idx = m & (mx == r)
    h[idx] = ((g - b)[idx] / df[idx]) % 6
    idx = m & (mx == g)
    h[idx] = ((b - r)[idx] / df[idx]) + 2
    idx = m & (mx == b)
    h[idx] = ((r - g)[idx] / df[idx]) + 4
    h = h / 6.0
    s = np.zeros_like(mx)
    s[mx > 1e-6] = df[mx > 1e-6] / mx[mx > 1e-6]
    return h, s, mx


def hsv_to_rgb(h, s, v):
    i = np.floor(h * 6).astype(np.int32)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, q, p, p, q])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=2)


def hue_shift(h, s):
    """Verschuift kleurgroepen naar hun periode-equivalent.
    h in [0,1): 0=rood, 0.083=oranje, 0.17=geel, 0.33=groen, 0.5=cyaan,
    0.66=blauw."""
    hn = h.copy()

    # groen (0.20..0.45) -> olijf/geelgroen, iets naar geel toe
    m = (h > 0.20) & (h < 0.45)
    hn[m] = 0.19 + (h[m] - 0.20) * 0.42

    # cyaan/blauw water (0.45..0.75) -> gedempt grijsblauw, iets naar cyaan
    m = (h >= 0.45) & (h < 0.75)
    hn[m] = 0.50 + (h[m] - 0.45) * 0.40

    # geel/oranje wegen (0.08..0.20) -> bleek oker
    m = (h >= 0.08) & (h <= 0.20)
    hn[m] = 0.095 + (h[m] - 0.08) * 0.35

    # rood (0..0.08 en >0.92) -> baksteen, nauwelijks verschoven
    return hn


def main():
    im = Image.open(SRC).convert("RGB")
    a = np.array(im)
    print("in :", a.shape)

    h, s, v = rgb_to_hsv(a)

    # papierwit beschermen
    white = (v > WHITE_KEEP) & (s < 0.10)

    h2 = hue_shift(h, s)

    # verzadiging dempen; sterk verzadigde vlakken iets extra
    s2 = s * SAT_FACTOR
    s2 = np.clip(s2 * (1.0 - 0.25 * s), 0, 1)

    # helderheid: vlakken iets lichter zodat de lijnen domineren, zoals in druk
    v2 = np.clip(0.06 + v * 0.945, 0, 1)
    # donkere lijnen juist niet oplichten
    dark = v < 0.45
    v2[dark] = np.clip(v[dark] * 0.96, 0, 1)

    out = hsv_to_rgb(h2, s2, v2)
    out[:, :, 2] *= WARM_B
    out = np.clip(out, 0, 1)

    # papier terug naar zuiver wit
    out[white] = np.stack([np.ones(white.sum()),
                           np.ones(white.sum()),
                           np.ones(white.sum())], axis=1) * 0.995

    res = (out * 255).astype(np.uint8)
    Image.fromarray(res).save(DST)
    print("out:", DST)

    hh, ss, vv = rgb_to_hsv(res)
    print("gem. saturatie na  :", round(float(ss.mean()), 3))
    print("gem. value na      :", round(float(vv.mean()), 3))


main()
