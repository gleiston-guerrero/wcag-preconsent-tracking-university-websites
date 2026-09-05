# Libro de códigos

*English version: [CODEBOOK.md](CODEBOOK.md)*

Documenta todos los archivos de datos del depósito. Codificación UTF-8. Los campos vacíos representan ausencia de dato, no cero.

---

## 1. Las dos mediciones

El depósito contiene dos mediciones del mismo fenómeno, tomadas con un día de diferencia y con distinto diseño. **Sus cifras de rastreo no son intercambiables.** Antes de cruzar cualquier tabla conviene tener claro de cuál procede.

| | Pasada única | Réplica multipunto |
|---|---|---|
| Fecha | 14 de agosto de 2026 | 15 de agosto de 2026 |
| Puntos de observación | uno, Ecuador | cuatro: EC, EU, GB, US |
| Visitas por sitio | una | tres por punto |
| Consolidación | ninguna | mayoría sobre las tres pasadas |
| Sitios | los 126 | 121 con éxito en las doce pasadas |
| Fuente | `data/raw/accessibility/` | `data/raw/tracking/` |
| Sustenta | accesibilidad y comparación entre grupos | contraste entre jurisdicciones |

En la pasada única, con la taxonomía extendida, el rastreo previo al consentimiento se observa en 41 de los 63 sitios ecuatorianos y en 43 de los 63 de referencia. En la réplica, sobre los 121 sitios retenidos, se observa en 82 desde Ecuador, 79 desde Estados Unidos, 76 desde Reino Unido y 73 desde Alemania. Ninguna de las dos cifras sustituye a la otra: la primera sostiene la comparación entre grupos, la segunda la comparación del mismo sitio bajo condiciones distintas.

Existe además una tercera cifra, la verificación en vivo que figura en las columnas `*_verificacion` de `cookies_126_sitios_v3.csv`, tomada por inspección manual en fechas distintas. Difiere de la medición automatizada en 39 de los 126 sitios. Está documentada en la sección 4.

---

## 2. Categorías comunes

**Grupo** (`grupo`): `Ecuador` o `Mundo` en los archivos JSON; `ecuador` o `mundo` en las tablas derivadas.

**Identificador de sitio** (`id`): entero de 1 a 126, estable en todos los archivos del depósito. Permite unir cualquier tabla con cualquier otra.

**Sí/no**: `yes` o `no` en las tablas CSV derivadas; booleano en los JSON.

**Nivel de conformidad** (`nivel`, `max_nivel_sin_fallo`): `A`, `AA` o `AAA`, según WCAG 2.2. Las reglas de nivel AAA estuvieron activas en la auditoría; la regla dominante en ese nivel es contraste mejorado, criterio 1.4.6, que exige una razón de 7:1.

**Principio** (`principio`): `Perceptible`, `Operable`, `Comprensible` o `Robusto`, los cuatro principios de WCAG.

**Punto de observación** (`vantage`, sufijo de nombre de archivo): `EC` Ecuador, `EU` Alemania, `GB` Reino Unido, `US` Estados Unidos. En `tracking_extended/` aparece además `CH`, Suiza.

**Cookie de rastreo**: nombre de cookie que coincide con alguno de los patrones de la taxonomía. La lista original cubría Google, Meta, TikTok, Microsoft Clarity, Hotjar, Matomo, Baidu y familias menores. La lista extendida añade el LinkedIn Insight Tag, la familia publicitaria completa de Microsoft, TapAd, StackAdapt, Snapchat y Sourcebuster. Ambas listas están, en forma de expresiones regulares, en `code/analysis/verificar_multipunto.py`, líneas 7 a 18. La extendida gobierna todas las cifras publicadas.

---

## 3. Datos crudos

### `data/raw/accessibility/resultados.json`

Lista JSON de 126 objetos, uno por sitio, ordenados por `id`. Es la fuente de verdad de la auditoría de pasada única: todas las tablas de `data/processed/` derivadas de accesibilidad se calculan a partir de este archivo.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | entero | Identificador del sitio. |
| `grupo` | texto | `Ecuador` o `Mundo`. |
| `sigla` | texto | Sigla de la institución. |
| `nombre` | texto | Nombre completo. |
| `pais` | texto | País de la institución. |
| `url` | texto | Portada auditada. |
| `ok` | booleano | La página cargó. Verdadero en los 126. |
| `https` | booleano | Certificado TLS válido. |
| `axe_version` | texto | Versión del motor. `4.13.0` en los 126. |
| `fecha` | fecha-hora | Momento de la visita, ISO 8601. |
| `cookies` | objeto | Ver abajo. |
| `accesibilidad` | objeto | Ver abajo. |

**`cookies`**

