# -*- coding: utf-8 -*-
"""Layer at which each vendor's pre-consent cookie is decided, by vantage point.

Reads the extended five-vantage campaign of 16 August 2026 (instrument v3.0,
data/raw/tracking_extended/), which records, for every site and pass, both the
cookie jar before any consent interaction and the network requests sent to each
vendor family.

For every site, vantage point and vendor family the three passes are consolidated
by majority:
    C  at least one cookie of the family is present (extended taxonomy, by name)
    R  the browser sent at least one request to a domain of the family

Reading, for a site at which the family sets a cookie from Ecuador:
    at the comparison vantage point, R and not C  -> decided by the VENDOR
        (its code ran and did not set the cookie)
    at the comparison vantage point, not R        -> decided UPSTREAM of the vendor
        (the site, its consent platform, its tag manager or another third party
         that would have called the vendor did not send the request)
    at the comparison vantage point, C            -> not suppressed

Only sites with at least two valid passes at all five vantage points enter.

Outputs
    data/processed/vendor_layer_by_site.csv    one row per site, family and vantage
    data/processed/vendor_layer_summary.csv    one row per family and vantage
    data/processed/tracking_extended_sites.csv site-level tracking by vantage
and prints the site-level Cochran Q and exact McNemar tests of the campaign.
"""
import csv, json, os, re, itertools
from math import comb
from scipy.stats import chi2

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RAW = os.path.join(ROOT, "data", "raw", "tracking_extended")
OUT = os.path.join(ROOT, "data", "processed")
VANTAGES = ["EC", "US", "EU", "GB", "CH"]
RUNS = (1, 2, 3)

COOKIE = {
    "Microsoft": [r"^_clck$", r"^_clsk$", r"^MUID$", r"^MR$", r"^SM$", r"^SRM_B$", r"^ANONCHK$", r"^CLID$", r"^_uet"],
    "LinkedIn": [r"^bcookie$", r"^bscookie$", r"^lidc$", r"^li_sugr$", r"^li_gc$", r"^UserMatchHistory$", r"^AnalyticsSyncHistory$"],
    "TapAd": [r"^TapAd_"],
    "StackAdapt": [r"^sa-user-id"],
    "Meta": [r"^_fbp$", r"^_fbc$", r"^fr$"],
    "Google Analytics": [r"^_ga", r"^_gid$", r"^__utm"],
}
NETWORK = {
    "Microsoft": {"Microsoft Clarity", "Microsoft Ads/UET"},
    "LinkedIn": {"LinkedIn"},
    "TapAd": {"TapAd"},
    "StackAdapt": {"StackAdapt"},
    "Meta": {"Meta"},
    "Google Analytics": {"Google Analytics"},
}
PATS = {f: [re.compile(p) for p in ps] for f, ps in COOKIE.items()}


def load():
    obs, ok, track, info = {}, {}, {}, {}
    for v in VANTAGES:
        for r in RUNS:
            with open(os.path.join(RAW, f"results_{v}_r{r}.json"), encoding="utf-8") as h:
                for s in json.load(h):
                    key = (s["sigla"], v)
                    info[s["sigla"]] = (s["id"], s["grupo"], s["pais"])
                    ok.setdefault(key, []).append(bool(s.get("ok")))
                    if not s.get("ok"):
                        continue
                    ck = s["cookies"]
                    names = set(ck.get("nombres_pre") or []) | set(ck.get("nombres_rastreo_ext") or [])
                    sent = {q["proveedor"] for q in (s.get("red_proveedores") or []) if q.get("peticion_emitida")}
                    fams_c = {f for f, ps in PATS.items() if any(p.search(n) for p in ps for n in names)}
                    fams_r = {f for f, ns in NETWORK.items() if ns & sent}
                    obs.setdefault(key, []).append((fams_c, fams_r, bool(ck.get("cmp"))))
                    track.setdefault(key, []).append(ck.get("rastreo_pre_ext", 0) > 0)
    return obs, ok, track, info


