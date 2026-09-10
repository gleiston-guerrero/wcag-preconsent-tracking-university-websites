# -*- coding: utf-8 -*-
"""cerrar_revisar.py - panorama y cierre de las filas marcadas REVISAR.

Distingue tres poblaciones, porque tratarlas igual seria un error:

  A. Filas que DECIDEN un veredicto de sitio y siguen sin resolver.
     Son las unicas que cambian una cifra del articulo.

  B. Filas remitidas al juicio humano cuyo criterio YA falla en ese sitio por
     otro elemento. La politica declarada del deposito las deja marcadas: su
     resultado no puede alterar ningun veredicto.

  C. Filas de la segunda codificacion, que debe resolver el segundo evaluador
     y no el primer autor, porque de su independencia depende la estimacion de
     fiabilidad entre codificadores.

Uso, desde la raiz del repositorio:

    python cerrar_revisar.py                 panorama, no escribe nada
    python cerrar_revisar.py hoja            escribe hoja_cierre_r02.txt con
                                             las filas del grupo A de la
                                             primera codificacion
    python cerrar_revisar.py fusionar CODIGO valida la hoja y anade las filas
                                             resueltas a qt1vmo_345_resolved.csv
                                             con ese codigo de evaluador
"""
import csv
import datetime
import glob
import io
import os
import re
import sys
from collections import Counter, defaultdict

R02 = "data/manual/act_round2"
R04 = "data/manual/act_round2/recoding_evaluator2"
RESUELTO = os.path.join(R02, "qt1vmo_345_resolved.csv")
HOJA = "hoja_cierre_r02.txt"
CRITERIOS = ("1.1.1", "1.4.3", "2.4.4")
VALIDOS = ("cumple", "falla")


def morir(m):
    print("\n*** " + m)
    sys.exit(1)


