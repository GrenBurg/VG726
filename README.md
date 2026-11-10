# VG726

Klein platform met een startpagina en vijf onderdelen:

| Map | Wat |
|---|---|
| `/` | Startpagina: kies wat je wilt doen |
| `uitrusting/` | Uitrustingsgids voor nieuwe leden (klikbare soldaat, voor- en achterkant) |
| `carpoolkaart/` | Carpoolkaart: woonplaatsen van deelnemers om samen te rijden |
| `setboek/` | Setboek, de sport-app (6-weken trainingsschema, werkt offline) |
| `reibert/` | Reibert Online: de inhoud van het boekje *Der Dienstunterricht im Heere* (2026), doorzoekbaar en met correcties |
| `funkgeraet/` | Bediensimulator Tornisterfunkgerät d2 (Torn.Fu.d2): opbouwen, afstemmen, morse-oefenen en online morsen via Ably |

Alles is statische HTML en draait op GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**.
De site staat daarna op `https://grenburg.github.io/VG726/`.

Een nieuw onderdeel toevoegen: maak een eigen map met een `index.html` en zet er een tegel voor in de startpagina.

## Funkgerät d2: online morsen

GitHub Pages serveert alleen statische bestanden en kan dus geen tijdelijke Ably-toegangscode ophalen.
Wie op deze site online wil morsen, vult zelf een Ably-sleutel in het venster *Online* in; die wordt nergens opgeslagen.
Zet hiervoor bij voorkeur een aparte, beperkte sleutel aan (alleen `tornfud2-*` kanalen, rechten publish/subscribe/presence), nooit de root-sleutel.
Alles behalve online morsen werkt zonder sleutel.
