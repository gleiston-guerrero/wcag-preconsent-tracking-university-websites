# Serie ecuatoriana desde Telconet, 7 de septiembre de 2026

*English version: [READ_ME.md](READ_ME.md)*

Tres pasadas sobre los 126 sitios del censo, desde una conexión residencial
ecuatoriana de Telconet S.A (AS27947, Guayaquil / Samborondón).

Propósito: control de operador. La campaña reportada en el artículo midió el
punto ecuatoriano desde ETAPA EP (AS27668, Cuenca). Esta serie comprueba si el
resultado ecuatoriano depende del operador de red.

NO es una segunda ocasión de medida ni forma parte de la replicación de cuatro
puntos. No debe mezclarse con data/raw/tracking/ ni con
data/raw/tracking_extended/.

Instrumento: el mismo audit_multivantage.js de la campaña reportada, sin
modificación. axe-core 4.13.0, Playwright 1.62.1, Node v24.12.0; la campaña de
agosto usó Node v24.18.1.

Registra el estado del tarro de cookies, no las peticiones de red.

Condiciones de medición: **una máquina distinta de la usada en agosto**, de las
mismas características y con el mismo software de seguridad instalado —Microsoft
Defender inactivo, McAfee instalado sin servicios de protección web o
antirrastreo en ejecución—. Chromium se lanza con perfil limpio y sin
extensiones. Una versión anterior de este archivo decía «misma máquina»; era
incorrecto y queda corregido aquí. La diferencia de versión de Node que consta en
los metadatos es consecuencia de la diferencia de máquina.

La máquina varía, por tanto, junto con el operador en esta comparación, y la
comparación no puede separar las dos cosas. Lo que lo hace tolerable es el
resultado: `code/analysis/controles_ecuador.py` no encuentra diferencia, de modo
que el resultado ecuatoriano sobrevive a dos cambios a la vez en lugar de a uno.
Si hubiera aparecido una diferencia, esta serie por sí sola no habría podido
decir si la causó el operador o la máquina.

Desde el 14 de septiembre de 2026 existe una tercera serie ecuatoriana,
`../tracking_etapa_september/`, tres pasadas desde ETAPA una semana después de
estas. Esa sí mantiene fijas la máquina, la ciudad y la versión de Node frente a
la campaña de agosto, de modo que las dos series responden a preguntas distintas
y el mismo script reporta las dos.
