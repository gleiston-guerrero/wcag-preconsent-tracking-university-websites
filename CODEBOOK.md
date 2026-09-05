# Libro de códigos

Codificación de caracteres UTF-8, separador coma, comillas dobles, fin de línea CRLF. Los campos vacíos representan ausencia de dato, no cero.

La columna `id` identifica cada uno de los 126 sitios auditados. La columna `grupo` toma los valores `ecuador` y `mundo` (`Ecuador` y `Mundo` en `resultados.csv`).

**Atención al unir tablas.** Existen dos numeraciones. Las partes I y II usan la del archivo crudo, con el grupo ecuatoriano primero. Las tablas de validación manual de la parte III usan la contraria, con el grupo de referencia primero, y llevan una columna adicional `id_auditoria` con el identificador equivalente. Toda unión entre la parte III y las demás debe hacerse por `id_auditoria`.

---

# Parte I — Auditoría automatizada

## `datos/resultados.json` — 126 registros

Salida cruda de `claude_auditar.js`. Lista de objetos, uno por sitio, con las claves `id`, `grupo`, `sigla`, `nombre`, `pais`, `url`, `ok`, `https`, `cookies`, `accesibilidad`, `axe_version` y `fecha`.

`cookies` y `accesibilidad` son estructuras anidadas: la primera contiene las cookies presentes antes del consentimiento con sus nombres y su clasificación; la segunda, las violaciones de axe-core con su regla, impacto, criterio y nodos afectados. Es la fuente de la que derivan todos los demás archivos de esta parte.

## `datos/resultados.csv` — 126 filas

Versión aplanada del anterior, una fila por sitio.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | entero | Identificador del sitio. |
| `grupo` | categoría | `Ecuador` o `Mundo`. |
| `sigla` | texto | Sigla de la institución. |
| `pais` | texto | Código ISO de dos letras. |
| `url` | texto | Portada auditada. |
| `ok` | booleano | `true` si la visita se completó. |
| `error` | texto | Mensaje de error si la visita falló. Vacío en todas las filas de este conjunto. |
| `title` | texto | Título de la página. |
| `lang` | texto | Valor del atributo `lang` del elemento raíz. |
| `viewport` | 0 / 1 | Presencia de metaetiqueta viewport. |
| `https` | 0 / 1 | La portada responde por HTTPS. |
| `cookies_pre` | entero | Cookies depositadas antes del consentimiento. |
| `rastreo_pre` | entero | De las anteriores, cuántas son de proveedores de seguimiento. |
| `nombres_rastreo` | texto | Nombres de esas cookies, separados por barra vertical. |
| `cmp` | texto | Plataforma de gestión de consentimiento detectada. Vacío si no se detectó ninguna. |
| `banner` | 0 / 1 | Banner de consentimiento visible en la carga inicial. |
| `ax_violaciones` | entero | Reglas de axe-core incumplidas. |
| `ax_nodos` | entero | Nodos afectados, sumando todas las reglas. |
| `nivelA_nodos`, `nivelAA_nodos`, `nivelAAA_nodos` | entero | Nodos afectados por nivel de conformidad. |
| `Perceptible`, `Operable`, `Comprensible`, `Robusto` | entero | Nodos afectados por principio WCAG. |
| `max_nivel_sin_fallo_auto` | categoría | `A`, `AA`, `AAA` o `ninguno`. |

## `datos/estudio_126_sitios.csv` — 126 filas

