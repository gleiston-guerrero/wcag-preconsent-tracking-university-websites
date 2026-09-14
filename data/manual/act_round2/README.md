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

The 349 applicable elements with their outcome and a written justification for
each: 236 passed, 113 failed. Every failure was determined against the image
itself, downloaded and examined. The file name keeps the count it had when it
was first deposited.

The file holds two provenances, recorded per row in the `evaluator_code`
column. 345 rows were coded with the assistance of a generative AI system and
reviewed by the first author, and are therefore **not** one of the two
independent human codings used to estimate inter-coder agreement. The remaining
four rows, images 27 to 30 of the social-media grid at Cornell, were resolved by
the first author alone. They were the last rows in this coding able to decide a
site verdict: closing them leaves no cell of the fifteen-by-three matrix open,
so the verdict table above is complete rather than provisional.

`code/analysis/comprobar_brecha.py` consolidates this file, `review_282_rows.csv`
and `recoding/` into the site verdicts and compares them with the automated
audit. `code/analysis/inventario_revisar.py` reports what remains marked
`REVISAR` and separates the rows that could still decide a verdict from those
that cannot.

## review_282_rows.csv

The subset of rows whose outcome determined a site-level verdict when the file was
extracted: 201 under SC 1.1.1 and 81 under SC 2.4.4.

**Only the 81 rows of SC 2.4.4 carry an outcome.** The other 201 are deliberately left
empty. By the time the resolution reached them, SC 1.1.1 had already been established as
failing at every site those rows belong to, through elements resolved in
`qt1vmo_345_resolved.csv`; a verdict on them can no longer change any cell of the
fifteen-by-three matrix. `code/analysis/inventario_revisar.py` reports this directly: of
the rows still marked `REVISAR` in the first coding, none can decide a verdict. Resolving
them would add completeness to the deposit, not evidence to the article.

The file was extracted as a worksheet with the outcome and justification columns
empty, and it carried no `evaluator_code` column: the 81 outcomes were filled in
without recording who filled them. The column was added on 14 September 2026 and
set to **`R02`** for those 81 rows, on the first author's attestation that the
`R02` coding resolved them. It is an attestation made after the fact, not a code
written at the time, and it is recorded here as such because 62 of those rows are
the only element-level comparisons in this round that support an inter-coder
reliability estimate.

Column names in every CSV of this folder are in English; the coded **values** stay in
Spanish (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), which is the
vocabulary the CODEBOOK defines.

## exclusiones_R04.tsv

The blocks excluded from the inter-coder estimate because the collector, not the
coder, put the wrong text in front of the evaluator. Tab-separated, one row per
affected block: `grupo` (`A` for the svg-style defect, `B` for the wrong image),
`hoja` and `bloque` as the evaluator saw them, `abbr`, `element_n`, `act_rule`,
`nombre_en_la_hoja` (the text actually shown), `selector`, and `motivo` in words.
Thirty-two rows covering twenty-nine distinct blocks; three blocks carry both
defects and appear twice.

The rule is applied by `code/analysis/acuerdo_act.py` to both codings alike, and
the section on inter-coder reliability below states what the coefficient is with
it and without it.

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

These are the verdicts of the first coding, `recoding/` with its resolutions. The
second coding returns the same table for 1.4.3 and 2.4.4 and differs in two cells
of 1.1.1; the section on inter-coder reliability below names them and says what
they change.

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

At site level the two codings now decide all 45 site-by-criterion cells, and the
comparison is reported below under inter-coder reliability, where it belongs:
site verdicts on 1.1.1 and 2.4.4 rest on human judgement and are not a property
of the instrument alone.

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

Three cells owe their verdict to an element only one coding saw and not to any
coder disagreeing: at Cornell SC 2.4.4 and at UTI SC 1.1.1, `R02` found a failing
element that `R04` did not see; at IAEN SC 2.4.4 the reverse happens. In all
three the other coding reached the same verdict through other elements, so none
of them shows up as a difference — but a site verdict *can* differ between two
codings without any coder disagreeing, and that is a property of the round, not
of the coders.

## The judgement rules: agreement, and why it is not inter-coder reliability

The second evaluator resolved the judgement rows on 11 September 2026 with
`instruments/resolver_r04.py`: the 318 rows that could still decide a site
verdict, 235 `cumple` and 83 `falla`, each with a written justification recorded
in the row's own `notes` field. `recoding_evaluator2/README.md` describes that
work and its record. That closes the round, and it makes a comparison on the
judgement rules possible for the first time. **It does not make that comparison an
estimate of inter-coder reliability, and the deposit does not report one.**

The reason is the provenance of the other side. On these three rules the outcome
in `recoding/` was not decided at collection; it was decided later, in
`qt1vmo_345_resolved.csv` and `review_282_rows.csv`. The 230 comparisons
therefore split in two, and `code/analysis/acuerdo_act.py` prints them apart
because they answer different questions:

