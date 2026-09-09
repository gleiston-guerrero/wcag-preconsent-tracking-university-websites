# Independent second coding of the ACT round

*Versión en español: [README_ES.md](README_ES.md)*

Fifteen files, one per site, 7 135 rows. The same fifteen home pages, the same
three success criteria and the same seven ACT rules as `../recoding/`, coded
independently by a second evaluator on 9 September 2026 with
`../instruments/act_recode_evaluator2.js`.

This is not a third round and not a re-measurement. It is the second of two
independent codings of one round, and it is what makes an inter-coder agreement
estimate possible for the ACT instrument. The evaluator worked from
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

## What it establishes so far

For **1.4.3**, where the rule leaves nothing to judgement, the second coding
reproduces the first exactly: four of the seven benchmark sites and all eight
Ecuadorian sites fail.

For **1.1.1** and **2.4.4** the rows that the rules refer to human judgement are
still marked `REVISAR` and the site verdicts are therefore provisional. Those rows
can only add failures, never remove them, so the verdicts recorded here are lower
bounds.

## Reproducibility caveat

The same caveat as the first coding applies. Repeated runs of the same site on the
same day differ by one to four applicable elements on pages with carousels or
rotating content, and counts of *inapplicable* elements are volatile and depend on
the site's technology; they should not be compared across sites.