Tabla analítica por sitio, producida por `estudio.py`. Repite parte de lo anterior con nombres normalizados y añade campos derivados.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `grupo`, `sigla`, `pais`, `url` | | Como arriba; `grupo` en minúsculas. |
| `universidad` | texto | Nombre completo de la institución. |
| `fecha` | fecha y hora | Momento de la auditoría, ISO 8601 con zona UTC. |
| `axe_version` | texto | `4.13.0` en todas las filas. |
| `ok`, `https`, `banner`, `viewport`, `skip_link` | `yes` / `no` | Indicadores booleanos. `skip_link` señala la presencia de un enlace de salto al contenido. |
| `cookies_total_pre` | entero | Cookies antes del consentimiento. |
| `cookies_rastreo_pre` | entero | De las anteriores, cuántas son de seguimiento. |
| `nombres_pre` | texto | Nombres de todas las cookies, separados por barra vertical. |
| `nombres_rastreo` | texto | Nombres de las de seguimiento. |
| `cmp` | texto | Plataforma de consentimiento detectada. |
| `title`, `lang` | texto | Título y atributo `lang`. |
| `ax_violaciones`, `ax_nodos` | entero | Reglas incumplidas y nodos afectados. |
| `nodos_A`, `nodos_AA`, `nodos_AAA` | entero | Nodos por nivel. |
| `perceptible`, `operable`, `comprensible`, `robusto` | entero | Nodos por principio. |
| `max_nivel_sin_fallo` | categoría | `A`, `AA`, `AAA` o `ninguno`. Nivel más alto sin ningún fallo automático detectado. |
| `incompletos` | entero | Comprobaciones que axe-core no pudo resolver y requieren revisión humana. Rango observado: 0 a 6. |
| `passes` | entero | Comprobaciones superadas. |

## `datos/estudio_reglas_por_sitio.csv` — 441 filas

Una fila por cada regla de axe-core incumplida en cada sitio. Un sitio con tres violaciones aporta tres filas.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `grupo`, `sigla` | | Identifican el sitio. |
| `regla` | texto | Identificador de la regla de axe-core, por ejemplo `color-contrast`. |
| `impacto` | categoría | `moderate`, `serious` o `critical`. |
| `criterio` | texto | Criterio de éxito de WCAG asociado. |
| `principio` | categoría | `Perceptible`, `Operable`, `Comprensible` o `Robusto`. |
| `nivel` | categoría | `A`, `AA` o `AAA`. |
| `nodos` | entero | Elementos afectados por esa regla en ese sitio. |
| `ayuda` | texto | Descripción de la regla, en inglés, tal como la entrega axe-core. |

## `datos/universidades.json` — 126 registros

Lista de sitios auditados: identificador, grupo, sigla, nombre y URL. Es la entrada de los scripts de auditoría.

## `datos/claude_seleccion63-mundo.json` — 63 registros

Construcción del grupo de referencia. Un objeto por institución con las claves `consenso`, `nombre`, `pais`, `present`, `qs`, `the`, `arwu` y `avg`: el número de rankings en que aparece, su posición en cada uno y la media de posiciones. Documenta por qué cada institución entró en la muestra.

---

# Parte II — Cookies previas al consentimiento

## `datos/cookies_126_sitios_v3.csv` — 126 filas

Producida por `reconstruir_cookies.py`. Las columnas de medición se derivan de `resultados.json`; las documentales proceden de la verificación manual de cada sitio.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `grupo`, `sigla`, `universidad` | | Identifican el sitio. |
| `sitio` | texto | Portada medida. |
| `fecha` | fecha y hora | Momento de la medición, ISO 8601. |
| `cookies_antes_consentir` | entero | Cookies depositadas antes de cualquier interacción. |
| `nombres_cookies` | texto | Sus nombres, separados por barra vertical. |
| `n_nombres_listados` | entero | Cuántos nombres recoge la columna anterior. |
| `rastreo` | `yes` / `no` | Alguna cookie coincide con la taxonomía base o con la extendida. |
| `rastreo_base` | `yes` / `no` | Alguna cookie coincide solo con la taxonomía base. Permite reproducir la clasificación anterior a la revisión. |
| `proveedores_rastreo` | texto | Proveedores identificados, separados por barra vertical. |
| `procedencia_rastreo` | texto | Qué taxonomías intervinieron y con qué proveedores. |
| `banner_estudio` | categoría | `yes` o `no_detectable`, según la medición automatizada. |
| `cmp_estudio` | texto | Plataforma de consentimiento detectada por el script. |
| `pais`, `region`, `ciudad` | texto | Localización de la institución. |
| `tipo` | categoría | Régimen de financiación: `Pública`, `Cofinanciada`, `Autofinanciada`. Vacío en las instituciones de referencia. |
| `cmp_verificacion` | texto | Plataforma identificada en la verificación manual. |
| `banner_verificacion` | `yes` / `no` | Banner observado en la verificación manual. |
| `fuente_verificacion` | texto | `verificacion en vivo`. |
| `polcookies_estudio` | `yes` / `no` | Política de cookies publicada y localizable. |
| `nota_documental` | texto | Observación sobre el documento localizado: tipo, año, marco legal citado. |

