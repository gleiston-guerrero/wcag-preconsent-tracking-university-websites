# Codificación independiente de la ronda ACT por un segundo evaluador

*English version: [README.md](README.md)*

Quince archivos, uno por sitio, 7 135 filas. Las mismas quince portadas, los
mismos tres criterios de conformidad y las mismas siete reglas ACT que
`../recoding/`, codificados de forma independiente por un segundo evaluador el 9
de septiembre de 2026 con `../instruments/act_recode_evaluator2.js`.

No es una tercera ronda ni una repetición de la medición. Es la segunda de dos
codificaciones independientes de una misma ronda, y es lo que permite medir la
reproducibilidad del instrumento ACT entre dos operadores. En las reglas que
remiten la decisión al juicio humano solo una parte de la comparación es humana
contra humana —62 elementos de enlace del criterio 2.4.4—, mientras que el lado
de 1.1.1 corre contra una resolución asistida y no sostiene, por tanto, ningún
coeficiente entre codificadores; `../README_ES.md` expone las dos. El
evaluador trabajó a partir de
`../instruments/SECOND_EVALUATOR_MANUAL_ES.md` y no vio la primera codificación,
ni las rondas anteriores, ni el borrador del artículo.

Los nombres de columna están en inglés; los **valores** codificados siguen en
español (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), que es el
vocabulario que define el CODEBOOK. Igual que en `../recoding/`.

## Código de evaluador

Los archivos se depositan bajo `R04`. El instrumento de recogida lleva un código
de marcador de posición, que el evaluador dejó sin cambiar; el código de esta
codificación se asignó al depositar los archivos y la columna `evaluator_code` se
fijó en consecuencia. No se alteró nada más de lo entregado, y los nombres de
archivo se normalizaron al formato de fecha que usa el resto del depósito.

## Un primer intento descartado

Una primera recogida del mismo día se descartó antes de depositarla. El navegador
del evaluador tenía activada la traducción automática, que reescribe la página:
los nombres accesibles volvían en español en los sitios en inglés y el navegador
había insertado elementos `font` en el DOM. El efecto recaía casi por completo
sobre los seis sitios en inglés del grupo de referencia y sobre ninguno de los
ocho ecuatorianos, de modo que habría sesgado exactamente la comparación que hace
el estudio. La recogida se repitió con la traducción desactivada. Los archivos de
esta carpeta proceden de esa segunda recogida y no contienen ningún elemento
`font` inyectado.

## Qué establece

En **1.4.3** y **2.4.4** la segunda codificación reproduce la primera
exactamente: en 1.4.3, donde la regla no deja nada al juicio, cuatro de los siete
sitios del grupo de referencia y los ocho ecuatorianos no satisfacen el criterio;
en 2.4.4 los quince sitios fallan en las dos codificaciones.

En **1.1.1** las dos codificaciones difieren en dos de los quince sitios, ECOTEC
y UC Berkeley, que esta codificación lee como satisfactorios y la primera como
fallidos. Esta codificación encuentra, por tanto, 12 de los 15 sitios fallando
1.1.1 donde la primera encuentra 14. Los dos desacuerdos son juicios de elemento
de la regla `qt1vmo` y los dos se exponen en `../README_ES.md`.

Ninguna celda de la matriz de quince por tres sigue siendo provisional: las filas
de juicio que podían decidir un veredicto se resolvieron el 11 de septiembre de
2026 (más abajo), de modo que los veredictos registrados aquí son veredictos, no
cotas inferiores.

## Cierre de las filas de juicio

El recolector deja marcadas `REVISAR` las filas que las reglas ACT remiten al
juicio humano: 1 351 de las 7 135. `../instruments/resolver_r04.py` las extrae a
una hoja de trabajo en texto plano y devuelve a estos archivos las decisiones del
evaluador, recalculando los veredictos de sitio.

Extrae solo las **318 filas que todavía deciden un veredicto de sitio**, 203 del
criterio 1.1.1 y 115 del 2.4.4. Donde un criterio ya falla en un sitio por otro
elemento, ninguna fila pendiente de ese sitio puede cambiar el veredicto, de modo
que esas filas se dejan marcadas. Es la política que sigue la primera
codificación. Se enuncia aquí porque tiene un coste: un evaluador que reciba solo
esas filas puede deducir qué sitios seguían abiertos. La alternativa, las 1 351
filas, es cuatro veces el trabajo y no cambia ninguna cifra reportada.