| Campo | Tipo | Descripción |
|---|---|---|
| `total_pre` | entero | Cookies presentes antes de cualquier interacción. |
| `rastreo_pre` | entero | De ellas, cuántas son de rastreo según la taxonomía base. |
| `nombres_pre` | lista | Nombres de todas las cookies observadas. |
| `nombres_rastreo` | lista | Nombres clasificados como de rastreo. |
| `cmp` | lista | Plataformas de gestión del consentimiento detectadas. |
| `banner` | booleano | Se mostró un aviso de cookies. |

**`accesibilidad`**

| Campo | Tipo | Descripción |
|---|---|---|
| `title` | texto | Contenido de `<title>`. |
| `lang` | texto | Atributo `lang` del documento. |
| `viewport` | booleano | Existe metaetiqueta de viewport. |
| `skipLink` | booleano | Existe enlace para saltar al contenido. |
| `violaciones` | entero | Reglas de axe-core con al menos un nodo que falla. |
| `nodos` | entero | Nodos que fallan, sumados sobre todas las reglas. |
| `porPrincipio` | objeto | Nodos que fallan por principio WCAG. |
| `porNivel` | objeto | Nodos que fallan por nivel: `A`, `AA`, `AAA`. |
| `maxNivelSinFallo` | texto | Nivel más alto sin ningún fallo detectado. |
| `incompletos` | entero | Comprobaciones que axe-core no pudo resolver y requieren revisión humana. |
| `passes` | entero | Reglas superadas. |
| `reglas` | lista | Una entrada por regla incumplida, con `id`, `impacto`, `criterio`, `principio`, `nivel`, `nodos` y `ayuda`. |

### `data/raw/accessibility/resultados.csv`

Vista aplanada del JSON anterior, 126 filas, para inspección rápida. Columnas: `id`, `grupo`, `sigla`, `pais`, `url`, `ok`, `error`, `title`, `lang`, `viewport`, `https`, `cookies_pre`, `rastreo_pre`, `nombres_rastreo`, `cmp`, `banner`, `ax_violaciones`, `ax_nodos`, `nivelA_nodos`, `nivelAA_nodos`, `nivelAAA_nodos`, `Perceptible`, `Operable`, `Comprensible`, `Robusto`, `max_nivel_sin_fallo_auto`. Para análisis, use `estudio_126_sitios.csv`, que es más completa.

### `data/raw/tracking/resultados_<PUNTO>_r<N>.json`

Trece archivos, uno por pasada. Misma estructura que `resultados.json`, con dos campos añadidos: `vantage` y `run`. La pasada `GB_r1` está truncada, con 5 053 bytes frente a los 25 000 habituales, porque se abortó al detectar que la VPN no había cambiado de país; se conserva como evidencia y el análisis la excluye.

### `data/raw/tracking/meta_<PUNTO>_r<N>.json`

Un archivo por pasada, con la evidencia de procedencia.

| Campo | Descripción |
|---|---|
| `vantage`, `run` | Punto de observación y número de pasada. |
| `inicio`, `fin`, `duracion_min` | Marcas de tiempo reales de la pasada. |
| `geolocalizacion` | Lecturas iniciales de `ipinfo.io` e `ipwho.is`: IP, país, ciudad y organización. |
| `coincide_con_vantage` | La ubicación observada coincide con la declarada. |
| `controles_de_ubicacion` | Siete comprobaciones por pasada: al inicio, tras los sitios 25, 50, 75, 100 y 125, y al final. Cada una con las dos lecturas y su veredicto. |
| `configuracion` | Espera para scripts, tiempo límite de carga, reintentos, inclusión de nivel AAA, medición de cookies y cadena de agente de usuario. |
| `axe_core`, `playwright`, `node`, `plataforma` | Versiones exactas del entorno. |
| `sitios`, `exitosos`, `fallidos` | Recuentos de la pasada. |

### `data/raw/tracking_extended/`

Cuarenta y ocho archivos de la campaña posterior de cinco puntos, con la misma estructura. **No sustentan ninguna cifra del artículo.** Ver el README.

### `data/raw/census/`

`universidades.json` es el censo de los 126 sitios auditados, con sigla, nombre, país y URL. `tops.json` contiene el top 75 de cada edición de ranking empleada. `seleccion63_mundo.json` documenta el consenso entre los tres rankings que define el grupo de referencia.

---

## 4. Tablas derivadas

### `estudio_126_sitios.csv` — 126 filas, 32 columnas

Aplanado canónico de `resultados.json`. Lo produce `estudio.py`.

