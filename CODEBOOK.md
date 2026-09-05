# Codebook

*Versión en español: [CODEBOOK_ES.md](CODEBOOK_ES.md)*

Documents every data file in the deposit. UTF-8 encoding. Empty fields mean absence of data, not zero.

File names, column names and code comments are in Spanish, the working language of the project. This codebook translates and defines each of them.

---

## 1. The two measurements

The deposit holds two measurements of the same phenomenon, taken a day apart with different designs. **Their tracking figures are not interchangeable.** Before combining any two tables, be clear which one they come from.

| | Single pass | Multi-vantage replication |
|---|---|---|
| Date | 14 August 2026 | 15 August 2026 |
| Vantage points | one, Ecuador | four: EC, EU, GB, US |
| Visits per site | one | three per vantage point |
| Consolidation | none | majority over the three passes |
| Sites | all 126 | 121 successful in all twelve passes |
| Source | `data/raw/accessibility/` | `data/raw/tracking/` |
| Supports | accessibility and between-group comparison | contrast between jurisdictions |

In the single pass, under the extended taxonomy, pre-consent tracking is observed at 41 of the 63 Ecuadorian sites and 43 of the 63 benchmark sites. In the replication, over the 121 retained sites, it is observed at 82 from Ecuador, 79 from the United States, 76 from the United Kingdom and 73 from Germany. Neither figure replaces the other: the first supports the between-group comparison, the second the within-site comparison across conditions.

A third figure exists, the live verification held in the `*_verificacion` columns of `cookies_126_sitios_v3.csv`, obtained by manual inspection on other dates. It differs from the automated measurement at 39 of the 126 sites. See section 4.

---

## 2. Common categories

**Group** (`grupo`): `Ecuador` or `Mundo` in the JSON files; `ecuador` or `mundo` in the derived tables. *Mundo* means the benchmark group.

**Site identifier** (`id`): integer from 1 to 126, stable across every file in the deposit. It joins any table to any other. The one exception is `matriz_documental.csv`, which carries a position within its group table rather than the global identifier.

**Yes/no**: `yes` or `no` in the derived CSV tables; boolean in the JSON files. The documentary matrix uses `si` / `no` instead, since it was transcribed from the article.

**Conformance level** (`nivel`, `max_nivel_sin_fallo`): `A`, `AA` or `AAA`, per WCAG 2.2. The AAA rules were active during the audit; the dominant rule at that level is enhanced contrast, success criterion 1.4.6, requiring a 7:1 ratio.

**Principle** (`principio`): `Perceptible`, `Operable`, `Comprensible` (Understandable) or `Robusto` (Robust), the four WCAG principles.

**Vantage point** (`vantage`, file-name suffix): `EC` Ecuador, `EU` Germany, `GB` United Kingdom, `US` United States. `CH`, Switzerland, appears only in `tracking_extended/`.

**Tracking cookie**: a cookie name matching one of the taxonomy patterns. The original list covered Google, Meta, TikTok, Microsoft Clarity, Hotjar, Matomo, Baidu and smaller families. The extended list adds the LinkedIn Insight Tag, the full Microsoft advertising family, TapAd, StackAdapt, Snapchat and Sourcebuster. Both lists, as regular expressions, are in `code/analysis/verificar_multipunto.py`, lines 7 to 18. The extended list governs every published figure.

---

## 3. Raw data

### `data/raw/accessibility/resultados.json`

A JSON array of 126 objects, one per site, ordered by `id`. This is the ground truth of the single-pass audit: every accessibility-derived table in `data/processed/` is computed from it.

| Field | Type | Description |
|---|---|---|
| `id` | integer | Site identifier. |
| `grupo` | text | `Ecuador` or `Mundo`. |
| `sigla` | text | Institutional acronym. |
| `nombre` | text | Full name. |
| `pais` | text | Country of the institution. |
| `url` | text | Home page audited. |
| `ok` | boolean | The page loaded. True for all 126. |
| `https` | boolean | The page was served over HTTPS. **Not** the same as the documentary indicator of Figure 1: see `tls_deficiencias_agosto2026.csv`. |
| `axe_version` | text | Engine version. `4.13.0` for all 126. |
| `fecha` | datetime | Time of the visit, ISO 8601. |
| `cookies` | object | See below. |
| `accesibilidad` | object | See below. |

