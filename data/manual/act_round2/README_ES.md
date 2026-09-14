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

Los 349 elementos aplicables con su resultado y una justificación escrita para
cada uno: 236 cumplen, 113 fallan. Cada fallo se determinó contra la imagen misma,
descargada y examinada. El nombre del archivo conserva el recuento que tenía
cuando se depositó por primera vez.

El archivo reúne dos procedencias, registradas fila a fila en la columna
`evaluator_code`. 345 filas se codificaron con la asistencia de un sistema de
inteligencia artificial generativa y fueron revisadas por el primer autor, de modo
que **no** son una de las dos codificaciones humanas independientes que se usan
para estimar el acuerdo entre codificadores. Las cuatro restantes, las imágenes 27
a 30 de la rejilla de redes sociales de Cornell, las resolvió el primer autor por
sí solo. Eran las últimas filas de esta codificación capaces de decidir un
veredicto de sitio: al cerrarlas no queda abierta ninguna celda de la matriz de
quince por tres, de modo que la tabla de veredictos de arriba es completa y no
provisional.

`code/analysis/comprobar_brecha.py` consolida este archivo, `review_282_rows.csv`
y `recoding/` en los veredictos de sitio y los compara con la auditoría
automatizada. `code/analysis/inventario_revisar.py` informa de lo que sigue
marcado `REVISAR` y separa las filas que aún podrían decidir un veredicto de las
que no.

## review_282_rows.csv

El subconjunto de filas cuyo resultado decidía un veredicto de sitio en el momento de
extraer el archivo: 201 del criterio 1.1.1 y 81 del 2.4.4.

**Solo las 81 filas del 2.4.4 llevan resultado.** Las otras 201 se dejan vacías a
propósito. Cuando la resolución llegó a ellas, el criterio 1.1.1 ya estaba establecido como
fallido en todos los sitios a los que pertenecen, por elementos resueltos en
`qt1vmo_345_resolved.csv`; un veredicto sobre ellas ya no puede cambiar ninguna celda de la
matriz de quince por tres. `code/analysis/inventario_revisar.py` lo informa directamente:
de las filas que siguen marcadas `REVISAR` en la primera codificación, ninguna decide un
veredicto. Resolverlas añadiría completitud al depósito, no evidencia al artículo.

El archivo se extrajo como hoja de trabajo con las columnas de resultado y
justificación vacías, y no llevaba columna `evaluator_code`: los 81 resultados se
rellenaron sin registrar quién los rellenó. La columna se añadió el 14 de
septiembre de 2026 y se fijó en **`R02`** para esas 81 filas, por atestación del
investigador principal de que esa codificación las resolvió. Es una atestación
hecha después, no un código escrito en su momento, y aquí queda registrada como
tal porque 62 de esas filas son las únicas comparaciones por elemento de esta
ronda que sostienen una estimación de fiabilidad entre codificadores.

Los nombres de columna de todos los CSV de esta carpeta están en inglés; los
**valores** codificados siguen en español (`mundo`/`ecuador`, `si`/`no`,
`cumple`/`falla`, `REVISAR`), que es el vocabulario que define el CODEBOOK.

## exclusiones_R04.tsv

Los bloques que quedan fuera de la estimación entre codificadores porque el
recolector, y no el codificador, puso ante el evaluador el texto equivocado.
Separado por tabuladores, una fila por bloque afectado: `grupo` (`A` para el
defecto del style del svg, `B` para la imagen equivocada), `hoja` y `bloque` tal
como los vio el evaluador, `abbr`, `element_n`, `act_rule`, `nombre_en_la_hoja`
(el texto que se mostró de hecho), `selector` y `motivo` en palabras. Treinta y
dos filas que cubren veintinueve bloques distintos; tres bloques llevan los dos
defectos y aparecen dos veces.

La regla la aplica `code/analysis/acuerdo_act.py` a las dos codificaciones por
igual, y la sección de fiabilidad entre codificadores, más abajo, dice cuánto
vale el coeficiente con ella y sin ella.

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

Son los veredictos de la primera codificación, `recoding/` con sus resoluciones.
La segunda codificación devuelve la misma tabla en 1.4.3 y 2.4.4 y difiere en dos
celdas de 1.1.1; la sección de fiabilidad entre codificadores, más abajo, las
nombra y dice qué cambian.

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

A nivel de sitio las dos codificaciones deciden ya las 45 celdas, y la
comparación se reporta más abajo, bajo fiabilidad entre codificadores, que es
donde corresponde: los veredictos de sitio en 1.1.1 y 2.4.4 descansan en el
juicio humano y no son una propiedad del instrumento por sí solo.

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