| Columna | Descripción |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `pais`, `url` | Identificación del sitio. |
| `fecha`, `axe_version`, `ok`, `https` | Metadatos de la visita. |
| `cookies_total_pre` | Cookies antes de consentir. |
| `cookies_rastreo_pre` | De ellas, de rastreo según la taxonomía base. |
| `nombres_pre`, `nombres_rastreo` | Nombres, separados por ` \| `. |
| `cmp`, `banner` | Plataforma de consentimiento y aviso. |
| `title`, `lang`, `viewport`, `skip_link` | Indicadores estructurales. |
| `ax_violaciones`, `ax_nodos` | Reglas incumplidas y nodos que fallan. |
| `nodos_A`, `nodos_AA`, `nodos_AAA` | Nodos que fallan por nivel. |
| `perceptible`, `operable`, `comprensible`, `robusto` | Nodos que fallan por principio. |
| `max_nivel_sin_fallo` | Nivel más alto sin fallos. |
| `incompletos`, `passes` | Comprobaciones no resueltas y reglas superadas. |

### `estudio_reglas_por_sitio.csv` — 441 filas, 10 columnas

Una fila por sitio y regla incumplida. Producida por el mismo script.

| Columna | Descripción |
|---|---|
| `id`, `grupo`, `sigla` | Sitio. |
| `regla` | Identificador de la regla de axe-core, por ejemplo `image-alt`. |
| `impacto` | Gravedad asignada por axe-core: `minor`, `moderate`, `serious`, `critical`. |
| `criterio` | Criterio de éxito de WCAG asociado. Vacío si la regla no mapea a ninguno. |
| `principio`, `nivel` | Principio y nivel del criterio. |
| `nodos` | Elementos que fallan esa regla en ese sitio. |
| `ayuda` | URL de la documentación de la regla. |

### `cookies_126_sitios_v3.csv` — 126 filas, 24 columnas

Tabla de cookies del artículo, con las dos taxonomías en columnas separadas. La produce `reconstruir_cookies.py` a partir de `resultados.json` y de `cookies_126_sitios_v2.csv`.

| Columna | Descripción |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | Identificación. |
| `fecha` | Momento de la medición automatizada. |
| `cookies_antes_consentir` | Cookies observadas antes de consentir. |
| `nombres_cookies` | Nombres, separados por ` \| `. |
| `n_nombres_listados` | Cuántos nombres hay en el campo anterior. |
| `rastreo_base` | Rastreo según la taxonomía original. |
| `rastreo` | Rastreo según la taxonomía extendida. **Esta es la columna que sustenta las cifras del artículo.** |
| `proveedores_rastreo` | Familias de proveedor reconocidas en ese sitio. |
| `procedencia_rastreo` | Por qué se clasificó así: qué fuente aportó el dato y qué taxonomía decidió. |
| `banner_estudio`, `cmp_estudio` | Aviso y plataforma detectados en la medición automatizada. |
| `pais`, `region`, `ciudad`, `tipo` | Atributos institucionales. |
| `cmp_verificacion`, `banner_verificacion`, `fuente_verificacion` | Resultados de la verificación manual en vivo, en fecha distinta. |
| `polcookies_estudio` | Existe política de cookies. |
| `nota_documental` | Observación cualitativa sobre los documentos publicados por la institución. |

La diferencia entre `rastreo_base` y `rastreo` es de un solo sitio ecuatoriano, que cruza el umbral porque sus únicas cookies coincidentes pertenecen a la familia Sourcebuster, añadida en la lista extendida. El recuento ecuatoriano pasa así de 40 a 41; el de referencia se mantiene en 43.

Las columnas `*_verificacion` proceden de una inspección manual distinta de la medición automatizada. Discrepan de la columna `rastreo` en 39 de los 126 sitios: 34 donde la medición automatizada detecta rastreo y la verificación en vivo no, y 5 en sentido contrario. No es un error de ninguna de las dos: son observaciones en momentos distintos de sitios que cambian. **No mezcle ambas columnas en un mismo recuento.**

### `cookies_126_sitios_v2.csv` — 126 filas

Versión previa, entrada necesaria de `reconstruir_cookies.py`. Se publica porque sin ella la v3 no se reproduce. No la use directamente para análisis.

### `cookies_nombres_sin_clasificar.csv` — 243 filas

Nombres de cookie observados que no coinciden con ninguna familia de la taxonomía, con el número de sitios en que aparecen. Es la evidencia de la decisión taxonómica: permite discutir si algún nombre debió clasificarse como rastreo.

| Columna | Descripción |
|---|---|
| `nombre_cookie` | Nombre observado. |
| `sitios_en_que_aparece` | Número de sitios distintos. |

### `cookies_divergencias_v2.csv` — 14 filas

Control de calidad. Sitios donde la tabla v2 listaba nombres de cookie que no aparecen en el JSON crudo, indicio de pérdida de datos en una fase intermedia.