**`cookies`**

| Field | Type | Description |
|---|---|---|
| `total_pre` | integer | Cookies present before any interaction. |
| `rastreo_pre` | integer | Of those, how many are tracking cookies under the base taxonomy. |
| `nombres_pre` | list | Names of all cookies observed. |
| `nombres_rastreo` | list | Names classified as tracking. |
| `cmp` | list | Consent management platforms detected. |
| `banner` | boolean | A cookie notice was displayed. |

**`accesibilidad`**

| Field | Type | Description |
|---|---|---|
| `title` | text | Contents of `<title>`. |
| `lang` | text | Document `lang` attribute. |
| `viewport` | boolean | A viewport meta tag exists. |
| `skipLink` | boolean | A skip-to-content link exists. |
| `violaciones` | integer | axe-core rules with at least one failing node. |
| `nodos` | integer | Failing nodes, summed over all rules. |
| `porPrincipio` | object | Failing nodes by WCAG principle. |
| `porNivel` | object | Failing nodes by level: `A`, `AA`, `AAA`. |
| `maxNivelSinFallo` | text | Highest level with no detected failure. |
| `incompletos` | integer | Checks axe-core could not resolve, needing human review. |
| `passes` | integer | Rules passed. |
| `reglas` | list | One entry per failing rule, with `id`, `impacto` (impact), `criterio` (success criterion), `principio`, `nivel`, `nodos` and `ayuda` (help URL). |

### `data/raw/accessibility/resultados.csv`

A flattened view of the JSON above, 126 rows, for quick inspection. Columns: `id`, `grupo`, `sigla`, `pais`, `url`, `ok`, `error`, `title`, `lang`, `viewport`, `https`, `cookies_pre`, `rastreo_pre`, `nombres_rastreo`, `cmp`, `banner`, `ax_violaciones`, `ax_nodos`, `nivelA_nodos`, `nivelAA_nodos`, `nivelAAA_nodos`, `Perceptible`, `Operable`, `Comprensible`, `Robusto`, `max_nivel_sin_fallo_auto`. For analysis use `estudio_126_sitios.csv`, which is more complete.

### `data/raw/tracking/resultados_<VANTAGE>_r<N>.json`

Thirteen files, one per pass. Same structure as `resultados.json`, plus two fields: `vantage` and `run`. Pass `GB_r1` is truncated, 49,546 bytes against the usual 280,000, because it aborted when the VPN had not switched country; it is kept as evidence and excluded from the analysis.

### `data/raw/tracking/meta_<VANTAGE>_r<N>.json`

One file per pass, holding the provenance evidence.

| Field | Description |
|---|---|
| `vantage`, `run` | Vantage point and pass number. |
| `inicio`, `fin`, `duracion_min` | Actual start, end and duration of the pass. |
| `geolocalizacion` | Initial readings from `ipinfo.io` and `ipwho.is`: IP, country, city and organisation. |
| `coincide_con_vantage` | The observed location matches the declared one. |
| `controles_de_ubicacion` | Seven checks per pass: at the start, after sites 25, 50, 75, 100 and 125, and at the end. Each with both readings and its verdict. |
| `configuracion` | Script wait, load timeout, retries, whether AAA rules were active, whether cookies were measured, and the user-agent string. |
| `axe_core`, `playwright`, `node`, `plataforma` | Exact environment versions. |
| `sitios`, `exitosos`, `fallidos` | Counts for the pass. |

### `data/raw/tracking_extended/`

Forty-eight files of the later five-vantage campaign, same structure. **They support no figure in the article.** See the README.

### `data/raw/census/`

`universidades.json` is the census of the 126 audited sites, with acronym, name, country and URL. `tops.json` holds the top 75 of each ranking edition used. `seleccion63_mundo.json` documents the consensus across the three rankings that defines the benchmark group.

---

## 4. Derived tables

### `estudio_126_sitios.csv` — 126 rows, 32 columns

Canonical flattening of `resultados.json`, produced by `estudio.py`.

