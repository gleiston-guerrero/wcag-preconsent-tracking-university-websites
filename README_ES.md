# Conformidad WCAG y rastreo previo al consentimiento en sitios web de universidades ecuatorianas y de referencia

*English version: [README.md](README.md)*

Datos, evidencia y código del artículo *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, enviado a *Universal Access in the Information Society* (Springer Nature).

**DOI del depósito (concepto, resuelve siempre a la última versión):** [10.5281/zenodo.22405998](https://doi.org/10.5281/zenodo.22405998)

---

## Historia de este repositorio

**Este repositorio se creó el 9 de septiembre de 2026 y no conserva deliberadamente ningún historial anterior a esa fecha.** La investigación que documenta empezó en agosto de 2026, en otro repositorio. La explicación va aquí y no en una nota al pie, porque la ausencia de historial es lo primero que notará quien lea con atención.

Aquel repositorio anterior había recibido *commits* con material que nunca debió versionarse: archivos que identificaban a los evaluadores humanos que participaron en la validación manual —nombres, correos institucionales y rutas locales de archivo—, junto con versiones tempranas del manuscrito.

Borrar esos archivos en un *commit* posterior no los habría eliminado. Git conserva todas las versiones que ha registrado, de modo que cualquier cosa confirmada una vez sigue siendo recuperable desde el historial; y reescribir el historial de un repositorio que otros pueden haber clonado o bifurcado tampoco ofrece garantía alguna. El único remedio fiable era dejar de usar aquel repositorio y empezar uno limpio que contuviera únicamente el depósito revisado. **El repositorio anterior se eliminó**, en lugar de corregirlo sobre la marcha. La eliminación lo retira de GitHub; no puede garantizar que nada se leyera o se copiara mientras estuvo en línea, y esa es justamente la razón de que el remedio sea un repositorio limpio y no un historial limpiado.

Este repositorio es ese comienzo limpio. Cada archivo se revisó en busca de contenido identificador antes de confirmarlo:

- Los evaluadores aparecen solo con códigos: `E01`–`E10` en la primera ronda de codificación, `D01` en la segunda codificación parcial, y `R01`, `R02` y `R03` en las rondas posteriores. Ningún archivo del depósito identifica a un evaluador: ninguno lleva el nombre, el correo electrónico ni una ruta local de nadie del equipo investigador.
- El depósito sí contiene direcciones de correo, y es deliberado. Aparecen en `docs/reports/` y en `data/manual/act_round2/image_evidence/`; se observaron en las páginas públicas de las propias instituciones auditadas y son los contactos de privacidad y protección de datos que esas universidades publican. Su presencia es la evidencia del indicador *contacto de privacidad o DPO*. Se reproducen tal como se observaron, no se recopilaron, y retirarlas eliminaría la prueba de lo que el artículo afirma.
- El manuscrito no se deposita aquí. Se envía a través de la revista, y sus borradores no forman parte del registro de investigación que este repositorio conserva.
- No se publica nada que identifique a una persona física. Las instituciones auditadas son organizaciones públicas y se nombran; quienes codificaron la muestra, no.

**El reinicio cuesta el historial de *commits*, no la evidencia.** No se alteró nada para que encajara: lo que se retiró fue material administrativo y borradores del manuscrito, nunca una medición. La cronología del trabajo de campo no depende de git en absoluto, porque cada medición lleva su propia marca de tiempo interna, escrita por el instrumento en el momento de la captura e independiente de cuándo se confirmó el archivo:

| Campaña | Marcas de tiempo internas |
|---|---|
| Auditoría de pasada única | 14 de agosto de 2026, 06:38–06:59 UTC |
| Réplica multipunto | 15 de agosto de 2026, 15:58–23:10 UTC |
| Campaña extendida de cinco puntos | 16 de agosto de 2026, 03:46–19:57 UTC |
| Control de operador Telconet | 7 de septiembre de 2026, 22:00–23:07 UTC |
| Validación manual, rondas 1–2 | 25 de agosto, 27 de agosto, 1–2 de septiembre de 2026 |
| Ronda ACT | 8 de septiembre de 2026 |

Esas marcas están dentro de los archivos JSON, CSV y de metadatos, son coherentes entre sí, y pueden comprobarse sin necesidad de confiar en el historial de este repositorio ni en su autor. `CHECKSUMS.txt` fija el contenido de cada archivo, y el registro de Zenodo fija la fecha de cada versión publicada.

---

## Qué contiene

El estudio mide dos barreras en 126 portadas universitarias: 63 instituciones ecuatorianas, que constituyen el censo nacional completo, y 63 instituciones de referencia extraídas del consenso de tres rankings internacionales. La primera barrera es la conformidad con WCAG 2.2, auditada con axe-core 4.13.0 en un navegador real. La segunda es la instalación de cookies de rastreo antes de cualquier interacción con una interfaz de consentimiento.

El depósito contiene **dos mediciones reportadas que no deben mezclarse**:

**Auditoría de pasada única**, 14 de agosto de 2026. Una visita a cada uno de los 126 sitios, desde un punto de observación en Ecuador. Es la fuente de todas las cifras de accesibilidad y de la comparación entre grupos. Archivo canónico: `data/raw/accessibility/results.json`.

**Réplica multipunto**, 15 de agosto de 2026. El mismo protocolo repetido desde cuatro ubicaciones geográficas, con tres pasadas válidas en cada una. Es la fuente del contraste entre jurisdicciones. Archivos en `data/raw/tracking/`.

Las dos difieren en fecha, en el conjunto de sitios retenidos y en la regla de consolidación, y sus cifras de rastreo no son intercambiables. `CODEBOOK.md` establece la relación entre ambas.

Se publican además otras dos campañas que **el artículo no analiza**: una campaña extendida de cinco puntos del 16 de agosto y un control de operador desde un segundo proveedor ecuatoriano el 7 de septiembre. Ambas se describen más abajo.

---

## Estructura

```
data/
  raw/
    accessibility/    results.json, results.csv
                      Pasada única, 126 sitios, 14 de agosto de 2026.
    appendix_documentary_tables.tex
                      las dos tablas de apéndice del artículo, depositadas
                      literalmente; fuente de la matriz documental.
    census/           universities.json           los 126 sitios auditados
                      tops.json                   top 75 de cada edición de ranking
                      selection63_benchmark.json  consenso que define el grupo de referencia
    tracking/         39 archivos de la réplica multipunto reportada:
                        results_{EC,EU,GB,US}_r*.{json,csv}
                        meta_*.json  IP pública, geolocalización y versiones por pasada
    tracking_extended/  48 archivos de una campaña posterior de cinco puntos,
                        incluida Suiza. NO analizada en el artículo.
    tracking_telconet/  9 archivos de un control de operador desde un segundo
                        proveedor ecuatoriano. NO analizado en el artículo.
  manual/             validación manual de tres criterios de conformidad en 15
                        sitios: cuatro rondas de codificación, 39 tablas CSV,
                        45 capturas de pantalla, los instrumentos de recolección
                        y su diccionario. Véase data/manual/README.md.
  processed/          catorce tablas derivadas; véase CODEBOOK.md
  interim/            se crea al ejecutar el código; no se versiona
code/
  collection/         audit.js               auditoría de pasada única
                      audit_multivantage.js  auditoría por punto de observación
                      run.bat, INSTALL.bat
                      axe/                   dependencias de la pasada única
                      extended/              instrumento y lanzadores de la
                                             campaña de cinco puntos
  analysis/           dieciséis scripts; véase «Reproducción»
docs/
  reports/            cuatro informes HTML de cookies
figures/              las seis figuras del artículo, en PDF
CODEBOOK.md           definición de cada columna de cada tabla
CHECKSUMS.txt         SHA-256 de cada archivo del depósito
```

**Sobre el idioma.** Los nombres de archivo y de directorio están en inglés. Dentro de los archivos la situación es mixta y deliberada: las tablas CSV de `data/manual/` llevan nombres de columna en inglés, mientras que las claves de los JSON crudos, las columnas de `data/raw/` y `data/processed/`, y los comentarios del código siguen en español, la lengua de trabajo del proyecto. Los **valores** codificados están en español en todo el depósito (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `1`/`P`/`0`, `REVISAR`). `CODEBOOK.md` traduce y define cada uno de ellos.

---

## Puntos de observación

La réplica reportada usa cuatro ubicaciones, todas medidas el 15 de agosto de 2026.

| Código | Ubicación | Red | Pasadas |
|---|---|---|---|
| `EC` | Cuenca, Ecuador | residencial, ETAPA EP, AS27668 | r1, r2, r3 |
| `EU` | Fráncfort, Alemania | centro de datos, AS14061 y AS46475 | r1, r2, r3 |
| `GB` | Londres, Reino Unido | centro de datos, AS21859 | r2, r3, r4 |
| `US` | Miami, Estados Unidos | centro de datos, AS46475 | r1, r2, r3 |

La pasada `GB_r1` se descartó porque la VPN todavía no había cambiado de país. El instrumento avisa al inicio de una pasada cuando el país detectado no coincide con el declarado, espera, y aborta en el primer control periódico de ubicación si la discrepancia persiste: `GB_r1` se detuvo tras 25 sitios, con `estado: "mal"` registrado en sus metadatos y sin marca de `fin`. Sus archivos permanecen en el depósito como evidencia de que el mecanismo de control funcionó; el análisis los excluye y `r4` es su reemplazo.

Cada `meta_*.json` registra siete controles de ubicación por pasada —al inicio, cada 25 sitios y al final— con la IP pública observada, su geolocalización y las versiones exactas de axe-core, Playwright y Node. Los 84 controles de las doce pasadas válidas coinciden con el punto de observación declarado. En 21 de esos 84 el segundo servicio de geolocalización devolvió error y el control se apoya en una sola lectura; las lecturas que sí respondieron son coherentes en todo el conjunto.

### La campaña extendida de cinco puntos

`data/raw/tracking_extended/` contiene una campaña posterior, del 16 de agosto de 2026, que añade un punto suizo y usa una construcción más reciente del instrumento. **El artículo no la analiza.** Se publica porque las mediciones existen y son válidas, no como respaldo de ninguna cifra del texto. No es una ampliación de la campaña reportada, sino una medición independiente, con otro instrumento, otro conjunto de pasadas y otra fecha. Cualquier análisis que la use debe tratarla por separado.

### El control de operador Telconet

`data/raw/tracking_telconet/` contiene tres pasadas sobre los 126 sitios desde una conexión residencial ecuatoriana de Telconet S.A. (AS27947, Guayaquil), el 7 de septiembre de 2026. Su propósito es estrecho: la campaña reportada midió el punto ecuatoriano desde ETAPA EP (AS27668, Cuenca), y esta serie comprueba si el resultado ecuatoriano depende del operador de red. **El artículo no la analiza**, y no debe fusionarse con ninguna de las campañas anteriores. Véase `data/raw/tracking_telconet/READ_ME.md`.

---

## Validación manual

`data/manual/` contiene la verificación manual de tres criterios de conformidad WCAG 2.2 —1.1.1 contenido no textual, 1.4.3 contraste (mínimo) y 2.4.4 propósito de los enlaces (en contexto)— sobre una submuestra de 15 sitios, siete del grupo de referencia y ocho del censo ecuatoriano.

Contiene cuatro rondas de codificación que **no deben fusionarse**, porque cada una usó un esquema distinto y la diferencia entre ellas es en sí misma un hallazgo: una primera ronda con diez evaluadores, una segunda codificación parcial de cinco sitios por un undécimo, una recodificación mejor documentada de los quince, y una ronda final anclada en las reglas de la W3C Accessibility Conformance Testing (ACT) que codifica cada elemento aplicable en lugar de una proporción muestreada. `data/manual/README.md` expone el acuerdo entre rondas y lo que establece y lo que no.

Las 45 capturas de `data/manual/captures/` son la evidencia de las dos primeras rondas.

---

## Reproducción

Node.js y Python 3. Las versiones que produjeron los resultados publicados están fijadas en `code/collection/package.json` (axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1) y en `code/analysis/requirements.txt` (Python 3.10.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9). El control de operador de septiembre se ejecutó con Node v24.12.0 en otra máquina; sus metadatos lo registran.

### Recolección

```bash
cd code/collection
npm install
node audit.js                                     # pasada única
node audit_multivantage.js --vantage=EC --run=1   # una pasada de un punto
```

`audit.js` lee el censo y escribe su salida de forma incremental; si se interrumpe, al volver a ejecutarlo reanuda donde se detuvo. `audit_multivantage.js` comprueba la geolocalización de la IP pública antes de empezar y en cada control periódico, y aborta la pasada si la ubicación deja de coincidir con el punto declarado.

### Análisis

Todos los scripts de `code/analysis/` se ejecutan **desde ese directorio** y encuentran sus datos por rutas relativas.

```bash
cd code/analysis
pip install -r requirements.txt

python build_entries.py              # reconstruye las entradas intermedias
python reconcile.py                  # cookies_126_sites_v2, reconciliation_changes
python qa_cookies.py                 # qa_irregularities
python rebuild_cookies.py ../../data/raw/accessibility ../../data/processed
python study.py                      # study_126_sites, study_rules_per_site
python verify_single_pass.py         # asociación entre las dos barreras
python sensitivity_sampling.py       # sensibilidad del grupo de referencia
python figures_uais.py               # cinco de las seis figuras
python fig_vantage.py                # figura de proveedor por punto
python verify_multivantage.py        # toda la sección de resultados multipunto
python sensitivity_inclusion.py ../../data/raw/tracking
python kappa_wcag.py                 # acuerdo de la validación manual
python extract_documentary_matrix.py # matriz documental desde los apéndices
python power_analysis.py             # potencia estadística de las comparaciones
python normalise_acronym.py          # normalización de siglas en el depósito
python verify_live_divergence.py     # automática vs verificación en vivo: 39 = 35 + 4
```

`extract_documentary_matrix.py` lee `data/raw/appendix_documentary_tables.tex`, las dos tablas de apéndice del artículo depositadas literalmente, y deriva de ellas la matriz documental. Aborta si los recuentos que obtiene no coinciden con los que reporta el artículo. El artículo en sí no se deposita; solo las dos tablas de las que la matriz se deriva, para que la derivación sea auditable y no una afirmación.

`verify_multivantage.py` reproduce la sección de resultados multipunto: proporciones por punto con intervalos de Wilson, prueba exacta de McNemar para cada par, corrección de Holm sobre las seis comparaciones, Q de Cochran, controles de renderizado y atribución de cookies por proveedor. `sensitivity_inclusion.py` repite ese análisis bajo las tres reglas de inclusión defendibles y muestra que el orden de los puntos de observación no depende de esa elección.

### Comprobación de integridad

```bash
sha256sum -c CHECKSUMS.txt
```

En PowerShell:

```powershell
Get-Content CHECKSUMS.txt | ForEach-Object {
    $h, $r = $_ -split '  ', 2
    $a = (Get-FileHash -LiteralPath $r -Algorithm SHA256).Hash.ToLower()
    if ($a -ne $h) { "MISMATCH: $r" }
}
```

---

## Alcance y límites

Las mediciones capturan la portada de cada institución en una fecha concreta. Los sitios cambian, así que una ejecución posterior no reproducirá los mismos valores: lo que se deposita es evidencia de lo observado, no una propiedad estable de los sitios.

La auditoría automática detecta un subconjunto de los fallos de conformidad. Un sitio sin violaciones detectadas por axe-core no es un sitio conforme; es un sitio sin fallos detectables por esa vía. Esa es la razón de la validación manual, y del desacuerdo entre rondas que esa validación documenta.

Cinco sitios quedan fuera del análisis pareado entre puntos de observación porque no cargaron en al menos una pasada. El artículo nombra cada uno, con su causa y un análisis de sensibilidad de esa exclusión.

El campo `https` de `results.json` informa `true` para los 126 sitios. Es un artefacto: Playwright rechaza los certificados inválidos como fallos de carga, de modo que un sitio con una cadena deficiente nunca llega a auditarse. Una comprobación manual en navegador identificó los cinco sitios ecuatorianos afectados; están registrados en `data/processed/tls_deficiencies_august2026.csv`.

La taxonomía de cookies de rastreo se amplió después de la recolección, una vez inspeccionados los nombres de cookie observados, y se aplicó reclasificando los nombres almacenados, sin volver a medir. `data/processed/cookies_unclassified_names.csv` lista los 243 nombres distintos que no coinciden con ninguna familia conocida, para que la clasificación pueda discutirse.

---

## Licencias

Datos y documentación bajo **CC BY 4.0** (`LICENSE`). Código bajo **MIT** (`LICENSE-CODE`).

Los informes HTML de `docs/reports/` incluyen nombres de cookies y de proveedores observados en sitios de terceros. Se publican como evidencia de la observación; los derechos sobre el contenido de esos sitios pertenecen a sus titulares.

---

## Autoría

- Gleiston Guerrero-Ulloa — Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo, Ecuador · [0000-0001-5990-2357](https://orcid.org/0000-0001-5990-2357)
- Andrea Zúñiga Paredes — Ministerio de Educación del Ecuador, Quito · [0000-0003-4042-1523](https://orcid.org/0000-0003-4042-1523)
- Efraín Díaz-Macías — Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo, Ecuador · [0000-0003-4087-029X](https://orcid.org/0000-0003-4087-029X)

## Cita

Los metadatos están en `CITATION.cff`. Cite el DOI de concepto del registro de Zenodo, que apunta siempre a la última versión, no el DOI de una versión concreta.
