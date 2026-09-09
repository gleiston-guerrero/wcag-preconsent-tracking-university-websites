# -*- coding: utf-8 -*-
"""normalise_acronym.py - Corrige la sigla de la Universidad Del Pacifico
en todo el deposito: UPACIFICO con tilde -> UPACIFICO sin tilde.

Motivo. La institucion escribe su sigla sin tilde de forma consistente en su
documentacion oficial: el glosario de su Informe de Gestion 2018 la define como
"UPACIFICO: UNIVERSIDAD DEL PACIFICO ECUADOR", su plan estrategico se titula
PEDI-UPACIFICO-2018-2022, y su dominio es upacifico.edu.ec. La tilde corresponde
al nombre, Universidad del Pacifico, no a la sigla.

Alcance. La sigla es una ETIQUETA arrastrada desde el censo de entrada, no una
cantidad medida. Corregirla no altera ninguna observacion: las mediciones son
los recuentos de cookies, las violaciones WCAG y los campos derivados de ellos,
que este script no toca. Por eso la correccion puede aplicarse tambien a los
ficheros de results sin comprometer la integridad del registro.

Precaucion deliberada. Solo se sustituye la forma ACENTUADA. La forma sin tilde
ya aparece en los datos dentro del titulo de la pagina auditada ("UPACIFICO
Ecuador. Formacion Universitaria de calidad"), que es texto observado y no debe
tocarse. Al sustituir unicamente el token acentuado, ese texto queda intacto.

Uso, desde la raiz del repositorio:
    python code/analysis/normalise_acronym.py            # informe, no modifica
    python code/analysis/normalise_acronym.py --aplicar  # aplica los cambios

El script informa antes de tocar nada, y al aplicar verifica que no queda
ninguna ocurrencia acentuada y que ningun fichero ha cambiado de numero de
lineas.
"""

import os
import sys

ACENTUADA = "UPAC\u00cdFICO"
SIN_TILDE = "UPACIFICO"
EXCLUIR_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
EXTENSIONES = {".json", ".csv", ".html", ".md", ".tex", ".txt", ".cff"}


def ficheros(raiz="."):
    for root, dirs, files in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in EXCLUIR_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in EXTENSIONES:
                yield os.path.join(root, f)


def main():
    aplicar = "--aplicar" in sys.argv
    afectados = []
    for p in ficheros():
        try:
            with open(p, encoding="utf-8", newline="") as fh:
                texto = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        n = texto.count(ACENTUADA)
        if n:
            afectados.append((p, n, texto))

    total = sum(n for _, n, _ in afectados)
    print(f"ficheros afectados: {len(afectados)}   ocurrencias: {total}")
    for p, n, _ in sorted(afectados):
        print(f"  {n:4d}  {p}")

    if not aplicar:
        print("\nmodo informe. Ejecute con --aplicar para hacer los cambios.")
        return

    print()
    for p, n, texto in afectados:
        lineas_antes = texto.count("\n")
        nuevo = texto.replace(ACENTUADA, SIN_TILDE)
        if nuevo.count("\n") != lineas_antes:
            sys.exit(f"ABORTADO: {p} cambiaria de numero de lineas.")
        # se conserva el final de linea original escribiendo en modo binario
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(nuevo)
        print(f"  corregido  {p}  ({n})")

    # verificacion final
    restantes = sum(
        open(p, encoding="utf-8", errors="ignore", newline="").read().count(ACENTUADA)
        for p in ficheros()
    )
    if restantes:
        sys.exit(f"\nVERIFICACION FALLIDA: quedan {restantes} ocurrencias acentuadas.")
    print(f"\nverificacion: 0 ocurrencias acentuadas restantes; "
          f"{total} sustituciones en {len(afectados)} ficheros.")


if __name__ == "__main__":
    main()
