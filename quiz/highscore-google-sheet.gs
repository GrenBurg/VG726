/**
 * VG726 — highscorelijst voor de quiz
 *
 * Dit script hoort bij een Google Sheet en bewaart de ingevoerde scores.
 * Instellen (eenmalig, ongeveer 5 minuten):
 *  1. Maak een nieuwe Google Sheet, bijvoorbeeld "VG726 Quiz Highscores".
 *  2. Menu Extensies → Apps Script. Wis wat er staat en plak dit hele bestand erin. Opslaan.
 *  3. Rechtsboven: Implementeren → Nieuwe implementatie → type "Web-app".
 *       Uitvoeren als: Ik
 *       Wie heeft toegang: Iedereen
 *     Klik Implementeren en geef toestemming met je Google-account.
 *  4. Kopieer de Web-app-URL (eindigt op /exec) en zet die in quiz/highscore-adres.js.
 *
 * Beheren: de scores staan in het tabblad "Highscores". Een regel wissen = van de lijst af.
 * Na een wijziging in dit script: Implementeren → Implementaties beheren → bewerken → Nieuwe versie.
 */

const TAB = 'Highscores';
const MAX_SCORE = 60;      // 6 onderdelen × 10 vragen
const TOP = 25;            // zoveel namen gaan terug naar de site

function tab_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(TAB);
  if (!sh) {
    sh = ss.insertSheet(TAB);
    sh.appendRow(['Naam', 'Score', 'Datum', 'Per onderdeel']);
    sh.setFrozenRows(1);
  }
  return sh;
}

// Beste score per naam, hoogste eerst; bij gelijke score wie het eerst was.
function lijst_() {
  const rows = tab_().getDataRange().getValues().slice(1);
  const best = {};
  rows.forEach(function (r) {
    const naam = String(r[0] || '').trim(), score = Number(r[1]), datum = r[2] instanceof Date ? r[2].getTime() : 0;
    if (!naam || !isFinite(score)) return;
    const k = naam.toLowerCase();
    if (!best[k] || score > best[k].score || (score === best[k].score && datum < best[k].t)) best[k] = { naam: naam, score: score, t: datum };
  });
  return Object.keys(best).map(function (k) { return best[k]; })
    .sort(function (a, b) { return b.score - a.score || a.t - b.t; })
    .slice(0, TOP)
    .map(function (x) { return { naam: x.naam, score: x.score }; });
}

function antwoord_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// Lijst opvragen
function doGet() {
  return antwoord_({ ok: true, list: lijst_() });
}

// Score invoeren: { naam, score, detail }
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const naam = String(d.naam || '').replace(/\s+/g, ' ').replace(/[<>]/g, '').trim().slice(0, 24);
    const score = Math.round(Number(d.score));
    if (!naam) return antwoord_({ ok: false, error: 'naam' });
    if (!isFinite(score) || score < 0 || score > MAX_SCORE) return antwoord_({ ok: false, error: 'score' });
    // eenvoudige rem: niet vaker dan eens per 3 seconden
    const props = PropertiesService.getScriptProperties(), nu = Date.now(), vorige = Number(props.getProperty('laatste') || 0);
    if (nu - vorige < 3000) return antwoord_({ ok: false, error: 'te snel' });
    props.setProperty('laatste', String(nu));
    tab_().appendRow([naam, score, new Date(), JSON.stringify(d.detail || {})]);
    return antwoord_({ ok: true, list: lijst_() });
  } catch (err) {
    return antwoord_({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (x) {}
  }
}
