# Codificación independiente de la ronda ACT por un segundo evaluador

*English version: [README.md](README.md)*

Quince archivos, uno por sitio, 7 135 filas. Las mismas quince portadas, los
mismos tres criterios de conformidad y las mismas siete reglas ACT que
`../recoding/`, codificados de forma independiente por un segundo evaluador el 9
de septiembre de 2026 con `../instruments/act_recode_evaluator2.js`.

No es una tercera ronda ni una repetición de la medición. Es la segunda de dos
codificaciones independientes de una misma ronda, y es lo que permite estimar el
acuerdo entre codificadores del instrumento ACT. El evaluador trabajó a partir de
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

## Qué establece hasta ahora

En **1.4.3**, donde la regla no deja nada al juicio, la segunda codificación
reproduce la primera exactamente: cuatro de los siete sitios del grupo de
referencia y los ocho ecuatorianos no satisfacen el criterio.

En **1.1.1** y **2.4.4** las filas que las reglas remiten al juicio humano siguen
marcadas `REVISAR`, de modo que los veredictos de sitio son provisionales. Esas
filas solo pueden añadir fallos, nunca quitarlos, así que los veredictos
registrados aquí son cotas inferiores.

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
