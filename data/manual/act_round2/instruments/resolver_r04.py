# -*- coding: utf-8 -*-
"""resolver_r04.py - instrumento para cerrar 1.1.1 y 2.4.4 en la codificacion R04.

El recolector deja marcadas REVISAR las filas que la regla ACT remite al juicio
humano. Este script las extrae a una hoja de trabajo en texto plano, y despues
devuelve al CSV lo que el evaluador escriba en ella.

Extrae SOLO las filas que todavia deciden un veredicto de sitio. Si un criterio
ya falla en un sitio por otro elemento, ninguna fila pendiente de ese sitio puede
cambiar el veredicto y se deja marcada, que es la misma politica que sigue la
primera codificacion. Eso reduce el trabajo de 1351 filas a las que importan.

    python resolver_r04.py hoja
        Escribe hoja_r04_111.txt y hoja_r04_244.txt. Texto plano y no CSV a
        proposito: las justificaciones llevan comas, comillas y punto y coma, y
        una hoja de calculo las destroza.

    python resolver_r04.py fusionar CODIGO
        Valida las hojas rellenadas, escribe los resultados en los quince CSV de
        recoding/, y recalcula los veredictos de sitio. Aborta sin escribir nada
        si algun bloque esta incompleto o mal escrito.

Ejecutar desde data/manual/act_round2/recoding_evaluator2/.

El evaluador debe trabajar con ../instruments/EVALUATOR_DECISION_CRITERIA.md
delante, y sin consultar ninguna codificacion anterior.
"""
import csv
import glob
import io
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

DIR = "recoding"
DIR_EV = "image_evidence"
HOJAS = {"1.1.1": "hoja_r04_111.txt", "2.4.4": "hoja_r04_244.txt"}
VALIDOS = ("cumple", "falla")

CABECERA = """\
# ============================================================================
# HOJA DE RESOLUCION - criterio %s, filas remitidas al juicio humano
# ============================================================================
#
# En cada bloque escriba, despues de "RESULTADO:", una sola palabra:
#
#     cumple   el elemento satisface la expectativa de la regla
#     falla    no la satisface
#
# No hay categoria intermedia. No escriba "parcial" ni deje el campo vacio.
# Escriba siempre una frase despues de "JUSTIFICACION:".
#
# ---------------------------------------------------------------------------
%s#
# ---------------------------------------------------------------------------
# NO edite este archivo con Excel ni con ninguna hoja de calculo. Use un editor
# de texto: Bloc de notas, Notepad++, VS Code. Guarde en UTF-8.
#
# No modifique las lineas de datos ni las cabeceras "=== NNN | ... ===".
#
# Tenga delante ../instruments/EVALUATOR_DECISION_CRITERIA.md. No consulte
# ninguna codificacion anterior ni el borrador del articulo.
# ============================================================================

"""

AYUDA = {
    "1.1.1": """\
# REGLA qt1vmo - el nombre de la imagen es descriptivo
#
#   Pregunta: el nombre accesible sirve un proposito equivalente al de la imagen?
#
#   Juzguelo CONTRA LA IMAGEN. Abra la direccion que aparece en "imagen" y mirela.
#   Un nombre que describe algo distinto de lo que se ve, o que no describe nada
#   ("imagen", "foto", el nombre del fichero), no sirve ese proposito.
#
#   Cuando el bloque dice SIN URL DE IMAGEN, la imagen es un fondo CSS o un svg en
#   linea y no tiene direccion propia: localicela en la pagina por su selector.
#
#   Una imagen puramente decorativa deberia no tener nombre; si lo tiene y ese
#   nombre no aporta nada, la regla no se satisface.
""",
    "2.4.4": """\
# REGLA 5effbb - el enlace es descriptivo en su contexto
#
#   Pregunta: quien solo oyera el nombre accesible, y el contexto si lo hay,
#   sabria adonde lleva el enlace?
#
#   El contexto es una LISTA CERRADA de WCAG: el parrafo, el elemento de lista,
#   o la celda de tabla con su encabezado que contiene el enlace. Un div o un
#   article que envuelve la seccion NO es contexto, ni lo es un titular que este
#   fuera de esos elementos, ni el texto que se ve cerca en pantalla.
#
#   Cuando el bloque dice SIN CONTEXTO PROGRAMATICO, juzgue el nombre por si
#   solo: es lo unico que la regla le permite considerar.
#
# REGLA fd3a94 - nombres identicos, proposito equivalente
#
#   Varios enlaces comparten nombre y contexto pero llevan a destinos distintos.
#   Pregunta: sirven esos destinos el mismo proposito? Destinos distintos no
#   implican propositos distintos.
""",
}


