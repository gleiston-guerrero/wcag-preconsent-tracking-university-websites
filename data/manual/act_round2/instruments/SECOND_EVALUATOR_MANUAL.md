# Manual del segundo evaluador — recodificación ACT

Estudio de accesibilidad y privacidad en sitios web universitarios. Se le pide
codificar de forma **independiente** tres criterios de accesibilidad sobre las
portadas de quince universities.

Independiente quiere decir: **no consulte codificaciones anteriores, ni results
de otros evaluadores, ni el borrador del artículo.** Su codificación se compara
con otra para medir el grado de acuerdo, y ese acuerdo solo tiene valor si las dos
se hicieron por separado.

Tiempo estimado: unas dos horas para la recogida, más el tiempo de las decisiones
de juicio, que se le explicará en un segundo documento.

---

## Qué se evalúa

Tres criterios de éxito de WCAG 2.2, que es además la norma internacional
ISO/IEC 40500:2025:

| Criterio | Nombre |
|---|---|
| **1.1.1** | Contenido no textual |
| **1.4.3** | Contraste (mínimo) |
| **2.4.4** | Propósito del enlace (en contexto) |

La codificación se ancla en las **reglas ACT** del W3C, cuyo formato es
Recomendación del W3C desde febrero de 2026. El vocabulario de resultado es
*aplicable*, *cumple*, *falla*, *no aplicable*. **No existe categoría intermedia**:
un elemento cumple o falla.

La unidad de codificación es **el elemento**, no el sitio. Un criterio no se
satisface en un sitio si algún elemento aplicable falla.

---

## Antes de empezar

1. Use **Google Chrome** o **Microsoft Edge**, en un ordenador de escritorio o
   portátil. No sirve el móvil.
2. Trabaje en una **ventana normal**, no de incógnito, y con la ventana
   maximizada. El tamaño de la ventana influye en qué elementos son visibles.
3. **No use VPN.** La medición debe hacerse desde su conexión habitual.
4. **No instale bloqueadores de anuncios ni extensiones de accesibilidad.** Si ya
   los tiene, desactívelos: alteran la página que se mide.

---

## Procedimiento, sitio por sitio

Repita estos seis pasos para cada una de las quince direcciones de la lista.

**1. Abra la dirección** en una pestaña nueva y espere a que la página cargue del
todo.

**2. Si aparece un aviso de cookies, ciérrelo.** Elija la opción que rechaza o la
que simplemente cierra. Si el aviso solo ofrece "Aceptar", acéptelo y **anótelo**.
Espere unos segundos tras cerrarlo: algunos avisos tardan en desaparecer.

Esto es importante: con el aviso encima, el texto que tapa no es visible y quedaría
fuera de la medición.

**3. Abra las herramientas de desarrollo** con la tecla **F12** y sitúese en la
pestaña **Consola**.

**4. Pegue el script** `act_recode_evaluator2.js` completo y pulse Intro.

La primera vez, Chrome bloqueará el pegado y le pedirá que escriba una frase de
confirmación. Si su Chrome está en español, escriba `permitir pegado`; si está en
inglés, `allow pasting`. Pulse Intro. Aparecerá un error de sintaxis: es normal,
el navegador registra la autorización igualmente. Vuelva a pegar el script.

**Antes de la primera ejecución**, cambie en el script la línea:

```javascript
const EVALUADOR = 'R03';   // <-- PONGA AQUI SU CODIGO DE EVALUADOR
```

Use siempre el mismo código en los quince sitios. **No escriba su nombre**: la
codificación se publica y los evaluadores se identifican por código.

**5. Espere a que termine.** Tarda entre veinte segundos y un minuto. Verá en la
consola unas líneas de resumen y se descargará un fichero CSV.

**6. Compruebe el nombre del fichero descargado.**

- Si termina en `_ok.csv`, correcto.
- Si termina en **`_MODALABIERTO.csv`**, el aviso de cookies seguía abierto.
  Ciérrelo bien y vuelva a run. Borre el fichero incorrecto.

El script deja en el portapapeles la línea de resumen, y además **acumula todas
las líneas de las ejecuciones anteriores**: al terminar el último sitio, el
portapapeles contiene las quince de golpe y basta con pegarlas una sola vez en un
documento de texto.

La acumulación vive en la pestaña de herramientas del navegador. Si cierra el
navegador a mitad, se pierde: pegue lo que lleve antes de cerrar. No es grave,
porque cada CSV lleva esos mismos datos dentro, en las columnas `estado_modal`,
`cmp_contenedores`, `cmp_elementos_excluidos` y `script_version`.

En la consola verá además una tabla con los sitios completados hasta el momento,
para que sepa en todo momento cuáles le faltan.

---

## Los quince sitios

Siete de un grupo internacional de referencia y ocho del censo ecuatoriano.
Hágalos en este orden.

```
https://www.berkeley.edu
https://www.ucl.ac.uk
https://www.cornell.edu
https://nus.edu.sg
https://www.northwestern.edu
https://www.manchester.ac.uk
https://hkust.edu.hk/
https://unesum.edu.ec
https://usecipol.edu.ec
https://www.iaen.edu.ec
https://www.ulvr.edu.ec
https://www.utpl.edu.ec
https://www.ups.edu.ec
https://www.indoamerica.edu.ec
https://ecotec.edu.ec
```

Sitios con aviso de cookies conocido, para que esté prevenido: **NUS**, que solo
ofrece "Aceptar"; **Northwestern**; **Manchester**; y **ECOTEC**.

---

## Qué hace el script y qué no

Decide por sí solo todo lo que la regla ACT define de forma mecánica: qué elemento
es aplicable, el contraste de 1.4.3 con su ratio y su umbral, si una imagen tiene
nombre accesible y si un enlace lo tiene.

Deja marcadas como **REVISAR** las filas donde la regla remite al juicio humano:
si el nombre de una imagen es descriptivo, si un enlace se entiende con su
contexto, y si enlaces de nombre idéntico sirven propósito equivalente.

**No rellene todavía esas filas.** Se le entregará un segundo documento con los
criterios de decisión y el subconjunto exacto que debe resolver.

---

## Qué entregar

Al terminar los quince sitios:

1. Los **quince ficheros CSV**, sin renombrar.
2. Las **quince líneas de resumen** `ACT|v5`, pegadas de una vez desde el
   portapapeles a un documento de texto.
3. Una **nota breve** con cualquier incidencia: sitios que no cargaron, avisos que
   solo permitían aceptar, páginas que cambiaron mientras medía, o cualquier cosa
   que le llamara la atención.

Esa nota importa. Si un sitio se comportó de forma extraña, es mejor saberlo que
descubrirlo al comparar los números.

---

## Advertencias

**No modifique los CSV descargados.** Si cree que hay un error, anótelo en la nota
de incidencias y déjelo tal cual.

**No ejecute el script dos veces sobre el mismo sitio** salvo que la primera saliera
con `_MODALABIERTO`. Si lo hace, conserve las dos y dígalo: las páginas cambian entre
ejecuciones y esa variación es en sí misma un dato.

**No consulte a nadie** que haya codificado antes estos sitios, ni pregunte por los
results esperados, hasta que haya entregado su codificación completa.
