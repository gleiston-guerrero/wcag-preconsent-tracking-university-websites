# -*- coding: utf-8 -*-
"""Los dos controles del punto de observacion ecuatoriano.

La campana reportada en el articulo midio Ecuador desde una sola conexion, de
ETAPA EP en Cuenca, el 15 de agosto de 2026. Eso deja abiertas dos preguntas que
el articulo no puede responder con esa campana sola:

  1. OPERADOR. Depende el resultado ecuatoriano del operador de red?
     Serie de Telconet (AS27947, Guayaquil), 7 de septiembre, frente a la serie
     de ETAPA de septiembre. Las dos son de septiembre, de modo que la fecha
     deja de confundirse con el operador, que es lo que ocurria al comparar
     Telconet con la campana de agosto. Sigue variando la maquina: la serie de
     Telconet se tomo en otra maquina, de las mismas caracteristicas y con el
     mismo software de seguridad, asi que este contraste mueve dos cosas a la
     vez y no puede separarlas.

  2. FECHA. Cuanto se mueve el fenomeno con todo lo demas fijo?
     Serie de ETAPA de septiembre frente a la campana de agosto. Mismo
     operador, misma ciudad, misma maquina, mismo instrumento y misma version
     de Node: lo unico que cambia es el mes. El deposito advierte en varios
     sitios que los sitios cambian de un dia para otro; esta es la cifra de esa
     advertencia.

Ninguno de los dos contrastes sostiene ninguna cifra del articulo: el articulo
no analiza estas series. Se calculan y se depositan para que la advertencia y el
control dejen de ser afirmaciones sin numero.

El veredicto de rastreo se construye igual que en la campana reportada: un sitio
rastrea si alguna cookie fijada antes de cualquier interaccion de consentimiento
coincide con la taxonomia ampliada, y las tres pasadas de cada serie se
consolidan por mayoria. La taxonomia NO se redefine aqui: se lee estaticamente
de verify_multivantage.py para que exista una unica fuente de verdad.

La prueba es la de McNemar exacta, bilateral, que es la que usa la seccion
multipunto. No se aplica correccion de multiplicidad: son dos contrastes
preespecificados que responden a preguntas distintas, no una familia.

Entradas : ../../data/raw/tracking/results_EC_r{1,2,3}.json
           ../../data/raw/tracking_telconet/results_EC_r{1,2,3}.json
           ../../data/raw/tracking_etapa_september/results_EC_r{1,2,3}.json
Salida   : informe por consola. No escribe ningun archivo.

Uso, desde code/analysis/:  python controles_ecuador.py
"""
import ast
import io
import json
import os
import re
from math import comb

FUENTE_TAXONOMIA = "verify_multivantage.py"
PASADAS = (1, 2, 3)

SERIES = (
	("ETAPA agosto", "../../data/raw/tracking"),
	("ETAPA septiembre", "../../data/raw/tracking_etapa_september"),
	("Telconet septiembre", "../../data/raw/tracking_telconet"),
)

# Cifras que declaran los READ_ME de las dos series de control. El script
# termina comprobandolas, igual que verify_live_divergence.py con las suyas.
ESPERADO = {
	"operador": {"n": 126, "a": 83, "b": 3, "c": 1, "d": 39},
	"fecha": {"n": 125, "a": 84, "b": 1, "c": 1, "d": 39},
}


def taxonomia(ruta=FUENTE_TAXONOMIA):
	"""Devuelve las dos listas de patrones tal como estan escritas en el modulo
	de referencia, sin importarlo ni volver a declararlas aqui."""
	arbol = ast.parse(io.open(ruta, encoding="utf-8").read())
	listas = {}
	for nodo in arbol.body:
		if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1:
			destino = nodo.targets[0]
			if isinstance(destino, ast.Name) and destino.id in ("ORIG", "ADD"):
				listas[destino.id] = ast.literal_eval(nodo.value)
	if set(listas) != {"ORIG", "ADD"}:
		raise SystemExit("no se encontraron ORIG y ADD en %s" % ruta)
	return listas["ORIG"], listas["ADD"]


def rastrea(nombres, patrones):
	return any(p.search(n) for n in nombres for p in patrones)


def mayoria(valores):
	"""Mayoria simple sobre las pasadas validas de un sitio."""
	return sum(1 for v in valores) and sum(1 for v in valores if v) * 2 > len(valores)


def serie(carpeta, patrones):
	"""Veredicto por sitio, consolidado por mayoria de las pasadas validas.

	Un sitio que fallo en todas las pasadas de la serie no entra: no hay
	observacion que consolidar. La campana de agosto tiene dos de esos.
	"""
	crudo = {}
	for r in PASADAS:
		ruta = os.path.join(carpeta, "results_EC_r%d.json" % r)
		with io.open(ruta, encoding="utf-8") as fh:
			for fila in json.load(fh):
				clave = fila.get("sigla") or fila.get("id")
				if not fila.get("ok"):
					crudo.setdefault(clave, [])
					continue
				crudo.setdefault(clave, []).append(
					rastrea(fila["cookies"]["nombres_pre"], patrones))
	return {s: mayoria(v) for s, v in crudo.items() if v}


