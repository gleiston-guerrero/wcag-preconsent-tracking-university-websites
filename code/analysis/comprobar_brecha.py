# -*- coding: utf-8 -*-
"""comprobar_brecha.py - cuanto pierde la auditoria automatizada frente a la
codificacion manual exhaustiva, en los quince sitios de la submuestra.

CONSOLIDA LAS TRES FUENTES de la codificacion manual, que es donde estaba el
error de la version anterior:

    data/manual/act_round2/recoding/*.csv        las 7836 filas del recolector
    data/manual/act_round2/qt1vmo_345_resolved.csv  las 345 filas de imagen resueltas
    data/manual/act_round2/review_282_rows.csv      las filas de juicio resueltas

Un par sitio-criterio NO SATISFACE el criterio si algun elemento aplicable falla
en cualquiera de las tres. Queda PENDIENTE si no falla en ninguna y todavia hay
filas marcadas REVISAR sin resolver en ninguna fuente.

Preguntas:

  1. Sitios sin ningun fallo de nivel A detectado por axe-core que no satisfacen
     1.1.1 o 2.4.4, ambos de nivel A.

  2. Criterio por criterio: celdas donde la codificacion manual encuentra fallos
     y axe-core no senala ninguna violacion de ESE criterio.

No escribe nada. Ejecutar desde la raiz del repositorio:

    python comprobar_brecha.py
"""
import csv
import glob
import io
import json
import os
import sys
from collections import Counter, defaultdict

AUTO = "data/raw/accessibility/results.json"
RAIZ_M = "data/manual/act_round2"
CRITERIOS = ("1.1.1", "1.4.3", "2.4.4")
NIVEL = {"1.1.1": "A", "1.4.3": "AA", "2.4.4": "A"}


def morir(m):
    print("\n*** " + m)
    sys.exit(1)


