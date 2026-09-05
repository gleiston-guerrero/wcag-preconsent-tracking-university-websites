# Datos y código del estudio de dos barreras de acceso equitativo en sitios web universitarios

Depósito que acompaña al manuscrito *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, sometido a *Universal Access in the Information Society*.

El estudio cubre 126 instituciones: el censo completo de 63 universidades ecuatorianas y 63 instituciones de referencia obtenidas por consenso de tres rankings internacionales (QS, THE, ARWU). Cada portada se midió en una sola pasada automatizada que registró, antes de cualquier interacción con el banner de consentimiento, las cookies depositadas y las violaciones detectadas por axe-core.

El depósito reúne tres componentes: la auditoría automatizada de accesibilidad, la medición de cookies previas al consentimiento con su verificación documental, y la validación humana de tres criterios WCAG sobre una submuestra de quince sitios.

> **Campos por completar antes del depósito**
> DOI, licencia, autoría y filiación, financiación y cita recomendada están marcados abajo con `[PENDIENTE]`. Ninguno se ha rellenado por defecto.

---

## Contenido

```
README.md
CODEBOOK.md
CHECKSUMS.txt
datos/
  resultados.json                        126 registros  salida cruda de la auditoría
  resultados.csv                         126 filas      misma salida, aplanada
  estudio_126_sitios.csv                 126 filas      tabla analítica por sitio
  estudio_reglas_por_sitio.csv           441 filas      una fila por regla incumplida
  cookies_126_sitios_v3.csv              126 filas      cookies y verificación documental
  cookies_nombres_sin_clasificar.csv     215 filas      nombres no atribuidos a ningún proveedor
  cookies_divergencias_v2.csv             14 filas      nombres de una fuente descartada
  qa_irregularidades.csv                 228 filas      control de calidad de la tabla anterior
  cambios_reconciliacion.csv              68 filas      traza de correcciones descartadas
  universidades.json                     126 registros  lista de sitios auditados
  claude_seleccion63-mundo.json           63 registros  construcción del grupo de referencia
scripts/
  claude_auditar.js                      auditoría de un punto de observación
  claude_auditar_multipunto.js           auditoría desde cinco puntos de observación
  claude_analizar_multipunto.py          consolidación y contrastes pareados
  claude_stats_uais.py                   estadísticos del manuscrito
  claude_figuras_uais.py                 figuras 1 y 2
  estudio.py                             genera las dos tablas analíticas
  reconstruir_cookies.py                 genera la tabla de cookies desde el crudo
  anadir_id_auditoria.py                 enlaza las dos numeraciones de sitios
  reconciliar.py                         proceso descartado, se conserva por trazabilidad
  qa_cookies.py                          detecta irregularidades
  kappa_wcag.py                          kappa de Cohen de la validación manual
validacion_wcag/
  wcag_validacion_15_sitios.csv           45 filas      primera evaluación
  wcag_doble_evaluacion_5_sitios.csv      15 filas      segunda evaluación
  wcag_pares_kappa.csv                    15 filas      pares primera/segunda
  wcag_validacion_anonimizado.xlsx        las tres tablas más una hoja LEEME
```

Las fuentes canónicas son `datos/resultados.json` para la auditoría y los CSV para todo lo demás. El libro de Excel es una comodidad de lectura y contiene los mismos valores que los tres CSV de validación.

---

## Componente 1 — Auditoría automatizada

Cada portada se visitó una sola vez con un navegador sin sesión previa. Se registraron las cookies presentes antes de cualquier clic, las violaciones de axe-core 4.13.0 con su regla, impacto, criterio de éxito y número de nodos afectados, y varios indicadores de la propia página: idioma declarado, metaetiqueta viewport, enlace de salto al contenido y uso de HTTPS.

`resultados.json` conserva la salida completa con las estructuras anidadas `cookies` y `accesibilidad`. `resultados.csv` es su versión aplanada. `estudio_126_sitios.csv` y `estudio_reglas_por_sitio.csv` son las tablas analíticas derivadas: la primera resume cada sitio, la segunda desglosa una fila por cada regla incumplida.

El campo `max_nivel_sin_fallo` resume el resultado por sitio: el nivel más alto de WCAG en el que no se detectó ningún fallo automático, o `ninguno` si hubo fallos ya en nivel A. Conviene leerlo con la limitación 3 de la lista final.

## Componente 2 — Cookies previas al consentimiento

`cookies_126_sitios_v3.csv` combina la medición de `resultados.json` con una verificación documental de cada sitio: presencia de banner, plataforma de gestión de consentimiento detectada, y política de cookies publicada. La columna `rastreo` clasifica si alguna de las cookies depositadas antes del consentimiento pertenece a un proveedor de seguimiento.

Toda columna de medición se deriva de `resultados.json` mediante `reconstruir_cookies.py`, que aplica dos taxonomías. La base es la transcripción literal de las expresiones regulares codificadas en `claude_auditar.js`; el script verifica que reproduce el campo `rastreo_pre` del archivo crudo en los 126 sitios, sin un solo desajuste. La extendida añade proveedores identificados en la revisión posterior y se aplica de forma sistemática a todos los sitios, no caso por caso. El libro de códigos lista ambas.

