# ACT round: element-level recoding of three WCAG success criteria

*Versión en español: [README_ES.md](README_ES.md)*

Second coding round on the 15-site subsample, 8 September 2026. Where the first
round (`../wcag_validation_15_sites.csv`, `../recoding_*.csv`) coded each
site by sampling elements and judging a proportion, this round codes **every
applicable element** under the W3C Accessibility Conformance Testing (ACT) Rules,
whose format became a W3C Recommendation in February 2026.

The outcome vocabulary is *applicable*, *passed*, *failed*, *inapplicable*. There
is no intermediate category, which removes the source of disagreement identified
between the earlier rounds.

Criteria: 1.1.1 non-text content, 1.4.3 contrast (minimum), 2.4.4 link purpose
(in context), all of WCAG 2.2 / ISO/IEC 40500:2025.

Rules applied: `23a2a8`, `qt1vmo`, `e88epe` for 1.1.1; `afw4f7` for 1.4.3;
`c487ae`, `5effbb`, `fd3a94` for 2.4.4.

---

## recoding/

Fifteen files, one per site, 7,836 rows. One row per applicable element, plus
rows recording elements the rule does not apply to and why.

The `_ok` suffix records that no consent dialogue was open when the site was
measured; the collector names the file `_MODALABIERTO` otherwise and those runs
were discarded. Consent dialogues were closed before measuring, because text a
dialogue covers is not visible and would fall outside rule `afw4f7` for a reason
unrelated to the page. Two sites, NUS and IAEN, offered only an accept button.

Rows marked `REVISAR` are those the rule refers to human judgement. Rows that
decide a site-level verdict were resolved; the remainder were left marked,
because the criterion had already failed on another element and their outcome
cannot change the verdict.

## image_evidence/

Fourteen files with the full evidence needed to judge rule `qt1vmo`: unabridged
image URL, srcset, CSS background image, inline svg markup, rendered and natural
dimensions, containing link and nearby text. ULVR has no file because no image
on that site is applicable to the rule.

Collected with a scroll pass that triggers lazy loading. Without it, 22 of 27
images on one site were empty placeholder svgs rather than photographs.

## qt1vmo_345_resolved.csv

The 345 applicable elements with their outcome and a written justification for
each: 232 passed, 113 failed. Every failure was determined against the image
itself, downloaded and examined.

Coding for this file was carried out with the assistance of a generative AI
system and reviewed by the first author, as recorded in the `evaluator_code`
column. It is therefore **not** one of the two independent human codings used to
estimate inter-coder agreement.

## review_282_rows.csv

The subset of rows whose outcome determines a site-level verdict, extracted for
review.

Column names in every CSV of this folder are in English; the coded **values** stay in
Spanish (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), which is the
vocabulary the CODEBOOK defines.

## instruments/

`act_recode.js` — collector for the three criteria, run in the browser console.
`act_images.js` — image evidence collector for `qt1vmo`.
`act_recode_evaluator2.js` — the same collector prepared for a second evaluator.
`SECOND_EVALUATOR_MANUAL.md` — collection protocol for the second evaluator.
`EVALUATOR_DECISION_CRITERIA.md` — decision criteria for the judgement rows, built
on the official W3C rule definitions and examples. It deliberately contains no
example from the fifteen sites under evaluation.

---

## What the round establishes

| Criterion | Benchmark group | Ecuadorian census |
|---|---|---|
| 1.1.1 | 6 of 7 do not satisfy | 8 of 8 |
| 1.4.3 | 4 of 7 | 8 of 8 |
| 2.4.4 | 7 of 7 | 8 of 8 |

No site satisfies all three. All eight Ecuadorian institutions fail all three.

## Reproducibility of the instrument

This round has two independent codings: `recoding/`, of 8 September 2026
(`R02`), and `recoding_evaluator2/`, of 9 September (`R04`).
`code/analysis/acuerdo_act.py` compares them and writes
`data/processed/act_agreement_summary.csv` and
`act_agreement_disagreements.csv`.

On the three rules the rule decides mechanically — `23a2a8`, `afw4f7` and
`c487ae` — the two codings agree on 3 186 of 3 189 element-level comparisons:
**99.9 per cent agreement, Cohen's kappa 0.996 with a 95 per cent CI of
[0.991, 1.000]**, with an identical prevalence of `cumple`, 86.7 per cent in
both. Agreement on which elements the rules apply to is 99.1 per cent with a
kappa of 0.981.

**This estimates the reproducibility of the instrument across independent
operators, not inter-coder reliability.** On these three rules the evaluator only
runs the script; the rule decides on its own.

The three disagreements are listed in `act_agreement_disagreements.csv` and they
show the mechanism of the variation. One is an off-screen label at Cornell,
`label.offscreen`, whose contrast computed as 1.00:1 in one run and 9.81:1 in the
other: a ratio of 1.00:1 means text and background are the same colour, so the
disagreement sits on the boundary of what counts as a visible character, which is
where rule `afw4f7` stops applying. The other two are links at UTI inside
rotating content, a tiled post grid and a carousel, whose accessible name depends
on which item occupied the slot at the moment of measurement. **The two run in
opposite directions**, so the variation carries no systematic bias.

At site level, the two codings return the same verdict in all 34 of the 45
site-by-criterion cells that both can decide, including the only three in which a
site *does* satisfy a criterion: SC 1.4.3 at Northwestern, UC Berkeley and UCL.
The remaining 11 cells hold rows referred to human judgement that one of the two
codings has not yet resolved.

## Element matching, and what it leaves out

The two codings enumerate elements independently and the home pages change from
one day to the next, so `element_n` does not designate the same element in both.
The comparison matches on abbreviation, criterion, rule and selector. 7 037
elements match; 799 rows of `R02` and 98 of `R04` have no counterpart.

Most of that gap is not a coding difference. **607 of the 799 unmatched rows of
`R02` are rows for inapplicable elements**, which enter no agreement calculation
and can change no verdict, and **504 of them belong to a single translation
widget** whose language list was rendered in the 8 September run and not in the
9 September one: that widget contributes 259 rows at IAEN and 264 at UTI in
`R02`, against 7 and 12 in `R04`.

What the gap does leave out is **129 rows of `R02` and 47 of `R04` that carry a
definite outcome**: elements one run saw and the other did not. The agreement
above is therefore computed over 96.1 per cent of the decided rows of `R02` and
98.5 per cent of those of `R04`.

Two of the eleven open cells are open for that reason and not through
disagreement: at Cornell SC 2.4.4 and at UTI SC 1.1.1, `R02` found a failing
element that `R04` did not see; at IAEN SC 2.4.4 the reverse happens. A site
verdict can therefore differ between two codings without any coder disagreeing.

## Inter-coder reliability: not yet estimated

The rows that the rules refer to human judgement — 318 under `qt1vmo`, 1 016
under `5effbb` and 17 under `fd3a94` — are still marked `REVISAR` in
`recoding_evaluator2/`. Until a second evaluator resolves them with
`../instruments/resolver_r04.py`, this round does not support an estimate of
inter-coder reliability, and none is reported.

Round 1 and this round do not share an instrument: the first coded each site by
sampling elements and judging a proportion, and this one enumerates every
applicable element under ACT rules. The differences between them over the 45
cells they share reflect that change of instrument — exhaustive enumeration finds
failures that proportional sampling does not — and not a disagreement between
people. No agreement statistic is reported for that comparison, because it would
measure the change of instrument rather than agreement between coders.
