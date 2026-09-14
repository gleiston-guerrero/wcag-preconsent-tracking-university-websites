# Registro de cambios

Versiones del registro de Zenodo cuyo DOI de concepto es
[10.5281/zenodo.22405998](https://doi.org/10.5281/zenodo.22405998). Cada entrada dice qué
cambió y, cuando se retiró una cifra, por qué. Los archivos ya publicados no se pueden
sustituir: una corrección es una versión nueva, y la anterior sigue siendo recuperable bajo
su propio DOI de versión. Por eso las retiradas se registran aquí en lugar de sobrescribirse
en silencio.

## 2.0.0 — 10 de septiembre de 2026

El número mayor cambia porque se retira un estadístico ya reportado, no solo porque se añada
material.

### Retirado

- **El acuerdo del 62,2 % con kappa de Cohen 0,201 sobre las 45 celdas sitio-criterio que
  comparten la ronda 1 y la ronda ACT, junto con la afirmación de que los 17 desacuerdos iban
  todos en la misma dirección.** Las cifras no salen de los archivos depositados. Recalcular
  la misma comparación da 37,8 % de acuerdo con kappa 0,097 y 28 desacuerdos si se mantienen
  las tres categorías de la ronda 1, y 73,3 % con kappa 0,226 y 12 desacuerdos si la `P` se
  cuenta como no conforme. Ninguno es 62,2 %, y 17 desacuerdos no corresponde a ninguno de
  los dos recuentos. `code/analysis/kappa_rondas.py` calcula ambos, de modo que la retirada
  se puede comprobar en lugar de creerse. La dirección de los desacuerdos sobrevive en lo
  sustancial: en el esquema binario, 11 de los 12 van hacia la no conformidad, que es la
  firma de la enumeración exhaustiva encontrando fallos que el muestreo proporcional no ve.
  Lo que no sobrevive es el «todos», ni la cifra. Nada la sustituye como estimación de
  fiabilidad entre codificadores, porque la ronda todavía no permite una; lo que la ronda
  reporta ahora en su lugar es la reproducibilidad del instrumento entre dos operadores
  independientes, descrita más abajo y etiquetada por lo que mide.

### Añadido

- **Una segunda codificación independiente de toda la ronda ACT** (`R04`, 9 de septiembre de
  2026): quince archivos y 7 135 filas en
  `data/manual/act_round2/recoding_evaluator2/recoding/`, con ocho archivos y 233 filas de
  evidencia de imagen. Una primera recogida del mismo evaluador se descartó y no se deposita:
  la traducción automática del navegador había reescrito los nombres accesibles y dejó
  elementos `<font>` en entre el 23,3 y el 55,5 % de las filas de los seis sitios en inglés.
  La recogida repetida no tiene ninguno.
- **Reproducibilidad del instrumento entre las dos codificaciones.** Sobre las tres reglas
  mecánicas —`23a2a8`, `afw4f7` y `c487ae`, donde la regla decide y el operador solo ejecuta
  el script— las dos codificaciones coinciden en 3 186 de 3 189 comparaciones por elemento:
  99,9 %, kappa de Cohen 0,996 con intervalo al 95 % de [0,991, 1,000] y prevalencia idéntica
  de la categoría mayoritaria, 86,7 %. Esto es reproducibilidad entre operadores, no
  fiabilidad entre codificadores, y `code/analysis/acuerdo_act.py` reporta las dos en bloques
  separados para que no se confundan.
- **La resolución de todas las filas de juicio capaces de decidir un veredicto de sitio.**
  `qt1vmo_345_resolved.csv` tiene ahora 349 filas, 236 que cumplen y 113 que fallan, y ninguna
  celda de la matriz de quince por tres queda abierta. Se registran dos procedencias por fila
  en `evaluator_code`: 345 filas resueltas con la asistencia de un modelo generativo y
  revisadas por el primer autor (`R03`), y cuatro resueltas por el primer autor solo (`R01`).
  Las filas asistidas quedan excluidas de toda estimación de acuerdo.
- **Los instrumentos de la ronda**, en `data/manual/act_round2/instruments/`: los dos
  recolectores, el recolector preparado para un segundo evaluador, el protocolo de recogida,
  los criterios de decisión de las filas de juicio y la herramienta de fusión.
- **Cinco scripts de análisis** en `code/analysis/`: `comprobar_brecha.py`, `acuerdo_act.py`,
  `inventario_revisar.py`, `cerrar_revisar.py` y `reparar_duplicados.py`.
- **`kappa_rondas.py`**, que reproduce todas las cifras de acuerdo de `data/manual/README.md`
  a partir de los archivos depositados y se detiene con error si alguna no sale. Antes de
  esta versión esas cifras se reportaban sin ningún script que las produjera.
- **Este registro de cambios**, en inglés y en español, y un `.zenodo.json` que fija los
  metadatos del registro en el repositorio y no solo en el formulario del depósito.

### Corregido

- Los dos límites superiores del intervalo de la comparación de la ronda 1 con la ronda 2 en
  `data/manual/README.md`, de [0,18, 0,60] y [0,35, 0,81] a [0,18, 0,61] y [0,35, 0,83]. Los
  límites inferiores estaban bien; los superiores no correspondían al error estándar sobre el
  que se construye el intervalo. Las estimaciones puntuales, 0,399 y 0,590, y los acuerdos
  observados, 60,0 y 80,0 %, no cambian y ahora son reproducibles.
- Esa misma comparación queda etiquetada por lo que mide —el efecto del cambio de instrumento
  entre las dos rondas— y se nombra la fuente de cada lado, hasta la columna. Dos archivos de
  `data/manual/` daban codificaciones distintas de la ronda 1 y solo uno de ellos produce las
  cifras reportadas.
- Nueve filas duplicadas en `qt1vmo_345_resolved.csv`, escritas por una fusión que comprobaba
  si un criterio ya fallaba en un sitio pero no si el elemento concreto tenía ya veredicto.
  Las nueve coincidían en resultado; se conservaron las filas depositadas y el recuento pasó
  de 358 a 349.
- `act_agreement_disagreements.csv` no era reproducible byte a byte: el emparejamiento recorre
  conjuntos, cuyo orden de iteración depende de la aleatorización del hash de cadenas de
  Python, de modo que los mismos datos producían las mismas filas en orden distinto en cada
  ejecución y el sha256 del manifiesto no se podía volver a obtener. Las filas van ahora
  ordenadas.
- Los cinco scripts de la ronda resolvían sus entradas contra el directorio de trabajo, dos
  esperando la raíz del repositorio y uno esperando `code/analysis/`. Todos resuelven ahora
  contra la raíz del repositorio y funcionan desde cualquiera de los dos sitios.
- Ocho fragmentos de prosa en español, en comentarios y mensajes de consola, donde un renombrado
  automático había sustituido una palabra española por su forma inglesa.

### Documentado

- Que 201 de las 282 filas de `review_282_rows.csv` se dejan sin resultado a propósito: cuando
  la resolución llegó a ellas, el criterio 1.1.1 ya estaba establecido como fallido en todos
  los sitios a los que pertenecen, así que ningún veredicto sobre ellas puede cambiar una
  cifra reportada.
- Que la submuestra de quince sitios se seleccionó de forma intencional y que el criterio no
  se registró en su momento. Ninguna cifra de la ronda se extrapola al censo.
- Que quedan 2 350 filas de juicio marcadas `REVISAR` entre las dos codificaciones, de las
  cuales 318 —todas en la segunda— podrían decidir todavía un veredicto y están en manos del
  segundo evaluador. Hasta que vuelvan no se reporta ninguna estimación de fiabilidad entre
  codificadores para las reglas de juicio, y `acuerdo_act.py` imprime ese bloque como
  pendiente en lugar de rellenarlo.

## 1.0.0 — 5 de septiembre de 2026

La primera versión publicada, [10.5281/zenodo.22405999](https://doi.org/10.5281/zenodo.22405999),
un único archivo comprimido de 3,0 MB bajo CC BY 4.0.

Se armó cuatro días antes de que existiera este repositorio y no corresponde al inventario de
archivos que fija aquí `CHECKSUMS.txt`. `README_ES.md`, en *Historia de este repositorio*,
explica por qué el repositorio se empezó limpio: uno anterior había recibido *commits* con
archivos que identificaban a los evaluadores humanos de la validación manual. Quien compare
las dos versiones debería descargar ambos archivos comprimidos en lugar de suponer que las
rutas comunes contienen lo mismo.