def cargar():
    filas = []
    for f in sorted(glob.glob(os.path.join(DIR, "*.csv"))):
        with io.open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                r["_archivo"] = f
                filas.append(r)
    if not filas:
        sys.exit("no hay CSV en %s/. Ejecute el script desde "
                 "data/manual/act_round2/recoding_evaluator2/." % DIR)
    return filas


def pendientes_que_deciden(filas):
    """REVISAR de los pares sitio-criterio que aun no fallan por otro elemento."""
    falla = defaultdict(bool)
    for r in filas:
        if r["outcome"].strip() == "falla":
            falla[(r["abbr"], r["criterion"])] = True
    return [r for r in filas
            if r["outcome"].strip() == "REVISAR"
            and r["criterion"] in HOJAS
            and not falla[(r["abbr"], r["criterion"])]]


def cargar_evidencia():
    """La pasada de imagenes (act_images.js) recoge la direccion sin recortar. Se
    indexa por tres claves porque las dos pasadas enumeran los elementos por
    separado y la numeracion no siempre coincide: la pagina cambia entre
    ejecuciones por carruseles y carga diferida."""
    if not os.path.isdir(DIR_EV):
        return None
    filas = []
    for f in sorted(glob.glob(os.path.join(DIR_EV, "*.csv"))):
        with io.open(f, encoding="utf-8-sig", newline="") as fh:
            filas += list(csv.DictReader(fh))
    if not filas:
        return None
    idx = {"n": {}, "sel": defaultdict(list), "nom": defaultdict(list)}
    for r in filas:
        idx["n"][(r["abbr"], r["element_n"])] = r
        idx["sel"][(r["abbr"], r["selector"])].append(r)
        idx["nom"][(r["abbr"], r["accessible_name"].strip())].append(r)
    idx["_n"] = len(filas)
    return idx


def buscar_evidencia(idx, fila, nombre):
    """Devuelve (registro, via) o (None, None). Cascada: numero de elemento,
    despues selector, despues nombre accesible."""
    if not idx:
        return None, None
    e = idx["n"].get((fila["abbr"], fila["element_n"]))
    if e:
        return e, "elemento"
    c = idx["sel"].get((fila["abbr"], fila["selector_or_description"]), [])
    c2 = [x for x in c if x["accessible_name"].strip() == nombre]
    if c2 or c:
        return (c2 or c)[0], "selector"
    c = idx["nom"].get((fila["abbr"], nombre), [])
    if c:
        return c[0], "nombre"
    return None, None


def url_imagen(src, url_sitio):
    """El recolector recorta la nota por la izquierda, de modo que la direccion de
    la imagen puede llegar sin esquema ni servidor. Se reconstruye a partir del
    servidor del sitio y SOLO se acepta si el fragmento recibido es sufijo exacto
    de la direccion reconstruida; en caso contrario se marca como recortada y no
    se inventa nada."""
    if not src:
        return "", "sin-url"
    if src.startswith("http"):
        return src, "completa"
    host = urlparse(url_sitio).netloc
    if not host:
        return src, "recortada"
    if src.startswith("/"):
        return "https://" + host + src, "reconstruida"
    i = src.find("/")
    if i == -1:
        return src, "recortada"
    cand = "https://" + host + src[i:]
    return (cand, "reconstruida") if cand.endswith(src) else (src, "recortada")


def campo(notas, etiqueta):
    m = re.search(r'%s:\s*("?)(.*?)\1(?=\s*\|\s|\s*$)' % etiqueta, notas or "")
    return m.group(2).strip() if m else ""


