# -*- coding: utf-8 -*-
import json, re, itertools, math
from collections import defaultdict
from scipy import stats

PAS = {"EC": [1,2,3], "EU": [1,2,3], "GB": [2,3,4], "US": [1,2,3]}
ORIG = [r"^_ga", r"^_gid$", r"^__utm", r"^_gcl_", r"^_gac_", r"^YSC$", r"^VISITOR_INFO",
        r"^IDE$", r"^test_cookie$", r"^_fbp$", r"^_fbc$", r"^fr$", r"^_tt_", r"^_ttp$",
        r"^_clck$", r"^_clsk$", r"^MUID$", r"^_uet", r"^personalization_id$", r"^_hj",
        r"^nmstat$", r"^_pk_", r"^pys", r"^_pin_", r"^AMCV_", r"^s_", r"^utag", r"^mbox",
        r"^Hm_lvt_", r"^Hm_lpvt_", r"^HMACCOUNT", r"^BAIDUID$", r"^__qca$", r"^_lc2_", r"^ln_or$"]
ADD = [r"^receive-cookie-deprecation$", r"^VISITOR_PRIVACY", r"^__Secure-YNID$",
       r"^__Secure-ROLLOUT", r"^DSID$", r"^ttcsid", r"^MR$", r"^SM$", r"^SRM_B$",
       r"^ANONCHK$", r"^CLID$", r"^bcookie$", r"^bscookie$", r"^lidc$", r"^li_sugr$",
       r"^li_gc$", r"^UserMatchHistory$", r"^AnalyticsSyncHistory$", r"^TapAd_",
       r"^sa-user-id", r"^_scid", r"^sc_at$", r"^muc_ads$", r"^_twpid$", r"^sbjs_", r"^_cs_"]
RO = [re.compile(p) for p in ORIG]
RE_ = [re.compile(p) for p in ORIG + ADD]

VENDOR = [
 ("Google Analytics/Ads", [r"^_ga", r"^_gid$", r"^__utm", r"^_gcl_", r"^_gac_"]),
 ("YouTube/DoubleClick", [r"^YSC$", r"^VISITOR_INFO", r"^VISITOR_PRIVACY", r"^__Secure-YNID$", r"^__Secure-ROLLOUT", r"^IDE$", r"^test_cookie$", r"^DSID$"]),
 ("Meta", [r"^_fbp$", r"^_fbc$", r"^fr$"]),
 ("TikTok", [r"^_tt_", r"^_ttp$", r"^ttcsid"]),
 ("Microsoft", [r"^_clck$", r"^_clsk$", r"^MUID$", r"^MR$", r"^SM$", r"^SRM_B$", r"^ANONCHK$", r"^CLID$", r"^_uet"]),
 ("LinkedIn", [r"^bcookie$", r"^bscookie$", r"^lidc$", r"^li_sugr$", r"^li_gc$", r"^UserMatchHistory$", r"^AnalyticsSyncHistory$"]),
 ("TapAd", [r"^TapAd_"]), ("StackAdapt", [r"^sa-user-id"]), ("Snapchat", [r"^_scid", r"^sc_at$"]),
 ("X/Twitter", [r"^muc_ads$", r"^personalization_id$", r"^_twpid$"]),
 ("Hotjar", [r"^_hj"]), ("Siteimprove", [r"^nmstat$"]), ("Matomo", [r"^_pk_"]),
 ("PixelYourSite/Sourcebuster", [r"^pys", r"^sbjs_"]), ("Pinterest", [r"^_pin_"]),
 ("Adobe/Tealium", [r"^AMCV_", r"^s_", r"^utag", r"^mbox"]), ("ContentSquare", [r"^_cs_"]),
 ("Baidu", [r"^Hm_lvt_", r"^Hm_lpvt_", r"^HMACCOUNT", r"^BAIDUID$"]),
 ("Quantcast", [r"^__qca$"]), ("LiveIntent", [r"^_lc2_", r"^ln_or$"]),
]
VEND = [(nm, [re.compile(p) for p in ps]) for nm, ps in VENDOR]
ALLVEND = [p for _, ps in VEND for p in ps]

