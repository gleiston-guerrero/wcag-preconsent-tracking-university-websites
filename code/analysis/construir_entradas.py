# -*- coding: utf-8 -*-
"""construir_entradas.py - Reconstruye las entradas intermedias de la cadena de
tablas de cookies a partir del material publicado en este repositorio.

La cadena completa es:

    docs/reports/reporte_cookies_combinado.html   -> _comb.json
    docs/reports/anexo_universidades_cookies.html -> _anex.json
    data/processed/reporte_cookies_nacionales.csv  }
    data/processed/reporte_cookies_extranjeras.csv } -> cookies_126_sitios.csv

    reconciliar.py         -> cookies_126_sitios_v2.csv, cambios_reconciliacion.csv
    qa_cookies.py          -> qa_irregularidades.csv
    reconstruir_cookies.py -> cookies_126_sitios_v3.csv,
                              cookies_nombres_sin_clasificar.csv,
                              cookies_divergencias_v2.csv

Los dos informes HTML llevan sus datos embebidos en una constante DATA de
JavaScript; este script los extrae sin ejecutar nada. La tabla de 126 sitios se
obtiene fusionando los dos informes CSV por grupo, con el identificador global
tomado del orden del informe combinado.

Uso, desde code/analysis/:
    python construir_entradas.py
    python construir_entradas.py <raiz_del_repositorio> <dir_salida>
"""

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1] if len(sys.argv) > 1 else "../..")
SALIDA = Path(sys.argv[2] if len(sys.argv) > 2 else RAIZ / "data/interim")
SALIDA.mkdir(parents=True, exist_ok=True)

FUENTES_HTML = [
    (RAIZ / "docs/reports/reporte_cookies_combinado.html", "_comb.json"),
    (RAIZ / "docs/reports/anexo_universidades_cookies.html", "_anex.json"),
]
NACIONALES = RAIZ / "data/processed/reporte_cookies_nacionales.csv"
EXTRANJERAS = RAIZ / "data/processed/reporte_cookies_extranjeras.csv"

CABECERA = ["id", "grupo", "n_grupo", "universidad", "sigla", "sitio", "pais",
            "region", "tipo", "ciudad", "verificacion_ec",
            "cookies_antes_consentir", "nombres_cookies", "n_cookies_listadas",
            "rastreo_ec", "cmp_live_ec", "banner_live_ec",
            "cmp_detectada_mundo", "banner_visible_mundo",
            "banner_estudio", "polcookies_estudio"]


def extraer_data(ruta: Path):
    """Devuelve la constante DATA embebida en el informe HTML."""
    html = ruta.read_text(encoding="utf-8")
    m = re.search(r"const\s+DATA\s*=\s*(\[.*?\])\s*;", html, re.S)
    if not m:
        sys.exit(f"No encuentro la constante DATA en {ruta}")
    return json.loads(m.group(1))


def n_listados(v):
    return len([x for x in re.split(r"[,|]", v or "") if x.strip()])


def main():
    for ruta, nombre in FUENTES_HTML:
        if not ruta.exists():
            sys.exit(f"No existe {ruta}")
        datos = extraer_data(ruta)
        if len(datos) != 126:
            sys.exit(f"{ruta.name}: esperaba 126 registros y hay {len(datos)}")
        destino = SALIDA / nombre
        with destino.open("w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False)
        print(f"{ruta.name} -> {nombre}: {len(datos)} registros")

    comb = json.loads((SALIDA / "_comb.json").read_text(encoding="utf-8"))
    orden = {r["sigla"]: i + 1 for i, r in enumerate(comb)}

    nac = list(csv.DictReader(NACIONALES.open(encoding="utf-8-sig")))
    ext = list(csv.DictReader(EXTRANJERAS.open(encoding="utf-8-sig")))
    if len(nac) != 63 or len(ext) != 63:
        sys.exit(f"esperaba 63 y 63 filas; hay {len(nac)} y {len(ext)}")

    filas = []
    for r in nac:
        filas.append({
            "id": orden.get(r["Sigla"], ""), "grupo": "ecuador",
            "n_grupo": r["#"], "universidad": r["Universidad"],
            "sigla": r["Sigla"], "sitio": r["Sitio"],
            "pais": "Ecuador", "region": "Ecuador",
            "tipo": r["Tipo"], "ciudad": r["Ciudad"],
            "verificacion_ec": r["Verificacion"],
            "cookies_antes_consentir": r["Cookies_antes_consentir"],
            "nombres_cookies": r["Nombres_cookies"],
            "n_cookies_listadas": n_listados(r["Nombres_cookies"]),
            "rastreo_ec": r["Rastreo"],
            "cmp_live_ec": r["CMP_live"], "banner_live_ec": r["Banner_live"],
            "cmp_detectada_mundo": "", "banner_visible_mundo": "",
            "banner_estudio": r["Banner_estudio"],
            "polcookies_estudio": r["PolCookies_estudio"]})
    for r in ext:
        filas.append({
            "id": orden.get(r["Sigla"], ""), "grupo": "mundo",
            "n_grupo": r["#"], "universidad": r["Universidad"],
            "sigla": r["Sigla"], "sitio": r["Sitio"],
            "pais": r["Pais"], "region": r["Region"],
            "tipo": "", "ciudad": "", "verificacion_ec": "",
            "cookies_antes_consentir": r["Cookies_antes_consentir"],
            "nombres_cookies": r["Nombres_cookies"],
            "n_cookies_listadas": n_listados(r["Nombres_cookies"]),
            "rastreo_ec": "", "cmp_live_ec": "", "banner_live_ec": "",
            "cmp_detectada_mundo": r["CMP_detectada"],
            "banner_visible_mundo": r["Banner_visible"],
            "banner_estudio": r["Banner_estudio"],
            "polcookies_estudio": r["PolCookies_estudio"]})

    sin_id = [f["sigla"] for f in filas if not f["id"]]
    if sin_id:
        sys.exit("siglas sin correspondencia en el informe combinado: "
                 + ", ".join(sin_id))
    filas.sort(key=lambda x: x["id"])

    destino = SALIDA / "cookies_126_sitios.csv"
    with destino.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CABECERA)
        w.writeheader()
        w.writerows(filas)
    print(f"cookies_126_sitios.csv: {len(filas)} filas -> {destino}")


if __name__ == "__main__":
    main()