def filas(ruta):
    if not os.path.isfile(ruta):
        return []
    with io.open(ruta, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def cargar(base, sub="recoding"):
    d = os.path.join(base, sub)
    if not os.path.isdir(d):
        morir("no existe %s (ejecute desde la raiz del repositorio)" % d)
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.csv"))):
        for r in filas(f):
            r["_archivo"] = f
            out.append(r)
    return out


def campo(notas, etiqueta):
    m = re.search(r'%s:\s*("?)(.*?)\1(?=\s*\|\s|\s*$)' % etiqueta, notas or "")
    return m.group(2).strip() if m else ""


def estado(rec, extra):
    """falla / pendiente / cumple por sitio y criterio, uniendo fuentes extra."""
    falla, rev, grupo = defaultdict(bool), defaultdict(int), {}
    for r in rec:
        grupo[r["abbr"]] = r["group"]
        o = r["outcome"].strip()
        if o == "falla":
            falla[(r["abbr"], r["criterion"])] = True
        elif o == "REVISAR":
            rev[(r["abbr"], r["criterion"])] += 1
    for r in extra:
        c = (r.get("criterion") or "1.1.1").strip() or "1.1.1"
        o = (r.get("outcome") or r.get("outcome_TOFILL") or "").strip()
        if not o:
            continue
        if o == "falla":
            falla[(r["abbr"], c)] = True
        rev[(r["abbr"], c)] = max(0, rev[(r["abbr"], c)] - 1)
    return falla, rev, grupo


def ya_resueltos(base):
    """Elementos con veredicto en los ficheros de resolucion.

    Comprobar esto es imprescindible y faltaba: una fila puede seguir marcada
    REVISAR en recoding/ y tener ya su veredicto en qt1vmo_345_resolved.csv,
    porque las resoluciones se depositan aparte. Sin esta comprobacion el grupo
    A incluia elementos ya juzgados y la fusion los escribia duplicados.
    """
    hecho = set()
    for nombre in ("qt1vmo_345_resolved.csv", "review_282_rows.csv"):
        for r in filas(os.path.join(base, nombre)):
            o = (r.get("outcome") or r.get("outcome_TOFILL") or "").strip()
            if o in ("cumple", "falla"):
                hecho.add((r["abbr"], (r.get("criterion") or "1.1.1").strip(),
                           r["element_n"]))
    return hecho


def grupo_a(rec, falla, hecho=frozenset()):
    """REVISAR que todavia deciden un veredicto y no estan ya resueltas."""
    return [r for r in rec
            if r["outcome"].strip() == "REVISAR"
            and not falla[(r["abbr"], r["criterion"])]
            and (r["abbr"], r["criterion"], r["element_n"]) not in hecho]


def indexar(directorio):
    """Indexa una carpeta de evidencia de imagen. Se guardan listas por clave,
    no una sola fila, porque en las rejillas y los carruseles muchos elementos
    comparten el mismo selector."""
    idx = {"n": {}, "sel": defaultdict(list), "abbr": defaultdict(list)}
    n = 0
    for f in sorted(glob.glob(os.path.join(directorio, "*.csv"))):
        for r in filas(f):
            n += 1
            idx["n"][(r["abbr"], r["element_n"])] = r
            idx["sel"][(r["abbr"], r.get("selector", ""))].append(r)
            idx["abbr"][r["abbr"]].append(r)
    idx["_n"] = n
    return idx if n else None


def evidencia_r02():
    return indexar(os.path.join(R02, "image_evidence"))


def evidencia_r04():
    """Evidencia de la segunda recogida. Solo se usa emparejando por NOMBRE
    ACCESIBLE, nunca por numero de elemento ni por selector: entre dos recogidas
    la rejilla rota y la posicion no designa el mismo elemento, mientras que el
    texto alternativo viaja con la imagen."""
    return indexar(os.path.join(R04, "image_evidence"))


def emparejar_evidencia(ev, fila, nombre):
    """Devuelve (registro, via) o (None, motivo).

    El nombre accesible que llega en la nota viene RECORTADO por el recolector,
    de modo que se compara por prefijo. Solo se acepta un emparejamiento cuando
    identifica UNA sola fila: ante varios candidatos se prefiere no ofrecer
    imagen antes que ofrecer la equivocada, que es lo que hacia la version
    anterior de este script en las rejillas de selector repetido.
    """
    if not ev:
        return None, "sin evidencia de imagen"

    def por_nombre(cands):
        if not nombre:
            return []
        pref = nombre.rstrip()
        return [c for c in cands
                if (c.get("accessible_name") or "").strip().startswith(pref)]

    # 1. numero de elemento, y solo si el nombre no lo desmiente
    e = ev["n"].get((fila["abbr"], fila["element_n"]))
    if e:
        if not nombre or por_nombre([e]):
            return e, "elemento"

    # 2. selector, exigiendo que el nombre desambigue
    cands = ev["sel"].get((fila["abbr"], fila["selector_or_description"]), [])
    if cands:
        c2 = por_nombre(cands)
        if len(c2) == 1:
            return c2[0], "selector y nombre"
        if len(cands) == 1 and not nombre:
            return cands[0], "selector unico"
        if len(c2) > 1:
            return None, "AMBIGUO: %d filas con el mismo selector y nombre" % len(c2)

    # 3. nombre solo, en todo el sitio
    c3 = por_nombre(ev["abbr"].get(fila["abbr"], []))
    if len(c3) == 1:
        return c3[0], "nombre"
    if len(c3) > 1:
        return None, "AMBIGUO: %d filas con ese nombre accesible" % len(c3)
    return None, "sin emparejar en la evidencia"


def emparejar_segunda(ev4, fila, nombre):
    """Ultimo recurso: la evidencia de la segunda recogida, SOLO por nombre."""
    if not ev4 or not nombre:
        return None, "sin evidencia de la segunda recogida"
    pref = nombre.rstrip()
    c = [x for x in ev4["abbr"].get(fila["abbr"], [])
         if (x.get("accessible_name") or "").strip().startswith(pref)]
    if len(c) == 1:
        return c[0], "nombre, evidencia de la segunda recogida"
    if len(c) > 1:
        return None, "AMBIGUO en la segunda recogida: %d filas" % len(c)
    return None, "sin emparejar en ninguna de las dos recogidas"


def panorama():
    rec2 = cargar(R02)
    res = filas(RESUELTO)
    rev282 = filas(os.path.join(R02, "review_282_rows.csv"))
    f2, r2, g2 = estado(rec2, res + rev282)
    a2 = grupo_a(rec2, f2, ya_resueltos(R02))

    print("PRIMERA CODIFICACION  (recoding/, 8 de septiembre)")
    print("-" * 74)
    print("  filas totales                        %5d" % len(rec2))
    print("  marcadas REVISAR                     %5d" % sum(1 for r in rec2 if r["outcome"].strip() == "REVISAR"))
    print("  resueltas en qt1vmo_345_resolved.csv %5d" % len(res))
    print("  resueltas en review_282_rows.csv     %5d"
          % sum(1 for r in rev282 if (r.get("outcome_TOFILL") or "").strip()))
    print("\n  GRUPO A - REVISAR que todavia deciden un veredicto: %d" % len(a2))
    for (s, c), n in sorted(Counter((r["abbr"], r["criterion"]) for r in a2).items()):
        print("     %-13s %-7s %3d filas   (regla %s)"
              % (s, c, n, ", ".join(sorted({r["act_rule"] for r in a2
                                            if r["abbr"] == s and r["criterion"] == c}))))
    celdas = [(s, c) for s in g2 for c in CRITERIOS]
    abiertas = [(s, c) for s, c in celdas if not f2[(s, c)] and r2[(s, c)] > 0]
    print("\n  celdas de sitio por criterio: %d | cerradas %d | abiertas %d"
          % (len(celdas), len(celdas) - len(abiertas), len(abiertas)))
    for s, c in abiertas:
        print("     abierta: %s %s" % (s, c))

    if os.path.isdir(os.path.join(R04, "recoding")):
        rec4 = cargar(R04)
        f4, r4, g4 = estado(rec4, [])
        a4 = grupo_a(rec4, f4)
        print("\nSEGUNDA CODIFICACION  (recoding_evaluator2/, 9 de septiembre)")
        print("-" * 74)
        print("  filas totales                        %5d" % len(rec4))
        print("  marcadas REVISAR                     %5d"
              % sum(1 for r in rec4 if r["outcome"].strip() == "REVISAR"))
        print("\n  GRUPO C - las que debe resolver el segundo evaluador: %d" % len(a4))
        for c, n in sorted(Counter(r["criterion"] for r in a4).items()):
            print("     criterio %-7s %3d filas" % (c, n))
        print("     (estan en las hojas hoja_r04_111.txt y hoja_r04_244.txt)")

    tot_b = (sum(1 for r in rec2 if r["outcome"].strip() == "REVISAR") - len(a2))
    print("\nGRUPO B - REVISAR cuyo criterio ya falla por otro elemento: %d en la" % tot_b)
    print("primera codificacion. La politica del deposito las deja marcadas: su")
    print("resultado no puede cambiar ningun veredicto ni ninguna cifra del articulo.")


CABECERA = """\
# ============================================================================
# CIERRE DE LA PRIMERA CODIFICACION - filas que aun deciden un veredicto
# ============================================================================
#
# Escriba en cada bloque, despues de "RESULTADO:", una sola palabra:
#
#     cumple   el nombre accesible sirve un proposito equivalente a la imagen
#     falla    no lo sirve
#
# No hay categoria intermedia. Escriba siempre una frase tras "JUSTIFICACION:".
#
# ---------------------------------------------------------------------------
# REGLA qt1vmo - el nombre de la imagen es descriptivo
#
#   Juzguelo CONTRA LA IMAGEN: abra la direccion de la linea "imagen".
#   Un nombre que describe algo distinto de lo que se ve, o que no describe
#   nada (el nombre del fichero, "imagen", "foto"), no sirve ese proposito.
#   Si la imagen esta dentro de un enlace, el nombre debe servir el proposito
#   del ENLACE y no solo describir la fotografia.
#
# ---------------------------------------------------------------------------
# NO edite este archivo con Excel. Use un editor de texto y guarde en UTF-8.
# No modifique las lineas de datos ni las cabeceras "=== NNN | ... ===".
# ============================================================================

"""


def hoja():
    rec2 = cargar(R02)
    res = filas(RESUELTO)
    rev282 = filas(os.path.join(R02, "review_282_rows.csv"))
    f2, _, _ = estado(rec2, res + rev282)
    a2 = grupo_a(rec2, f2, ya_resueltos(R02))
    if not a2:
        print("No queda ninguna fila que decida un veredicto. Nada que hacer.")
        return
    ev = evidencia_r02()
    ev4 = evidencia_r04()
    print("evidencia de imagen: primera recogida %s | segunda %s"
          % ("%d filas" % ev["_n"] if ev else "no disponible",
             "%d filas" % ev4["_n"] if ev4 else "no disponible"))
    vias = Counter()
    sin = []
    s = io.StringIO()
    s.write(CABECERA)
    for i, r in enumerate(a2, 1):
        s.write("=== %03d | %s | elemento %s | criterio %s | regla %s ===\n"
                % (i, r["abbr"], r["element_n"], r["criterion"], r["act_rule"]))
        nom = campo(r["notes"], "nombre")
        s.write("nombre    : %s\n" % nom)
        e, via = emparejar_evidencia(ev, r, nom)
        if not (e and (e.get("full_src") or "").strip()):
            e2, via2 = emparejar_segunda(ev4, r, nom)
            if e2 and (e2.get("full_src") or "").strip():
                e, via = e2, via2
        if e and (e.get("full_src") or "").strip():
            s.write("imagen    : %s\n" % e["full_src"].strip())
            if "segunda recogida" in via:
                s.write("            [direccion tomada de la recogida del 9 de septiembre,\n")
                s.write("             emparejada por el nombre accesible]\n")
            vias[via] += 1
            if e.get("css_width"):
                s.write("mostrada  : %sx%s px" % (e["css_width"], e["css_height"]))
                if e.get("natural_width"):
                    s.write("   (original %sx%s)" % (e["natural_width"], e["natural_height"]))
                s.write("\n")
            if (e.get("containing_link") or "").strip():
                s.write("enlace    : %s\n" % e["containing_link"].strip())
            if (e.get("nearby_text") or "").strip():
                s.write("texto     : %s\n" % e["nearby_text"].strip()[:160])
        else:
            src = campo(r["notes"], "src")
            s.write("imagen    : SIN DIRECCION FIABLE (%s)\n" % via)
            if src:
                s.write("            fragmento recortado por el recolector: %s\n" % src)
            s.write("            localice la imagen en la pagina por su selector\n")
            vias[via] += 1
            sin.append("%03d  %s #%s  %s" % (i, r["abbr"], r["element_n"], nom[:60]))
        s.write("pagina    : %s\n" % r["url"])
        s.write("selector  : %s\n" % r["selector_or_description"])
        s.write("RESULTADO:\nJUSTIFICACION:\n\n")
    io.open(HOJA, "w", encoding="utf-8", newline="").write(s.getvalue())
    print("escrito %s con %d bloques: %s"
          % (HOJA, len(a2), dict(Counter("%s %s" % (r["abbr"], r["criterion"]) for r in a2))))
    print("\nComo se emparejo la imagen de cada bloque:")
    for k, v in vias.most_common():
        print("   %-46s %d" % (k, v))
    if sin:
        print("\n   %d bloques SIN direccion fiable:" % len(sin))
        for x in sin:
            print("      " + x)
        print("   No los juzgue contra una imagen que el script no ha identificado:")
        print("   localicelos en la pagina por su selector, o vuelva a pasar")
        print("   act_images.js por ese sitio.")
    # Comprobacion: ninguna direccion debe aparecer en dos bloques distintos.
    srcs = re.findall(r"(?m)^imagen    : (https?://\S+)$", s.getvalue())
    rep = [u for u, n in Counter(srcs).items() if n > 1]
    if rep:
        print("\n   AVISO: %d direccion(es) aparecen en mas de un bloque:" % len(rep))
        for u in rep:
            print("      %s" % u)
        print("   Revise esos bloques antes de juzgarlos: un mismo fichero de imagen")
        print("   con dos nombres accesibles distintos es un hallazgo o un error de")
        print("   emparejamiento, y hay que distinguir cual de los dos es.")


def fusionar(codigo):
    rec2 = cargar(R02)
    res = filas(RESUELTO)
    rev282 = filas(os.path.join(R02, "review_282_rows.csv"))
    f2, _, _ = estado(rec2, res + rev282)
    a2 = grupo_a(rec2, f2, ya_resueltos(R02))
    if not os.path.isfile(HOJA):
        morir("falta %s. Genere la hoja con: python cerrar_revisar.py hoja" % HOJA)
    texto = io.open(HOJA, encoding="utf-8-sig").read()
    trozos = re.split(r"(?m)^=== (\d{3}) \| ", texto)[1:]
    d = {}
    for n, cuerpo in zip(trozos[0::2], trozos[1::2]):
        m1 = re.search(r"(?m)^RESULTADO:[ \t]*(.*)$", cuerpo)
        m2 = re.search(r"(?m)^JUSTIFICACION:[ \t]*(.*)$", cuerpo)
        d[int(n)] = ((m1.group(1).strip() if m1 else ""), (m2.group(1).strip() if m2 else ""))
    if len(d) != len(a2):
        morir("la hoja tiene %d bloques y se esperaban %d" % (len(d), len(a2)))
    problemas = []
    for i, r in enumerate(a2, 1):
        v, j = d[i]
        if v not in VALIDOS:
            problemas.append("  bloque %03d (%s #%s): RESULTADO = %r" % (i, r["abbr"], r["element_n"], v))
        elif not j:
            problemas.append("  bloque %03d (%s #%s): JUSTIFICACION vacia" % (i, r["abbr"], r["element_n"]))
    if problemas:
        print("\n".join(problemas))
        morir("%d bloques sin resolver o mal escritos. No se escribe nada." % len(problemas))

    if not res:
        morir("no encuentro %s" % RESUELTO)
    campos = list(res[0].keys())
    hoy = datetime.date.today().isoformat()
    nuevas = []
    for i, r in enumerate(a2, 1):
        v, j = d[i]
        fila = {k: "" for k in campos}
        for k, orig in (("id", "id"), ("group", "group"), ("abbr", "abbr"),
                        ("criterion", "criterion"), ("act_rule", "act_rule"),
                        ("element_n", "element_n")):
            if k in fila:
                fila[k] = r.get(orig, "")
        if "selector" in fila:
            fila["selector"] = r["selector_or_description"]
        if "accessible_name" in fila:
            fila["accessible_name"] = campo(r["notes"], "nombre")
        if "outcome" in fila:
            fila["outcome"] = v
        if "justification" in fila:
            fila["justification"] = j
        if "evaluator_code" in fila:
            fila["evaluator_code"] = codigo
        if "date" in fila:
            fila["date"] = hoy
        nuevas.append(fila)

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=campos, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(res + nuevas)
    io.open(RESUELTO, "w", encoding="utf-8", newline="").write("\ufeff" + buf.getvalue())
    print("%s: %d filas (%d anteriores + %d nuevas con codigo %s)"
          % (RESUELTO, len(res) + len(nuevas), len(res), len(nuevas), codigo))
    print("\nEjecute ahora:")
    print("   python comprobar_brecha.py")
    print("para recalcular los veredictos y comprobar que no queda ninguna celda abierta.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        panorama()
    elif sys.argv[1] == "hoja":
        hoja()
    elif sys.argv[1] == "fusionar":
        if len(sys.argv) < 3:
            morir("indique el codigo de evaluador: python cerrar_revisar.py fusionar R01")
        fusionar(sys.argv[2])
    else:
        sys.exit(__doc__)
