/* ===========================================================================
   act_recode.js — recoding ACT de 1.1.1, 1.4.3 y 2.4.4
   ---------------------------------------------------------------------------
   Se pega en la consola del navegador, con la pagina cargada y SIN haber
   interactuado con ningun aviso de cookies.

   Que hace y que NO hace. Esta es la parte importante.

   El script decide por si solo todo lo que la regla ACT define de forma
   mecanica: que elemento es APLICABLE, y el resultado de las expectativas que
   son comprobables por codigo. Deja marcado como REVISAR, con toda la
   informacion necesaria al lado, unicamente lo que la regla remite al juicio
   humano: si un nombre accesible es descriptivo (qt1vmo) y si un enlace se
   entiende con su contexto programatico (5effbb).

   No inventa un veredicto donde la regla pide criterio. Ese es el punto: el
   desacuerdo entre codificadores no estaba en el juicio, estaba en decidir que
   se miraba. Eso ya no lo decide la persona.

   Reglas implementadas:
     1.1.1  23a2a8  imagen con nombre accesible no vacio
            qt1vmo  nombre accesible de imagen descriptivo        -> REVISAR
            e88epe  imagen fuera del arbol de accesibilidad es decorativa
     1.4.3  afw4f7  texto con contraste minimo
     2.4.4  c487ae  enlace con nombre accesible no vacio
            5effbb  enlace descriptivo en su contexto             -> REVISAR
            fd3a94  nombres identicos, mismo contexto             -> REVISAR

   USO:
     1. Abrir la pagina. No interactuar con nada.
     2. F12, pestana Console.
     3. Pegar este archivo entero y pulsar Enter.
     4. Se descarga un CSV con una fila por elemento aplicable.
     5. Rellenar a mano solo las filas marcadas REVISAR.
   =========================================================================== */

