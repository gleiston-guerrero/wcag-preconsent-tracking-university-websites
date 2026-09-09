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

Existe además una tercera cifra, la verificación en vivo que figura en las columnas `*_verificacion` de `cookies_126_sites_v3.csv`, tomada por inspección manual en fechas distintas. Difiere de la medición automatizada en 39 de los 126 sitios. Está documentada en la sección 4.

---

## 2. Categorías comunes

**Grupo** (`grupo`): `Ecuador` o `Mundo` en los archivos JSON; `ecuador` o `mundo` en las tablas derivadas.

**Identificador de sitio** (`id`): entero de 1 a 126, **definido por `data/raw/census/universities.json`**, que es la lista autoritativa. Es estable en todos los archivos del depósito: un identificador designa a una sola institución en todas partes, de modo que permite unir cualquier tabla con cualquier otra. `sigla` sirve igualmente como clave de unión y es la que hay que usar donde una tabla no lleve `id`. La única excepción es `documentary_matrix.csv`, cuya columna `#` es la posición dentro de la tabla de su grupo y no el identificador global; esa tabla se une por `Abbr.`

**Sí/no**: `yes` o `no` en las tablas CSV derivadas; booleano en los JSON. La matriz documental usa `si` y `no`, porque se transcribió del artículo.

**Nivel de conformidad** (`nivel`, `max_nivel_sin_fallo`): `A`, `AA` o `AAA`, según WCAG 2.2. Las reglas de nivel AAA estuvieron activas en la auditoría; la regla dominante en ese nivel es contraste mejorado, criterio 1.4.6, que exige una razón de 7:1.

**Principio** (`principio`): `Perceptible`, `Operable`, `Comprensible` o `Robusto`, los cuatro principios de WCAG.

**Punto de observación** (`vantage`, sufijo de nombre de archivo): `EC` Ecuador, `EU` Alemania, `GB` Reino Unido, `US` Estados Unidos. En `tracking_extended/` aparece además `CH`, Suiza.

**Cookie de rastreo**: nombre de cookie que coincide con alguno de los patrones de la taxonomía. La lista original cubría Google, Meta, TikTok, Microsoft Clarity, Hotjar, Matomo, Baidu y familias menores. La lista extendida añade el LinkedIn Insight Tag, la familia publicitaria completa de Microsoft, TapAd, StackAdapt, Snapchat y Sourcebuster. Ambas listas, en forma de expresiones regulares, están en `code/analysis/verify_multivantage.py`, líneas 7 a 18. La extendida gobierna todas las cifras publicadas.

---

## 3. Datos crudos

### `data/raw/accessibility/results.json`

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
| `https` | booleano | La página se sirvió por HTTPS. **No** equivale al indicador documental de la Figura 1: ver `tls_deficiencies_august2026.csv`. |
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

### `data/raw/accessibility/results.csv`

Vista aplanada del JSON anterior, 126 filas, para inspección rápida. Columnas: `id`, `grupo`, `sigla`, `pais`, `url`, `ok`, `error`, `title`, `lang`, `viewport`, `https`, `cookies_pre`, `rastreo_pre`, `nombres_rastreo`, `cmp`, `banner`, `ax_violaciones`, `ax_nodos`, `nivelA_nodos`, `nivelAA_nodos`, `nivelAAA_nodos`, `Perceptible`, `Operable`, `Comprensible`, `Robusto`, `max_nivel_sin_fallo_auto`. Para análisis, use `study_126_sites.csv`, que es más completa.

### `data/raw/tracking/results_<PUNTO>_r<N>.json`

Trece archivos, uno por pasada. Misma estructura que `results.json`, con dos campos añadidos: `vantage` y `run`. La pasada `GB_r1` está truncada, con 49 546 bytes frente a los 280 000 habituales, porque se abortó al detectar que la VPN no había cambiado de país; se conserva como evidencia y el análisis la excluye.

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

`universities.json` es el censo de los 126 sitios auditados, con sigla, nombre, país y URL. `tops.json` contiene el top 75 de cada edición de ranking empleada. `selection63_benchmark.json` documenta el consenso entre los tres rankings que define el grupo de referencia.

