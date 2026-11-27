#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zoekt lettertypebestanden op, zodat de scripts ook buiten deze container
draaien. De Playfair- en Unifraktur-bestanden staan in fonts/ naast de
scripts; DejaVu komt van het systeem en staat per besturingssysteem ergens
anders.
"""
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))

ZOEKPADEN = [
    os.path.join(HIER, "fonts"),
    os.path.join(HIER, "..", "fonts"),
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/share/fonts/TTF",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.fonts"),
    os.path.expanduser("~/Library/Fonts"),
    "/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    r"C:\Windows\Fonts",
]


def pad(naam):
    """Volledig pad naar een lettertypebestand, of een duidelijke foutmelding."""
    if os.path.isabs(naam) and os.path.exists(naam):
        return naam
    for d in ZOEKPADEN:
        p = os.path.join(d, os.path.basename(naam))
        if os.path.exists(p):
            return p
    sys.exit(
        f"Lettertype niet gevonden: {naam}\n"
        "Zet het in de map fonts/ naast dit script, of installeer de "
        "DejaVu-lettertypen (Debian/Ubuntu: apt install fonts-dejavu)."
    )
