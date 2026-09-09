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

Condiciones de medición: misma máquina y misma configuración de seguridad que
en agosto. Microsoft Defender inactivo, McAfee instalado sin servicios de
protección web o antirrastreo en ejecución. Chromium se lanza con perfil limpio
y sin extensiones.
