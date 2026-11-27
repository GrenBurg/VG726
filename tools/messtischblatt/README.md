# Meßtischblatt-template

Gereedschap om kaarten te maken in de vormgeving van een Preußisches
Meßtischblatt, voor gebruik bij reenactment. Alles is vector: het resultaat is
een PDF die op ware grootte scherp afdrukt.

De maatvoering is overgenomen van een echt blad — **4614 (2656) Arnsberg Süd,
X.1944** — door het gescande origineel recht te draaien en op te meten. Kader,
randverdeling, Planzeiger, legenda en typografie staan daardoor op de plek van
het origineel, niet op een plek die er ongeveer op lijkt.

Met deze bestanden zijn de bladen **Wilp** en **Haaksbergen** gemaakt die onder
[Kaarten](../../maps/) staan.

## Wat staat hier

| bestand | wat het doet |
|---|---|
| `mtb_template.py` | het hoofdscript: tekent een volledig blad (654 × 549 mm, kaartvlak 466 × 444 mm) |
| `mtb_template_haaksbergen.py` | dezelfde template, variant waarmee het blad Haaksbergen is gemaakt |
| `mtb_symbols.py` | ruim zestig Duitse kaartsymbolen (bos, moeras, wegklassen, kerk, molen, trig-punt …) |
| `fontpad.py` | zoekt de lettertypen op, zodat het ook buiten deze container draait |
| `fonts/` | Playfair Display en UnifrakturCook (SIL OFL, mogen mee) |
| `terrein/` | procedurele terreingenerator — verzint een kaartblad in plaats van er een na te tekenen |
| `bron/` | gereedschap om een moderne stafkaart tot bronmateriaal te verwerken |

## Benodigdheden

```sh
pip install -r requirements.txt
sudo apt install fonts-dejavu      # Debian/Ubuntu; macOS en Windows: zie fonts/LEESMIJ.txt
```

## Een blad maken van een bestaande stafkaart

De werkwijze in vier stappen, met de scripts uit `bron/`:

1. **`resample_utm.py` / `resample33.py`** — de Nederlandse stafkaart (1 : 50 000,
   RD-raster) in één keer herbemonsteren langs de UTM-assen en naar 1 : 25 000
   brengen. In één bewerking, want elke extra herbemonstering maakt het beeld
   zachter. Let op de meridiaanconvergentie: RD en UTM 32U staan hier ongeveer
   2,85° uit elkaar.
2. **`colorize.py`** — de moderne kleuren omzetten naar het palet van een
   periodekaart. Geen vergeling: voor reenactment is de kaart *nieuw*.
3. **`heights.py` + `edge_heights.py`** — hoogtecijfers met OCR uit de bron
   lezen en daarmee de hoogtewaarden in de randband bepalen. De *posities* komen
   uit de kaart zelf (waar snijdt een hoogtelijn de kaderlijn), de *waarden* uit
   inverse-afstandsweging over de gevonden punten.
4. **`mtb_template.py`** — het blad tekenen met de verwerkte kaartafbeelding erin.

De bronkaarten zelf staan hier niet: dat zijn bestanden van Defensie en het
Kadaster van tientallen megabytes, en dit is een openbare repo.

### Een maat nameten

De getallen bovenin `mtb_template.py` zijn millimeters, opgemeten aan het
origineel:

```python
PAPER_W = 654.2;  PAPER_H = 549.0
MAP_W   = 466.0;  MAP_H   = 443.8     # neat line
GRAD_BAND = 6.634                      # de gradenband langs het kaartvlak
GAP_INNER = 0.911; HEAVY_W = 1.145; GAP_OUTER = 1.017
```

Wie een andere maat wil, verandert ze daar; de rest van het blad rekent mee.

## Een blad verzinnen (`terrein/`)

Voor oefeningen en voor de infanteriegame is er geen bestaande kaart nodig.
`terrein/` maakt er zelf een:

```sh
cd terrein
python3 terrain_gen.py 1943      # seed -> terrain.json
python3 terrain_draw.py          # terrain.json -> messtischblatt_game.pdf
```

- `terrain_field.py` — het hoogteveld (eigen Perlin-ruis, geen externe
  afhankelijkheid). Generator én tekenlaag gebruiken deze ene functie, anders
  lopen de hoogtelijnen niet door de hoogtecijfers.
- `terrain_gen.py` — beek, wegen per klasse, bos, moeras, weide, heide,
  bebouwing, kerk, molen, begraafplaats, trig- en hoogtepunten. Schrijft
  `terrain.json`.
- `terrain_draw.py` — tekent daar een Meßtischblatt van.

Alle coördinaten in `terrain.json` staan in **meters vanaf de linkeronderhoek**
van het kaartvlak, los van de kaartschaal. Daardoor is dezelfde data ook
bruikbaar in een game-engine voor zicht, dekking en begaanbaarheid.

## Truppenkarte-overlay

`bron/truppenkarte_overlay.py` is iets anders: dat legt een periodekader over
een PDF-export uit [map.army](https://map.army) heen (A3, 1 : 25 000),
zwart-wit. Handig als je snel een kaart van een bestaand gebied nodig hebt.

## Let op

Dit zijn moderne kaarten in historische vormgeving, gemaakt voor reenactment.
Waar een echte stafkaart als bron is gebruikt, is het kaartbeeld van nu: wegen
en bebouwing kloppen met het heden, niet met 1944.
