#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procedurele terreingenerator voor een fictief oostfront-kaartblad.

Levert terreindata als JSON. Die data dient twee doelen:
  1. het tekenen van een Meßtischblatt (terrain_draw.py)
  2. de game zelf -- hoogteveld, wegen, bos en bebouwing zijn precies wat
     een engine nodig heeft voor zicht, dekking en begaanbaarheid

Alle coördinaten in METERS vanaf de linkerbenedenhoek van het kaartvlak,
zodat de data onafhankelijk is van de kaartschaal.

Het terreinmodel is bewust eenvoudig gehouden en past bij een Russisch
beeklandschap: een dal dat van oost naar west afwatert, bos op de hogere
flanken, akkers en weiden in het dal, een dorp aan de doorgaande weg.
"""
import json
import math
import random
import sys

# ------------------------------------------------------------- parameters --
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1943

WIDTH_M = 2900.0          # kaartvlak oost-west
HEIGHT_M = 2800.0         # noord-zuid
CONTOUR_INTERVAL = 2.5    # hoogtelijnen om de 2,5 m (vlak landschap)

VILLAGE_NAME = "Perdunowka"      # Duitse transcriptie; vrij te wijzigen
HAMLET_NAME = "Nowo-Sselo"
STREAM_NAME = "Losch"            # beeknaam
WOOD_NAME = "Tschornyj Les"      # 'zwart bos'

rnd = random.Random(SEED)

# ------------------------------------------------------------ hoogteveld ---
# Het hoogteveld zit in een eigen module, zodat de tekenlaag en de game
# precies dezelfde functie gebruiken.
import terrain_field as field

field.init(SEED, WIDTH_M, HEIGHT_M)
fbm = field.fbm
valley_axis_y = field.valley_axis_y
elevation = field.elevation
BASE_H, SLOPE_EW, FLANK = field.BASE_H, field.SLOPE_EW, field.FLANK


# --------------------------------------------------------------- wegen -----
def _poly(points, n=140):
    """Catmull-Rom door de steunpunten, voor natuurlijk slingerende lijnen."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        for j in range(n // (len(pts) - 3) + 1):
            t = j / (n / (len(pts) - 3))
            if t > 1:
                break
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    return out


# de beek volgt de dalas
stream = [(x, valley_axis_y(x) + 22.0 * math.sin(x / 140.0))
          for x in range(0, int(WIDTH_M) + 1, 25)]

# dorp aan de beek, iets ten oosten van het midden
VX = 0.60 * WIDTH_M
VY = valley_axis_y(VX) - 95.0

# doorgaande weg (II A) oost-west door het dal, langs het dorp
road_main = _poly([
    (-40.0, valley_axis_y(0.0) - 150.0),
    (0.22 * WIDTH_M, valley_axis_y(0.22 * WIDTH_M) - 190.0),
    (0.42 * WIDTH_M, valley_axis_y(0.42 * WIDTH_M) - 120.0),
    (VX, VY),
    (0.80 * WIDTH_M, valley_axis_y(0.80 * WIDTH_M) - 140.0),
    (WIDTH_M + 40.0, valley_axis_y(WIDTH_M) - 165.0),
], n=220)

# zijweg (III) naar het noorden, over de flank het bos in
road_north = _poly([
    (VX - 60.0, VY),
    (VX - 180.0, VY - 340.0),
    (VX - 120.0, VY - 700.0),
    (VX - 250.0, VY - 1050.0),
], n=120)

# veldweg (III) naar het zuiden, naar het gehucht
HX, HY = 0.27 * WIDTH_M, valley_axis_y(0.27 * WIDTH_M) + 560.0
road_south = _poly([
    (0.38 * WIDTH_M, valley_axis_y(0.38 * WIDTH_M) - 150.0),
    (0.34 * WIDTH_M, valley_axis_y(0.34 * WIDTH_M) + 180.0),
    (HX + 60.0, HY - 90.0),
    (HX, HY),
], n=110)

# karrenspoor langs de beek
road_track = _poly([
    (0.10 * WIDTH_M, valley_axis_y(0.10 * WIDTH_M) + 70.0),
    (0.30 * WIDTH_M, valley_axis_y(0.30 * WIDTH_M) + 55.0),
    (0.52 * WIDTH_M, valley_axis_y(0.52 * WIDTH_M) + 80.0),
    (0.72 * WIDTH_M, valley_axis_y(0.72 * WIDTH_M) + 45.0),
], n=120)


