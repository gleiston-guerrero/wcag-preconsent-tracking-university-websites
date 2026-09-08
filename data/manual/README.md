# Manual validation of three WCAG success criteria

Manual verification of the automated audit for three success criteria on a subsample of
15 sites: seven from the benchmark group and eight from the Ecuadorian census. The
criteria are **1.1.1** non-text content, **1.4.3** contrast (minimum) and **2.4.4** link
purpose (in context), all of WCAG 2.2, which is also published as ISO/IEC 40500:2025.

The folder holds **two rounds of coding by different evaluators**, plus the instrument
prepared for a third. They must not be merged: each round used a different coding scheme,
and the difference between them is itself a finding.

---

## Coding rounds

### Round 1 — 27 August 2026, evaluators `E01` to `E10`

`wcag_validation_15_sites.csv` — 45 rows, one per site and criterion. Each row records
the code, the sample size `n`, the number of failures `f`, the evaluator code, the date,
the duration in minutes, the number of captures and a technical opinion.

`manual_coding_15_universities.csv` — 15 rows, one per site, with the three codes
side by side and a bound on each. **Every row states `un solo codificador`, a single
coder**, in all three status columns. It is a record of the first pass and carries no
inter-coder evidence; it is published for completeness.

### Round 2 — 1 September 2026, evaluator `R01`

`recoding_111.csv`, `recoding_143.csv`, `recoding_244.csv` — 15 rows
each, one per site. Better documented than round 1: they add the UTC extraction stamp,
the total number of elements detected against the sample examined, the list of failing
elements and a substantive note per cell. Several of those notes record the decisions
that turned out to drive the disagreement, such as the exclusion of visually hidden text
from the contrast measurement, and the unreliability of a DOM traversal for establishing
the context of a link.

### Partial second coding — 25 August 2026, evaluator `D01`

`wcag_double_evaluation_5_sites.csv` — 15 rows covering five sites, with a justification
per cell and an explicit judgement on whether the evidence supplied supports the code as
delivered.

`wcag_kappa_pairs.csv` — pairs of first and second coding with an agreement column, for
those five sites.

`wcag_validation_anonymised.xlsx` — the round-1 workbook without evaluator names.

---

## What the agreement between rounds shows

Computed over the 45 cells shared by round 1 and round 2:

| Coding scheme | Observed agreement | Cohen's kappa | 95% CI |
|---|---|---|---|
| Three categories (`1` / `P` / `0`) | 60.0% | 0.399 | [0.18, 0.60] |
| Binary (`P` counted as not conforming) | 80.0% | 0.590 | [0.35, 0.81] |

On the five sites coded by all three evaluators, the same pattern holds and no single
coder is the outlier: `R01` against round 1 gives 0.375 in three categories and 0.737
binary; `R01` against `D01` gives 0.192 and 0.324; round 1 against `D01` gives 0.457 and
0.359.

Of the 18 disagreements across the 45 cells, almost all are between `P` and one of the
extremes rather than between conforming and non-conforming. The coders saw the same thing
and differed on where the threshold of *partial* lay. **The dichotomy is reliable; the
trichotomy is not.**

`kappa_wcag.py` in `code/analysis/` reproduces these figures.

---

## The instrument prepared in response

`act_recoding_5_sites_TEMPLATE.csv` and `act_recoding_DICTIONARY.md`

An empty template and its data dictionary for a third round, anchored in the W3C
Accessibility Conformance Testing (ACT) Rules, whose format became a W3C Recommendation
in February 2026. Two changes follow from that anchoring:

- The outcome vocabulary is *applicable*, *passed*, *failed*, *inapplicable*. There is no
  intermediate category, which removes the source of disagreement identified above.
- The unit of coding is the individual element rather than the site, and what counts as an
  applicable element is fixed by the rule rather than decided by the evaluator. Rule
  `afw4f7` applies to any visible character, so visually hidden text is outside its scope
  by definition; and the context of a link is the *programmatically determined link
  context* of WCAG, a closed list, not whichever ancestor a DOM traversal reaches.

Rules used: `23a2a8`, `qt1vmo` and `e88epe` for 1.1.1; `afw4f7` for 1.4.3; `c487ae`,
`5effbb` and `fd3a94` for 2.4.4.

The template is **not yet filled in**. Until it is, the article reports no result from this
round.

---

## captures/

Forty-five screenshots, fifteen per criterion, in `1.1.1/`, `1.4.3/` and `2.4.4/`. Named
by institution. They are the evidence behind round 1 and round 2.

---

## Evaluator codes

`E01`–`E10`, `D01` and `R01`. No file in this folder contains a name, an e-mail address or
a local path. Versions carrying evaluator names exist but are not part of this deposit.
