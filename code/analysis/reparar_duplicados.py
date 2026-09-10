# -*- coding: utf-8 -*-
"""reparar_duplicados.py - quita de qt1vmo_345_resolved.csv las filas duplicadas.

Que paso. La fusion del cierre anadio trece filas de Cornell, pero nueve de esos
elementos ya estaban resueltos en el fichero por el evaluador R03: los elementos
10, 11, 12, 23, 24, 25, 26, 31 y 32. Solo cuatro estaban realmente pendientes,
los elementos 27, 28, 29 y 30. El instrumento que extrajo las filas comprobaba
si el criterio ya fallaba en el sitio, pero no si el elemento concreto tenia ya
veredicto.

Que hace. Busca en TODO el fichero, no solo en Cornell, cualquier par de sigla y
elemento con mas de una fila. Antes de quitar nada comprueba que las filas
duplicadas coinciden en el resultado: si dos procedencias discrepan, se detiene
e informa, porque eso es un conflicto de codificacion y no una duplicacion.
Cuando coinciden, conserva la fila mas antigua, la que ya estaba depositada, y
descarta la anadida.

No escribe nada con --solo-ver. Ejecutar desde la raiz del repositorio.
"""
import argparse
import csv
import io
import os
import sys
from collections import Counter, defaultdict

CSV = "data/manual/act_round2/qt1vmo_345_resolved.csv"


def morir(m):
    print("\n*** ABORTADO: " + m)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-ver", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(CSV):
        morir("no encuentro %s (ejecute desde la raiz del repositorio)" % CSV)
    with io.open(CSV, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        campos = list(rd.fieldnames)
        rows = list(rd)

    print("Estado de partida")
    print("-" * 70)
    print("  filas %d | %s" % (len(rows), dict(Counter(r["outcome"].strip() for r in rows))))
    print("  por evaluador: %s" % dict(Counter(r["evaluator_code"].strip() for r in rows)))

    # --- localizar duplicados en todo el fichero ----------------------------
    porclave = defaultdict(list)
    for i, r in enumerate(rows):
        porclave[(r["abbr"], r["element_n"])].append(i)
    dups = {k: v for k, v in porclave.items() if len(v) > 1}

    print("\nDuplicados de sigla y elemento: %d" % len(dups))
    if not dups:
        print("  no hay nada que reparar.")
        return

    conflictos, quitar = [], []
    for (sig, el), idxs in sorted(dups.items(), key=lambda x: (x[0][0], int(x[0][1]) if x[0][1].isdigit() else 0)):
        res = {rows[i]["outcome"].strip() for i in idxs}
        evs = [rows[i]["evaluator_code"].strip() for i in idxs]
        marca = ""
        if len(res) > 1:
            conflictos.append((sig, el, evs, sorted(res)))
            marca = "   <== CONFLICTO"
        else:
            # se conserva la primera aparicion, que es la ya depositada
            quitar += idxs[1:]
        print("  %-13s elemento %-4s %d filas  evaluadores %s  resultado %s%s"
              % (sig, el, len(idxs), ",".join(evs), "/".join(sorted(res)), marca))

    if conflictos:
        print("\n%d elemento(s) con resultados que NO coinciden entre procedencias:" % len(conflictos))
        for sig, el, evs, res in conflictos:
            print("   %s #%s: %s dicen %s" % (sig, el, ",".join(evs), " y ".join(res)))
        morir("eso es un conflicto de codificacion, no una duplicacion.\n"
              "           Hay que decidir cual vale antes de quitar ninguna fila.")

    print("\n  filas a quitar: %d (se conserva la mas antigua de cada par)" % len(quitar))
    for i in sorted(quitar):
        r = rows[i]
        print("     %-13s elemento %-4s evaluador %s  %s"
              % (r["abbr"], r["element_n"], r["evaluator_code"].strip(), r["outcome"].strip()))

    if a.solo_ver:
        print("\n--solo-ver: no se escribe nada. Fin.")
        return

    fuera = set(quitar)
    nuevas = [r for i, r in enumerate(rows) if i not in fuera]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=campos, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(nuevas)
    io.open(CSV, "w", encoding="utf-8", newline="").write("﻿" + buf.getvalue())

    res = Counter(r["outcome"].strip() for r in nuevas)
    print("\nReparado")
    print("-" * 70)
    print("  filas %d | %s" % (len(nuevas), dict(res)))
    print("  por evaluador: %s" % dict(Counter(r["evaluator_code"].strip() for r in nuevas)))
    porclave2 = defaultdict(int)
    for r in nuevas:
        porclave2[(r["abbr"], r["element_n"])] += 1
    rest = [k for k, v in porclave2.items() if v > 1]
    print("  duplicados restantes: %d" % len(rest))
    if len(nuevas) != 349 or res["cumple"] != 236 or res["falla"] != 113:
        print("\n  AVISO: esperaba 349 filas con 236 cumple y 113 falla.")
        print("  Revise la salida antes de continuar.")
    else:
        print("  coincide con lo previsto: 349 filas, 236 cumple, 113 falla")
    print("\nEjecute ahora:  python %TEMP%\\comprobar_brecha.py")


if __name__ == "__main__":
    main()
