# -*- coding: utf-8 -*-
"""inventario_revisar.py - inventario completo de las filas marcadas REVISAR.

Responde a la pregunta "que falta para cerrarlo todo" con cifras, y distingue lo
que cambia una cifra del articulo de lo que no.

  A. Deciden un veredicto de sitio y siguen sin resolver.
  B. Su criterio ya falla en ese sitio por otro elemento: resolverlas no puede
     cambiar ningun veredicto ni ninguna cifra publicada.
  C. Filas de la segunda codificacion, que corresponden al segundo evaluador.

Y calcula aparte lo unico que exige resolver filas del grupo B: el subconjunto
EMPAREJADO que haria falta para estimar la fiabilidad entre codificadores en las
reglas de juicio, que hoy no se puede estimar porque ninguna fila tiene
resultado definitivo en las dos codificaciones a la vez.

No escribe nada. Ejecutar desde la raiz del repositorio.
"""
import csv
import glob
import io
import os
import sys
from collections import Counter, defaultdict

R02 = "data/manual/act_round2"
R04 = "data/manual/act_round2/recoding_evaluator2"
JUICIO = ("qt1vmo", "5effbb", "fd3a94")


def filas(p):
    if not os.path.isfile(p):
        return []
    with io.open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def cargar(base):
    d = os.path.join(base, "recoding")
    if not os.path.isdir(d):
        sys.exit("no existe %s (ejecute desde la raiz del repositorio)" % d)
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.csv"))):
        out += filas(f)
    return out


def resuelto_en(base):
    """Devuelve (elementos_resueltos, pares_sitio_criterio_que_fallan)."""
    hecho, fallan = set(), set()
    for nombre in ("qt1vmo_345_resolved.csv", "review_282_rows.csv"):
        for r in filas(os.path.join(base, nombre)):
            o = (r.get("outcome") or r.get("outcome_TOFILL") or "").strip()
            if o not in ("cumple", "falla"):
                continue
            c = (r.get("criterion") or "1.1.1").strip()
            hecho.add((r["abbr"], c, r["element_n"]))
            if o == "falla":
                fallan.add((r["abbr"], c))
    return hecho, fallan


def analizar(rec, hecho, fallos_ext, etiqueta):
    """fallos_ext: pares (sigla, criterio) que fallan segun los ficheros de
    resolucion. Sin ellos, un sitio cuyo unico fallo de un criterio esta en el
    fichero de resoluciones parecia no fallar, y sus filas REVISAR se contaban
    como capaces de decidir un veredicto cuando ya no podian decidir nada."""
    falla = defaultdict(bool)
    for r in rec:
        if r["outcome"].strip() == "falla":
            falla[(r["abbr"], r["criterion"])] = True
    for k in fallos_ext:
        falla[k] = True
    rev = [r for r in rec if r["outcome"].strip() == "REVISAR"]
    pend = [r for r in rev if (r["abbr"], r["criterion"], r["element_n"]) not in hecho]
    a = [r for r in pend if not falla[(r["abbr"], r["criterion"])]]
    b = [r for r in pend if falla[(r["abbr"], r["criterion"])]]
    print("\n%s" % etiqueta)
    print("-" * 74)
    print("  filas totales                  %5d" % len(rec))
    print("  marcadas REVISAR               %5d" % len(rev))
    print("  ya resueltas en otro fichero   %5d" % (len(rev) - len(pend)))
    print("  sin resolver                   %5d" % len(pend))
    print("     grupo A, deciden veredicto  %5d  %s"
          % (len(a), dict(Counter(r["act_rule"] for r in a))))
    for (s, c), n in sorted(Counter((r["abbr"], r["criterion"]) for r in a).items()):
        print("        %-13s %-7s %4d filas" % (s, c, n))
    print("     grupo B, no cambian nada    %5d  %s"
          % (len(b), dict(Counter(r["act_rule"] for r in b))))
    return pend, a, b


def main():
    rec2 = cargar(R02)
    h2, f2 = resuelto_en(R02)
    p2, a2, b2 = analizar(rec2, h2, f2, "PRIMERA CODIFICACION  (R02/R03/R01, 8 de septiembre)")

    rec4 = cargar(R04)
    h4, f4 = resuelto_en(R04)
    p4, a4, b4 = analizar(rec4, h4, f4, "SEGUNDA CODIFICACION  (R04, 9 de septiembre)")

    print("\n" + "=" * 74)
    print("PARA CERRARLO ABSOLUTAMENTE TODO")
    print("=" * 74)
    print("  juicios humanos pendientes: %d  (%d en la primera, %d en la segunda)"
          % (len(p2) + len(p4), len(p2), len(p4)))
    print("  de esos, los que cambian alguna cifra del articulo: %d" % (len(a2) + len(a4)))
    print("  de esos, los que no cambian ninguna:                %d" % (len(b2) + len(b4)))

    # --- el subconjunto emparejado que daria la kappa de juicio -------------
    def clave(r):
        return (r["abbr"], r["criterion"], r["act_rule"], r["selector_or_description"])

    def indice(rec, hecho):
        d = defaultdict(list)
        for r in rec:
            if r["act_rule"] in JUICIO:
                d[clave(r)].append(r)
        return d

    i2, i4 = indice(rec2, h2), indice(rec4, h4)
    comunes = sorted(set(i2) & set(i4))
    pares = sum(min(len(i2[k]), len(i4[k])) for k in comunes)

    def sin_resolver(rec, hecho, k, idx):
        return sum(1 for r in idx[k]
                   if r["outcome"].strip() == "REVISAR"
                   and (r["abbr"], r["criterion"], r["element_n"]) not in hecho)

    falta2 = sum(min(sin_resolver(rec2, h2, k, i2), len(i4[k])) for k in comunes)
    falta4 = sum(min(sin_resolver(rec4, h4, k, i4), len(i2[k])) for k in comunes)

    print("\n" + "=" * 74)
    print("LO UNICO QUE EXIGE RESOLVER FILAS DEL GRUPO B")
    print("=" * 74)
    print("  La fiabilidad entre codificadores en las reglas de juicio necesita")
    print("  filas con resultado definitivo en LAS DOS codificaciones. Hoy no hay")
    print("  ninguna, de modo que el bloque B de acuerdo_act.py sale vacio.")
    print("\n  elementos de juicio emparejables entre las dos codificaciones: %d" % pares)
    print("  de esos, sin resolver en la primera:  %d" % falta2)
    print("  de esos, sin resolver en la segunda:  %d" % falta4)
    print("\n  Resolver esos y solo esos da la kappa. Todo lo demas es completitud")
    print("  del deposito, no evidencia para el articulo.")
    print("\n  Y hay un limite estructural: las filas de la primera codificacion las")
    print("  resuelve el primer autor y las de la segunda el segundo evaluador. Si")
    print("  una misma persona resuelve ambas, la kappa deja de medir acuerdo entre")
    print("  codificadores y no debe reportarse como tal.")


if __name__ == "__main__":
    main()
