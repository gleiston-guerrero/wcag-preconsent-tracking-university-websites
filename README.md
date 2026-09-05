# WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites

*Versión en español: [README_ES.md](README_ES.md)*

Data, evidence and code for the article *Two barriers to equitable access: WCAG conformance and pre-consent tracking on Ecuadorian and top-ranked university websites*, submitted to *Universal Access in the Information Society* (Springer Nature).

**Deposit DOI:** `10.5281/zenodo.XXXXXXX` *(pending until the Zenodo record is published)*

---

## What this contains

The study measures two barriers across 126 university home pages: 63 Ecuadorian institutions, which are the complete national census, and 63 benchmark institutions drawn from the consensus of three international rankings. The first barrier is WCAG 2.2 conformance, audited with axe-core 4.13.0 in a real browser. The second is the setting of tracking cookies before any interaction with a consent interface.

The deposit holds **two distinct measurements that must not be mixed**:

**Single-pass audit**, 14 August 2026. One visit to each of the 126 sites, from a vantage point in Ecuador. This is the source of every accessibility figure and of the between-group comparison. Canonical file: `data/raw/accessibility/resultados.json`.

**Multi-vantage replication**, 15 August 2026. The same protocol repeated from four geographic locations, with three valid passes at each. This is the source of the contrast between jurisdictions. Files in `data/raw/tracking/`.

The two differ in date, in the set of retained sites and in consolidation rule. The article says so explicitly: their tracking figures are not interchangeable. `CODEBOOK.md` sets out the relation between them.

---

## Structure

```
data/
  raw/
    accessibility/    resultados.json, resultados.csv
                      Single pass, 126 sites, 14 August 2026.
    census/           universidades.json      the 126 audited sites
                      tops.json               top 75 of each ranking edition
                      seleccion63_mundo.json  consensus defining the benchmark group
    tracking/         39 files of the reported multi-vantage replication:
                        resultados_{EC,EU,GB,US}_r*.{json,csv}
                        meta_*.json  public IP, geolocation and versions per pass
    tracking_extended/  48 files of a later five-vantage campaign, including
                        Switzerland, NOT analysed in the article. See below.
  processed/          eleven derived tables; see CODEBOOK.md
  interim/            created when the code runs; not versioned
code/
  collection/         auditar.js             single-pass audit
                      auditar_multipunto.js  audit by vantage point
                      ejecutar.bat, INSTALAR.bat
                      axe/                   dependencies of the single pass
                      extended/              instrument and launchers of the
                                             five-vantage campaign
  analysis/           eleven scripts; see "Reproduction"
docs/
  reports/            four HTML cookie reports
figures/              the six figures of the article, in PDF
CODEBOOK.md           definition of every column of every table
CHECKSUMS.txt         SHA-256 of every file in the deposit
```

Note that file names, column names and code comments are in Spanish, the working language of the project. `CODEBOOK.md` translates and defines each of them.

---

## Vantage points

The reported replication uses four locations, all measured on 15 August 2026.

| Code | Location | Network | Passes |
|---|---|---|---|
| `EC` | Cuenca, Ecuador | residential, ETAPA EP, AS27668 | r1, r2, r3 |
| `EU` | Frankfurt, Germany | data centre, AS14061 and AS46475 | r1, r2, r3 |
| `GB` | London, United Kingdom | data centre, AS21859 | r2, r3, r4 |
| `US` | Miami, United States | data centre, AS46475 | r1, r2, r3 |

Pass `GB_r1` was aborted automatically because the VPN had not yet switched country, and was discarded; its replacement is `r4`. Its files remain in the deposit as evidence that the control mechanism worked, but the analysis excludes them.

Each `meta_*.json` records seven location checks per pass, at the start, after every 25 sites and at the end, with the public IP observed, its geolocation according to two independent services, and the exact versions of axe-core, Playwright and Node. All 84 checks across the twelve valid passes match the declared vantage point.

### The extended five-vantage campaign

`data/raw/tracking_extended/` holds a later campaign that adds a Swiss vantage point and uses a more recent version of the instrument. **The article does not analyse it.** It is released because the measurements exist and are valid, not as support for any figure in the text. It is not an extension of the reported campaign but an independent measurement, with a different instrument, a different set of passes and a different date. Any analysis using it must treat it separately.

---

## Reproduction

Node.js and Python 3. The versions that produced the published results are pinned in `code/collection/package.json` (axe-core 4.13.0, Playwright 1.62.1, Node v24.18.1) and in `code/analysis/requirements.txt` (Python 3.10.3, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.9).

### Collection

```bash
cd code/collection
npm install
node auditar.js                                   # single pass
node auditar_multipunto.js --vantage=EC --run=1   # one pass of one vantage point
```

`auditar.js` reads the census and writes its output incrementally; if interrupted, running it again resumes where it stopped. `auditar_multipunto.js` checks the geolocation of the public IP and aborts if it does not match the vantage point given, so the measurement has to be taken from the declared location.

### Analysis

All scripts in `code/analysis/` are run **from that directory** and find their data by relative paths.

```bash
cd code/analysis
pip install -r requirements.txt

python construir_entradas.py      # rebuilds the intermediate inputs
python reconciliar.py             # cookies_126_sitios_v2, cambios_reconciliacion
python qa_cookies.py              # qa_irregularidades
python reconstruir_cookies.py ../../data/raw/accessibility ../../data/processed
python estudio.py                 # estudio_126_sitios, estudio_reglas_por_sitio
python verificar_pasada_unica.py  # association between the two barriers
python sensibilidad_muestreo.py   # sensitivity of the benchmark group
python figuras_uais.py            # five of the six figures
python fig_vantage.py             # vendor-by-vantage figure
python verificar_multipunto.py    # the whole multi-vantage results section
python sensibilidad_inclusion.py ../../data/raw/tracking
```

`verificar_multipunto.py` reproduces the multi-vantage results section: proportions per vantage point with Wilson intervals, exact McNemar test for each pair, Holm correction across the six comparisons, Cochran's Q, rendering controls and cookie attribution by vendor. `sensibilidad_inclusion.py` repeats that analysis under the three defensible inclusion rules and shows that the ordering of the vantage points does not depend on that choice.

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

Automated auditing detects a subset of conformance failures. A site with no violations detected by axe-core is not a conformant site; it is a site with no failures detectable that way.

Five sites fall out of the paired analysis across vantage points because they failed to load on at least one pass. The article names each of them, with the cause and a sensitivity analysis of that exclusion.

The tracking-cookie taxonomy was extended after collection, once the observed cookie names had been inspected, and was applied by reclassifying the stored names, with no re-measurement. `data/processed/cookies_nombres_sin_clasificar.csv` lists the 243 distinct names that match no known family, so that the classification can be contested.

---

## Licences

Data and documentation under **CC BY 4.0** (`LICENSE`). Code under **MIT** (`LICENSE-CODE`).

The HTML reports in `docs/reports/` include cookie and vendor names observed on third-party sites. They are published as evidence of the observation; rights over the content of those sites belong to their owners.

---

## Citation

Metadata is in `CITATION.cff`. Cite the concept DOI of the Zenodo record, which always points to the latest version, not the DOI of a specific version.