def hit(names, pats): return any(p.search(x) for x in names for p in pats)

data = {}   # (vantage, run) -> {id: rec}
for v, runs in PAS.items():
    for r in runs:
        d = json.load(open("../../data/raw/tracking/resultados_%s_r%d.json" % (v, r), encoding="utf-8"))
        data[(v, r)] = {x["id"]: x for x in d if x.get("ok")}

ids_all = sorted(set.intersection(*[set(data[(v, r)]) for v in PAS for r in PAS[v]]))
print("Sitios con exito en las 12 pasadas:", len(ids_all))

def mayoria(vals):
    return sum(vals) * 2 > len(vals)

cons = {}   # (vantage, medida) -> {id: bool}
for v in PAS:
    for tag, pats in (("orig", RO), ("ext", RE_)):
        cons[(v, tag)] = {i: mayoria([hit(data[(v, r)][i]["cookies"]["nombres_pre"], pats)
                                      for r in PAS[v]]) for i in ids_all}

print("\n== Rastreo consolidado (regla de mayoria sobre 3 pasadas) ==")
for tag in ("orig", "ext"):
    print(" lista %-5s" % tag, {v: sum(cons[(v, tag)].values()) for v in ("EC", "US", "GB", "EU")})

def wilson(k, n, z=1.959963985):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * max(0, c - h), 100 * min(1, c + h)

N = len(ids_all)
print("\n== Proporciones (lista extendida) ==")
for v in ("EC", "US", "GB", "EU"):
    k = sum(cons[(v, "ext")].values())
    lo, hi = wilson(k, N)
    print("  %s  %d/%d = %.1f%%  IC95 %.1f-%.1f" % (v, k, N, 100 * k / N, lo, hi))

print("\n== McNemar exacto (lista extendida) ==")
pares = [("EC","EU"),("EC","GB"),("US","EU"),("US","GB"),("GB","EU"),("EC","US")]
res = []
for x, y in pares:
    a = b = c = d = 0
    for i in ids_all:
        px, py = cons[(x,"ext")][i], cons[(y,"ext")][i]
        if px and py: a += 1
        elif px and not py: b += 1
        elif not px and py: c += 1
        else: d += 1
    p = float(stats.binomtest(b, b + c, 0.5).pvalue) if b + c else 1.0
    res.append((x, y, a, b, c, d, p))
    print("  %s vs %s  a=%d b=%d c=%d d=%d  disc=%d  p=%.4f" % (x, y, a, b, c, d, b + c, p))

orden = sorted(range(6), key=lambda k: res[k][6])
adj = [0]*6; prev = 0
for rank, k in enumerate(orden):
    val = min(1.0, res[k][6] * (6 - rank)); val = max(val, prev); prev = val; adj[k] = val
print("\n== Holm (6 comparaciones) ==")
for k in orden:
    print("  %s vs %s  p=%.4f -> pH=%.3f" % (res[k][0], res[k][1], res[k][6], adj[k]))

# Cochran Q
tab = [[cons[(v,"ext")][i] for v in ("EC","EU","GB","US")] for i in ids_all]
kk = 4
G = [sum(col) for col in zip(*tab)]
L = [sum(row) for row in tab]
num = (kk - 1) * (kk * sum(g * g for g in G) - sum(G) ** 2)
den = kk * sum(L) - sum(l * l for l in L)
Q = num / den
print("\n== Cochran Q ==  Q=%.2f  gl=3  p=%.5f" % (Q, 1 - stats.chi2.cdf(Q, 3)))

print("\n== Controles de renderizado (media de violaciones WCAG por sitio) ==")
for v in ("EC","EU","GB","US"):
    m = sum(sum(data[(v,r)][i]["accesibilidad"]["violaciones"] for r in PAS[v]) / len(PAS[v]) for i in ids_all) / N
    print("  %s  %.3f" % (v, m))