---

## 4. Tablas derivadas

### `study_126_sites.csv` — 126 filas, 32 columnas

Aplanado canónico de `results.json`. Lo produce `study.py`.

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

### `study_rules_per_site.csv` — 441 filas, 10 columnas

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

### `cookies_126_sites_v3.csv` — 126 filas, 24 columnas

Tabla de cookies del artículo, con las dos taxonomías en columnas separadas. La produce `rebuild_cookies.py` a partir de `results.json` y de `cookies_126_sites_v2.csv`.

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

Las columnas `*_verificacion` proceden de una inspección manual distinta de la medición automatizada. Discrepan de la columna `rastreo` en 39 de los 126 sitios: 35 donde la medición automatizada detecta rastreo y la verificación en vivo no, y 4 en sentido contrario. Esos cuatro son EPN, FLACSO, UTE y Peking, donde la comprobación en vivo encontró cookies de Google Analytics o de Baidu que la pasada automatizada no había registrado. Ninguna de las dos observaciones es errónea: se toman en momentos distintos de sitios que cambian. `verify_live_divergence.py` recalcula las tres cifras a partir de las tablas depositadas. **No mezcle ambas columnas en un mismo recuento.**

### `cookies_126_sites_v2.csv` — 126 filas

Versión previa, entrada necesaria de `rebuild_cookies.py`. Se publica porque sin ella la v3 no se reproduce. No la use directamente para análisis.

### `cookies_unclassified_names.csv` — 243 filas

Nombres de cookie observados que no coinciden con ninguna familia de la taxonomía, con el número de sitios en que aparecen. Es la evidencia de la decisión taxonómica: permite discutir si algún nombre debió clasificarse como rastreo.

| Columna | Descripción |
|---|---|
| `nombre_cookie` | Nombre observado. |
| `sitios_en_que_aparece` | Número de sitios distintos. |

### `cookies_divergences_v2.csv` — 14 filas

Control de calidad. Sitios donde la tabla v2 listaba nombres de cookie que no aparecen en el JSON crudo, indicio de pérdida de datos en una fase intermedia.

| Columna | Descripción |
|---|---|
| `id`, `sigla`, `grupo` | Sitio. |
| `nombres_no_presentes_en_crudo` | Nombres afectados. |

### `reconciliation_changes.csv` — 68 filas

Registro de auditoría de la reconciliación entre el inventario y los informes HTML. Producida por `reconcile.py`.

| Columna | Descripción |
|---|---|
| `sigla` | Institución. |
| `campo` | Campo modificado. |
| `antes`, `despues` | Valor anterior y nuevo. |
| `motivo` | Regla que justificó el cambio. |

### `qa_irregularities.csv` — 228 filas

Incidencias detectadas en el inventario, con código de tipo y acción sugerida. Producida por `qa_cookies.py`. Se publica como evidencia del control de calidad, no como dato de análisis.

| Columna | Descripción |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | Sitio. |
| `codigo` | Tipo de incidencia, de `I1` a `I9`. |
| `irregularidad` | Descripción. |
| `valor_actual` | Valor que la motivó. |
| `accion_requerida` | Corrección sugerida. |

### `report_cookies_domestic.csv` — 63 filas · `report_cookies_foreign.csv` — 63 filas

Inventarios por grupo, con los campos de la verificación manual. Son entrada de `build_entries.py`, que los fusiona para reconstruir la tabla de 126 sitios. Las columnas de cookies de estos archivos corresponden a la **verificación en vivo**, no a la medición automatizada.

Nacionales: `#`, `Universidad`, `Sigla`, `Tipo`, `Ciudad`, `Sitio`, `Verificacion`, `Cookies_antes_consentir`, `Nombres_cookies`, `Rastreo`, `CMP_live`, `Banner_live`, `Banner_estudio`, `PolCookies_estudio`.

