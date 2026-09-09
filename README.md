# WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites

*Versión en español: [README_ES.md](README_ES.md)*

Data, evidence and code for the article *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, submitted to *Universal Access in the Information Society* (Springer Nature).

**Deposit DOI (concept, always resolves to the latest version):** [10.5281/zenodo.22405998](https://doi.org/10.5281/zenodo.22405998)

---

## Repository history

**This repository was created on 9 September 2026 and deliberately carries no commit history before that date.** The research it documents began in August 2026, in a different repository. The explanation belongs here rather than in a footnote, because the absence of history is the first thing a careful reader will notice.

That earlier repository had received commits containing material that should never have been versioned: files identifying the human evaluators who took part in the manual validation — names, institutional e-mail addresses and local file paths — together with early drafts of the manuscript.

Deleting those files in a later commit would not have removed them. Git preserves every version it has ever recorded, so anything committed once stays retrievable from the history; and rewriting the history of a repository that others may already have cloned or forked offers no guarantee either. The only reliable remedy was to stop using that repository and start a clean one containing nothing but the reviewed deposit. **The earlier repository was deleted**, rather than corrected in place. Deletion removes it from GitHub; it cannot guarantee that nothing was read or copied while it was online, and that is precisely why the remedy here is a clean repository and not a cleaned history.

This repository is that clean start. Every file here was checked for identifying content before being committed:

- Evaluators appear only under codes — `E01`–`E10` for the first coding round, `D01` for the partial second coding, `R01`, `R02` and `R03` for the later rounds. No file in the deposit identifies an evaluator: none carries the name, the e-mail address or a local file path of anyone on the research team.
- The deposit does contain e-mail addresses, and that is deliberate. They appear in `docs/reports/` and in `data/manual/act_round2/image_evidence/`; they were observed on the audited institutions' own public pages, and they are the privacy and data-protection contacts those universities publish. Their presence is the evidence behind the *privacy contact or DPO* indicator. They are reproduced as observed, not collected, and removing them would remove the proof of what the article reports.
- The manuscript is not deposited here. It is submitted through the journal, and its drafts are not part of the research record this repository holds.
- Nothing that identifies a natural person is published. The institutions audited are public organisations and are named; the people who coded the sample are not.

**The reset costs the commit history, not the evidence.** Nothing was altered to make it fit: what was removed was administrative material and manuscript drafts, never a measurement. The chronology of the fieldwork does not depend on git at all, because every measurement carries its own internal timestamp, recorded by the instrument at the moment of capture and independent of when the file was committed:

| Campaign | Internal timestamps |
|---|---|
| Single-pass audit | 14 August 2026, 06:38–06:59 UTC |
| Multi-vantage replication | 15 August 2026, 15:58–23:10 UTC |
| Extended five-vantage campaign | 16 August 2026, 03:46–19:57 UTC |
| Telconet operator control | 7 September 2026, 22:00–23:07 UTC |
| Manual validation, rounds 1–2 | 25 August, 27 August, 1–2 September 2026 |
| ACT round | 8 September 2026 |

Those stamps are inside the raw JSON, CSV and metadata files, they are consistent with one another, and they can be checked without trusting this repository's history or its author. `CHECKSUMS.txt` fixes the content of every file, and the Zenodo record fixes the date of each published version.

---

## What this contains

The study measures two barriers across 126 university home pages: 63 Ecuadorian institutions, which are the complete national census, and 63 benchmark institutions drawn from the consensus of three international rankings. The first barrier is WCAG 2.2 conformance, audited with axe-core 4.13.0 in a real browser. The second is the setting of tracking cookies before any interaction with a consent interface.

The deposit holds **two reported measurements that must not be mixed**:

**Single-pass audit**, 14 August 2026. One visit to each of the 126 sites, from a vantage point in Ecuador. This is the source of every accessibility figure and of the between-group comparison. Canonical file: `data/raw/accessibility/results.json`.

**Multi-vantage replication**, 15 August 2026. The same protocol repeated from four geographic locations, with three valid passes at each. This is the source of the contrast between jurisdictions. Files in `data/raw/tracking/`.

The two differ in date, in the set of retained sites and in consolidation rule, and their tracking figures are not interchangeable. `CODEBOOK.md` sets out the relation between them.

Two further campaigns are released but **not analysed in the article**: an extended five-vantage campaign of 16 August, and an operator control from a second Ecuadorian ISP on 7 September. Both are described below.

---

## Structure

```
data/
  raw/
    accessibility/    results.json, results.csv
                      Single pass, 126 sites, 14 August 2026.
    appendix_documentary_tables.tex
                      the two appendix tables of the article, deposited
                      verbatim; source of the documentary matrix.
    census/           universities.json           the 126 audited sites
                      tops.json                   top 75 of each ranking edition
                      selection63_benchmark.json  consensus defining the benchmark group
    tracking/         39 files of the reported multi-vantage replication:
                        results_{EC,EU,GB,US}_r*.{json,csv}
                        meta_*.json  public IP, geolocation and versions per pass
    tracking_extended/  48 files of a later five-vantage campaign, including
                        Switzerland. NOT analysed in the article.
    tracking_telconet/  9 files of an operator control from a second Ecuadorian
                        ISP. NOT analysed in the article.
  manual/             manual validation of three success criteria on 15 sites:
                        four coding rounds, 39 CSV tables, 45 screenshots,
                        the collection instruments and their data dictionary.
                        See data/manual/README.md.
  processed/          fourteen derived tables; see CODEBOOK.md
  interim/            created when the code runs; not versioned
code/
  collection/         audit.js               single-pass audit
                      audit_multivantage.js  audit by vantage point
                      run.bat, INSTALL.bat
                      axe/                   dependencies of the single pass
                      extended/              instrument and launchers of the
                                             five-vantage campaign
  analysis/           sixteen scripts; see "Reproduction"
docs/
  reports/            four HTML cookie reports
figures/              the six figures of the article, in PDF
CODEBOOK.md           definition of every column of every table
CHECKSUMS.txt         SHA-256 of every file in the deposit
```

**On language.** File and directory names are in English. Inside the files the situation is mixed and deliberate: the CSV tables under `data/manual/` carry English column names, while the raw JSON keys, the columns of `data/raw/` and `data/processed/`, and the code comments remain in Spanish, the working language of the project. Coded **values** are Spanish throughout (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `1`/`P`/`0`, `REVISAR`). `CODEBOOK.md` translates and defines every one of them.

---

## Vantage points

The reported replication uses four locations, all measured on 15 August 2026.

| Code | Location | Network | Passes |
|---|---|---|---|
| `EC` | Cuenca, Ecuador | residential, ETAPA EP, AS27668 | r1, r2, r3 |
| `EU` | Frankfurt, Germany | data centre, AS14061 and AS46475 | r1, r2, r3 |
| `GB` | London, United Kingdom | data centre, AS21859 | r2, r3, r4 |
| `US` | Miami, United States | data centre, AS46475 | r1, r2, r3 |

Pass `GB_r1` was discarded because the VPN had not yet switched country. The instrument warns at the start of a pass when the detected country does not match the one declared, waits, and then aborts at the first periodic location check if the mismatch persists: `GB_r1` stopped after 25 sites, with `estado: "mal"` recorded in its metadata and no `fin` timestamp. Its files remain in the deposit as evidence that the control mechanism worked; the analysis excludes them and `r4` is its replacement.

Each `meta_*.json` records seven location checks per pass — at the start, after every 25 sites and at the end — with the public IP observed, its geolocation and the exact versions of axe-core, Playwright and Node. All 84 checks across the twelve valid passes match the declared vantage point. In 21 of those 84 the second geolocation service returned an error and the check rests on a single reading; the readings that did succeed are consistent throughout.

### The extended five-vantage campaign

`data/raw/tracking_extended/` holds a later campaign, 16 August 2026, that adds a Swiss vantage point and uses a more recent build of the instrument. **The article does not analyse it.** It is released because the measurements exist and are valid, not as support for any figure in the text. It is not an extension of the reported campaign but an independent measurement, with a different instrument, a different set of passes and a different date. Any analysis using it must treat it separately.

### The Telconet operator control

`data/raw/tracking_telconet/` holds three passes over the 126 sites from a residential Ecuadorian connection of Telconet S.A. (AS27947, Guayaquil), on 7 September 2026. Its purpose is narrow: the reported campaign measured the Ecuadorian vantage point from ETAPA EP (AS27668, Cuenca), and this series checks whether the Ecuadorian result depends on the network operator. **The article does not analyse it**, and it must not be merged with either of the campaigns above. See `data/raw/tracking_telconet/READ_ME.md`.

---

## Manual validation

`data/manual/` holds the manual verification of three WCAG 2.2 success criteria — 1.1.1 non-text content, 1.4.3 contrast (minimum) and 2.4.4 link purpose (in context) — on a subsample of 15 sites, seven from the benchmark group and eight from the Ecuadorian census.

It contains four coding rounds that **must not be merged**, because each used a different coding scheme and the difference between them is itself a finding: a first round by ten evaluators, a partial second coding of five sites by an eleventh, a better documented recoding of all fifteen, and a final round anchored in the W3C Accessibility Conformance Testing (ACT) Rules that codes every applicable element rather than a sampled proportion. `data/manual/README.md` sets out the agreement between rounds and what it does and does not establish.

The 45 screenshots in `data/manual/captures/` are the evidence behind the first two rounds.

---

## Reproduction

Node.js and Python 3. The versions that produced the published results are pinned in `code/collection/package.json` (axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1) and in `code/analysis/requirements.txt` (Python 3.10.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9). The September operator control ran on Node v24.12.0 on a different machine; its metadata records this.

### Collection

```bash
cd code/collection
npm install
node audit.js                                     # single pass
node audit_multivantage.js --vantage=EC --run=1   # one pass of one vantage point
```

`audit.js` reads the census and writes its output incrementally; if interrupted, running it again resumes where it stopped. `audit_multivantage.js` checks the geolocation of the public IP before starting and at every periodic check, and aborts the pass if the location stops matching the vantage point declared.

### Analysis

All scripts in `code/analysis/` are run **from that directory** and find their data by relative paths.

```bash
cd code/analysis
pip install -r requirements.txt

python build_entries.py              # rebuilds the intermediate inputs
python reconcile.py                  # cookies_126_sites_v2, reconciliation_changes
python qa_cookies.py                 # qa_irregularities
python rebuild_cookies.py ../../data/raw/accessibility ../../data/processed
python study.py                      # study_126_sites, study_rules_per_site
python verify_single_pass.py         # association between the two barriers
python sensitivity_sampling.py       # sensitivity of the benchmark group
python figures_uais.py               # five of the six figures
python fig_vantage.py                # vendor-by-vantage figure
python verify_multivantage.py        # the whole multi-vantage results section
python sensitivity_inclusion.py ../../data/raw/tracking
python kappa_wcag.py                 # agreement of the manual validation
python extract_documentary_matrix.py # documentary matrix from the appendices
python power_analysis.py             # statistical power of the comparisons
python normalise_acronym.py          # acronym normalisation across the deposit
python verify_live_divergence.py     # automated pass vs live check: 39 = 35 + 4
```

`extract_documentary_matrix.py` reads `data/raw/appendix_documentary_tables.tex`, the two appendix tables of the article deposited verbatim, and derives the documentary matrix from them. It aborts if the counts it obtains do not match the ones the article reports. The article itself is not deposited; only the two tables the matrix is derived from, so that the derivation is auditable rather than asserted.

`verify_multivantage.py` reproduces the multi-vantage results section: proportions per vantage point with Wilson intervals, exact McNemar test for each pair, Holm correction across the six comparisons, Cochran's Q, rendering controls and cookie attribution by vendor. `sensitivity_inclusion.py` repeats that analysis under the three defensible inclusion rules and shows that the ordering of the vantage points does not depend on that choice.

### Integrity check

```bash
sha256sum -c CHECKSUMS.txt
```

In PowerShell:

```powershell
Get-Content CHECKSUMS.txt | ForEach-Object {
    $h, $r = $_ -split '  ', 2
    $a = (Get-FileHash -LiteralPath $r -Algorithm SHA256).Hash.ToLower()
    if ($a -ne $h) { "MISMATCH: $r" }
}
```

---

## Scope and limits

The measurements capture each institution's home page on a specific date. Sites change, so a later run will not reproduce the same values: what is deposited is evidence of what was observed, not a stable property of the sites.

Automated auditing detects a subset of conformance failures. A site with no violations detected by axe-core is not a conformant site; it is a site with no failures detectable that way. That is the reason for the manual validation, and for the disagreement between rounds that it documents.

Five sites fall out of the paired analysis across vantage points because they failed to load on at least one pass. The article names each of them, with the cause and a sensitivity analysis of that exclusion.

The `https` field of `results.json` reports `true` for all 126 sites. This is an artefact: Playwright rejects invalid certificates as load failures, so a site with a deficient chain never reaches the audit at all. A manual browser check identified the five Ecuadorian sites concerned; they are recorded in `data/processed/tls_deficiencies_august2026.csv`.

The tracking-cookie taxonomy was extended after collection, once the observed cookie names had been inspected, and was applied by reclassifying the stored names, with no re-measurement. `data/processed/cookies_unclassified_names.csv` lists the 243 distinct names that match no known family, so that the classification can be contested.

---

## Licences

Data and documentation under **CC BY 4.0** (`LICENSE`). Code under **MIT** (`LICENSE-CODE`).

The HTML reports in `docs/reports/` include cookie and vendor names observed on third-party sites. They are published as evidence of the observation; rights over the content of those sites belong to their owners.

---

## Authors

- Gleiston Guerrero-Ulloa — Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo, Ecuador · [0000-0001-5990-2357](https://orcid.org/0000-0001-5990-2357)
- Andrea Zúñiga Paredes — Ministerio de Educación del Ecuador, Quito · [0000-0003-4042-1523](https://orcid.org/0000-0003-4042-1523)
- Efraín Díaz-Macías — Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo, Ecuador · [0000-0003-4087-029X](https://orcid.org/0000-0003-4087-029X)

## Citation

Metadata is in `CITATION.cff`. Cite the concept DOI of the Zenodo record, which always points to the latest version, not the DOI of a specific version.
