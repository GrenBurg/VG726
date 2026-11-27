#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Het hoogteveld. Apart gehouden omdat zowel de generator als de tekenlaag
(en straks de game-engine) dezelfde functie moeten gebruiken: anders lopen
de hoogtelijnen niet door de hoogtecijfers.

Gebruik: init(seed, width_m, height_m) en daarna elevation(x, y).
"""
import math
import random

WIDTH_M = 2900.0
HEIGHT_M = 2800.0

BASE_H = 118.0            # hoogte bij de monding (west), m boven zeeniveau
SLOPE_EW = 14.0           # het dal loopt naar het westen af
FLANK = 26.0              # hoogteverschil dal -> flank

_P = []


def init(seed, width_m=None, height_m=None):
    global _P, WIDTH_M, HEIGHT_M
    if width_m:
        WIDTH_M = float(width_m)
    if height_m:
        HEIGHT_M = float(height_m)
    p = list(range(256))
    random.Random(seed).shuffle(p)
    _P = p * 2


def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def _grad(h, x, y):
    h &= 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)


def _perlin(x, y):
    xi, yi = int(math.floor(x)) & 255, int(math.floor(y)) & 255
    xf, yf = x - math.floor(x), y - math.floor(y)
    u, v = _fade(xf), _fade(yf)
    aa = _P[_P[xi] + yi]
    ab = _P[_P[xi] + yi + 1]
    ba = _P[_P[xi + 1] + yi]
    bb = _P[_P[xi + 1] + yi + 1]
    x1 = _grad(aa, xf, yf) + u * (_grad(ba, xf - 1, yf) - _grad(aa, xf, yf))
    x2 = _grad(ab, xf, yf - 1) + u * (_grad(bb, xf - 1, yf - 1) - _grad(ab, xf, yf - 1))
    return x1 + v * (x2 - x1)


def fbm(x, y, octaves=5, lac=2.0, gain=0.5):
    amp, freq, total, norm = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        total += amp * _perlin(x * freq, y * freq)
        norm += amp
        amp *= gain
        freq *= lac
    return total / norm


def valley_axis_y(x):
    """Noord-zuidpositie van de dalas bij oost-westpositie x (meters)."""
    return (0.52 * HEIGHT_M
            + 230.0 * math.sin(x / WIDTH_M * 2.1 * math.pi + 0.7)
            + 90.0 * math.sin(x / WIDTH_M * 5.3 * math.pi + 2.1))


def elevation(x, y):
    """Hoogte in meters op positie (x, y)."""
    d = abs(y - valley_axis_y(x))
    # dalprofiel: vlakke bodem, dan oplopende flanken die afvlakken
    flank = FLANK * (1.0 - math.exp(-(d / 620.0) ** 1.7))
    along = SLOPE_EW * (x / WIDTH_M)
    rough = 5.2 * fbm(x / 900.0, y / 900.0, octaves=5)
    micro = 1.1 * fbm(x / 230.0 + 11.0, y / 230.0 + 7.0, octaves=3)
    return BASE_H + along + flank + rough + micro
