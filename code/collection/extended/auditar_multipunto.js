/* ============================================================================
 *  AUDITOR MULTIPUNTO — WCAG + PRIVACIDAD DE SITIOS WEB UNIVERSITARIOS
 *  ---------------------------------------------------------------------------
 *  Version 3.0 (agosto 2026). Extiende la version 2.0 con CUATRO registros
 *  nuevos, todos PASIVOS, exigidos por la revision por pares:
 *
 *    (1) PETICIONES DE RED por proveedor. Para cada familia de proveedor se
 *        registra si la peticion llego a EMITIRSE y si alguna respuesta trajo
 *        cabecera Set-Cookie. Esto separa dos mecanismos que el frasco de
 *        cookies confunde:
 *           peticion emitida + sin Set-Cookie  -> decision en el PROVEEDOR
 *           peticion nunca emitida             -> decision en el SITIO, su
 *                                                 gestor de consentimiento o
 *                                                 su gestor de etiquetas
 *    (2) ESTADO DE CONSENTIMIENTO POR DEFECTO en el HTML servido: presencia de
 *        gtag('consent','default',...), de su parametro region, del consent
 *        mode de UET y del de Clarity, con los fragmentos literales que lo
 *        justifican.
 *    (3) TAMANO DEL ARBOL DE DOCUMENTO y otras medidas de complejidad, para
 *        normalizar los nodos con fallo (violaciones por cada mil nodos).
 *    (4) CABECERAS DE RESPUESTA del documento principal y senales de gestor de
 *        contenidos, alojamiento y red de distribucion.
 *
 *  Se anaden ademas los puntos de observacion GB (Reino Unido) y CH (Suiza), y
 *  una etiqueta --red para distinguir conexion residencial de centro de datos.
 *
 *  COMPARABILIDAD. Ningun parametro de medicion cambia respecto de la version
 *  2.0: misma espera, mismo tiempo limite, mismo agente de usuario, mismas
 *  etiquetas de axe, mismo orden de visita y ninguna interaccion con banners.
 *  Los registros nuevos son observadores; no alteran lo que la pagina hace.
 *  Se conservan las DOS taxonomias de cookies (la original y la extendida) para
 *  que las cifras nuevas sean comparables con las ya publicadas sin necesidad
 *  de reclasificar despues.
 *
 *  USO (Windows, desde la carpeta del proyecto):
 *      node auditar_multipunto.js --vantage=EC --run=1 --red=residencial
 *      node auditar_multipunto.js --vantage=EU --run=1 --red=centro_datos
 *      node auditar_multipunto.js --vantage=EU --run=1 --red=residencial
 *      node auditar_multipunto.js --vantage=CH --run=1 --red=centro_datos
 *
 *  Prueba piloto con los primeros 5 sitios:
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
const RED     = arg('red', '').toLowerCase();
const CIUDAD  = arg('ciudad', '');

const VANTAGES_VALIDOS = ['EC', 'EU', 'GB', 'US', 'CH'];
if (!VANTAGES_VALIDOS.includes(VANTAGE)) {
	console.error('\nERROR: falta o es invalido --vantage.');
	console.error('       Valores admitidos: EC (Ecuador), EU (Union Europea),');
	console.error('                          GB (Reino Unido), US (Estados Unidos), CH (Suiza).');
	console.error('       Ejemplo: node auditar_multipunto.js --vantage=CH --run=1 --red=centro_datos\n');
	process.exit(1);
}
if (RUN === '' || isNaN(parseInt(RUN, 10))) {
	console.error('\nERROR: falta o es invalido --run (numero de pasada, entero).');
	console.error('       Ejemplo: node auditar_multipunto.js --vantage=EU --run=1\n');
	process.exit(1);
}
if (!['residencial', 'centro_datos'].includes(RED)) {
	console.error('\nERROR: falta o es invalido --red.');
	console.error('       Valores admitidos: residencial | centro_datos');
	console.error('       Es OBLIGATORIO porque el tipo de red es una variable del diseno:');
	console.error('       sin ella no puede descartarse el artefacto de gestion de bots.\n');
	process.exit(1);
}

// --------------------------- Configuracion ---------------------------------
// NO MODIFICAR: identicos a la auditoria de agosto de 2026 para que las
// mediciones sigan siendo comparables con las ya publicadas.
const ESPERA_JS_MS  = 4000;
const TIMEOUT_MS    = 45000;
const REINTENTOS    = 1;
const INCLUIR_AAA   = true;
const MEDIR_COOKIES = true;
const USER_AGENT    = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/128.0 Safari/537.36';

const CHEQUEO_CADA  = 25;
const ARCHIVO_LISTA = 'universidades.json';
const SUFIJO        = `${VANTAGE}_r${RUN}`;
const SALIDA_JSON   = `resultados_${SUFIJO}.json`;
const SALIDA_CSV    = `resultados_${SUFIJO}.csv`;
const SALIDA_META   = `meta_${SUFIJO}.json`;

// --------------------------- Utilidades ------------------------------------
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// Taxonomia ORIGINAL (la de la auditoria publicada). Se conserva intacta.
const RASTREO_ORIGINAL = [
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

// Taxonomia EXTENDIDA (la usada en el articulo). Anade las familias omitidas.
const RASTREO_EXTENDIDA = RASTREO_ORIGINAL.concat([
	/^receive-cookie-deprecation$/,
	/^VISITOR_PRIVACY/, /^__Secure-YNID$/, /^__Secure-ROLLOUT/, /^DSID$/,
	/^ttcsid/,
	/^MR$/, /^SM$/, /^SRM_B$/, /^ANONCHK$/, /^CLID$/,
	/^bcookie$/, /^bscookie$/, /^lidc$/, /^li_sugr$/, /^li_gc$/,
	/^UserMatchHistory$/, /^AnalyticsSyncHistory$/,
	/^TapAd_/, /^sa-user-id/, /^_scid/, /^sc_at$/,
	/^muc_ads$/, /^_twpid$/,
	/^sbjs_/, /^_cs_/
]);

const esRastreoOrig = (n) => RASTREO_ORIGINAL.some((re) => re.test(n));
const esRastreoExt  = (n) => RASTREO_EXTENDIDA.some((re) => re.test(n));

// --------------------------- Dominios por proveedor ------------------------
// Cada familia se identifica por los dominios a los que el navegador dirige la
// peticion. Es la contrapartida, del lado de la red, de la taxonomia de nombres
// de cookie: permite saber si la peticion se emitio aunque no deje cookie.
const PROVEEDORES = [
	['Google Analytics', [/(^|\.)google-analytics\.com$/, /(^|\.)analytics\.google\.com$/]],
	['Google Tag Manager', [/(^|\.)googletagmanager\.com$/]],
	['Google Ads',       [/(^|\.)doubleclick\.net$/, /(^|\.)googleadservices\.com$/,
	                      /(^|\.)googlesyndication\.com$/, /(^|\.)google\.com$/]],
	['YouTube',          [/(^|\.)youtube\.com$/, /(^|\.)youtube-nocookie\.com$/, /(^|\.)ytimg\.com$/]],
	['Microsoft Clarity',[/(^|\.)clarity\.ms$/]],
	['Microsoft Ads/UET',[/(^|\.)bat\.bing\.com$/, /(^|\.)bing\.com$/, /(^|\.)c\.bing\.com$/,
	                      /(^|\.)clarity\.microsoft\.com$/]],
	['Meta',             [/(^|\.)facebook\.com$/, /(^|\.)facebook\.net$/, /(^|\.)fbcdn\.net$/]],
	['TikTok',           [/(^|\.)tiktok\.com$/, /(^|\.)analytics\.tiktok\.com$/, /(^|\.)byteoversea\.com$/]],
	['LinkedIn',         [/(^|\.)linkedin\.com$/, /(^|\.)licdn\.com$/, /(^|\.)ads\.linkedin\.com$/]],
	['TapAd',            [/(^|\.)tapad\.com$/]],
	['StackAdapt',       [/(^|\.)stackadapt\.com$/, /(^|\.)srv\.stackadapt\.com$/]],
	['Snapchat',         [/(^|\.)snapchat\.com$/, /(^|\.)sc-static\.net$/]],
	['X/Twitter',        [/(^|\.)twitter\.com$/, /(^|\.)x\.com$/, /(^|\.)ads-twitter\.com$/, /(^|\.)t\.co$/]],
	['Hotjar',           [/(^|\.)hotjar\.com$/, /(^|\.)hotjar\.io$/]],
	['Matomo',           [/(^|\.)matomo\.cloud$/, /(^|\.)matomo\.org$/]],
	['Siteimprove',      [/(^|\.)siteimprove\.com$/, /(^|\.)siteimproveanalytics\.(com|io)$/]],
	['Pinterest',        [/(^|\.)pinterest\.com$/, /(^|\.)pinimg\.com$/, /(^|\.)ct\.pinterest\.com$/]],
	['Adobe',            [/(^|\.)omtrdc\.net$/, /(^|\.)demdex\.net$/, /(^|\.)adobedtm\.com$/,
	                      /(^|\.)everesttech\.net$/]],
	['Tealium',          [/(^|\.)tiqcdn\.com$/, /(^|\.)tealiumiq\.com$/]],
	['ContentSquare',    [/(^|\.)contentsquare\.net$/, /(^|\.)content-square\.net$/]],
	['Baidu',            [/(^|\.)hm\.baidu\.com$/, /(^|\.)baidu\.com$/]],
	['Quantcast',        [/(^|\.)quantserve\.com$/, /(^|\.)quantcast\.com$/]],
	['LiveIntent',       [/(^|\.)liadm\.com$/, /(^|\.)liveintent\.com$/]],
	['Sourcebuster',     [/(^|\.)sourcebuster\.com$/]]
];

function proveedorDe(host) {
	for (const [nombre, patrones] of PROVEEDORES) {
		if (patrones.some((re) => re.test(host))) return nombre;
	}
	return null;
}

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

// --------------------------- (2) Consentimiento por defecto ----------------
// Busca en el HTML SERVIDO y en los scripts en linea las marcas de un estado de
// consentimiento por defecto regionalizado. Guarda los fragmentos literales
// para que la deteccion sea auditable y no haya que fiarse de la etiqueta.
function analizarConsentPorDefecto(html) {
	const out = {
		gtag_consent_default: false,
		gtag_consent_default_con_region: false,
		regiones_declaradas: [],
		uet_consent: false,
		clarity_consent: false,
		fragmentos: []
	};
	if (!html) return out;

	const reDefault = /(gtag|dataLayer\.push)[\s\S]{0,80}?["']consent["'][\s\S]{0,40}?["']default["']/gi;
	let m;
	while ((m = reDefault.exec(html)) !== null) {
		out.gtag_consent_default = true;
		const ventana = html.slice(m.index, m.index + 700);
		out.fragmentos.push(ventana.slice(0, 400));
		const reRegion = /["']region["']\s*:\s*\[([^\]]{0,400})\]/i.exec(ventana);
		if (reRegion) {
			out.gtag_consent_default_con_region = true;
			const codigos = reRegion[1].match(/["']([A-Z]{2}(?:-[A-Z0-9]{1,3})?)["']/g) || [];
			for (const c of codigos) {
				const limpio = c.replace(/["']/g, '');
				if (!out.regiones_declaradas.includes(limpio)) out.regiones_declaradas.push(limpio);
			}
		}
		if (out.fragmentos.length >= 8) break;
	}

	if (/uetq[\s\S]{0,200}?["']consent["']/i.test(html) ||
	    /["']set["']\s*,\s*["']consent["'][\s\S]{0,80}?ad_storage/i.test(html)) {
		out.uet_consent = true;
	}
	if (/clarity\s*\(\s*["']consent/i.test(html)) out.clarity_consent = true;

	return out;
}

// --------------------------- (4) Pila tecnica ------------------------------
function analizarPila(cabeceras, html) {
	const h = {};
	for (const k of Object.keys(cabeceras || {})) h[k.toLowerCase()] = cabeceras[k];
	const blob = (html || '').slice(0, 200000);

	const cdn = [];
	if (h['cf-ray'] || /cloudflare/i.test(h['server'] || '')) cdn.push('Cloudflare');
	if (h['x-amz-cf-id'] || /cloudfront/i.test(h['via'] || '')) cdn.push('CloudFront');
	if (h['x-served-by'] || /varnish/i.test(h['via'] || '')) cdn.push('Fastly/Varnish');
	if (/akamai/i.test((h['server'] || '') + (h['x-cache'] || '') + (h['via'] || ''))) cdn.push('Akamai');
	if (h['x-vercel-id']) cdn.push('Vercel');
	if (h['x-azure-ref'] || /azure/i.test(h['server'] || '')) cdn.push('Azure');
	if (h['x-github-request-id']) cdn.push('GitHub Pages');
	if (/incapsula|imperva/i.test(JSON.stringify(h))) cdn.push('Imperva');
	if (/sucuri/i.test(JSON.stringify(h))) cdn.push('Sucuri');

	const cms = [];
	const gen = /<meta[^>]+name=["']generator["'][^>]+content=["']([^"']+)["']/i.exec(blob);
	if (gen) cms.push('generator: ' + gen[1].slice(0, 80));
	if (/\/wp-content\/|\/wp-includes\//i.test(blob)) cms.push('WordPress');
	if (/\/sites\/default\/files\/|drupal/i.test(blob)) cms.push('Drupal');
	if (/\/media\/jui\/|joomla/i.test(blob)) cms.push('Joomla');
	if (/typo3/i.test(blob)) cms.push('TYPO3');
	if (/moodle/i.test(blob)) cms.push('Moodle');
	if (/liferay/i.test(blob)) cms.push('Liferay');
	if (/sharepoint|_layouts\/15/i.test(blob)) cms.push('SharePoint');
	if (/wix\.com|wixstatic/i.test(blob)) cms.push('Wix');
	if (/squarespace/i.test(blob)) cms.push('Squarespace');

	return {
		servidor: h['server'] || null,
		x_powered_by: h['x-powered-by'] || null,
		x_generator: h['x-generator'] || null,
		cdn: Array.from(new Set(cdn)),
		cms: Array.from(new Set(cms)),
		cabeceras_crudas: h
	};
}

// --------------------------- Evidencia del punto de observacion ------------
const PAIS_ESPERADO = {
	EC: ['EC'],
	US: ['US'],
	GB: ['GB', 'UK'],
	CH: ['CH'],
	EU: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT',
	     'LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE']
};

async function comprobarUbicacion(browser, silencioso) {
	const ctx = await browser.newContext({ userAgent: USER_AGENT });
	const page = await ctx.newPage();
	const lecturas = [];
	for (const url of ['https://ipinfo.io/json', 'https://ipapi.co/json/']) {
		try {
			await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
			const txt = await page.evaluate(() => document.body.innerText);
			const j = JSON.parse(txt);
			lecturas.push({
				servicio: url,
				ip: j.ip || null,
				pais: j.country || j.country_code || null,
				ciudad: j.city || null,
				organizacion: j.org || j.asn || null
			});
		} catch (e) {
			lecturas.push({ servicio: url, error: String(e).split('\n')[0] });
		}
	}
	await ctx.close();
	if (!silencioso) lecturas.forEach((u) => console.log('  ' + JSON.stringify(u)));
	return lecturas;
}

function ubicacionCorrecta(lecturas) {
	const paises = lecturas.map((u) => u.pais).filter(Boolean);
	return paises.length > 0 && paises.every((p) => PAIS_ESPERADO[VANTAGE].includes(p));
}

// --------------------------- Analisis por sitio ----------------------------
async function auditarSitio(browser, uni) {
	const ctx = await browser.newContext({ ignoreHTTPSErrors: true, userAgent: USER_AGENT });
	const page = await ctx.newPage();
	const rec = { ...uni, vantage: VANTAGE, run: parseInt(RUN, 10), red: RED,
	              ok: false, https: uni.url.startsWith('https') };

	// --- (1) Observadores de red. Se instalan ANTES de navegar. -------------
	const redPorProveedor = new Map();   // proveedor -> { peticiones, set_cookie, hosts, ejemplos }
	const dominiosTerceros = new Set();
	let cabecerasDoc = null;
	let htmlServido = null;

	const anotar = (proveedor, campo, host, url) => {
		if (!redPorProveedor.has(proveedor)) {
			redPorProveedor.set(proveedor, { peticiones: 0, respuestas: 0, set_cookie: 0,
			                                 hosts: [], ejemplos: [] });
		}
		const e = redPorProveedor.get(proveedor);
		e[campo] += 1;
		if (host && !e.hosts.includes(host)) e.hosts.push(host);
		if (url && e.ejemplos.length < 3) e.ejemplos.push(url.slice(0, 200));
	};

	page.on('request', (req) => {
		try {
			const host = new URL(req.url()).hostname;
			dominiosTerceros.add(host);
			const prov = proveedorDe(host);
			if (prov) anotar(prov, 'peticiones', host, req.url());
		} catch (e) { /* URL no analizable: se ignora */ }
	});

	page.on('response', async (res) => {
		try {
			const host = new URL(res.url()).hostname;
			const prov = proveedorDe(host);
			if (prov) {
				anotar(prov, 'respuestas', host, null);
				let cabs = [];
				try { cabs = await res.headersArray(); } catch (e) { cabs = []; }
				if (cabs.some((c) => c.name.toLowerCase() === 'set-cookie')) {
					anotar(prov, 'set_cookie', host, null);
				}
			}
		} catch (e) { /* respuesta ya descartada: se ignora */ }
	});

	let intento = 0, cargo = false, ultimoError = '';
	let respuestaDoc = null;
	while (intento <= REINTENTOS && !cargo) {
		try {
			respuestaDoc = await page.goto(uni.url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT_MS });
			cargo = true;
		} catch (e) { ultimoError = String(e).split('\n')[0]; intento++; }
	}
	if (!cargo) { rec.error = ultimoError; rec.fecha = new Date().toISOString(); await ctx.close(); return rec; }

	// --- (4) Cabeceras y cuerpo del documento principal ---------------------
	try {
		if (respuestaDoc) {
			cabecerasDoc = await respuestaDoc.allHeaders();
			try { htmlServido = await respuestaDoc.text(); } catch (e) { htmlServido = null; }
		}
	} catch (e) { cabecerasDoc = null; }

	try {
		await page.waitForTimeout(ESPERA_JS_MS);

		if (MEDIR_COOKIES) {
			const cookies = await ctx.cookies();
			const nombres = cookies.map((c) => c.name);

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
				// Scripts en linea: donde suele vivir el consent default.
				const enLinea = Array.from(document.querySelectorAll('script:not([src])'))
					.map((s) => s.textContent || '').join('\n').slice(0, 200000);
				return { blob: (src + ' ' + globalesCMP).slice(0, 20000),
				         tcf: typeof window.__tcfapi === 'function', banner: !!tieneBanner,
				         enLinea };
			});
			const cmp = CMPS.filter(([, re]) => re.test(htmlProbe.blob)).map(([n]) => n);
			if (htmlProbe.tcf && !cmp.includes('IAB-TCF')) cmp.push('IAB-TCF');

			rec.cookies = {
				total_pre: nombres.length,
				rastreo_pre: nombres.filter(esRastreoOrig).length,           // taxonomia original
				rastreo_pre_ext: nombres.filter(esRastreoExt).length,        // taxonomia extendida
				nombres_pre: nombres,
				nombres_rastreo: nombres.filter(esRastreoOrig),
				nombres_rastreo_ext: nombres.filter(esRastreoExt),
				cmp,
				banner: htmlProbe.banner
			};

			// --- (2) Consentimiento por defecto: HTML servido + scripts en linea
			rec.consentimiento_por_defecto = analizarConsentPorDefecto(
				(htmlServido || '') + '\n' + (htmlProbe.enLinea || ''));
		}

		// --- (3) Complejidad del documento. Se mide ANTES de inyectar axe,
		//         para que el propio script de axe no altere el recuento.
		rec.complejidad = await page.evaluate(() => {
			let nodosTotales = 0;
			const tw = document.createTreeWalker(document, NodeFilter.SHOW_ALL, null);
			while (tw.nextNode()) nodosTotales++;
			return {
				elementos: document.getElementsByTagName('*').length,
				nodos_totales: nodosTotales,
				profundidad_max: (function () {
					let max = 0;
					const rec2 = (el, d) => {
						if (d > max) max = d;
						for (const h of el.children) rec2(h, d + 1);
					};
					rec2(document.documentElement, 1);
					return max;
				})(),
				imagenes: document.images.length,
				enlaces: document.links.length,
				controles: document.querySelectorAll('input,select,textarea,button').length,
				iframes: document.querySelectorAll('iframe').length,
				longitud_texto: (document.body ? (document.body.innerText || '').length : 0)
			};
		});

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

		// Comprobaciones que la herramienta NO puede decidir: se detallan por
		// regla, no solo en total, porque son la medida de la cobertura del
		// verificador automatico.
		const incompletasPorRegla = ax.incomplete.map((v) => ({
			id: v.id, criterio: criterioDe(v.tags).num, nivel: nivelDe(v.tags),
			nodos: v.nodes.length
		})).sort((a, b) => b.nodos - a.nodos);
		const nodosIncompletos = incompletasPorRegla.reduce((s, r) => s + r.nodos, 0);

		let maxNivelSinFallo = 'ninguno';
		if (!nivelesConFallo.has('A')) {
			maxNivelSinFallo = 'A';
			if (!nivelesConFallo.has('AA')) {
				maxNivelSinFallo = 'AA';
				if (!nivelesConFallo.has('AAA')) maxNivelSinFallo = 'AAA';
			}
		}

		const el = (rec.complejidad && rec.complejidad.elementos) || 0;

		rec.accesibilidad = {
			title: await page.title(),
			lang: await page.evaluate(() => document.documentElement.getAttribute('lang')),
			viewport: await page.evaluate(() => !!document.querySelector('meta[name="viewport"]')),
			violaciones: ax.violations.length,
			nodos,
			nodos_por_mil_elementos: el > 0 ? +(1000 * nodos / el).toFixed(2) : null,
			porPrincipio,
			porNivel,
			maxNivelSinFallo,
			incompletos: ax.incomplete.length,
			incompletos_nodos: nodosIncompletos,
			incompletos_por_regla: incompletasPorRegla.slice(0, 25),
			passes: ax.passes.length,
			reglas: reglas.slice(0, 25)
		};

		// --- (1) Volcado del registro de red ---------------------------------
		rec.red_proveedores = Array.from(redPorProveedor.entries())
			.map(([proveedor, e]) => ({
				proveedor,
				peticion_emitida: e.peticiones > 0,
				peticiones: e.peticiones,
				respuestas: e.respuestas,
				respuestas_con_set_cookie: e.set_cookie,
				// Lectura del mecanismo, explicita para no dejarla al analisis:
				//   emitida sin Set-Cookie -> capa del proveedor
				//   nunca emitida          -> capa del sitio / CMP / gestor de etiquetas
				capa_sugerida: e.peticiones > 0
					? (e.set_cookie > 0 ? 'cookie_establecida' : 'proveedor_no_devuelve_set_cookie')
					: 'peticion_no_emitida',
				hosts: e.hosts,
				ejemplos: e.ejemplos
			}))
			.sort((a, b) => b.peticiones - a.peticiones);
		rec.dominios_terceros = Array.from(dominiosTerceros)
			.filter((h) => { try { return new URL(uni.url).hostname !== h; } catch (e) { return true; } });
		rec.n_dominios_terceros = rec.dominios_terceros.length;

		// --- (4) Pila tecnica ------------------------------------------------
		rec.pila = analizarPila(cabecerasDoc, htmlServido);

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
		'id','vantage','run','red','grupo','sigla','pais','url','ok','error','title','lang','viewport','https',
		'cookies_pre','rastreo_pre','rastreo_pre_ext','nombres_rastreo_ext','cmp','banner',
		'consent_default','consent_default_region','regiones','uet_consent','clarity_consent',
		'ax_violaciones','ax_nodos','elementos','nodos_totales','nodos_por_mil_elementos',
		'nivelA_nodos','nivelAA_nodos','nivelAAA_nodos',
		'Perceptible','Operable','Comprensible','Robusto','max_nivel_sin_fallo_auto',
		'incompletos','incompletos_nodos','n_dominios_terceros',
		'prov_emitida_sin_cookie','prov_no_emitida','servidor','cdn','cms','fecha'
	];
	const filas = [cab.join(',')];
	for (const r of res) {
		const a = r.accesibilidad || {};
		const c = r.cookies || {};
		const p = (a.porPrincipio || {});
		const n = (a.porNivel || {});
		const x = r.complejidad || {};
		const cd = r.consentimiento_por_defecto || {};
		const pl = r.pila || {};
		const redp = r.red_proveedores || [];
		const celda = (v) => {
			const s = (v === undefined || v === null) ? '' : String(v);
			return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
		};
		filas.push([
			r.id, r.vantage, r.run, r.red, r.grupo, r.sigla, r.pais, r.url, r.ok, r.error || '',
			a.title || '', a.lang || '', a.viewport ? 1 : 0, r.https ? 1 : 0,
			c.total_pre ?? '', c.rastreo_pre ?? '', c.rastreo_pre_ext ?? '',
			(c.nombres_rastreo_ext || []).join(' '),
			(c.cmp || []).join(' '), c.banner === undefined ? '' : (c.banner ? 1 : 0),
			cd.gtag_consent_default ? 1 : 0, cd.gtag_consent_default_con_region ? 1 : 0,
			(cd.regiones_declaradas || []).join(' '),
			cd.uet_consent ? 1 : 0, cd.clarity_consent ? 1 : 0,
			a.violaciones ?? '', a.nodos ?? '',
			x.elementos ?? '', x.nodos_totales ?? '', a.nodos_por_mil_elementos ?? '',
			n.A ?? '', n.AA ?? '', n.AAA ?? '',
			p.Perceptible ?? '', p.Operable ?? '', p.Comprensible ?? '', p.Robusto ?? '',
			a.maxNivelSinFallo || '', a.incompletos ?? '', a.incompletos_nodos ?? '',
			r.n_dominios_terceros ?? '',
			redp.filter((q) => q.capa_sugerida === 'proveedor_no_devuelve_set_cookie').map((q) => q.proveedor).join(' '),
			redp.filter((q) => q.capa_sugerida === 'peticion_no_emitida').map((q) => q.proveedor).join(' '),
			pl.servidor || '', (pl.cdn || []).join(' '), (pl.cms || []).join(' '),
			r.fecha || ''
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
	console.log(`  AUDITORIA MULTIPUNTO v3.0 — punto: ${VANTAGE}   pasada: ${RUN}`);
	console.log(`  Tipo de red: ${RED}${CIUDAD ? '   ciudad: ' + CIUDAD : ''}`);
	console.log(`  Sitios en la lista: ${lista.length}`);
	console.log('=======================================================\n');

	console.log('Comprobando desde que pais se esta midiendo...');
	const ubic = await comprobarUbicacion(browser, false);
	const paises = ubic.map((u) => u.pais).filter(Boolean);
	const coincide = ubicacionCorrecta(ubic);

	const meta = {
		vantage: VANTAGE,
		run: parseInt(RUN, 10),
		red: RED,
		ciudad: CIUDAD || null,
		version_auditor: '3.0',
		inicio: new Date().toISOString(),
		geolocalizacion: ubic,
		coincide_con_vantage: coincide,
		controles_de_ubicacion: [{ momento: 'inicio', sitio: 0, lecturas: ubic, correcta: coincide }],
		configuracion: { ESPERA_JS_MS, TIMEOUT_MS, REINTENTOS, INCLUIR_AAA, MEDIR_COOKIES, USER_AGENT },
		registros_nuevos: ['red_proveedores', 'consentimiento_por_defecto', 'complejidad', 'pila',
		                   'rastreo_pre_ext', 'incompletos_por_regla'],
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
			const sinCookie = (rec.red_proveedores || [])
				.filter((q) => q.capa_sugerida === 'proveedor_no_devuelve_set_cookie').length;
			const noEmitida = (rec.red_proveedores || [])
				.filter((q) => q.capa_sugerida === 'peticion_no_emitida').length;
			const ck = rec.cookies ? `cookies ${c.total_pre} (${c.rastreo_pre_ext} rastreo) | banner ${c.banner ? 'SI' : 'no'} | ` : '';
			const cdr = rec.consentimiento_por_defecto && rec.consentimiento_por_defecto.gtag_consent_default_con_region ? ' | consent-default REGION' : '';
			console.log(`OK | WCAG ${a.violaciones} viol (${a.nodos} nodos, ${a.nodos_por_mil_elementos}/mil) | ${ck}red: ${sinCookie} sin-set-cookie, ${noEmitida} no-emitida${cdr}`);
		} else {
			console.log('FALLO: ' + (rec.error || 'desconocido'));
		}
		const limpio = resultados.filter(Boolean);
		guardarJSON(limpio);
		guardarCSV(limpio);

		const esUltimo = (i === lista.length - 1);
		if (((i + 1) % CHEQUEO_CADA === 0) || esUltimo) {
			const chk = await comprobarUbicacion(browser, true);
			const bien = ubicacionCorrecta(chk);
			meta.controles_de_ubicacion.push({
				momento: esUltimo ? 'final' : 'intermedio',
				sitio: i + 1, lecturas: chk, correcta: bien
			});
			fs.writeFileSync(SALIDA_META, JSON.stringify(meta, null, 2));
			if (!bien) {
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
