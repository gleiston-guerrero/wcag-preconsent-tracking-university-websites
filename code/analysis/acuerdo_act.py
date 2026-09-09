# -*- coding: utf-8 -*-
"""acuerdo_act.py - acuerdo entre las dos codificaciones de la ronda ACT.

Compara la primera codificacion, recoding/ (R02, 8 de septiembre de 2026), con la
segunda, recoding_evaluator2/recoding/ (R04, 9 de septiembre de 2026). Las dos
aplican el mismo instrumento a las mismas quince portadas, y se hicieron de forma
independiente.

El informe SEPARA dos cosas que no son lo mismo y que no deben promediarse:

  BLOQUE A - reglas mecanicas: 23a2a8, afw4f7, c487ae
      La regla decide sola. El evaluador solo ejecuta el script. El acuerdo aqui
      mide REPRODUCIBILIDAD DEL INSTRUMENTO: si dos ejecuciones vieron los mismos
      elementos y calcularon los mismos valores. No mide juicio humano.

  BLOQUE B - reglas de juicio: qt1vmo, 5effbb, fd3a94
      La regla remite al juicio humano y deja la fila marcada REVISAR. El acuerdo
      aqui mide FIABILIDAD ENTRE CODIFICADORES, que es lo que pide un revisor
      cuando pregunta por la kappa. Solo entran las filas donde AMBAS
      codificaciones tienen un resultado definitivo.

  BLOQUE C - veredictos de sitio: 15 sitios x 3 criterios = 45 celdas
      No depende del emparejamiento de elementos, asi que es la cifra mas robusta
      y la directamente comparable con la que hoy declara el README de la ronda.

EMPAREJAMIENTO DE ELEMENTOS. Las dos codificaciones enumeran los elementos por
separado y las portadas cambian de un dia para otro, de modo que `element_n` no
designa el mismo elemento en las dos. La clave es

    sigla + criterio + regla_act + selector

y dentro de cada grupo se emparejan por orden de `element_n`. Si un grupo tiene
distinto numero de elementos en cada codificacion, se emparejan los primeros y el
resto se cuenta como sin pareja. El informe da esas cifras: son un dato sobre la
volatilidad de las portadas, no un defecto que haya que esconder.

Uso, desde code/analysis/:

    python acuerdo_act.py

Escribe en ../../data/processed/:
    act_agreement_summary.csv          una fila por bloque y estrato
    act_agreement_disagreements.csv    una fila por desacuerdo, para inspeccion
"""
import csv
import glob
import io
import math
import os
import sys
from collections import Counter, defaultdict

R02 = "../../data/manual/act_round2/recoding"
R04 = "../../data/manual/act_round2/recoding_evaluator2/recoding"
SALIDA = "../../data/processed"

MECANICAS = ("23a2a8", "afw4f7", "c487ae")
JUICIO = ("qt1vmo", "5effbb", "fd3a94")
CRITERIOS = ("1.1.1", "1.4.3", "2.4.4")
DEFINITIVOS = ("cumple", "falla")