Tres celdas deben su veredicto a un elemento que solo vio una de las
codificaciones, y no a que ningún codificador discrepe: en Cornell 2.4.4 y en
UTI 1.1.1, `R02` encontró un elemento que falla y `R04` no llegó a verlo; en
IAEN 2.4.4 ocurre lo contrario. En las tres la otra codificación llegó al mismo
veredicto por otros elementos, de modo que ninguna aparece como diferencia; pero
un veredicto de sitio *puede* diferir entre dos codificaciones sin que ningún
codificador discrepe, y eso es una propiedad de la ronda, no de los
codificadores.

## Las reglas de juicio: acuerdo, y por qué no es fiabilidad entre codificadores

El segundo evaluador resolvió las filas de juicio el 11 de septiembre de 2026 con
`instruments/resolver_r04.py`: las 318 filas que aún podían decidir un veredicto
de sitio, 235 `cumple` y 83 `falla`, cada una con su justificación escrita en el
propio campo `notes` de la fila. `recoding_evaluator2/README_ES.md` describe ese
trabajo y su registro. Eso cierra la ronda y hace posible por primera vez una
comparación en las reglas de juicio. **No convierte esa comparación en una
estimación de fiabilidad entre codificadores, y el depósito no reporta ninguna.**

La razón es la procedencia del otro lado. En estas tres reglas el resultado de
`recoding/` no se decidió al recoger, sino después, en `qt1vmo_345_resolved.csv`
y `review_282_rows.csv`. Las 230 comparaciones se parten, por tanto, en dos, y
`code/analysis/acuerdo_act.py` las imprime por separado porque responden a
preguntas distintas:

| Lado `recoding/` decidido por | n | Criterio | Acuerdo | Kappa | Qué es |
|---|---|---|---|---|---|
| `R02`, un codificador humano | 62 | 2.4.4 | 82,3 % | 0,178 [−0,262, 0,619] | fiabilidad entre codificadores |
| `R03`, la resolución asistida | 168 | 1.1.1 | 76,2 % | 0,390 [0,225, 0,555] | acuerdo, no entre codificadores |

**Solo la primera fila es una estimación de fiabilidad entre codificadores, y es
estrecha.** Las 62 comparaciones son enlaces de un único sitio, UCL, bajo las
reglas `5effbb` y `fd3a94`; 49 de las 62 son `cumple` en las dos codificaciones,
una prevalencia del 83,9 % en `R02` y del 91,9 % en `R04`. Con esa prevalencia y
esa n el coeficiente casi no informa: su intervalo va de −0,26 a 0,62 e incluye
el cero, de modo que **no establece la fiabilidad, pero tampoco la refuta.** La
cifra interpretable es el acuerdo observado, el 82,3 %, y descansa en los enlaces
de un solo sitio y no en la muestra.

La segunda fila es el acuerdo entre una codificación humana y una resolución
asistida revisada por el investigador principal. Merece reportarse y aquí se
reporta, pero no es fiabilidad entre codificadores y no se ofrece como tal. Un
coeficiente para 1.1.1 exigiría que un codificador humano decidiera de nuevo esos
168 elementos de imagen sin el archivo asistido delante.

El código `R02` de las 81 filas resueltas de `review_282_rows.csv` se añadió el
14 de septiembre de 2026 por atestación del investigador principal, que declara
que esa codificación las resolvió. La columna no se escribió cuando se rellenó la
hoja, y el depósito registra la atestación como atestación.

Tomadas en conjunto, en las tres reglas que remiten la decisión al juicio humano
—`qt1vmo`, `5effbb`, `fd3a94`— los dos lados coinciden en 179 de 230
comparaciones por elemento: **77,8 % de acuerdo, kappa de Cohen 0,363 con IC del
95 % de [0,209, 0,518]**. Ese total mezcla las dos procedencias anteriores y se
reporta por completitud, no como coeficiente de fiabilidad.

| Regla | n | Acuerdo | Kappa | IC 95% |
|---|---|---|---|---|
| `qt1vmo` (1.1.1) | 168 | 76,2 % | 0,390 | [0,225, 0,555] |
| `5effbb` (2.4.4) | 61 | 83,6 % | 0,212 | [−0,235, 0,659] |
| `fd3a94` (2.4.4) | 1 | 0,0 % | no se reporta, n < 10 | — |
| **Las tres** | **230** | **77,8 %** | **0,363** | **[0,209, 0,518]** |