Las 318 filas las resolvió el evaluador el 11 de septiembre de 2026 en una sola
sesión de unas cinco horas: **235 `cumple` y 83 `falla`**, cada una con su
justificación escrita. La justificación se añade al propio campo `notes` de la
fila detrás de la marca `|| RESUELTO R04:`, de modo que la decisión y la
evidencia que vio el evaluador viajan juntas y el texto original del campo no se
sobrescribe. Nada más cambió en los quince archivos: la fusión modificó las
columnas `outcome` y `notes` de exactamente esas 318 filas y ninguna otra
columna, fila ni archivo.

`registro_R04.tsv` es el registro que la herramienta escribió mientras avanzaba
el trabajo: una línea por decisión, con la fecha y hora, el código del evaluador,
la hoja, el bloque, el sitio, la regla y el resultado. Contiene 331 líneas para
318 bloques porque trece bloques se decidieron dos veces; vale la segunda
decisión. Cuatro decisiones se cambiaron fuera de la herramienta y por eso no
constan en él; `nota_incidencias.txt` las enumera.

`nota_incidencias.txt` es la nota de incidencias del evaluador, compilada por el
investigador principal a partir de las justificaciones escritas, del registro de
la sesión y de observaciones que el evaluador comunicó de palabra, que van
marcadas como tales. Su último apartado es del investigador principal y va
etiquetado como no perteneciente al evaluador. Dos campos, la versión del
navegador y la lista de extensiones activas, siguen marcados como pendientes.

## Consistencia interna de las justificaciones

Dos fórmulas se repiten en las justificaciones escritas y se usan de forma
consistente. *«Aunque no tenga contexto»* quiere decir que el nombre por sí solo
está lo bastante claro como para no tener que leer el contexto; aparece como
única justificación de 47 decisiones y las 47 son `cumple`. *«No hay contexto»* y
*«Sin contexto no sabría»* quieren decir lo contrario, que el nombre por sí solo
no alcanza; aparecen 4 veces y las 4 son `falla`.

Un par es inconsistente, y queda registrado en lugar de ajustado. Bajo la regla
`5effbb`, el enlace de salto de UCL, nombre accesible `"Skip to main content"`,
se decidió `cumple`, y el de Cornell, `"Skip to content"`, se decidió `falla`;
ninguno tiene contexto programático y los dos enlaces son funcionalmente el
mismo. Es un juicio de elemento en cada dirección y forma parte de lo que mide la
cifra de acuerdo de `../README_ES.md`.

## Nombres accesibles recortados

El campo `notes` muestra el nombre accesible hasta 120 caracteres. En **8 de los
318 bloques** el nombre presentado al evaluador era más corto que el que
`../image_evidence/` registra para el mismo elemento. Siete de los ocho se
decidieron `cumple`, y en ellos el recorte no pudo cambiar la decisión: el
fragmento mostrado ya era descriptivo y el nombre completo lo prolonga. El octavo
se decidió `falla` y perdió dos caracteres. Los nombres completos están en
`image_evidence/`, y `../README_ES.md` enuncia la cota que esto pone a la
estimación de acuerdo.

## Una limitación del recolector

`act_recode_evaluator2.js` acota la longitud del campo `notes` y lo recorta por la
izquierda. Cuando el nombre accesible de una imagen es largo, lo que se pierde es
el principio de la dirección de la imagen. De las 203 filas del criterio 1.1.1 que
deciden un veredicto, 44 traen la dirección completa, 34 se pueden reconstruir a
partir del servidor del sitio y verificar, 70 llegan recortadas sin posibilidad de
recuperarlas, y 55 no traen ninguna porque la imagen es un fondo CSS o un svg en
línea.

Una reconstrucción se acepta solo cuando el fragmento recibido es sufijo exacto de
la dirección reconstruida; donde no lo es, la hoja declara que la dirección venía
recortada y ofrece en su lugar el selector del elemento. No se adivina nada.

La regla `qt1vmo` exige juzgar contra la imagen, de modo que esas filas no pueden
cerrarse solo con la hoja. `../instruments/act_images.js` es la pasada que recoge
la dirección sin recortar, el `srcset`, el fondo CSS y las dimensiones
renderizadas; produjo `../image_evidence/` para la primera codificación y es la vía
también para estas filas.

## Advertencia sobre reproducibilidad

Rige la misma advertencia que en la primera codificación. Ejecuciones repetidas
del mismo sitio el mismo día difieren en uno a cuatro elementos aplicables en
páginas con carruseles o contenido rotatorio, y los recuentos de elementos *no
aplicables* son volátiles y dependen de la tecnología del sitio; no deben
compararse entre sitios.
