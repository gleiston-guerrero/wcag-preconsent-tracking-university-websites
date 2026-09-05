# WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites

Datos, evidencia y cÃ³digo del artÃ­culo *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, sometido a *Universal Access in the Information Society* (Springer Nature).

**DOI del depÃ³sito:** `10.5281/zenodo.XXXXXXX` *(pendiente hasta la publicaciÃ³n del registro en Zenodo)*

---

## QuÃ© contiene

El estudio mide dos barreras sobre 126 portadas universitarias: 63 instituciones ecuatorianas, que constituyen el censo completo del sistema, y 63 instituciones de referencia obtenidas del consenso de tres rankings internacionales. La primera barrera es la conformidad con WCAG 2.2, auditada con axe-core 4.13.0 sobre un navegador real. La segunda es el depÃ³sito de cookies de rastreo antes de cualquier interacciÃ³n con una interfaz de consentimiento.

El depÃ³sito contiene **dos mediciones distintas que no deben mezclarse**:

**AuditorÃ­a de pasada Ãºnica**, 14 de agosto de 2026. Una sola visita a cada uno de los 126 sitios, desde un punto de observaciÃ³n en Ecuador. Es la fuente de todas las cifras de accesibilidad y de la comparaciÃ³n entre grupos. Archivo canÃ³nico: `data/raw/accessibility/resultados.json`.

**RÃ©plica multipunto**, 15 de agosto de 2026. El mismo protocolo repetido desde cuatro ubicaciones geogrÃ¡ficas, con tres pasadas vÃ¡lidas en cada una. Es la fuente del contraste entre jurisdicciones. Archivos en `data/raw/tracking/`.

Las dos difieren en fecha, en conjunto de sitios retenidos y en regla de consolidaciÃ³n. El artÃ­culo lo advierte de forma expresa: las cifras de rastreo de una y otra no son intercambiables. `CODEBOOK.md` detalla la relaciÃ³n entre ellas.

---

## Estructura

```
data/
  raw/
    accessibility/    resultados.json, resultados.csv
                      Pasada Ãºnica, 126 sitios, 14 de agosto de 2026.
    census/           universidades.json  censo de los 126 sitios auditados
                      tops.json           top 75 de cada edicion de ranking
                      seleccion63_mundo.json  consenso que define el grupo de referencia
    tracking/         39 archivos de la replica multipunto reportada:
                        resultados_{EC,EU,GB,US}_r*.{json,csv}
                        meta_*.json  IP publica, geolocalizacion y versiones por pasada
    tracking_extended/  48 archivos de una campana posterior de cinco puntos,
                        con Suiza, NO analizada en el articulo. Ver mas abajo.
  processed/          once tablas derivadas; ver CODEBOOK.md
  interim/            se crea al ejecutar el codigo; no se versiona
code/
  collection/         auditar.js             auditoria de pasada unica
                      auditar_multipunto.js  auditoria por punto de observacion
                      ejecutar.bat, INSTALAR.bat
                      axe/                   dependencias de la pasada unica
                      extended/              instrumento y lanzadores de la campana
                                             de cinco puntos
  analysis/           once scripts; ver "Reproduccion"
docs/                 protocolo de la campana multipunto, en .tex y .pdf
  reports/            cuatro informes HTML de cookies
figures/              las seis figuras del articulo, en PDF
CODEBOOK.md           definicion de cada columna de cada tabla
CHECKSUMS.txt         SHA-256 de todos los archivos del deposito
```

---

## Puntos de observaciÃ³n

La rÃ©plica reportada usa cuatro ubicaciones, todas medidas el 15 de agosto de 2026.

| CÃ³digo | UbicaciÃ³n | Red | Pasadas |
|---|---|---|---|
| `EC` | Cuenca, Ecuador | residencial, ETAPA EP, AS27668 | r1, r2, r3 |
| `EU` | FrÃ¡ncfort, Alemania | centro de datos, AS14061 y AS46475 | r1, r2, r3 |
| `GB` | Londres, Reino Unido | centro de datos, AS21859 | r2, r3, r4 |
| `US` | Miami, Estados Unidos | centro de datos, AS46475 | r1, r2, r3 |

La pasada `GB_r1` se abortÃ³ automÃ¡ticamente porque la VPN no habÃ­a cambiado de paÃ­s todavÃ­a, y quedÃ³ descartada; su reemplazo es `r4`. Los archivos de esa pasada se conservan en el depÃ³sito como evidencia del mecanismo de control, pero el anÃ¡lisis los excluye.

Cada `meta_*.json` registra siete verificaciones de ubicaciÃ³n por pasada, al inicio, cada 25 sitios y al final, con la IP pÃºblica observada, su geolocalizaciÃ³n segÃºn dos servicios independientes, y las versiones exactas de axe-core, Playwright y Node. Las 84 verificaciones de las doce pasadas vÃ¡lidas coinciden con el punto declarado.

### La campaÃ±a extendida de cinco puntos