def majority(values):
    return sum(values) * 2 > len(values)


def exact_mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n)


def main():
    obs, ok, track, info = load()
    sites = sorted({k[0] for k in ok})
    kept = [x for x in sites if all(sum(ok[(x, v)]) >= 2 for v in VANTAGES)]
    print(f"sites with at least two valid passes at all five vantage points: {len(kept)} of {len(sites)}")
    print("excluded:", ", ".join(x for x in sites if x not in kept))

    rows, summary = [], []
    for fam in COOKIE:
        focal = [x for x in kept if majority([fam in o[0] for o in obs[(x, "EC")]])]
        for v in VANTAGES:
            n_c = n_vendor = n_upstream = 0
            for x in kept:
                o = obs[(x, v)]
                c = majority([fam in q[0] for q in o])
                r = majority([fam in q[1] for q in o])
                cmp_ = majority([q[2] for q in o])
                if x in focal:
                    if c:
                        n_c += 1; layer = "cookie_set"
                    elif r:
                        n_vendor += 1; layer = "vendor"
                    else:
                        n_upstream += 1; layer = "upstream"
                else:
                    layer = ""
                rows.append({"id": info[x][0], "abbr": x, "group": info[x][1], "country": info[x][2],
                             "family": fam, "vantage": v, "cookie": int(c), "request_sent": int(r),
                             "cmp_detected": int(cmp_), "focal_cookie_from_EC": int(x in focal),
                             "layer_if_focal": layer})
            summary.append({"family": fam, "vantage": v, "focal_sites": len(focal),
                            "cookie_set": n_c, "request_sent_no_cookie": n_vendor,
                            "request_not_sent": n_upstream})
            print(f"{fam:17s} {v}: focal {len(focal):3d} | cookie set {n_c:3d} | "
                  f"request sent, no cookie {n_vendor:3d} | request not sent {n_upstream:3d}")

    with open(os.path.join(OUT, "vendor_layer_by_site.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "vendor_layer_summary.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(summary[0]), lineterminator="\n"); w.writeheader(); w.writerows(summary)

    # Site-level tracking under the extended taxonomy, majority of three passes
    full = [x for x in sites if all(sum(ok[(x, v)]) == 3 for v in VANTAGES)]
    M = {(x, v): majority(track[(x, v)]) for x in full for v in VANTAGES}
    with open(os.path.join(OUT, "tracking_extended_sites.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.writer(h, lineterminator="\n"); w.writerow(["id", "abbr", "group"] + VANTAGES)
        for x in full:
            w.writerow([info[x][0], x, info[x][1]] + [int(M[(x, v)]) for v in VANTAGES])
    k = len(VANTAGES)
    X = [[int(M[(x, v)]) for v in VANTAGES] for x in full]
    C = [sum(r[j] for r in X) for j in range(k)]
    R = [sum(r) for r in X]
    N = sum(R)
    Q = (k - 1) * (k * sum(c * c for c in C) - N * N) / (k * N - sum(r * r for r in R))
    print(f"\nsite-level tracking, n = {len(full)}:", dict(zip(VANTAGES, C)))
    print(f"Cochran Q = {Q:.2f}, df = {k - 1}, p = {chi2.sf(Q, k - 1):.5f}")
    tests = []
    for a, b in itertools.combinations(VANTAGES, 2):
        b_ = sum(M[(x, a)] and not M[(x, b)] for x in full)
        c_ = sum(M[(x, b)] and not M[(x, a)] for x in full)
        tests.append((exact_mcnemar(b_, c_), a, b, b_, c_))
    tests.sort()
    prev = 0.0
    for i, (p, a, b, b_, c_) in enumerate(tests):
        adj = max(prev, min(1.0, (len(tests) - i) * p)); prev = adj
        print(f"  {a} vs {b}: {b_} / {c_} discordant, exact p = {p:.4f}, Holm p = {adj:.4f}")


if __name__ == "__main__":
    main()
