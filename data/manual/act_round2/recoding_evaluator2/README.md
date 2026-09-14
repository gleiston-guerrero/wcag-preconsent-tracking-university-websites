# Independent second coding of the ACT round

*Versión en español: [README_ES.md](README_ES.md)*

Fifteen files, one per site, 7 135 rows. The same fifteen home pages, the same
three success criteria and the same seven ACT rules as `../recoding/`, coded
independently by a second evaluator on 9 September 2026 with
`../instruments/act_recode_evaluator2.js`.

This is not a third round and not a re-measurement. It is the second of two
independent codings of one round, and it is what makes the reproducibility of the
ACT instrument across two operators measurable. On the rules that refer the
decision to human judgement only part of the comparison is human against human —
62 link elements under SC 2.4.4 — while the SC 1.1.1 side runs against an assisted
resolution and therefore supports no inter-coder coefficient; `../README.md` sets
out both. The evaluator worked from
`../instruments/SECOND_EVALUATOR_MANUAL.md` and did not see the first coding, the
earlier rounds or the draft of the article.

Column names are in English; the coded **values** remain in Spanish
(`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), the vocabulary the
CODEBOOK defines. This matches `../recoding/`.

## Evaluator code

The files are deposited under `R04`. The collection instrument ships with a
placeholder code, which the evaluator left unchanged; the code for this coding was
assigned when the files were deposited, and the `evaluator_code` column was set
accordingly. Nothing else in the delivered files was altered, and the file names
were normalised to the date format used elsewhere in the deposit.

## A discarded first attempt

A first collection on the same day was discarded before deposit. The evaluator's
browser had automatic translation enabled, which rewrites the page: the accessible
names came back in Spanish on the English-language sites and the browser had
inserted `font` elements into the DOM. The effect fell almost entirely on the six
English-language sites of the benchmark group and on none of the eight Ecuadorian
ones, so it would have biased exactly the comparison the study makes. The
collection was repeated with translation disabled. The files here are from that
second collection, and they contain no injected `font` elements.

## What it establishes

For **1.4.3** and **2.4.4** the second coding reproduces the first exactly: on
1.4.3, where the rule leaves nothing to judgement, four of the seven benchmark
sites and all eight Ecuadorian sites fail; on 2.4.4 all fifteen sites fail in
both codings.

For **1.1.1** the two codings differ in two of the fifteen sites, ECOTEC and UC
Berkeley, which this coding reads as satisfying the criterion and the first reads
as failing it. This coding therefore finds 12 of the 15 sites failing 1.1.1 where
the first finds 14. Both disagreements are element-level judgements of rule
`qt1vmo` and both are set out in `../README.md`.

No cell of the fifteen-by-three matrix is provisional any longer: the judgement
rows that could decide a verdict were resolved on 11 September 2026 (below), so
the verdicts recorded here are verdicts, not lower bounds.

## Closing the judgement rows

The collector leaves marked `REVISAR` the rows that the ACT rules refer to human
judgement: 1 351 of the 7 135. `../instruments/resolver_r04.py` extracts them to a
plain-text worksheet and merges the evaluator's decisions back into these files,
recomputing the site verdicts.

It extracts only the **318 rows that still decide a site verdict**, 203 of SC 1.1.1
and 115 of SC 2.4.4. Where a criterion already fails at a site through another
element, no pending row of that site can change the verdict, so those rows stay
marked. This is the policy the first coding follows. It is stated here because it
has a cost: an evaluator who receives only those rows can infer which sites were
still open. The alternative, all 1 351 rows, is four times the work and changes no
reported figure.

The 318 rows were resolved by the evaluator on 11 September 2026 in a single
session of about five hours: **235 `cumple` and 83 `falla`**, each with a written
justification. The justification is appended to the row's own `notes` field after
the marker `|| RESUELTO R04:`, so the decision and the evidence the evaluator saw
travel together and the original text of the field is not overwritten. Nothing
else in the fifteen files changed: the merge modified the `outcome` and `notes`
columns of exactly those 318 rows and no other column, row or file.

`registro_R04.tsv` is the session log the tool wrote as the work proceeded: one
line per decision, with the timestamp, the evaluator code, the worksheet, the
block, the site, the rule and the result. It holds 331 lines for 318 blocks
because thirteen blocks were decided twice; the second decision is the one that
stands. Four decisions were changed outside the tool and therefore do not appear
in it; `nota_incidencias.txt` lists them.

`nota_incidencias.txt` is the evaluator's incident note, compiled by the first
author from the written justifications, the session log and remarks the evaluator
made orally, which are labelled as such. Its last section is the first author's
own, and is labelled as not being the evaluator's. Two fields, the browser version
and the list of active extensions, are still marked as pending.

## Internal consistency of the justifications

Two formulas recur in the written justifications and they are used consistently.
*"Aunque no tenga contexto"* means the name alone is clear enough that the
context need not be read; it appears as the sole justification of 47 decisions
and all 47 are `cumple`. *"No hay contexto"* and *"Sin contexto no sabría"* mean
the opposite, that the name alone does not suffice; they appear 4 times and all 4
are `falla`.

One pair is inconsistent, and it is recorded rather than adjusted. Under rule
`5effbb`, the skip link of UCL, accessible name `"Skip to main content"`, was
decided `cumple`, and the skip link of Cornell, `"Skip to content"`, was decided
`falla`; neither has a programmatic context, and the two links are functionally
the same. That is one element-level judgement in each direction and it is part of
what the agreement figure in `../README.md` measures.

## Truncated accessible names

The `notes` field shows the accessible name up to 120 characters. In **8 of the
318 blocks** the name presented to the evaluator was shorter than the name
`../image_evidence/` records for the same element. Seven of the eight were decided
`cumple`, and for those the truncation cannot have changed the decision: the
fragment shown was already descriptive and the full name extends it. The eighth
was decided `falla` and lost two characters. The full names are in
`image_evidence/`, and `../README.md` states the bound this places on the
agreement estimate.

## A limitation of the collector

`act_recode_evaluator2.js` caps the length of the `notes` field and truncates it
from the left. When an image's accessible name is long, what is lost is the
beginning of the image address. Of the 203 rows of SC 1.1.1 that decide a verdict,
44 carry a complete address, 34 can be reconstructed from the site's host and
verified, 70 are truncated beyond recovery, and 55 carry none because the image is
a CSS background or an inline svg.

A reconstruction is accepted only when the fragment received is an exact suffix of
the reconstructed address; where it is not, the worksheet says the address was
truncated and gives the element's selector instead. Nothing is guessed.

Rule `qt1vmo` requires the judgement to be made against the image, so those rows
cannot be closed from the worksheet alone. `../instruments/act_images.js` is the
pass that collects the uncropped address, the `srcset`, the CSS background and the
rendered dimensions; it produced `../image_evidence/` for the first coding and it
is the route for these rows too.

## Reproducibility caveat

The same caveat as the first coding applies. Repeated runs of the same site on the
same day differ by one to four applicable elements on pages with carousels or
rotating content, and counts of *inapplicable* elements are volatile and depend on
the site's technology; they should not be compared across sites.