La matriz de confusión es casi simétrica: 30 filas `cumple` en `R02` y `falla` en
`R04`, 21 al contrario. La prevalencia de `cumple` es del 79,6 % en `R02` y del
75,7 % en `R04`. Con una categoría que domina en ese grado, la kappa queda
deprimida respecto del acuerdo observado —la paradoja de Feinstein y Cicchetti—,
y por eso se dan las dos cifras junto a la prevalencia.

**Sea lo que sea esta cifra, no es el 0,996 de más arriba.** En las reglas
mecánicas el evaluador ejecuta un script y decide la regla, de modo que lo que se
mide es si el instrumento devuelve lo mismo en dos manos. En estas tres reglas la
regla se detiene y pregunta si un nombre sirve un propósito equivalente al de una
imagen, o si el propósito de un enlace puede determinarse a partir de su nombre y
su contexto. Esa pregunta se responde con 0,363, un acuerdo *aceptable* en la
lectura convencional del coeficiente y nada más. Reportar solo la cifra mecánica
describiría mal la ronda; reportar ésta como fiabilidad entre codificadores la
describiría mal en el otro sentido.

### La regla de exclusión

Veintinueve bloques de elemento quedan fuera de esta estimación, enumerados con
su motivo en `exclusiones_R04.tsv`. Los veintinueve son bloques en los que el
recolector, y no el codificador, puso ante el evaluador el texto equivocado: en
diecisiete la línea `nombre` lleva el texto del elemento `style` de un svg en
línea en lugar del nombre accesible, y en quince la línea `imagen` apunta a otro
elemento de la página; tres bloques están en los dos grupos. Los dos defectos
están documentados en `recoding_evaluator2/nota_incidencias.txt`, el primero por
el evaluador y el segundo por el investigador principal.

La regla se fijó antes de computar el coeficiente, se aplica igual a las dos
codificaciones y retira 57 filas. No es un filtro sobre el desacuerdo: de hecho
*baja* el coeficiente, porque los bloques excluidos son de los que las dos
codificaciones coincidían.

### Resoluciones sin fila donde aterrizar

`code/analysis/acuerdo_act.py` traslada las resoluciones a las filas `REVISAR` de
`recoding/` antes de comparar nada, emparejando primero por `element_n` —exacto
dentro de una misma pasada, porque los archivos de resolución salieron de esas
mismas filas— y con el selector más el nombre accesible como respaldo. 402 de las
430 resoluciones aterrizan en una fila. **Las 28 restantes no corresponden a
ninguna fila de `recoding/`**: 13 en IAEN, 7 en UNESUM, 4 en HKUST, 3 en UTI y 1
en UTPL, todas de `qt1vmo`, 19 `falla` y 9 `cumple`. En 21 el selector no aparece
en `recoding/` para ese sitio y esa regla; en las otras 7 sí aparece, pero no
coinciden ni el número de elemento ni el nombre accesible, que es la firma del
contenido rotatorio.

Se dejan fuera de la comparación en lugar de forzarlas sobre una fila, y ningún
veredicto de sitio depende de ellas: los cinco sitios fallan 1.1.1 en las dos
codificaciones por otros elementos. El recuento se imprime en cada ejecución.

### Cuánto depende la cifra de esas decisiones

| Variante | n | Acuerdo | Kappa |
|---|---|---|---|
| Como se reporta | 230 | 77,8 % | 0,363 [0,209, 0,518] |
| Sin la regla de exclusión | 258 | 76,7 % | 0,432 [0,306, 0,558] |
| Emparejando también por `element_n` | 220 | 77,3 % | 0,355 [0,198, 0,512] |

En las tres, el acuerdo se mantiene entre el 76,7 y el 77,8 % y la kappa entre
0,355 y 0,432. La cifra de nivel de sitio es idéntica en las tres.

Una cota distinta y más estrecha: en 8 de los 318 bloques el nombre accesible que
se mostró al evaluador venía recortado a 120 caracteres. Siete se decidieron
`cumple`, y en ellos el fragmento mostrado ya era descriptivo y el nombre
completo solo lo prolonga; el octavo perdió dos caracteres. Ninguna decisión
depende del recorte. `recoding_evaluator2/README_ES.md` da el detalle.

### Veredictos de sitio

La comparación a nivel de sitio no depende en absoluto del emparejamiento de
elementos, y es el nivel en el que el artículo hace sus afirmaciones. Las dos
codificaciones deciden las 45 celdas de sitio por criterio y devuelven el mismo
veredicto en **43 de 45: 95,6 %, kappa 0,776 con IC de [0,473, 1,000]**. Los
criterios 1.4.3 y 2.4.4 son idénticos celda a celda, incluidas las tres celdas en
las que un sitio *sí* satisface un criterio, 1.4.3 en Northwestern, UC Berkeley y
UCL.

