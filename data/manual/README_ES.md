# Validación manual de tres criterios de conformidad WCAG

*English version: [README.md](README.md)*

Verificación manual de la auditoría automatizada para tres criterios de conformidad sobre
una submuestra de 15 sitios: siete del grupo de referencia y ocho del censo ecuatoriano.
Los criterios son **1.1.1** contenido no textual, **1.4.3** contraste (mínimo) y **2.4.4**
propósito del enlace (en contexto), todos de WCAG 2.2, publicada además como
ISO/IEC 40500:2025.

La carpeta contiene **dos rondas de codificación por evaluadores distintos**, más el
instrumento preparado para una tercera. No deben fusionarse: cada ronda usó un esquema de
codificación diferente, y la diferencia entre ellas es en sí misma un hallazgo.

Los nombres de columna de todos los CSV de esta carpeta están en inglés. Los **valores**
codificados siguen en español (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `1`/`P`/`0`,
`REVISAR`), que es el vocabulario que define el CODEBOOK.

---

## Rondas de codificación

### Ronda 1 — 27 de agosto de 2026, evaluadores `E01` a `E10`

`wcag_validation_15_sites.csv` — 45 filas, una por sitio y criterio. Cada fila registra el
código, el tamaño de muestra `n`, el número de fallos `f`, el código del evaluador, la
fecha, la duración en minutos, el número de capturas y un dictamen técnico.

`manual_coding_15_universities.csv` — 15 filas, una por sitio, con los tres códigos en
paralelo y una cota sobre cada uno. **Todas las filas declaran `un solo codificador`**, en
las tres columnas de estado. Es el registro de la primera pasada y no aporta evidencia
entre codificadores; se publica por completitud.

### Ronda 2 — 1–2 de septiembre de 2026, evaluador `R01`

`recoding_111.csv`, `recoding_143.csv`, `recoding_244.csv` — 15 filas cada uno, una por
sitio. La sesión transcurrió desde la mañana del 1 de septiembre hasta la madrugada del 2;
`extraction_utc` lleva la marca UTC de cada lectura y `date` el día al que pertenece. Mejor
documentada que la ronda 1: añaden la marca UTC de extracción, el total de elementos
detectados frente a la muestra examinada, la lista de elementos que fallan y una nota
sustantiva por celda. Varias de esas notas registran las decisiones que resultaron ser el
motor del desacuerdo, como la exclusión del texto oculto visualmente en la medición de
contraste, o la falta de fiabilidad de un recorrido del DOM para establecer el contexto de
un enlace.

### Segunda codificación parcial — 25 de agosto de 2026, evaluador `D01`

`wcag_double_evaluation_5_sites.csv` — 15 filas que cubren cinco sitios, con una
justificación por celda y un juicio explícito sobre si la evidencia aportada sostiene el
código tal como se entregó.

`wcag_kappa_pairs.csv` — parejas de primera y segunda codificación con una columna de
acuerdo, para esos cinco sitios.

`wcag_validation_anonymised.xlsx` — el libro de la ronda 1 sin nombres de evaluador.

---

## Qué muestra el acuerdo entre rondas

Calculado sobre las 45 celdas que comparten la ronda 1 y la ronda 2:

| Esquema de codificación | Acuerdo observado | Kappa de Cohen | IC 95 % |
|---|---|---|---|
| Tres categorías (`1` / `P` / `0`) | 60,0 % | 0,399 | [0,18, 0,60] |
| Binario (`P` contado como no conforme) | 80,0 % | 0,590 | [0,35, 0,81] |

En los cinco sitios codificados por los tres evaluadores el patrón se mantiene y ningún
codificador es el atípico: `R01` frente a la ronda 1 da 0,375 en tres categorías y 0,737 en
binario; `R01` frente a `D01` da 0,192 y 0,324; la ronda 1 frente a `D01` da 0,457 y 0,359.

De los 18 desacuerdos sobre las 45 celdas, casi todos se dan entre `P` y uno de los
extremos, y no entre conforme y no conforme. Los codificadores vieron lo mismo y
discreparon sobre dónde estaba el umbral de *parcial*. **La dicotomía es fiable; la
tricotomía no.**

`kappa_wcag.py`, en `code/analysis/`, calcula la kappa de los cinco sitios de doble
codificación de `wcag_kappa_pairs.csv`: 0,517 excluyendo la pareja con evidencia
contradictoria y 0,457 incluyéndola. Las cifras de la tabla anterior, que comparan la ronda
1 con la ronda 2 sobre las 45 celdas, no las produce ningún script depositado.

---

## El instrumento preparado en respuesta

`act_recoding_5_sites_TEMPLATE.csv` y `act_recoding_DICTIONARY.md`

Una plantilla vacía y su diccionario de datos para una tercera ronda, anclada en las reglas
de Accessibility Conformance Testing (ACT) del W3C, cuyo formato pasó a ser Recomendación
del W3C en febrero de 2026. De ese anclaje se siguen dos cambios:

- El vocabulario de resultado es *aplicable*, *cumple*, *falla*, *no aplicable*. No hay
  categoría intermedia, lo que elimina la fuente de desacuerdo identificada arriba.
- La unidad de codificación es el elemento individual y no el sitio, y lo que cuenta como
  elemento aplicable lo fija la regla, no lo decide el evaluador. La regla `afw4f7` aplica a
  cualquier carácter visible, de modo que el texto oculto visualmente queda fuera de su
  alcance por definición; y el contexto de un enlace es el *contexto de enlace determinado
  programáticamente* de WCAG, una lista cerrada, no el ascendiente al que llegue un
  recorrido del DOM.

Reglas usadas: `23a2a8`, `qt1vmo` y `e88epe` para 1.1.1; `afw4f7` para 1.4.3; `c487ae`,
`5effbb` y `fd3a94` para 2.4.4.

La plantilla **todavía no está rellenada**. Hasta que lo esté, el artículo no reporta
ningún resultado de esta ronda.

---

## captures/

Cuarenta y cinco capturas de pantalla, quince por criterio, en `1.1.1/`, `1.4.3/` y
`2.4.4/`. Nombradas por institución. Son la evidencia de las rondas 1 y 2.

---

## Códigos de evaluador

`E01`–`E10` en la primera ronda de codificación, `D01` en la segunda codificación parcial,
y `R01`, `R02` y `R03` en las rondas de recodificación y ACT. Ningún archivo de esta
carpeta identifica a un evaluador: ninguno lleva el nombre, el correo electrónico ni una
ruta local de nadie del equipo investigador. Existen versiones con nombres de evaluador,
pero no forman parte de este depósito.

Las direcciones de correo que sí aparecen, en `act_round2/image_evidence/`, se observaron
en las portadas de las propias instituciones auditadas y se reproducen tal como se
observaron. Pertenecen a esas instituciones, no al equipo investigador.