| `recoding/` side decided by | n | Criterion | Agreement | Kappa | What it is |
|---|---|---|---|---|---|
| `R02`, a human coder | 62 | 2.4.4 | 82.3% | 0.178 [−0.262, 0.619] | inter-coder reliability |
| `R03`, the assisted resolution | 168 | 1.1.1 | 76.2% | 0.390 [0.225, 0.555] | agreement, not inter-coder |

**Only the first row is an inter-coder reliability estimate, and it is a narrow
one.** All 62 of those comparisons are links at a single site, UCL, under rules
`5effbb` and `fd3a94`; 49 of the 62 are `cumple` in both codings, a prevalence of
83.9 per cent in `R02` and 91.9 per cent in `R04`. At that prevalence and that n
the coefficient carries almost no information: its interval runs from −0.26 to
0.62 and includes zero, so **it does not establish reliability, and it does not
refute it either.** The observed agreement, 82.3 per cent, is the interpretable
figure, and it rests on one site's links rather than on the sample.

The second row is the agreement between one human coding and an assisted
resolution reviewed by the first author. It is worth reporting and it is reported
here, but it is not inter-coder reliability and is not offered as such. A
coefficient for SC 1.1.1 would require a human coder to decide those 168 image
elements again without the assisted file in front of them.

The `R02` code on the 81 resolved rows of `review_282_rows.csv` was added on 14
September 2026 on the first author's attestation that that coding resolved them.
The column was not written at the time the worksheet was filled in, and the
deposit records the attestation as an attestation.

Taken together, across all three rules that refer the decision to human
judgement — `qt1vmo`, `5effbb`, `fd3a94` — the two sides agree on 179 of 230
element-level comparisons: **77.8 per cent agreement, Cohen's kappa 0.363 with a
95 per cent CI of [0.209, 0.518]**. That total mixes the two provenances above
and is reported for completeness, not as a reliability coefficient.

| Rule | n | Agreement | Kappa | CI 95% |
|---|---|---|---|---|
| `qt1vmo` (1.1.1) | 168 | 76.2% | 0.390 | [0.225, 0.555] |
| `5effbb` (2.4.4) | 61 | 83.6% | 0.212 | [−0.235, 0.659] |
| `fd3a94` (2.4.4) | 1 | 0.0% | not reported, n < 10 | — |
| **All three** | **230** | **77.8%** | **0.363** | **[0.209, 0.518]** |

The confusion matrix is close to symmetric: 30 rows `cumple` in `R02` and `falla`
in `R04`, 21 the other way. The prevalence of `cumple` is 79.6 per cent in `R02`
and 75.7 per cent in `R04`. With a category that dominates to that degree, kappa
is depressed relative to the observed agreement — the Feinstein–Cicchetti
paradox — which is why both figures and the prevalence are given together.

**Whatever this figure is, it is not the 0.996 reported above.** On the
mechanical rules the evaluator runs a script and the rule decides, so what is
measured is whether the instrument returns the same thing in two hands. On these
three rules the rule stops and asks whether a name serves a purpose equivalent to
an image, or whether a link's purpose can be determined from its name and
context. That question is answered at 0.363, *fair* agreement on the conventional
reading of the coefficient and no better. Reporting only the mechanical figure
would misdescribe the round; reporting this one as inter-coder reliability would
misdescribe it in the other direction.

### The exclusion rule

Twenty-nine element-level blocks are excluded from this estimate, listed with
their reason in `exclusiones_R04.tsv`. All twenty-nine are blocks where the
collector, not the coder, put the wrong text in front of the evaluator: in
seventeen the `nombre` line carries the text of an inline svg's `style` element
instead of the accessible name, and in fifteen the `imagen` line points to a
different element of the page; three blocks are in both groups. Both defects are
documented in `recoding_evaluator2/nota_incidencias.txt`, the first by the
evaluator and the second by the first author.

The rule was fixed before the coefficient was computed, is applied identically to
both codings, and removes 57 rows. It is not a filter on disagreement: it happens
to *lower* the coefficient, because the excluded blocks are ones the two codings
mostly agreed on.

### Resolutions with no row to land on

`code/analysis/acuerdo_act.py` carries the resolutions back into the `REVISAR`
rows of `recoding/` before comparing anything, matching first on `element_n` —
exact within a single pass, because the resolution files were extracted from
those very rows — and falling back to the selector plus the accessible name. 402
of the 430 resolutions land on a row. **The remaining 28 correspond to no row of
`recoding/` at all**: 13 at IAEN, 7 at UNESUM, 4 at HKUST, 3 at UTI and 1 at
UTPL, all under `qt1vmo`, 19 of them `falla` and 9 `cumple`. In 21 the selector
does not occur anywhere in `recoding/` for that site and rule; in the other 7 it
does, but neither the element number nor the accessible name matches, which is
the signature of rotating content.

