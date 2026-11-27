#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haalt het kaartvlak uit de moderne stafkaart en hersamplet het langs de
UTM-assen, zodat het kilometerraster haaks op het kader komt te staan.

Achtergrond: het Nederlandse 1:50.000-blad is in RD (Rijksdriehoek)
opgemaakt; het UTM-raster is er als overdruk overheen gelegd en loopt
daardoor 2,864 graden schuin over het blad (gemeten; analytisch volgt uit
het verschil in meridiaanconvergentie tussen UTM32 en RD: 2,853 graden).

Een simpele crop levert dus een scheef raster op. Daarom hier een affiene
transformatie die de UTM-assen recht zet, in een enkele resampling-stap.
"""
import math
import subprocess
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# ------------------------------------------------- gemeten brongeometrie ---
SLOPE = 0.050025                 # dx/dy van een lijn van constante E
DPI_SRC = 600
S = 1000.0 / 25.4 / 50000.0 * 1000 * DPI_SRC / 25.4   # px per km, 1:50000
S = 20.0 * DPI_SRC / 25.4                              # 1 km = 20 mm op 1:50000
print("bron px/km:", round(S, 3))

# anker (E=340, N=5792) in bron-pixels bij 200 dpi, opgelost uit:
#   - rasterlijn E ligt op de bovenste neat line (py=298) bij px=1549+(E-340)*157.5
#   - rasterlijn N ligt op de linker neat line (px=1296) bij py=330+(5792-N)*157.5
AX200, AY200 = 1543.23, 317.0   # AX gecorrigeerd voor 43 m systematische offset
AX, AY = AX200 * 3, AY200 * 3     # naar 600 dpi

n = math.sqrt(1.0 + SLOPE * SLOPE)
eE = (1.0 / n, -SLOPE / n)         # richting van toenemende E, in bron-px
eN = (-SLOPE / n, -1.0 / n)        # richting van toenemende N

# ------------------------------------------------------- gewenste uitsnede -
E0, E1 = 340.60, 352.25
N0, N1 = 5779.305, 5790.400
OUT_W = int(round((E1 - E0) * S))
OUT_H = int(round((N1 - N0) * S))
print("uitvoer:", OUT_W, "x", OUT_H, "px")


def src_of(E, N):
    return (AX + (E - 340) * S * eE[0] + (N - 5792) * S * eN[0],
            AY + (E - 340) * S * eE[1] + (N - 5792) * S * eN[1])


corners = [src_of(E, N) for E in (E0, E1) for N in (N0, N1)]
xs = [p[0] for p in corners]
ys = [p[1] for p in corners]
PAD = 40
bx0 = int(math.floor(min(xs))) - PAD
by0 = int(math.floor(min(ys))) - PAD
bw = int(math.ceil(max(xs) - min(xs))) + 2 * PAD
bh = int(math.ceil(max(ys) - min(ys))) + 2 * PAD
print("bron-crop:", bx0, by0, bw, bh)

subprocess.run(["pdftoppm", "-png", "-r", str(DPI_SRC),
                "-x", str(bx0), "-y", str(by0), "-W", str(bw), "-H", str(bh),
                "base.pdf", "srcreg"], check=True)

src = Image.open("srcreg-1.png").convert("RGB")
print("bron geladen:", src.size)

# ----------------------------------------------- affiene transformatie -----
# out(ox,oy) -> E = E0 + ox/S ; N = N1 - oy/S
# src = A + (E-340)*S*eE + (N-5792)*S*eN, daarna verschoven met (bx0,by0)
a = eE[0]
b = -eN[0]
cc = AX + (E0 - 340) * S * eE[0] + (N1 - 5792) * S * eN[0] - bx0
d = eE[1]
e = -eN[1]
f = AY + (E0 - 340) * S * eE[1] + (N1 - 5792) * S * eN[1] - by0

out = src.transform((OUT_W, OUT_H), Image.AFFINE, (a, b, cc, d, e, f),
                    resample=Image.BICUBIC)
out.save("map_utm.png")
print("geschreven: map_utm.png", out.size)

# controle: waar liggen de hele-km rasterlijnen in de uitvoer?
for E in range(341, 353):
    print("  E", E, "->", round((E - E0) * S / (DPI_SRC / 25.4), 1), "mm")
