# -*- coding: utf-8 -*-
"""
sensibilidad_inclusion.py - Sensibilidad a la regla de inclusion de sitios en la
replica multipunto.

El analisis principal (verificar_multipunto.py) exige que un sitio se haya medido
con exito en LAS TRES pasadas de LOS CUATRO puntos de observacion. Esa es la
regla mas estricta de las tres defendibles. Este script repite el analisis bajo
las otras dos y comprueba si la ordenacion de los puntos y el contraste
Ecuador-Alemania son invariantes a esa eleccion.

Reglas:
  R3  el sitio tiene 3 pasadas validas en cada punto  (regla del articulo)
  R2  el sitio tiene al menos 2 pasadas validas en cada punto
  R1  el sitio tiene al menos 1 pasada valida en cada punto

Consolidacion: regla de mayoria sobre las pasadas validas de cada punto. Con dos
pasadas y empate, el sitio no se consolida y queda fuera bajo esa regla.

Taxonomia: la lista extendida, identica a la de verificar_multipunto.py.

ENTRADA:  los archivos resultados_<PUNTO>_r<PASADA>.json de la carpeta indicada.
SALIDA:   por consola, y opcionalmente en CSV con --csv.

Uso:
    python sensibilidad_inclusion.py ../../data/raw/tracking
    python sensibilidad_inclusion.py ../../data/raw/tracking --csv sensibilidad.csv
"""

import argparse
import csv
import itertools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from scipy import stats

# --------------------------------------------------------------------------
# Pasadas validas por punto de observacion. GB r1 se aborto automaticamente
# cuando la VPN aun no habia cambiado de pais y fue descartada; su reemplazo
# es r4. Identico a PAS en verificar_multipunto.py.
# --------------------------------------------------------------------------
PAS = {"EC": [1, 2, 3], "EU": [1, 2, 3], "GB": [2, 3, 4], "US": [1, 2, 3]}
ORDEN = ["EC", "EU", "GB", "US"]

# --------------------------------------------------------------------------
# Taxonomia extendida de cookies de rastreo. Copiada literalmente de
# verificar_multipunto.py para que ambos scripts clasifiquen igual.
# --------------------------------------------------------------------------
ORIG = [r"^_ga", r"^_gid$", r"^__utm", r"^_gcl_", r"^_gac_", r"^YSC$", r"^VISITOR_INFO",
        r"^IDE$", r"^test_cookie$", r"^_fbp$", r"^_fbc$", r"^fr$", r"^_tt_", r"^_ttp$",
        r"^_clck$", r"^_clsk$", r"^MUID$", r"^_uet", r"^personalization_id$", r"^_hj",
        r"^nmstat$", r"^_pk_", r"^pys", r"^_pin_", r"^AMCV_", r"^s_", r"^utag", r"^mbox",
        r"^Hm_lvt_", r"^Hm_lpvt_", r"^HMACCOUNT", r"^BAIDUID$", r"^__qca$", r"^_lc2_",
        r"^ln_or$"]
ADD = [r"^receive-cookie-deprecation$", r"^VISITOR_PRIVACY", r"^__Secure-YNID$",
       r"^__Secure-ROLLOUT", r"^DSID$", r"^ttcsid", r"^MR$", r"^SM$", r"^SRM_B$",
       r"^ANONCHK$", r"^CLID$", r"^bcookie$", r"^bscookie$", r"^lidc$", r"^li_sugr$",
       r"^li_gc$", r"^UserMatchHistory$", r"^AnalyticsSyncHistory$", r"^TapAd_",
       r"^sa-user-id", r"^_scid", r"^sc_at$", r"^muc_ads$", r"^_twpid$", r"^sbjs_",
       r"^_cs_"]
PATRONES = [re.compile(p) for p in ORIG + ADD]


def rastrea(nombres):
    return any(p.search(n) for n in nombres for p in PATRONES)


def nombres_de(rec):
    """Nombres de cookie previos al consentimiento, tolerante al esquema."""
    for clave in ("nombres_pre", "cookies_pre_nombres", "nombres"):
        if clave in rec and rec[clave]:
            return list(rec[clave])
    c = rec.get("cookies")
    if isinstance(c, dict):
        return list(c.get("nombres_pre") or [])
    if isinstance(c, list):
        return [x.get("name", "") for x in c if isinstance(x, dict)]
    return []


def cargar(carpeta: Path):
    """(punto, pasada) -> {id_sitio: bool rastreo}, solo sitios cargados con exito."""
    datos = {}
    for punto, pasadas in PAS.items():
        for r in pasadas:
            ruta = carpeta / f"resultados_{punto}_r{r}.json"
            if not ruta.exists():
                sys.exit(f"No se encuentra {ruta}")
            registros = json.loads(ruta.read_text(encoding="utf-8"))
            d = {}
            for rec in registros:
                if not rec.get("ok"):
                    continue
                d[rec["id"]] = rastrea(nombres_de(rec))
            datos[(punto, r)] = d
    return datos