| Columna | Descripción |
|---|---|
| `id`, `sigla`, `grupo` | Sitio. |
| `nombres_no_presentes_en_crudo` | Nombres afectados. |

### `cambios_reconciliacion.csv` — 68 filas

Registro de auditoría de la reconciliación entre el inventario y los informes HTML. Producida por `reconciliar.py`.

| Columna | Descripción |
|---|---|
| `sigla` | Institución. |
| `campo` | Campo modificado. |
| `antes`, `despues` | Valor anterior y nuevo. |
| `motivo` | Regla que justificó el cambio. |

### `qa_irregularidades.csv` — 228 filas

Incidencias detectadas en el inventario, con código de tipo y acción sugerida. Producida por `qa_cookies.py`. Se publica como evidencia del control de calidad, no como dato de análisis.

| Columna | Descripción |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | Sitio. |
| `codigo` | Tipo de incidencia, de `I1` a `I9`. |
| `irregularidad` | Descripción. |
| `valor_actual` | Valor que la motivó. |
| `accion_requerida` | Corrección sugerida. |

### `reporte_cookies_nacionales.csv` — 63 filas · `reporte_cookies_extranjeras.csv` — 63 filas

Inventarios por grupo, con los campos de la verificación manual. Son entrada de `construir_entradas.py`, que los fusiona para reconstruir la tabla de 126 sitios. Las columnas de cookies de estos archivos corresponden a la **verificación en vivo**, no a la medición automatizada.

Nacionales: `#`, `Universidad`, `Sigla`, `Tipo`, `Ciudad`, `Sitio`, `Verificacion`, `Cookies_antes_consentir`, `Nombres_cookies`, `Rastreo`, `CMP_live`, `Banner_live`, `Banner_estudio`, `PolCookies_estudio`.

Extranjeras: `#`, `Universidad`, `Sigla`, `Pais`, `Region`, `Sitio`, `Cookies_antes_consentir`, `Nombres_cookies`, `CMP_detectada`, `Banner_visible`, `Banner_estudio`, `PolCookies_estudio`.

### `sensibilidad_inclusion.csv` — 3 filas

Resultado del análisis de sensibilidad a la regla de inclusión de la réplica multipunto. Una fila por regla.

| Columna | Descripción |
|---|---|
| `regla` | `R3` tres pasadas válidas por punto, la del artículo; `R2` al menos dos; `R1` al menos una. |
| `n` | Sitios retenidos bajo esa regla. |
| `Q`, `p_Q` | Q de Cochran sobre los cuatro puntos y su valor p, con 3 grados de libertad. |
| `marg_EC`, `marg_EU`, `marg_GB`, `marg_US` | Sitios con rastreo en cada punto. |
| `p_<par>` | Valor p exacto de McNemar de cada par. |
| `pholm_<par>` | El mismo valor tras la corrección de Holm sobre las seis comparaciones. |

---

## 5. Informes HTML

`docs/reports/` contiene cuatro informes navegables generados durante el trabajo de campo. No son datos primarios, pero **sí son entrada del código**: `construir_entradas.py` extrae de `reporte_cookies_combinado.html` y de `anexo_universidades_cookies.html` los datos embebidos en su constante `DATA` de JavaScript, que son necesarios para reproducir la cadena de tablas de cookies. Por eso se publican.

---

## 6. Cadena de dependencias

Quién produce qué, y a partir de qué.

```
resultados.json ────────────────────────────► estudio.py
                                                 ├─► estudio_126_sitios.csv
                                                 └─► estudio_reglas_por_sitio.csv

reporte_cookies_nacionales.csv   ┐
reporte_cookies_extranjeras.csv  ├─► construir_entradas.py ─► data/interim/
reporte_cookies_combinado.html   │                              _comb.json
anexo_universidades_cookies.html ┘                              _anex.json
                                                                cookies_126_sitios.csv
                                                                     │
data/interim/ ──────────────────► reconciliar.py ──────────────────┤
                                     ├─► cookies_126_sitios_v2.csv │
                                     └─► cambios_reconciliacion.csv│
                                                                    │
data/interim/ ──────────────────► qa_cookies.py ─► qa_irregularidades.csv

resultados.json + v2 ───────────► reconstruir_cookies.py
                                     ├─► cookies_126_sitios_v3.csv
                                     ├─► cookies_nombres_sin_clasificar.csv
                                     └─► cookies_divergencias_v2.csv

data/raw/tracking/ ─────────────► verificar_multipunto.py     (seccion multipunto)
                                ► sensibilidad_inclusion.py   ─► sensibilidad_inclusion.csv
```

Los archivos de `data/interim/` no se versionan porque `construir_entradas.py` los regenera desde material que sí está publicado.
