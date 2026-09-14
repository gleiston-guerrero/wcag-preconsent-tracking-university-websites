# -*- coding: utf-8 -*-
"""Reproduce las cifras de acuerdo entre rondas de data/manual/README.md.

Compara la ronda 1 (muestreo de elementos y juicio de una proporcion) con la
ronda 2 (enumeracion exhaustiva bajo reglas ACT) sobre las 45 celdas que
comparten, y las tres codificaciones de los cinco sitios de doble codificacion.

Lo que estas cifras miden es el efecto del CAMBIO DE INSTRUMENTO entre las dos
rondas. No son una estimacion de fiabilidad entre codificadores y no deben
reportarse como tal: la de la ronda ACT esta en acuerdo_act.py, que separa las
reglas mecanicas de las reglas de juicio.

Funciona desde cualquier directorio. Termina con error si alguna cifra no
coincide con la reportada en data/manual/README.md.
"""

import csv
import glob
import io
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "..", "data", "manual")

CRITERIOS = ("1.1.1", "1.4.3", "2.4.4")

# Cifras reportadas en data/manual/README.md; el script se detiene si no salen.
ESPERADO = {
    "tri": (45, 0.600, 0.399, 0.18, 0.61),
    "bin": (45, 0.800, 0.590, 0.35, 0.83),
    "desacuerdos": 18,
    "R01 vs ronda1": (0.375, 0.737),
    "R01 vs D01": (0.192, 0.324),
    "ronda1 vs D01": (0.457, 0.359),
    # Comparacion de la ronda 1 con la ronda ACT del 8-9 de septiembre. Sustituye
    # al 62,2 % con kappa 0,201 que declararon los README de act_round2 hasta la
    # version 2.0.0 y que no se reproduce desde los ficheros depositados.
    "act_tri": (45, 0.378, 0.097, 28),
    "act_bin": (45, 0.733, 0.226, 12),
    "act_direccion": (1, 11),
}


def filas(rel):
    ruta = os.path.join(BASE, rel)
    if not os.path.exists(ruta):
        sys.exit("no existe %s\n(el deposito esta incompleto)" % ruta)
    with io.open(ruta, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(io.StringIO(fh.read())))


def kappa(pares, binario):
    """Kappa de Cohen sin ponderar. IC 95 % con el error estandar asintotico
    sqrt(po(1-po)/(n(1-pe)^2))."""
    if binario:
        pares = [("1" if a == "1" else "0", "1" if b == "1" else "0") for a, b in pares]
    cats = sorted(set(a for a, _ in pares) | set(b for _, b in pares))
    n = len(pares)
    po = sum(1 for a, b in pares if a == b) / float(n)
    p1 = dict((c, sum(1 for a, _ in pares if a == c) / float(n)) for c in cats)
    p2 = dict((c, sum(1 for _, b in pares if b == c) / float(n)) for c in cats)
    pe = sum(p1[c] * p2[c] for c in cats)
    k = (po - pe) / (1 - pe)
    se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2))
    return n, po, k, k - 1.96 * se, k + 1.96 * se, p1, p2


def comprobar(nombre, obtenido, esperado, tol=0.0006):
    if abs(obtenido - esperado) > tol:
        sys.exit("DISCREPANCIA en %s: obtenido %.4f, reportado %.4f" % (nombre, obtenido, esperado))


def main():
    # ronda 1: la codificacion admitida de agosto, una fila por sitio y criterio
    r1 = {}
    for r in filas("wcag_validation_15_sites.csv"):
        r1[(r["abbr"].strip(), r["criterion"].strip())] = r["code"].strip()

    # ronda 2: la recodificacion del primer autor, un fichero por criterio
    r2 = {}
    for fichero, crit in (("recoding_111.csv", "1.1.1"),
                          ("recoding_143.csv", "1.4.3"),
                          ("recoding_244.csv", "2.4.4")):
        for r in filas(fichero):
            r2[(r["abbr"].strip(), crit)] = r["code"].strip()

    # segunda codificacion parcial de agosto, cinco sitios, tal como se entrego
    d01 = {}
    for r in filas("wcag_double_evaluation_5_sites.csv"):
        d01[(r["abbr"].strip(), r["criterion"].strip())] = r["delivered_code"].strip()

    comunes = sorted(set(r1) & set(r2))
    print("Comparacion entre rondas: efecto del cambio de instrumento")
    print("-" * 78)
    print("  ronda 1  wcag_validation_15_sites.csv          %d celdas" % len(r1))
    print("  ronda 2  recoding_111/143/244.csv              %d celdas" % len(r2))
    print("  celdas comparables                             %d" % len(comunes))
    print("")

    pares = [(r1[c], r2[c]) for c in comunes]
    for etiqueta, binario in (("tri", False), ("bin", True)):
        n, po, k, lo, hi, p1, p2 = kappa(pares, binario)
        esp = ESPERADO[etiqueta]
        print("  %s  n=%d  acuerdo=%.1f%%  kappa=%.3f  IC95%% [%.2f, %.2f]"
              % ("tres categorias" if etiqueta == "tri" else "binario        ",
                 n, 100 * po, k, lo, hi))
        print("       marginales ronda 1 %s | ronda 2 %s"
              % (dict((c, int(round(v * n))) for c, v in sorted(p1.items())),
                 dict((c, int(round(v * n))) for c, v in sorted(p2.items()))))
        comprobar("acuerdo observado (%s)" % etiqueta, po, esp[1])
        comprobar("kappa (%s)" % etiqueta, k, esp[2])
        comprobar("IC inferior (%s)" % etiqueta, round(lo, 2), esp[3])
        comprobar("IC superior (%s)" % etiqueta, round(hi, 2), esp[4])

    desac = [(c, r1[c], r2[c]) for c in comunes if r1[c] != r2[c]]
    conP = [d for d in desac if "P" in (d[1], d[2])]
    print("")
    print("  desacuerdos: %d de %d celdas" % (len(desac), len(comunes)))
    print("     entre P y un extremo        : %d" % len(conP))
    print("     entre conforme y no conforme: %d" % (len(desac) - len(conP)))
    if len(desac) != ESPERADO["desacuerdos"]:
        sys.exit("DISCREPANCIA en el numero de desacuerdos: %d, reportados %d"
                 % (len(desac), ESPERADO["desacuerdos"]))
    for c, a, b in desac:
        print("       %-14s %-6s  ronda1=%s  ronda2=%s" % (c[0], c[1], a, b))

    print("")
    print("Los cinco sitios que codificaron los tres evaluadores")
    print("-" * 78)
    tres = sorted(set(r1) & set(r2) & set(d01))
    print("  celdas: %d en %d sitios" % (len(tres), len(set(a for a, _ in tres))))
    for nombre, izq, der in (("R01 vs ronda1", r2, r1),
                             ("R01 vs D01", r2, d01),
                             ("ronda1 vs D01", r1, d01)):
        pp = [(izq[c], der[c]) for c in tres]
        _, _, kt, _, _, _, _ = kappa(pp, False)
        _, _, kb, _, _, _, _ = kappa(pp, True)
        esp = ESPERADO[nombre]
        print("  %-14s  tres categorias %.3f   binario %.3f" % (nombre, kt, kb))
        comprobar("%s (tres categorias)" % nombre, kt, esp[0])
        comprobar("%s (binario)" % nombre, kb, esp[1])
    print("")
    print("  D01 se toma de la columna delivered_code, el codigo tal como se")
    print("  entrego, no del admissible_code admitido tras revisar la evidencia.")

    ronda_act(r1)

    print("")
    print("verificacion: todas las cifras coinciden con las reportadas en")
    print("data/manual/README.md.")