### Taxonomía base

Transcripción literal de la constante `RASTREO` de `claude_auditar.js`. El script de reconstrucción verifica que reproduce el campo `rastreo_pre` del archivo crudo en los 126 sitios.

| Proveedor | Patrones |
|---|---|
| Google Analytics y Ads | `^_ga`, `^_gid$`, `^__utm`, `^_gcl_au$`, `^_gac_` |
| Meta | `^_fbp$`, `^_fbc$`, `^fr$` |
| TikTok | `^_tt_`, `^_ttp$` |
| Microsoft Clarity y Bing | `^_clck$`, `^_clsk$`, `^MUID$`, `^_uet` |
| Hotjar | `^_hj` |
| Siteimprove, Matomo, PixelYourSite, Pinterest | `^nmstat$`, `^_pk_`, `^pys`, `^_pin_` |
| Adobe y Tealium | `^AMCV_`, `^s_`, `^utag`, `^mbox` |
| Baidu | `^Hm_lvt_`, `^Hm_lpvt_`, `^HMACCOUNT$`, `^BAIDUID$` |
| Quantcast, LinkedIn, LiveRamp, X | `^__qca$`, `^ln_or$`, `^_lc2_`, `^personalization_id$` |
| YouTube y DoubleClick | `^YSC$`, `^VISITOR_INFO`, `^IDE$`, `^test_cookie$` |

### Taxonomía extendida

Proveedores identificados al revisar los nombres que la taxonomía base no atribuía. Se aplica a los 126 sitios.

| Proveedor | Patrones | Función declarada |
|---|---|---|
| Sourcebuster | `^sbjs_` | atribución de tráfico |
| ContentSquare | `^_cs_` | analítica de sesión |
| LinkedIn | `^bcookie$`, `^bscookie$`, `^lidc$`, `^li_sugr$`, `^li_gc$`, `^UserMatchHistory$`, `^AnalyticsSyncHistory$` | identificación y sincronización publicitaria |
| Microsoft | `^CLID$`, `^ANONCHK$`, `^MR$`, `^SM$`, `^SRM_B$` | medición e identificación entre dominios |
| TikTok | `^ttcsid` | identificador de sesión de conversión |
| X/Twitter | `^_twpid$` | identificador de asociación |
| PubMatic | `^pbid$` | identificador publicitario |
| PixelYourSite | `^_pys`, `^last_pys` | atribución de tráfico |
| Adobe | `^AMCVS_` | identificador de sesión |

De los 25 sitios en que la ampliación detecta algún proveedor, ninguno cambia de clasificación: todos llevaban ya una cookie reconocida por la taxonomía base. El único sitio cuya clasificación depende de la taxonomía extendida es UPEC, por sus cookies `sbjs_*`.

## `datos/cookies_nombres_sin_clasificar.csv` — 215 filas

Nombres de cookie que ninguna taxonomía atribuye a un proveedor de seguimiento.

| Columna | Tipo | Descripción |
|---|---|---|
| `nombre_cookie` | texto | Nombre tal como lo registró el navegador. |
| `sitios_en_que_aparece` | entero | Número de sitios en que se observó. |

La mayoría son cookies de sesión, balanceo de carga o protección frente a bots: `PHPSESSID`, `JSESSIONID`, `__cf_bm`, `AWSALB`, `cf_clearance`. Se publica para que la clasificación sea auditable.

## `datos/cookies_divergencias_v2.csv` — 14 filas

Constancia del motivo por el que se descartó una tabla anterior.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `sigla`, `grupo` | | Identifican el sitio. |
| `nombres_no_presentes_en_crudo` | texto | Nombres que aquella tabla listaba y que `resultados.json` no registra. |

## `datos/qa_irregularidades.csv` — 228 filas

Control de calidad de la tabla de cookies descartada. Se conserva por trazabilidad del proceso; no debe usarse como fuente de ningún indicador. Una fila por irregularidad detectada.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | | Identifican el sitio. |
| `codigo` | categoría | Código de irregularidad, `I1` a `I9`. |
| `irregularidad` | texto | Descripción del código. |
| `valor_actual` | texto | Valor que presentaba el campo afectado. |
| `accion_requerida` | texto | Qué hacer, o constancia de que no procede acción. |