# --------------------------------------------------------------------------- #
# estadistica
# --------------------------------------------------------------------------- #
def kappa_cohen(pares):
    """pares: lista de (a, b). Devuelve un dict con n, acuerdo, kappa, ic y matriz.

    La kappa no esta definida cuando las dos codificaciones usan una sola
    categoria: el acuerdo esperado es 1 y el denominador se anula. En ese caso se
    informa del acuerdo observado y se dice que la kappa no aplica, en lugar de
    devolver un cero o un uno enganosos.

    El intervalo es la aproximacion asintotica habitual,
    SE = sqrt(po(1-po) / (n(1-pe)^2)), valida con n grande.
    """
    n = len(pares)
    if n == 0:
        return {"n": 0, "po": None, "kappa": None, "ic": None, "matriz": {},
                "nota": "sin pares comparables"}
    cats = sorted({x for p in pares for x in p})
    m = Counter(pares)
    po = sum(m[(c, c)] for c in cats) / n
    f1 = Counter(a for a, _ in pares)
    f2 = Counter(b for _, b in pares)
    pe = sum((f1[c] / n) * (f2[c] / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        return {"n": n, "po": po, "kappa": None, "ic": None, "matriz": dict(m),
                "nota": "kappa no definida: una sola categoria en ambas codificaciones"}
    k = (po - pe) / (1 - pe)
    se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2))
    # El intervalo asintotico puede salirse de [-1, 1] con muestras pequenas o
    # marginales muy desequilibradas. Se recorta al rango valido de la kappa y se
    # avisa, en lugar de imprimir un limite imposible.
    lo, hi = max(-1.0, k - 1.96 * se), min(1.0, k + 1.96 * se)
    desbal = min(min(f1[c] for c in cats), min(f2[c] for c in cats)) / n
    nota = ""
    if desbal < 0.05:
        nota = ("kappa inestable: la categoria minoritaria es el %.1f%% de los casos; "
                "lea el acuerdo observado junto a ella" % (100 * desbal))
    elif n < 30:
        nota = "kappa poco fiable: n < 30"
    return {"n": n, "po": po, "kappa": k, "ic": (lo, hi),
            "matriz": dict(m), "nota": nota}


def fmt(res):
    if res["n"] == 0:
        return "sin pares comparables"
    s = "n=%-5d acuerdo=%6.1f%%" % (res["n"], 100 * res["po"])
    if res["kappa"] is None:
        return s + "   kappa: " + res["nota"]
    s += "   kappa=%.3f  IC95%% [%.3f, %.3f]" % (
        res["kappa"], res["ic"][0], res["ic"][1])
    if res["nota"]:
        s += "\n        AVISO: " + res["nota"]
    return s


# --------------------------------------------------------------------------- #
# carga y emparejamiento
# --------------------------------------------------------------------------- #
def cargar(directorio, etiqueta):
    if not os.path.isdir(directorio):
        sys.exit("no existe %s\n(ejecute el script desde code/analysis/)" % directorio)
    filas = []
    for f in sorted(glob.glob(os.path.join(directorio, "*.csv"))):
        with io.open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                r["_cod"] = etiqueta
                filas.append(r)
    if not filas:
        sys.exit("no hay CSV en %s" % directorio)
    print("  %-4s %5d filas  %2d sitios  %s"
          % (etiqueta, len(filas), len({r["abbr"] for r in filas}), directorio))
    return filas


def clave(r):
    return (r["abbr"], r["criterion"], r["act_rule"], r["selector_or_description"])


def emparejar(a, b):
    """Devuelve (pares, sin_pareja_a, sin_pareja_b)."""
    ga, gb = defaultdict(list), defaultdict(list)
    for r in a:
        ga[clave(r)].append(r)
    for r in b:
        gb[clave(r)].append(r)
    orden = lambda rs: sorted(rs, key=lambda r: int(r["element_n"].split("+")[0])
                              if r["element_n"].split("+")[0].isdigit() else 0)
    pares, sa, sb = [], [], []
    for k in set(ga) | set(gb):
        la, lb = orden(ga.get(k, [])), orden(gb.get(k, []))
        n = min(len(la), len(lb))
        pares += list(zip(la[:n], lb[:n]))
        sa += la[n:]
        sb += lb[n:]
    return pares, sa, sb