# ------------------------------------------------------------- vlakken -----
def _blob(cx, cy, rx, ry, rough, n=56, seed=0):
    """Onregelmatig gesloten vlak rond (cx, cy)."""
    r = random.Random(seed)
    phases = [r.uniform(0, 6.283) for _ in range(4)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = (1.0
             + rough * 0.45 * math.sin(3 * a + phases[0])
             + rough * 0.30 * math.sin(5 * a + phases[1])
             + rough * 0.18 * math.sin(8 * a + phases[2]))
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


woods = [
    {"kind": "nadelwald", "name": WOOD_NAME,
     "poly": _blob(0.30 * WIDTH_M, 0.17 * HEIGHT_M, 560, 330, 0.30, seed=11)},
    {"kind": "nadelwald", "name": None,
     "poly": _blob(0.80 * WIDTH_M, 0.14 * HEIGHT_M, 400, 250, 0.34, seed=12)},
    {"kind": "laubwald", "name": None,
     "poly": _blob(0.13 * WIDTH_M, 0.72 * HEIGHT_M, 330, 240, 0.32, seed=13)},
    {"kind": "mischwald", "name": None,
     "poly": _blob(0.72 * WIDTH_M, 0.84 * HEIGHT_M, 450, 260, 0.30, seed=14)},
]

marsh = [{"kind": "bruch", "name": None,
          "poly": _blob(0.47 * WIDTH_M, valley_axis_y(0.47 * WIDTH_M) + 150,
                        300, 120, 0.26, seed=21)}]

meadow = [
    {"kind": "wiese", "name": None,
     "poly": _blob(0.20 * WIDTH_M, valley_axis_y(0.20 * WIDTH_M) + 60,
                   360, 150, 0.22, seed=31)},
    {"kind": "wiese", "name": None,
     "poly": _blob(0.66 * WIDTH_M, valley_axis_y(0.66 * WIDTH_M) + 130,
                   320, 140, 0.24, seed=32)},
]

heath = [{"kind": "heide", "name": None,
          "poly": _blob(0.90 * WIDTH_M, 0.52 * HEIGHT_M, 260, 300, 0.28, seed=41)}]


# ------------------------------------------------------------ bebouwing ----
def _houses_along(path, t0, t1, count, offset, seed):
    """Zet huisjes langs een deel van een weg, afwisselend links en rechts."""
    r = random.Random(seed)
    out = []
    for i in range(count):
        t = t0 + (t1 - t0) * (i / max(1, count - 1))
        k = int(t * (len(path) - 1))
        x, y = path[k]
        nx, ny = path[min(k + 1, len(path) - 1)]
        dx, dy = nx - x, ny - y
        L = math.hypot(dx, dy) or 1.0
        px, py = -dy / L, dx / L
        side = 1 if i % 2 == 0 else -1
        d = offset + r.uniform(-9, 14)
        out.append({
            "x": x + px * d * side + r.uniform(-7, 7),
            "y": y + py * d * side + r.uniform(-7, 7),
            "w": r.uniform(13, 20),
            "h": r.uniform(9, 14),
            "rot": math.degrees(math.atan2(dy, dx)) + r.uniform(-7, 7),
        })
    return out


buildings = _houses_along(road_main, 0.44, 0.66, 26, 34, 101)
buildings += _houses_along(road_north, 0.00, 0.14, 6, 30, 102)
hamlet = _houses_along(road_south, 0.84, 1.00, 9, 28, 103)

church = {"x": VX - 20.0, "y": VY + 46.0}
windmill = {"x": VX + 330.0, "y": VY - 210.0}
cemetery = _blob(VX - 470.0, VY + 235.0, 72, 50, 0.16, n=28, seed=51)

# ---------------------------------------------------------- trig-punten ----
trig = []
for _ in range(3):
    while True:
        x, y = rnd.uniform(200, WIDTH_M - 200), rnd.uniform(200, HEIGHT_M - 200)
        if abs(y - valley_axis_y(x)) > 420:
            trig.append({"x": x, "y": y, "h": round(elevation(x, y), 1)})
            break

spot_heights = []
for _ in range(16):
    x, y = rnd.uniform(80, WIDTH_M - 80), rnd.uniform(80, HEIGHT_M - 80)
    spot_heights.append({"x": x, "y": y, "h": round(elevation(x, y), 1)})

# ----------------------------------------------------------------- uit -----
data = {
    "meta": {
        "seed": SEED,
        "width_m": WIDTH_M,
        "height_m": HEIGHT_M,
        "contour_interval_m": CONTOUR_INTERVAL,
        "elevation_min_m": None,
        "elevation_max_m": None,
        "names": {"village": VILLAGE_NAME, "hamlet": HAMLET_NAME,
                  "stream": STREAM_NAME, "wood": WOOD_NAME},
    },
    "roads": [
        {"cls": "IIA", "name": None, "path": road_main},
        {"cls": "III", "name": None, "path": road_north},
        {"cls": "III", "name": None, "path": road_south},
        {"cls": "track", "name": None, "path": road_track},
    ],
    "stream": {"name": STREAM_NAME, "path": stream},
    "areas": woods + marsh + meadow + heath,
    "buildings": buildings,
    "hamlet_buildings": hamlet,
    "church": church,
    "windmill": windmill,
    "cemetery": cemetery,
    "trig": trig,
    "spot_heights": spot_heights,
    "labels": [
        {"text": VILLAGE_NAME, "x": VX, "y": VY - 165, "kind": "village"},
        {"text": HAMLET_NAME, "x": HX, "y": HY + 55, "kind": "hamlet"},
        {"text": WOOD_NAME, "x": 0.30 * WIDTH_M, "y": 0.17 * HEIGHT_M, "kind": "wood"},
    ],
}

# hoogtebereik bepalen voor de hoogtelijnen
lo, hi = 1e9, -1e9
for j in range(0, 141):
    for i in range(0, 141):
        h = elevation(i / 140 * WIDTH_M, j / 140 * HEIGHT_M)
        lo, hi = min(lo, h), max(hi, h)
data["meta"]["elevation_min_m"] = round(lo, 2)
data["meta"]["elevation_max_m"] = round(hi, 2)

with open("terrain.json", "w") as f:
    json.dump(data, f)

print(f"seed {SEED}   {WIDTH_M:.0f} x {HEIGHT_M:.0f} m")
print(f"hoogte {lo:.1f} .. {hi:.1f} m  (verschil {hi-lo:.1f} m)")
print(f"hoogtelijnen om de {CONTOUR_INTERVAL} m -> "
      f"{int((hi-lo)/CONTOUR_INTERVAL)} stuks")
print(f"wegen {len(data['roads'])}, vlakken {len(data['areas'])}, "
      f"gebouwen {len(buildings)+len(hamlet)}")
print("geschreven: terrain.json")