Extranjeras: `#`, `Universidad`, `Sigla`, `Pais`, `Region`, `Sitio`, `Cookies_antes_consentir`, `Nombres_cookies`, `CMP_detectada`, `Banner_visible`, `Banner_estudio`, `PolCookies_estudio`.

### `documentary_matrix.csv` — 126 filas

Indicadores documentales, codificados inspeccionando el aviso de privacidad de primer nivel de cada institución en agosto de 2026. Son los recuentos que sustentan la Figura 1 del artículo. La produce `extract_documentary_matrix.py`; ver la nota de procedencia más abajo.

| Columna | Descripción |
|---|---|
| `grupo` | `mundo` (referencia) o `ecuador`. |
| `#` | Posición dentro de la tabla de su grupo. **No** es el `id` global del sitio. |
| `Abbr.` | Sigla de la institución. Enlaza con `sigla` en las demás tablas. |
| `C` | País, ISO 3166-1 alfa-2. Solo grupo de referencia. |
| `QS`, `THE`, `ARWU` | Posición en cada ranking, `--` si no está en ese top 75. Solo grupo de referencia. |
| `Type` | Pública o privada. Solo grupo ecuatoriano. |
| `Not.` (referencia) / `Notice` (Ecuador) | Publica aviso de privacidad de primer nivel. |
| `Frm.` / `LOPDP` | Nombra un instrumento legal específico. |
| `Rts.` / `Rights` | Enumera los derechos de la persona titular de los datos. |
| `DPO` | Identifica contacto de privacidad o delegado de protección de datos. |
| `Ckp.` | Publica política de cookies específica. Solo grupo de referencia. |
| `Acc.` | Declara accesibilidad o herramientas de accesibilidad. |
| `Transp.` | Transparencia según la ley ecuatoriana de acceso a la información (LOTAIP). Solo grupo ecuatoriano. **No** es seguridad de transporte. |
| `nueva_2024` | La institución fue creada en 2024 o después, marcada con doble daga en el apéndice del artículo. Solo grupo ecuatoriano. |

Valores: `si` presente, `no` ausente, `parcial` alcance limitado o marco genérico, `nv` no verificable por este método, y `no_aplica` donde la columna no aplica a ese grupo. Ninguna celda queda vacía. Un asterisco final marca las dos celdas corregidas tras la re-verificación manual que reporta el artículo. El código `parcial` se usa 25 veces: 18 en el grupo de referencia y 7 en el censo ecuatoriano. En todos los porcentajes que reporta el artículo se agrega con `no`, lo cual es una decisión del análisis y no una propiedad de la codificación; `documentary_matrix_long.csv` permite calcular cualquier otra agregación.

Los dos grupos se codificaron con conjuntos de columnas en parte distintos, y por eso algunas quedan vacías en un grupo y no en el otro. El grupo ecuatoriano tiene entre dos y seis celdas `nv` por indicador; el de referencia no tiene ninguna. Esa asimetría es en sí misma un hallazgo y queda invisible en los porcentajes agregados.

**Procedencia.** Estos indicadores se codificaron manualmente y se publican institución por institución en los apéndices del artículo. Las dos tablas de apéndice se depositan literalmente como `data/raw/appendix_documentary_tables.tex`, y `extract_documentary_matrix.py` deriva de ellas esta tabla y su forma larga, de modo que toda la derivación se ejecuta dentro de este repositorio. Sin argumentos, el script reproduce exactamente los cinco recuentos de la Figura 1: 59 y 39 para el aviso de privacidad, 47 y 31 para el marco citado, 47 y 35 para los derechos, 54 y 24 para el contacto de privacidad, y 47 y 7 para la declaración de accesibilidad, y aborta si alguno falla. Solo se depositan las dos tablas, no el artículo, que difunde la revista.

### `documentary_matrix_long.csv` — 756 filas

