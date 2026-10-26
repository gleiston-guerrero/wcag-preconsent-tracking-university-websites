# Ecuadorian series from ETAPA, 14 September 2026

*Versión en español: [READ_ME_ES.md](READ_ME_ES.md)*

Three passes over the 126 sites of the census, from the same Ecuadorian
residential connection of ETAPA EP (AS27668, Cuenca) that the reported campaign
used, with no virtual private network.

This series exists for two reasons, and it answers a different question in each.

**It completes the operator control.** `../tracking_telconet/` measures the census
from a second Ecuadorian operator, but it was taken on 7 September, three weeks
after the reported campaign of 15 August, so comparing it with that campaign
mixed the operator with the date. Compared against this series instead, both
sides are from September and the date stops varying.

**It isolates the date.** Against the August campaign, this series holds the
operator, the city, the machine, the instrument, the Node version and the
configuration fixed, and varies only the month. It is the only comparison in the
deposit that does. The deposit warns in several places that the sites change from
one day to the next; this is the figure behind that warning.

`code/analysis/controles_ecuador.py` reports both contrasts and aborts if they do
not match the figures given below.

**This series is not part of the four-vantage replication and the article does
not analyse it.** It must not be merged with `../tracking/` or with
`../tracking_extended/`.

## Measurement conditions

| | |
|---|---|
| Passes | 3, run consecutively on 14 September 2026, 21:49–23:25 UTC |
| Duration | 19 minutes each |
| Sites | 126 attempted, **126 successful and 0 failed in all three passes** |
| Location checks | 7 per pass, 21 in total: at the start, after sites 25, 50, 75, 100 and 125, and at the end. All 21 returned `AS27668 ETAPA EP`, Cuenca, with the same IPv4 address throughout |
| Machine | the same machine as the August campaign, same security configuration: Microsoft Defender inactive, McAfee installed with no web-protection or anti-tracking services running |
| Instrument | `code/collection/audit_multivantage.js`, unmodified |
| Versions | axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1 — the same Node as the August campaign |
| Browser | Chromium launched with a clean profile and no extensions |

It records the state of the cookie jar, not the network requests, like the
campaigns it is compared with.

## What the two contrasts give

A site is counted as tracking if any cookie set before any consent interaction
matches the extended taxonomy, with the three passes of each series consolidated
by majority — the same construction the article uses. The test is the two-sided
exact McNemar test on the discordant pairs.

**Stability within this series: 126 of 126 sites return the same verdict in all
three passes.** The August campaign gives 123 of 124 and the Telconet series 122
of 126.

| Contrast | n | Tracking | a, b, c, d | Discordant | p |
|---|---|---|---|---|---|
| Operator: ETAPA vs Telconet, both September | 126 | 86 (68.3 %) vs 84 (66.7 %) | 83, 3, 1, 39 | 4 | 0.625 |
| Date: ETAPA September vs ETAPA August | 125 | 85 (68.0 %) vs 85 (68.0 %) | 84, 1, 1, 39 | 2 | 1.000 |

The operator contrast still varies the machine and the city alongside the
operator, because the Telconet series was taken on a different machine. It
therefore moves three things at once and cannot separate them; it is conclusive
only because no difference appears. Had one appeared, this pair of series could
not have said which of the three caused it.

The date contrast is the clean one. Two sites of 125 changed verdict in a month,
ULVR and UPenn, in opposite directions. Both proportions are 68.0 %, and they
agree with the 67.8 % the article reports for Ecuador in the multi-vantage
section.

Neither contrast supports any figure in the article. What they establish is
negative and worth having: the Ecuadorian result is not an artefact of the
network operator, and it is not an artefact of the day it was measured.

## The accessibility side of the same two occasions

Each pass also records an `accesibilidad` object, so this series and the August
campaign give **two occasions of the instrument's accessibility output over the
same 126 home pages**, one month apart, with operator, city, machine, instrument
and versions held fixed. `code/analysis/deriva_accesibilidad.py` reports it and
aborts if the figures below do not reproduce.

**This is not the accessibility measurement the article reports.** Every
accessibility figure in the article comes from the single-pass audit of 14 August
2026, `../accessibility/results.json`, which has never been repeated. What
follows bounds the drift of the instrument's output, not of that measurement, and
does not replace it.

Within each series the binary verdict is perfectly stable: whether a site has any
failing node at level A is identical across all three passes in **124 of 124**
sites in August and **126 of 126** in September.

| Comparison | n | August | September | Result |
|---|---|---|---|---|
| Any failing node at level A | 125 | 94 (75.2 %) | 94 (75.2 %) | a=93, b=1, c=1, d=30; 2 discordant; exact McNemar *p* = 1.000 |
| Highest level with no failure | 125 | — | — | identical at 122 of 125 (97.6 %) |
| Failing nodes, median per site | 125 | 23 | 21 | median change 0; no change at 69 of 125 sites; interquartile range of the change 0 to +1 |

The two sites that change verdict are U. Hemisferios, which stops failing level
A, and UCL, which starts. The three whose highest clean level moves are Princeton
(AAA to AA), U. Hemisferios (none to A) and UCL (AAA to none). UCL is the only
site in both lists and the only one that moved appreciably.

The third row is the weakest of the three and is given for completeness only:
failing-node counts are not normalised by page complexity, so a large portal
accumulates more nodes without being less accessible. The totals fall by 2.9 per
cent over the month, which says less than the fact that 69 of 125 sites do not
move at all.
