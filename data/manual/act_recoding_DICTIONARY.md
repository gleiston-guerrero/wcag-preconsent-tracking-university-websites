# ACT recoding sheet — column dictionary

*Versión en español: [act_recoding_DICTIONARY_ES.md](act_recoding_DICTIONARY_ES.md)*

One row **per applicable element**, not per site. The template carries one starter row
per site and rule; the evaluator adds as many rows as there are applicable elements.

| Column | What to write |
|---|---|
| `id`, `group`, `abbr`, `url` | Site identification, already filled in |
| `criterion` | 1.1.1, 1.4.3 or 2.4.4 |
| `act_rule` | Six-character identifier of the ACT rule |
| `rule_name` | Official name of the rule, already filled in |
| `element_n` | Sequential number of the element within the rule and the site |
| `selector_or_description` | CSS selector or a description that allows the element to be found again |
| `applicable` | `si` or `no`. **The rule decides this, not the evaluator.** If `no`, leave `outcome` empty and state in `notes` which of the rule's exclusions applies |
| `outcome` | `cumple` or `falla`. There is no intermediate category |
| `measured_value` | For 1.4.3 only: contrast ratio to two decimal places. Empty for the others |
| `programmatic_context` | For 2.4.4 (`5effbb`) only: the paragraph, list item or table cell with its header that supplies the context. A generic wrapping element is **not** context |
| `evaluator_code` | Evaluator code. Do not write names |
| `date` | YYYY-MM-DD |
| `capture` | File name of the evidence |
| `notes` | Brief justification. Required when `applicable=no` or `outcome=falla` |

> **Column names** are in English, in line with the rest of the deposit. **Values** remain in Spanish (`mundo`/`ecuador`, `si`/`no`, `cumple`/`falla`, `REVISAR`), which is the vocabulary the CODEBOOK defines.

## How this aggregates to the site level

A criterion is **not satisfied** at a site if any applicable element of any of its rules
has `outcome=falla`. If every applicable element passes, it is satisfied. If there is no
applicable element at all, the criterion is `not applicable` for that site.

No proportion of failures is computed and no sample size is fixed: every applicable
element is examined. That removes both the partial category and the argument about
sampling, which were the two sources of disagreement between the earlier coders.

## Thresholds and exclusions, rule by rule

**afw4f7, contrast.** Applies to any *visible* character of a text node. Threshold:
4.5:1, or 3.0:1 for large text. Inapplicable: a disabled ancestor, the label of a
disabled control, purely decorative text, text that expresses nothing in human language.
Visually hidden text is not a visible character and therefore falls outside the rule:
**it is not excluded by the evaluator's judgement, it is excluded by definition**.

**23a2a8, image accessible name.** Applies to `img` and to elements with the semantic
role `img`, except those that are programmatically hidden. Passes if the accessible name
is not empty, or if the role is `none` or `presentation`.

**qt1vmo, descriptive name.** Applies to visible `img`, `canvas` and `svg` with a
non-empty accessible name. Inapplicable if an ancestor is named by the author, or if the
image request is not fully available. Passes if the name serves a purpose equivalent to
the non-text content.

**e88epe, decorative image.** An image outside the accessibility tree is treated as
decorative.

**c487ae, link name.** Applies to every link included in the accessibility tree. Passes
if the accessible name is not empty.

**5effbb, link is descriptive in context.** Applies to every link in the accessibility
tree with a non-empty accessible name. Passes if the name, together with its
*programmatically determined link context*, describes the purpose of the link. That
context is a closed list fixed by WCAG: paragraph, list item, table cell with its header.
A `div` or an `article` wrapping the page is **not** context.

**fd3a94, links with identical names.** Links with an identical accessible name in the
same context must serve an equivalent purpose.
