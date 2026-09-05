# -*- coding: utf-8 -*-
"""extraer_matriz_documental.py - Extrae la matriz documental de los apendices
del manuscrito y la convierte en una tabla CSV.

Los indicadores documentales de la Figura 1 (aviso de privacidad, marco legal
citado, derechos enumerados, contacto o DPO, politica de cookies, declaracion
de accesibilidad) se publican institucion por institucion en los apendices del
articulo, pero no existen como archivo de datos. Este script los recupera del
fuente LaTeX y produce esa tabla, ademas de contar cada indicador por grupo
para poder contrastarlo con las cifras reportadas.

Uso:
    python extraer_matriz_documental.py <ruta_al_tex> [salida.csv]

Ejemplo:
    python extraer_matriz_documental.py "C:\\Repositorios\\_no_publicar\\manuscrito\\privacidad_UAIS_en.tex" matriz_documental.csv
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

# Codigos LaTeX de celda -> valor legible
CODIGOS = [
    (r"\\si\b", "si"),
    (r"\\no\b", "no"),
    (r"\\nv\b", "nv"),
    (r"\\textbf\{P\}", "parcial"),
]

# Cifras codificadas a mano en figuras_uais.py, bloque BLOCKS.
# (etiqueta en la figura, columna del apendice, benchmark, ecuador)
ESPERADO = [
    ("Privacy notice published", "Not.", "Notice", 59, 39),
    ("Applicable framework cited", "Frm.", "LOPDP", 47, 31),
    ("Data-subject rights listed", "Rts.", "Rights", 47, 35),
    ("Privacy contact or DPO", "DPO", "DPO", 54, 24),
    ("Accessibility statement", "Acc.", "Acc.", 47, 7),
]


def limpiar(celda: str) -> str:
    """Convierte una celda LaTeX en un valor legible."""
    c = celda.strip()
    marcada = "$^\\dagger$" in c or "\\dagger" in c
    for patron, valor in CODIGOS:
        if re.search(patron, c):
            return valor + ("*" if marcada else "")
    # celda de texto: se limpia de comandos y llaves
    c = re.sub(r"\\textbf\{([^}]*)\}", r"\1", c)
    c = re.sub(r"\$\^?\\dagger\$", "", c)
    c = re.sub(r"\\[a-zA-Z]+\s*", "", c)
    return c.replace("{", "").replace("}", "").replace("~", " ").strip()


def extraer_tabla(texto: str, etiqueta: str, grupo: str):
    """Devuelve (cabeceras, filas) de la longtable que sigue a \\label{etiqueta}."""
    i = texto.find("\\label{" + etiqueta + "}")
    if i < 0:
        sys.exit("No encuentro la etiqueta " + etiqueta)
    j = texto.find("\\begin{longtable}", i)
    k = texto.find("\\end{longtable}", j)
    if j < 0 or k < 0:
        sys.exit("No encuentro la longtable de " + etiqueta)
    bloque = texto[j:k]

    # La primera fila con \textbf{ y & es la cabecera
    cabeceras = None
    filas = []
    for linea in bloque.split("\\\\"):
        l = linea.strip()
        if not l or l.startswith("%"):
            continue
        if "\\multicolumn" in l or "\\caption" in l:
            continue
        celdas = [c for c in l.split("&")]
        if len(celdas) < 6:
            continue
        celdas = [limpiar(c) for c in celdas]
        if cabeceras is None and any("Abbr" in c or "Sigla" in c for c in celdas):
            cabeceras = celdas
            continue
        if cabeceras is not None and celdas[0].isdigit():
            fila = dict(zip(cabeceras, celdas))
            fila["grupo"] = grupo
            filas.append(fila)
    if cabeceras is None:
        sys.exit("No encuentro la cabecera de " + etiqueta)
    return cabeceras, filas


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    tex = Path(sys.argv[1])
    salida = Path(sys.argv[2] if len(sys.argv) > 2 else "matriz_documental.csv")
    texto = tex.read_text(encoding="utf-8")

    cab_m, filas_m = extraer_tabla(texto, "ap:mundo", "mundo")
    cab_e, filas_e = extraer_tabla(texto, "ap:ecuador", "ecuador")

    print("cabecera benchmark :", cab_m)
    print("cabecera ecuador   :", cab_e)
    print("filas benchmark    :", len(filas_m))
    print("filas ecuador      :", len(filas_e))

    campos = ["grupo"] + [c for c in cab_m]
    for c in cab_e:
        if c not in campos:
            campos.append(c)
    with salida.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, restval="")
        w.writeheader()
        w.writerows(filas_m + filas_e)
    print("escrito", salida, "con", len(filas_m) + len(filas_e), "filas")

    print("\n=== recuento por indicador ===")
    print("%-30s %-6s %-24s %-24s" % ("indicador", "col", "benchmark", "ecuador"))
    for etiqueta, col, col_e, esp_m, esp_e in ESPERADO:
        cm = Counter(f.get(col, "").rstrip("*") for f in filas_m)
        ce = Counter(f.get(col_e, "").rstrip("*") for f in filas_e)
        sm, se = cm.get("si", 0), ce.get("si", 0)
        marca_m = "coincide" if sm == esp_m else "DIFIERE, esperado %d" % esp_m
        marca_e = "coincide" if se == esp_e else "DIFIERE, esperado %d" % esp_e
        print("%-30s %-6s %3d %-20s %3d %-20s" % (etiqueta, col, sm, marca_m, se, marca_e))
        otros_m = {k: v for k, v in cm.items() if k not in ("si", "no", "")}
        otros_e = {k: v for k, v in ce.items() if k not in ("si", "no", "")}
        if otros_m or otros_e:
            print("%-37s otros codigos: benchmark %s, ecuador %s" % ("", otros_m, otros_e))

    marcadas = sum(1 for f in filas_m + filas_e
                   for v in f.values() if isinstance(v, str) and v.endswith("*"))
    print("\nceldas corregidas tras la re-verificacion manual:", marcadas)


if __name__ == "__main__":
    main()
