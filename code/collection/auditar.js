/* ============================================================================
 *  AUDITOR WCAG + PRIVACIDAD DE SITIOS WEB UNIVERSITARIOS
 *  ---------------------------------------------------------------------------
 *  Recolecta, para cada universidad de "universidades.json", evidencia REAL y
 *  reproducible del cumplimiento de accesibilidad (WCAG 2.1/2.2 con axe-core)
 *  y del comportamiento de cookies ANTES de cualquier consentimiento.
 *
 *  No inventa nada: todo sale del navegador real cargando cada sitio.
 *  Escribe los resultados de forma incremental (resistente a cortes) en:
 *      - resultados.json  (detalle completo, fuente de verdad)
 *      - resultados.csv   (resumen para vista rapida)
 *
 *  Es REANUDABLE: si se corta, al volver a ejecutarlo continua donde quedo.
 *
 *  Uso (ver LEEME.txt):   node auditar.js
 * ==========================================================================*/

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// --------------------------- Configuracion ---------------------------------
const ESPERA_JS_MS   = 4000;   // tiempo para que carguen scripts / CMP
const TIMEOUT_MS     = 45000;  // timeout de carga por sitio
const REINTENTOS     = 1;      // reintentos si falla la carga
const INCLUIR_AAA    = true;   // incluir criterios nivel AAA en el analisis
const MEDIR_COOKIES  = true;   // true = re-mide cookies/CMP/banner en la misma pasada
                               // (recomendado: mismo metodo y fecha que la accesibilidad).
                               // Ponlo en false si prefieres NO repetir la parte de cookies.
const ARCHIVO_LISTA  = 'universidades.json';
const SALIDA_JSON     = 'resultados.json';
const SALIDA_CSV      = 'resultados.csv';

// --------------------------- Utilidades ------------------------------------
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// Cookies consideradas de rastreo (analitica / marketing / fingerprint)
const RASTREO = [
  /^_ga/, /^_gid$/, /^__utm/, /^_gcl_au$/, /^_gac_/,      // Google Analytics/Ads
  /^_fbp$/, /^_fbc$/, /^fr$/,                              // Meta / Facebook
  /^_tt_/, /^_ttp$/,                                       // TikTok
  /^_clck$/, /^_clsk$/, /^MUID$/,                          // Microsoft Clarity/Bing
  /^_hj/, /^_uet/,                                         // Hotjar / Bing UET
  /^nmstat$/, /^_pk_/, /^pys/, /^_pin_/,                   // Siteimprove/Matomo/Pinterest
  /^AMCV_/, /^s_/, /^utag/, /^mbox/,                       // Adobe / Tealium
  /^Hm_lvt_/, /^Hm_lpvt_/, /^HMACCOUNT$/, /^BAIDUID$/,     // Baidu
  /^__qca$/, /^ln_or$/, /^_lc2_/, /^personalization_id$/,  // Quantcast/LinkedIn/Twitter
  /^YSC$/, /^VISITOR_INFO/, /^IDE$/, /^test_cookie$/       // YouTube/DoubleClick
];
const esRastreo = (n) => RASTREO.some((re) => re.test(n));

// Firmas de plataformas de gestion del consentimiento (CMP)
const CMPS = [
  ['OneTrust',    /onetrust|otSDKStub|cookielaw\.org|optanon/i],
  ['Cookiebot',   /cookiebot|consent\.cookiebot/i],
  ['Usercentrics',/usercentrics|uc\.usercentrics/i],
  ['Didomi',      /didomi/i],
  ['TrustArc',    /trustarc|truste\.com|consent\.trustarc/i],
  ['CookieYes',   /cookieyes|cky-|cookie-law-info/i],
  ['Complianz',   /complianz|cmplz/i],
  ['Osano',       /osano/i],
  ['Quantcast',   /quantcast|choice\.consensu/i],
  ['Termly',      /termly/i],
  ['Iubenda',     /iubenda/i],
  ['Tarteaucitron',/tarteaucitron/i],
  ['CookieScript',/cookie-script|cookiescript/i]
];

