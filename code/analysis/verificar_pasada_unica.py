# -*- coding: utf-8 -*-
import json, re, math, statistics
from collections import Counter
from scipy import stats

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
RO = [re.compile(p) for p in ORIG]; RE_ = [re.compile(p) for p in ORIG + ADD]
def hit(ns, ps): return any(p.search(x) for x in ns for p in ps)

d = json.load(open("../../data/raw/accessibility/resultados.json", encoding="utf-8"))
G = {"Mundo": [x for x in d if x["grupo"] == "Mundo"],
     "Ecuador": [x for x in d if x["grupo"] == "Ecuador"]}

print("== Indicadores en vivo (Tabla 1) ==")
print("%-34s %10s %10s" % ("", "Benchmark", "Ecuador"))
def fila(nm, f):
    v = [sum(1 for x in G[g] if f(x)) for g in ("Mundo", "Ecuador")]
    print("%-34s %10s %10s" % (nm, "%d/63 (%.1f)" % (v[0], 100*v[0]/63),
                                    "%d/63 (%.1f)" % (v[1], 100*v[1]/63)))
    return v
tr_o = fila("Tracking (lista ORIGINAL)", lambda x: hit(x["cookies"]["nombres_pre"], RO))
tr_e = fila("Tracking (lista EXTENDIDA)", lambda x: hit(x["cookies"]["nombres_pre"], RE_))
fila("At least one cookie", lambda x: x["cookies"]["total_pre"] > 0)
fila("Consent banner shown", lambda x: bool(x["cookies"]["banner"]))
fila("CMP detected", lambda x: len(x["cookies"]["cmp"]) > 0)
fila("No level-A failure", lambda x: x["accesibilidad"]["porNivel"].get("A", 0) == 0)
fila("No failure at any level", lambda x: x["accesibilidad"]["violaciones"] == 0)
fila("Valid TLS certificate", lambda x: x["https"])

print("\n== Tabla 3 (WCAG) ==")
for g in ("Mundo", "Ecuador"):
    S = G[g]
    med = statistics.median([x["accesibilidad"]["violaciones"] for x in S])
    nodos = Counter()
    for x in S:
        for k, v in x["accesibilidad"]["porNivel"].items(): nodos[k] += v
    tot = sum(nodos.values())
    reglas = Counter()
    for x in S:
        for r in x["accesibilidad"]["reglas"]: reglas[r["criterio"]] += 1
    print(" %-8s mediana reglas=%s  nodos A/AA/AAA=%d/%d/%d  = %.0f%%/%.0f%%/%.0f%%" %
          (g, med, nodos["A"], nodos["AA"], nodos["AAA"],
           100*nodos["A"]/tot, 100*nodos["AA"]/tot, 100*nodos["AAA"]/tot))
    ren = nodos["A"] + nodos["AA"]
    print("          sin AAA: %.1f%% / %.1f%%" % (100*nodos["A"]/ren, 100*nodos["AA"]/ren))
    for c in ("2.4.4", "1.4.3", "1.1.1"):
        print("          %s: %d/63 = %.1f%%" % (c, reglas[c], 100*reglas[c]/63))

print("\n== Tabla 4 (RQ4) ==")
for g in ("Mundo", "Ecuador"):
    S = G[g]
    A = lambda x: x["accesibilidad"]["porNivel"].get("A", 0) == 0
    T = lambda x: hit(x["cookies"]["nombres_pre"], RO)
    c = [sum(1 for x in S if A(x) == a and T(x) == t) for a, t in ((1,0),(1,1),(0,0),(0,1))]
    orr = (c[0]*c[3])/(c[1]*c[2]) if c[1]*c[2] else float("nan")
    p = stats.fisher_exact([[c[0], c[1]], [c[2], c[3]]])[1]
    print(" %-8s A+T- %d  A+T+ %d  A-T- %d  A-T+ %d  OR=%.2f  p=%.3f" % (g, *c, orr, p))
rho, pr = stats.spearmanr([x["accesibilidad"]["nodos"] for x in d],
                          [len([n for n in x["cookies"]["nombres_pre"] if hit([n], RO)]) for x in d])
print(" Spearman global (nodos vs cookies de rastreo): rho=%.3f p=%.3f" % (rho, pr))
rho2, pr2 = stats.spearmanr([x["accesibilidad"]["violaciones"] for x in d],
                            [len([n for n in x["cookies"]["nombres_pre"] if hit([n], RO)]) for x in d])
print(" Spearman (violaciones vs cookies): rho=%.3f p=%.3f" % (rho2, pr2))
