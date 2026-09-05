/* ============================================================================
 *  AUDITOR MULTIPUNTO — WCAG + PRIVACIDAD DE SITIOS WEB UNIVERSITARIOS
 *  ---------------------------------------------------------------------------
 *  Version 2.0 (agosto 2026). Extiende auditar.js con:
 *    - Etiqueta de PUNTO DE OBSERVACION (--vantage) y numero de PASADA (--run)
 *    - Registro de la IP publica y su geolocalizacion como EVIDENCIA de que la
 *      medicion se hizo realmente desde el pais declarado
 *    - Un archivo de salida por (punto de observacion, pasada), de modo que los
 *      resultados quedan PAREADOS sitio a sitio y admiten la prueba de McNemar
 *    - Orden de visita FIJO en todas las pasadas, para que cada sitio se mida
 *      siempre en el mismo momento relativo de la pasada
 *
 *  El metodo de medicion es IDENTICO al de la auditoria de agosto de 2026,
 *  para que los resultados sean comparables con los ya publicados.
 *
 *  USO (Windows, desde la carpeta del proyecto):
 *      node auditar_multipunto.js --vantage=EC --run=1
 *      node auditar_multipunto.js --vantage=EU --run=1
 *      node auditar_multipunto.js --vantage=US --run=1
 *
 *  Prueba piloto con los primeros 5 sitios (para comprobar que todo funciona):
 *      node auditar_multipunto.js --vantage=EC --run=0 --limit=5
 * ==========================================================================*/

const { chromium } = require('playwright');
const fs = require('fs');

// --------------------------- Argumentos de linea de ordenes ----------------
function arg(nombre, porDefecto) {
	const p = process.argv.find((a) => a.startsWith('--' + nombre + '='));
	return p ? p.split('=').slice(1).join('=') : porDefecto;
}

const VANTAGE = arg('vantage', '').toUpperCase();
const RUN     = arg('run', '');
const LIMIT   = parseInt(arg('limit', '0'), 10) || 0;

const VANTAGES_VALIDOS = ['EC', 'EU', 'US', 'GB'];
if (!VANTAGES_VALIDOS.includes(VANTAGE)) {
	console.error('\nERROR: falta o es invalido --vantage.');
	console.error('       Valores admitidos: EC (Ecuador), EU (Union Europea), US (Estados Unidos).');
	console.error('       Ejemplo: node auditar_multipunto.js --vantage=EU --run=1\n');
	process.exit(1);
}
if (RUN === '' || isNaN(parseInt(RUN, 10))) {
	console.error('\nERROR: falta o es invalido --run (numero de pasada, entero).');
	console.error('       Ejemplo: node auditar_multipunto.js --vantage=EU --run=1\n');
	process.exit(1);
}

// --------------------------- Configuracion ---------------------------------
// NO MODIFICAR: estos valores deben ser identicos a los de la auditoria de
// agosto de 2026 para que las mediciones sean comparables.
const ESPERA_JS_MS  = 4000;
const TIMEOUT_MS    = 45000;
const REINTENTOS    = 1;
const INCLUIR_AAA   = true;
const MEDIR_COOKIES = true;
const USER_AGENT    = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/128.0 Safari/537.36';

const CHEQUEO_CADA  = 25;   // cada cuantos sitios se revuelve a comprobar el pais
const ARCHIVO_LISTA = 'universidades.json';
const SUFIJO        = `${VANTAGE}_r${RUN}`;
const SALIDA_JSON   = `resultados_${SUFIJO}.json`;
const SALIDA_CSV    = `resultados_${SUFIJO}.csv`;
const SALIDA_META   = `meta_${SUFIJO}.json`;

// --------------------------- Utilidades ------------------------------------
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const RASTREO = [
	/^_ga/, /^_gid$/, /^__utm/, /^_gcl_au$/, /^_gac_/,
	/^_fbp$/, /^_fbc$/, /^fr$/,
	/^_tt_/, /^_ttp$/,
	/^_clck$/, /^_clsk$/, /^MUID$/,
	/^_hj/, /^_uet/,
	/^nmstat$/, /^_pk_/, /^pys/, /^_pin_/,
	/^AMCV_/, /^s_/, /^utag/, /^mbox/,
	/^Hm_lvt_/, /^Hm_lpvt_/, /^HMACCOUNT$/, /^BAIDUID$/,
	/^__qca$/, /^ln_or$/, /^_lc2_/, /^personalization_id$/,
	/^YSC$/, /^VISITOR_INFO/, /^IDE$/, /^test_cookie$/
];
const esRastreo = (n) => RASTREO.some((re) => re.test(n));