def mcnemar_exacto(b, c):
	"""Binomial exacta bilateral sobre los pares discordantes."""
	n = b + c
	if n == 0:
		return 1.0
	k = min(b, c)
	return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def estabilidad(carpeta, patrones):
	"""Porcentaje de sitios con el mismo veredicto en las tres pasadas."""
	crudo = {}
	for r in PASADAS:
		ruta = os.path.join(carpeta, "results_EC_r%d.json" % r)
		with io.open(ruta, encoding="utf-8") as fh:
			for fila in json.load(fh):
				if not fila.get("ok"):
					continue
				clave = fila.get("sigla") or fila.get("id")
				crudo.setdefault(clave, []).append(
					rastrea(fila["cookies"]["nombres_pre"], patrones))
	completos = {s: v for s, v in crudo.items() if len(v) == len(PASADAS)}
	iguales = [s for s, v in completos.items() if len(set(v)) == 1]
	return len(completos), len(iguales), sorted(set(completos) - set(iguales))


def contraste(titulo, explicacion, a_nombre, A, b_nombre, B, etiqueta):
	comunes = sorted(set(A) & set(B))
	a = sum(1 for s in comunes if A[s] and B[s])
	b = sum(1 for s in comunes if A[s] and not B[s])
	c = sum(1 for s in comunes if not A[s] and B[s])
	d = sum(1 for s in comunes if not A[s] and not B[s])
	p = mcnemar_exacto(b, c)
	print("\n" + "=" * 78)
	print(titulo)
	print("=" * 78)
	for linea in explicacion:
		print("  " + linea)
	print("\n  sitios con veredicto en las dos series: %d" % len(comunes))
	print("  rastreo previo al consentimiento:")
	print("    %-22s %3d de %d  (%.1f %%)"
		  % (a_nombre, a + b, len(comunes), 100.0 * (a + b) / len(comunes)))
	print("    %-22s %3d de %d  (%.1f %%)"
		  % (b_nombre, a + c, len(comunes), 100.0 * (a + c) / len(comunes)))
	print("\n  tabla de McNemar (a: rastreo en las dos; b: solo en la primera;")
	print("                    c: solo en la segunda; d: en ninguna)")
	print("    a=%d  b=%d  c=%d  d=%d" % (a, b, c, d))
	print("    pares discordantes: %d   McNemar exacta bilateral p=%.4f" % (b + c, p))
	if b + c:
		print("\n  los discordantes, uno por uno:")
		for s in comunes:
			if A[s] != B[s]:
				print("    %-14s %s -> %s" % (s, "rastrea" if A[s] else "no rastrea",
											  "no rastrea" if A[s] else "rastrea"))
	# Comprobacion de las cifras declaradas en los READ_ME de las series.
	esp = ESPERADO[etiqueta]
	obtenido = {"n": len(comunes), "a": a, "b": b, "c": c, "d": d}
	if obtenido != esp:
		print("\n  DISCREPANCIA con las cifras declaradas en los READ_ME:")
		print("    declarado: %s" % esp)
		print("    obtenido : %s" % obtenido)
		return False
	print("\n  las cifras coinciden con las declaradas en los READ_ME de las series.")
	return True


def main():
	orig, add = taxonomia()
	patrones = [re.compile(p) for p in orig + add]
	print("taxonomia ampliada leida de %s: %d patrones (%d originales + %d anadidos)"
		  % (FUENTE_TAXONOMIA, len(patrones), len(orig), len(add)))

	datos = {}
	print("\nseries y estabilidad entre sus tres pasadas:")
	for nombre, carpeta in SERIES:
		datos[nombre] = serie(carpeta, patrones)
		n, ig, inest = estabilidad(carpeta, patrones)
		print("  %-20s %3d sitios con veredicto | %d de %d sitios con las tres "
			  "pasadas iguales (%.1f %%)"
			  % (nombre, len(datos[nombre]), ig, n, 100.0 * ig / n))
		if inest:
			print("  %-20s oscilan: %s" % ("", ", ".join(inest)))

	ok1 = contraste(
		"CONTROL DE OPERADOR - ETAPA frente a Telconet, las dos en septiembre",
		["Pregunta: depende el resultado ecuatoriano del operador de red?",
		 "Fijo: el mes, el instrumento, la configuracion y el censo.",
		 "Varia: el operador, la ciudad y la maquina. El contraste mueve tres",
		 "cosas a la vez y no puede separarlas; solo es concluyente si NO",
		 "aparece diferencia, como ocurre."],
		"ETAPA septiembre", datos["ETAPA septiembre"],
		"Telconet septiembre", datos["Telconet septiembre"], "operador")

	ok2 = contraste(
		"ESTABILIDAD TEMPORAL - ETAPA en agosto frente a ETAPA en septiembre",
		["Pregunta: cuanto se mueve el fenomeno con todo lo demas fijo?",
		 "Fijo: el operador, la ciudad, la maquina, el instrumento, la version",
		 "de Node, la configuracion y el censo.",
		 "Varia: solo el mes. Es la unica comparacion del deposito que aisla",
		 "la fecha, y pone cifra a la advertencia de que los sitios cambian."],
		"ETAPA septiembre", datos["ETAPA septiembre"],
		"ETAPA agosto", datos["ETAPA agosto"], "fecha")

	print("\n" + "=" * 78)
	print("QUE SOSTIENEN Y QUE NO")
	print("=" * 78)
	print("  Ninguna cifra del articulo depende de estos dos contrastes: el")
	print("  articulo no analiza ninguna de las dos series de control. Lo que")
	print("  establecen es que el resultado ecuatoriano reportado no es un")
	print("  artefacto del operador de red ni de la fecha de medicion.")
	print("  Tampoco son una replicacion del hallazgo principal, que es la")
	print("  diferencia entre puntos de observacion y vive en data/raw/tracking/.")

	if not (ok1 and ok2):
		raise SystemExit("\nABORTA: alguna cifra no coincide con lo declarado.")


if __name__ == "__main__":
	main()
