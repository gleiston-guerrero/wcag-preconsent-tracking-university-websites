# WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites

Datos, evidencia y código del artículo *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, sometido a *Universal Access in the Information Society* (Springer Nature).

**DOI del depósito:** `10.5281/zenodo.XXXXXXX` *(pendiente hasta la publicación del registro en Zenodo)*

---

## Qué contiene

El estudio mide dos barreras sobre 126 portadas universitarias: 63 instituciones ecuatorianas, que constituyen el censo completo del sistema, y 63 instituciones de referencia obtenidas del consenso de tres rankings internacionales. La primera barrera es la conformidad con WCAG 2.2, auditada con axe-core 4.13.0 sobre un navegador real. La segunda es el depósito de cookies de rastreo antes de cualquier interacción con una interfaz de consentimiento.

El depósito contiene **dos mediciones distintas que no deben mezclarse**:

**Auditoría de pasada única**, 14 de agosto de 2026. Una sola visita a cada uno de los 126 sitios, desde un punto de observación en Ecuador. Es la fuente de todas las cifras de accesibilidad y de la comparación entre grupos. Archivo canónico: `data/raw/accessibility/resultados.json`.

**Réplica multipunto**, 15 de agosto de 2026. El mismo protocolo repetido desde cuatro ubicaciones geográficas, con tres pasadas válidas en cada una. Es la fuente del contraste entre jurisdicciones. Archivos en `data/raw/tracking/`.

Las dos difieren en fecha, en conjunto de sitios retenidos y en regla de consolidación. El artículo lo advierte de forma expresa: las cifras de rastreo de una y otra no son intercambiables. `CODEBOOK.md` detalla la relación entre ellas.

---

## Estructura

```
data/
  raw/
    accessibility/    resultados.json, resultados.csv
                      Pasada única, 126 sitios, 14 de agosto de 2026.
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

## Puntos de observación

La réplica reportada usa cuatro ubicaciones, todas medidas el 15 de agosto de 2026.

| Código | Ubicación | Red | Pasadas |
|---|---|---|---|
| `EC` | Cuenca, Ecuador | residencial, ETAPA EP, AS27668 | r1, r2, r3 |
| `EU` | Fráncfort, Alemania | centro de datos, AS14061 y AS46475 | r1, r2, r3 |
| `GB` | Londres, Reino Unido | centro de datos, AS21859 | r2, r3, r4 |
| `US` | Miami, Estados Unidos | centro de datos, AS46475 | r1, r2, r3 |

La pasada `GB_r1` se abortó automáticamente porque la VPN no había cambiado de país todavía, y quedó descartada; su reemplazo es `r4`. Los archivos de esa pasada se conservan en el depósito como evidencia del mecanismo de control, pero el análisis los excluye.

Cada `meta_*.json` registra siete verificaciones de ubicación por pasada, al inicio, cada 25 sitios y al final, con la IP pública observada, su geolocalización según dos servicios independientes, y las versiones exactas de axe-core, Playwright y Node. Las 84 verificaciones de las doce pasadas válidas coinciden con el punto declarado.

### La campaña extendida de cinco puntos

`data/raw/tracking_extended/` contiene una campaña posterior que añade un punto de observación en Suiza y usa una versión más reciente del instrumento. **El artículo no la analiza**: se publica porque las mediciones existen y son válidas, no como respaldo de ninguna cifra del texto. No es una ampliación de la campaña reportada, sino una medición independiente, con distinto instrumento, distinto conjunto de pasadas y distinta fecha. Cualquier análisis que la use debe tratarla por separado.

---

## Reproducción

Node.js y Python 3. Las versiones con las que se produjeron los resultados publicados están fijadas en `code/collection/package.json` (axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1) y en `code/analysis/requirements.txt` (Python 3.10.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9).

### Recolección

```bash
cd code/collection
npm install
node auditar.js                                   # pasada unica
node auditar_multipunto.js --vantage=EC --run=1   # una pasada de un punto
```

`auditar.js` lee el censo y escribe la salida de forma incremental; si se interrumpe, al volver a ejecutarlo continúa donde quedó. `auditar_multipunto.js` comprueba la geolocalización de la IP y aborta si no coincide con el punto indicado, de modo que la medición debe hacerse realmente desde la ubicación declarada.

### Análisis

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

El análisis multipunto se ejecuta desde la carpeta de datos, porque busca los archivos de pasada en el directorio de trabajo:

```bash
cd ../../data/raw/tracking
python ../../../code/analysis/verificar_multipunto.py
python ../../../code/analysis/sensibilidad_inclusion.py .
```

`verificar_multipunto.py` reproduce la sección de resultados multipunto: proporciones por punto de observación con intervalos de Wilson, prueba exacta de McNemar para cada par, corrección de Holm sobre las seis comparaciones, Q de Cochran, controles de renderizado y atribución de cookies por proveedor. `sensibilidad_inclusion.py` repite ese análisis bajo las tres reglas de inclusión defendibles y comprueba que la ordenación de los puntos no depende de esa elección.

### Verificación de integridad

```bash
sha256sum -c CHECKSUMS.txt
```

En PowerShell:

```powershell
Get-Content CHECKSUMS.txt | ForEach-Object {
    $h, $r = $_ -split '  ', 2
    $a = (Get-FileHash -LiteralPath $r -Algorithm SHA256).Hash.ToLower()
    if ($a -ne $h) { "DIFIERE: $r" }
}
```

---

## Alcance y límites

Las mediciones capturan la portada de cada institución en una fecha concreta. Los sitios cambian, de modo que una reejecución posterior no reproducirá los mismos valores: lo que se deposita es la evidencia de lo observado, no una propiedad estable de los sitios.

La auditoría automatizada detecta un subconjunto de los fallos de conformidad. Un sitio sin violaciones detectadas por axe-core no es un sitio conforme; es un sitio sin fallos detectables por esa vía.

Cinco sitios quedaron fuera del análisis pareado entre puntos de observación por no cargar en al menos una pasada. Están nombrados uno a uno en el artículo, junto con la causa y un análisis de sensibilidad frente a esa exclusión.

La taxonomía de cookies de rastreo se amplió después de la recolección, tras inspeccionar los nombres efectivamente observados, y se aplicó reclasificando los nombres ya almacenados, sin volver a medir. `data/processed/cookies_nombres_sin_clasificar.csv` recoge los 243 nombres distintos que no coinciden con ninguna familia conocida, para que la clasificación pueda discutirse.

---

## Licencias

Datos y documentación bajo **CC BY 4.0** (`LICENSE`). Código bajo **MIT** (`LICENSE-CODE`).

Los informes HTML de `docs/reports/` incluyen nombres de cookies y de proveedores observados en sitios de terceros. Se publican como evidencia de la observación; los derechos sobre el contenido de esos sitios corresponden a sus titulares.

---

## Cita

Los metadatos están en `CITATION.cff`. Cite el DOI de concepto del registro de Zenodo, que apunta siempre a la última versión, no el DOI de una versión concreta.