(() => {
'use strict';

/* Identificacion del sitio. Se rellena sola a partir del censo de los 15
   sitios de la submuestra; si la pagina no es ninguno de ellos, quedan vacios
   y los rellena usted a mano en el CSV. */
const CENSO = {
	'berkeley.edu':      { id: 7,   grupo: 'mundo',   sigla: 'UC Berkeley'  },
	'ucl.ac.uk':         { id: 14,  grupo: 'mundo',   sigla: 'UCL'          },
	'cornell.edu':       { id: 15,  grupo: 'mundo',   sigla: 'Cornell'      },
	'nus.edu.sg':        { id: 22,  grupo: 'mundo',   sigla: 'NUS'          },
	'northwestern.edu':  { id: 29,  grupo: 'mundo',   sigla: 'Northwestern' },
	'manchester.ac.uk':  { id: 40,  grupo: 'mundo',   sigla: 'Manchester'   },
	'hkust.edu.hk':      { id: 58,  grupo: 'mundo',   sigla: 'HKUST'        },
	'unesum.edu.ec':     { id: 83,  grupo: 'ecuador', sigla: 'UNESUM'       },
	'usecipol.edu.ec':   { id: 95,  grupo: 'ecuador', sigla: 'USECIPOL'     },
	'iaen.edu.ec':       { id: 96,  grupo: 'ecuador', sigla: 'IAEN'         },
	'ulvr.edu.ec':       { id: 102, grupo: 'ecuador', sigla: 'ULVR'         },
	'utpl.edu.ec':       { id: 103, grupo: 'ecuador', sigla: 'UTPL'         },
	'ups.edu.ec':        { id: 106, grupo: 'ecuador', sigla: 'UPS'          },
	'indoamerica.edu.ec':{ id: 114, grupo: 'ecuador', sigla: 'UTI'          },
	'ecotec.edu.ec':     { id: 124, grupo: 'ecuador', sigla: 'ECOTEC'       }
};
const host = location.hostname.replace(/^www\./, '');
const clave = Object.keys(CENSO).find(k => host === k || host.endsWith('.' + k));
const SITIO = Object.assign({ id: '', grupo: '', sigla: '' },
	clave ? CENSO[clave] : {}, { url: location.href });
if (!clave) console.warn('AVISO: este dominio no esta en la submuestra de 15 sitios. Rellene id, grupo y sigla a mano en el CSV.');
else console.log(`Sitio reconocido: ${SITIO.sigla} (id ${SITIO.id}, grupo ${SITIO.grupo})`);

const EVALUADOR = 'R02';                 // <-- cambielo por su codigo de evaluador
const FECHA = new Date().toISOString().slice(0, 10);
const filas = [];

/* Contenedores de gestores de consentimiento (CMP). Su contenido esta en el DOM
   pero no forma parte de la pagina evaluada: es interfaz del gestor, no
   contenido de la institucion. Se excluye del recuento en lugar de listarlo
   como no aplicable, que inflaba los ficheros con cientos de filas inutiles. */
const SEL_CMP = [
	'.cky-consent-container', '.cky-preference-center', '.cky-modal', '#cookieyes',
	'#onetrust-consent-sdk', '#onetrust-banner-sdk', '#onetrust-pc-sdk', '.ot-sdk-container',
	'#CybotCookiebotDialog', '#cookiebanner',
	'.cmplz-cookiebanner', '#cmplz-cookiebanner-container',
	'#cookiescript_injected', '.cc-window', '#tarteaucitronRoot',
	'#cookie-law-info-bar', '.cli-modal', '#hs-eu-cookie-confirmation',
	'#usercentrics-root', '#didomi-host', '#truste-consent-track',
	'#gdpr-cookie-message', '.termsfeed-com---nb', '#axeptio_overlay',
	/* Prefijos de clase e id propios de cada gestor. Son necesarios porque el
	   panel de preferencias suele ser hermano del aviso y no descendiente
	   suyo: en CookieYes, .cky-preference-center y .cky-audit-table cuelgan
	   del body, no de .cky-consent-container. Un selector de contenedor solo
	   deja fuera cientos de elementos que no son contenido del sitio. */
	'[class^="cky-"]', '[id^="cky"]', '[id^="ckyPreference"]',
	'[class^="ot-"]', '[id^="onetrust-"]',
	'[class^="cmplz-"]', '[id^="cmplz-"]',
	'[class^="cli-"]', '[id^="cookie-law-info"]',
	'[id^="CybotCookiebot"]', '[class^="CybotCookiebot"]',
	'[class^="cookiescript"]', '[id^="cookiescript"]',
	'[class^="tarteaucitron"]', '[id^="tarteaucitron"]',
	'[class^="didomi-"]', '[id^="didomi-"]',
	'[class^="uc-"]', '[id^="usercentrics"]'
].join(',');

/* Deteccion del gestor de consentimiento.

   Tres cautelas aprendidas a base de fallos:

   1. Se excluyen style, script, link y noscript. Su textContent es codigo, no
      texto de la pagina, y contarlo falseaba cualquier proporcion.
   2. No se aplica ningun umbral de proporcion de texto. El panel de auditoria
      de CookieYes contiene legitimamente mas texto que la portada: un umbral
      descartaba justo el contenedor que habia que excluir.
   3. Se conservan solo los contenedores externos. Un panel con cientos de
      descendientes contaba como cientos de contenedores.
*/
const CANDIDATOS = [...document.querySelectorAll(SEL_CMP)]
	.filter(e => !['STYLE', 'SCRIPT', 'LINK', 'NOSCRIPT', 'META'].includes(e.tagName));
const CMPS = CANDIDATOS.filter(e => !CANDIDATOS.some(o => o !== e && o.contains(e)));

const nCMP = CMPS.length;
const nDescartados = CMPS.reduce((a, c) => a + 1 + c.querySelectorAll('*').length, 0);
console.log(`Gestor de consentimiento: ${nCMP} contenedor(es) externo(s), ${nDescartados} elementos del DOM excluidos del recuento.`);
CMPS.forEach(e => console.log(`   excluido: ${e.tagName}${e.id ? '#' + e.id : ''}${(e.className && typeof e.className === 'string') ? '.' + e.className.trim().split(/\s+/)[0] : ''} (${e.querySelectorAll('*').length} descendientes)`));

/* Un aviso de cookies abierto ocupa una parte apreciable de la ventana y esta
   fijado o superpuesto. Un icono de chat o una barra de redes sociales tambien
   son visibles y no son un modal: por eso se exige superficie y posicionamiento,
   no solo visibilidad. */
const modalVisible = CMPS.some(e => {
	const r = e.getBoundingClientRect();
	const st = getComputedStyle(e);
	if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return false;
	if (r.width < 200 || r.height < 80) return false;
	const areaVentana = innerWidth * innerHeight;
	if ((r.width * r.height) / areaVentana < 0.06) return false;
	return ['fixed', 'sticky', 'absolute'].includes(st.position) || parseInt(st.zIndex, 10) > 100;
});

const ESTADO_MODAL = nCMP === 0 ? 'sin CMP detectada'
	: (modalVisible ? 'MODAL ABIERTO' : 'modal cerrado');
console.log(`Estado del aviso: ${ESTADO_MODAL}`);
if (modalVisible) console.warn('AVISO: hay un aviso de consentimiento visible y de tamano apreciable. Cierrelo y vuelva a run.');

const enCMP = el => CMPS.some(c => c.contains(el));

/* --- utilidades comunes ------------------------------------------------- */

const visible = el => {
	if (!el || !el.getClientRects) return false;
	const s = getComputedStyle(el);
	if (s.display === 'none' || s.visibility === 'hidden' || s.visibility === 'collapse') return false;
	if (parseFloat(s.opacity) === 0) return false;
	const r = el.getBoundingClientRect();
	if (r.width === 0 || r.height === 0) return false;
	// texto oculto visualmente: clip, indentado fuera de pantalla, tamano cero
	if (parseFloat(s.fontSize) === 0) return false;
	if (parseFloat(s.textIndent) < -999) return false;
	const clip = s.clip || s.clipPath || '';
	if (/rect\(\s*0(px)?[, ]/.test(clip) || clip === 'inset(50%)') return false;
	if (r.width <= 1 && r.height <= 1) return false;
	return true;
};

const ocultoProgramaticamente = el => {
	if (el.getAttribute('aria-hidden') === 'true') return true;
	if (el.hasAttribute('hidden')) return true;
	let n = el;
	while (n && n !== document.body) {
		const s = getComputedStyle(n);
		if (s.display === 'none' || s.visibility === 'hidden') return true;
		if (n.getAttribute && n.getAttribute('aria-hidden') === 'true') return true;
		n = n.parentElement;
	}
	return false;
};

// nombre accesible, aproximacion al algoritmo accname en el orden que aplica
// a imagenes y enlaces. No cubre todos los casos del estandar.
const nombreAccesible = el => {
	const lb = el.getAttribute('aria-labelledby');
	if (lb) {
		const t = lb.split(/\s+/).map(id => {
			const r = document.getElementById(id);
			return r ? r.textContent.trim() : '';
		}).join(' ').trim();
		if (t) return t;
	}
	const al = el.getAttribute('aria-label');
	if (al && al.trim()) return al.trim();
	if (el.tagName === 'IMG' || el.tagName === 'AREA' || el.tagName === 'INPUT') {
		const alt = el.getAttribute('alt');
		if (alt !== null) return alt.trim();
	}
	if (el.tagName === 'SVG' || el.tagName === 'svg') {
		const t = el.querySelector('title');
		if (t) return t.textContent.trim();
	}
	const txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
	if (txt) return txt;
	const ti = el.getAttribute('title');
	return ti ? ti.trim() : '';
};

const selector = el => {
	if (el.id) return `#${el.id}`;
	const partes = [];
	let n = el;
	for (let i = 0; n && n.nodeType === 1 && i < 4; i++) {
		let s = n.tagName.toLowerCase();
		if (n.className && typeof n.className === 'string') {
			const c = n.className.trim().split(/\s+/)[0];
			if (c) s += '.' + c;
		}
		partes.unshift(s);
		n = n.parentElement;
	}
	return partes.join(' > ');
};

const esc = v => {
	const s = (v === null || v === undefined) ? '' : String(v);
	return /[",\n;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
};

const fila = o => filas.push(Object.assign({
	id: SITIO.id, grupo: SITIO.grupo, sigla: SITIO.sigla, url: SITIO.url,
	criterio: '', regla_act: '', regla_nombre: '', elemento_n: '',
	selector_o_descripcion: '', aplicable: '', resultado: '', valor_medido: '',
	contexto_programatico: '', evaluador_cod: EVALUADOR, fecha: FECHA,
	captura: '', observacion: '', estado_modal: ESTADO_MODAL
}, o));

/* --- 1.4.3  afw4f7  contraste minimo ------------------------------------ */

const luminancia = ([r, g, b]) => {
	const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
	return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
const rgb = s => {
	const m = (s || '').match(/rgba?\(([^)]+)\)/);
	if (!m) return null;
	const p = m[1].split(',').map(x => parseFloat(x.trim()));
	return { c: [p[0], p[1], p[2]], a: p.length > 3 ? p[3] : 1 };
};
const fondoEfectivo = el => {
	let n = el;
	while (n && n !== document.documentElement) {
		const b = rgb(getComputedStyle(n).backgroundColor);
		if (b && b.a > 0) return b.c;
		n = n.parentElement;
	}
	return [255, 255, 255];
};
const ratio = (a, b) => {
	const l1 = luminancia(a), l2 = luminancia(b);
	return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
};

(() => {
	const R = 'afw4f7', N = 'Text has minimum contrast';
	const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
	const vistos = new Set();
	let n = 0, fallos = 0;
	let nodo;
	while ((nodo = w.nextNode())) {
		const t = nodo.nodeValue.replace(/\s+/g, ' ').trim();
		if (!t) continue;
		const el = nodo.parentElement;
		if (!el || vistos.has(el)) continue;
		vistos.add(el);
		if (['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue;
		if (enCMP(el)) continue;                     // interfaz del gestor de consentimiento

		if (!visible(el)) {
			fila({ criterio: '1.4.3', regla_act: R, regla_nombre: N, elemento_n: ++n,
				selector_o_descripcion: selector(el), aplicable: 'no',
				observacion: 'No es un caracter visible: la regla no aplica. Texto oculto visualmente, de tamano cero o desplazado fuera de pantalla.' });
			continue;
		}
		const s = getComputedStyle(el);
		const fg = rgb(s.color);
		if (!fg) continue;
		const bg = fondoEfectivo(el);
		const px = parseFloat(s.fontSize);
		const bold = parseInt(s.fontWeight, 10) >= 700;
		const grande = px >= 24 || (bold && px >= 18.66);
		const umbral = grande ? 3.0 : 4.5;
		const r = ratio(fg.c, bg);
		const ok = r >= umbral - 0.005;
		if (!ok) fallos++;
		fila({ criterio: '1.4.3', regla_act: R, regla_nombre: N, elemento_n: ++n,
			selector_o_descripcion: selector(el), aplicable: 'si',
			resultado: ok ? 'cumple' : 'falla',
			valor_medido: r.toFixed(2) + ':1',
			observacion: `umbral ${umbral}:1 (${grande ? 'texto grande' : 'texto normal'}, ${px.toFixed(1)}px${bold ? ' negrita' : ''}); texto: "${t.slice(0, 60)}"` });
	}
	console.log(`1.4.3  afw4f7 : ${n} elementos, ${fallos} fallan`);
})();

/* --- 1.1.1  23a2a8 / qt1vmo / e88epe ------------------------------------ */

(() => {
	const els = [...document.querySelectorAll('img, canvas, svg, [role="img"]')].filter(e => !enCMP(e));
	let n = 0, fallos = 0, revisar = 0;
	els.forEach(el => {
		n++;
		const sel = selector(el);
		if (ocultoProgramaticamente(el)) {
			fila({ criterio: '1.1.1', regla_act: 'e88epe', regla_nombre: 'Image not in the accessibility tree is decorative',
				elemento_n: n, selector_o_descripcion: sel, aplicable: 'no',
				observacion: 'Fuera del arbol de accesibilidad: se trata como decorativa.' });
			return;
		}
		const rol = (el.getAttribute('role') || '').toLowerCase();
		const nombre = nombreAccesible(el);
		const decorativa = rol === 'none' || rol === 'presentation' ||
			(el.tagName === 'IMG' && el.getAttribute('alt') === '');
		if (decorativa) {
			fila({ criterio: '1.1.1', regla_act: '23a2a8', regla_nombre: 'Image has non-empty accessible name',
				elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'cumple',
				observacion: 'Marcada como decorativa: alt vacio o rol none/presentation. La expectativa lo admite.' });
			return;
		}
		if (!nombre) {
			fallos++;
			fila({ criterio: '1.1.1', regla_act: '23a2a8', regla_nombre: 'Image has non-empty accessible name',
				elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'falla',
				observacion: 'Sin nombre accesible y sin rol none/presentation.' });
			return;
		}
		fila({ criterio: '1.1.1', regla_act: '23a2a8', regla_nombre: 'Image has non-empty accessible name',
			elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'cumple',
			observacion: `nombre accesible: "${nombre.slice(0, 80)}"` });
		revisar++;
		fila({ criterio: '1.1.1', regla_act: 'qt1vmo', regla_nombre: 'Image accessible name is descriptive',
			elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'REVISAR',
			observacion: `JUICIO HUMANO. ¿El nombre sirve un proposito equivalente al contenido no textual? nombre: "${nombre.slice(0, 120)}" | src: ${(el.currentSrc || el.src || '').slice(-70)}` });
	});
	console.log(`1.1.1  imagenes: ${n} elementos, ${fallos} sin nombre, ${revisar} pendientes de juicio`);
})();

/* --- 2.4.4  c487ae / 5effbb / fd3a94 ------------------------------------ */

(() => {
	const CTX = 'P, LI, TD, TH, DD, DT, FIGCAPTION, BLOCKQUOTE';
	const contextoProgramatico = a => {
		const c = a.closest(CTX);
		if (!c) return '';
		const t = (c.textContent || '').replace(/\s+/g, ' ').trim();
		return t.slice(0, 160);
	};
	const enlaces = [...document.querySelectorAll('a[href], [role="link"]')]
		.filter(a => !ocultoProgramaticamente(a) && !enCMP(a));
	const porNombre = {};
	let n = 0, fallos = 0, revisar = 0;
	enlaces.forEach(a => {
		n++;
		const sel = selector(a);
		const nombre = nombreAccesible(a);
		if (!nombre) {
			fallos++;
			fila({ criterio: '2.4.4', regla_act: 'c487ae', regla_nombre: 'Link has non-empty accessible name',
				elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'falla',
				observacion: `href: ${(a.getAttribute('href') || '').slice(0, 80)}` });
			return;
		}
		fila({ criterio: '2.4.4', regla_act: 'c487ae', regla_nombre: 'Link has non-empty accessible name',
			elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'cumple',
			observacion: `nombre: "${nombre.slice(0, 80)}"` });

		const ctx = contextoProgramatico(a);
		revisar++;
		fila({ criterio: '2.4.4', regla_act: '5effbb', regla_nombre: 'Link in context is descriptive',
			elemento_n: n, selector_o_descripcion: sel, aplicable: 'si', resultado: 'REVISAR',
			contexto_programatico: ctx || 'SIN CONTEXTO PROGRAMATICO',
			observacion: `JUICIO HUMANO. ¿Nombre + contexto describen el proposito? nombre: "${nombre.slice(0, 80)}" | href: ${(a.getAttribute('href') || '').slice(0, 60)}${ctx ? '' : ' | AVISO: no hay parrafo, elemento de lista ni celda que lo contenga. Un div o article envolvente NO es contexto programatico.'}` });

		const k = nombre.toLowerCase() + '||' + ctx;
		(porNombre[k] = porNombre[k] || []).push({ n, sel, href: a.href });
	});
	Object.entries(porNombre).forEach(([k, v]) => {
		if (v.length < 2) return;
		const destinos = new Set(v.map(x => x.href));
		if (destinos.size < 2) return;
		fila({ criterio: '2.4.4', regla_act: 'fd3a94',
			regla_nombre: 'Links with identical accessible names and same context serve equivalent purpose',
			elemento_n: v.map(x => x.n).join('+'), selector_o_descripcion: v.map(x => x.sel).join(' ; '),
			aplicable: 'si', resultado: 'REVISAR',
			contexto_programatico: k.split('||')[1],
			observacion: `JUICIO HUMANO. ${v.length} enlaces con el mismo nombre accesible y el mismo contexto apuntan a ${destinos.size} destinos distintos. ¿Sirven un proposito equivalente? destinos: ${[...destinos].map(d => d.slice(-50)).join(' | ')}` });
	});
	console.log(`2.4.4  enlaces : ${n} elementos, ${fallos} sin nombre, ${revisar} pendientes de juicio`);
})();

/* --- salida ------------------------------------------------------------- */

if (filas.length === 0) {
	console.error('ABORTADO: no se ha generado ninguna fila. Revise si un selector de CMP esta capturando la pagina entera, o si la pagina no habia terminado de cargar. No se descarga ningun CSV.');
	return;
}

const cols = ['id','grupo','sigla','url','criterio','regla_act','regla_nombre','elemento_n',
	'selector_o_descripcion','aplicable','resultado','valor_medido','contexto_programatico',
	'evaluador_cod','fecha','captura','observacion','estado_modal'];
const csv = '\ufeff' + cols.join(',') + '\n' +
	filas.map(f => cols.map(c => esc(f[c])).join(',')).join('\n');

const pend = filas.filter(f => f.resultado === 'REVISAR').length;
const cnt = c => filas.filter(f => f.criterio === c).length;
const res = (c, r) => filas.filter(f => f.criterio === c && f.resultado === r).length;
const apl = (c, a) => filas.filter(f => f.criterio === c && f.aplicable === a).length;

/* Bloque de resumen en una sola linea, pensado para pegarlo tal cual en la
   conversacion. Contiene todo lo necesario para verificar la ejecucion sin
   abrir el CSV. */
const resumen = [
	'ACT|v5',
	`sitio=${SITIO.sigla || 'DESCONOCIDO'}`,
	`id=${SITIO.id}`,
	`grupo=${SITIO.grupo}`,
	`host=${location.hostname}`,
	`fecha=${FECHA}`,
	`evaluador=${EVALUADOR}`,
	`cmp_contenedores=${nCMP}`,
	`cmp_elementos_excluidos=${nDescartados}`,
	`modal=${ESTADO_MODAL}`,
	`filas=${filas.length}`,
	`143=${cnt('1.4.3')}(ap${apl('1.4.3','si')}/noap${apl('1.4.3','no')}/falla${res('1.4.3','falla')})`,
	`111=${cnt('1.1.1')}(ap${apl('1.1.1','si')}/noap${apl('1.1.1','no')}/falla${res('1.1.1','falla')})`,
	`244=${cnt('2.4.4')}(ap${apl('2.4.4','si')}/noap${apl('2.4.4','no')}/falla${res('2.4.4','falla')})`,
	`cumple=${filas.filter(f => f.resultado === 'cumple').length}`,
	`falla=${filas.filter(f => f.resultado === 'falla').length}`,
	`revisar=${pend}`
].join(' ');

console.log('\n' + '='.repeat(78));
console.log(resumen);
console.log('='.repeat(78));
console.log('Copie la linea de arriba y peguela en la conversacion.');
console.log(`Quedan ${pend} filas marcadas REVISAR: rellene su columna resultado con cumple o falla. Sin categoria intermedia.`);

try { copy(resumen); console.log('(La linea se ha copiado al portapapeles.)'); } catch (e) {}

const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
const sufijo = modalVisible ? 'MODALABIERTO' : 'ok';
a.download = `act_${location.hostname.replace(/\W+/g, '_')}_${FECHA}_${sufijo}.csv`;
document.body.appendChild(a); a.click(); a.remove();

window.__actFilas = filas;   // por si quiere inspeccionarlas en consola
})();
