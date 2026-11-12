/* VG726 — taalwissel NL / DE / EN
 *
 * Gebruik in een pagina:
 *   <script src="../i18n.js"></script>
 *   <script>VG726.add({ de:{ "Nederlandse tekst":"Deutscher Text" }, en:{ ... } })</script>
 *
 * - Elementen met data-i18n krijgen hun vertaling; de sleutel is de Nederlandse
 *   inhoud zelf (spaties samengevoegd), of de waarde van data-i18n als die gevuld is.
 * - data-i18n-attr="alt,title,aria-label,placeholder" vertaalt die attributen.
 * - In JavaScript: VG726.t("Nederlandse tekst"), VG726.lang, en het event
 *   "vg726:lang" op window om opnieuw te tekenen na een taalwissel.
 * - Vlaggetjes komen rechtsboven, of in een element met id="vg-lang" als dat bestaat.
 *   <body data-no-flags> zet ze uit.
 */
(function () {
  var KEY = 'vg726.lang', LANGS = ['nl', 'de', 'en'];
  var NAMES = { nl: 'Nederlands', de: 'Deutsch', en: 'English' };
  var lang = 'nl';
  try { var s = localStorage.getItem(KEY); if (LANGS.indexOf(s) >= 0) lang = s; } catch (e) {}

  var dicts = { de: {}, en: {} };
  var missing = {};
  var norm = function (s) { return String(s).replace(/\s+/g, ' ').trim(); };

  function t(nl) {
    if (lang === 'nl' || nl == null) return nl;
    var k = norm(nl), d = dicts[lang];
    if (!k) return nl;
    if (Object.prototype.hasOwnProperty.call(d, k)) return d[k];
    missing[lang + '|' + k] = 1;
    return nl;
  }

  // originele (Nederlandse) inhoud per element bewaren
  var ORIG = '__vgOrig', ORIGA = '__vgOrigAttr';
  function apply(root) {
    root = root || document;
    var els = root.querySelectorAll('[data-i18n]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el[ORIG] == null) el[ORIG] = el.innerHTML;
      var key = el.getAttribute('data-i18n') || el[ORIG];
      var out = lang === 'nl' ? el[ORIG] : t(key);
      if (out === key && lang !== 'nl') out = el[ORIG];
      if (el.innerHTML !== out) el.innerHTML = out;
    }
    var ats = root.querySelectorAll('[data-i18n-attr]');
    for (var j = 0; j < ats.length; j++) {
      var a = ats[j];
      if (!a[ORIGA]) a[ORIGA] = {};
      var names = a.getAttribute('data-i18n-attr').split(',');
      for (var n = 0; n < names.length; n++) {
        var nm = names[n].trim(); if (!nm) continue;
        if (a[ORIGA][nm] == null) a[ORIGA][nm] = a.getAttribute(nm) || '';
        a.setAttribute(nm, lang === 'nl' ? a[ORIGA][nm] : t(a[ORIGA][nm]));
      }
    }
    document.documentElement.lang = lang;
  }

  function add(d) {
    for (var l in d) {
      if (!dicts[l]) continue;
      for (var k in d[l]) dicts[l][norm(k)] = d[l][k];
    }
  }

  function set(l) {
    if (LANGS.indexOf(l) < 0 || l === lang) return;
    lang = l;
    try { localStorage.setItem(KEY, l); } catch (e) {}
    api.lang = l;
    apply();
    paintFlags();
    try { window.dispatchEvent(new CustomEvent('vg726:lang', { detail: { lang: l } })); } catch (e) {}
  }

  /* ---------- vlaggetjes ---------- */
  var FLAGS = {
    nl: '<svg viewBox="0 0 9 6"><rect width="9" height="6" fill="#21468B"/><rect width="9" height="4" fill="#fff"/><rect width="9" height="2" fill="#AE1C28"/></svg>',
    de: '<svg viewBox="0 0 5 3"><rect width="5" height="3" fill="#FFCE00"/><rect width="5" height="2" fill="#DD0000"/><rect width="5" height="1" fill="#000"/></svg>',
    en: '<svg viewBox="0 0 60 30"><clipPath id="vgUkS"><path d="M0 0v30h60V0z"/></clipPath><clipPath id="vgUkT"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#vgUkS)"><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#vgUkT)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></g></svg>'
  };
  var box = null;
  function buildFlags() {
    if (document.body.hasAttribute('data-no-flags')) return;
    var st = document.createElement('style');
    st.textContent =
      '.vg-lang{display:flex;gap:6px;align-items:center;z-index:1000}' +
      '.vg-lang.vg-float{position:absolute;top:12px;right:14px}' +
      '.vg-lang button{all:unset;cursor:pointer;display:block;width:28px;height:19px;padding:2px;border:1px solid transparent;opacity:.5;transition:opacity .15s,border-color .15s;line-height:0}' +
      '.vg-lang button:hover{opacity:.85}' +
      '.vg-lang button[aria-pressed="true"]{opacity:1;border-color:rgba(36,35,29,.55)}' +
      '.vg-lang button:focus-visible{outline:2px solid #8e2316;outline-offset:1px}' +
      '.vg-lang svg{width:100%;height:100%;display:block;box-shadow:0 0 0 1px rgba(0,0,0,.18)}' +
      '@media print{.vg-lang{display:none}}';
    document.head.appendChild(st);
    box = document.getElementById('vg-lang');
    if (!box) {
      box = document.createElement('div');
      box.className = 'vg-float';
      if (getComputedStyle(document.body).position === 'static') document.body.style.position = 'relative';
      document.body.appendChild(box);
    }
    box.classList.add('vg-lang');
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', 'Taal / Sprache / Language');
    LANGS.forEach(function (l) {
      var b = document.createElement('button');
      b.type = 'button'; b.dataset.lang = l;
      b.title = NAMES[l]; b.setAttribute('aria-label', NAMES[l]);
      b.innerHTML = FLAGS[l];
      b.addEventListener('click', function () { set(l); });
      box.appendChild(b);
    });
    paintFlags();
  }
  function paintFlags() {
    if (!box) return;
    var bs = box.querySelectorAll('button');
    for (var i = 0; i < bs.length; i++) bs[i].setAttribute('aria-pressed', bs[i].dataset.lang === lang ? 'true' : 'false');
  }

  var api = window.VG726 = {
    lang: lang, t: t, add: add, apply: apply, set: set,
    missing: function () { return Object.keys(missing); }
  };

  function init() { buildFlags(); apply(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
