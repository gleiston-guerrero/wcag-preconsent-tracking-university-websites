# -*- coding: utf-8 -*-
"""extract_documentary_matrix.py - Extrae la matriz documental de los apendices
del manuscrito y la convierte en una tabla CSV.

Los indicadores documentales de la Figura 1 (aviso de privacidad, marco legal
citado, derechos enumerados, contacto o DPO, politica de cookies, declaracion
de accesibilidad) se publican institucion por institucion en los apendices del
articulo, pero no existen como archivo de datos. Este script los recupera del
fuente LaTeX y produce esa tabla, ademas de contar cada indicador por grupo
para poder contrastarlo con las cifras reportadas.

Uso:
    python extract_documentary_matrix.py <ruta_al_tex> [salida.csv]

Ejemplo:
    python extract_documentary_matrix.py "..\\manuscrito\\privacidad_UAIS_en.tex" documentary_matrix.csv

Salidas:
    <salida>.csv        matriz ancha, una fila por institucion
    <salida:-4>_long.csv  matriz larga (tidy), una fila por celda

--------------------------------------------------------------------------
CORRECCIONES respecto de la version anterior
--------------------------------------------------------------------------
1. El codigo de celda "parcial" se escribe en el LaTeX como la macro \\pc, no
   como \\textbf{P}. La tabla de CODIGOS solo contemplaba la segunda forma, de
   modo que ninguna de las 25 celdas parciales coincidia con un patron y caia
   en la rama de limpieza de texto, donde la expresion \\[a-zA-Z]+ borraba la
   macro y dejaba la cadena vacia. El CSV publicado exportaba por tanto 25
   codigos "parcial" como celdas vacias, y el libro de codigos declara que una
   celda vacia significa que la columna no aplica a ese grupo. Se anaden \\pc
   y \\parcial a los patrones, conservando \\textbf{P} por compatibilidad.
2. Las instituciones creadas en 2024 o despues se marcan en el apendice
   ecuatoriano con $^\\ddagger$. La limpieza de texto borraba la macro pero
   dejaba el residuo "$^$" pegado a la sigla (por ejemplo "USECIPOL$^$").
   Ahora la marca se retira de la sigla y se registra en una columna propia.
3. Ninguna celda queda vacia. Donde la columna no aplica al grupo se escribe
   el valor explicito "no_aplica", de modo que el fichero no contenga ningun
   valor cuyo significado dependa de una nota externa.
4. La verificacion final ya no comprueba solo los recuentos de "si": tambien
   contrasta los recuentos de "parcial" y de "nv" contra los valores esperados,
   que es justo lo que habria detectado el fallo anterior.
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

# Codigos LaTeX de celda -> valor legible.
# El orden importa: \nv antes que \no seria incorrecto, pero \b lo evita.
CODIGOS = [
    (r"\\si\b", "si"),
    (r"\\no\b", "no"),
    (r"\\nv\b", "nv"),
    (r"\\pc\b", "parcial"),          # <- macro realmente usada en el .tex
    (r"\\parcial\b", "parcial"),     # alias defensivo
    (r"\\textbf\{P\}", "parcial"),   # forma antigua, se conserva
]

# Valor explicito para las celdas cuya columna no aplica al grupo de la fila.
NO_APLICA = "no_aplica"

# Columnas por grupo, para poder distinguir "no aplica" de "sin codigo".
COLS_MUNDO = ["C", "QS", "THE", "ARWU", "Not.", "Frm.", "Rts.", "DPO", "Ckp.", "Acc."]
COLS_ECUADOR = ["Type", "Notice", "LOPDP", "Rights", "DPO", "Acc.", "Transp."]

# Cifras codificadas a mano en figures_uais.py, bloque BLOCKS.
# (etiqueta, columna benchmark, columna ecuador, si_bench, si_ec, parc_bench,
#  parc_ec, nv_bench, nv_ec)
ESPERADO = [
    ("Privacy notice published",   "Not.", "Notice", 59, 39,  2, 5, 0, 3),
    ("Applicable framework cited", "Frm.", "LOPDP",  47, 31, 11, 1, 0, 6),
    ("Data-subject rights listed", "Rts.", "Rights", 47, 35,  5, 0, 0, 4),
    ("Privacy contact or DPO",     "DPO",  "DPO",    54, 24,  0, 0, 0, 4),
    ("Accessibility statement",    "Acc.", "Acc.",   47,  7,  0, 1, 0, 2),
]


def limpiar(celda: str):
    """Convierte una celda LaTeX en (valor legible, marcada_dagger, nueva_2024)."""
    c = celda.strip()
    # \ddagger marca institucion creada en 2024 o despues; \dagger marca celda
    # corregida tras la re-verificacion manual. Se comprueba \ddagger primero,
    # porque la cadena "\dagger" no aparece dentro de "\ddagger" pero conviene
    # dejar el orden explicito.
    nueva = "\\ddagger" in c
    marcada = re.search(r"(?<!d)\\dagger", c) is not None
    for patron, valor in CODIGOS:
        if re.search(patron, c):
            return valor + ("*" if marcada else ""), marcada, nueva
    # celda de texto: se limpia de comandos, llaves y residuos de superindice
    c = re.sub(r"\\textbf\{([^}]*)\}", r"\1", c)
    c = re.sub(r"\$\^?\\d?dagger\$", "", c)
    c = re.sub(r"\\[a-zA-Z]+\s*", "", c)
    c = c.replace("{", "").replace("}", "").replace("~", " ")
    c = re.sub(r"\$\^?\s*\$", "", c)      # residuo "$^$" tras borrar la macro
    c = c.replace("$", "").strip()
    return c, marcada, nueva


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

    cabeceras = None
    filas = []
    for linea in bloque.split("\\\\"):
        l = linea.strip()
        if not l or l.startswith("%"):
            continue
        if "\\multicolumn" in l or "\\caption" in l:
            continue
        celdas_txt = l.split("&")
        if len(celdas_txt) < 6:
            continue
        limpias = [limpiar(c) for c in celdas_txt]
        celdas = [v for v, _, _ in limpias]
        if cabeceras is None and any("Abbr" in c or "Sigla" in c for c in celdas):
            cabeceras = celdas
            continue
        if cabeceras is not None and celdas[0].isdigit():
            fila = dict(zip(cabeceras, celdas))
            fila["grupo"] = grupo
            fila["nueva_2024"] = "si" if any(n for _, _, n in limpias) else "no"
            filas.append(fila)
    if cabeceras is None:
        sys.exit("No encuentro la cabecera de " + etiqueta)
    return cabeceras, filas


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    tex = Path(sys.argv[1])
    salida = Path(sys.argv[2] if len(sys.argv) > 2 else "documentary_matrix.csv")
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
    campos.append("nueva_2024")

    # Ninguna celda vacia: se marca explicitamente lo que no aplica al grupo.
    aplica = {"mundo": set(COLS_MUNDO), "ecuador": set(COLS_ECUADOR)}
    for fila in filas_m + filas_e:
        for c in campos:
            if c in ("grupo", "#", "\\#", "Abbr.", "nueva_2024"):
                continue
            if c not in aplica[fila["grupo"]]:
                fila[c] = NO_APLICA
            elif not str(fila.get(c, "")).strip():
                fila[c] = ""     # se deja vacio solo si de verdad falta un codigo

    with salida.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, restval="")
        w.writeheader()
        w.writerows(filas_m + filas_e)
    print("escrito", salida, "con", len(filas_m) + len(filas_e), "filas")

    # Formato largo (tidy), una fila por celda codificada.
    indicadores = [("Not.", "Notice", "aviso_privacidad"),
                   ("Frm.", "LOPDP", "marco_normativo"),
                   ("Rts.", "Rights", "derechos"),
                   ("DPO", "DPO", "contacto_dpo"),
                   ("Ckp.", None, "politica_cookies"),
                   ("Acc.", "Acc.", "declaracion_accesibilidad"),
                   (None, "Transp.", "transparencia_lotaip")]
    largo = salida.with_name(salida.stem + "_long.csv")
    with largo.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["grupo", "abbr", "indicador", "columna_apendice",
                    "valor", "corregida_reverificacion"])
        for fila in filas_m + filas_e:
            g = fila["grupo"]
            for col_m, col_e, nombre in indicadores:
                col = col_m if g == "mundo" else col_e
                if col is None:
                    continue
                v = str(fila.get(col, ""))
                if v == NO_APLICA or v == "":
                    continue
                w.writerow([g, fila.get("Abbr.", ""), nombre, col,
                            v.rstrip("*"), "si" if v.endswith("*") else "no"])
    print("escrito", largo)

    print("\n=== verificacion de recuentos ===")
    fallos = 0
    cab = "%-28s %-6s %-26s %-26s" % ("indicador", "col", "benchmark", "ecuador")
    print(cab)
    for etiqueta, col, col_e, e_sm, e_se, e_pm, e_pe, e_nm, e_ne in ESPERADO:
        cm = Counter(str(f.get(col, "")).rstrip("*") for f in filas_m)
        ce = Counter(str(f.get(col_e, "")).rstrip("*") for f in filas_e)
        obs = [(cm.get("si", 0), e_sm), (ce.get("si", 0), e_se),
               (cm.get("parcial", 0), e_pm), (ce.get("parcial", 0), e_pe),
               (cm.get("nv", 0), e_nm), (ce.get("nv", 0), e_ne)]
        ok = all(o == e for o, e in obs)
        fallos += 0 if ok else 1
        print("%-28s %-6s si=%2d P=%2d nv=%d %-8s si=%2d P=%2d nv=%d %-8s" % (
            etiqueta, col,
            cm.get("si", 0), cm.get("parcial", 0), cm.get("nv", 0),
            "ok" if obs[0][0] == obs[0][1] and obs[2][0] == obs[2][1] and obs[4][0] == obs[4][1] else "DIFIERE",
            ce.get("si", 0), ce.get("parcial", 0), ce.get("nv", 0),
            "ok" if obs[1][0] == obs[1][1] and obs[3][0] == obs[3][1] and obs[5][0] == obs[5][1] else "DIFIERE"))
        vacias_m = cm.get("", 0)
        vacias_e = ce.get("", 0)
        if vacias_m or vacias_e:
            fallos += 1
            print("%-35s CELDAS SIN CODIGO: benchmark %d, ecuador %d" % ("", vacias_m, vacias_e))

    marcadas = sum(1 for f in filas_m + filas_e
                   for v in f.values() if isinstance(v, str) and v.endswith("*"))
    print("\nceldas corregidas tras la re-verificacion manual:", marcadas, "(esperado 2)")
    nuevas = sum(1 for f in filas_m + filas_e if f.get("nueva_2024") == "si")
    print("instituciones creadas en 2024 o despues:", nuevas)
    if fallos or marcadas != 2:
        sys.exit("\nVERIFICACION FALLIDA: la extraccion no reproduce las cifras esperadas.")
    print("\nverificacion completa: la extraccion reproduce todas las cifras esperadas.")


if __name__ == "__main__":
    main()