They are left out of the comparison rather than forced onto a row, and no site
verdict depends on them: all five sites fail SC 1.1.1 in both codings through
other elements. The count is printed on every run.

### How much the figure depends on those decisions

| Variant | n | Agreement | Kappa |
|---|---|---|---|
| As reported | 230 | 77.8% | 0.363 [0.209, 0.518] |
| Without the exclusion rule | 258 | 76.7% | 0.432 [0.306, 0.558] |
| Matching also on `element_n` | 220 | 77.3% | 0.355 [0.198, 0.512] |

Across the three, agreement stays between 76.7 and 77.8 per cent and kappa
between 0.355 and 0.432. The site-level figure below is identical in all three.

A separate and narrower bound: in 8 of the 318 blocks the accessible name shown
to the evaluator was truncated at 120 characters. Seven were decided `cumple`,
where the fragment shown was already descriptive and the full name only extends
it, and the eighth lost two characters. No decision turns on the truncation.
`recoding_evaluator2/README.md` gives the detail.

### Site verdicts

The site-level comparison does not depend on matching elements at all, and it is
the level at which the article makes its claims. The two codings decide all 45
site-by-criterion cells and return the same verdict in **43 of 45: 95.6 per cent,
kappa 0.776 with a CI of [0.473, 1.000]**. SC 1.4.3 and SC 2.4.4 are identical
cell by cell, including the three cells in which a site *does* satisfy a
criterion, SC 1.4.3 at Northwestern, UC Berkeley and UCL.

The provenance caveat above applies here too, and unequally: the fifteen SC 1.4.3
cells rest on the mechanical rule alone, so that row of the comparison is a clean
two-operator reproduction, while the SC 1.1.1 and SC 2.4.4 cells inherit their
`recoding/` verdict from the assisted resolution.

Both disagreements are under SC 1.1.1, rule `qt1vmo`, and in both `R02` reads
`falla` where `R04` reads `cumple`:

- **UC Berkeley**, an image whose accessible name is `"A scientist wearing a blue
  lab coat that reads"` — the page's own alt text, which stops mid-sentence.
  `R02` read the incomplete name as failing; `R04` recorded *"el nombre es lo que
  la imagen muestra"*. The full name is in `image_evidence/`, and it is 46
  characters: the name really does end there.
- **ECOTEC**, two award logos, `qs-logo-white` and `innovatec-logo-white`, whose
  accessible names name the distinction rather than the logo
  (`"Reconocimiento QS Stars de Universidad ECOTEC"`, `"World University Rankings
  América y el Caribe"`). `R04` recorded *"el nombre dice más que la imagen"* and
  read them as passing.

These two cells are the only place where the second coding would change a figure
of the article, and both fall inside SC 1.1.1: `R04` finds 12 of the 15 sites
failing that criterion where `R02` finds 14.

The ECOTEC cell carries a further caveat that the deposit records rather than
resolves. The evaluator has since confirmed that the two logos in question are
among the images that rendered white on a white ground, visible on the page only
with effort and plainly when the file itself is opened. That confirmation closes
an open point of `recoding_evaluator2/nota_incidencias.txt`: it is why the
evaluator marked nothing as non-visible.

It does not make these blocks a defect of the collector, and they are therefore
**not** in `exclusiones_R04.tsv`. That file has one ground and one only: the
collector put the wrong text in front of the evaluator. Here it did not — the
accessible name and the image address are both the element's own. What rule
`qt1vmo` asks is whether the name serves a purpose equivalent to the image, and
how conspicuous the image is on the page is not part of that question. Both
codings could see the image: `R03` judged it from the downloaded file, `R04` from
the page with effort. Excluding these blocks would remove the one disagreement
that touches a figure of the article, on a ground the exclusion rule does not
provide, so the deposit states the consequence instead of taking it.

The consequence is worth stating plainly, because it is the largest single
dependency in the SC 1.1.1 census. The ECOTEC 1.1.1 verdict rests entirely on
these two elements in **both** codings. Were they set aside — on the view that an
evaluator who cannot readily see the non-text content cannot judge its accessible
name — neither coding would have a failing element left in that cell, the two
would agree, and the site would no longer fail SC 1.1.1: the Ecuadorian census
for that criterion would read 7 of 8 rather than 8 of 8, and the gap count of
§4.5 of the article would fall by one cell. That is a judgement for the authors
and, if it is taken, it changes a reported figure rather than only a reliability
estimate.

Round 1 and this round do not share an instrument: the first coded each site by
sampling elements and judging a proportion, and this one enumerates every
applicable element under ACT rules. The differences between them over the 45
cells they share reflect that change of instrument — exhaustive enumeration finds
failures that proportional sampling does not — and not a disagreement between
people. That comparison is quantified in `../README.md`, and it is labelled there
for what it measures: the effect of the change of instrument, never agreement
between coders. `code/analysis/kappa_rondas.py` reproduces it.
