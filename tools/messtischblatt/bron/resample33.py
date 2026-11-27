#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hersamplet blad 33 Oost (Apeldoorn/Deventer) langs de UTM 32U-assen,
gecentreerd rond Wilp.

Net als bij blad 34 Oost is het blad in RD opgemaakt en ligt het
UTM-raster er schuin overheen. Helling gemeten aan de RANDTIKKEN (niet
aan de labels, die staan boven +5,8 px en onder +3,0 px naast hun lijn
en geven daardoor een 0,04 graad te grote helling): 2,8363 graden.
Analytisch volgt uit het verschil in meridiaanconvergentie UTM32 vs RD
op 52,2N / 6,08O: 2,8555 graden -- dat bevestigt de meting.

Anker: snijpunt van rasterlijn E=300 (boven x 1542,2 / onder x 1737,3)
en N=5790 (links y 959,6), alle drie uit randtikken.

Dit blad draagt TWEE rasters (zone 31U blauw, zone 32U zwart). Alleen
het zwarte 32U-raster wordt gebruikt, net als op het Haaksbergen-blad.

Schaal: langs de bladrand meten de rastertikken 157,67 px/km, maar dat is
de SCHUINE doorsnede. De loodrechte rasterafstand is 157,67 / sqrt(1+s^2)
= 157,478 px/km, wat overeenkomt met de theoretische 157,480 (20 mm/km bij
200 dpi) tot op 0,001%. De bron is dus exact op schaal. S_SRC moet de
loodrechte afstand zijn omdat eE en eN genormaliseerd zijn.
"""
import math
import subprocess
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# ------------------------------------------------- gemeten brongeometrie ---
SLOPE = 0.049632                      # dx/dy van een lijn van constante E
DPI_SRC = 600
S_SRC = 157.478 * (DPI_SRC / 200.0)   # LOODRECHTE rasterafstand (zie kop)
S_DST = 20.0 * DPI_SRC / 25.4         # doel: 1 km = 20 mm op 1:50000-render
print(f"bron px/km {S_SRC:.3f}   doel px/km {S_DST:.3f}   "
      f"schaalverschil {100*(S_SRC/S_DST-1):+.3f}%")

# anker: snijpunt van rasterlijn E=300 en N=5790, in bron-px bij 200 dpi
AX200, AY200 = 1573.92, 946.03
AX, AY = AX200 * (DPI_SRC / 200.0), AY200 * (DPI_SRC / 200.0)
EREF, NREF = 300.0, 5790.0

n = math.sqrt(1.0 + SLOPE * SLOPE)
eE = (1.0 / n, -SLOPE / n)
eN = (-SLOPE / n, -1.0 / n)

# ------------------------------------------- uitsnede, gecentreerd op Wilp -
# Wilp (dorpskern, gemeten op de bron) ligt op E 305,509 / N 5789,282.
# Horizontaal exact gecentreerd; verticaal loopt het kader bovenaan tegen
# de bladrand, dus Wilp zit daar op 33% in plaats van 50%.
# E0 is 40 m bijgesteld zodat de eerste rasterlijn op een nette 16,0 mm valt.
E0, E1 = 299.60, 311.25
N0, N1 = 5781.805, 5792.900

OUT_W = int(round((E1 - E0) * S_DST))
OUT_H = int(round((N1 - N0) * S_DST))
print(f"uitsnede {E1-E0:.3f} x {N1-N0:.3f} km  ->  {OUT_W} x {OUT_H} px")


def src_of(E, N):
    return (AX + (E - EREF) * S_SRC * eE[0] + (N - NREF) * S_SRC * eN[0],
            AY + (E - EREF) * S_SRC * eE[1] + (N - NREF) * S_SRC * eN[1])


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
                "base33.pdf", "src33"], check=True)

src = Image.open("src33-1.png").convert("RGB")
print("bron geladen:", src.size)

# out(ox,oy) -> E = E0 + ox/S_DST ; N = N1 - oy/S_DST
a = (S_SRC / S_DST) * eE[0]
b = -(S_SRC / S_DST) * eN[0]
cc = src_of(E0, N1)[0] - bx0
d = (S_SRC / S_DST) * eE[1]
e = -(S_SRC / S_DST) * eN[1]
f = src_of(E0, N1)[1] - by0

out = src.transform((OUT_W, OUT_H), Image.AFFINE, (a, b, cc, d, e, f),
                    resample=Image.BICUBIC)
out.save("wilp_utm.png")
print("geschreven: wilp_utm.png", out.size)

print("\nrasterlijnen in de uitvoer (mm op het 1:25000-blad):")
for E in range(int(math.ceil(E0)), int(math.floor(E1)) + 1):
    print(f"  E {E} -> {(E - E0) * 40:6.1f} mm")
for N in range(int(math.floor(N1)), int(math.ceil(N0)) - 1, -1):
    print(f"  N {N} -> {(N1 - N) * 40:6.1f} mm")