// Principio POUR segun el primer digito del criterio WCAG (p.ej. "1.4.3" -> 1)
const PRINCIPIO = { '1': 'Perceptible', '2': 'Operable', '3': 'Comprensible', '4': 'Robusto' };

// Deriva nivel A / AA / AAA a partir de los tags de axe (wcag2a, wcag2aa, wcag21aaa...)
function nivelDe(tags) {
  let nivel = null;
  for (const t of tags) {
    const m = /^wcag\d+(a{1,3})$/.exec(t);
    if (m) {
      const l = m[1].toUpperCase();               // A | AA | AAA
      if (l === 'AAA') return 'AAA';
      if (l === 'AA' && nivel !== 'AAA') nivel = 'AA';
      if (l === 'A' && !nivel) nivel = 'A';
    }
  }
  return nivel;
}

// Deriva el numero de criterio (p.ej. "143" -> "1.4.3") y su principio
function criterioDe(tags) {
  for (const t of tags) {
    const m = /^wcag(\d)(\d)(\d+)$/.exec(t);       // wcag143 -> 1.4.3
    if (m) return { num: `${m[1]}.${m[2]}.${m[3]}`, principio: PRINCIPIO[m[1]] || 'Otro' };
  }
  return { num: null, principio: 'Otro' };
}

function guardarJSON(res) {
  fs.writeFileSync(SALIDA_JSON, JSON.stringify(res, null, 2));
}

function guardarCSV(res) {
  const cab = [
    'id','grupo','sigla','pais','url','ok','error','title','lang','viewport','https',
    'cookies_pre','rastreo_pre','nombres_rastreo','cmp','banner',
    'ax_violaciones','ax_nodos','nivelA_nodos','nivelAA_nodos','nivelAAA_nodos',
    'Perceptible','Operable','Comprensible','Robusto','max_nivel_sin_fallo_auto'
  ];
  const filas = [cab.join(',')];
  for (const r of res) {
    const a = r.accesibilidad || {};
    const c = r.cookies || {};
    const p = (a.porPrincipio || {});
    const n = (a.porNivel || {});
    const celda = (v) => {
      const s = (v === undefined || v === null) ? '' : String(v);
      return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    };
    filas.push([
      r.id, r.grupo, r.sigla, r.pais, r.url, r.ok, r.error || '', a.title || '', a.lang || '',
      a.viewport ? 1 : 0, r.https ? 1 : 0,
      c.total_pre ?? '', c.rastreo_pre ?? '', (c.nombres_rastreo || []).join(' '),
      (c.cmp || []).join(' '), c.banner ? 1 : 0,
      a.violaciones ?? '', a.nodos ?? '',
      n.A ?? '', n.AA ?? '', n.AAA ?? '',
      p.Perceptible ?? '', p.Operable ?? '', p.Comprensible ?? '', p.Robusto ?? '',
      a.maxNivelSinFallo || ''
    ].map(celda).join(','));
  }
  fs.writeFileSync(SALIDA_CSV, filas.join('\n'));
}

