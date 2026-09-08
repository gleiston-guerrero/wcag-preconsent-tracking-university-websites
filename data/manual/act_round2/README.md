# ACT round: element-level recoding of three WCAG success criteria

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
system and reviewed by the first author, as recorded in the `evaluador_cod`
column. It is therefore **not** one of the two independent human codings used to
estimate inter-coder agreement.

## review_282_rows.csv

The subset of rows whose outcome determines a site-level verdict, extracted for
review.

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

Agreement with the first round, over the 45 site-by-criterion cells they share,
is 62.2% with a Cohen's kappa of 0.201. **That figure does not estimate
inter-coder reliability.** All 17 disagreements run in the same direction, from
pass to fail, which is the signature of a change of instrument rather than of
disagreement between coders: exhaustive enumeration finds failures that
proportional sampling does not. The figure is reported as a sensitivity analysis
of the coding procedure.

## Reproducibility caveat

Repeated runs of the same site on the same day differ by one to four applicable
elements on pages with carousels or rotating content. No verdict changed across
any repetition. Counts of *inapplicable* elements are volatile and depend on the
site's technology — one site contributed 249 inapplicable rows from a translation
widget alone — and should not be compared across sites.