def generar():
    filas = cargar()
    dec = pendientes_que_deciden(filas)
    if not dec:
        sys.exit("no queda ninguna fila pendiente que decida un veredicto.")
    estados = Counter()
    evidencia = cargar_evidencia()
    if evidencia:
        print("evidencia de imagen: %d filas en %s/" % (evidencia["_n"], DIR_EV))
    else:
        print("sin %s/: la direccion de imagen saldra de la nota, que viene recortada" % DIR_EV)
    for crit, nombre in HOJAS.items():
        sub = [r for r in dec if r["criterion"] == crit]
        if not sub:
            print("%s: nada pendiente, no se escribe hoja" % crit)
            continue
        s = io.StringIO()
        s.write(CABECERA % (crit, AYUDA[crit]))
        for i, r in enumerate(sub, 1):
            s.write("=== %03d | %s | elemento %s | regla %s ===\n"
                    % (i, r["abbr"], r["element_n"], r["act_rule"]))
            notas = r["notes"] or ""
            if r["act_rule"] == "fd3a94":
                s.write("enlaces con nombre y contexto identicos y destino distinto\n")
                destinos = campo(notas, "destinos")
                for d in [x.strip() for x in destinos.split("|") if x.strip()]:
                    s.write("   -> %s\n" % d)
            elif r["act_rule"] == "qt1vmo":
                nom = campo(notas, "nombre")
                s.write("nombre    : %s\n" % nom)
                ev, via = buscar_evidencia(evidencia, r, nom)
                if ev and ev["full_src"].strip():
                    u, estado = ev["full_src"].strip(), "completa"
                    if ev.get("css_width"):
                        s.write("mostrada  : %sx%s px" % (ev["css_width"], ev["css_height"]))
                        if ev.get("natural_width"):
                            s.write("   (original %sx%s)" % (ev["natural_width"], ev["natural_height"]))
                        s.write("\n")
                    if ev.get("containing_link", "").strip():
                        s.write("enlace    : %s\n" % ev["containing_link"].strip())
                    if ev.get("nearby_text", "").strip():
                        s.write("texto     : %s\n" % ev["nearby_text"].strip()[:160])
                else:
                    u, estado = url_imagen(campo(notas, "src"), r["url"])
                if estado == "completa":
                    s.write("imagen    : %s\n" % u)
                elif estado == "reconstruida":
                    s.write("imagen    : %s   [direccion reconstruida]\n" % u)
                elif estado == "recortada":
                    s.write("imagen    : DIRECCION RECORTADA, fragmento: %s\n" % u)
                    s.write("            localice la imagen en la pagina por su selector\n")
                else:
                    s.write("imagen    : SIN URL, es fondo CSS o svg en linea\n")
                    s.write("            localice la imagen en la pagina por su selector\n")
                s.write("pagina    : %s\n" % r["url"])
                s.write("selector  : %s\n" % r["selector_or_description"])
                estados[estado] += 1
            else:
                s.write("nombre    : %s\n" % campo(notas, "nombre"))
                s.write("destino   : %s\n" % campo(notas, "href"))
                ctx = (r["programmatic_context"] or "").strip()
                s.write("contexto  : %s\n" % (ctx if ctx else "SIN CONTEXTO PROGRAMATICO"))
            s.write("RESULTADO:\nJUSTIFICACION:\n\n")
        io.open(nombre, "w", encoding="utf-8", newline="").write(s.getvalue())
        print("escrito %s: %d bloques (%s)"
              % (nombre, len(sub), dict(Counter(r["abbr"] for r in sub))))
    print("\nTotal a resolver: %d filas de las %d marcadas REVISAR."
          % (len(dec), sum(1 for r in filas if r["outcome"].strip() == "REVISAR")))
    if estados:
        malas = estados["recortada"] + estados["sin-url"]
        print("\nDireccion de imagen en la hoja de 1.1.1:")
        for k in ("completa", "reconstruida", "recortada", "sin-url"):
            if estados[k]:
                print("   %-13s %d" % (k, estados[k]))
        if malas:
            print("\n   AVISO: %d de %d bloques no traen una direccion utilizable."
                  % (malas, sum(estados.values())))
            if evidencia:
                print("   Son elementos sin direccion propia, fondo CSS o svg en linea, o que la")
                print("   pasada de imagenes no llego a ver. Localicelos por su selector.")
            else:
                print("   Ejecute ../instruments/act_images.js en los sitios afectados y vuelva a")
                print("   generar la hoja: recoge la direccion sin recortar, el srcset, el fondo")
                print("   CSS y las dimensiones. Es el instrumento previsto para esto.")