def filas(ruta):
    if not os.path.isfile(ruta):
        return []
    with io.open(ruta, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def consolidar():
    """Devuelve (veredictos, grupo, procedencia) con las tres fuentes unidas."""
    falla, rev, grupo = defaultdict(bool), defaultdict(int), {}
    proc = defaultdict(Counter)

    # --- fuente 1: el recolector -------------------------------------------
    rec = []
    for f in sorted(glob.glob(os.path.join(RAIZ_M, "recoding", "*.csv"))):
        rec += filas(f)
    n1 = len(rec)
    for r in rec:
        grupo[r["abbr"]] = r["group"]
        if r["outcome"].strip() == "falla":
            falla[(r["abbr"], r["criterion"])] = True
            proc[(r["abbr"], r["criterion"])]["recoding"] += 1
    if not grupo:
        morir("no encuentro %s/recoding/ (ejecute desde la raiz del repositorio)" % RAIZ_M)

    # --- fuentes 2 y 3: las resoluciones ------------------------------------
    # Se anota QUE elemento quedo resuelto, en lugar de descontar una unidad de
    # un contador. Descontar era fragil y estaba mal: el descuento vivia dentro
    # de la rama que solo se ejecuta cuando el resultado es "falla", de modo que
    # las resoluciones que dicen "cumple" no cerraban nada y un sitio cuyas
    # filas de juicio todas cumplen se quedaba marcado como abierto para
    # siempre.
    resueltos = set()

    r2 = filas(os.path.join(RAIZ_M, "qt1vmo_345_resolved.csv"))
    for r in r2:
        c = (r.get("criterion") or "1.1.1").strip() or "1.1.1"
        o = (r.get("outcome") or "").strip()
        if o not in ("cumple", "falla"):
            continue
        resueltos.add((r["abbr"], c, r["element_n"]))
        if o == "falla":
            falla[(r["abbr"], c)] = True
            proc[(r["abbr"], c)]["qt1vmo_resolved"] += 1

    r3 = filas(os.path.join(RAIZ_M, "review_282_rows.csv"))
    resueltas3 = 0
    for r in r3:
        o = (r.get("outcome_TOFILL") or r.get("outcome") or "").strip()
        if o not in ("cumple", "falla"):
            continue
        resueltas3 += 1
        c = r["criterion"].strip()
        resueltos.add((r["abbr"], c, r["element_n"]))
        if o == "falla":
            falla[(r["abbr"], c)] = True
            proc[(r["abbr"], c)]["review_282"] += 1

    # Se recuenta lo pendiente contra el conjunto de elementos resueltos.
    rev = defaultdict(int)
    for r in rec:
        if r["outcome"].strip() == "REVISAR" \
           and (r["abbr"], r["criterion"], r["element_n"]) not in resueltos:
            rev[(r["abbr"], r["criterion"])] += 1

    print("Fuentes de la codificacion manual:")
    print("  recoding/                    %5d filas" % n1)
    print("  qt1vmo_345_resolved.csv      %5d filas" % len(r2))
    print("  review_282_rows.csv          %5d filas, %d con resultado" % (len(r3), resueltas3))

    v = {}
    for s in grupo:
        for c in CRITERIOS:
            v[(s, c)] = ("falla" if falla[(s, c)]
                         else "pendiente" if rev[(s, c)] > 0 else "cumple")
    return v, grupo, proc, rev


def main():
    print("Brecha entre la auditoria automatizada y la codificacion manual")
    print("=" * 78)
    v, grupo, proc, rev = consolidar()
    sitios = sorted(grupo, key=lambda s: (grupo[s], s))
    print("\nSubmuestra: %d sitios (%s)" % (len(sitios), dict(Counter(grupo.values()))))

    # --- veredictos consolidados, contra lo que declara el README -----------
    print("\nVeredictos consolidados por criterio:")
    for c in CRITERIOS:
        for g in ("mundo", "ecuador"):
            ss = [s for s in sitios if grupo[s] == g]
            k = sum(1 for s in ss if v[(s, c)] == "falla")
            p = sum(1 for s in ss if v[(s, c)] == "pendiente")
            print("  %s %-8s %d de %d no satisfacen%s"
                  % (c, g, k, len(ss), "   (%d sin cerrar)" % p if p else ""))
    tres = [s for s in sitios if all(v[(s, c)] == "falla" for c in CRITERIOS)]
    ninguno = [s for s in sitios if all(v[(s, c)] == "cumple" for c in CRITERIOS)]
    print("\n  no satisfacen los tres : %d de %d  (%s)"
          % (len(tres), len(sitios), ", ".join(tres) if tres else "-"))
    print("  satisfacen los tres    : %d de %d" % (len(ninguno), len(sitios)))

    if not os.path.isfile(AUTO):
        morir("no encuentro %s" % AUTO)
    registros = json.load(io.open(AUTO, encoding="utf-8"))
    if isinstance(registros, dict):
        registros = list(registros.values())
    auto = {}
    for r in registros:
        if not isinstance(r, dict) or "sigla" not in r:
            continue
        a = r.get("accesibilidad") or {}
        niv = a.get("porNivel") or {}
        crits = set()
        for g in (a.get("reglas") or []):
            if isinstance(g, dict) and g.get("criterio"):
                crits.add(str(g["criterio"]).strip())
        auto[r["sigla"]] = {"A": niv.get("A"), "AA": niv.get("AA"), "AAA": niv.get("AAA"),
                            "criterios": crits}
    conA0 = [s for s, d in auto.items() if d["A"] == 0]
    cero = [s for s, d in auto.items()
            if d["A"] == 0 and d["AA"] == 0 and d["AAA"] == 0]
    print("\nCenso completo: %d sitios | sin fallo de nivel A: %d (%.1f%%) | sin"
          % (len(auto), len(conA0), 100.0 * len(conA0) / max(1, len(auto))))
    print("ninguna violacion en ningun nivel: %d (%.1f%%)"
          % (len(cero), 100.0 * len(cero) / max(1, len(auto))))

    # --- tabla ---------------------------------------------------------------
    print("\n" + "=" * 78)
    print("%-13s %-8s %5s %5s %5s  %-20s %s"
          % ("sitio", "grupo", "A", "AA", "AAA", "axe senala", "manual"))
    print("-" * 78)
    brecha_nivel, brecha_cero = [], []
    brecha_crit = defaultdict(list)
    for s in sitios:
        d = auto.get(s)
        man = " ".join("%s=%s" % (c, v[(s, c)][:4]) for c in CRITERIOS)
        if d is None:
            print("%-13s %-8s   sin datos automaticos          %s" % (s, grupo[s], man))
            continue
        sen = sorted(c for c in CRITERIOS if c in d["criterios"])
        marca = ""
        if d["A"] == 0 and any(v[(s, c)] == "falla" for c in CRITERIOS if NIVEL[c] == "A"):
            brecha_nivel.append(s)
            marca = "  <== nivel A"
        if d["A"] == d["AA"] == d["AAA"] == 0 and any(v[(s, c)] == "falla" for c in CRITERIOS):
            brecha_cero.append(s)
            marca += " / cero violaciones"
        for c in CRITERIOS:
            if c not in d["criterios"] and v[(s, c)] == "falla":
                brecha_crit[c].append(s)
        print("%-13s %-8s %5s %5s %5s  %-20s %s%s"
              % (s, grupo[s], d["A"], d["AA"], d["AAA"],
                 ", ".join(sen) or "ninguno", man, marca))

    # --- respuestas ----------------------------------------------------------
    print("\n" + "=" * 78)
    print("Sitios con CERO fallos de nivel A detectados que no satisfacen 1.1.1")
    print("o 2.4.4 (ambos nivel A): %d de %d" % (len(brecha_nivel), len(sitios)))
    for s in brecha_nivel:
        cu = [c for c in CRITERIOS if NIVEL[c] == "A" and v[(s, c)] == "falla"]
        print("   %-13s %-8s falla %s" % (s, grupo[s], " y ".join(cu)))
    print("\nSitios sin NINGUNA violacion detectada en ningun nivel que no")
    print("satisfacen algun criterio: %d" % len(brecha_cero))
    for s in brecha_cero:
        cu = [c for c in CRITERIOS if v[(s, c)] == "falla"]
        print("   %-13s %-8s falla %s" % (s, grupo[s], ", ".join(cu)))

    print("\n" + "=" * 78)
    print("Brecha criterio por criterio")
    print("=" * 78)
    total_falla = total_ciego = total_pend = 0
    for c in CRITERIOS:
        conf = [s for s in sitios if v[(s, c)] == "falla"]
        pend = [s for s in sitios if v[(s, c)] == "pendiente"]
        ciegos = brecha_crit[c]
        total_falla += len(conf); total_ciego += len(ciegos); total_pend += len(pend)
        print("\n  %s (nivel %s): no satisfacen %d de %d, sin cerrar %d"
              % (c, NIVEL[c], len(conf), len(sitios), len(pend)))
        print("    axe-core no senala el criterio en %d de esos %d"
              % (len(ciegos), len(conf)))
        if ciegos:
            print("      " + ", ".join(ciegos))
    print("\n  TOTAL: la codificacion manual encuentra fallos en %d de las %d celdas"
          % (total_falla, 3 * len(sitios)))
    print("  sitio-criterio; en %d de esas %d la auditoria automatizada no senala"
          % (total_ciego, total_falla))
    print("  ninguna violacion del criterio correspondiente (%.0f%%)."
          % (100.0 * total_ciego / max(1, total_falla)))
    if total_pend:
        print("\n  %d celdas siguen sin cerrar. Las cifras son cotas inferiores:" % total_pend)
        print("  resolverlas solo puede aumentar los fallos, nunca reducirlos.")
    else:
        print("\n  No queda ninguna celda sin cerrar: las cifras son definitivas.")


if __name__ == "__main__":
    main()