const CMPS = [
	['OneTrust',     /onetrust|otSDKStub|cookielaw\.org|optanon/i],
	['Cookiebot',    /cookiebot|consent\.cookiebot/i],
	['Usercentrics', /usercentrics|uc\.usercentrics/i],
	['Didomi',       /didomi/i],
	['TrustArc',     /trustarc|truste\.com|consent\.trustarc/i],
	['CookieYes',    /cookieyes|cky-|cookie-law-info/i],
	['Complianz',    /complianz|cmplz/i],
	['Osano',        /osano/i],
	['Quantcast',    /quantcast|choice\.consensu/i],
	['Termly',       /termly/i],
	['Iubenda',      /iubenda/i],
	['Tarteaucitron',/tarteaucitron/i],
	['CookieScript', /cookie-script|cookiescript/i]
];

const PRINCIPIO = { '1': 'Perceptible', '2': 'Operable', '3': 'Comprensible', '4': 'Robusto' };

function nivelDe(tags) {
	let nivel = null;
	for (const t of tags) {
		const m = /^wcag\d+(a{1,3})$/.exec(t);
		if (m) {
			const l = m[1].toUpperCase();
			if (l === 'AAA') return 'AAA';
			if (l === 'AA' && nivel !== 'AAA') nivel = 'AA';
			if (l === 'A' && !nivel) nivel = 'A';
		}
	}
	return nivel;
}

function criterioDe(tags) {
	for (const t of tags) {
		const m = /^wcag(\d)(\d)(\d+)$/.exec(t);
		if (m) return { num: `${m[1]}.${m[2]}.${m[3]}`, principio: PRINCIPIO[m[1]] || 'Otro' };
	}
	return { num: null, principio: 'Otro' };
}

// --------------------------- Evidencia del punto de observacion ------------
// Consulta dos servicios independientes de geolocalizacion por IP. Si el pais
// devuelto NO coincide con el declarado en --vantage, el programa AVISA y pide
// confirmacion explicita, porque medir desde el pais equivocado invalida la
// pasada entera.
const PAIS_ESPERADO = { EC: ['EC'], US: ['US'], GB: ['GB', 'UK'], EU: [
	'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT',
	'LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE'
] };

// Servicios de geolocalizacion por IP. Se consultan por orden hasta obtener
// DOS lecturas validas. Tener varios evita que un corte puntual de uno de
// ellos aborte una pasada de 40 minutos.
const SERVICIOS_GEO = [
	'https://ipinfo.io/json',
	'https://ipwho.is/',
	'https://api.country.is/',
	'https://ifconfig.co/json'
];

// Normaliza el codigo de pais de dos letras entre los distintos formatos.
function codigoPais(j) {
	const c = j.country_code || j.countryCode || j.country_iso ||
	          (typeof j.country === 'string' && j.country.length === 2 ? j.country : null);
	return c ? String(c).toUpperCase() : null;
}

async function comprobarUbicacion(browser, silencioso) {
	const ctx = await browser.newContext({ userAgent: USER_AGENT });
	const page = await ctx.newPage();
	const lecturas = [];
	let validas = 0;
	for (const url of SERVICIOS_GEO) {
		if (validas >= 2) break;
		try {
			await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
			const txt = (await page.evaluate(() => document.body ? document.body.innerText : '')).trim();
			if (!txt) throw new Error('respuesta vacia');
			const j = JSON.parse(txt);
			const pais = codigoPais(j);
			if (!pais) throw new Error('sin codigo de pais en la respuesta');
			lecturas.push({
				servicio: url,
				ip: j.ip || null,
				pais,
				ciudad: j.city || null,
				organizacion: j.org || j.asn || j.connection && j.connection.org || null
			});
			validas++;
		} catch (e) {
			lecturas.push({ servicio: url, error: String(e).split('\n')[0].slice(0, 120) });
		}
	}
	await ctx.close();
	if (!silencioso) lecturas.forEach((u) => console.log('  ' + JSON.stringify(u)));
	return lecturas;
}