def veredictos_act():
    """Veredicto por sitio y criterio de la ronda ACT del 8-9 de septiembre.
    Un criterio falla en un sitio si algun elemento aplicable falla."""
    base = os.path.join(BASE, "act_round2")
    falla = {}
    for fichero in sorted(glob.glob(os.path.join(base, "recoding", "*.csv"))):
        with io.open(fichero, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(io.StringIO(fh.read())):
                clave = (r["abbr"].strip(), r["criterion"].strip())
                falla[clave] = falla.get(clave, False) or r["outcome"].strip() == "falla"
    for nombre, col in (("qt1vmo_345_resolved.csv", "outcome"),
                        ("review_282_rows.csv", "outcome_TOFILL")):
        for r in filas(os.path.join("act_round2", nombre)):
            clave = (r["abbr"].strip(), (r.get("criterion") or "1.1.1").strip())
            falla[clave] = falla.get(clave, False) or (r.get(col) or "").strip() == "falla"
    return dict((k, "0" if v else "1") for k, v in falla.items())


def ronda_act(r1):
    """La comparacion de la ronda 1 con la ronda ACT, que sustituye a la cifra
    retirada en la version 2.0.0 del deposito."""
    act = veredictos_act()
    comunes = sorted(set(r1) & set(act))
    print("")
    print("La ronda 1 frente a la ronda ACT del 8 y 9 de septiembre")
    print("-" * 78)
    print("  La ronda ACT solo tiene dos categorias: cumple o falla. La ronda 1")
    print("  tiene tres. Se dan los dos esquemas porque la eleccion cambia el")
    print("  resultado, y ninguno de los dos mide acuerdo entre codificadores:")
    print("  miden el efecto de enumerar todos los elementos en lugar de")
    print("  muestrear una proporcion.")
    print("  celdas comparables: %d" % len(comunes))
    for etiqueta, clave, trans in (
            ("tres categorias, P no coincide con nada", "act_tri", lambda x: x),
            ("binario, P contado como no conforme", "act_bin",
             lambda x: "1" if x == "1" else "0")):
        pares = [(trans(r1[c]), act[c]) for c in comunes]
        n, po, k, _, _, _, _ = kappa(pares, False)
        desac = n - int(round(po * n))
        esp = ESPERADO[clave]
        print("  %-40s n=%d  acuerdo=%.1f%%  kappa=%.3f  desacuerdos=%d"
              % (etiqueta, n, 100 * po, k, desac))
        comprobar("acuerdo (%s)" % clave, po, esp[1], tol=0.0006)
        comprobar("kappa (%s)" % clave, k, esp[2], tol=0.0006)
        if desac != esp[3]:
            sys.exit("DISCREPANCIA en los desacuerdos de %s: %d, reportados %d"
                     % (clave, desac, esp[3]))
    sube = baja = 0
    for c in comunes:
        a = "1" if r1[c] == "1" else "0"
        if a != act[c]:
            if act[c] == "1":
                sube += 1
            else:
                baja += 1
    print("  direccion en el esquema binario: %d hacia conforme, %d hacia no conforme"
          % (sube, baja))
    if (sube, baja) != ESPERADO["act_direccion"]:
        sys.exit("DISCREPANCIA en la direccion: %d/%d, reportados %d/%d"
                 % ((sube, baja) + ESPERADO["act_direccion"]))
    print("")
    print("  Hasta la version 2.0.0 los README de act_round2 declaraban 62,2 % de")
    print("  acuerdo con kappa 0,201 y 17 desacuerdos para esta comparacion.")
    print("  Ninguno de los dos esquemas da esas cifras, y por eso se retiraron.")


if __name__ == "__main__":
    main()
