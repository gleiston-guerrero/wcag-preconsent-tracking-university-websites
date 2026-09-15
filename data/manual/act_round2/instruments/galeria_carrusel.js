(async () => {
  const SOLO_CARRUSELES = true;   // false = todas las imagenes de la pagina
  const CARRUSEL = '.swiper, .swiper-container, .slick-slider, .owl-carousel, .splide, .carousel, .elementor-image-carousel, .flickity-enabled';
  const abs = u => { try { return new URL(u, location.href).href; } catch (e) { return u; } };
  const deCss = bg => { const m = (bg || '').match(/url\(["']?(.*?)["']?\)/); return m ? abs(m[1]) : ''; };
  const nombre = e => {
    const ids = e.getAttribute('aria-labelledby');
    if (ids) return ids.split(/\s+/).map(i => (document.getElementById(i) || {}).textContent || '').join(' ').trim();
    return e.getAttribute('aria-label') ?? e.getAttribute('alt') ?? e.getAttribute('title') ?? '(sin nombre)';
  };
  const ruta = e => {
    const p = [];
    for (let n = e; n && n.nodeType === 1 && p.length < 5; n = n.parentElement) {
      if (n.id) { p.unshift('#' + CSS.escape(n.id)); break; }
      p.unshift(n.tagName.toLowerCase() + [...n.classList].slice(0, 2).map(c => '.' + CSS.escape(c)).join(''));
    }
    return p.join(' > ');
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const filas = [];
  document.querySelectorAll('*').forEach(e => {
    if (SOLO_CARRUSELES && !e.closest(CARRUSEL)) return;
    let src = '';
    if (e.tagName === 'IMG') src = abs(e.currentSrc || e.getAttribute('src') || e.dataset.src || e.dataset.lazySrc || '');
    else src = deCss(getComputedStyle(e).backgroundImage) || (e.dataset.background || e.dataset.bg ? abs(e.dataset.background || e.dataset.bg) : '');
    if (!src || !(e.tagName === 'IMG' || e.getAttribute('role') === 'img' || e.hasAttribute('aria-label') || e.dataset.background || e.dataset.bg)) return;
    const r = e.getBoundingClientRect();
    filas.push({ nombre: nombre(e), src, selector: ruta(e), mostrada: Math.round(r.width) + 'x' + Math.round(r.height) + ' px',
                 clon: !!e.closest('.swiper-slide-duplicate, .slick-cloned, .cloned'), dato: '' });
  });
  for (const f of filas) {
    try { const b = await (await fetch(f.src)).blob();
          f.dato = await new Promise(ok => { const fr = new FileReader(); fr.onload = () => ok(fr.result); fr.readAsDataURL(b); }); }
    catch (e) { f.dato = f.src; }
  }
  const tarjetas = filas.map((f, i) => `<section class="${f.clon ? 'clon' : ''}"><h3>${i + 1}. ${esc(f.nombre)}</h3>
    <div class="img"><img src="${esc(f.dato)}" alt=""></div><table>
    <tr><th>nombre</th><td>${esc(f.nombre)}</td></tr><tr><th>url</th><td><a href="${esc(f.src)}">${esc(f.src)}</a></td></tr>
    <tr><th>mostrada</th><td>${esc(f.mostrada)}</td></tr><tr><th>selector</th><td>${esc(f.selector)}</td></tr>
    ${f.clon ? '<tr><th>aviso</th><td>diapositiva CLONADA por el carrusel (repeticion de otra)</td></tr>' : ''}</table></section>`).join('\n');
  const html = `<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Carrusel ${esc(location.hostname)}</title><style>
    body{font:15px/1.4 system-ui,Segoe UI,sans-serif;max-width:1000px;margin:auto;padding:1rem;background:#fafafa}
    section{background:#fff;border:1px solid #ccc;border-radius:6px;padding:.7rem 1rem;margin:1rem 0}section.clon{opacity:.6}
    h3{margin:.1rem 0 .5rem;color:#1f4e79}.img{padding:.5rem;background:repeating-conic-gradient(#e6e6e6 0 25%,#fff 0 50%) 0 0/16px 16px}
    body.oscuro .img{background:repeating-conic-gradient(#333 0 25%,#222 0 50%) 0 0/16px 16px}.img img{max-width:100%;max-height:320px;display:block}
    th{width:6rem;text-align:left;color:#555;vertical-align:top}td{word-break:break-all}#f{position:fixed;top:.5rem;right:.5rem}</style></head><body>
    <button id="f" onclick="document.body.classList.toggle('oscuro')">Fondo claro / oscuro</button>
    <h1>Imagenes de carrusel</h1><p>Pagina: ${esc(location.href)}<br>Capturado: ${new Date().toLocaleString()} &middot; ${filas.length} elementos</p>
    ${tarjetas}</body></html>`;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
  a.download = 'carrusel_' + location.hostname + '_' + new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-') + '.html';
  document.body.appendChild(a); a.click(); a.remove();
  console.table(filas.map(({ nombre, src, mostrada, clon }) => ({ nombre, src, mostrada, clon })));
})();