def consolidar(datos, minimo):
    """Aplica la regla de inclusion y consolida por mayoria.

    Devuelve {id_sitio: {punto: bool}} con los sitios que superan la regla en
    los cuatro puntos y no empatan en ninguno.
    """
    ids = set()
    for d in datos.values():
        ids |= set(d)
    salida = {}
    for i in sorted(ids):
        por_punto = {}
        admisible = True
        for punto, pasadas in PAS.items():
            obs = [datos[(punto, r)][i] for r in pasadas if i in datos[(punto, r)]]
            if len(obs) < minimo:
                admisible = False
                break
            si = sum(obs)
            no = len(obs) - si
            if si == no:                      # empate: no se puede consolidar
                admisible = False
                break
            por_punto[punto] = si > no
        if admisible:
            salida[i] = por_punto
    return salida


def mcnemar_exacto(cons, a, b):
    """Devuelve (n11, b, c, n00, p) para el par de puntos (a, b)."""
    t11 = tb = tc = t00 = 0
    for v in cons.values():
        x, y = v[a], v[b]
        if x and y:
            t11 += 1
        elif x and not y:
            tb += 1
        elif not x and y:
            tc += 1
        else:
            t00 += 1
    n = tb + tc
    p = 1.0 if n == 0 else min(1.0, 2 * stats.binom.cdf(min(tb, tc), n, 0.5))
    return t11, tb, tc, t00, p


def holm(pares):
    """[(etiqueta, p)] -> [(etiqueta, p, p_ajustada)] por Holm-Bonferroni."""
    orden = sorted(pares, key=lambda x: x[1])
    m = len(orden)
    ajust, previo = [], 0.0
    for k, (etq, p) in enumerate(orden):
        v = min(1.0, max(previo, (m - k) * p))
        previo = v
        ajust.append((etq, p, v))
    return ajust


def cochran_q(cons):
    puntos = ORDEN
    k = len(puntos)
    filas = [[1 if v[p] else 0 for p in puntos] for v in cons.values()]
    Li = [sum(f) for f in filas]
    Gj = [sum(f[j] for f in filas) for j in range(k)]
    N = sum(Li)
    num = (k - 1) * (k * sum(g * g for g in Gj) - N * N)
    den = k * N - sum(l * l for l in Li)
    if den == 0:
        return 0.0, 1.0
    Q = num / den
    return Q, 1 - stats.chi2.cdf(Q, k - 1)


def analizar(datos, minimo, etiqueta):
    cons = consolidar(datos, minimo)
    n = len(cons)
    marg = {p: sum(1 for v in cons.values() if v[p]) for p in ORDEN}
    Q, pQ = cochran_q(cons)
    pares = []
    detalle = {}
    for a, b in itertools.combinations(ORDEN, 2):
        t11, tb, tc, t00, p = mcnemar_exacto(cons, a, b)
        pares.append((f"{a}-{b}", p))
        detalle[f"{a}-{b}"] = (t11, tb, tc, t00, p)
    ajust = holm(pares)

    print(f"\n===== {etiqueta}  (n = {n} sitios) =====")
    print("Marginales: " + "   ".join(
        f"{p}={marg[p]} ({100*marg[p]/n:.1f}%)" for p in ORDEN))
    print(f"Cochran Q = {Q:.2f}   gl = 3   p = {pQ:.5f}")
    print(f"{'par':>8} {'a':>4} {'b':>4} {'c':>4} {'d':>4} {'p exacto':>10} {'p Holm':>9}")
    for etq, p, pa in sorted(ajust, key=lambda x: x[1]):
        t11, tb, tc, t00, _ = detalle[etq]
        print(f"{etq:>8} {t11:4d} {tb:4d} {tc:4d} {t00:4d} {p:10.5f} {pa:9.4f}")
    return {"regla": etiqueta, "n": n, "Q": Q, "p_Q": pQ,
            **{f"marg_{p}": marg[p] for p in ORDEN},
            **{f"p_{e}": detalle[e][4] for e in detalle},
            **{f"pholm_{e}": pa for e, _, pa in ajust}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta", nargs="?", default="../../data/raw/tracking")
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()

    datos = cargar(Path(args.carpeta))
    filas = [
        analizar(datos, 3, "R3  tres pasadas validas por punto (regla del articulo)"),
        analizar(datos, 2, "R2  al menos dos pasadas validas por punto"),
        analizar(datos, 1, "R1  al menos una pasada valida por punto"),
    ]
    if args.csv:
        with open(args.csv, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(filas)
        print(f"\nEscrito {args.csv}")


if __name__ == "__main__":
    main()
