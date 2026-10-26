# Hoja de recodificación ACT — diccionario de columnas

*English version: [act_recoding_DICTIONARY.md](act_recoding_DICTIONARY.md)*

Una fila **por elemento aplicable**, no por sitio. La plantilla trae una fila de arranque
por sitio y regla; el evaluador añade tantas filas como elementos aplicables encuentre.

| Columna | Qué se escribe |
|---|---|
| `id`, `group`, `abbr`, `url` | Identificación del sitio, ya rellenada |
| `criterion` | 1.1.1, 1.4.3 o 2.4.4 |
| `act_rule` | Identificador de seis caracteres de la regla ACT |
| `rule_name` | Nombre oficial de la regla, ya rellenado |
| `element_n` | Número correlativo del elemento dentro de la regla y el sitio |
| `selector_or_description` | Selector CSS o descripción que permita volver al elemento |
| `applicable` | `si` o `no`. **La decide la regla, no el evaluador.** Si `no`, deje `outcome` vacío y explique en `notes` cuál de las exclusiones de la regla se aplica |
| `outcome` | `cumple` o `falla`. Sin categoría intermedia |
| `measured_value` | Solo para 1.4.3: ratio de contraste con dos decimales. Vacío en los demás |
| `programmatic_context` | Solo para 2.4.4 (`5effbb`): párrafo, elemento de lista o celda con encabezado que aporta el contexto. Un elemento envolvente genérico **no** es contexto |
| `evaluator_code` | Código del evaluador. No escriba nombres |
| `date` | AAAA-MM-DD |
| `capture` | Nombre del fichero de evidencia |
| `notes` | Justificación breve. Obligatoria cuando `applicable=no` o `outcome=falla` |

> Los **nombres de columna** están en inglés, en línea con el resto del depósito. Los **valores** siguen en español (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), que es el vocabulario que define el CODEBOOK.

## Cómo se agrega al nivel de sitio

Un criterio **no se satisface** en un sitio si algún elemento aplicable de alguna de sus
reglas tiene `outcome=falla`. Si todos los elementos aplicables cumplen, se satisface.
Si no hay ningún elemento aplicable, el criterio es `no aplicable` para ese sitio.

No se calcula proporción de fallos ni se fija tamaño de muestra: se examinan todos los
elementos aplicables. Eso elimina a la vez la categoría parcial y la discusión sobre el
muestreo, que fueron las dos fuentes de desacuerdo entre los codificadores anteriores.

## Umbrales y exclusiones, por regla

**afw4f7, contraste.** Aplica a cualquier carácter *visible* de un nodo de texto. Umbral:
4,5:1, o 3,0:1 para texto de gran tamaño. Inaplicable: ascendiente deshabilitado, etiqueta
de un control deshabilitado, texto puramente decorativo, texto que no expresa nada en
lenguaje humano. El texto oculto visualmente no es un carácter visible y por tanto queda
fuera de la regla: **no se excluye por criterio del evaluador, se excluye por definición**.

**23a2a8, nombre accesible de imagen.** Aplica a `img` y a elementos con rol semántico
`img`, salvo los programáticamente ocultos. Cumple si el nombre accesible no está vacío,
o si el rol es `none` o `presentation`.

**qt1vmo, nombre descriptivo.** Aplica a `img`, `canvas` y `svg` visibles con nombre
accesible no vacío. Inaplicable si un ascendiente está nombrado por el autor, o si la
petición de la imagen no está completamente disponible. Cumple si el nombre sirve un
propósito equivalente al contenido no textual.

**e88epe, imagen decorativa.** Una imagen fuera del árbol de accesibilidad se trata como
decorativa.

**c487ae, nombre de enlace.** Aplica a todo enlace incluido en el árbol de accesibilidad.
Cumple si el nombre accesible no está vacío.

**5effbb, enlace descriptivo en contexto.** Aplica a todo enlace del árbol de accesibilidad
con nombre accesible no vacío. Cumple si el nombre, junto con su *contexto de enlace
determinado programáticamente*, describe el propósito del enlace. Ese contexto es una lista
cerrada de WCAG: párrafo, elemento de lista, celda de tabla con su encabezado. Un `div` o un
`article` que envuelve la página **no** es contexto.

**fd3a94, enlaces de nombre idéntico.** Enlaces con nombre accesible idéntico en el mismo
contexto deben servir un propósito equivalente.
