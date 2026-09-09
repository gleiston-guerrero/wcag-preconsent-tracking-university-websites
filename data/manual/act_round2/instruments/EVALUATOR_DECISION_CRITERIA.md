# Criterios de decisión — filas marcadas REVISAR

Segundo documento del segundo evaluador. Léalo **después** de haber ejecutado el
script en los quince sitios y **antes** de rellenar ninguna casilla.

El script ya ha decidido todo lo que la regla define de forma mecánica. Lo que
queda son las filas marcadas `REVISAR`, donde la regla ACT remite explícitamente
al juicio de una persona. Este documento fija cómo tomar ese juicio.

Todos los ejemplos de este documento están tomados de la documentación oficial de
las reglas ACT del W3C. **Ninguno procede de los quince sitios que usted evalúa**,
para no condicionar su criterio.

---

## Regla única de decisión

En cada fila `REVISAR`, escriba en la columna `resultado` una de dos palabras:

| | |
|---|---|
| `cumple` | El elemento satisface la expectativa de la regla |
| `falla` | No la satisface |

**No existe categoría intermedia.** No escriba «parcial», «dudoso», ni deje la
casilla vacía. Si duda, elija y explique su duda en `justificacion`.

Rellene siempre la columna `justificacion` con una frase. Esa frase es lo que
permitirá reconcile las discrepancias después.

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

1. Abra la dirección de la columna `src` o localice el elemento con el `selector`.
2. Mire la imagen.
3. Lea el nombre accesible.
4. Decida si el segundo sirve el propósito del primero.

Si la imagen no carga o no puede localizarla, escriba `falla` solo si está seguro;
si no puede verla, deje la fila sin rellenar y **anótelo en su nota de incidencias**.
Una fila sin resolver es preferible a una resuelta a ciegas.

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

El script ya ha extraído el contexto válido y lo ha puesto en la columna
`contexto_programatico`. Cuando esa columna dice `SIN CONTEXTO PROGRAMATICO`,
significa que **no hay ninguno**: debe juzgar el nombre accesible por sí solo.

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

Lea el nombre accesible y el contexto de la columna. Pregúntese: **¿podría alguien
que solo oye esto saber adónde lleva el enlace?**

Un usuario de lector de pantalla puede navegar saltando de enlace en enlace, sin
oír el resto de la página. Esa es la situación que la regla contempla.

---

## Regla `fd3a94` — nombres idénticos, propósito equivalente

**Expectativa oficial:** enlaces con el mismo nombre accesible y el mismo contexto
sirven un propósito equivalente.

El script solo genera estas filas cuando ha encontrado **dos o más enlaces con
nombre y contexto idénticos que apuntan a destinos distintos**, y le indica cuáles
son esos destinos en la columna `observacion`.

**La pregunta:** ¿esos destinos distintos sirven el mismo propósito?

Destinos distintos no implican propósitos distintos. Dos enlaces «Descargar» que
lleven a dos copias del mismo documento sirven el mismo propósito. Dos enlaces con
el mismo nombre que lleven a contenidos sin relación entre sí, no.

---

## Cuánto tiene que revisar

Puede detenerse antes de terminar, y conviene que sepa por qué.

Un criterio **no se satisface** en un sitio en cuanto **un** elemento aplicable
falla. Si al revisar las filas de un criterio en un sitio encuentra un `falla`
claro, el veredicto de ese sitio ya está decidido y las filas restantes de ese
mismo criterio y sitio no lo cambiarán.

Sin embargo, **para esta comparación conviene que las resuelva todas**, porque el
acuerdo se mide fila a fila y no solo sitio a sitio. Si el volumen resulta
inabordable, resuelva al menos todas las filas de los criterios que no tengan
ningún `falla` previo, y avise de dónde se detuvo.

---

## Lo que no debe hacer

**No consulte codificaciones anteriores** de estos sitios, ni suyas ni de nadie.

**No use herramientas automáticas de accesibilidad** para decidir estas filas. Las
comprobaciones automáticas ya están hechas; lo que se le pide es exactamente lo que
ninguna herramienta puede hacer.

**No pregunte cuál es el resultado esperado.** No hay resultado esperado.

**No modifique ninguna otra columna** del CSV. Solo `resultado` y `justificacion`.

---

## Qué entregar

Los quince CSV con las columnas `resultado` y `justificacion` rellenas en las filas
`REVISAR`, sin renombrar los ficheros, más su nota de incidencias.

Si en algún momento le pareció que la regla no cubría bien un caso, dígalo en la
nota. Ese tipo de observación es tan útil como la codificación misma.
