# -*- coding: utf-8 -*-
"""
Kappa de Cohen para la validacion manual WCAG.

Entrada : data/wcag_kappa_pairs.csv
Salida  : acuerdo observado, acuerdo esperado y kappa, sin ponderar y con
          pesos lineales sobre el orden 0 < P < 1.

Uso: python kappa_wcag.py [ruta_csv]
"""
import csv
import sys

CATEGORIAS = ["0", "P", "1"]
ORDEN = {"0": 0, "P": 1, "1": 2}


def peso_lineal(a, b):
    return 1 - abs(ORDEN[a] - ORDEN[b]) / (len(CATEGORIAS) - 1)


def kappa(pares, peso=None):
    n = len(pares)
    if n == 0:
        raise ValueError("no hay pares")
    po = sum(1.0 if a == b else (0.0 if peso is None else peso(a, b)) for a, b in pares) / n
    ma = {c: sum(1 for a, _ in pares if a == c) for c in CATEGORIAS}
    mb = {c: sum(1 for _, b in pares if b == c) for c in CATEGORIAS}
    pe = sum(
        (1.0 if x == y else (0.0 if peso is None else peso(x, y))) * ma[x] * mb[y] / (n * n)
        for x in CATEGORIAS
        for y in CATEGORIAS
    )
    return po, pe, (po - pe) / (1 - pe), ma, mb


def cargar(ruta, solo_admisibles=True):
    pares = []
    with open(ruta, encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            if solo_admisibles and fila["entra_en_kappa"] != "si":
                continue
            pares.append((fila["codigo_primera"], fila["codigo_segunda"]))
    return pares


def informe(pares, titulo):
    po, pe, k, ma, mb = kappa(pares)
    po_w, pe_w, k_w, _, _ = kappa(pares, peso_lineal)
    print(titulo)
    print(f"  pares          {len(pares)}")
    print(f"  coincidencias  {sum(1 for a, b in pares if a == b)}")
    print(f"  po             {po:.4f}")
    print(f"  pe             {pe:.4f}")
    print(f"  kappa          {k:.4f}")
    print(f"  kappa lineal   {k_w:.4f}")
    print(f"  marginales     primera {ma}  segunda {mb}")
    print()


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "../data/wcag_kappa_pairs.csv"
    informe(cargar(ruta, True), "Escenario adoptado: se excluye el par con evidencia contradictoria")
    informe(cargar(ruta, False), "Escenario alternativo: los quince pares tal como se entregaron")