// Devuelve 'ok', 'mal' o 'indeterminado'.
//   ok            = todas las lecturas con pais coinciden con el punto declarado
//   mal           = alguna lectura dice un pais distinto  -> la VPN fallo
//   indeterminado = ningun servicio respondio  -> no se puede afirmar nada
function estadoUbicacion(lecturas) {
	const paises = lecturas.map((u) => u.pais).filter(Boolean);
	if (paises.length === 0) return 'indeterminado';
	return paises.every((p) => PAIS_ESPERADO[VANTAGE].includes(p)) ? 'ok' : 'mal';
}

function ubicacionCorrecta(lecturas) {
	return estadoUbicacion(lecturas) === 'ok';
}

// --------------------------- Analisis por sitio ----------------------------
async function auditarSitio(browser, uni) {
	const ctx = await browser.newContext({ ignoreHTTPSErrors: true, userAgent: USER_AGENT });
	const page = await ctx.newPage();
	const rec = { ...uni, vantage: VANTAGE, run: parseInt(RUN, 10),
	              ok: false, https: uni.url.startsWith('https') };

	let intento = 0, cargo = false, ultimoError = '';
	while (intento <= REINTENTOS && !cargo) {
		try {
			await page.goto(uni.url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT_MS });
			cargo = true;
		} catch (e) { ultimoError = String(e).split('\n')[0]; intento++; }
	}
	if (!cargo) { rec.error = ultimoError; rec.fecha = new Date().toISOString(); await ctx.close(); return rec; }

	try {
		await page.waitForTimeout(ESPERA_JS_MS);

		if (MEDIR_COOKIES) {
			const cookies = await ctx.cookies();
			const nombres = cookies.map((c) => c.name);
			const rastreoNombres = nombres.filter(esRastreo);

			const htmlProbe = await page.evaluate(() => {
				const src = []
					.concat(Array.from(document.scripts).map((s) => s.src || ''))
					.concat(Array.from(document.querySelectorAll('iframe')).map((f) => f.src || ''))
					.concat(Array.from(document.querySelectorAll('link[href]')).map((l) => l.href || ''))
					.join(' ');
				const globalesCMP = ['OneTrust','Optanon','OptanonWrapper','Cookiebot','CookieConsent',
					'Didomi','usercentrics','UC_UI','__tcfapi','Osano','cmplz_manage_consent','CookieScript',
					'cookieyes','cky','tarteaucitron','truste','_iub','Termly']
					.filter((k) => typeof window[k] !== 'undefined').join(' ');
				const tieneBanner = !!Array.from(document.querySelectorAll('div,section,dialog,aside,[role="dialog"]'))
					.find((el) => {
						const st = getComputedStyle(el);
						const r = /cookie|consentimiento|consent|privac/i.test((el.textContent || '').slice(0, 400));
						return r && (st.position === 'fixed' || st.position === 'sticky')
							&& el.offsetHeight > 0 && el.offsetHeight < 600;
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
		}

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
			reglas.push({ id: v.id, impacto: v.impact, criterio: crit.num,
			              principio: crit.principio, nivel, nodos: nn, ayuda: v.help });
		}
		reglas.sort((a, b) => b.nodos - a.nodos);

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
			violaciones: ax.violations.length,
			nodos,
			porPrincipio,
			porNivel,
			maxNivelSinFallo,
			incompletos: ax.incomplete.length,
			passes: ax.passes.length,
			reglas: reglas.slice(0, 25)
		};
		rec.axe_version = ax.testEngine ? ax.testEngine.version : null;
		rec.url_final = page.url();
		rec.ok = true;
	} catch (e) {
		rec.error = 'analisis: ' + String(e).split('\n')[0];
	}
	rec.fecha = new Date().toISOString();
	await ctx.close();
	return rec;
}

// --------------------------- Salidas ---------------------------------------
function guardarJSON(res) { fs.writeFileSync(SALIDA_JSON, JSON.stringify(res, null, 2)); }

function guardarCSV(res) {
	const cab = [
		'id','vantage','run','grupo','sigla','pais','url','ok','error','title','lang','viewport','https',
		'cookies_pre','rastreo_pre','nombres_rastreo','cmp','banner',
		'ax_violaciones','ax_nodos','nivelA_nodos','nivelAA_nodos','nivelAAA_nodos',
		'Perceptible','Operable','Comprensible','Robusto','max_nivel_sin_fallo_auto','incompletos','fecha'
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
			r.id, r.vantage, r.run, r.grupo, r.sigla, r.pais, r.url, r.ok, r.error || '',
			a.title || '', a.lang || '', a.viewport ? 1 : 0, r.https ? 1 : 0,
			c.total_pre ?? '', c.rastreo_pre ?? '', (c.nombres_rastreo || []).join(' '),
			(c.cmp || []).join(' '), c.banner === undefined ? '' : (c.banner ? 1 : 0),
			a.violaciones ?? '', a.nodos ?? '',
			n.A ?? '', n.AA ?? '', n.AAA ?? '',
			p.Perceptible ?? '', p.Operable ?? '', p.Comprensible ?? '', p.Robusto ?? '',
			a.maxNivelSinFallo || '', a.incompletos ?? '', r.fecha || ''
		].map(celda).join(','));
	}
	fs.writeFileSync(SALIDA_CSV, filas.join('\n'));
}

