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

El acuerdo con la primera ronda, sobre las 45 celdas de sitio por criterio que
comparten, es del 62,2 % con una kappa de Cohen de 0,201. **Esa cifra no estima la
fiabilidad entre codificadores.** Los 17 desacuerdos van todos en la misma
dirección, de cumple a falla, que es la firma de un cambio de instrumento y no de
un desacuerdo entre codificadores: la enumeración exhaustiva encuentra fallos que
el muestreo proporcional no encuentra. La cifra se reporta como análisis de
sensibilidad del procedimiento de codificación.

## Advertencia sobre reproducibilidad

Ejecuciones repetidas del mismo sitio el mismo día difieren en uno a cuatro
elementos aplicables en páginas con carruseles o contenido rotatorio. Ningún
veredicto cambió en ninguna repetición. Los recuentos de elementos *no aplicables*
son volátiles y dependen de la tecnología del sitio —un solo sitio aportó 249
filas de no aplicable únicamente por un widget de traducción— y no deben
compararse entre sitios.