`data/raw/tracking_extended/` contiene una campaÃ±a posterior que aÃ±ade un punto de observaciÃ³n en Suiza y usa una versiÃ³n mÃ¡s reciente del instrumento. **El artÃ­culo no la analiza**: se publica porque las mediciones existen y son vÃ¡lidas, no como respaldo de ninguna cifra del texto. No es una ampliaciÃ³n de la campaÃ±a reportada, sino una mediciÃ³n independiente, con distinto instrumento, distinto conjunto de pasadas y distinta fecha. Cualquier anÃ¡lisis que la use debe tratarla por separado.

---

## ReproducciÃ³n

Node.js y Python 3. Las versiones con las que se produjeron los resultados publicados estÃ¡n fijadas en `code/collection/package.json` (axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1) y en `code/analysis/requirements.txt` (Python 3.10.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9).

### RecolecciÃ³n

```bash
cd code/collection
npm install
node auditar.js                                   # pasada unica
node auditar_multipunto.js --vantage=EC --run=1   # una pasada de un punto
```

`auditar.js` lee el censo y escribe la salida de forma incremental; si se interrumpe, al volver a ejecutarlo continÃºa donde quedÃ³. `auditar_multipunto.js` comprueba la geolocalizaciÃ³n de la IP y aborta si no coincide con el punto indicado, de modo que la mediciÃ³n debe hacerse realmente desde la ubicaciÃ³n declarada.

### AnÃ¡lisis

Los scripts de `code/analysis/` se ejecutan **desde esa carpeta** y encuentran los datos por rutas relativas.

```bash
cd code/analysis
pip install -r requirements.txt

python construir_entradas.py      # reconstruye las entradas intermedias
python reconciliar.py             # cookies_126_sitios_v2, cambios_reconciliacion
python qa_cookies.py              # qa_irregularidades
python reconstruir_cookies.py ../../data/raw/accessibility ../../data/processed
python estudio.py                 # estudio_126_sitios, estudio_reglas_por_sitio
python verificar_pasada_unica.py  # asociacion entre las dos barreras
python sensibilidad_muestreo.py   # sensibilidad del grupo de referencia
python figuras_uais.py            # cinco de las seis figuras
python fig_vantage.py             # figura de proveedores por punto de observacion
```

El anÃ¡lisis multipunto se ejecuta desde la carpeta de datos, porque busca los archivos de pasada en el directorio de trabajo:

```bash
cd ../../data/raw/tracking
python ../../../code/analysis/verificar_multipunto.py
python ../../../code/analysis/sensibilidad_inclusion.py .
```

`verificar_multipunto.py` reproduce la secciÃ³n de resultados multipunto: proporciones por punto de observaciÃ³n con intervalos de Wilson, prueba exacta de McNemar para cada par, correcciÃ³n de Holm sobre las seis comparaciones, Q de Cochran, controles de renderizado y atribuciÃ³n de cookies por proveedor. `sensibilidad_inclusion.py` repite ese anÃ¡lisis bajo las tres reglas de inclusiÃ³n defendibles y comprueba que la ordenaciÃ³n de los puntos no depende de esa elecciÃ³n.

### VerificaciÃ³n de integridad

```bash
sha256sum -c CHECKSUMS.txt
```

En PowerShell:

```powershell
Get-Content CHECKSUMS.txt | ForEach-Object {
    $h, $r = $_ -split '\s+', 2
    $a = (Get-FileHash $r -Algorithm SHA256).Hash.ToLower()
    if ($a -ne $h) { "DIFIERE: $r" }
}
```

---

## Alcance y lÃ­mites

Las mediciones capturan la portada de cada instituciÃ³n en una fecha concreta. Los sitios cambian, de modo que una reejecuciÃ³n posterior no reproducirÃ¡ los mismos valores: lo que se deposita es la evidencia de lo observado, no una propiedad estable de los sitios.

La auditorÃ­a automatizada detecta un subconjunto de los fallos de conformidad. Un sitio sin violaciones detectadas por axe-core no es un sitio conforme; es un sitio sin fallos detectables por esa vÃ­a.

Cinco sitios quedaron fuera del anÃ¡lisis pareado entre puntos de observaciÃ³n por no cargar en al menos una pasada. EstÃ¡n nombrados uno a uno en el artÃ­culo, junto con la causa y un anÃ¡lisis de sensibilidad frente a esa exclusiÃ³n.

La taxonomÃ­a de cookies de rastreo se ampliÃ³ despuÃ©s de la recolecciÃ³n, tras inspeccionar los nombres efectivamente observados, y se aplicÃ³ reclasificando los nombres ya almacenados, sin volver a medir. `data/processed/cookies_nombres_sin_clasificar.csv` recoge los 243 nombres distintos que no coinciden con ninguna familia conocida, para que la clasificaciÃ³n pueda discutirse.

---

## Licencias

Datos y documentaciÃ³n bajo **CC BY 4.0** (`LICENSE`). CÃ³digo bajo **MIT** (`LICENSE-CODE`).

Los informes HTML de `docs/reports/` incluyen nombres de cookies y de proveedores observados en sitios de terceros. Se publican como evidencia de la observaciÃ³n; los derechos sobre el contenido de esos sitios corresponden a sus titulares.

---

## Cita

Los metadatos estÃ¡n en `CITATION.cff`. Cite el DOI de concepto del registro de Zenodo, que apunta siempre a la Ãºltima versiÃ³n, no el DOI de una versiÃ³n concreta.
