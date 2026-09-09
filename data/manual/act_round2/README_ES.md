# Ronda ACT: recodificación por elemento de tres criterios de conformidad WCAG

*English version: [README.md](README.md)*

Segunda ronda de codificación sobre la submuestra de 15 sitios, 8 de septiembre de
2026. Donde la primera ronda (`../wcag_validation_15_sites.csv`,
`../recoding_*.csv`) codificaba cada sitio muestreando elementos y juzgando una
proporción, esta ronda codifica **todos los elementos aplicables** bajo las reglas
de Accessibility Conformance Testing (ACT) del W3C, cuyo formato pasó a ser
Recomendación del W3C en febrero de 2026.

El vocabulario de resultado es *aplicable*, *cumple*, *falla*, *no aplicable*. No
hay categoría intermedia, lo que elimina la fuente de desacuerdo identificada
entre las rondas anteriores.

Criterios: 1.1.1 contenido no textual, 1.4.3 contraste (mínimo), 2.4.4 propósito
del enlace (en contexto), todos de WCAG 2.2 / ISO/IEC 40500:2025.

Reglas aplicadas: `23a2a8`, `qt1vmo`, `e88epe` para 1.1.1; `afw4f7` para 1.4.3;
`c487ae`, `5effbb`, `fd3a94` para 2.4.4.

---

## recoding/

Quince archivos, uno por sitio, 7 836 filas. Una fila por elemento aplicable, más
filas que registran los elementos a los que la regla no aplica y por qué.

El sufijo `_ok` registra que no había ningún diálogo de consentimiento abierto
cuando se midió el sitio; en caso contrario el recolector nombra el archivo
`_MODALABIERTO` y esas ejecuciones se descartaron. Los diálogos de consentimiento
se cerraron antes de medir, porque el texto que un diálogo tapa no es visible y
quedaría fuera de la regla `afw4f7` por un motivo ajeno a la página. Dos sitios,
NUS e IAEN, solo ofrecían un botón de aceptar.

Las filas marcadas `REVISAR` son aquellas que la regla remite al juicio humano.
Las filas que deciden un veredicto de sitio se resolvieron; el resto se dejaron
marcadas, porque el criterio ya había fallado en otro elemento y su resultado no
puede cambiar el veredicto.

## image_evidence/

Catorce archivos con toda la evidencia necesaria para juzgar la regla `qt1vmo`:
URL de imagen sin recortar, srcset, imagen de fondo CSS, marcado svg en línea,
dimensiones renderizadas y naturales, enlace contenedor y texto próximo. ULVR no
tiene archivo porque ninguna imagen de ese sitio es aplicable a la regla.

Recogidos con una pasada de desplazamiento que dispara la carga diferida. Sin
ella, 22 de 27 imágenes de un sitio eran svg de marcador de posición vacíos en
lugar de fotografías.

## qt1vmo_345_resolved.csv

Los 345 elementos aplicables con su resultado y una justificación escrita para
cada uno: 232 cumplen, 113 fallan. Cada fallo se determinó contra la imagen misma,
descargada y examinada.

La codificación de este archivo se realizó con la asistencia de un sistema de
inteligencia artificial generativa y fue revisada por el primer autor, según
consta en la columna `evaluator_code`. Por tanto **no** es una de las dos
codificaciones humanas independientes que se usan para estimar el acuerdo entre
codificadores.

## review_282_rows.csv

El subconjunto de filas cuyo resultado determina un veredicto de sitio, extraído
para revisión.

Los nombres de columna de todos los CSV de esta carpeta están en inglés; los
**valores** codificados siguen en español (`mundo`/`ecuador`, `si`/`no`,
`cumple`/`falla`, `REVISAR`), que es el vocabulario que define el CODEBOOK.

## instruments/

`act_recode.js` — recolector de los tres criterios, se ejecuta en la consola del
navegador.
`act_images.js` — recolector de evidencia de imagen para `qt1vmo`.
`act_recode_evaluator2.js` — el mismo recolector preparado para un segundo
evaluador.
`SECOND_EVALUATOR_MANUAL.md` — protocolo de recogida para el segundo evaluador.
`EVALUATOR_DECISION_CRITERIA.md` — criterios de decisión para las filas de juicio,
construidos sobre las definiciones y los ejemplos oficiales de las reglas del W3C.
Deliberadamente no contiene ningún ejemplo de los quince sitios en evaluación.

---

## Qué establece la ronda

| Criterio | Grupo de referencia | Censo ecuatoriano |
|---|---|---|
| 1.1.1 | 6 de 7 no satisfacen | 8 de 8 |
| 1.4.3 | 4 de 7 | 8 de 8 |
| 2.4.4 | 7 de 7 | 8 de 8 |

Ningún sitio satisface los tres. Las ocho instituciones ecuatorianas fallan los
tres.

## Reproducibilidad del instrumento