La taxonomía extendida cambia la clasificación de un solo sitio, UPEC, cuyas cookies `sbjs_*` de Sourcebuster la taxonomía base no reconocía. Los recuentos de sitios con rastreo previo al consentimiento son 43 de 63 en el grupo de referencia y 41 de 63 en el ecuatoriano.

`cookies_nombres_sin_clasificar.csv` lista los nombres de cookie que ninguna taxonomía atribuye a un proveedor de seguimiento, con el número de sitios en que aparecen. Se publica para que la clasificación sea auditable: quien discrepe de una atribución puede verla y rehacer el recuento.

**Una tabla anterior fue descartada.** Una versión previa de este archivo tomó la medición de dos fuentes intermedias que habían perdido la lista de nombres de cookies en 52 sitios, lo que produjo 27 falsos negativos en la columna de rastreo, concentrados en el grupo de referencia. Esa tabla no forma parte del depósito. `cookies_divergencias_v2.csv` documenta los 14 sitios en que aquella fuente listaba nombres de cookie que el archivo crudo no registra; se publica para dejar constancia del motivo del descarte.

`qa_irregularidades.csv` y `cambios_reconciliacion.csv` documentan controles y correcciones aplicados a la tabla descartada. Se conservan por trazabilidad del proceso y no deben usarse como fuente de ningún indicador. Lo mismo vale para `reconciliar.py` y `qa_cookies.py`.

## Componente 3 — Validación manual WCAG

Quince sitios, tres criterios de éxito: 1.1.1 contenido no textual, 1.4.3 contraste mínimo (nivel AA) y 2.4.4 propósito del enlace en su contexto. Cada persona evaluadora inspeccionó los elementos candidatos de un sitio con las herramientas de desarrollador del navegador a 1280 × 720 px, registró el número de elementos inspeccionados (`n`) y el número que falla el criterio (`f`), y asignó un código.

| Código | Condición |
|---|---|
| `1` | cumple, `f = 0` |
| `P` | parcial, `f/n ≤ 0,20` |
| `0` | no cumple, `f/n > 0,20` |

Cinco de los quince sitios (ids 7, 14, 83, 95, 96) se designaron como sitios de control y recibieron una segunda evaluación independiente para estimar la fiabilidad entre evaluadores.

Trabajo de campo: del 17 al 28 de agosto de 2026.

**Dos numeraciones de sitio.** Las tres tablas de esta carpeta numeran los 126 sitios con el grupo de referencia primero y el ecuatoriano después; el resto del depósito y `resultados.json` lo hacen al revés. La columna `id` conserva la numeración original de la validación, porque es la que aparece en las entregas de las personas evaluadoras. La columna `id_auditoria`, añadida por `anadir_id_auditoria.py`, da el identificador equivalente en el resto del depósito. **Para unir estas tablas con las de las partes 1 y 2 debe usarse `id_auditoria`, nunca `id`.** La correspondencia se estableció por URL de portada y se verificó contra la sigla en los quince sitios.

### Fiabilidad entre evaluadores

| Escenario | Pares | Coincidencias | po | pe | κ | κ ponderada |
|---|---|---|---|---|---|---|
| Se excluye el par con evidencia contradictoria (adoptado) | 14 | 10 | 0,7143 | 0,4082 | **0,5172** | 0,4948 |
| Los quince pares tal como se entregaron | 15 | 10 | 0,6667 | 0,3867 | 0,4565 | 0,4595 |

Ambos valores quedan por debajo del umbral de 0,60 fijado para el manuscrito. La doble codificación se declara pendiente, no resuelta.

El par excluido es IAEN (id 96), criterio 2.4.4: la captura de la segunda evaluación muestra un enlace cuyo único texto es «Clic aquí», lo que prueba `f ≥ 1` y descarta el código `1` que declaró. Como no aportó un recuento propio de ese criterio, no puede separarse `P` de `0`, y el par se retira en lugar de reasignarse.

---

## Reproducción

Requisitos: Node.js con Playwright y axe-core 4.13.0 para los scripts de auditoría; Python 3 para los de análisis. `kappa_wcag.py` solo requiere la biblioteca estándar.

La auditoría parte de `datos/universidades.json`, cuya mitad de referencia se construyó con el procedimiento documentado en `datos/claude_seleccion63-mundo.json`.

```bash
node scripts/claude_auditar.js                       # produce resultados.json y resultados.csv
python scripts/estudio.py                            # produce las dos tablas analíticas
python scripts/reconstruir_cookies.py datos datos    # produce cookies_126_sitios_v3.csv
python scripts/anadir_id_auditoria.py datos validacion_wcag
python scripts/claude_stats_uais.py                  # estadísticos del manuscrito
python scripts/claude_figuras_uais.py                # figuras 1 y 2
python scripts/kappa_wcag.py validacion_wcag/wcag_pares_kappa.csv
```