| Código | Irregularidad |
|---|---|
| `I1` | Medición de cookies ausente |
| `I2` | Verificación en vivo sin completar |
| `I3` | Lista de nombres de cookies truncada |
| `I4` | Sin banner en el estudio pero visible en vivo |
| `I5` | Banner en el estudio pero ausente en vivo |
| `I6` | Sin clasificación de rastreo |
| `I7` | Plataforma de consentimiento cargada sin banner visible |
| `I8` | Valor sin tilde en `rastreo_ec` |
| `I9` | Campo multivalor separado por coma |

No todos los códigos señalan errores. `I7` registra sitios que cargan una plataforma de gestión de consentimiento sin llegar a mostrar el banner: es un hallazgo sustantivo del estudio, y su columna `accion_requerida` lo indica expresamente. `I4` e `I5` recogen discrepancias entre la medición automatizada y la verificación en vivo, que pueden deberse a que el banner se muestre por región o por sesión.

## `datos/cambios_reconciliacion.csv` — 68 filas

Traza de las correcciones aplicadas al conciliar fuentes en la tabla descartada. Se conserva por trazabilidad; no debe usarse como fuente de ningún indicador. Una fila por cambio.

| Columna | Tipo | Descripción |
|---|---|---|
| `sigla` | texto | Institución afectada. |
| `campo` | categoría | Campo modificado: `rastreo`, `cookies_antes_consentir` o `nombres_cookies`. |
| `antes` | texto | Valor anterior. |
| `despues` | texto | Valor adoptado. |
| `motivo` | texto | Razón del cambio. |

Los cuatro motivos que aparecen son: importación desde el informe HTML combinado, restauración desde esa misma fuente, conservación del valor del CSV por ser posterior al HTML, y reclasificación porque las cookies coinciden con la lista de seguimiento de `auditar.js`.

---

# Parte III — Validación manual WCAG

## Categorías comunes

**Código de criterio** (`codigo`, `codigo_entregado`, `codigo_admisible`, `codigo_primera`, `codigo_segunda`)

| Valor | Significado |
|---|---|
| `1` | Cumple. Exige `f = 0`. |
| `P` | Parcial. `f/n ≤ 0,20`. |
| `0` | No cumple. `f/n > 0,20`. |
| `EXCLUIDO` | Solo en `codigo_admisible`. La evidencia de la propia persona evaluadora descarta el código que declaró, pero no permite asignar otro. |
| vacío | Sin evaluación. |

**Criterio** (`criterio`): `1.1.1` contenido no textual · `1.4.3` contraste mínimo, nivel AA · `2.4.4` propósito del enlace en su contexto.

**Persona evaluadora**: `E01`–`E10` en la primera evaluación, `D01` en la segunda. Seudónimos; ver README.

## `validacion_wcag/wcag_validacion_15_sitios.csv` — 45 filas

Primera evaluación. Una fila por sitio y criterio. Recoge a la persona retenida en cada sitio tras auditar las doce entregas recibidas.

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | entero | Identificador del sitio en la numeración de la validación. |
| `id_auditoria` | entero | Identificador equivalente en el resto del depósito. Es la columna con la que debe unirse. |
| `grupo` | texto | `ecuador` o `mundo`. |
| `sigla` | texto | Sigla de la institución. |
| `url` | texto | Portada evaluada. |
| `criterio` | texto | Criterio de éxito. |
| `criterio_nombre` | texto | Nombre del criterio. |
| `codigo` | categoría | Código asignado. |
| `n` | entero | Elementos inspeccionados para ese criterio. |
| `f` | entero | Elementos que fallan el criterio. |
| `f_sobre_n` | decimal | `f/n`, redondeado a cuatro decimales. |
| `evaluador_cod` | categoría | Seudónimo. |
| `fecha` | fecha | Día de la inspección, `AAAA-MM-DD`. |
| `duracion_min` | entero | Duración declarada de la sesión, en minutos. Sustituye a las horas de reloj. |
| `configuracion` | texto | Configuración del navegador tal como se observa en las capturas o se declara. |
| `capturas` | entero | Capturas aportadas en la entrega completa, no por criterio. |
| `estado` | categoría | `ADMITIDA`, `ADMITIDA CON RESERVA`, `NO ADMISIBLE`. |
| `dictamen_tecnico` | texto | Resultado de la auditoría de esa entrega: qué respalda la evidencia, qué reserva queda, qué comprobación externa se hizo. |

