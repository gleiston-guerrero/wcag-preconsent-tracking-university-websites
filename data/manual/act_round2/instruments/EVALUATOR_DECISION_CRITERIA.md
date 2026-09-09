# Decision criteria — rows marked REVISAR

*Versión en español: [EVALUATOR_DECISION_CRITERIA_ES.md](EVALUATOR_DECISION_CRITERIA_ES.md)*

The second evaluator's second document. Read it **after** running the script on
the fifteen sites and **before** filling in any cell.

The script has already decided everything the rule defines mechanically. What is
left are the rows marked `REVISAR`, where the ACT rule refers explicitly to a
person's judgement. This document sets out how to make that judgement.

Every example in this document is taken from the official W3C documentation of
the ACT rules. **None comes from the fifteen sites you are evaluating**, so as
not to condition your judgement.

---

## The single decision rule

In each `REVISAR` row, write one of two words in the `outcome` column:

| | |
|---|---|
| `cumple` | The element satisfies the rule's expectation |
| `falla` | It does not |

**There is no intermediate category.** Do not write "partial" or "unsure", and do
not leave the cell empty. If you are in doubt, choose and explain the doubt in
`justification`.

Always fill in the `justification` column with a sentence. That sentence is what
will make it possible to reconcile the discrepancies afterwards.

---

## Rule `qt1vmo` — an image's name is descriptive

**Official expectation:** the element's accessible name serves a purpose
equivalent to the non-text content.

**The question to ask yourself:** if someone could not see this image and heard
only this text, would they receive what the image communicates?

You are not asked whether the text is well written, nor whether it is long or
short, nor whether you like it. You are asked whether it **serves the same
purpose**.

### Official W3C examples

**Passes.** An image of the W3C logo with `alt="W3C logo"`. The text identifies
what the image shows.

**Fails.** The same image of the W3C logo with `alt="ERCIM logo"`. The text
describes the image incorrectly: it names a different organisation.

**Fails.** An `svg` showing the HTML5 logo with `aria-label="W3C"`. The name does
not correspond to what is depicted.

### What to do in practice

1. Open the address in the `src` column, or locate the element with the `selector`.
2. Look at the image.
3. Read the accessible name.
4. Decide whether the second serves the purpose of the first.

If the image does not load or you cannot locate it, write `falla` only if you are
certain; if you cannot see it, leave the row unfilled and **note it in your
incident note**. An unresolved row is preferable to one resolved blind.

### Cases you will meet and how to treat them

**Images containing text.** If the image is a poster, a logo with words, a table
or a chart with labels, the accessible name must convey that text. Ask yourself
whether all the information the image supplies arrives through the name.

**Illustrative photographs.** Decide whether the name conveys what the photograph
communicates in its context.

**Icons and small graphic elements.** Those the author has marked as decorative
were already resolved by the script and do not reach you.

---

## Rule `5effbb` — the link is descriptive in its context

**Official expectation:** the link's accessible name, together with its
*programmatically determined link context*, describes the purpose of the link.

### What programmatically determined context is

This is the most important part of the document, because it is where it is
easiest to go wrong.

The context is a **closed list** defined by WCAG. Only text that sits in the
following counts:

- the **paragraph** containing the link
- the **list item** containing it
- the **table cell** containing it, together with its header

A heading outside those elements is **not** context, nor is a `div` or an
`article` wrapping the section, nor text that appears nearby on screen, nor
anything you infer from the page's design.

The script has already extracted the valid context and placed it in the
`programmatic_context` column. When that column says `SIN CONTEXTO PROGRAMATICO`,
it means there is **none**: you must judge the accessible name on its own.

### Official W3C examples

**Passes.** `<a href="#desc">See the description of this product.</a>` The name
describes the purpose on its own.

**Passes.** `<p>See the description of <a href="#desc">this product</a>.</p>` The
name is "this product", which would not suffice on its own, but the paragraph
containing it is valid context and completes the description.

**Fails.** `<a href="#desc">More</a>` with no paragraph containing it. The name
does not describe the purpose and there is no context to complete it.

**Fails.** A link whose text is only understandable through information sitting in
**another** `p` element than the one containing the link. That text is not
programmatically determined context even if it reads right beside it.

### What to do in practice

Read the accessible name and the context in the column. Ask yourself: **could
someone who hears only this know where the link leads?**

A screen reader user can navigate by jumping from link to link, without hearing
the rest of the page. That is the situation the rule contemplates.

---

## Rule `fd3a94` — identical names, equivalent purpose

**Official expectation:** links with the same accessible name and the same context
serve an equivalent purpose.

The script only generates these rows when it has found **two or more links with
identical name and context pointing to different destinations**, and it tells you
which those destinations are in the `notes` column.

**The question:** do those different destinations serve the same purpose?

Different destinations do not imply different purposes. Two "Download" links
leading to two copies of the same document serve the same purpose. Two links with
the same name leading to unrelated content do not.

---

## How much you have to review

You may stop before finishing, and it is worth knowing why.

A criterion is **not satisfied** at a site as soon as **one** applicable element
fails. If, while reviewing the rows of a criterion at a site, you find a clear
`falla`, that site's verdict is already decided and the remaining rows of that
same criterion and site will not change it.

For this comparison, however, **it is preferable that you resolve them all**,
because agreement is measured row by row and not only site by site. If the volume
proves unmanageable, resolve at least every row of the criteria that have no prior
`falla`, and report where you stopped.

---

## What not to do

**Do not consult earlier codings** of these sites, whether yours or anyone else's.

**Do not use automated accessibility tools** to decide these rows. The automated
checks are already done; what is asked of you is precisely what no tool can do.

**Do not ask what the expected result is.** There is no expected result.

**Do not modify any other column** of the CSV. Only `outcome` and `justification`.

---

## What to deliver

The fifteen CSVs with the `outcome` and `justification` columns filled in on the
`REVISAR` rows, without renaming the files, plus your incident note.

If at any point you felt the rule did not cover a case well, say so in the note.
That kind of observation is as useful as the coding itself.
