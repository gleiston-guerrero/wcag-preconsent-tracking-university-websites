# -*- coding: utf-8 -*-
"""Deriva del lado de accesibilidad entre dos ocasiones separadas un mes.

QUE MIDE ESTO Y QUE NO MIDE. Es la primera cosa que hay que leer.

Las cifras de accesibilidad del articulo salen de la pasada unica del 14 de
agosto de 2026, data/raw/accessibility/results.json, que NO se ha repetido. Este
script no la toca y no dice nada sobre ella.

Lo que si tiene dos ocasiones es el campo `accesibilidad` que los recolectores
multipunto registran de paso en cada pasada:

    data/raw/tracking/                   15 de agosto de 2026
    data/raw/tracking_etapa_september/   14 de septiembre de 2026

Las dos series son del mismo operador (ETAPA EP, AS27668, Cuenca), la misma
maquina, el mismo instrumento y las mismas versiones. Lo unico que cambia entre
ellas es el mes. Este script acota, por tanto, cuanto se mueve LA SALIDA DEL
INSTRUMENTO EN ACCESIBILIDAD sobre las mismas 126 portadas en un mes. No es la
medicion reportada y no la sustituye.

Por que importa: el deposito advierte repetidamente que los sitios cambian de un
dia para otro, y code/analysis/controles_ecuador.py pone cifra a esa advertencia
para el rastreo. Esto hace lo mismo para el otro lado del estudio.

Tres comparaciones, de la mas robusta a la mas fragil:

  1. VEREDICTO BINARIO: si el sitio tiene algun nodo que falla de nivel A. Es la
     forma mas cercana al veredicto de rastreo y la que menos depende de
     recuentos. Se consolida por mayoria de las tres pasadas de cada serie y se
     contrasta con McNemar exacta bilateral.

  2. NIVEL MAS ALTO SIN FALLO (`maxNivelSinFallo`), categorico: A, AA, AAA o
     ninguno. Se consolida por mayoria; ningun sitio queda sin mayoria clara.

  3. RECUENTO DE NODOS QUE FALLAN. Es el mas fragil: los recuentos son
     volatiles y composicionales, y no estan normalizados por complejidad de la
     pagina, de modo que un portal grande acumula mas nodos sin ser menos
     accesible. Se da la mediana por sitio, no la media, y la distribucion del
     cambio, no solo el total.

Entradas : ../../data/raw/tracking/results_EC_r{1,2,3}.json
           ../../data/raw/tracking_etapa_september/results_EC_r{1,2,3}.json
Salida   : informe por consola. No escribe ningun archivo.

Uso, desde code/analysis/:  python deriva_accesibilidad.py
"""
import collections
import io
import json
import os
import statistics
from math import comb

PASADAS = (1, 2, 3)

SERIES = (
	("agosto", "../../data/raw/tracking"),
	("septiembre", "../../data/raw/tracking_etapa_september"),
)

# Cifras que declaran los READ_ME de las dos series. El script termina
# comprobandolas, igual que controles_ecuador.py con las suyas.
ESPERADO = {
	"n": 125,
	"a": 93, "b": 1, "c": 1, "d": 30,
	"nivel_igual": 122,
	"sin_cambio_nodos": 69,
}


def cargar(carpeta):
	"""Por sitio, una entrada por pasada valida.

	Un sitio que fallo en una pasada aporta las demas; si fallo en todas no
	entra. La campana de agosto tiene dos fallos, de modo que un sitio queda
	con una sola pasada y por eso se cuenta aparte.
	"""
	datos = {}
	for r in PASADAS:
		ruta = os.path.join(carpeta, "results_EC_r%d.json" % r)
		with io.open(ruta, encoding="utf-8") as fh:
			for fila in json.load(fh):
				if not fila.get("ok"):
					continue
				a = fila["accesibilidad"]
				datos.setdefault(fila["sigla"], []).append({
					"fallo_a": a["porNivel"].get("A", 0) > 0,
					"nodos": a["nodos"],
					"nivel": a["maxNivelSinFallo"],
				})
	return datos


def mayoria_binaria(valores):
	return sum(1 for v in valores if v) * 2 > len(valores)


def mayoria_categorica(valores):
	"""Devuelve la categoria mayoritaria, o None si no hay mayoria estricta.

	No se desempata de forma arbitraria: un sitio sin mayoria clara se informa
	y se deja fuera en lugar de asignarle una categoria inventada.
	"""
	cuenta = collections.Counter(valores)
	cat, n = cuenta.most_common(1)[0]
	return cat if n * 2 > len(valores) else None


