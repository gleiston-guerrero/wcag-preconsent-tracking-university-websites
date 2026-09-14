# Serie ecuatoriana desde ETAPA, 14 de septiembre de 2026

*English version: [READ_ME.md](READ_ME.md)*

Tres pasadas sobre los 126 sitios del censo, desde la misma conexión residencial
ecuatoriana de ETAPA EP (AS27668, Cuenca) que usó la campaña reportada, sin red
privada virtual.

Esta serie existe por dos motivos, y responde a una pregunta distinta en cada
uno.

**Completa el control de operador.** `../tracking_telconet/` mide el censo desde
un segundo operador ecuatoriano, pero se tomó el 7 de septiembre, tres semanas
después de la campaña reportada del 15 de agosto, de modo que compararla con esa
campaña mezclaba el operador con la fecha. Comparada en cambio con esta serie,
los dos lados son de septiembre y la fecha deja de variar.

**Aísla la fecha.** Frente a la campaña de agosto, esta serie mantiene fijos el
operador, la ciudad, la máquina, el instrumento, la versión de Node y la
configuración, y varía solo el mes. Es la única comparación del depósito que lo
hace. El depósito advierte en varios sitios que los sitios cambian de un día para
otro; ésta es la cifra que hay detrás de esa advertencia.

`code/analysis/controles_ecuador.py` reporta los dos contrastes y aborta si no
coinciden con las cifras de más abajo.

**Esta serie no forma parte de la replicación de cuatro puntos y el artículo no
la analiza.** No debe mezclarse con `../tracking/` ni con
`../tracking_extended/`.

## Condiciones de medición

| | |
|---|---|
| Pasadas | 3, seguidas, el 14 de septiembre de 2026, de 21:49 a 23:25 UTC |
| Duración | 19 minutos cada una |
| Sitios | 126 intentados, **126 exitosos y 0 fallidos en las tres pasadas** |
| Controles de ubicación | 7 por pasada, 21 en total: al inicio, tras los sitios 25, 50, 75, 100 y 125, y al final. Los 21 devolvieron `AS27668 ETAPA EP`, Cuenca, con la misma dirección IPv4 de principio a fin |
| Máquina | la misma máquina de la campaña de agosto, con la misma configuración de seguridad: Microsoft Defender inactivo, McAfee instalado sin servicios de protección web o antirrastreo en ejecución |
| Instrumento | `code/collection/audit_multivantage.js`, sin modificación |
| Versiones | axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1 — el mismo Node de la campaña de agosto |
| Navegador | Chromium lanzado con perfil limpio y sin extensiones |

Registra el estado del tarro de cookies, no las peticiones de red, igual que las
campañas con las que se compara.

## Qué dan los dos contrastes

Un sitio cuenta como que rastrea si alguna cookie fijada antes de cualquier
interacción de consentimiento coincide con la taxonomía ampliada, consolidando
las tres pasadas de cada serie por mayoría: la misma construcción que usa el
artículo. La prueba es la de McNemar exacta bilateral sobre los pares
discordantes.

**Estabilidad dentro de esta serie: 126 de 126 sitios devuelven el mismo
veredicto en las tres pasadas.** La campaña de agosto da 123 de 124 y la serie de
Telconet, 122 de 126.

| Contraste | n | Rastreo | a, b, c, d | Discordantes | p |
|---|---|---|---|---|---|
| Operador: ETAPA frente a Telconet, las dos en septiembre | 126 | 86 (68,3 %) frente a 84 (66,7 %) | 83, 3, 1, 39 | 4 | 0,625 |
| Fecha: ETAPA septiembre frente a ETAPA agosto | 125 | 85 (68,0 %) frente a 85 (68,0 %) | 84, 1, 1, 39 | 2 | 1,000 |

El contraste de operador sigue variando la máquina y la ciudad junto con el
operador, porque la serie de Telconet se tomó en otra máquina. Mueve, por tanto,
tres cosas a la vez y no puede separarlas; es concluyente solo porque no aparece
diferencia. Si hubiera aparecido, este par de series no habría podido decir cuál
de las tres la causó.

El contraste de fecha es el limpio. Dos sitios de 125 cambiaron de veredicto en
un mes, ULVR y UPenn, en direcciones opuestas. Las dos proporciones son del
68,0 %, y concuerdan con el 67,8 % que el artículo reporta para Ecuador en la
sección multipunto.

Ninguno de los dos contrastes sostiene ninguna cifra del artículo. Lo que
establecen es negativo y vale tenerlo: el resultado ecuatoriano no es un
artefacto del operador de red ni un artefacto del día en que se midió.
