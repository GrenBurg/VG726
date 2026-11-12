/* Melden oefenen — situaties.
 * Bron voor de regels: „Karten und Geländekunde“ (blz. 17–18, Meldungen) en
 * „Der Marschkompaß“ (blz. 20, Teilstriche bei Meldungen).
 *
 * Elke situatie:
 *   sit    tekst van de situatie in nl/de/en
 *   form   'block' (Meldeblock) of 'kurz' (korte mondelinge melding)
 *   checks verplichte punten: f = velden waarin gezocht wordt (of 'alle'),
 *          re = reguliere expressie (umlauts mogen; ä/ae/a tellen gelijk),
 *          l  = wat er gecontroleerd wordt (nl/de/en)
 *   warn   extra waarschuwingen alleen voor deze situatie
 *   model  voorbeeldmelding (Duits)
 */
window.MELDEN = [
  {
    id: 'wilp', blad: 'Wilp',
    t: { nl: 'Ingraven bij Wilp', de: 'Eingraben bei Wilp', en: 'Digging in near Wilp' },
    sit: {
      nl: 'Je bent Gefreiter Bakker en leidt een Spähtrupp van de 2. Gruppe. Op 6 november 1944 om 14.20 uur zie je vanaf de dijk twaalf vijandelijke soldaten die zich ingraven, ongeveer 600 meter ten noorden van de kerk van Wilp. Stuur een melding naar je compagnie, de 2. Kompanie.',
      de: 'Du bist Gefreiter Bakker und führst einen Spähtrupp der 2. Gruppe. Am 6. November 1944 um 14.20 Uhr siehst du vom Deich aus zwölf feindliche Soldaten, die sich eingraben, etwa 600 Meter nördlich der Kirche von Wilp. Schicke eine Meldung an deine Kompanie, die 2. Kompanie.',
      en: 'You are Gefreiter Bakker, leading a Spähtrupp of the 2. Gruppe. On 6 November 1944 at 14:20 you see from the dyke twelve enemy soldiers digging in, about 600 metres north of the church of Wilp. Send a report to your company, the 2. Kompanie.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'sp[aä]htrupp', l: { nl: 'Afzender is de eenheid: Spähtrupp …', de: 'Absender ist die Einheit: Spähtrupp …', en: 'Sender is the unit: Spähtrupp …' } },
      { f: ['an'], re: '\\b2\\b.*(kompanie|kp)|\\b2\\s*\\.\\s*\\/', l: { nl: 'Aan: 2. Kompanie', de: 'An: 2. Kompanie', en: 'To: 2. Kompanie' } },
      { f: ['wann'], re: '\\b6\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 6. 11. 44', de: 'Datum: 6. 11. 44', en: 'Date: 6. 11. 44' } },
      { f: ['wann'], re: '\\b14[\\s.:]?20\\b', l: { nl: 'Tijd: 14²⁰', de: 'Zeit: 14²⁰', en: 'Time: 14²⁰' } },
      { f: ['wer'], re: '\\b12\\b|zwölf', l: { nl: 'Precies aantal: zwölf', de: 'Genaue Zahl: zwölf', en: 'Exact number: zwölf' } },
      { f: ['wer'], re: 'sch[uü]tz|soldat|mann|männer|infanter|gruppe', l: { nl: 'Wat: Schützen / Soldaten', de: 'Was: Schützen / Soldaten', en: 'What: Schützen / Soldaten' } },
      { f: ['wer', 'wie'], re: 'grab|gräbt|schanz|stellung', l: { nl: 'Wat doen ze: Eingraben', de: 'Was tun sie: Eingraben', en: 'What are they doing: Eingraben' } },
      { f: ['wo'], re: 'wilp', l: { nl: 'Plaatsnaam zoals op de kaart: Wilp', de: 'Ortsname wie auf der Karte: Wilp', en: 'Place name as on the map: Wilp' } },
      { f: ['wo'], re: 'nord|nörd', l: { nl: 'Windrichting: nördlich', de: 'Himmelsrichtung: nördlich', en: 'Compass direction: nördlich' } },
      { f: ['wo'], re: '600|sechshundert', l: { nl: 'Afstand: 600 Meter', de: 'Entfernung: 600 Meter', en: 'Distance: 600 Meter' } }
    ],
    model: {
      abs: 'Spähtrupp Bakker, 2. Gruppe', an: '2. Kompanie', wann: '6. 11. 44, 14²⁰',
      wer: 'Zwölf feindliche Schützen, ungefähr Gruppenstärke', wie: 'beim Eingraben',
      wo: '600 Meter nördlich Kirche Wilp', zus: '', sig: 'Jan Bakker, Gefreiter'
    }
  },
  {
    id: 'twello-marsch', blad: 'Wilp',
    t: { nl: 'Kolonne naar Twello', de: 'Kolonne nach Twello', en: 'Column towards Twello' },
    sit: {
      nl: 'Je staat op post bij Twello (Posten van de 1. Gruppe, Grenadier Visser). Op 7 november 1944 om 07.45 uur zie je drie tanks en ongeveer acht vrachtwagens over de weg van Deventer naar Twello rijden, in de richting van Twello. Meld het aan je Zugführer, de 2. Zug.',
      de: 'Du stehst Posten bei Twello (Posten der 1. Gruppe, Grenadier Visser). Am 7. November 1944 um 07.45 Uhr siehst du drei Panzer und ungefähr acht Lastkraftwagen auf der Straße von Deventer nach Twello fahren, in Richtung Twello. Melde es deinem Zugführer, dem 2. Zug.',
      en: 'You are on sentry duty near Twello (sentry of the 1. Gruppe, Grenadier Visser). On 7 November 1944 at 07:45 you see three tanks and about eight lorries driving along the road from Deventer to Twello, heading for Twello. Report it to your platoon commander, the 2. Zug.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'posten|gruppe', l: { nl: 'Afzender is de eenheid: Posten, 1. Gruppe', de: 'Absender ist die Einheit: Posten, 1. Gruppe', en: 'Sender is the unit: Posten, 1. Gruppe' } },
      { f: ['an'], re: '\\b2\\b.*zug|zugf', l: { nl: 'Aan: 2. Zug', de: 'An: 2. Zug', en: 'To: 2. Zug' } },
      { f: ['wann'], re: '\\b7\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 7. 11. 44', de: 'Datum: 7. 11. 44', en: 'Date: 7. 11. 44' } },
      { f: ['wann'], re: '\\b0?7[\\s.:]?45\\b', l: { nl: 'Tijd: 07⁴⁵', de: 'Zeit: 07⁴⁵', en: 'Time: 07⁴⁵' } },
      { f: ['wer'], re: '(\\b3\\b|drei)[^,;]*panzer', l: { nl: 'Drei Panzer', de: 'Drei Panzer', en: 'Drei Panzer' } },
      { f: ['wer'], re: '(\\b8\\b|acht)[^,;]*(lkw|lastkraftwagen|lastwagen|kraftwagen|fahrzeug)', l: { nl: 'Ungefähr acht Lastkraftwagen', de: 'Ungefähr acht Lastkraftwagen', en: 'Ungefähr acht Lastkraftwagen' } },
      { f: ['wie'], re: 'marsch|fahr|vormarsch|bewegung|unterwegs|rollen', l: { nl: 'Wat doen ze: auf dem Marsch', de: 'Was tun sie: auf dem Marsch', en: 'What are they doing: auf dem Marsch' } },
      { f: ['wie', 'wo'], re: 'deventer.*twello', l: { nl: 'Weg met twee punten in marsrichting: Deventer – Twello', de: 'Straße mit zwei Punkten in Marschrichtung: Deventer – Twello', en: 'Road named by two points in the direction of march: Deventer – Twello' } }
    ],
    warn: [
      { f: ['wie', 'wo'], re: 'twello.*deventer', not: 'deventer.*twello', l: { nl: 'Noem de weg in de marsrichting: eerst Deventer, dan Twello.', de: 'Nenne die Straße in Marschrichtung: erst Deventer, dann Twello.', en: 'Name the road in the direction of march: Deventer first, then Twello.' } }
    ],
    model: {
      abs: 'Posten, 1. Gruppe', an: '2. Zug', wann: '7. 11. 44, 07⁴⁵',
      wer: 'Drei Panzer und ungefähr acht Lastkraftwagen', wie: 'auf dem Marsch von Deventer nach Twello',
      wo: 'Straße Deventer–Twello', zus: '', sig: 'Piet Visser, Grenadier'
    }
  },
  {
    id: 'ijssel-nacht', blad: 'Wilp',
    t: { nl: 'Nacht aan de IJssel', de: 'Nacht an der Yssel', en: 'Night on the IJssel' },
    sit: {
      nl: 'Je hebt met de Feldwache van de 3. Gruppe (Unteroffizier Mulder) de wacht aan de IJssel. In de nacht van 7 op 8 november 1944, om 02.10 uur, zie je bij maanlicht ongeveer zes vijandelijke soldaten die in rubberboten de IJssel oversteken naar de westoever, 300 meter ten zuiden van de verkeersbrug bij Deventer. Meld aan de 2. Kompanie.',
      de: 'Du stehst mit der Feldwache der 3. Gruppe (Unteroffizier Mulder) an der Yssel. In der Nacht vom 7. zum 8. November 1944, um 02.10 Uhr, siehst du im Mondlicht ungefähr sechs feindliche Soldaten, die in Schlauchbooten über die Yssel auf das Westufer setzen, 300 Meter südlich der Straßenbrücke bei Deventer. Melde an die 2. Kompanie.',
      en: 'You are on guard on the IJssel with the Feldwache of the 3. Gruppe (Unteroffizier Mulder). In the night of 7 to 8 November 1944, at 02:10, you see by moonlight about six enemy soldiers crossing the IJssel in rubber boats to the west bank, 300 metres south of the road bridge at Deventer. Report to the 2. Kompanie.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'feldwache', l: { nl: 'Afzender is de eenheid: Feldwache …', de: 'Absender ist die Einheit: Feldwache …', en: 'Sender is the unit: Feldwache …' } },
      { f: ['an'], re: '\\b2\\b.*(kompanie|kp)|\\b2\\s*\\.\\s*\\/', l: { nl: 'Aan: 2. Kompanie', de: 'An: 2. Kompanie', en: 'To: 2. Kompanie' } },
      { f: ['wann'], re: 'nacht\\s*7\\s*\\.?\\s*\\/\\s*8', l: { nl: 'Nacht geschreven als: Nacht 7./8. 11. 44', de: 'Nacht geschrieben als: Nacht 7./8. 11. 44', en: 'Night written as: Nacht 7./8. 11. 44' } },
      { f: ['wann'], re: '\\b0?2[\\s.:]?10\\b', l: { nl: 'Tijd: 02¹⁰', de: 'Zeit: 02¹⁰', en: 'Time: 02¹⁰' } },
      { f: ['wer'], re: '\\b6\\b|sechs', l: { nl: 'Aantal: ungefähr sechs', de: 'Zahl: ungefähr sechs', en: 'Number: ungefähr sechs' } },
      { f: ['wer'], re: 'mann|soldat|sch[uü]tz|feind', l: { nl: 'Wat: feindliche Soldaten', de: 'Was: feindliche Soldaten', en: 'What: feindliche Soldaten' } },
      { f: ['wer', 'wie'], re: 'über|setz|boot|kahn|queren|quert', l: { nl: 'Wat doen ze: übersetzen in Schlauchbooten', de: 'Was tun sie: Übersetzen in Schlauchbooten', en: 'What are they doing: übersetzen in Schlauchbooten' } },
      { f: ['wo'], re: 'yssel|ijssel|issel', l: { nl: 'Naam rivier: Yssel / IJssel', de: 'Name des Flusses: Yssel', en: 'Name of the river: Yssel / IJssel' } },
      { f: ['wo'], re: 'süd', l: { nl: 'Windrichting: südlich', de: 'Himmelsrichtung: südlich', en: 'Compass direction: südlich' } },
      { f: ['wo'], re: '300|dreihundert', l: { nl: 'Afstand: 300 Meter', de: 'Entfernung: 300 Meter', en: 'Distance: 300 Meter' } },
      { f: ['wo'], re: 'brücke', l: { nl: 'Vast punt: Straßenbrücke Deventer', de: 'Fester Punkt: Straßenbrücke Deventer', en: 'Fixed point: Straßenbrücke Deventer' } }
    ],
    model: {
      abs: 'Feldwache Mulder, 3. Gruppe', an: '2. Kompanie', wann: 'Nacht 7./8. 11. 44, 02¹⁰',
      wer: 'Ungefähr sechs feindliche Soldaten', wie: 'beim Übersetzen in Schlauchbooten auf das Westufer',
      wo: 'Yssel, 300 Meter südlich Straßenbrücke Deventer', zus: 'Bei Mondlicht beobachtet.', sig: 'Kees Mulder, Unteroffizier'
    }
  },
  {
    id: 'voorst-bauer', blad: 'Wilp',
    t: { nl: 'Wat de boer zegt', de: 'Was der Bauer sagt', en: 'What the farmer says' },
    sit: {
      nl: 'Je bent met Spähtrupp De Vries bij Voorst. Op 8 november 1944 om 11.00 uur vertelt een boer je dat er sinds vanochtend twee vijandelijke kanonnen in stelling staan in de boomgaard aan de noordrand van Voorst. Je hebt ze zelf niet gezien. Meld aan de 2. Kompanie.',
      de: 'Du bist mit dem Spähtrupp De Vries bei Voorst. Am 8. November 1944 um 11.00 Uhr erzählt dir ein Bauer, dass seit heute früh zwei feindliche Geschütze im Obstgarten am Nordrand von Voorst in Stellung stehen. Du hast sie nicht selbst gesehen. Melde an die 2. Kompanie.',
      en: 'You are with Spähtrupp De Vries near Voorst. On 8 November 1944 at 11:00 a farmer tells you that since this morning two enemy guns have been in position in the orchard on the northern edge of Voorst. You have not seen them yourself. Report to the 2. Kompanie.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'sp[aä]htrupp', l: { nl: 'Afzender is de eenheid: Spähtrupp …', de: 'Absender ist die Einheit: Spähtrupp …', en: 'Sender is the unit: Spähtrupp …' } },
      { f: ['an'], re: '\\b2\\b.*(kompanie|kp)|\\b2\\s*\\.\\s*\\/', l: { nl: 'Aan: 2. Kompanie', de: 'An: 2. Kompanie', en: 'To: 2. Kompanie' } },
      { f: ['wann'], re: '\\b8\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 8. 11. 44', de: 'Datum: 8. 11. 44', en: 'Date: 8. 11. 44' } },
      { f: ['wann'], re: '\\b11[\\s.:]?00\\b', l: { nl: 'Tijd: 11⁰⁰', de: 'Zeit: 11⁰⁰', en: 'Time: 11⁰⁰' } },
      { f: ['wer'], re: '(\\b2\\b|zwei)[^,;]*(geschütz|kanone|pak|haubitze)', l: { nl: 'Zwei Geschütze', de: 'Zwei Geschütze', en: 'Zwei Geschütze' } },
      { f: ['wer', 'wie'], re: 'stellung', l: { nl: 'Wat doen ze: in Stellung', de: 'Was tun sie: in Stellung', en: 'What are they doing: in Stellung' } },
      { f: ['wo'], re: 'voorst', l: { nl: 'Plaatsnaam: Voorst', de: 'Ortsname: Voorst', en: 'Place name: Voorst' } },
      { f: ['wo'], re: 'nord|nörd', l: { nl: 'Windrichting: Nordrand', de: 'Himmelsrichtung: Nordrand', en: 'Compass direction: Nordrand' } },
      { f: 'alle', re: 'nach aussage|laut |vermutlich|anscheinend|angeblich|bauer|einwohner|zivil|nicht selbst', l: { nl: 'Feit en vermoeden gescheiden: bron noemen („nach Aussage eines Bauern“) of „vermutlich“', de: 'Tatsache und Vermutung getrennt: Quelle nennen („nach Aussage eines Bauern“) oder „vermutlich“', en: 'Fact kept apart from assumption: name the source (“nach Aussage eines Bauern”) or write “vermutlich”' } }
    ],
    model: {
      abs: 'Spähtrupp De Vries', an: '2. Kompanie', wann: '8. 11. 44, 11⁰⁰',
      wer: 'Zwei feindliche Geschütze', wie: 'in Stellung, seit heute früh',
      wo: 'Obstgarten am Nordrand Voorst', zus: 'Nach Aussage eines Bauern, nicht selbst gesehen.', sig: 'Henk de Vries, Obergefreiter'
    }
  },
  {
    id: 'twello-frei', blad: 'Wilp',
    t: { nl: 'Twello is leeg', de: 'Twello ist leer', en: 'Twello is empty' },
    sit: {
      nl: 'Je Spähtrupp (Spähtrupp Jansen) heeft op 8 november 1944 tussen 15.00 en 15.30 uur het dorp Twello doorzocht. Je hebt geen vijand gezien. Volgens de inwoners zijn er sinds gisteren ook geen vijandelijke soldaten in het dorp geweest. Meld om 15.30 uur aan de 2. Kompanie. Ook waar de vijand níet is, is belangrijk!',
      de: 'Dein Spähtrupp (Spähtrupp Jansen) hat am 8. November 1944 zwischen 15.00 und 15.30 Uhr das Dorf Twello durchsucht. Du hast keinen Feind gesehen. Nach Aussage der Einwohner waren seit gestern auch keine feindlichen Soldaten im Dorf. Melde um 15.30 Uhr an die 2. Kompanie. Auch wo der Feind nicht ist, ist wichtig!',
      en: 'Your Spähtrupp (Spähtrupp Jansen) searched the village of Twello on 8 November 1944 between 15:00 and 15:30. You saw no enemy. According to the inhabitants there have been no enemy soldiers in the village since yesterday either. Report at 15:30 to the 2. Kompanie. Where the enemy is not matters too!'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'sp[aä]htrupp', l: { nl: 'Afzender is de eenheid: Spähtrupp …', de: 'Absender ist die Einheit: Spähtrupp …', en: 'Sender is the unit: Spähtrupp …' } },
      { f: ['an'], re: '\\b2\\b.*(kompanie|kp)|\\b2\\s*\\.\\s*\\/', l: { nl: 'Aan: 2. Kompanie', de: 'An: 2. Kompanie', en: 'To: 2. Kompanie' } },
      { f: ['wann'], re: '\\b8\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 8. 11. 44', de: 'Datum: 8. 11. 44', en: 'Date: 8. 11. 44' } },
      { f: ['wann'], re: '\\b15[\\s.:]?30\\b', l: { nl: 'Tijd: 15³⁰', de: 'Zeit: 15³⁰', en: 'Time: 15³⁰' } },
      { f: ['wer', 'wie', 'wo'], re: 'feindfrei|kein(en)? feind|frei vo[mn] feind|vom feind frei|nicht besetzt|unbesetzt', l: { nl: 'Gemeld: feindfrei / kein Feind', de: 'Gemeldet: feindfrei / kein Feind', en: 'Reported: feindfrei / kein Feind' } },
      { f: ['wo'], re: 'twello', l: { nl: 'Plaatsnaam: Twello', de: 'Ortsname: Twello', en: 'Place name: Twello' } },
      { f: 'alle', re: 'nach aussage|laut |einwohner|bewohner|vermutlich|zivil', l: { nl: 'Wat de inwoners zeggen apart, met bron („nach Aussage der Einwohner“)', de: 'Was die Einwohner sagen getrennt, mit Quelle („nach Aussage der Einwohner“)', en: 'What the inhabitants say kept apart, with source (“nach Aussage der Einwohner”)' } }
    ],
    model: {
      abs: 'Spähtrupp Jansen', an: '2. Kompanie', wann: '8. 11. 44, 15³⁰',
      wer: 'Kein Feind', wie: '—',
      wo: 'Twello feindfrei', zus: 'Nach Aussage der Einwohner seit gestern kein Feind im Ort.', sig: 'Willem Jansen, Gefreiter'
    }
  },
  {
    id: 'haaksbergen-sperre', blad: 'Haaksbergen',
    t: { nl: 'Wegversperring bij Haaksbergen', de: 'Straßensperre bei Haaksbergen', en: 'Roadblock near Haaksbergen' },
    sit: {
      nl: 'Je bent met Spähtrupp Smit op pad. Op 9 november 1944 om 09.30 uur zie je vier vijandelijke soldaten die bomen omzagen en een versperring bouwen op de weg van Haaksbergen naar Boekelo, ongeveer 1 kilometer ten noordoosten van Haaksbergen. Meld aan de 3. Kompanie.',
      de: 'Du bist mit dem Spähtrupp Smit unterwegs. Am 9. November 1944 um 09.30 Uhr siehst du vier feindliche Soldaten, die Bäume fällen und eine Sperre auf der Straße von Haaksbergen nach Boekelo bauen, ungefähr 1 Kilometer nordostwärts Haaksbergen. Melde an die 3. Kompanie.',
      en: 'You are out with Spähtrupp Smit. On 9 November 1944 at 09:30 you see four enemy soldiers felling trees and building a barrier on the road from Haaksbergen to Boekelo, about 1 kilometre north-east of Haaksbergen. Report to the 3. Kompanie.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'sp[aä]htrupp', l: { nl: 'Afzender is de eenheid: Spähtrupp …', de: 'Absender ist die Einheit: Spähtrupp …', en: 'Sender is the unit: Spähtrupp …' } },
      { f: ['an'], re: '\\b3\\b.*(kompanie|kp)|\\b3\\s*\\.\\s*\\/', l: { nl: 'Aan: 3. Kompanie', de: 'An: 3. Kompanie', en: 'To: 3. Kompanie' } },
      { f: ['wann'], re: '\\b9\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 9. 11. 44', de: 'Datum: 9. 11. 44', en: 'Date: 9. 11. 44' } },
      { f: ['wann'], re: '\\b0?9[\\s.:]?30\\b', l: { nl: 'Tijd: 09³⁰', de: 'Zeit: 09³⁰', en: 'Time: 09³⁰' } },
      { f: ['wer'], re: '\\b4\\b|vier', l: { nl: 'Precies aantal: vier', de: 'Genaue Zahl: vier', en: 'Exact number: vier' } },
      { f: ['wer'], re: 'mann|soldat|sch[uü]tz|pionier', l: { nl: 'Wat: feindliche Soldaten', de: 'Was: feindliche Soldaten', en: 'What: feindliche Soldaten' } },
      { f: ['wer', 'wie'], re: 'sperr|barrik|baum|bäum|fäll', l: { nl: 'Wat doen ze: beim Anlegen einer (Baum)sperre', de: 'Was tun sie: beim Anlegen einer (Baum)sperre', en: 'What are they doing: beim Anlegen einer (Baum)sperre' } },
      { f: ['wie', 'wo'], re: 'haaksbergen.*boekelo', l: { nl: 'Weg met twee punten: Haaksbergen – Boekelo', de: 'Straße mit zwei Punkten: Haaksbergen – Boekelo', en: 'Road named by two points: Haaksbergen – Boekelo' } },
      { f: ['wo'], re: 'nord\\s*-?\\s*ost|nordöst', l: { nl: 'Windrichting: nordostwärts', de: 'Himmelsrichtung: nordostwärts', en: 'Compass direction: nordostwärts' } },
      { f: ['wo'], re: '\\b1\\s*(km|kilometer)|1000|tausend|ein(en)? kilometer', l: { nl: 'Afstand: 1 km', de: 'Entfernung: 1 km', en: 'Distance: 1 km' } }
    ],
    model: {
      abs: 'Spähtrupp Smit', an: '3. Kompanie', wann: '9. 11. 44, 09³⁰',
      wer: 'Vier feindliche Soldaten', wie: 'beim Anlegen einer Baumsperre auf der Straße Haaksbergen–Boekelo',
      wo: '1 km nordostwärts Haaksbergen, Straße Haaksbergen–Boekelo', zus: '', sig: 'Gerrit Smit, Obergefreiter'
    }
  },
  {
    id: 'isidorushoeve-mg', blad: 'Haaksbergen',
    t: { nl: 'MG aan de bosrand', de: 'MG am Waldrand', en: 'MG at the edge of the wood' },
    sit: {
      nl: 'Je staat op post voor de 1. Gruppe (Grenadier Kok). Op 10 november 1944 om 16.10 uur zie je aan de bosrand, ongeveer 400 meter ten westen van de kerk van Sint Isidorushoeve, een vijandelijk machinegeweer met drie man bediening. Ze zijn bezig hun stelling te camoufleren. Meld aan je Zugführer, de 1. Zug.',
      de: 'Du stehst Posten für die 1. Gruppe (Grenadier Kok). Am 10. November 1944 um 16.10 Uhr siehst du am Waldrand, etwa 400 Meter westlich der Kirche von Sint Isidorushoeve, ein feindliches Maschinengewehr mit drei Mann Bedienung. Sie tarnen gerade ihre Stellung. Melde deinem Zugführer, dem 1. Zug.',
      en: 'You are on sentry duty for the 1. Gruppe (Grenadier Kok). On 10 November 1944 at 16:10 you see at the edge of the wood, about 400 metres west of the church of Sint Isidorushoeve, an enemy machine gun with a crew of three. They are camouflaging their position. Report to your platoon commander, the 1. Zug.'
    },
    form: 'block',
    checks: [
      { f: ['abs'], re: 'posten|gruppe', l: { nl: 'Afzender is de eenheid: Posten, 1. Gruppe', de: 'Absender ist die Einheit: Posten, 1. Gruppe', en: 'Sender is the unit: Posten, 1. Gruppe' } },
      { f: ['an'], re: '\\b1\\b.*zug|zugf', l: { nl: 'Aan: 1. Zug', de: 'An: 1. Zug', en: 'To: 1. Zug' } },
      { f: ['wann'], re: '\\b10\\s*\\.\\s*(11|nov)', l: { nl: 'Datum: 10. 11. 44', de: 'Datum: 10. 11. 44', en: 'Date: 10. 11. 44' } },
      { f: ['wann'], re: '\\b16[\\s.:]?10\\b', l: { nl: 'Tijd: 16¹⁰', de: 'Zeit: 16¹⁰', en: 'Time: 16¹⁰' } },
      { f: ['wer'], re: '\\bmg\\b|maschinengewehr', l: { nl: 'Wat: ein feindliches MG', de: 'Was: ein feindliches MG', en: 'What: ein feindliches MG' } },
      { f: ['wer'], re: '\\b3\\b|drei', l: { nl: 'Bediening: drei Mann', de: 'Bedienung: drei Mann', en: 'Crew: drei Mann' } },
      { f: ['wer', 'wie'], re: 'tarn', l: { nl: 'Wat doen ze: beim Tarnen', de: 'Was tun sie: beim Tarnen', en: 'What are they doing: beim Tarnen' } },
      { f: ['wo'], re: 'isidorus', l: { nl: 'Plaatsnaam volledig: Sint Isidorushoeve', de: 'Ortsname voll: Sint Isidorushoeve', en: 'Full place name: Sint Isidorushoeve' } },
      { f: ['wo'], re: 'west', l: { nl: 'Windrichting: westlich', de: 'Himmelsrichtung: westlich', en: 'Compass direction: westlich' } },
      { f: ['wo'], re: '400|vierhundert', l: { nl: 'Afstand: 400 Meter', de: 'Entfernung: 400 Meter', en: 'Distance: 400 Meter' } },
      { f: ['wo'], re: 'wald', l: { nl: 'Terrein: Waldrand', de: 'Gelände: Waldrand', en: 'Terrain: Waldrand' } }
    ],
    model: {
      abs: 'Posten, 1. Gruppe', an: '1. Zug', wann: '10. 11. 44, 16¹⁰',
      wer: 'Ein feindliches MG, drei Mann Bedienung', wie: 'beim Tarnen der Stellung',
      wo: 'Waldrand 400 Meter westlich Kirche Sint Isidorushoeve', zus: '', sig: 'Dirk Kok, Grenadier'
    }
  },
  {
    id: 'boekelo-kurz', blad: 'Haaksbergen',
    t: { nl: 'Kort en mondeling', de: 'Kurz und mündlich', en: 'Short and spoken' },
    sit: {
      nl: 'Je ligt met je Spähtrupp aan de noordrand van Boekelo. Je ziet een vijandelijke verkenningspatrouille op ongeveer 900 meter. Met de Marschkompaß meet je de richting: 10 (Teilstriche). Geef je Gruppenführer een korte mondelinge melding. Bij een Spähtrupp noem je ook je eigen standplaats.',
      de: 'Du liegst mit deinem Spähtrupp am Nordrand von Boekelo. Du siehst einen feindlichen Spähtrupp auf ungefähr 900 Meter. Mit dem Marschkompaß misst du die Richtung: 10 (Teilstriche). Gib deinem Gruppenführer eine kurze mündliche Meldung. Beim Spähtrupp nennst du auch deinen eigenen Standpunkt.',
      en: 'You are lying with your Spähtrupp on the northern edge of Boekelo. You see an enemy reconnaissance patrol at about 900 metres. With the Marschkompaß you measure the direction: 10 (Teilstriche). Give your Gruppenführer a short spoken report. On a Spähtrupp you also give your own position.'
    },
    form: 'kurz',
    checks: [
      { f: ['kurz'], re: 'sp[aä]htrupp|patrouille', l: { nl: 'Wat: feindlicher Spähtrupp', de: 'Was: feindlicher Spähtrupp', en: 'What: feindlicher Spähtrupp' } },
      { f: ['kurz'], re: '900|neunhundert', l: { nl: 'Afstand: 900 Meter', de: 'Entfernung: 900 Meter', en: 'Distance: 900 Meter' } },
      { f: ['kurz'], re: '\\bin\\s*10\\b|richtung\\s*10\\b|\\b10\\s*teilstrich', l: { nl: 'Richting als Teilstriche: „in 10“', de: 'Richtung in Teilstrichen: „in 10“', en: 'Direction in Teilstriche: “in 10”' } },
      { f: ['kurz'], re: 'boekelo', l: { nl: 'Eigen standplaats: Nordrand Boekelo', de: 'Eigener Standpunkt: Nordrand Boekelo', en: 'Own position: Nordrand Boekelo' } }
    ],
    model: { kurz: 'Feindlicher Spähtrupp 900 Meter in 10. Eigener Standpunkt Nordrand Boekelo.' }
  }
];