print("\n== Proveedores: sitios con >=1 cookie, por punto de observacion ==")
print("  %-28s %5s %5s %5s %5s" % ("vendor", "EC", "US", "GB", "EU"))
for nm, pats in VEND:
    row = []
    for v in ("EC","US","GB","EU"):
        row.append(sum(1 for i in ids_all if mayoria([hit(data[(v,r)][i]["cookies"]["nombres_pre"], pats) for r in PAS[v]])))
    if max(row) > 0:
        print("  %-28s %5d %5d %5d %5d" % (nm, *row))

print("\n== Cookies NO atribuibles a proveedor (total, media por sitio) ==")
for v in ("EC","US","GB","EU"):
    tot = 0
    for i in ids_all:
        c = sum(len([x for x in data[(v,r)][i]["cookies"]["nombres_pre"] if not any(p.search(x) for p in ALLVEND)]) for r in PAS[v]) / len(PAS[v])
        tot += c
    print("  %s  %.1f" % (v, tot))

print("\n" + "="*72)
print("P0-N3: efecto de la taxonomia extendida en el punto de observacion EC")
print("="*72)
# por grupo, sobre TODOS los sitios con exito en las 3 pasadas EC
ids_ec = sorted(set.intersection(*[set(data[("EC", r)]) for r in PAS["EC"]]))
print("Sitios con exito en las 3 pasadas EC:", len(ids_ec))
for grupo in ("mundo", "ecuador"):
    sub = [i for i in ids_ec if data[("EC",1)][i]["grupo"] == grupo]
    o = sum(1 for i in sub if mayoria([hit(data[("EC",r)][i]["cookies"]["nombres_pre"], RO) for r in PAS["EC"]]))
    e = sum(1 for i in sub if mayoria([hit(data[("EC",r)][i]["cookies"]["nombres_pre"], RE_) for r in PAS["EC"]]))
    camb = [data[("EC",1)][i]["sigla"] for i in sub
            if mayoria([hit(data[("EC",r)][i]["cookies"]["nombres_pre"], RE_) for r in PAS["EC"]])
            != mayoria([hit(data[("EC",r)][i]["cookies"]["nombres_pre"], RO) for r in PAS["EC"]])]
    print("  %-8s n=%d  original=%d  extendida=%d  cambian: %s" % (grupo, len(sub), o, e, camb or "ninguno"))

print("\n-- por pasada individual EC (sin consolidar) --")
for r in PAS["EC"]:
    for grupo in ("mundo", "ecuador"):
        sub = [x for x in data[("EC",r)].values() if x["grupo"] == grupo]
        o = sum(1 for x in sub if hit(x["cookies"]["nombres_pre"], RO))
        e = sum(1 for x in sub if hit(x["cookies"]["nombres_pre"], RE_))
        print("   r%d %-8s n=%d  orig=%d  ext=%d" % (r, grupo, len(sub), o, e))

print("\n== Cookies de proveedor: total y caida respecto de EC ==")
tot = {}
for v in ("EC","US","GB","EU"):
    s = 0
    for i in ids_all:
        s += sum(len([x for x in data[(v,r)][i]["cookies"]["nombres_pre"]
                      if any(p.search(x) for p in ALLVEND)]) for r in PAS[v]) / len(PAS[v])
    tot[v] = s
for v in ("US","GB","EU"):
    print("  %s  %.1f  caida %.1f%%" % (v, tot[v], 100*(tot["EC"]-tot[v])/tot["EC"]))
print("  EC  %.1f" % tot["EC"])

print("\n== Estabilidad entre pasadas del indicador de rastreo (lista extendida) ==")
for v in ("EC","EU","GB","US"):
    rs = PAS[v]; acuerdos = []
    for a, b in itertools.combinations(rs, 2):
        ig = sum(1 for i in ids_all
                 if hit(data[(v,a)][i]["cookies"]["nombres_pre"], RE_) == hit(data[(v,b)][i]["cookies"]["nombres_pre"], RE_))
        acuerdos.append(100*ig/len(ids_all))
    print("  %s  %s" % (v, " ".join("%.1f%%" % x for x in acuerdos)))