La misma matriz en formato largo, una fila por celda codificada. Columnas: `grupo`, `abbr`, `indicador`, `columna_apendice`, `valor`, `corregida_reverificacion`. Las celdas que no aplican al grupo se omiten en lugar de codificarse, de modo que cada fila lleva una decisión de codificación. Es el formato que hay que usar para cualquier agregación distinta de la que reporta el artículo. Distribución de las 756 celdas codificadas: 451 `si`, 256 `no`, 25 `parcial`, 24 `nv`. Las 24 celdas `nv` pertenecen todas al censo ecuatoriano; el grupo de referencia no tiene ninguna.

### `tls_deficiencies_august2026.csv` — 5 filas

Los cinco sitios ecuatorianos cuya cadena TLS se encontró deficiente en la verificación documental de agosto de 2026. Son la diferencia entre los 63 sitios servidos por HTTPS y los 58 contados como certificado válido en la Figura 1 y en la tabla de results.

| Columna | Descripción |
|---|---|
| `sigla` | Sigla de la institución. |
| `universidad` | Nombre completo. |
| `url` | Portada comprobada. |
| `observacion` | Lo observado en agosto de 2026. |
| `fecha_observacion` | Mes de la observación. |
| `verificacion_posterior` | Resultado de recomprobar la cadena el 5 de septiembre de 2026. |

**Por qué existe este archivo.** Este indicador se codificó inspeccionando cada sitio en un navegador, no con el auditor automatizado, y ambos no miden lo mismo: el campo `https` del auditor registra que la página se sirvió por HTTPS, y Playwright rechaza de plano un certificado inválido, de modo que una cadena rota aparecería como fallo de carga y no como `https: false`. Por eso `results.json` marca `https: true` en los 126 sitios mientras el artículo reporta 58 de 63 para Ecuador.

Los cinco certificados eran válidos al recomprobarlos el 5 de septiembre de 2026, renovados en el intervalo; queda un rastro residual, y es que el dominio raíz de ESPAM MFL sigue sin resolver y solo responde el host `www`. La observación de agosto no es reproducible hoy, lo cual es una propiedad del objeto medido y no un defecto del registro: los sitios cambian, como advierte el README.

### `sensitivity_inclusion.csv` — 3 filas

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

`docs/reports/` contiene cuatro informes navegables generados durante el trabajo de campo. No son datos primarios, pero **sí son entrada del código**: `build_entries.py` extrae de `report_cookies_combined.html` y de `appendix_universities_cookies.html` los datos embebidos en su constante `DATA` de JavaScript, que son necesarios para reproducir la cadena de tablas de cookies. Por eso se publican.

---

## 6. Cadena de dependencias

Quién produce qué, y a partir de qué.

```
results.json ────────────────────────────► study.py
                                                 ├─► study_126_sites.csv
                                                 └─► study_rules_per_site.csv

report_cookies_domestic.csv   ┐
report_cookies_foreign.csv  ├─► build_entries.py ─► data/interim/
report_cookies_combined.html   │                              _comb.json
appendix_universities_cookies.html ┘                              _anex.json
                                                                cookies_126_sites.csv
                                                                     │
data/interim/ ──────────────────► reconcile.py ──────────────────┤
                                     ├─► cookies_126_sites_v2.csv │
                                     └─► reconciliation_changes.csv│
                                                                    │
data/interim/ ──────────────────► qa_cookies.py ─► qa_irregularities.csv

results.json + v2 ───────────► rebuild_cookies.py
                                     ├─► cookies_126_sites_v3.csv
                                     ├─► cookies_unclassified_names.csv
                                     └─► cookies_divergences_v2.csv

cookies_126_sites_v3.csv    ┐
report_cookies_domestic.csv ├─► verify_live_divergence.py   (39 = 35 + 4)
report_cookies_foreign.csv  ┘

data/raw/tracking/ ─────────────► verify_multivantage.py     (sección de resultados)
                                ► sensitivity_inclusion.py   ─► sensitivity_inclusion.csv

appendix_documentary_tables.tex ► extract_documentary_matrix.py ─┬─► documentary_matrix.csv
                                                                 └─► documentary_matrix_long.csv
```

Los archivos de `data/interim/` no se versionan porque `build_entries.py` los regenera desde material que sí está publicado. Todos los pasos del esquema se ejecutan solo con este repositorio.