La advertencia de procedencia anterior rige también aquí, y de forma desigual:
las quince celdas de 1.4.3 descansan solo en la regla mecánica, de modo que esa
fila de la comparación es una reproducción limpia entre dos operadores, mientras
que las celdas de 1.1.1 y 2.4.4 heredan su veredicto de `recoding/` de la
resolución asistida.

Los dos desacuerdos están en 1.1.1, regla `qt1vmo`, y en los dos `R02` lee
`falla` donde `R04` lee `cumple`:

- **UC Berkeley**, una imagen cuyo nombre accesible es `"A scientist wearing a
  blue lab coat that reads"` —el texto alternativo de la propia página, que se
  corta a mitad de frase—. `R02` leyó el nombre incompleto como fallo; `R04`
  anotó *«el nombre es lo que la imagen muestra»*. El nombre completo está en
  `image_evidence/` y tiene 46 caracteres: el nombre termina realmente ahí.
- **ECOTEC**, dos logotipos de reconocimiento, `qs-logo-white` e
  `innovatec-logo-white`, cuyos nombres accesibles nombran la distinción y no el
  logotipo (`"Reconocimiento QS Stars de Universidad ECOTEC"`, `"World University
  Rankings América y el Caribe"`). `R04` anotó *«el nombre dice más que la
  imagen»* y los leyó como satisfactorios.

Estas dos celdas son el único lugar en el que la segunda codificación cambiaría
una cifra del artículo, y las dos caen en 1.1.1: `R04` encuentra 12 de los 15
sitios fallando ese criterio donde `R02` encuentra 14.

La celda de ECOTEC arrastra una advertencia más, que el depósito registra en
lugar de resolver. El evaluador ha confirmado después que los dos logotipos en
cuestión están entre las imágenes que se renderizaban en blanco sobre fondo
blanco, visibles en la página solo con esfuerzo y con claridad al abrir el propio
archivo. Esa confirmación cierra un punto abierto de
`recoding_evaluator2/nota_incidencias.txt`: es la razón por la que el evaluador no
marcó nada como no visible.

Eso no convierte estos bloques en un defecto del recolector, y por eso **no**
están en `exclusiones_R04.tsv`. Ese archivo tiene un solo fundamento: que el
recolector puso ante el evaluador el texto equivocado. Aquí no lo hizo: el nombre
accesible y la dirección de la imagen son los del propio elemento. Lo que
pregunta la regla `qt1vmo` es si el nombre sirve un propósito equivalente al de
la imagen, y cuán conspicua sea la imagen en la página no forma parte de esa
pregunta. Las dos codificaciones pudieron ver la imagen: `R03` la juzgó desde el
archivo descargado y `R04` desde la página con esfuerzo. Excluir estos bloques
retiraría el único desacuerdo que toca una cifra del artículo, y por un
fundamento que la regla de exclusión no contempla, de modo que el depósito
enuncia la consecuencia en lugar de tomarla.

La consecuencia merece enunciarse con claridad, porque es la mayor dependencia
individual del censo de 1.1.1. El veredicto de ECOTEC en 1.1.1 descansa por
entero en estos dos elementos en **las dos** codificaciones. Si se dejaran de
lado —con el criterio de que un evaluador que no puede ver con facilidad el
contenido no textual no puede juzgar su nombre accesible—, a ninguna de las dos
codificaciones le quedaría un elemento que falle en esa celda, las dos
coincidirían y el sitio dejaría de fallar 1.1.1: el censo ecuatoriano de ese
criterio pasaría a 7 de 8 en lugar de 8 de 8, y el recuento de la brecha de la
§4.5 del artículo bajaría una celda. Es una decisión de los autores y, si se
toma, cambia una cifra reportada y no solo una estimación de fiabilidad.

La ronda 1 y esta ronda no comparten instrumento: la primera codificaba cada
sitio muestreando elementos y juzgando una proporción, y ésta enumera todos los
elementos aplicables bajo reglas ACT. Las diferencias entre ambas sobre las 45
celdas que comparten reflejan ese cambio de instrumento —la enumeración
exhaustiva encuentra fallos que el muestreo proporcional no encuentra— y no un
desacuerdo entre personas. Esa comparación se cuantifica en `../README_ES.md`, y
allí queda etiquetada por lo que mide: el efecto del cambio de instrumento, nunca
el acuerdo entre codificadores. `code/analysis/kappa_rondas.py` la reproduce.