| Column | Description |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `pais`, `url` | Site identification. |
| `fecha`, `axe_version`, `ok`, `https` | Visit metadata. |
| `cookies_total_pre` | Cookies before consent. |
| `cookies_rastreo_pre` | Of those, tracking cookies under the base taxonomy. |
| `nombres_pre`, `nombres_rastreo` | Names, separated by ` \| `. |
| `cmp`, `banner` | Consent platform and notice. |
| `title`, `lang`, `viewport`, `skip_link` | Structural indicators. |
| `ax_violaciones`, `ax_nodos` | Rules failed and failing nodes. |
| `nodos_A`, `nodos_AA`, `nodos_AAA` | Failing nodes by level. |
| `perceptible`, `operable`, `comprensible`, `robusto` | Failing nodes by principle. |
| `max_nivel_sin_fallo` | Highest level with no failures. |
| `incompletos`, `passes` | Unresolved checks and rules passed. |

### `estudio_reglas_por_sitio.csv` — 441 rows, 10 columns

One row per site and failed rule. Same script.

| Column | Description |
|---|---|
| `id`, `grupo`, `sigla` | Site. |
| `regla` | axe-core rule identifier, for example `image-alt`. |
| `impacto` | Severity assigned by axe-core: `minor`, `moderate`, `serious`, `critical`. |
| `criterio` | Associated WCAG success criterion. Empty when the rule maps to none. |
| `principio`, `nivel` | Principle and level of the criterion. |
| `nodos` | Elements failing that rule on that site. |
| `ayuda` | URL of the rule documentation. |

### `cookies_126_sitios_v3.csv` — 126 rows, 24 columns

The cookie table of the article, with both taxonomies in separate columns. Produced by `reconstruir_cookies.py` from `resultados.json` and `cookies_126_sitios_v2.csv`.

| Column | Description |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | Identification. |
| `fecha` | Time of the automated measurement. |
| `cookies_antes_consentir` | Cookies observed before consent. |
| `nombres_cookies` | Names, separated by ` \| `. |
| `n_nombres_listados` | How many names the previous field holds. |
| `rastreo_base` | Tracking under the original taxonomy. |
| `rastreo` | Tracking under the extended taxonomy. **This is the column behind the article's figures.** |
| `proveedores_rastreo` | Vendor families recognised on that site. |
| `procedencia_rastreo` | Why it was classified that way: which source supplied the datum and which taxonomy decided. |
| `banner_estudio`, `cmp_estudio` | Notice and platform detected in the automated measurement. |
| `pais`, `region`, `ciudad`, `tipo` | Institutional attributes. |
| `cmp_verificacion`, `banner_verificacion`, `fuente_verificacion` | Results of the manual live verification, on a different date. |
| `polcookies_estudio` | A cookie policy exists. |
| `nota_documental` | Qualitative note on the documents the institution publishes. |

The difference between `rastreo_base` and `rastreo` is a single Ecuadorian site, which crosses the threshold because its only matching cookies belong to the Sourcebuster family added in the extended list. The Ecuadorian count therefore rises from 40 to 41; the benchmark count stays at 43.

The `*_verificacion` columns come from a manual inspection distinct from the automated measurement. They disagree with the `rastreo` column at 39 of the 126 sites: 34 where the automated measurement detects tracking and the live verification does not, and 5 the other way round. Neither is in error: they are observations at different moments of sites that change. **Do not mix the two columns in a single count.**

### `cookies_126_sitios_v2.csv` — 126 rows

Earlier version, a required input of `reconstruir_cookies.py`. It is released because without it v3 cannot be reproduced. Do not use it directly for analysis.

### `cookies_nombres_sin_clasificar.csv` — 243 rows

Observed cookie names matching no family in the taxonomy, with the number of sites where each appears. This is the evidence behind the taxonomic decision: it allows any name to be contested.

| Column | Description |
|---|---|
| `nombre_cookie` | Observed name. |
| `sitios_en_que_aparece` | Number of distinct sites. |

### `cookies_divergencias_v2.csv` — 14 rows

Quality control. Sites where the v2 table listed cookie names absent from the raw JSON, a sign of data loss at an intermediate stage.