// --------------------------- Analisis por sitio ----------------------------
async function auditarSitio(browser, uni) {
  const ctx = await browser.newContext({
    ignoreHTTPSErrors: true,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
  });
  const page = await ctx.newPage();
  const rec = { ...uni, ok: false, https: uni.url.startsWith('https') };

  let intento = 0, cargo = false, ultimoError = '';
  while (intento <= REINTENTOS && !cargo) {
    try {
      await page.goto(uni.url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT_MS });
      cargo = true;
    } catch (e) { ultimoError = String(e).split('\n')[0]; intento++; }
  }
  if (!cargo) { rec.error = ultimoError; await ctx.close(); return rec; }

  try {
    await page.waitForTimeout(ESPERA_JS_MS);

    if (MEDIR_COOKIES) {
    // ---- COOKIES previas al consentimiento (sin tocar el banner) ----
    const cookies = await ctx.cookies();
    const nombres = cookies.map((c) => c.name);
    const rastreoNombres = nombres.filter(esRastreo);

    // ---- CMP y banner (heuristica sobre HTML + globales) ----
    const htmlProbe = await page.evaluate(() => {
      // Fuentes fiables: src de scripts/iframes y href de <link> (no todos los globals del navegador)
      const src = []
        .concat(Array.from(document.scripts).map((s) => s.src || ''))
        .concat(Array.from(document.querySelectorAll('iframe')).map((f) => f.src || ''))
        .concat(Array.from(document.querySelectorAll('link[href]')).map((l) => l.href || ''))
        .join(' ');
      // Globales especificos de CMP conocidos (lista blanca, sin ruido)
      const globalesCMP = ['OneTrust','Optanon','OptanonWrapper','Cookiebot','CookieConsent',
        'Didomi','usercentrics','UC_UI','__tcfapi','Osano','cmplz_manage_consent','CookieScript',
        'cookieyes','cky','tarteaucitron','truste','_iub','Termly']
        .filter((k) => typeof window[k] !== 'undefined').join(' ');
      const txt = (document.body ? document.body.innerText : '').slice(0, 6000).toLowerCase();
      const tieneBanner = !!Array.from(document.querySelectorAll('div,section,dialog,aside,[role="dialog"]'))
        .find((el) => {
          const st = getComputedStyle(el);
          const r = /cookie|consentimiento|consent|privac/i.test((el.textContent || '').slice(0, 400));
          return r && (st.position === 'fixed' || st.position === 'sticky') && el.offsetHeight > 0 && el.offsetHeight < 600;
        });
      return { blob: (src + ' ' + globalesCMP).slice(0, 20000),
               tcf: typeof window.__tcfapi === 'function', banner: !!tieneBanner };
    });
    const cmp = CMPS.filter(([, re]) => re.test(htmlProbe.blob)).map(([n]) => n);
    if (htmlProbe.tcf && !cmp.includes('IAB-TCF')) cmp.push('IAB-TCF');

    rec.cookies = {
      total_pre: nombres.length,
      rastreo_pre: rastreoNombres.length,
      nombres_pre: nombres,
      nombres_rastreo: rastreoNombres,
      cmp,
      banner: htmlProbe.banner
    };
    } // fin MEDIR_COOKIES

    // ---- ACCESIBILIDAD: axe-core ----
    const tags = ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22a','wcag22aa'];
    if (INCLUIR_AAA) tags.push('wcag2aaa','wcag21aaa');
    await page.evaluate(axeSource);
    const ax = await page.evaluate(async (tgs) => {
      return await window.axe.run(document, { runOnly: { type: 'tag', values: tgs },
        resultTypes: ['violations', 'passes', 'incomplete'] });
    }, tags);

    const porPrincipio = { Perceptible: 0, Operable: 0, Comprensible: 0, Robusto: 0 };
    const porNivel = { A: 0, AA: 0, AAA: 0 };
    const nivelesConFallo = new Set();
    const reglas = [];
    let nodos = 0;
    for (const v of ax.violations) {
      const crit = criterioDe(v.tags);
      const nivel = nivelDe(v.tags);
      const nn = v.nodes.length;
      nodos += nn;
      if (porPrincipio[crit.principio] !== undefined) porPrincipio[crit.principio] += nn;
      if (nivel) { porNivel[nivel] += nn; nivelesConFallo.add(nivel); }
      reglas.push({ id: v.id, impacto: v.impact, criterio: crit.num, principio: crit.principio, nivel, nodos: nn, ayuda: v.help });
    }
    reglas.sort((a, b) => b.nodos - a.nodos);

    // "max nivel sin fallo automatico": A si no hay fallos A; AA si ademas no hay AA; etc.
    let maxNivelSinFallo = 'ninguno';
    if (!nivelesConFallo.has('A')) {
      maxNivelSinFallo = 'A';
      if (!nivelesConFallo.has('AA')) {
        maxNivelSinFallo = 'AA';
        if (!nivelesConFallo.has('AAA')) maxNivelSinFallo = 'AAA';
      }
    }

    rec.accesibilidad = {
      title: await page.title(),
      lang: await page.evaluate(() => document.documentElement.getAttribute('lang')),
      viewport: await page.evaluate(() => !!document.querySelector('meta[name="viewport"]')),
      skipLink: await page.evaluate(() => !!document.querySelector('a[href^="#"]')
        && /saltar|skip|contenido principal|main content/i.test(document.body.innerText.slice(0, 1500))),
      violaciones: ax.violations.length,
      nodos,
      porPrincipio,
      porNivel,
      maxNivelSinFallo,
      incompletos: ax.incomplete.length,       // requieren revision humana
      passes: ax.passes.length,
      reglas: reglas.slice(0, 25)
    };
    rec.axe_version = ax.testEngine ? ax.testEngine.version : null;
    rec.fecha = new Date().toISOString();
    rec.ok = true;
  } catch (e) {
    rec.error = 'analisis: ' + String(e).split('\n')[0];
  }
  await ctx.close();
  return rec;
}

