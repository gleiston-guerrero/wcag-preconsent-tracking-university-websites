# -*- coding: utf-8 -*-
"""Aplana resultados.json en dos tablas canonicas."""
import csv, json, sys
from pathlib import Path

ENTRADA = Path(sys.argv[1] if len(sys.argv) > 1 else "../../data/raw/accessibility/resultados.json")
SALIDA  = Path(sys.argv[2] if len(sys.argv) > 2 else "../../data/processed")
SALIDA.mkdir(parents=True, exist_ok=True)

d = json.load(open(ENTRADA, encoding="utf-8"))
d.sort(key=lambda r: r["id"])
assert len(d) == 126 and all(r["ok"] for r in d)

H1 = ["id","grupo","sigla","universidad","pais","url","fecha","axe_version","ok","https",
      "cookies_total_pre","cookies_rastreo_pre","nombres_pre","nombres_rastreo",
      "cmp","banner",
      "title","lang","viewport","skip_link",
      "ax_violaciones","ax_nodos","nodos_A","nodos_AA","nodos_AAA",
      "perceptible","operable","comprensible","robusto",
      "max_nivel_sin_fallo","incompletos","passes"]
H2 = ["id","grupo","sigla","regla","impacto","criterio","principio","nivel","nodos","ayuda"]
R1, R2 = [], []

for r in d:
    c = r["cookies"]; a = r["accesibilidad"]; n = a["porNivel"]; p = a["porPrincipio"]
    R1.append([r["id"], "ecuador" if r["grupo"] == "Ecuador" else "mundo", r["sigla"],
               r["nombre"], r["pais"], r["url"], r["fecha"], r["axe_version"],
               "yes" if r["ok"] else "no", "yes" if r["https"] else "no",
               c["total_pre"], c["rastreo_pre"],
               " | ".join(c["nombres_pre"]), " | ".join(c["nombres_rastreo"]),
               " | ".join(c["cmp"]), "yes" if c["banner"] else "no",
               a["title"], a["lang"], "yes" if a["viewport"] else "no",
               "yes" if a.get("skipLink") else "no",
               a["violaciones"], a["nodos"], n["A"], n["AA"], n["AAA"],
               p["Perceptible"], p["Operable"], p["Comprensible"], p["Robusto"],
               a["maxNivelSinFallo"], a.get("incompletos", ""), a.get("passes", "")])
    for x in a["reglas"]:
        R2.append([r["id"], "ecuador" if r["grupo"] == "Ecuador" else "mundo", r["sigla"],
                   x["id"], x["impacto"], x["criterio"] or "", x["principio"],
                   x["nivel"] or "", x["nodos"], x["ayuda"]])

for nom, H, R in (("estudio_126_sitios", H1, R1), ("estudio_reglas_por_sitio", H2, R2)):
    with open(SALIDA / f"{nom}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(H); w.writerows(R)

print("estudio_126_sitios.csv     :", len(R1), "filas,", len(H1), "columnas")
print("estudio_reglas_por_sitio.csv:", len(R2), "filas,", len(H2), "columnas")
print("nombres de cookies mas largos:", max(len(x[12].split(' | ')) for x in R1))
