# Criterios de decisión — filas marcadas REVISAR

*English version: [EVALUATOR_DECISION_CRITERIA.md](EVALUATOR_DECISION_CRITERIA.md)*

Segundo documento del segundo evaluador, para la **segunda fase** del trabajo. La
primera, la recogida con el script en los quince sitios, ya está hecha. Lo que
queda es resolver las filas que la regla remite al juicio humano, y se resuelven
en dos hojas de texto plano, `hoja_r04_111.txt` y `hoja_r04_244.txt`, no en los
CSV. Lea este documento **antes** de escribir nada en las hojas.

El script ya ha decidido todo lo que la regla define de forma mecánica. Lo que
queda son las filas marcadas `REVISAR`, donde la regla ACT remite explícitamente
al juicio de una persona. Este documento fija cómo tomar ese juicio.

Todos los ejemplos de este documento están tomados de la documentación oficial de
las reglas ACT del W3C. **Ninguno procede de los quince sitios que usted evalúa**,
para no condicionar su criterio.

---

## Regla única de decisión

Cada fila es un bloque de la hoja. En cada bloque, escriba después de
`RESULTADO:` una de estas palabras:

| | |
|---|---|
| `cumple` | El elemento satisface la expectativa de la regla |
| `falla` | No la satisface |
| `no-visible` | No se puede juzgar: el elemento ya no está en la página, o la imagen no se puede ver |

**No existe categoría intermedia.** No escriba «parcial», «dudoso», ni deje el
campo vacío. Si duda entre `cumple` y `falla`, elija y explique su duda.

`no-visible` no es una tercera categoría de juicio: es la constancia de que no
hubo nada que juzgar. Esas filas quedan registradas como no decidibles y no entran
en ninguna comparación. Úselo solo cuando de verdad no haya nada que mirar, nunca
para evitar una decisión difícil.

Escriba siempre una frase después de `JUSTIFICACION:`. Esa frase es lo que
permitirá reconciliar las discrepancias después, y en el caso de `no-visible` debe
decir qué fue lo que no pudo ver. La herramienta que devuelve las hojas al CSV
rechaza la hoja completa, sin escribir nada, si algún bloque queda vacío, lleva
una palabra que no sea una de las tres, o no lleva justificación.

---

## Regla `qt1vmo` — el nombre de una imagen es descriptivo

**Expectativa oficial:** el nombre accesible del elemento sirve un propósito
equivalente al contenido no textual.

**La pregunta que debe hacerse:** si alguien no pudiera ver esta imagen y solo
oyera este texto, ¿recibiría lo que la imagen comunica?

No se pregunta si el texto está bien escrito, ni si es largo o corto, ni si a
usted le gusta. Se pregunta si **sirve el mismo propósito**.

### Ejemplos oficiales del W3C

**Cumple.** Una imagen del logotipo del W3C con `alt="W3C logo"`. El texto
identifica lo que la imagen muestra.

**Falla.** La misma imagen del logotipo del W3C con `alt="ERCIM logo"`. El texto
describe incorrectamente la imagen: nombra otra organización.

**Falla.** Un `svg` que muestra el logotipo de HTML5 con `aria-label="W3C"`. El
nombre no corresponde a lo que se representa.

### Qué hacer en la práctica

1. Abra la dirección de la línea `imagen` del bloque, o localice el elemento en la
   página con la línea `selector`.
2. Mire la imagen.
3. Lea el nombre accesible, que es la línea `nombre`.
4. Decida si el segundo sirve el propósito del primero.

Treinta y ocho de los 203 bloques de 1.1.1 no traen una dirección utilizable:
son fondos CSS, `svg` en línea o imágenes que la pasada no llegó a ver. En esos,
localice el elemento por su selector.

Si aun así la imagen no se puede ver, escriba `no-visible` y diga en la
justificación qué buscó y qué encontró. No escriba `falla` por no haber podido
mirar: eso no es un juicio, y una fila registrada como no decidible es preferible
a una resuelta a ciegas.

### Casos que encontrará y cómo tratarlos

**Imágenes que contienen texto.** Si la imagen es un cartel, un logotipo con
palabras, una tabla o un gráfico con rótulos, el nombre accesible debe transmitir
ese texto. Pregúntese si toda la información que aporta la imagen llega por el
nombre.

**Fotografías ilustrativas.** Decida si el nombre transmite lo que la fotografía
comunica en su contexto.

**Iconos y elementos gráficos pequeños.** Los que el autor ha marcado como
decorativos ya los resolvió el script y no llegan a usted.

---

## Regla `5effbb` — el enlace es descriptivo en su contexto

**Expectativa oficial:** el nombre accesible del enlace, junto con su *contexto de
enlace determinado programáticamente*, describe el propósito del enlace.

### Qué es el contexto determinado programáticamente

Esto es lo más importante del documento, porque es donde más fácil resulta
equivocarse.

El contexto es una **lista cerrada** definida por WCAG. Solo cuenta el texto que
está en:

- el **párrafo** que contiene el enlace
- el **elemento de lista** que lo contiene
- la **celda de tabla** que lo contiene, junto con su encabezado

**No es contexto** un titular que esté fuera de esos elementos, ni un `div` o un
`article` que envuelva la sección, ni el texto que se ve cerca en pantalla, ni lo
que usted deduzca del diseño de la página.

El script ya ha extraído el contexto válido y lo ha puesto en la línea `contexto`
del bloque. Cuando esa línea dice `SIN CONTEXTO PROGRAMATICO`, significa que **no
hay ninguno**: debe juzgar el nombre accesible por sí solo.

La hoja de 2.4.4 no le da la dirección de la página, y es a propósito: la regla no
le permite considerar lo que se ve alrededor del enlace. Lo que la regla admite es
el nombre, el contexto de esa lista cerrada y el destino, y las tres cosas están
en el bloque.

### Ejemplos oficiales del W3C

**Cumple.** `<a href="#desc">See the description of this product.</a>` El nombre
describe por sí solo el propósito.

**Cumple.** `<p>See the description of <a href="#desc">this product</a>.</p>` El
nombre es «this product», que por sí solo no bastaría, pero el párrafo que lo
contiene sí es contexto válido y completa la descripción.

**Falla.** `<a href="#desc">More</a>` sin párrafo que lo contenga. El nombre no
describe el propósito y no hay contexto que lo complete.

**Falla.** Un enlace cuyo texto solo se entiende por información que está en
**otro** elemento `p` distinto del que contiene el enlace. Ese texto no es
contexto determinado programáticamente aunque se lea justo al lado.

### Qué hacer en la práctica

Lea las líneas `nombre` y `contexto` del bloque. Pregúntese: **¿podría alguien
que solo oye esto saber adónde lleva el enlace?**

Un usuario de lector de pantalla puede navegar saltando de enlace en enlace, sin
oír el resto de la página. Esa es la situación que la regla contempla.

---

## Regla `fd3a94` — nombres idénticos, propósito equivalente

**Expectativa oficial:** enlaces con el mismo nombre accesible y el mismo contexto
sirven un propósito equivalente.

El script solo genera estas filas cuando ha encontrado **dos o más enlaces con
nombre y contexto idénticos que apuntan a destinos distintos**. Hay tres bloques
así. Cada uno le da el nombre compartido, el contexto, la dirección de la página y
el destino de cada uno de los enlaces del grupo.

Aquí sí tiene la dirección de la página, porque la pregunta es sobre los destinos
y **los destinos vienen recortados a 60 caracteres** por el recolector. En el
bloque de Cornell los dos destinos coinciden hasta el corte: son la misma
dirección con parámetros de seguimiento distintos, y la única forma de verlo es
abrir la página y mirar los dos enlaces.

**La pregunta:** ¿esos destinos distintos sirven el mismo propósito?

Destinos distintos no implican propósitos distintos. Dos enlaces «Descargar» que
lleven a dos copias del mismo documento sirven el mismo propósito. Dos enlaces con
el mismo nombre que lleven a contenidos sin relación entre sí, no.

---

## Cuánto tiene que revisar

Las dos hojas traen **318 bloques**: 203 del criterio 1.1.1 y 115 del 2.4.4. No
son todas las filas que su recogida dejó marcadas `REVISAR`, que son 1 351, sino
solo las que todavía deciden el veredicto de un sitio. Las otras 1 033 pertenecen
a criterios que ya fallan en su sitio por otro elemento, así que resolverlas no
cambiaría ningún resultado y no se le piden.

**Resuelva los 318.** La herramienta no acepta hojas a medias: rechaza la hoja
completa si queda un solo bloque sin responder. Si el volumen resulta inabordable,
dígalo antes de empezar y se parte el trabajo por sitios.

---

## Lo que no debe hacer

**No consulte codificaciones anteriores** de estos sitios, ni suyas ni de nadie.

**No use herramientas automáticas de accesibilidad** para decidir estas filas. Las
comprobaciones automáticas ya están hechas; lo que se le pide es exactamente lo que
ninguna herramienta puede hacer.

**No pregunte cuál es el resultado esperado.** No hay resultado esperado.

**No modifique las líneas de datos ni las cabeceras** `=== NNN | ... ===` de las
hojas. Escriba solo después de `RESULTADO:` y de `JUSTIFICACION:`.

**No abra las hojas con Excel ni con ninguna hoja de cálculo.** Son texto plano a
propósito, porque las justificaciones llevan comas, comillas y punto y coma, y una
hoja de cálculo las destroza. Use el Bloc de notas, Notepad++ o VS Code, y guarde
en UTF-8.

---

## Qué entregar

Las dos hojas, `hoja_r04_111.txt` y `hoja_r04_244.txt`, rellenas y sin renombrar,
más su nota de incidencias. Nada más: los CSV no se tocan, de eso se encarga la
herramienta al recibir las hojas.

Si en algún momento le pareció que la regla no cubría bien un caso, dígalo en la
nota. Ese tipo de observación es tan útil como la codificación misma.