// --------------------------- Programa principal ----------------------------
(async () => {
  if (!fs.existsSync(ARCHIVO_LISTA)) { console.error('Falta ' + ARCHIVO_LISTA); process.exit(1); }
  const lista = JSON.parse(fs.readFileSync(ARCHIVO_LISTA, 'utf8'));

  // Reanudacion: cargar resultados previos y saltar los ya hechos con exito
  let previos = [];
  if (fs.existsSync(SALIDA_JSON)) {
    try { previos = JSON.parse(fs.readFileSync(SALIDA_JSON, 'utf8')); } catch (e) { previos = []; }
  }
  const hechos = new Map(previos.map((r) => [r.id, r]));
  const resultados = lista.map((u) => hechos.get(u.id) || null);

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  console.log('== Auditoria de ' + lista.length + ' universidades (axe-core + cookies) ==\n');

  for (let i = 0; i < lista.length; i++) {
    const uni = lista[i];
    if (resultados[i] && resultados[i].ok) {
      console.log(`[${i + 1}/${lista.length}] ${uni.sigla} — ya auditado, se omite`);
      continue;
    }
    process.stdout.write(`[${i + 1}/${lista.length}] ${uni.grupo} · ${uni.sigla}  ${uni.url}  ... `);
    const rec = await auditarSitio(browser, uni);
    resultados[i] = rec;
    if (rec.ok) {
      const a = rec.accesibilidad, c = rec.cookies || {};
      const cookieMsg = rec.cookies ? `cookies: ${c.total_pre} (${c.rastreo_pre} rastreo) | CMP: ${(c.cmp[0] || '-')} | ` : '';
      console.log(`OK  | WCAG: ${a.violaciones} viol (${a.nodos} nodos) | ${cookieMsg}sin-fallo≤${a.maxNivelSinFallo}`);
    } else {
      console.log('FALLO: ' + (rec.error || 'desconocido'));
    }
    // Guardado incremental tras cada sitio
    const limpio = resultados.filter(Boolean);
    guardarJSON(limpio);
    guardarCSV(limpio);
  }

  await browser.close();
  const final = resultados.filter(Boolean);
  const ok = final.filter((r) => r.ok).length;
  console.log(`\n== Terminado: ${ok}/${lista.length} auditados con exito ==`);
  console.log('Archivos generados: ' + SALIDA_JSON + '  y  ' + SALIDA_CSV);
  console.log('Envia esos dos archivos de vuelta para el analisis.');
})();