`claude_auditar_multipunto.js` y `claude_analizar_multipunto.py` corresponden a la campaña desde cinco puntos de observación (Ecuador, Alemania, Reino Unido, Estados Unidos y Suiza). **Los resultados por punto de observación no forman parte de este depósito**; se incluyen los scripts para documentar el procedimiento. `[PENDIENTE: decidir si se depositan los archivos resultados_XX_rN.json y meta_XX_rN.json]`

Las rutas de entrada y salida están escritas en cada script y pueden requerir ajuste según dónde se sitúe el directorio de trabajo.

---

## Anonimización

Las personas evaluadoras aparecen como `E01`–`E10` (primera evaluación) y `D01` (segunda). Los códigos se asignaron por orden de recepción de las entregas y no codifican ningún atributo de las personas.

Se han suprimido del depósito:

- nombres y apellidos, en las columnas y también dentro de los campos de texto libre;
- nombres de archivo de las entregas, que contenían apellidos;
- horas de reloj de inicio y fin, sustituidas por `duracion_min`, que conserva el valor metodológico sin identificar sesiones;
- marcas horarias de las capturas de pantalla;
- el identificador de un formulario de Google enlazado desde uno de los sitios, sustituido por `[ID]`.

**No se depositan las capturas de pantalla originales.** Contienen barras de tareas, avatares de perfil de navegador, pestañas abiertas, relojes de sistema y widgets de clima con localidad; son identificadoras. Se conservan bajo custodia del equipo investigador y pueden facilitarse, recortadas al panel de herramientas de desarrollador, a petición razonada.

La correspondencia entre código y persona se conserva **fuera** de este depósito.

**Riesgo residual.** Dentro del grupo evaluador, la combinación de sitio asignado y fecha podría permitir la reidentificación. Quien reutilice estos datos no debe intentarla.

Los componentes 1 y 2 no contienen datos personales: miden sitios web institucionales, no personas.

---

## Limitaciones que deben citarse junto con los datos

1. Cada persona evaluadora construyó su propia muestra de elementos. Los valores de `n` no son comparables entre filas del mismo sitio, y esta es la causa principal de la dispersión que se observa en `f`.
2. La segunda evaluación declaró un único par `n`/`f` por sitio en lugar de uno por criterio. Ocho de sus quince códigos son coherentes con ese recuento; siete no tienen recuento propio contra el que verificarse.
3. Las herramientas automatizadas detectan una fracción de los problemas de accesibilidad. Un sitio sin violaciones de axe-core no es un sitio conforme; `max_nivel_sin_fallo` describe la ausencia de fallos detectados automáticamente, no la conformidad.
4. Ninguna de las cinco capturas de 1.4.3 de la segunda evaluación contiene una relación de contraste calculada. Ese criterio queda sin verificación gráfica en la segunda ronda.
5. Dos sitios, HKUST (id 58) y ECOTEC (id 124), figuran como `NO ADMISIBLE`: el `n`/`f` entregado no sostiene los códigos declarados. Se conservan por transparencia y no deben entrar en ningún análisis.
6. Siete sitios figuran como `ADMITIDA CON RESERVA`. El motivo concreto de cada uno está en la columna `dictamen_tecnico`.
7. La validación manual cubre tres criterios de éxito, no la norma completa. No es una declaración de conformidad de ninguno de los sitios.
8. La clasificación de rastreo es conservadora. Atribuye una cookie a un proveedor de seguimiento solo cuando su nombre coincide con un patrón de las dos taxonomías publicadas; los nombres no atribuidos se listan en `cookies_nombres_sin_clasificar.csv`. Los recuentos deben leerse como cota inferior.
9. La medición de cookies corresponde a una sola visita a la portada, sin navegación interna y sin interacción con el banner. No describe el comportamiento del sitio tras aceptar o rechazar.
10. Los sitios cambian. Los datos describen el estado de cada portada en la fecha registrada en el campo `fecha`.

---

## Integridad

`CHECKSUMS.txt` contiene el resumen SHA-256 de cada archivo del depósito, con rutas relativas a la raíz. Para verificar en Linux o macOS:

```bash
sha256sum -c CHECKSUMS.txt
```

En Windows, con PowerShell:

```powershell
Get-ChildItem . -Recurse -File -Exclude CHECKSUMS.txt | Get-FileHash -Algorithm SHA256 |
  % { "{0}  {1}" -f $_.Hash.ToLower(), $_.Path.Replace("$PWD\","").Replace("\","/") }
```

---

## Cita recomendada

`[PENDIENTE: autoría, año, título del conjunto de datos, repositorio, DOI]`

## Licencia

`[PENDIENTE]`

## Autoría y contacto

`[PENDIENTE: nombre, filiación, ORCID, correo de contacto]`

## Financiación

`[PENDIENTE]`

## Consideraciones éticas

La participación en la validación manual fue parte de una actividad formativa. Los datos publicados son seudonimizados y no contienen categorías especiales de datos personales. `[PENDIENTE: referencia del dictamen o exención del comité de ética, si procede]`
