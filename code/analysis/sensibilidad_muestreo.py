# -*- coding: utf-8 -*-
"""
sensibilidad_muestreo.py Ã¢â‚¬â€ Sensibilidad de la composicion del grupo de referencia.

Responde a la observacion m11 de la revision: comprobar cuanto cambia el grupo de
63 instituciones si se alteran las decisiones arbitrarias de la regla de agregacion
(constante de imputacion, profundidad del corte, prioridad lexicografica) y si se
sustituyen las ediciones de los rankings por las mas recientes.

ENTRADA:  tops.json, con el top 75 de cada edicion, ya normalizado.
SALIDA:   tabla de solapamiento por variante e instituciones que se intercambian.
"""

import json
import re
import unicodedata
import difflib

# Equivalencias entre rankings verificadas a mano. Son necesarias porque la misma
# institucion aparece con nombres distintos en cada ranking; sin esta tabla, EPFL
# se contabiliza como tres instituciones presentes en un solo ranking cada una.
ALIAS = [
    (["swiss federal technology lausanne", "ecole polytechnique federale lausanne",
      "epfl ecole polytechnique federale lausanne"], "EPFL"),
    (["swiss federal technology zurich", "eth zurich",
      "eth zurich swiss federal technology"], "ETH Zurich"),
    (["london", "ucl"], "University College London"),
    (["paris sciences et lettres psl", "psl"], "PSL"),
    (["korea advanced science technology kaist",
      "korea advanced science and technology"], "KAIST"),
    (["science technology china", "china science technology"], "USTC"),
]

ALIAS_SIGLA = {
    "MIT": "massachusetts technology", "Caltech": "california technology",
    "UCL": "University College London", "EPFL": "EPFL",
    "HKUST": "hong kong science technology", "USTC": "USTC",
    "NTU": "nanyang technological", "KAIST": "KAIST",
    "NUS": "national singapore", "ETH": "ETH Zurich",
    "LMU": "munich", "TUM": "technical munich",
    "UBC": "british columbia", "LSE": "london economics political science",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\(.*?\)", " ", s).replace("-", " ")
    s = re.sub(r"\b(university|universite|universitat|universiteit|of|de|the|college|"
               r"institute|institut|school|hochschule|univ|at|and|for)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return re.sub(r"\s+", " ", s)


def canon(k):
    for grupo, nombre in ALIAS:
        if k in grupo:
            return nombre
    return k


def unir(eds):
    """Reconcilia los nombres de las tres ediciones en claves canonicas."""
    out = {}
    for nomed, ed in eds.items():
        for k, (pos, nombre) in ed.items():
            c = canon(k)
            if c not in out:
                m = difflib.get_close_matches(c, list(out), n=1, cutoff=0.80)
                if m:
                    c = m[0]
            out.setdefault(c, {"nombre": nombre, "pos": {}})
            out[c]["pos"][nomed] = pos
    return out


def seleccionar(eds, n=63, imputacion=76, prioridad_cobertura=True, corte=75):
    """Aplica la regla de agregacion. Las tres decisiones arbitrarias son parametros."""
    eds = {k: {kk: vv for kk, vv in v.items() if vv[0] <= corte} for k, v in eds.items()}
    c = unir(eds)
    filas = []
    for k, v in c.items():
        pos = [v["pos"].get(e, imputacion) for e in eds]
        present = len(v["pos"])
        filas.append((present, sum(pos) / len(eds), k, v["nombre"]))
    if prioridad_cobertura:
        filas.sort(key=lambda x: (-x[0], x[1], x[3]))
    else:
        filas.sort(key=lambda x: (x[1], x[3]))
    return filas[:n]


def comparar(base, variante):
    """Devuelve solapamiento y las instituciones que se intercambian."""
    claves_v = {f[2]: f[3] for f in variante}
    lista_v = list(claves_v)
    emparejadas, salen = set(), []
    for _, _, k, nombre in base:
        m = k if k in claves_v else (difflib.get_close_matches(k, lista_v, n=1, cutoff=0.72) or [None])[0]
        if m:
            emparejadas.add(m)
        else:
            salen.append(nombre)
    entran = [claves_v[k] for k in claves_v if k not in emparejadas]
    return len(base) - len(salen), sorted(salen), sorted(entran)


def main():
    t = json.load(open("../../data/raw/census/tops.json", encoding="utf-8"))
    t = {k: {kk: (vv[0], vv[1]) for kk, vv in v.items()} for k, v in t.items()}

    orig = {"qs": t["qs26"], "the": t["the26"], "arwu": t["arwu25"]}
    base = seleccionar(orig)

    variantes = [
        ("Ediciones mas recientes (QS 2027, THE 2026, ARWU 2026)",
         lambda: seleccionar({"qs": t["qs27"], "the": t["the26"], "arwu": t["arwu26"]})),
        ("Imputacion 100 en lugar de 76",
         lambda: seleccionar(orig, imputacion=100)),
        ("Imputacion 80 en lugar de 76",
         lambda: seleccionar(orig, imputacion=80)),
        ("Sin prioridad lexicografica (solo posicion media)",
         lambda: seleccionar(orig, prioridad_cobertura=False)),
        ("Corte del ranking en 50 en lugar de 75",
         lambda: seleccionar(orig, corte=50)),
        ("Corte del ranking en 100 en lugar de 75",
         lambda: seleccionar(orig, corte=100)),
    ]

    print("=" * 78)
    print("  SENSIBILIDAD DE LA COMPOSICION DEL GRUPO DE REFERENCIA (n = 63)")
    print("=" * 78)
    print(f"\nRegla base: 3 rankings, top 75, imputacion 76, prioridad a la cobertura.")
    print(f"Instituciones en la union tras reconciliar nombres: "
          f"{len(unir(orig))}\n")

    print(f"{'Variante':56s} {'Coinciden':>10s} {'%':>7s}")
    print("-" * 78)
    detalles = []
    for nombre, fn in variantes:
        v = fn()
        n, salen, entran = comparar(base, v)
        print(f"{nombre:56s} {n:>7d}/63 {100*n/63:6.1f}%")
        detalles.append((nombre, salen, entran))

    print()
    for nombre, salen, entran in detalles:
        if not salen and not entran:
            continue
        print("-" * 78)
        print(nombre)
        for s in salen:
            print("   sale   -", s)
        for e in entran:
            print("   entra  +", e)

    print()
    print("Nota: la reconciliacion de nombres entre rankings es manual y esta en ALIAS.")
    print("Sin ella, una institucion con tres denominaciones distintas se contabiliza")
    print("tres veces y la regla de cobertura da resultados erroneos.")


if __name__ == "__main__":
    main()
