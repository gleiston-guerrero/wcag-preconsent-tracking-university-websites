# Manual validation of three WCAG success criteria

*Versión en español: [README_ES.md](README_ES.md)*

Manual verification of the automated audit for three success criteria on a subsample of
15 sites: seven from the benchmark group and eight from the Ecuadorian census. The
criteria are **1.1.1** non-text content, **1.4.3** contrast (minimum) and **2.4.4** link
purpose (in context), all of WCAG 2.2, which is also published as ISO/IEC 40500:2025.

**How the fifteen sites were chosen.** The subsample was selected purposively, to cover both
groups and a range of automated outcomes, and the criterion was not recorded in writing at the
time. It cannot be reconstructed now, so it is stated here as what it is: a purposive
selection of unrecorded rule. Nothing measured on these fifteen sites is extrapolated to the
126 of the census, and the article does not present them as a probability sample.

The folder holds **two rounds of coding by different evaluators**, plus the instrument
prepared for a third. They must not be merged: each round used a different coding scheme,
and the difference between them is itself a finding.

Column names in every CSV of this folder are in English. The coded **values** stay in
Spanish (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `1`/`P`/`0`, `REVISAR`), which is
the vocabulary the CODEBOOK defines.

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

### Round 2 — 1–2 September 2026, evaluator `R01`

`recoding_111.csv`, `recoding_143.csv`, `recoding_244.csv` — 15 rows
each, one per site. The session ran from the morning of 1 September into the early hours of
2 September; `extraction_utc` carries the UTC stamp of each reading and `date` the day it
belongs to. Better documented than round 1: they add the UTC extraction stamp,
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

## What the comparison between rounds shows

Computed over the 45 cells shared by round 1 and round 2, taking round 1 from the `code`
column of `wcag_validation_15_sites.csv` and round 2 from the `code` column of
`recoding_111.csv`, `recoding_143.csv` and `recoding_244.csv`:

| Coding scheme | Observed agreement | Cohen's kappa | 95% CI |
|---|---|---|---|
| Three categories (`1` / `P` / `0`) | 60.0% | 0.399 | [0.18, 0.61] |
| Binary (`P` counted as not conforming) | 80.0% | 0.590 | [0.35, 0.83] |

**What this statistic measures, and what it does not.** The two rounds do not share an
instrument: round 1 sampled elements at each site and judged a proportion, and round 2
enumerates every applicable element under ACT rules. The figures above therefore quantify
how far the change of instrument moved the verdicts. They are not an estimate of
inter-coder reliability, and must not be read as one. The inter-coder estimate for the ACT
round is reported in `act_round2/README.md`, separately for the mechanical rules and for
the judgement rules.

On the five sites coded by all three evaluators, the same pattern holds and no single
coder is the outlier: `R01` against round 1 gives 0.375 in three categories and 0.737
binary; `R01` against `D01` gives 0.192 and 0.324; round 1 against `D01` gives 0.457 and
0.359. `D01` here is the `delivered_code` column of `wcag_double_evaluation_5_sites.csv`,
that is, the code as the second evaluator submitted it, not the `admissible_code` that the
review of the evidence later allowed.

Of the 18 disagreements across the 45 cells, 17 are between `P` and one of the extremes and
only one — SC 1.4.3 at HKUST — is between conforming and non-conforming. The coders saw the same thing
and differed on where the threshold of *partial* lay. **The dichotomy is reliable; the
trichotomy is not.**

### Round 1 against the ACT round of 8 and 9 September

The ACT round codes each applicable element under a rule and returns a site verdict with two
values only, conforming or failing. Round 1 has three. The comparison therefore depends on
how `P` is treated, and the choice changes the answer: keeping the three categories gives
37.8 per cent agreement with a kappa of 0.097 over 28 disagreements, and counting `P` as not
conforming gives 73.3 per cent with a kappa of 0.226 over 12. In the binary scheme 11 of
those 12 disagreements run toward non-conformity, which is what exhaustive enumeration does
to verdicts reached by sampling a proportion of the elements.

Until version 2.0.0 of this deposit the READMEs of `act_round2/` reported this comparison as
62.2 per cent agreement with a kappa of 0.201 over 17 disagreements. Neither scheme yields
those numbers, they could not be recomputed from the deposited files, and they were
withdrawn. `CHANGELOG.md` records the withdrawal.

`kappa_wcag.py`, in `code/analysis/`, computes the kappa of the five double-coded sites of
`wcag_kappa_pairs.csv`: 0.517 excluding the pair with contradictory evidence and 0.457
including it. `kappa_rondas.py`, in the same folder, reproduces every figure of this
section from the deposited files — the 45-cell comparison, its confidence intervals, the
count and type of the disagreements, and the three pairwise comparisons of the five
double-coded sites — and stops with an error if any of them fails to come out. The 95 per
cent intervals use the asymptotic standard error
`sqrt(po(1-po)/(n(1-pe)^2))`.

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

`E01`–`E10` for the first coding round, `D01` for the partial second coding, `R01` for
the first author's manual recoding, `R02` for the ACT collection of 8 September, `R03` for
the assisted resolution of the `qt1vmo` image elements, and `R04` for the independent
second evaluator. Each code designates one coding and one only. No file in this folder identifies an
evaluator: none carries the name, the e-mail address or a local file path of anyone on the
research team. Versions carrying evaluator names exist but are not part of this deposit.

The e-mail addresses that do appear, in `act_round2/image_evidence/`, were observed on the
audited institutions' own home pages and are reproduced as observed. They belong to those
institutions, not to the research team.