`estado` se aplica a la entrega completa de esa persona en ese sitio, de modo que las tres filas de un mismo sitio comparten valor. Las filas con `NO ADMISIBLE` conservan los códigos por transparencia y no deben usarse.

## `validacion_wcag/wcag_doble_evaluacion_5_sitios.csv` — 15 filas

Segunda evaluación independiente sobre los cinco sitios de control.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `id_auditoria`, `grupo`, `sigla`, `url`, `criterio`, `criterio_nombre` | | Como arriba. |
| `codigo_entregado` | categoría | Código tal como lo declaró la persona evaluadora. |
| `codigo_admisible` | categoría | Código utilizable tras contrastarlo con su propia evidencia. Coincide con el anterior salvo donde vale `EXCLUIDO`. |
| `n_declarado_unico_por_sitio` | entero | Elementos inspeccionados. **Se declaró un solo valor por sitio, no uno por criterio**, de ahí el nombre. |
| `f_declarado_unico_por_sitio` | entero | Elementos que fallan, con la misma salvedad. |
| `f_sobre_n` | decimal | Cociente del par anterior. |
| `coherente_con_nf` | `si` / `NO` | Si el código declarado se deriva del cociente del sitio. `NO` no significa que el código sea falso, sino que no hay recuento propio del criterio contra el que verificarlo. |
| `evaluador_cod` | categoría | `D01`. |
| `fecha` | fecha | Fecha declarada en la hoja de entrega. |
| `nodo_inspeccionado` | texto | Elemento del DOM seleccionado en la captura correspondiente, transcrito de ella. |
| `documenta_criterio` | `SI` / `NO` / `PARCIAL` | Si la captura documenta el criterio bajo el que está archivada. |
| `tipo_correccion` | categoría | `NINGUNA`, `CONFIRMA` (la evidencia sostiene el código), `CORRIGE` (la evidencia lo descarta). |
| `justificacion` | texto | Razonamiento de la fila anterior. |

Regla aplicada para `tipo_correccion`: una captura puede demostrar que al menos un elemento falla, y con ello que `f ≥ 1`, lo que descarta el código `1`. Nunca puede demostrar que `f = 0`, porque inspecciona un elemento y no la muestra. Tampoco puede separar `P` de `0`, porque esa frontera depende del cociente. Solo es corregible, por tanto, la celda en la que se declaró `1` y la captura muestra un elemento que falla.

## `validacion_wcag/wcag_pares_kappa.csv` — 15 filas

Emparejamiento de primera y segunda evaluación en los sitios de control.

| Columna | Tipo | Descripción |
|---|---|---|
| `id`, `id_auditoria`, `sigla`, `criterio` | | Como arriba. |
| `evaluador_primera_cod` | categoría | Seudónimo de la primera evaluación. |
| `codigo_primera` | categoría | Su código. |
| `n_primera`, `f_primera` | entero | Su recuento para ese criterio. |
| `evaluador_segunda_cod` | categoría | `D01`. |
| `codigo_segunda` | categoría | Código de la segunda evaluación, tal como se entregó. |
| `acuerdo` | 0 / 1 / vacío | `1` si los dos códigos coinciden. Vacío en las filas excluidas. |
| `entra_en_kappa` | `si` / `no` | Filtro del escenario adoptado. |
| `motivo_exclusion` | texto | Vacío salvo en la fila excluida. |

Para reproducir el escenario alternativo de los quince pares, ignórese `entra_en_kappa` y trátese `codigo_segunda` como el valor de la segunda persona en todas las filas. El script `scripts/kappa_wcag.py` calcula ambos.

## `validacion_wcag/wcag_validacion_anonimizado.xlsx`

Mismos datos en tres hojas (`validacion`, `doble_evaluacion`, `pares_kappa`) más una hoja `LEEME`. En `pares_kappa` el bloque final calcula po, pe y κ mediante fórmulas vivas sobre las filas de la hoja. Los valores numéricos van en azul y los calculados en negro.
