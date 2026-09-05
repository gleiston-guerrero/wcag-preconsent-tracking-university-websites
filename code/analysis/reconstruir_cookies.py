#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruye la tabla de cookies previas al consentimiento desde resultados.json.

Motivo: cookies_126_sitios_v2.csv tomo la medicion de fuentes intermedias
(csv_ecuador, html_combinado) que perdieron la lista de nombres en 52 sitios.
En 27 de ellos eso produjo un falso negativo en la columna rastreo.

Este script vuelve a la fuente cruda, aplica la taxonomia base replicando las
expresiones regulares de auditar.js, aplica la taxonomia extendida de forma
sistematica a los 126 sitios, y conserva las columnas documentales de la tabla
anterior, que no estan en ningun otro archivo.

No inventa valores. Toda columna de medicion sale de resultados.json.

Uso:
    python reconstruir_cookies.py <dir_datos> <dir_salida>
"""
import csv
import json
import re
import sys
from pathlib import Path

# --- Taxonomia base: transcripcion literal de RASTREO en auditar.js --------
BASE = [
    (r"^_ga", "Google Analytics"), (r"^_gid$", "Google Analytics"),
    (r"^__utm", "Google Analytics"), (r"^_gcl_au$", "Google Ads"),
    (r"^_gac_", "Google Ads"),
    (r"^_fbp$", "Meta"), (r"^_fbc$", "Meta"), (r"^fr$", "Meta"),
    (r"^_tt_", "TikTok"), (r"^_ttp$", "TikTok"),
    (r"^_clck$", "Microsoft Clarity"), (r"^_clsk$", "Microsoft Clarity"),
    (r"^MUID$", "Microsoft"),
    (r"^_hj", "Hotjar"), (r"^_uet", "Bing UET"),
    (r"^nmstat$", "Siteimprove"), (r"^_pk_", "Matomo"),
    (r"^pys", "PixelYourSite"), (r"^_pin_", "Pinterest"),
    (r"^AMCV_", "Adobe"), (r"^s_", "Adobe"), (r"^utag", "Tealium"),
    (r"^mbox", "Adobe Target"),
    (r"^Hm_lvt_", "Baidu"), (r"^Hm_lpvt_", "Baidu"),
    (r"^HMACCOUNT$", "Baidu"), (r"^BAIDUID$", "Baidu"),
    (r"^__qca$", "Quantcast"), (r"^ln_or$", "LinkedIn"),
    (r"^_lc2_", "LiveRamp"), (r"^personalization_id$", "X/Twitter"),
    (r"^YSC$", "YouTube"), (r"^VISITOR_INFO", "YouTube"),
    (r"^IDE$", "DoubleClick"), (r"^test_cookie$", "DoubleClick"),
]

# --- Taxonomia extendida: proveedores identificados tras la auditoria -----
# Cada entrada debe poder justificarse ante un revisor.
EXT = [
    (r"^sbjs_", "Sourcebuster", "atribucion de trafico"),
    (r"^_cs_", "ContentSquare", "analitica de sesion"),
]

BASE_RE = [(re.compile(p), v) for p, v in BASE]
EXT_RE = [(re.compile(p), v, d) for p, v, d in EXT]

# Columnas documentales que solo existen en la tabla anterior.
DOC = ["pais", "region", "ciudad", "tipo", "cmp_verificacion",
       "banner_verificacion", "fuente_verificacion", "polcookies_estudio",
       "nota_documental"]


def clasificar(nombres):
    """Devuelve (proveedores_base, proveedores_ext) para una lista de nombres."""
    b, e = [], []
    for n in nombres:
        if not n:
            continue
        for rx, v in BASE_RE:
            if rx.search(n):
                if v not in b:
                    b.append(v)
                break
        else:
            for rx, v, d in EXT_RE:
                if rx.search(n):
                    if v not in e:
                        e.append(v)
                    break
    return b, e


def main(dir_datos, dir_salida):
    dd, ds = Path(dir_datos), Path(dir_salida)
    ds.mkdir(parents=True, exist_ok=True)

    raw = json.loads((dd / "resultados.json").read_text(encoding="utf-8"))
    with (dd / "cookies_126_sitios_v2.csv").open(encoding="utf-8-sig") as f:
        prev = {r["id"]: r for r in csv.DictReader(f)}

    filas, sin_clasificar, divergencias = [], {}, []

    for r in raw:
        sid = str(r["id"])
        c = r.get("cookies") or {}
        nombres = [n for n in (c.get("nombres_pre") or []) if n]
        base, ext = clasificar(nombres)
        p = prev.get(sid, {})

        # Nombres que la tabla anterior listaba y el crudo no registra.
        ant = [n.strip() for n in (p.get("nombres_cookies") or "").split("|") if n.strip()]
        extra = [n for n in ant if n not in nombres]
        if extra:
            divergencias.append({
                "id": sid, "sigla": r.get("sigla", ""), "grupo": r.get("grupo", ""),
                "nombres_no_presentes_en_crudo": " | ".join(extra),
            })

        for n in nombres:
            if not any(rx.search(n) for rx, _ in BASE_RE) and \
               not any(rx.search(n) for rx, _, _ in EXT_RE):
                sin_clasificar.setdefault(n, 0)
                sin_clasificar[n] += 1

        prov = base + ext
        if base and ext:
            proc = "taxonomia base y extendida: " + ", ".join(prov)
        elif ext:
            proc = "taxonomia extendida: " + ", ".join(ext)
        elif base:
            proc = "taxonomia base: " + ", ".join(base)
        else:
            proc = "sin coincidencia con ninguna taxonomia"

        fila = {
            "id": sid,
            "grupo": r.get("grupo", ""),
            "sigla": r.get("sigla", ""),
            "universidad": r.get("nombre", ""),
            "sitio": r.get("url", ""),
            "fecha": r.get("fecha", ""),
            "cookies_antes_consentir": c.get("total_pre", 0),
            "nombres_cookies": " | ".join(nombres),
            "n_nombres_listados": len(nombres),
            "rastreo": "yes" if prov else "no",
            "rastreo_base": "yes" if base else "no",
            "proveedores_rastreo": " | ".join(prov),
            "procedencia_rastreo": proc,
            "banner_estudio": "yes" if c.get("banner") else "no_detectable",
            "cmp_estudio": " | ".join(c.get("cmp") or []),
        }
        for k in DOC:
            fila[k] = p.get(k, "")
        filas.append(fila)

    cab = list(filas[0].keys())
    with (ds / "cookies_126_sitios_v3.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cab)
        w.writeheader()
        w.writerows(filas)

    with (ds / "cookies_nombres_sin_clasificar.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nombre_cookie", "sitios_en_que_aparece"])
        for n, k in sorted(sin_clasificar.items(), key=lambda x: (-x[1], x[0])):
            w.writerow([n, k])

    with (ds / "cookies_divergencias_v2.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "sigla", "grupo", "nombres_no_presentes_en_crudo"])
        w.writeheader()
        w.writerows(divergencias)

    # --- Verificacion: la taxonomia base debe reproducir rastreo_pre -------
    desajuste = 0
    for r in raw:
        c = r.get("cookies") or {}
        b, _ = clasificar([n for n in (c.get("nombres_pre") or []) if n])
        if bool(b) != (c.get("rastreo_pre", 0) > 0):
            desajuste += 1
            print("  DESAJUSTE base:", r.get("sigla"))

    ec = sum(1 for x in filas if x["grupo"] in ("ecuador", "Ecuador") and x["rastreo"] == "yes")
    mu = sum(1 for x in filas if x["grupo"] not in ("ecuador", "Ecuador") and x["rastreo"] == "yes")
    ecb = sum(1 for x in filas if x["grupo"] in ("ecuador", "Ecuador") and x["rastreo_base"] == "yes")
    mub = sum(1 for x in filas if x["grupo"] not in ("ecuador", "Ecuador") and x["rastreo_base"] == "yes")

    print("filas escritas:", len(filas))
    print("desajustes de la taxonomia base frente a rastreo_pre:", desajuste)
    print("rastreo, taxonomia base       -> referencia %d : ecuador %d" % (mub, ecb))
    print("rastreo, base + extendida     -> referencia %d : ecuador %d" % (mu, ec))
    print("nombres sin clasificar (distintos):", len(sin_clasificar))
    print("sitios con nombres divergentes en v2:", len(divergencias))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos",
         sys.argv[2] if len(sys.argv) > 2 else "datos")
