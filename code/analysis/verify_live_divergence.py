# -*- coding: utf-8 -*-
"""Divergencia entre la medicion automatizada y la verificacion en vivo.

El deposito contiene dos observaciones del mismo fenomeno tomadas en momentos
distintos: la pasada automatizada del 14 de agosto de 2026, cuyo veredicto de
rastreo esta en la columna `rastreo` de cookies_126_sites_v3.csv, y una
verificacion manual en vivo posterior, cuyos nombres de cookie estan en la
columna `Nombres_cookies` de los dos inventarios por grupo.

Ninguna de las dos corrige a la otra: los sitios cambian entre una fecha y la
siguiente. Lo que este script cuantifica es cuanto y en que direccion difieren,
que es la cifra que reporta la seccion 4 del CODEBOOK.

La taxonomia NO se redefine aqui. Se lee estaticamente de verify_multivantage.py
para que exista una unica fuente de verdad y las dos no puedan divergir.

Entradas : ../../data/processed/cookies_126_sites_v3.csv
           ../../data/processed/report_cookies_domestic.csv
           ../../data/processed/report_cookies_foreign.csv
Salida   : informe por consola. No escribe ningun archivo.

Uso: python verify_live_divergence.py
"""
import ast
import csv
import re

FUENTE_TAXONOMIA = "verify_multivantage.py"
V3 = "../../data/processed/cookies_126_sites_v3.csv"
INVENTARIOS = ["../../data/processed/report_cookies_domestic.csv",
               "../../data/processed/report_cookies_foreign.csv"]

# Cifras publicadas en el CODEBOOK, seccion 4. El script termina comprobandolas.
ESPERADO = {"total": 39, "solo_automatica": 35, "solo_en_vivo": 4}


def taxonomia(ruta=FUENTE_TAXONOMIA):
    """Devuelve las dos listas de patrones tal como estan escritas en el
    modulo de referencia, sin importarlo ni volver a declararlas aqui."""
    arbol = ast.parse(open(ruta, encoding="utf-8").read())
    listas = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1:
            destino = nodo.targets[0]
            if isinstance(destino, ast.Name) and destino.id in ("ORIG", "ADD"):
                listas[destino.id] = ast.literal_eval(nodo.value)
    if set(listas) != {"ORIG", "ADD"}:
        raise SystemExit(f"no se encontraron ORIG y ADD en {ruta}")
    return listas["ORIG"], listas["ADD"]


def si_no(valor):
    return (valor or "").strip().lower() in ("yes", "si", "sí", "true", "1")


def nombres(celda):
    """Los dos inventarios separan los nombres de cookie por coma o por barra."""
    return [n.strip() for n in re.split(r"[|,]", celda or "") if n.strip()]


def main():
    orig, add = taxonomia()
    patrones = [re.compile(p) for p in orig + add]
    print(f"taxonomia extendida leida de {FUENTE_TAXONOMIA}: "
          f"{len(orig)} patrones originales + {len(add)} anadidos")

    v3 = {r["sigla"]: r for r in csv.DictReader(open(V3, encoding="utf-8-sig"))}
    vivo = {}
    for ruta in INVENTARIOS:
        for r in csv.DictReader(open(ruta, encoding="utf-8-sig")):
            vivo[r["Sigla"]] = r
    if len(v3) != 126 or len(vivo) != 126:
        raise SystemExit(f"se esperaban 126 sitios; hay {len(v3)} y {len(vivo)}")

    solo_auto, solo_vivo, acuerdo = [], [], 0
    for sigla, fila in v3.items():
        automatica = si_no(fila["rastreo"])
        en_vivo = any(p.search(n) for n in nombres(vivo[sigla].get("Nombres_cookies"))
                      for p in patrones)
        if automatica and not en_vivo:
            solo_auto.append(sigla)
        elif en_vivo and not automatica:
            solo_vivo.append((sigla, vivo[sigla].get("Nombres_cookies", "").strip()))
        else:
            acuerdo += 1

    total = len(solo_auto) + len(solo_vivo)
    print()
    print(f"sitios comparados                       : {len(v3)}")
    print(f"coinciden                               : {acuerdo}")
    print(f"discrepan                               : {total}")
    print(f"  solo la medicion automatizada detecta : {len(solo_auto)}")
    print(f"  solo la verificacion en vivo detecta  : {len(solo_vivo)}")
    print()
    print("sitios donde solo la verificacion en vivo detecta rastreo:")
    for sigla, nombres_vivos in sorted(solo_vivo):
        print(f"  {sigla:12s} {nombres_vivos}")
    print()
    print("sitios donde solo la medicion automatizada detecta rastreo:")
    print("  " + ", ".join(sorted(solo_auto)))

    print()
    obtenido = {"total": total, "solo_automatica": len(solo_auto),
                "solo_en_vivo": len(solo_vivo)}
    if obtenido == ESPERADO:
        print("verificacion: las tres cifras coinciden con las reportadas en el CODEBOOK.")
    else:
        raise SystemExit(f"DISCREPANCIA con el CODEBOOK: esperado {ESPERADO}, "
                         f"obtenido {obtenido}")


if __name__ == "__main__":
    main()