def mcnemar_exacto(b, c):
	n = b + c
	if n == 0:
		return 1.0
	k = min(b, c)
	return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main():
	datos = {}
	print("=" * 78)
	print("DERIVA DE ACCESIBILIDAD ENTRE DOS OCASIONES, A UN MES DE DISTANCIA")
	print("=" * 78)
	print("  Mismo operador, ciudad, maquina, instrumento y versiones; solo cambia")
	print("  el mes. NO es la medicion de accesibilidad que reporta el articulo,")
	print("  que sale de la pasada unica del 14 de agosto y no se ha repetido.")
	print()
	for nombre, carpeta in SERIES:
		datos[nombre] = cargar(carpeta)
		completos = {s: v for s, v in datos[nombre].items() if len(v) == len(PASADAS)}
		parciales = len(datos[nombre]) - len(completos)
		iguales = sum(1 for v in completos.values() if len({x["fallo_a"] for x in v}) == 1)
		print("  %-11s %3d sitios con observacion (%d con menos de %d pasadas)"
			  % (nombre, len(datos[nombre]), parciales, len(PASADAS)))
		print("  %-11s veredicto de nivel A igual en las tres pasadas: %d de %d (%.1f %%)"
			  % ("", iguales, len(completos), 100.0 * iguales / len(completos)))

	ago, sep = datos["agosto"], datos["septiembre"]
	comunes = sorted(set(ago) & set(sep))

	# --- 1. veredicto binario de nivel A -------------------------------------
	A = {s: mayoria_binaria([x["fallo_a"] for x in ago[s]]) for s in comunes}
	B = {s: mayoria_binaria([x["fallo_a"] for x in sep[s]]) for s in comunes}
	a = sum(1 for s in comunes if A[s] and B[s])
	b = sum(1 for s in comunes if A[s] and not B[s])
	c = sum(1 for s in comunes if not A[s] and B[s])
	d = sum(1 for s in comunes if not A[s] and not B[s])
	p = mcnemar_exacto(b, c)
	print("\n" + "-" * 78)
	print("  1. ALGUN NODO QUE FALLA DE NIVEL A   (n=%d sitios en las dos series)"
		  % len(comunes))
	print("-" * 78)
	print("    agosto      %3d de %d  (%.1f %%)"
		  % (a + b, len(comunes), 100.0 * (a + b) / len(comunes)))
	print("    septiembre  %3d de %d  (%.1f %%)"
		  % (a + c, len(comunes), 100.0 * (a + c) / len(comunes)))
	print("    a=%d  b=%d  c=%d  d=%d" % (a, b, c, d))
	print("    pares discordantes: %d   McNemar exacta bilateral p=%.4f" % (b + c, p))
	for s in comunes:
		if A[s] != B[s]:
			print("      %-16s %s -> %s" % (s, "falla nivel A" if A[s] else "sin fallo de nivel A",
											"sin fallo de nivel A" if A[s] else "falla nivel A"))

	# --- 2. nivel mas alto sin fallo -----------------------------------------
	ca = {s: mayoria_categorica([x["nivel"] for x in ago[s]]) for s in comunes}
	cb = {s: mayoria_categorica([x["nivel"] for x in sep[s]]) for s in comunes}
	sin_mayoria = [s for s in comunes if ca[s] is None or cb[s] is None]
	decidibles = [s for s in comunes if s not in sin_mayoria]
	iguales = [s for s in decidibles if ca[s] == cb[s]]
	print("\n" + "-" * 78)
	print("  2. NIVEL MAS ALTO SIN FALLO")
	print("-" * 78)
	print("    identico entre ocasiones: %d de %d (%.1f %%)"
		  % (len(iguales), len(decidibles), 100.0 * len(iguales) / len(decidibles)))
	if sin_mayoria:
		print("    sin mayoria clara en alguna serie, excluidos: %s" % ", ".join(sin_mayoria))
	for s in decidibles:
		if ca[s] != cb[s]:
			print("      %-16s %s -> %s" % (s, ca[s], cb[s]))

	# --- 3. recuento de nodos ------------------------------------------------
	na = {s: statistics.median([x["nodos"] for x in ago[s]]) for s in comunes}
	nb = {s: statistics.median([x["nodos"] for x in sep[s]]) for s in comunes}
	dif = [nb[s] - na[s] for s in comunes]
	q1, q2, q3 = statistics.quantiles(dif, n=4)
	print("\n" + "-" * 78)
	print("  3. NODOS QUE FALLAN   (mediana por sitio sobre las tres pasadas)")
	print("-" * 78)
	print("    agosto      mediana %5.0f por sitio | total %d" % (statistics.median(na.values()), sum(na.values())))
	print("    septiembre  mediana %5.0f por sitio | total %d" % (statistics.median(nb.values()), sum(nb.values())))
	print("    variacion del total: %+.1f %%"
		  % (100.0 * (sum(nb.values()) - sum(na.values())) / sum(na.values())))
	print("    cambio por sitio: mediana %+.0f | cuartiles %+.0f / %+.0f / %+.0f"
		  % (statistics.median(dif), q1, q2, q3))
	print("    sin cambio en %d de %d sitios" % (sum(1 for x in dif if x == 0), len(dif)))
	print("    Esta tercera comparacion es la mas fragil de las tres: los recuentos")
	print("    de nodos no estan normalizados por complejidad de la pagina, de modo")
	print("    que un portal grande acumula mas nodos sin ser menos accesible. Se")
	print("    da por completitud y no sostiene ninguna afirmacion.")

	# --- comprobacion de lo declarado ---------------------------------------
	obtenido = {"n": len(comunes), "a": a, "b": b, "c": c, "d": d,
				"nivel_igual": len(iguales),
				"sin_cambio_nodos": sum(1 for x in dif if x == 0)}
	print("\n" + "=" * 78)
	if obtenido != ESPERADO:
		print("DISCREPANCIA con las cifras declaradas en los READ_ME:")
		print("  declarado: %s" % ESPERADO)
		print("  obtenido : %s" % obtenido)
		raise SystemExit("\nABORTA: las cifras no coinciden con lo declarado.")
	print("Las cifras coinciden con las declaradas en el READ_ME de la serie de")
	print("septiembre. Ninguna cifra del articulo depende de ellas: el articulo no")
	print("analiza esta serie, y su medicion de accesibilidad es la pasada unica del")
	print("14 de agosto, que no tiene segunda ocasion.")
	print("=" * 78)


if __name__ == "__main__":
	main()