| Column | Description |
|---|---|
| `id`, `sigla`, `grupo` | Site. |
| `nombres_no_presentes_en_crudo` | Names affected. |

### `cambios_reconciliacion.csv` — 68 rows

Audit trail of the reconciliation between the inventory and the HTML reports. Produced by `reconciliar.py`.

| Column | Description |
|---|---|
| `sigla` | Institution. |
| `campo` | Field changed. |
| `antes`, `despues` | Previous and new value. |
| `motivo` | Rule that justified the change. |

### `qa_irregularidades.csv` — 228 rows

Issues found in the inventory, with a type code and a suggested action. Produced by `qa_cookies.py`. Released as evidence of quality control, not as analysis data.

| Column | Description |
|---|---|
| `id`, `grupo`, `sigla`, `universidad`, `sitio` | Site. |
| `codigo` | Issue type, `I1` to `I9`. |
| `irregularidad` | Description. |
| `valor_actual` | The value that triggered it. |
| `accion_requerida` | Suggested correction. |

### `reporte_cookies_nacionales.csv` — 63 rows · `reporte_cookies_extranjeras.csv` — 63 rows

Inventories by group, holding the manual verification fields. They are inputs to `construir_entradas.py`, which merges them to rebuild the 126-site table. The cookie columns of these files come from the **live verification**, not from the automated measurement.

National: `#`, `Universidad`, `Sigla`, `Tipo`, `Ciudad`, `Sitio`, `Verificacion`, `Cookies_antes_consentir`, `Nombres_cookies`, `Rastreo`, `CMP_live`, `Banner_live`, `Banner_estudio`, `PolCookies_estudio`.

Foreign: `#`, `Universidad`, `Sigla`, `Pais`, `Region`, `Sitio`, `Cookies_antes_consentir`, `Nombres_cookies`, `CMP_detectada`, `Banner_visible`, `Banner_estudio`, `PolCookies_estudio`.

### `matriz_documental.csv` — 126 rows

Documentary indicators, coded by inspecting each institution's first-level privacy notice in August 2026. These are the counts behind Figure 1 of the article. Produced by `extraer_matriz_documental.py`; see the provenance note below.

| Column | Description |
|---|---|
| `grupo` | `mundo` (benchmark) or `ecuador`. |
| `#` | Position within its group table. **Not** the global site `id`. |
| `Abbr.` | Institutional acronym. Joins to `sigla` in the other tables. |
| `C` | Country, ISO 3166-1 alpha-2. Benchmark group only. |
| `QS`, `THE`, `ARWU` | Position in each ranking, `--` if absent from that top 75. Benchmark group only. |
| `Type` | Public or private. Ecuadorian group only. |
| `Not.` (benchmark) / `Notice` (Ecuador) | A first-level privacy notice is published. |
| `Frm.` / `LOPDP` | A specific legal instrument is named. |
| `Rts.` / `Rights` | Data-subject rights are enumerated. |
| `DPO` | A privacy contact or data protection officer is identified. |
| `Ckp.` | A dedicated cookie policy is published. Benchmark group only. |
| `Acc.` | An accessibility statement or accessibility tools are declared. |
| `Transp.` | Transparency under the Ecuadorian access-to-information act (LOTAIP). Ecuadorian group only. It is **not** transport security. |

Values: `si` present, `no` absent, `parcial` limited scope or a generic framework, `nv` not verifiable by this method, and empty where the column does not apply to that group. A trailing `*` marks the two cells corrected after the manual re-verification reported in the article.

The two groups were coded with partly different column sets, which is why some columns are empty for one group and not the other. The Ecuadorian group carries between two and six `nv` cells per indicator; the benchmark group carries none. That asymmetry is itself a finding and is invisible in the aggregate percentages.

**Provenance.** These indicators were coded manually and published institution by institution in the article appendices. `extraer_matriz_documental.py` recovers them from the LaTeX source of the article, which is **not** part of this deposit, since the rights belong to the publisher. The script therefore cannot be run from this repository alone; it is released so the extraction is auditable, and its output is the table above. Run against the article source, it reproduces the five counts of Figure 1 exactly: 59 and 39 for the privacy notice, 47 and 31 for the framework cited, 47 and 35 for rights, 54 and 24 for the privacy contact, and 47 and 7 for the accessibility statement.

