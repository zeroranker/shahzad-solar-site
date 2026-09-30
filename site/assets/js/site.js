/* ============================================================================
   SHAHZAD SOLAR — site behaviour
   ~9 KB unminified. No framework, no dependencies, no trackers.

   Contents
     1. Nav (mobile) + language preference
     2. The Solar Day lab  — 24h curve + net-billing arithmetic
     3. Buyer-protection checklist (progress, persisted)
     4. Contact form (progressive, no backend required)
     5. Small utilities
   ========================================================================= */
(function () {
  'use strict';

  /* ------------------------------------------- 0. release the web fonts
     The Google Fonts link ships with media="print" so it never blocks the
     first paint; something then flips it to media="all" to actually fetch the
     fonts. That used to be an inline onload="this.media='all'" attribute,
     which is an inline event handler and is therefore covered by script-src.
     A strict CSP silently blocked it: the link stayed media="print", the
     fonts never loaded, and the site lost its typographic identity in
     production while looking fine on a dev server that sends no policy.

     This script is deferred, so it runs after the document is parsed but
     before DOMContentLoaded — earlier than the load event the old handler
     waited for. The <noscript> block in the markup still carries a plain
     stylesheet link for readers without JavaScript. */
  Array.prototype.forEach.call(
    document.querySelectorAll('link[rel="stylesheet"][media="print"]'),
    function (l) { l.media = 'all'; }
  );

  /* ------------------------------------------------ 1. nav + language */
  var nav = document.querySelector('[data-nav]');
  var navBtn = document.querySelector('[data-nav-toggle]');
  if (nav && navBtn) {
    navBtn.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      navBtn.setAttribute('aria-expanded', String(!open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.setAttribute('data-open', 'false');
        navBtn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
        nav.setAttribute('data-open', 'false');
        navBtn.setAttribute('aria-expanded', 'false');
        navBtn.focus();
      }
    });
  }

  /* Preferred language is remembered, but the URL always wins so that a
     shared link lands in the right language. */
  try {
    var pref = localStorage.getItem('ss-lang');
    if (pref && !document.documentElement.getAttribute('data-lang-locked')) {
      var here = document.documentElement.lang === 'ur' ? '/ur/' : '/en/';
      if (pref === 'ur' && here === '/en/') { /* only redirect from the neutral root */ }
    }
  } catch (e) { /* storage blocked — the toggle still works, it just won't persist */ }

  /* ------------------------------------------------------- utilities */
  function fmt(n, d) {
    return new Intl.NumberFormat('en-PK', {
      minimumFractionDigits: d || 0, maximumFractionDigits: d === undefined ? 0 : d
    }).format(n);
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ==================================================== 2. THE SOLAR DAY
     The point of this tool is to make one idea visible:
     under net billing, the kWh you use yourself is worth the full retail
     tariff, and the kWh you export is worth far less. Sizing and load
     shape matter more than panel count.

     Assumptions are stated on-screen and sourced in the page footer.
     ==================================================================== */
  var lab = document.querySelector('[data-daylab]');
  if (lab) {
    /* The same tool runs on the Urdu pages. Every string it writes has to
       come out in the reader's language, not in English with a number in it. */
    var UR = document.documentElement.getAttribute('lang') === 'ur';
    var T = UR ? {
      units: ' یونٹ',
      rs: 'روپے ',
      season: { summer: 'گرمی', winter: 'سردی' },
      lead: 'ایک ماہ میں یہ نظام تقریباً <b>',
      leadMid: '</b> یونٹ بناتا ہے۔ ان میں سے <b>',
      leadPct: '</b> فیصد آپ خود استعمال کرتے ہیں، اور <b>',
      leadExp: '</b> یونٹ محض 11 روپے یونٹ میں بکتے ہیں جب کہ آپ گھر 47.20 روپے یونٹ میں خریدتے ہیں۔ ',
      good: 'یہ نیٹ بلنگ کا بہترین معاملہ ہے: تقریباً پوری پیداوار آپ کے ٹیاریف کے پورے قیمت سے بچ جاتی ہے، اور برآمد کی قیمت سے کوئی زیادہ فرق نہیں پڑتا۔',
      mid: 'یہ چل سکتا ہے۔ مگر <b>',
      midEnd: '</b> پیداوار تقریباً ایک چوتھائی پر بک رہی ہے۔ ایک بیٹری، یا تھوڑا چھوٹا نظام، اس پورے فرق کو واپس لے سکتا ہے۔',
      bad: 'اِن اعداد کے تحت یہ ایک <em>برآمدی</em> نظام ہے، اور برآمد کی قیمت ہی وہ چیز ہے جسے نیٹ بلنگ نے بند کر دی ہے۔ چھوٹا نظام، یا دن کے وقت زیادہ چلنے والی لوڈ کے ساتھ جوڑا گیا نظام، آپ کے لیے زیادہ قیمتی ہوگا۔'
    } : {
      units: ' units', rs: 'Rs ',
      season: { summer: 'summer', winter: 'winter' }
    };

    var svg = lab.querySelector('[data-chart]');
    var W = 720, H = 300, PADL = 46, PADR = 16, PADT = 18, PADB = 34;
    var iw = W - PADL - PADR, ih = H - PADT - PADB;

    /* --- load shapes, normalised to 1.0 at their own peak -------------- */
    var LOADS = {
      home: { label: 'Home', peak: 12, shape: [0,0,0,0,.02,.05,.14,.26,.38,.44,.5,.55,.58,.56,.52,.5,.52,.58,.66,.72,.7,.58,.4,.2,.06,0] },
      shop: { label: 'Shop / office', peak: 14, shape: [0,0,0,0,.02,.06,.2,.4,.62,.78,.88,.94,1,.98,.95,.93,.9,.86,.7,.5,.3,.14,.05,0,0,0] },
      mill: { label: 'Factory (3-shift)', peak: 16, shape: [.62,.64,.66,.66,.66,.68,.74,.86,.96,1,1,1,1,1,1,.99,.97,.96,.94,.92,.88,.84,.78,.72,.68,.65] }
    };
    /* --- generation: a bell from ~06:30 to ~19:00, scaled by season ----
       Width is chosen so that one kW of installed capacity yields about
       4.2 kWh across a day, which is Faisalabad's realistic figure. The
       shape is deliberately sharper than a wide Gaussian: real irradiance
       is not a plateau. */
    function genShape(mult) {
      var out = [], peak = 12.75, width = 1.85;
      for (var h = 0; h < 24; h++) {
        var v = Math.exp(-Math.pow(h - peak, 2) / (2 * width * width));
        out.push(Math.max(0, v) * mult);
      }
      return out;
    }
    var SEASONS = {
      summer: { label: 'Summer', mult: 1.0, factor: 1.0, days: 30 },
      winter: { label: 'Winter', mult: 0.62, factor: 0.62, days: 30 }
    };
    /* --- FESCO column D, effective 12 Feb 2026 (Rs/kWh) ----------------- */
    var RATES = {
      res700:  { label: 'Home, unprotected >700 units', rate: 47.20 },
      res400:  { label: 'Home, unprotected 301–400 units', rate: 36.46 },
      res100:  { label: 'Home, unprotected 001–100 units', rate: 22.44 },
      comm:    { label: 'Commercial ≥5 kW', rate: 39.76 },
      ind:     { label: 'Industrial B2, 25–500 kW', rate: 24.16 },
      agri:    { label: 'Agricultural tubewell', rate: 28.90 }
    };
    var EXPORT_RATE = 11;   /* Power Division via The News, 10 Feb 2026 — a formula, not a fixed price */
    var KWH_PER_KW_DAY = 4.2; /* middle of Faisalabad's ~4–5 peak-sun-hour range */

    /* The bell's shape is fixed; only its amplitude moves with system size and
       season. Deriving the amplitude from KWH_PER_KW_DAY and the bell's own sum
       means the yield stated on screen and the yield the model computes are the
       same number by construction — they cannot drift apart. */
    var GEN_SHAPE_SUM = genShape(1).reduce(function (a, b) { return a + b; }, 0);
    var GEN_AMPLITUDE = KWH_PER_KW_DAY / GEN_SHAPE_SUM; /* kW at solar noon, per kW installed */

    var state = { kw: 5, usage: 400, profile: 'home', season: 'summer', rate: 'res700' };

    var elKw = lab.querySelector('[data-ctl="kw"]');
    var elUse = lab.querySelector('[data-ctl="usage"]');
    var elRate = lab.querySelector('[data-ctl="rate"]');
    var outGen = lab.querySelector('[data-out="gen"]');
    var outSelf = lab.querySelector('[data-out="self"]');
    var outExp = lab.querySelector('[data-out="export"]');
    var outOld = lab.querySelector('[data-out="old"]');
    var outNew = lab.querySelector('[data-out="new"]');
    var outDelta = lab.querySelector('[data-out="delta"]');
    var outVerdict = lab.querySelector('[data-out="verdict"]');

    function x(h) { return PADL + (h / 24) * iw; }
    function y(v, max) { return PADT + ih - (v / max) * ih; }

    function line(pts) {
      return pts.map(function (p, i) { return (i ? 'L' : 'M') + x(p[0]).toFixed(1) + ' ' + y(p[1], max).toFixed(1); }).join(' ');
    }

    var max = 10;

    function render() {
      var load = LOADS[state.profile].shape;
      var cons = state.usage / 30 / 24;               /* kWh per hour */
      var genMult = state.kw * GEN_AMPLITUDE * SEASONS[state.season].mult; /* kW at solar noon */
      var gen = genShape(genMult);
      var loadAbs = load.map(function (f) { return f * cons; });

      max = Math.max(1, Math.max.apply(null, gen), Math.max.apply(null, loadAbs)) * 1.16;

      var parts = [];

      /* grid bands */
      [0, 6, 12, 18, 24].forEach(function (t) {
        parts.push('<line x1="' + x(t) + '" y1="' + PADT + '" x2="' + x(t) + '" y2="' + (PADT + ih) +
          '" stroke="var(--rule-chart)" stroke-width="1"/>');
        parts.push('<text x="' + x(t) + '" y="' + (H - 12) + '" text-anchor="middle" ' +
          'font-size="11" fill="var(--text-2)" font-family="var(--mono)">' +
          (t === 24 ? '24:00' : String(t).padStart(2, '0') + ':00') + '</text>');
      });
      parts.push('<line x1="' + PADL + '" y1="' + (PADT + ih) + '" x2="' + (W - PADR) + '" y2="' + (PADT + ih) +
        '" stroke="var(--rule-chart)" stroke-width="1"/>');

      /* surplus band: generation above load, hour by hour — this is the part
         that now earns ~Rs 11 instead of the full retail tariff. */
      var band = [];
      for (var h = 0; h < 24; h++) {
        var top = gen[h], bot = loadAbs[h];
        band.push([h, Math.max(bot, top)]);
      }
      for (var h2 = 24; h2 >= 0; h2--) band.push([h2, Math.min(loadAbs[h2 % 24], gen[h2 % 24])]);
      parts.push('<path d="' + line(band) + ' Z" fill="var(--signal)" opacity="0.13"/>');

      /* load area */
      var loadPts = loadAbs.map(function (v, i) { return [i, v]; });
      parts.push('<path d="' + line(loadPts) + ' L' + x(24) + ' ' + (PADT + ih) + ' L' + x(0) + ' ' + (PADT + ih) +
        ' Z" fill="var(--ink-3)" opacity="0.08"/>');

      /* curves */
      parts.push('<path d="' + line(gen.map(function (v, i) { return [i, v]; })) +
        '" fill="none" stroke="var(--sun-deep)" stroke-width="2.5" stroke-linejoin="round"/>');
      parts.push('<path d="' + line(loadPts) +
        '" fill="none" stroke="var(--ink)" stroke-width="2" stroke-dasharray="5 4" stroke-linejoin="round"/>');

      /* y axis */
      [0, 0.5, 1].forEach(function (t) {
        var v = max * t;
        parts.push('<text x="' + (PADL - 8) + '" y="' + (y(v, max) + 4) + '" text-anchor="end" ' +
          'font-size="11" fill="var(--text-2)" font-family="var(--mono)">' + v.toFixed(1) + '</text>');
      });

      svg.innerHTML = parts.join('');

      /* ---- the arithmetic -------------------------------------------
         The chart loop sums 24 hours, so these start out as DAILY figures.
         Everything a customer compares against a bill is monthly. */
      var dGen = 0, dSelf = 0, dExp = 0;
      for (var k = 0; k < 24; k++) {
        var g = gen[k], l = loadAbs[k];
        var used = Math.min(g, l);
        dSelf += used; dExp += (g - used); dGen += g;
      }
      var DAYS = 30;
      var mGen = dGen * DAYS, mSelf = dSelf * DAYS, mExp = dExp * DAYS;

      var retail = RATES[state.rate].rate;
      var underOld = mGen * retail;                      /* every kWh cancelled retail */
      var underNew = mSelf * retail + mExp * EXPORT_RATE; /* split pricing */
      var delta = underOld - underNew;

      if (outGen) outGen.textContent = fmt(mGen) + T.units;
      if (outSelf) outSelf.textContent = fmt(mSelf) + T.units;
      if (outExp) outExp.textContent = fmt(mExp) + T.units;
      if (outOld) outOld.textContent = T.rs + fmt(underOld);
      if (outNew) outNew.textContent = T.rs + fmt(underNew);
      if (outDelta) {
        outDelta.textContent = delta >= 0 ? T.rs + fmt(delta) : T.rs + '0';
        /* Logical property, not border-left: on the Urdu pages the accent
           belongs on the reading-start edge, which is the right. */
        outDelta.parentElement.style.borderInlineStartColor =
          delta > mGen * retail * 0.2 ? 'var(--signal)' : 'var(--good)';
      }
      if (outVerdict) {
        var pct = mGen ? Math.round(mSelf / mGen * 100) : 0;
        var season = T.season[state.season === 'summer' ? 'summer' : 'winter'];
        if (UR) {
          var leadU = T.lead + fmt(mGen) + ' ' + season + T.leadMid + pct + T.leadPct +
                      fmt(mExp) + T.leadExp;
          outVerdict.innerHTML =
            pct >= 80 ? leadU + T.good :
            pct >= 45 ? leadU + T.mid + Math.round(100 - pct) + T.midEnd :
                        leadU + T.bad;
        } else {
          var lead = 'Over a month this array makes about <b>' + fmt(mGen) + ' units</b> in ' +
                     season + '. <b>' + pct + '%</b> of that is used on site, and <b>' +
                     fmt(mExp) + ' units</b> are sold at about Rs 11 instead of Rs ' +
                     retail.toFixed(2) + '. ';
          outVerdict.innerHTML =
            pct >= 80 ? lead + 'That is the good case under net billing: nearly all of your generation still displaces the full retail tariff, and the export price barely matters.' :
            pct >= 45 ? lead + 'That is workable. But <b>' + Math.round(100 - pct) + '%</b> of output is sold at roughly a quarter of what you pay. A battery, or a somewhat smaller array, would recover much of that gap.' :
                        lead + 'On these settings this is an <em>export</em> system, and export is exactly what net billing stopped paying properly for. A smaller array, or one matched to a load that runs harder in daylight, will be worth more to you.';
        }
      }
    }

    function bind(name) {
      lab.querySelectorAll('[data-seg="' + name + '"] button').forEach(function (b) {
        b.addEventListener('click', function () {
          lab.querySelectorAll('[data-seg="' + name + '"] button').forEach(function (o) {
            o.setAttribute('aria-pressed', String(o === b));
          });
          state[name] = b.dataset.val;
          render();
        });
      });
    }
    bind('profile');
    bind('season');

    if (elKw) elKw.addEventListener('input', function () { state.kw = +elKw.value; syncOut(); render(); });
    if (elUse) elUse.addEventListener('input', function () { state.usage = +elUse.value; syncOut(); render(); });
    if (elRate) elRate.addEventListener('change', function () { state.rate = elRate.value; render(); });
    function syncOut() {
      var a = lab.querySelector('[data-out="kw"]'), b = lab.querySelector('[data-out="usage"]');
      if (a) a.textContent = elKw.value + ' kW';
      if (b) b.textContent = elUse.value + (UR ? ' یونٹ فی ماہ' : ' units/month');
    }
    syncOut();
    render();
  }

  /* ============================================== 3. buyer checklist */
  var cl = document.querySelector('[data-checklist]');
  if (cl) {
    var clUr = document.documentElement.getAttribute('lang') === 'ur';
    var boxes = cl.querySelectorAll('input[type="checkbox"]');
    var bar = cl.parentElement.querySelector('[data-progress-bar]');
    var txt = cl.parentElement.querySelector('[data-progress-text]');
    var reset = cl.parentElement.querySelector('[data-checklist-reset]');
    var KEY = 'ss-checklist-v1';

    function paint() {
      var done = 0;
      boxes.forEach(function (b) { if (b.checked) done++; });
      if (bar) bar.style.width = (boxes.length ? done / boxes.length * 100 : 0) + '%';
      if (txt) txt.textContent = clUr
        ? done + ' میں سے ' + boxes.length + ' پر نشان لگا'
        : done + ' of ' + boxes.length + ' checked';
      /* Keep the progressbar's value in step with the bar we just resized. */
      var track = bar && bar.parentElement;
      if (track && track.hasAttribute('role')) {
        track.setAttribute('aria-valuenow', String(done));
        track.setAttribute('aria-valuetext', txt ? txt.textContent : done + ' of ' + boxes.length);
      }
      try { localStorage.setItem(KEY, JSON.stringify(boxesToArray())); } catch (e) {}
    }
    function boxesToArray() {
      return Array.prototype.map.call(boxes, function (b) { return b.checked; });
    }
    function loadState() {
      try {
        var raw = JSON.parse(localStorage.getItem(KEY) || 'null');
        if (Array.isArray(raw)) boxes.forEach(function (b, i) { if (raw[i]) b.checked = true; });
      } catch (e) {}
      paint();
    }
    boxes.forEach(function (b) { b.addEventListener('change', paint); });
    if (reset) reset.addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; });
      try { localStorage.removeItem(KEY); } catch (e) {}
      paint();
    });
    loadState();
  }

  /* ================================================== 4. contact form */
  document.querySelectorAll('[data-form]').forEach(function (form) {
    var status = form.querySelector('[data-form-status]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      /* No backend is wired up. Rather than pretend a message was sent, we
         hand the visitor a fully composed WhatsApp message — the channel
         this market actually closes on — and say plainly what happened. */
      var d = new FormData(form);
      var name = (d.get('name') || '').toString().trim();
      var cat = (d.get('category') || '').toString();
      var kw = (d.get('kw') || '').toString().trim();
      var msg = (d.get('message') || '').toString().trim();
      var phone = (d.get('phone') || '').toString().trim();
      var when = (d.get('when') || '').toString();

      var lines = ['Assalam-o-Alaikum, I found your website.', ''];
      if (name) lines.push('My name is ' + name + '.');
      if (cat) lines.push('I am enquiring about: ' + cat.replace(/-/g, ' ') + '.');
      if (kw) lines.push('Approximate system size: ' + kw + ' kW.');
      if (when) lines.push('Preferred contact time: ' + when + '.');
      if (phone) lines.push('My number: ' + phone + '.');
      if (msg) lines.push('', msg);
      lines.push('', 'Sent from the Shahzad Solar website.');

      var wa = form.getAttribute('data-wa') || '923474666664';
      var url = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(lines.join('\n'));

      if (status) {
        var fUr = document.documentElement.getAttribute('lang') === 'ur';
        status.setAttribute('data-state', 'ok');
        status.innerHTML = fUr
          ? 'آپ کا پیغام تیار ہے۔ <b>اس فارم کے پیچھے کوئی سرور نہیں ہے</b>، اس لیے کچھ ' +
            'بھیجا یا محفوظ نہیں ہوا &#8212; نیچے والا بٹن واٹس ایپ کھولتا ہے جس میں آپ کا لکھا ' +
            'ہوا سب پہلے سے بھرا ہوگا۔ وہاں بھیجیں، یہ براہِ راست ہمیں پہنچ جائے گا۔'
          : 'Your message is ready. <b>This site has no server behind the form</b>, so ' +
            'nothing was sent or stored — the button below opens WhatsApp with everything you typed already filled in. ' +
            'Tap send there and it reaches the team directly.';
      }
      var go = form.querySelector('[data-form-go]');
      if (go) { go.href = url; go.hidden = false; }
    });
  });

  /* ==================================================== 5. small utils */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = String(new Date().getFullYear());

  /* Print was an inline onclick="window.print()" on the checklist — the only
     inline event handler anywhere in a body. Moved here so the site stays
     free of inline script, which is what a strict Content-Security-Policy
     without 'unsafe-inline' would demand. */
  document.querySelectorAll('[data-print]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });
})();