# --------------------------------------------------------------------------- #
# informe
# --------------------------------------------------------------------------- #
def bloque(titulo, explicacion, pares, reglas, resumen, desacuerdos, etiqueta):
    print("\n" + "=" * 78)
    print(titulo)
    print("=" * 78)
    for linea in explicacion:
        print("  " + linea)

    sub = [(x, y) for x, y in pares if x["act_rule"] in reglas]
    comp = [(x, y) for x, y in sub
            if x["outcome"].strip() in DEFINITIVOS and y["outcome"].strip() in DEFINITIVOS]
    rev_a = sum(1 for x, _ in sub if x["outcome"].strip() == "REVISAR")
    rev_b = sum(1 for _, y in sub if y["outcome"].strip() == "REVISAR")

    print("\n  pares emparejados en estas reglas: %d" % len(sub))
    print("  con resultado definitivo en ambas : %d" % len(comp))
    print("  marcados REVISAR: %d en R02, %d en R04" % (rev_a, rev_b))

    if not comp:
        print("\n  PENDIENTE: no hay ninguna fila con resultado definitivo en las dos")
        print("  codificaciones. Este bloque no se puede calcular todavia.")
        resumen.append({"bloque": etiqueta, "estrato": "TOTAL", "n": 0,
                        "acuerdo": "", "kappa": "", "ic_inf": "", "ic_sup": "",
                        "nota": "pendiente: faltan resoluciones de juicio"})
        return

    def par(x, y):
        return (x["outcome"].strip(), y["outcome"].strip())

    print()
    for r in sorted({x["act_rule"] for x, _ in comp}):
        s = [(x, y) for x, y in comp if x["act_rule"] == r]
        res = kappa_cohen([par(x, y) for x, y in s])
        print("  regla %-9s %s" % (r, fmt(res)))
        resumen.append({"bloque": etiqueta, "estrato": "regla " + r, "n": res["n"],
                        "acuerdo": "%.4f" % res["po"],
                        "kappa": "" if res["kappa"] is None else "%.4f" % res["kappa"],
                        "ic_inf": "" if res["ic"] is None else "%.4f" % res["ic"][0],
                        "ic_sup": "" if res["ic"] is None else "%.4f" % res["ic"][1],
                        "nota": res["nota"]})
    print()
    for c in CRITERIOS:
        s = [(x, y) for x, y in comp if x["criterion"] == c]
        if not s:
            continue
        res = kappa_cohen([par(x, y) for x, y in s])
        print("  criterio %-7s %s" % (c, fmt(res)))
        resumen.append({"bloque": etiqueta, "estrato": "criterio " + c, "n": res["n"],
                        "acuerdo": "%.4f" % res["po"],
                        "kappa": "" if res["kappa"] is None else "%.4f" % res["kappa"],
                        "ic_inf": "" if res["ic"] is None else "%.4f" % res["ic"][0],
                        "ic_sup": "" if res["ic"] is None else "%.4f" % res["ic"][1],
                        "nota": res["nota"]})

    res = kappa_cohen([par(x, y) for x, y in comp])
    print("\n  TOTAL del bloque   %s" % fmt(res))
    print("  matriz de confusion (R02, R04): %s" % res["matriz"])
    print("  prevalencia de 'cumple': %.1f%% en R02, %.1f%% en R04"
          % (100 * sum(1 for x, _ in comp if x["outcome"].strip() == "cumple") / len(comp),
             100 * sum(1 for _, y in comp if y["outcome"].strip() == "cumple") / len(comp)))
    print("  (la kappa baja cuando una categoria domina, aunque el acuerdo sea alto:")
    print("   por eso se dan las dos cifras y la prevalencia junto a ellas)")
    resumen.append({"bloque": etiqueta, "estrato": "TOTAL", "n": res["n"],
                    "acuerdo": "%.4f" % res["po"],
                    "kappa": "" if res["kappa"] is None else "%.4f" % res["kappa"],
                    "ic_inf": "" if res["ic"] is None else "%.4f" % res["ic"][0],
                    "ic_sup": "" if res["ic"] is None else "%.4f" % res["ic"][1],
                    "nota": res["nota"]})

    for x, y in comp:
        if x["outcome"].strip() != y["outcome"].strip():
            desacuerdos.append({
                "bloque": etiqueta, "abbr": x["abbr"], "group": x["group"],
                "criterion": x["criterion"], "act_rule": x["act_rule"],
                "selector": x["selector_or_description"],
                "element_n_R02": x["element_n"], "element_n_R04": y["element_n"],
                "outcome_R02": x["outcome"].strip(), "outcome_R04": y["outcome"].strip(),
                "measured_R02": x.get("measured_value", ""),
                "measured_R04": y.get("measured_value", ""),
            })