### `tls_deficiencias_agosto2026.csv` — 5 rows

The five Ecuadorian sites whose TLS chain was found deficient in the documentary check of August 2026. They are the difference between the 63 sites served over HTTPS and the 58 counted as having a valid certificate in Figure 1 and in the results table.

| Column | Description |
|---|---|
| `sigla` | Institutional acronym. |
| `universidad` | Full name. |
| `url` | Home page checked. |
| `observacion` | What was found in August 2026. |
| `fecha_observacion` | Month of the observation. |
| `verificacion_posterior` | Result of re-checking the chain on 5 September 2026. |

**Why this file exists.** This indicator was coded by inspecting each site in a browser, not by the automated auditor, and the two do not measure the same thing: the auditor's `https` field records that the page was served over HTTPS, and Playwright rejects an invalid certificate outright, so a broken chain would appear as a load failure rather than as `https: false`. That is why `resultados.json` shows `https: true` for all 126 sites while the article reports 58 of 63 for Ecuador.

All five certificates were valid when re-checked on 5 September 2026, having been renewed in the interval; one residual trace remains, in that the apex domain of ESPAM MFL still does not resolve and only the `www` host does. The August observation is therefore not reproducible today, which is a property of the object measured rather than a defect of the record: sites change, as stated in the README.

### `sensibilidad_inclusion.csv` — 3 rows

Result of the sensitivity analysis on the inclusion rule of the multi-vantage replication. One row per rule.

| Column | Description |
|---|---|
| `regla` | `R3` three valid passes per vantage point, the article's rule; `R2` at least two; `R1` at least one. |
| `n` | Sites retained under that rule. |
| `Q`, `p_Q` | Cochran's Q over the four vantage points and its p value, 3 degrees of freedom. |
| `marg_EC`, `marg_EU`, `marg_GB`, `marg_US` | Sites with tracking at each vantage point. |
| `p_<pair>` | Exact McNemar p value for each pair. |
| `pholm_<pair>` | The same value after Holm correction across the six comparisons. |

---

## 5. HTML reports

`docs/reports/` holds four browsable reports produced during fieldwork. They are not primary data, but they **are inputs to the code**: `construir_entradas.py` extracts from `reporte_cookies_combinado.html` and `anexo_universidades_cookies.html` the data embedded in their JavaScript `DATA` constant, which is needed to reproduce the cookie table chain. That is why they are released.

---

## 6. Dependency chain

What produces what, and from what.

```
resultados.json ────────────────────────────► estudio.py
                                                 ├─► estudio_126_sitios.csv
                                                 └─► estudio_reglas_por_sitio.csv

reporte_cookies_nacionales.csv   ┐
reporte_cookies_extranjeras.csv  ├─► construir_entradas.py ─► data/interim/
reporte_cookies_combinado.html   │                              _comb.json
anexo_universidades_cookies.html ┘                              _anex.json
                                                                cookies_126_sitios.csv
                                                                     │
data/interim/ ──────────────────► reconciliar.py ──────────────────┤
                                     ├─► cookies_126_sitios_v2.csv │
                                     └─► cambios_reconciliacion.csv│
                                                                    │
data/interim/ ──────────────────► qa_cookies.py ─► qa_irregularidades.csv

resultados.json + v2 ───────────► reconstruir_cookies.py
                                     ├─► cookies_126_sitios_v3.csv
                                     ├─► cookies_nombres_sin_clasificar.csv
                                     └─► cookies_divergencias_v2.csv

data/raw/tracking/ ─────────────► verificar_multipunto.py     (results section)
                                ► sensibilidad_inclusion.py   ─► sensibilidad_inclusion.csv

article appendices (external) ──► extraer_matriz_documental.py ─► matriz_documental.csv
```

Files in `data/interim/` are not versioned because `construir_entradas.py` regenerates them from material that is published. The article source is not part of the deposit, which is why the last step above cannot be run from this repository alone.
