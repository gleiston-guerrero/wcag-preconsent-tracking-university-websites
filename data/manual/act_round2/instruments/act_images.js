/* ===========================================================================
   act_images.js — evidencia completa de imagenes para la regla ACT qt1vmo
   ---------------------------------------------------------------------------
   Complementa a act_recode. Aquel guardaba solo los ultimos 70 caracteres
   del src, lo que dejo 108 de 201 direcciones truncadas y 50 sin direccion
   alguna. Este script recoge la evidencia completa:

     - src y currentSrc sin truncar, resueltos a URL absoluta
     - srcset, para saber que variante se estaba sirviendo
     - background-image de CSS, que es como los carruseles de Elementor
       colocan sus imagenes y por eso no tenian src
     - el marcado completo de los svg en linea, que tampoco tienen src
     - las dimensiones representadas, utiles para distinguir un icono
       decorativo de una fotografia de contenido

   Solo recorre elementos APLICABLES a qt1vmo segun la regla: img, canvas y svg
   visibles, con nombre accesible no vacio, no ocultos programaticamente y sin
   un ascendiente nombrado por el autor. La aplicabilidad se decide igual que
   en act_recodificar, de modo que las filas se corresponden una a una.

   USO: abrir la portada, cerrar el aviso de cookies si lo hay, F12, Consola,
   pegar y Enter. Se descarga un CSV.
   =========================================================================== */