// --------------------------- Programa principal ----------------------------
(async () => {
	if (!fs.existsSync(ARCHIVO_LISTA)) {
		console.error('ERROR: falta el archivo ' + ARCHIVO_LISTA + ' en esta carpeta.');
		process.exit(1);
	}
	let lista = JSON.parse(fs.readFileSync(ARCHIVO_LISTA, 'utf8'));
	if (LIMIT > 0) lista = lista.slice(0, LIMIT);

	let previos = [];
	if (fs.existsSync(SALIDA_JSON)) {
		try { previos = JSON.parse(fs.readFileSync(SALIDA_JSON, 'utf8')); } catch (e) { previos = []; }
	}
	const hechos = new Map(previos.map((r) => [r.id, r]));
	const resultados = lista.map((u) => hechos.get(u.id) || null);

	const browser = await chromium.launch({ headless: true,
		args: ['--no-sandbox', '--disable-dev-shm-usage'] });

	console.log('\n=======================================================');
	console.log(`  AUDITORIA MULTIPUNTO — punto: ${VANTAGE}   pasada: ${RUN}`);
	console.log(`  Sitios en la lista: ${lista.length}`);
	console.log('=======================================================\n');

	// --- Evidencia de ubicacion ---
	console.log('Comprobando desde que pais se esta midiendo...');
	const ubic = await comprobarUbicacion(browser, false);
	const paises = ubic.map((u) => u.pais).filter(Boolean);
	const coincide = ubicacionCorrecta(ubic);

	const meta = {
		vantage: VANTAGE,
		run: parseInt(RUN, 10),
		inicio: new Date().toISOString(),
		geolocalizacion: ubic,
		coincide_con_vantage: coincide,
		controles_de_ubicacion: [{ momento: 'inicio', sitio: 0, lecturas: ubic, correcta: coincide }],
		configuracion: { ESPERA_JS_MS, TIMEOUT_MS, REINTENTOS, INCLUIR_AAA, MEDIR_COOKIES, USER_AGENT },
		axe_core: require('axe-core/package.json').version,
		playwright: require('playwright/package.json').version,
		node: process.version,
		plataforma: process.platform + ' ' + process.arch,
		sitios: lista.length
	};

	if (!coincide) {
		console.log('\n  *** AVISO ***');
		console.log('  El pais detectado NO coincide con --vantage=' + VANTAGE + '.');
		console.log('  Paises detectados: ' + (paises.join(', ') || '(ninguno)'));
		console.log('  Si esta usando VPN, compruebe que esta conectada al pais correcto');
		console.log('  ANTES de continuar. La pasada se marcara como sospechosa en meta_' + SUFIJO + '.json.');
		console.log('  Esperando 15 segundos: pulse Ctrl+C para abortar.\n');
		await new Promise((r) => setTimeout(r, 15000));
	} else {
		console.log('  OK: la ubicacion coincide con el punto declarado.\n');
	}
	fs.writeFileSync(SALIDA_META, JSON.stringify(meta, null, 2));

	const t0 = Date.now();
	for (let i = 0; i < lista.length; i++) {
		const uni = lista[i];
		if (resultados[i] && resultados[i].ok) {
			console.log(`[${i + 1}/${lista.length}] ${uni.sigla} — ya auditado en esta pasada, se omite`);
			continue;
		}
		process.stdout.write(`[${i + 1}/${lista.length}] ${VANTAGE} · ${uni.sigla}  ${uni.url}  ... `);
		const rec = await auditarSitio(browser, uni);
		resultados[i] = rec;
		if (rec.ok) {
			const a = rec.accesibilidad, c = rec.cookies || {};
			const ck = rec.cookies ? `cookies ${c.total_pre} (${c.rastreo_pre} rastreo) | banner ${c.banner ? 'SI' : 'no'} | CMP ${(c.cmp[0] || '-')} | ` : '';
			console.log(`OK | WCAG ${a.violaciones} viol (${a.nodos} nodos) | ${ck}sin-fallo<=${a.maxNivelSinFallo}`);
		} else {
			console.log('FALLO: ' + (rec.error || 'desconocido'));
		}
		const limpio = resultados.filter(Boolean);
		guardarJSON(limpio);
		guardarCSV(limpio);

		// --- Control periodico de ubicacion -------------------------------------
		// Compensa la falta de cortafuegos de emergencia (kill switch) en algunas
		// VPN: si la conexion se cae a mitad de la pasada, aqui se detecta.
		const esUltimo = (i === lista.length - 1);
		if (((i + 1) % CHEQUEO_CADA === 0) || esUltimo) {
			const chk = await comprobarUbicacion(browser, true);
			const estado = estadoUbicacion(chk);
			meta.controles_de_ubicacion.push({
				momento: esUltimo ? 'final' : 'intermedio',
				sitio: i + 1, lecturas: chk, correcta: estado === 'ok', estado
			});
			fs.writeFileSync(SALIDA_META, JSON.stringify(meta, null, 2));
			if (estado === 'indeterminado') {
				console.log(`      [control de ubicacion tras ${i + 1} sitios: NO CONCLUYENTE, ` +
					'ningun servicio respondio; la pasada continua]');
			} else if (estado === 'mal') {
				console.log('');
				console.log('  *** ALERTA: LA VPN SE CAYO O CAMBIO DE PAIS ***');
				console.log('  Detectado tras el sitio ' + (i + 1) + '. Paises leidos: ' +
					(chk.map((u) => u.pais).filter(Boolean).join(', ') || '(ninguno)'));
				console.log('  Los sitios medidos desde el ultimo control son SOSPECHOSOS.');
				console.log('  Reconecte la VPN al pais correcto y repita la pasada COMPLETA:');
				console.log('  borre resultados_' + SUFIJO + '.* y meta_' + SUFIJO + '.json.');
				console.log('  Abortando en 10 segundos.');
				console.log('');
				await new Promise((r) => setTimeout(r, 10000));
				await browser.close();
				process.exit(2);
			} else {
				console.log(`      [control de ubicacion tras ${i + 1} sitios: correcto]`);
			}
		}
	}

	await browser.close();
	const final = resultados.filter(Boolean);
	const ok = final.filter((r) => r.ok).length;
	meta.fin = new Date().toISOString();
	meta.duracion_min = Math.round((Date.now() - t0) / 60000);
	meta.exitosos = ok;
	meta.fallidos = final.length - ok;
	fs.writeFileSync(SALIDA_META, JSON.stringify(meta, null, 2));

	console.log('\n=======================================================');
	console.log(`  Terminado: ${ok}/${lista.length} auditados con exito`);
	console.log(`  Duracion: ${meta.duracion_min} minutos`);
	console.log(`  Controles de ubicacion superados: ${meta.controles_de_ubicacion.filter((c) => c.correcta).length}/${meta.controles_de_ubicacion.length}`);
	console.log(`  Archivos: ${SALIDA_JSON}, ${SALIDA_CSV}, ${SALIDA_META}`);
	console.log('=======================================================\n');
	console.log('Conserve los TRES archivos. El de meta_ es la evidencia de');
	console.log('que la medicion se hizo desde el pais declarado.\n');
})();