def veredictos(filas):
    """falla si algun elemento aplicable falla; pendiente si queda REVISAR."""
    falla, rev, sitios = defaultdict(bool), defaultdict(int), {}
    for r in filas:
        sitios[r["abbr"]] = r["group"]
        o = r["outcome"].strip()
        if o == "falla":
            falla[(r["abbr"], r["criterion"])] = True
        elif o == "REVISAR":
            rev[(r["abbr"], r["criterion"])] += 1
    v = {}
    for s in sitios:
        for c in CRITERIOS:
            v[(s, c)] = ("falla" if falla[(s, c)]
                         else "pendiente" if rev[(s, c)] else "cumple")
    return v, sitios


def main():
    print("Acuerdo entre las dos codificaciones de la ronda ACT")
    print("-" * 78)
    a = cargar(R02, "R02")
    b = cargar(R04, "R04")

    pares, sa, sb = emparejar(a, b)
    print("\nEmparejamiento por sigla + criterio + regla + selector:")
    print("  pares            %5d" % len(pares))
    print("  solo en R02      %5d  %s" % (len(sa), dict(Counter(r["abbr"] for r in sa))))
    print("  solo en R04      %5d  %s" % (len(sb), dict(Counter(r["abbr"] for r in sb))))
    print("  cobertura        %5.1f%% de R02, %5.1f%% de R04"
          % (100.0 * len(pares) / len(a), 100.0 * len(pares) / len(b)))

    # Un hueco de emparejamiento solo importa si la fila que falta llevaba un
    # resultado. Las filas no aplicables no entran en ningun calculo de acuerdo ni
    # pueden mover un veredicto: su ausencia no sesga nada.
    def tipo(r):
        o = r["outcome"].strip()
        return o if o in ("cumple", "falla", "REVISAR") else "no aplicable"
    print("\n  Las filas sin pareja, por tipo de resultado:")
    for etq, lista in (("solo en R02", sa), ("solo en R04", sb)):
        if not lista:
            print("    %-12s ninguna" % etq)
            continue
        c = Counter(tipo(r) for r in lista)
        pesan = c["cumple"] + c["falla"] + c["REVISAR"]
        print("    %-12s %4d  no aplicable %4d  cumple %3d  falla %3d  REVISAR %4d"
              % (etq, len(lista), c["no aplicable"], c["cumple"], c["falla"], c["REVISAR"]))
        print("    %-12s de esas, %d llevan resultado y pesan en el acuerdo (%.1f%% de la codificacion)"
              % ("", pesan, 100.0 * pesan / (len(a) if etq.endswith("R02") else len(b))))
    tr = lambda rs: sum(1 for r in rs if any(k in (r["selector_or_description"] or "").lower()
                                             for k in ("gtranslate", "gt_", "translate")))
    print("    de las filas sin pareja, %d en R02 y %d en R04 pertenecen a un widget"
          % (tr(sa), tr(sb)))
    print("    de traduccion, cuya lista de idiomas se renderiza o no segun la ejecucion.")

    apl = [(x["applicable"].strip(), y["applicable"].strip()) for x, y in pares
           if x["applicable"].strip() and y["applicable"].strip()]
    if apl:
        print("\nAcuerdo sobre la APLICABILIDAD de los pares emparejados:")
        print("  " + fmt(kappa_cohen(apl)))

    resumen, desac = [], []
    bloque("BLOQUE A - reglas mecanicas: reproducibilidad del instrumento",
           ["Reglas 23a2a8, afw4f7 y c487ae. La regla decide sola; el evaluador solo",
            "ejecuta el script. El acuerdo mide si dos ejecuciones vieron lo mismo,",
            "NO si dos personas juzgan igual."],
           pares, MECANICAS, resumen, desac, "A_mecanicas")

    bloque("BLOQUE B - reglas de juicio: fiabilidad entre codificadores",
           ["Reglas qt1vmo, 5effbb y fd3a94. La regla remite al juicio humano.",
            "Esta es la cifra que responde a la pregunta por la fiabilidad entre",
            "codificadores. Requiere que las dos codificaciones hayan resuelto sus",
            "filas REVISAR."],
           pares, JUICIO, resumen, desac, "B_juicio")

    print("\n" + "=" * 78)
    print("BLOQUE C - veredictos de sitio: 15 sitios x 3 criterios")
    print("=" * 78)
    print("  No depende del emparejamiento de elementos. Es la cifra directamente")
    print("  comparable con la que declara hoy el README de la ronda.")
    v2, s2 = veredictos(a)
    v4, s4 = veredictos(b)
    comunes = sorted(set(s2) & set(s4))
    print("\n  %-13s %-30s %-30s" % ("sitio", "R02", "R04"))
    celdas = []
    for s in comunes:
        f = []
        for c in CRITERIOS:
            f.append((v2[(s, c)], v4[(s, c)]))
        print("  %-13s %-30s %-30s%s"
              % (s, " ".join("%-9s" % x for x, _ in f),
                 " ".join("%-9s" % y for _, y in f),
                 "" if all(x == y for x, y in f) else "   <-- difiere"))
        for c, (x, y) in zip(CRITERIOS, f):
            celdas.append((s, c, x, y))
    firmes = [(x, y) for _, _, x, y in celdas if x != "pendiente" and y != "pendiente"]
    pend = len(celdas) - len(firmes)
    print("\n  celdas totales %d | comparables %d | con algun 'pendiente' %d"
          % (len(celdas), len(firmes), pend))
    if firmes:
        res = kappa_cohen(firmes)
        print("  " + fmt(res))
        resumen.append({"bloque": "C_veredictos", "estrato": "45 celdas", "n": res["n"],
                        "acuerdo": "%.4f" % res["po"],
                        "kappa": "" if res["kappa"] is None else "%.4f" % res["kappa"],
                        "ic_inf": "" if res["ic"] is None else "%.4f" % res["ic"][0],
                        "ic_sup": "" if res["ic"] is None else "%.4f" % res["ic"][1],
                        "nota": ("excluye %d celdas con REVISAR sin resolver" % pend
                                 + ("; " + res["nota"] if res["nota"] else ""))})
        for s, c, x, y in celdas:
            if x != y and x != "pendiente" and y != "pendiente":
                desac.append({"bloque": "C_veredictos", "abbr": s, "group": s2.get(s, ""),
                              "criterion": c, "act_rule": "", "selector": "",
                              "element_n_R02": "", "element_n_R04": "",
                              "outcome_R02": x, "outcome_R04": y,
                              "measured_R02": "", "measured_R04": ""})

    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    cs = ["bloque", "estrato", "n", "acuerdo", "kappa", "ic_inf", "ic_sup", "nota"]
    with io.open(os.path.join(SALIDA, "act_agreement_summary.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cs, lineterminator="\n")
        w.writeheader()
        w.writerows(resumen)
    cd = ["bloque", "abbr", "group", "criterion", "act_rule", "selector",
          "element_n_R02", "element_n_R04", "outcome_R02", "outcome_R04",
          "measured_R02", "measured_R04"]
    with io.open(os.path.join(SALIDA, "act_agreement_disagreements.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cd, lineterminator="\n")
        w.writeheader()
        w.writerows(desac)
    print("\nEscritos:")
    print("  %s/act_agreement_summary.csv        %d filas" % (SALIDA, len(resumen)))
    print("  %s/act_agreement_disagreements.csv  %d filas" % (SALIDA, len(desac)))


if __name__ == "__main__":
    main()