def leer_hoja(nombre):
    if not os.path.isfile(nombre):
        return {}
    texto = io.open(nombre, encoding="utf-8-sig").read()
    trozos = re.split(r"(?m)^=== (\d{3}) \| ", texto)[1:]
    d = {}
    for n, cuerpo in zip(trozos[0::2], trozos[1::2]):
        res = re.search(r"(?m)^RESULTADO:[ \t]*(.*)$", cuerpo)
        jus = re.search(r"(?m)^JUSTIFICACION:[ \t]*(.*)$", cuerpo)
        d[int(n)] = (res.group(1).strip() if res else "",
                     jus.group(1).strip() if jus else "")
    return d


def fusionar(codigo):
    filas = cargar()
    dec = pendientes_que_deciden(filas)
    problemas = []
    resueltas = {}
    for crit, nombre in HOJAS.items():
        sub = [r for r in dec if r["criterion"] == crit]
        if not sub:
            continue
        hoja = leer_hoja(nombre)
        if not hoja:
            sys.exit("falta %s. Genere las hojas con: python resolver_r04.py hoja" % nombre)
        if len(hoja) != len(sub):
            sys.exit("%s tiene %d bloques y se esperaban %d"
                     % (nombre, len(hoja), len(sub)))
        for i, r in enumerate(sub, 1):
            res, jus = hoja[i]
            etq = "%s bloque %03d (%s #%s)" % (nombre, i, r["abbr"], r["element_n"])
            if res not in VALIDOS:
                problemas.append("  %s: RESULTADO = %r; debe ser cumple o falla" % (etq, res))
            elif not jus:
                problemas.append("  %s: JUSTIFICACION vacia" % etq)
            else:
                resueltas[id(r)] = (res, jus)
    if problemas:
        print("\n".join(problemas))
        sys.exit("\n%d bloques sin resolver o mal escritos. No se escribe nada."
                 % len(problemas))

    por_archivo = defaultdict(list)
    for r in filas:
        por_archivo[r["_archivo"]].append(r)
    escritas = 0
    for archivo, rs in sorted(por_archivo.items()):
        tocado = False
        for r in rs:
            if id(r) in resueltas:
                r["outcome"], jus = resueltas[id(r)]
                r["notes"] = ((r["notes"] or "") + " || RESUELTO %s: %s" % (codigo, jus)).strip()
                tocado = True
                escritas += 1
        if not tocado:
            continue
        campos = [c for c in rs[0].keys() if c != "_archivo"]
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=campos, lineterminator="\n",
                           quoting=csv.QUOTE_MINIMAL, extrasaction="ignore")
        w.writeheader()
        w.writerows(rs)
        io.open(archivo, "w", encoding="utf-8", newline="").write("\ufeff" + buf.getvalue())
        print("actualizado %s" % archivo)
    print("\n%d filas resueltas por %s" % (escritas, codigo))

    filas = cargar()
    falla = defaultdict(bool)
    pend = defaultdict(int)
    grupo = {}
    for r in filas:
        grupo[r["abbr"]] = r["group"]
        o = r["outcome"].strip()
        if o == "falla":
            falla[(r["abbr"], r["criterion"])] = True
        elif o == "REVISAR":
            pend[(r["abbr"], r["criterion"])] += 1
    print("\n=== veredictos de la codificacion %s tras la fusion ===" % codigo)
    for c in ("1.1.1", "1.4.3", "2.4.4"):
        for g in ("mundo", "ecuador"):
            sitios = sorted(s for s, gg in grupo.items() if gg == g)
            k = sum(1 for s in sitios if falla[(s, c)])
            abiertos = [s for s in sitios
                        if not falla[(s, c)] and pend[(s, c)]]
            print("  %s %-8s %d de %d no satisfacen%s"
                  % (c, g, k, len(sitios),
                     "" if not abiertos else "   (sin cerrar: %s)" % ", ".join(abiertos)))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("hoja", "fusionar"):
        sys.exit(__doc__)
    if sys.argv[1] == "hoja":
        generar()
    else:
        if len(sys.argv) < 3:
            sys.exit("indique el codigo de evaluador: python resolver_r04.py fusionar R04")
        fusionar(sys.argv[2])
