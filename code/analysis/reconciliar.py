# -*- coding: utf-8 -*-
"""Reconcilia el inventario de 126 sitios con los datos embebidos en los informes HTML."""
import csv, json, re, sys
from pathlib import Path

# Rutas por argumento. Por defecto, relativas a la raiz del repositorio si el
# script se ejecuta desde code/analysis/.
INTERIM = Path(sys.argv[1] if len(sys.argv) > 1 else "../../data/interim")
SALIDA  = Path(sys.argv[2] if len(sys.argv) > 2 else "../../data/processed")
SALIDA.mkdir(parents=True, exist_ok=True)

comb = json.load(open(INTERIM / "_comb.json", encoding="utf-8"))
anex = json.load(open(INTERIM / "_anex.json", encoding="utf-8"))
R    = list(csv.DictReader(open(INTERIM / "cookies_126_sitios.csv", encoding="utf-8")))
cm = {r["sigla"]: r for r in comb}
am = {r["sigla"]: r for r in anex}
assert len(comb) == len(anex) == len(R) == 126

def si_no(v):
    if v in ("Si", "Sí", "si", "sí", True):  return "yes"
    if v in ("No", "no", False):             return "no"
    return ""

def barras(v):
    if not v or v.strip() in ("", "0"): return "", 0
    p = [x.strip() for x in re.split(r"[,|]", v) if x.strip()]
    return " | ".join(p), len(p)

H = ["id","grupo","n_grupo","universidad","sigla","sitio","pais","region","tipo","ciudad",
     "cookies_antes_consentir","nombres_cookies","n_nombres_listados","nombres_truncados",
     "rastreo","procedencia_rastreo",
     "cmp_verificacion","banner_verificacion","fuente_verificacion",
     "banner_estudio","polcookies_estudio","nota_documental","revisar"]
OUT, CAMBIOS = [], []

for r in R:
    s = r["sigla"]; c = cm[s]; a = am[s]
    rev = []

    # --- cookies: se restaura desde el HTML cuando el CSV perdio el dato
    n = r["cookies_antes_consentir"]
    nombres = r["nombres_cookies"]
    cmpv = r["cmp_live_ec"] or r["cmp_detectada_mundo"]
    bann = r["banner_live_ec"] or r["banner_visible_mundo"]
    if n == "" and c["live_cookies"] is not None:
        n = str(c["live_cookies"]); nombres = c["live_names"]
        cmpv = c["live_cmp"]; bann = c["live_banner"]
        CAMBIOS.append([s, "cookies_antes_consentir", "(vacio)", n, "restaurado del informe HTML combinado"])
        CAMBIOS.append([s, "nombres_cookies", "(vacio)", nombres, "restaurado del informe HTML combinado"])
        rev.append("medicion restaurada desde el HTML; confirmar contra el JSON crudo")

    nombres, k = barras(nombres)
    trunc = "yes" if (n not in ("", "0") and k == 10 and int(n) > 10) else "no"

    # --- rastreo
    if r["rastreo_ec"]:
        rast = si_no(r["rastreo_ec"]); proc = "csv_ecuador"
        html = "yes" if c["track"] else "no"
        if html != rast:
            CAMBIOS.append([s, "rastreo", f"HTML={html}", f"CSV={rast}", "se conserva el valor del CSV, posterior al HTML"])
            rev.append(f"el informe HTML clasifica este sitio como rastreo={html}")
    else:
        rast = "yes" if c["track"] else "no"; proc = "html_combinado"
        CAMBIOS.append([s, "rastreo", "(vacio)", rast, "importado del informe HTML combinado"])

    OUT.append([
        r["id"], r["grupo"], r["n_grupo"], r["universidad"], s, r["sitio"],
        r["pais"], r["region"], r["tipo"], r["ciudad"],
        n, nombres, k if n != "" else "", trunc,
        rast, proc,
        " | ".join(x.strip() for x in cmpv.split(",") if x.strip()), si_no(bann), "verificacion en vivo",
        si_no(r["banner_estudio"]) if r["banner_estudio"] != "No detectable" else "no_detectable",
        si_no(r["polcookies_estudio"]),
        a["nota"], "; ".join(rev),
    ])

# --- reclasificacion segun la taxonomia literal de auditar.js (lineas 38-50)
import re as _re
RASTREO_JS = [r"^_ga", r"^_gid$", r"^__utm", r"^_gcl_au$", r"^_gac_",
  r"^_fbp$", r"^_fbc$", r"^fr$", r"^_tt_", r"^_ttp$",
  r"^_clck$", r"^_clsk$", r"^MUID$", r"^_hj", r"^_uet",
  r"^nmstat$", r"^_pk_", r"^pys", r"^_pin_",
  r"^AMCV_", r"^s_", r"^utag", r"^mbox",
  r"^Hm_lvt_", r"^Hm_lpvt_", r"^HMACCOUNT$", r"^BAIDUID$",
  r"^__qca$", r"^ln_or$", r"^_lc2_", r"^personalization_id$",
  r"^YSC$", r"^VISITOR_INFO", r"^IDE$", r"^test_cookie$"]
_RX = [_re.compile(x) for x in RASTREO_JS]

I_NOM, I_RAST, I_PROC, I_REV, I_SIG = 11, 14, 15, 22, 4
EXTENDIDA = {"UPEC": "Sourcebuster (sbjs_*), atribucion de trafico",
             "Stanford": "ContentSquare (_cs_id), analitica de sesion"}
for o in OUT:
    nombres = [x.strip() for x in o[I_NOM].split("|") if x.strip()]
    base = "yes" if any(r.search(n) for n in nombres for r in _RX) else "no"
    if base == o[I_RAST]:
        o[I_PROC] = o[I_PROC] + " | taxonomia base confirma"
    elif o[I_SIG] in EXTENDIDA and o[I_RAST] == "yes":
        o[I_PROC] = o[I_PROC] + " | taxonomia extendida: " + EXTENDIDA[o[I_SIG]]
    else:
        ant = o[I_RAST]
        o[I_RAST] = base
        o[I_PROC] = "taxonomia auditar.js"
        o[I_REV] = ("; " if o[I_REV] else "") .join(filter(None, [o[I_REV],
            f"rastreo corregido de {ant} a {base} aplicando la taxonomia del codigo"]))
        CAMBIOS.append([o[I_SIG], "rastreo", ant, base,
                        "las cookies coinciden con la lista RASTREO de auditar.js"])

with open(SALIDA / "cookies_126_sitios_v2.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(H); w.writerows(OUT)
with open(SALIDA / "cambios_reconciliacion.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["sigla","campo","antes","despues","motivo"]); w.writerows(CAMBIOS)

from collections import Counter
print("filas:", len(OUT), "| cambios registrados:", len(CAMBIOS))
print("rastreo yes por grupo:", Counter(o[1] for o in OUT if o[14] == "yes"))
print("procedencia:", Counter(o[15] for o in OUT))
print("celdas vacias en cookies:", sum(1 for o in OUT if o[10] == ""))
print("listas truncadas:", sum(1 for o in OUT if o[13] == "yes"))
print("notas documentales no vacias:", sum(1 for o in OUT if o[21].strip()))
print("filas marcadas para revisar:", sum(1 for o in OUT if o[22]))
for o in OUT:
    if o[22]: print("   ", o[4], "->", o[22])
