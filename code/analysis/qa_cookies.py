# -*- coding: utf-8 -*-
"""Detecta y lista, fila a fila, las irregularidades del inventario de 126 sitios."""
import csv, sys

ENTRADA = sys.argv[1] if len(sys.argv) > 1 else "../../data/interim/cookies_126_sitios.csv"
SALIDA  = sys.argv[2] if len(sys.argv) > 2 else "../../data/processed/qa_irregularidades.csv"

R = list(csv.DictReader(open(ENTRADA, encoding="utf-8")))

def live(r):
    return r["banner_live_ec"] or r["banner_visible_mundo"]
def cmp_(r):
    return r["cmp_live_ec"] or r["cmp_detectada_mundo"]

hall = []
def add(r, cod, desc, valor, accion):
    hall.append([r["id"], r["grupo"], r["sigla"], r["universidad"], r["sitio"],
                 cod, desc, valor, accion])

for r in R:
    n = r["cookies_antes_consentir"]
    k = r["n_cookies_listadas"]

    # I1 medicion ausente
    if n == "":
        add(r, "I1", "Medicion de cookies ausente", "celda vacia",
            "Repetir la pasada con el mismo protocolo y registrar el resultado, o declarar el sitio como no medido y excluirlo de los denominadores")

    # I2 verificacion pendiente
    if r["verificacion_ec"] == "Pendiente":
        add(r, "I2", "Verificacion en vivo sin completar", "Pendiente",
            "Completar la verificacion en vivo o marcar la fila como no verificada de forma explicita")

    # I3 lista de nombres truncada
    if n not in ("", "0") and k not in ("",) and int(k) == 10 and int(n) > 10:
        add(r, "I3", "Lista de nombres de cookies truncada", f"declaradas {n}, listadas {k}",
            "Recuperar los nombres completos del JSON crudo o declarar el limite de 10 en el libro de codigos")

    # I4 banner: el estudio no lo detecta pero en vivo si aparece
    if r["banner_estudio"] == "No detectable" and live(r) in ("Si", "Sí"):
        add(r, "I4", "Sin banner en el estudio pero visible en vivo", f"estudio=No detectable, en vivo={live(r)}, CMP={cmp_(r) or 'sin dato'}",
            "Decidir si 'No detectable' significa ausencia de banner o fallo del detector; si es lo segundo, recodificar como no determinado")

    # I5 banner: el estudio lo detecta pero en vivo no aparece
    if r["banner_estudio"] == "Sí" and live(r) == "No":
        add(r, "I5", "Banner en el estudio pero ausente en vivo", f"estudio=Si, en vivo=No, CMP={cmp_(r) or 'sin dato'}",
            "Comprobar si el sitio retiro el banner entre ambas mediciones y fechar cada observacion por separado")

    # I6 sin clasificacion de rastreo
    if r["grupo"] == "mundo" and not r["rastreo_ec"]:
        add(r, "I6", "Sin clasificacion de rastreo", "columna vacia",
            "Aplicar la misma taxonomia de rastreo que en el bloque de Ecuador a partir de los nombres de cookies")

    # I7 CMP cargada sin banner visible
    if cmp_(r) not in ("", "Ninguna") and live(r) == "No":
        add(r, "I7", "Plataforma de consentimiento cargada sin banner visible", f"CMP={cmp_(r)}, banner en vivo=No",
            "Ninguna: es un hallazgo del estudio, no un error. Verificar que el manuscrito lo interpreta asi")

    # I8 codificacion si/no heterogenea
    for col in ("rastreo_ec", "banner_live_ec", "banner_visible_mundo", "banner_estudio", "polcookies_estudio"):
        if r[col] == "Si":
            add(r, "I8", f"Valor sin tilde en {col}", "Si",
                "Normalizar a 'Si' o a 'Yes' en todas las columnas booleanas del conjunto")
            break

    # I9 campo multivalor con coma
    if "," in cmp_(r):
        add(r, "I9", "Campo multivalor separado por coma", cmp_(r),
            "Sustituir la coma por barra vertical, como ya se hizo en nombres_cookies")

with open(SALIDA, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["id","grupo","sigla","universidad","sitio","codigo","irregularidad","valor_actual","accion_requerida"])
    w.writerows(hall)

from collections import Counter
c = Counter(h[5] for h in hall)
print(f"filas revisadas: {len(R)}   incidencias: {len(hall)}")
for k in sorted(c): print(f"  {k}: {c[k]}")
print(f"informe -> {SALIDA}")
