# VG726

Klein platform met een startpagina en zeven onderdelen:

| Map | Wat |
|---|---|
| `/` | Startpagina: kies wat je wilt doen |
| `uitrusting/` | Uitrustingsgids voor nieuwe leden (klikbare soldaat, voor- en achterkant) |
| `carpoolkaart/` | Carpoolkaart: woonplaatsen van deelnemers om samen te rijden |
| `setboek/` | Setboek, de sport-app (12-weken trainingsschema, werkt offline) |
| `reibert/` | Reibert Online: de inhoud van het boekje *Der Dienstunterricht im Heere* (2026), doorzoekbaar en met correcties |
| `funkgeraet/` | Bediensimulator Tornisterfunkgerät d2 (Torn.Fu.d2): opbouwen, afstemmen, morse-oefenen en online morsen via Ably |
| `downloads/` | Downloads: keuzemenu voor infobladen en kaarten |
| `downloads/infobladen/` | Infobladen: Merkblätter om af te drukken (Buchstabiertafel A6, Führungszeichen A5 gevouwen) |
| `downloads/drukwerken/` | Drukwerken: Das neue Soldaten-Liederbuch als A5 en als A4-boekje om te printen |
| `downloads/kaarten/` | Kaarten: kaartbladen in Meßtischblatt-stijl als PDF (Wilp, Haaksbergen) |
| `tarntafel/` | Tarntafel-generator: codetabel voor het Funksprechverkehr naar het systeem van de Tarntafel J.R. 726 (1942), af te drukken als PDF, met Excel-sleutel |

Alles is statische HTML en draait op GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / root**.
De site staat daarna op `https://grenburg.github.io/VG726/`.

Een nieuw onderdeel toevoegen: maak een eigen map met een `index.html` en zet er een tegel voor in de startpagina.

## Funkgerät d2: online morsen

GitHub Pages serveert alleen statische bestanden en kan dus geen tijdelijke Ably-toegangscode ophalen.
Wie op deze site online wil morsen, vult zelf een Ably-sleutel in het venster *Online* in; die wordt nergens opgeslagen.
Zet hiervoor bij voorkeur een aparte, beperkte sleutel aan (alleen `tornfud2-*` kanalen, rechten publish/subscribe/presence), nooit de root-sleutel.
Alles behalve online morsen werkt zonder sleutel.

## Tarntafel

De generator draait volledig in de browser. Dezelfde **sleutel** met dezelfde invoer geeft altijd dezelfde tafel, dus de leiding kan de tafel delen met een link (knop *Link kopiëren*, de invoer zit in de link na `#`). Afdrukken op A4 zonder marges; de Excel-sleutel bevat de Nederlandse vertaling van alle begrippen.

## Talen

De site is er in het Nederlands, Duits en Engels (Reibert blijft Nederlands). `i18n.js` zet de vlaggetjes rechtsboven en onthoudt de gekozen taal. Elke pagina laadt daarnaast een `vertalingen.js` met de Duitse en Engelse teksten; de sleutel is steeds de Nederlandse tekst. Nieuwe tekst toevoegen: geef het element `data-i18n` en zet de vertaling in `vertalingen.js`.