Esta ronda tiene dos codificaciones independientes: `recoding/`, del 8 de
septiembre de 2026 (`R02`), y `recoding_evaluator2/`, del 9 de septiembre
(`R04`). `code/analysis/acuerdo_act.py` las compara y escribe
`data/processed/act_agreement_summary.csv` y
`act_agreement_disagreements.csv`.

Sobre las tres reglas que deciden mecánicamente —`23a2a8`, `afw4f7` y
`c487ae`— las dos codificaciones coinciden en 3 186 de 3 189 comparaciones por
elemento: **99,9 % de acuerdo, kappa de Cohen 0,996 con IC 95 % [0,991, 1,000]**,
con idéntica prevalencia de `cumple`, el 86,7 % en ambas. El acuerdo sobre qué
elementos son aplicables es del 99,1 % con kappa 0,981.

**Esto estima la reproducibilidad del instrumento entre operadores
independientes, no la fiabilidad entre codificadores.** En estas tres reglas el
evaluador solo ejecuta el script; la regla decide sola.

Los tres desacuerdos están listados en `act_agreement_disagreements.csv` y
explican el mecanismo de la variación. Uno es una etiqueta fuera de pantalla de
Cornell, `label.offscreen`, cuyo contraste se computó como 1,00:1 en una
ejecución y 9,81:1 en la otra: un ratio de 1,00:1 significa que texto y fondo
son del mismo color, de modo que el desacuerdo está en la frontera de lo que
cuenta como carácter visible, que es donde la regla `afw4f7` deja de aplicar.
Los otros dos son enlaces de UTI dentro de contenido rotatorio, una rejilla de
entradas y un carrusel, cuyo nombre accesible depende de qué elemento ocupaba la
casilla al medir. **Los dos van en direcciones opuestas**, de modo que la
variación no tiene sesgo sistemático.

A nivel de sitio, las dos codificaciones devuelven el mismo veredicto en las 34
de las 45 celdas de sitio por criterio que ambas pueden decidir, incluidas las
tres únicas en las que un sitio *sí* satisface un criterio: 1.4.3 en
Northwestern, UC Berkeley y UCL. Las 11 celdas restantes contienen filas
remitidas al juicio humano que una de las dos codificaciones no ha resuelto
todavía.

## Emparejamiento de elementos, y qué queda fuera

Las dos codificaciones enumeran los elementos por separado y las portadas
cambian de un día para otro, de modo que `element_n` no designa el mismo
elemento en las dos. La comparación empareja por sigla, criterio, regla y
selector. Emparejan 7 037 elementos; quedan sin pareja 799 filas de `R02` y 98
de `R04`.

La mayor parte de ese hueco no es una diferencia de codificación. **607 de las
799 filas sin pareja de `R02` son filas de elementos no aplicables**, que no
entran en ningún cálculo de acuerdo ni pueden cambiar un veredicto, y **504 de
ellas pertenecen a un único widget de traducción** cuya lista de idiomas se
renderizó en la ejecución del 8 de septiembre y no en la del 9: ese widget
aporta 259 filas en IAEN y 264 en UTI en `R02`, frente a 7 y 12 en `R04`.

Lo que el hueco sí deja fuera son **129 filas de `R02` y 47 de `R04` que llevan
un resultado definitivo**: elementos que una ejecución vio y la otra no. El
acuerdo anterior se calcula, por tanto, sobre el 96,1 % de las filas decididas
de `R02` y el 98,5 % de las de `R04`.

Dos de las once celdas sin cerrar lo están por ese motivo y no por desacuerdo:
en Cornell 2.4.4 y en UTI 1.1.1, `R02` encontró un elemento que falla y `R04` no
llegó a verlo; en IAEN 2.4.4 ocurre lo contrario. Un veredicto de sitio puede
así diferir entre dos codificaciones sin que ningún codificador discrepe.

## Fiabilidad entre codificadores: todavía no estimada

Las filas que las reglas remiten al juicio humano —318 de `qt1vmo`, 1 016 de
`5effbb` y 17 de `fd3a94`— siguen marcadas `REVISAR` en `recoding_evaluator2/`.
Hasta que un segundo evaluador las resuelva con
`../instruments/resolver_r04.py`, esta ronda no permite estimar fiabilidad entre
codificadores, y no se reporta ninguna.

La ronda 1 y esta ronda no comparten instrumento: la primera codificaba cada
sitio muestreando elementos y juzgando una proporción, y ésta enumera todos los
elementos aplicables bajo reglas ACT. Las diferencias entre ambas sobre las 45
celdas que comparten reflejan ese cambio de instrumento —la enumeración
exhaustiva encuentra fallos que el muestreo proporcional no encuentra— y no un
desacuerdo entre personas. Por eso no se reporta ningún estadístico de acuerdo
para esa comparación: mediría el cambio de instrumento, no el acuerdo entre
codificadores.
