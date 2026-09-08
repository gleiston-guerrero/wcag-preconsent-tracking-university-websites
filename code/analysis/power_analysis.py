# -*- coding: utf-8 -*-
"""power_analysis.py - Reproduce las cuatro cantidades de power_analysis y tamano muestral
que reporta la Seccion 4.2 del articulo.

Ninguna cifra del articulo debe descansar en un calculo que el lector no pueda
rehacer. Este script existe por eso: se ejecuta sin argumentos, no lee ningun
fichero de datos, y su salida es exactamente lo que dice el texto.

Uso:
    python power_analysis.py

Requiere: scipy.

Proporciones observadas (Tabla 1, fila "Tracking cookies set", lista extendida):
    grupo de referencia  43/63 = 0.6825
    censo ecuatoriano    41/63 = 0.6508
    diferencia            3.2 puntos porcentuales
"""

import math
from scipy.stats import norm

P1 = 43 / 63          # grupo de referencia
P2 = 41 / 63          # censo ecuatoriano
P_BASE = (P1 + P2) / 2
ALPHA = 0.05
POWER = 0.80

z = lambda a: norm.ppf(1 - a)


def n_superioridad(p1, p2, alpha=ALPHA, power=POWER):
    """Tamano por grupo para DETECTAR una diferencia entre dos proporciones.

    Prueba bilateral de dos proporciones independientes, aproximacion normal
    con varianza agrupada bajo la hipotesis nula y varianza no agrupada bajo la
    alternativa. Es la formula estandar de Fleiss sin correccion de continuidad.
    """
    pbar = (p1 + p2) / 2
    num = (z(alpha / 2) * math.sqrt(2 * pbar * (1 - pbar))
           + z(1 - power) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return num / (p1 - p2) ** 2


def minima_diferencia_detectable(n=63, p=P_BASE, alpha=ALPHA, power=POWER):
    """Menor diferencia que el diseno detecta con la power_analysis declarada.

    Se resuelve por biseccion sobre n_superioridad, que es monotona en la
    diferencia. No hay forma cerrada porque la varianza depende de la propia
    diferencia.
    """
    lo, hi = 1e-4, 0.6
    for _ in range(200):
        mid = (lo + hi) / 2
        if n_superioridad(p + mid / 2, p - mid / 2, alpha, power) <= n:
            hi = mid
        else:
            lo = mid
    return hi


def n_equivalencia(delta, diferencia_verdadera, p=P_BASE, alpha=ALPHA, power=POWER):
    """Tamano por grupo para ESTABLECER equivalencia dentro de +-delta (TOST).

    Dos pruebas unilaterales al nivel alpha. La power_analysis la gobierna la holgura
    entre el margen y la diferencia verdadera supuesta, de modo que el resultado
    es muy sensible a ese supuesto: por eso el articulo reporta dos valores y
    no uno.
    """
    varianza = 2 * p * (1 - p)
    holgura = delta - abs(diferencia_verdadera)
    if holgura <= 0:
        raise ValueError("la diferencia verdadera supuesta no cabe dentro del margen")
    return varianza * (z(alpha) + z(1 - power)) ** 2 / holgura ** 2


if __name__ == "__main__":
    d_obs = P1 - P2
    print("Proporciones observadas")
    print(f"  referencia 43/63 = {P1:.4f}   Ecuador 41/63 = {P2:.4f}"
          f"   diferencia = {100 * d_obs:.1f} pp")
    print(f"  proporcion base usada en los calculos: {P_BASE:.4f}")
    print(f"  alfa = {ALPHA}, power_analysis = {POWER:.0%}\n")

    mdd = minima_diferencia_detectable()
    n_det = n_superioridad(P1, P2)
    n_nula = n_equivalencia(0.10, 0.0)
    n_obs = n_equivalencia(0.10, d_obs)

    print("Seccion 4.2 del articulo")
    print(f"  menor diferencia detectable con n=63 por grupo ......... {100 * mdd:.1f} pp")
    print(f"  n por grupo para detectar la diferencia observada ...... {math.ceil(n_det):,}")
    print(f"  n por grupo para equivalencia +-10 pp, diferencia nula .. {math.ceil(n_nula):,}")
    print(f"  n por grupo para equivalencia +-10 pp, diferencia 3.2 pp  {math.ceil(n_obs):,}")

    esperado = {"mdd": 23.3, "n_det": 3461, "n_nula": 275, "n_obs": 590}
    obtenido = {"mdd": round(100 * mdd, 1), "n_det": math.ceil(n_det),
                "n_nula": math.ceil(n_nula), "n_obs": math.ceil(n_obs)}
    if obtenido == esperado:
        print("\nverificacion: las cuatro cifras coinciden con las reportadas en el articulo.")
    else:
        print(f"\nVERIFICACION FALLIDA: esperado {esperado}, obtenido {obtenido}")
        raise SystemExit(1)
