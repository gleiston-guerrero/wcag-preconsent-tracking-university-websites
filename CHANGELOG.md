# Changelog

Versions of the Zenodo record whose concept DOI is
[10.5281/zenodo.22405998](https://doi.org/10.5281/zenodo.22405998). Each entry states what
changed and, where a figure was withdrawn, why. Files already published cannot be replaced:
a correction is a new version, and the earlier one stays retrievable under its own version
DOI. That is why withdrawals are recorded here rather than silently overwritten.

## 2.0.0 — 10 September 2026

The major number changes because a previously reported statistic is withdrawn, not merely
because material was added.

### Withdrawn

- **The agreement statistic of 62.2 per cent with a Cohen's kappa of 0.201 over the 45
  site-by-criterion cells shared by round 1 and the ACT round, and the accompanying claim
  that all 17 disagreements ran in the same direction.** The figures do not come out of the
  deposited files. Recomputing the same comparison gives 37.8 per cent agreement with a
  kappa of 0.097 and 28 disagreements when round 1's three categories are kept, and 73.3
  per cent with a kappa of 0.226 and 12 disagreements when `P` is counted as not
  conforming. Neither is 62.2 per cent, and 17 disagreements corresponds to neither count.
  `code/analysis/kappa_rondas.py` computes both, so the withdrawal can be checked rather
  than taken on trust. The direction of the disagreements survives in substance: in the
  binary scheme 11 of the 12 run toward non-conformity, which is the signature of
  exhaustive enumeration finding failures that proportional sampling misses. What does not
  survive is "all", and neither does the figure. Nothing replaces it as an estimate of
  inter-coder reliability, because the round does not yet support one; what the round now
  reports instead is reproducibility of the instrument across two independent operators,
  described below and labelled for what it measures.

### Added

- **A second, independent coding of the whole ACT round** (`R04`, 9 September 2026):
  fifteen files and 7 135 rows in `data/manual/act_round2/recoding_evaluator2/recoding/`,
  with eight files and 233 rows of image evidence. A first collection by the same evaluator
  was discarded and is not deposited: the browser's automatic translation had rewritten the
  accessible names, leaving `<font>` elements in between 23.3 and 55.5 per cent of the rows
  at the six English-language sites. The repeated collection has none.
- **Instrument reproducibility across the two codings.** Over the three mechanical rules —
  `23a2a8`, `afw4f7` and `c487ae`, where the rule decides and the operator only runs the
  script — the two codings agree on 3 186 of 3 189 element-level comparisons: 99.9 per
  cent, Cohen's kappa 0.996 with a 95 per cent interval of [0.991, 1.000], and an identical
  majority-class prevalence of 86.7 per cent. This is reproducibility across operators, not
  inter-coder reliability, and `code/analysis/acuerdo_act.py` reports the two in separate
  blocks so that they cannot be confused.
- **Resolution of every judgement row able to decide a site verdict.**
  `qt1vmo_345_resolved.csv` now holds 349 rows, 236 conforming and 113 failing, and no cell
  of the fifteen-by-three matrix is open. Two provenances are recorded per row in
  `evaluator_code`: 345 rows resolved with the assistance of a generative model and
  reviewed by the first author (`R03`), and four resolved by the first author alone
  (`R01`). The assisted rows are excluded from every agreement estimate.
- **The instruments of the round**, in `data/manual/act_round2/instruments/`: the two
  collectors, the collector prepared for a second evaluator, the collection protocol, the
  decision criteria for the judgement rows, and the merge tool.
- **Five analysis scripts** in `code/analysis/`: `comprobar_brecha.py`, `acuerdo_act.py`,
  `inventario_revisar.py`, `cerrar_revisar.py` and `reparar_duplicados.py`.
- **`kappa_rondas.py`**, which reproduces every agreement figure of
  `data/manual/README.md` from the deposited files and stops with an error if any of them
  fails to come out. Before this version those figures were reported without a script that
  produced them.
- **This changelog**, in English and Spanish, and a `.zenodo.json` that fixes the record's
  metadata in the repository rather than only in the deposit form.

### Corrected

- The two upper confidence bounds of the round-1-against-round-2 comparison in
  `data/manual/README.md`, from [0.18, 0.60] and [0.35, 0.81] to [0.18, 0.61] and
  [0.35, 0.83]. The lower bounds were right; the upper ones did not match the standard
  error the interval is built on. The point estimates, 0.399 and 0.590, and the observed
  agreements, 60.0 and 80.0 per cent, are unchanged and now reproducible.
- That same comparison is now labelled for what it measures — the effect of the change of
  instrument between the two rounds — and the source of each side of it is named, down to
  the column. Two files in `data/manual/` gave different round-1 codings and only one of
  them yields the reported figures.
- Nine duplicate rows in `qt1vmo_345_resolved.csv`, written by a merge that checked whether
  a criterion already failed at a site but not whether the individual element already had a
  verdict. All nine agreed on outcome; the deposited rows were kept and the count went from
  358 to 349.
- `act_agreement_disagreements.csv` was not reproducible byte for byte: the pairing
  iterates sets, whose iteration order depends on Python's per-process string hash
  randomisation, so the same data produced the same rows in a different order on every run
  and the sha256 of the manifest could not be obtained again. The rows are now sorted.
- The six figures of `figures/` were not reproducible byte for byte either: matplotlib
  writes the time of the run inside each PDF, so the same plot came out with different bytes
  on every execution and six of the 305 entries of `CHECKSUMS.txt` could not be obtained
  again by regenerating the figure. The scripts now suppress that date. The content is
  unchanged — the regenerated figures are pixel-identical to the ones this version replaces —
  and two separate runs now produce identical bytes.
- The five scripts of the round resolved their inputs against the current working
  directory, two of them expecting the repository root and one expecting
  `code/analysis/`. All of them now resolve against the root of the repository and run from
  either place.
- Eight fragments of Spanish prose in comments and console messages where an automated
  renaming had replaced a Spanish word with its English form.

### Documented

- That 201 of the 282 rows of `review_282_rows.csv` are deliberately left without an
  outcome: by the time the resolution reached them, SC 1.1.1 was already established as
  failing at every site they belong to, so no verdict on them can change a reported figure.
- That the subsample of fifteen sites was selected purposively and that the criterion was
  not recorded at the time. No figure of the round is extrapolated to the census.
- That 2 350 judgement rows remain marked `REVISAR` across the two codings, of which 318 —
  all in the second coding — could still decide a verdict and are with the second evaluator.
  Until they come back, no inter-coder reliability estimate is reported for the judgement
  rules, and `acuerdo_act.py` prints that block as pending rather than filling it.

## 1.0.0 — 5 September 2026

The first published version, [10.5281/zenodo.22405999](https://doi.org/10.5281/zenodo.22405999),
a single archive of 3.0 MB under CC BY 4.0.

It was assembled four days before this repository was created and does not correspond to
the file inventory that `CHECKSUMS.txt` fixes here. `README.md`, under *Repository
history*, explains why the repository was started clean: an earlier one had received
commits containing files that identified the human evaluators of the manual validation.
Readers comparing the two versions should download both archives rather than assume that
paths shared between them hold the same content.