(async () => {
'use strict';

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
const SITIO = Object.assign({ id: '', grupo: '', sigla: '' }, clave ? CENSO[clave] : {});
if (!clave) console.warn('AVISO: este dominio no esta en la submuestra de quince sitios.');
else console.log(`Sitio reconocido: ${SITIO.sigla} (id ${SITIO.id})`);

const EVALUADOR = 'R02';
const FECHA = new Date().toISOString().slice(0, 10);

/* --- mismos criterios de aplicabilidad que act_recode --------------- */

const SEL_CMP = [
	'.cky-consent-container', '.cky-preference-center', '.cky-modal', '#cookieyes',
	'#onetrust-consent-sdk', '#onetrust-banner-sdk', '#onetrust-pc-sdk',
	'#CybotCookiebotDialog', '.cmplz-cookiebanner', '#cmplz-cookiebanner-container',
	'#cookiescript_injected', '.cc-window', '#tarteaucitronRoot',
	'[class^="cky-"]', '[id^="cky"]', '[class^="cmplz-"]', '[id^="cmplz-"]',
	'[id^="CybotCookiebot"]', '[id^="onetrust-"]', '[class^="tarteaucitron"]'
].join(',');
const CAND = [...document.querySelectorAll(SEL_CMP)]
	.filter(e => !['STYLE', 'SCRIPT', 'LINK', 'NOSCRIPT', 'META'].includes(e.tagName));
const CMPS = CAND.filter(e => !CAND.some(o => o !== e && o.contains(e)));
const enCMP = el => CMPS.some(c => c.contains(el));

const ocultoProgramaticamente = el => {
	if (el.getAttribute('aria-hidden') === 'true' || el.hasAttribute('hidden')) return true;
	let n = el;
	while (n && n !== document.body) {
		const s = getComputedStyle(n);
		if (s.display === 'none' || s.visibility === 'hidden') return true;
		if (n.getAttribute && n.getAttribute('aria-hidden') === 'true') return true;
		n = n.parentElement;
	}
	return false;
};

const nombreAccesible = el => {
	const lb = el.getAttribute('aria-labelledby');
	if (lb) {
		const t = lb.split(/\s+/).map(id => {
			const r = document.getElementById(id); return r ? r.textContent.trim() : '';
		}).join(' ').trim();
		if (t) return t;
	}
	const al = el.getAttribute('aria-label');
	if (al && al.trim()) return al.trim();
	if (el.tagName === 'IMG') { const a = el.getAttribute('alt'); if (a !== null) return a.trim(); }
	if (el.tagName.toLowerCase() === 'svg') { const t = el.querySelector('title'); if (t) return t.textContent.trim(); }
	const txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
	if (txt) return txt;
	const ti = el.getAttribute('title');
	return ti ? ti.trim() : '';
};

const selector = el => {
	if (el.id) return `#${el.id}`;
	const p = []; let n = el;
	for (let i = 0; n && n.nodeType === 1 && i < 4; i++) {
		let s = n.tagName.toLowerCase();
		if (n.className && typeof n.className === 'string') {
			const c = n.className.trim().split(/\s+/)[0]; if (c) s += '.' + c;
		}
		p.unshift(s); n = n.parentElement;
	}
	return p.join(' > ');
};

const abs = u => { try { return new URL(u, location.href).href; } catch (e) { return u || ''; } };

/* --- disparo de la carga diferida --------------------------------------
   Elementor y otros constructores sirven un marcador vacio del tamano
   correcto -- por ejemplo <svg viewBox='0 0 400 400'></svg> -- y solo cargan
   la imagen real cuando el elemento entra en el viewport. Si se mide antes,
   se captura el marcador y no la fotografia. Este barrido recorre la pagina
   entera, espera a que las imagenes terminen de decodificarse y vuelve al
   inicio. Sin el, 22 de las 27 imagenes de un sitio resultaron ser marcadores
   vacios. */

const dormir = ms => new Promise(r => setTimeout(r, ms));

console.log('Recorriendo la pagina para disparar la carga diferida...');
const alturaTotal = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
const paso = Math.round(innerHeight * 0.8);
for (let y = 0; y < alturaTotal; y += paso) {
	scrollTo(0, y);
	await dormir(320);
}
scrollTo(0, alturaTotal);
await dormir(900);
scrollTo(0, 0);
await dormir(600);

/* Se fuerza la decodificacion de todo lo que siga pendiente y se espera a que
   las imagenes que aun no han terminado de cargar lo hagan, con un tope para
   no quedarse bloqueado en una que nunca llegue. */
const pendientes = [...document.images].filter(im => !im.complete);
console.log(`Esperando a ${pendientes.length} imagen(es) que aun cargaban...`);
await Promise.race([
	Promise.allSettled(pendientes.map(im => im.decode().catch(() => {}))),
	dormir(8000)
]);
await dormir(400);

/* Cuantos marcadores vacios quedan, para que el problema no vuelva a pasar
   inadvertido. */
const huecos = [...document.querySelectorAll('svg')]
	.filter(e => e.children.length === 0 && !(e.textContent || '').trim()).length;
console.log(`SVG vacios restantes en la pagina: ${huecos}`);

/* --- recorrido ---------------------------------------------------------- */

const filas = [];
let n = 0;

[...document.querySelectorAll('img, canvas, svg, [role="img"]')]
	.filter(e => !enCMP(e))
	.forEach(el => {
		n++;
		if (ocultoProgramaticamente(el)) return;                 // e88epe, inaplicable
		const rol = (el.getAttribute('role') || '').toLowerCase();
		if (rol === 'none' || rol === 'presentation') return;    // decorativa declarada
		if (el.tagName === 'IMG' && el.getAttribute('alt') === '') return;
		const nombre = nombreAccesible(el);
		if (!nombre) return;                                     // falla 23a2a8, no llega a qt1vmo

		const cs = getComputedStyle(el);
		const r = el.getBoundingClientRect();

		// origen de la imagen, por orden de fiabilidad
		let src = '', origen = '';
		if (el.currentSrc) { src = abs(el.currentSrc); origen = 'currentSrc'; }
		else if (el.getAttribute && el.getAttribute('src')) { src = abs(el.getAttribute('src')); origen = 'src'; }
		if (!src) {
			// background-image, propio o del ascendiente inmediato (patron de Elementor)
			for (const cand of [el, el.parentElement, el.parentElement && el.parentElement.parentElement]) {
				if (!cand) continue;
				const bi = getComputedStyle(cand).backgroundImage;
				const m = bi && bi.match(/url\(["']?([^"')]+)["']?\)/);
				if (m) { src = abs(m[1]); origen = 'background-image de ' + (cand === el ? 'el mismo' : selector(cand)); break; }
			}
		}
		let svgMarkup = '', marcadorVacio = '';
		if (el.tagName.toLowerCase() === 'svg') {
			svgMarkup = el.outerHTML.replace(/\s+/g, ' ').slice(0, 1500);
			origen = origen || 'svg en linea';
			if (el.children.length === 0 && !(el.textContent || '').trim()) marcadorVacio = 'SI';
		}
		if (/^data:image\/svg\+xml/.test(src) && /viewBox=[^>]*><\/svg>/.test(decodeURIComponent(src))) marcadorVacio = 'SI';

		filas.push({
			id: SITIO.id, grupo: SITIO.grupo, sigla: SITIO.sigla, url_pagina: location.href,
			criterio: '1.1.1', regla_act: 'qt1vmo', elemento_n: n,
			etiqueta: el.tagName.toLowerCase(),
			selector: selector(el),
			nombre_accesible: nombre,
			origen_nombre: el.getAttribute('aria-label') ? 'aria-label'
				: (el.getAttribute('aria-labelledby') ? 'aria-labelledby'
				: (el.tagName === 'IMG' ? 'alt' : 'otro')),
			src_completo: src,
			origen_src: origen,
			srcset: (el.getAttribute && el.getAttribute('srcset')) ? el.getAttribute('srcset').slice(0, 400) : '',
			ancho_css: Math.round(r.width), alto_css: Math.round(r.height),
			ancho_natural: el.naturalWidth || '', alto_natural: el.naturalHeight || '',
			enlace_contenedor: (() => { const a = el.closest('a'); return a ? abs(a.getAttribute('href') || '') : ''; })(),
			texto_proximo: (() => {
				const c = el.closest('figure, li, p, article, section, div');
				return c ? (c.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 200) : '';
			})(),
			svg_markup: svgMarkup, marcador_vacio: marcadorVacio,
			evaluador_cod: EVALUADOR, fecha: FECHA,
			resultado_RELLENAR: '', justificacion_RELLENAR: ''
		});
	});

/* --- salida ------------------------------------------------------------- */

if (!filas.length) { console.error('ABORTADO: ninguna imagen aplicable a qt1vmo.'); return; }

const cols = Object.keys(filas[0]);
const esc = v => { const s = v == null ? '' : String(v); return /[",\n;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
const csv = '\ufeff' + cols.join(',') + '\n' + filas.map(f => cols.map(c => esc(f[c])).join(',')).join('\n');

const sinSrc = filas.filter(f => !f.src_completo && !f.svg_markup).length;
const resumen = `IMG|v1 sitio=${SITIO.sigla || 'DESCONOCIDO'} id=${SITIO.id} host=${location.hostname} fecha=${FECHA} aplicables_qt1vmo=${filas.length} con_src=${filas.filter(f => f.src_completo).length} svg_en_linea=${filas.filter(f => f.svg_markup).length} sin_origen=${sinSrc} marcadores_vacios=${filas.filter(f=>f.marcador_vacio).length} svg_vacios_en_pagina=${huecos}`;
console.log('\n' + '='.repeat(78));
console.log(resumen);
console.log('='.repeat(78));
try { copy(resumen); console.log('(Copiado al portapapeles.)'); } catch (e) {}

const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
a.download = `img_${location.hostname.replace(/\W+/g, '_')}_${FECHA}.csv`;
document.body.appendChild(a); a.click(); a.remove();
})();
