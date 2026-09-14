# Decision criteria — rows marked REVISAR

*Versión en español: [EVALUATOR_DECISION_CRITERIA_ES.md](EVALUATOR_DECISION_CRITERIA_ES.md)*

The second evaluator's second document, for the **second stage** of the work. The
first, the collection with the script across the fifteen sites, is done. What
remains is to resolve the rows the rule refers to human judgement, and they are
resolved in two plain-text worksheets, `hoja_r04_111.txt` and `hoja_r04_244.txt`,
not in the CSVs. Read this document **before** writing anything in the sheets.

The script has already decided everything the rule defines mechanically. What is
left are the rows marked `REVISAR`, where the ACT rule refers explicitly to a
person's judgement. This document sets out how to make that judgement.

Every example in this document is taken from the official W3C documentation of
the ACT rules. **None comes from the fifteen sites you are evaluating**, so as
not to condition your judgement.

---

## The single decision rule

Each row is one block of the sheet. In each block, write after `RESULTADO:` one
of these words:

| | |
|---|---|
| `cumple` | The element satisfies the rule's expectation |
| `falla` | It does not |
| `no-visible` | It cannot be judged: the element is no longer on the page, or the image cannot be seen |

**There is no intermediate category.** Do not write "partial" or "unsure", and do
not leave the field empty. If you are in doubt between `cumple` and `falla`,
choose and explain the doubt.

`no-visible` is not a third category of judgement: it is the record that there was
nothing to judge. Those rows are kept as undecidable and enter no comparison. Use
it only when there really is nothing to look at, never to avoid a hard call.

Always write a sentence after `JUSTIFICACION:`. That sentence is what will make it
possible to reconcile the discrepancies afterwards, and for `no-visible` it must
say what you could not see. The tool that returns the sheets to the CSVs rejects
the whole sheet, writing nothing, if any block is left empty, carries a word other
than those three, or has no justification.

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

1. Open the address on the block's `imagen` line, or locate the element on the
   page with its `selector` line.
2. Look at the image.
3. Read the accessible name.
4. Decide whether the second serves the purpose of the first.

If the image does not load or you cannot locate it, write `falla` only if you are
certain. Thirty-eight of the 203 blocks of SC 1.1.1 carry no usable address —
CSS backgrounds, inline `svg`, or images the pass did not see — and there you
locate the element by its selector. If the image still cannot be seen, write
`no-visible` and say in the justification what you looked for and what you found.
Do not write `falla` because you could not look: that is not a judgement, and a
row recorded as undecidable is preferable to one resolved blind.

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
block's `contexto` line. When that line says `SIN CONTEXTO PROGRAMATICO`,
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

Read the block's `nombre` and `contexto` lines. Ask yourself: **could
someone who hears only this know where the link leads?**

A screen reader user can navigate by jumping from link to link, without hearing
the rest of the page. That is the situation the rule contemplates.

---

## Rule `fd3a94` — identical names, equivalent purpose

**Official expectation:** links with the same accessible name and the same context
serve an equivalent purpose.

The script only generates these rows when it has found **two or more links with
identical name and context pointing to different destinations**, and it tells you
those destinations are. There are three such blocks. Each gives you the shared
name, the context, the page address and the destination of every link in the
group. Here you do get the page address, because the question is about the
destinations and **the destinations come truncated at 60 characters** by the
collector. In the Cornell block the two destinations are identical up to the cut:
they are the same address under different tracking parameters, and the only way to
see it is to open the page and look at the two links.

**The question:** do those different destinations serve the same purpose?

Different destinations do not imply different purposes. Two "Download" links
leading to two copies of the same document serve the same purpose. Two links with
the same name leading to unrelated content do not.

---

## How much you have to review

The two sheets carry **318 blocks**: 203 of SC 1.1.1 and 115 of SC 2.4.4. They
are not every row your collection left marked `REVISAR`, which is 1 351, but only
those that still decide a site's verdict. The other 1 033 belong to criteria that
already fail at their site through another element, so resolving them would change
no result and they are not asked of you.

**Resolve all 318.** The tool accepts no half-filled sheet: it rejects the whole
sheet if a single block is left unanswered. If the volume proves unmanageable, say
so before starting and the work is split by site.

---

## What not to do

**Do not consult earlier codings** of these sites, whether yours or anyone else's.

**Do not use automated accessibility tools** to decide these rows. The automated
checks are already done; what is asked of you is precisely what no tool can do.

**Do not ask what the expected result is.** There is no expected result.

**Do not modify the data lines or the `=== NNN | ... ===` headers** of the sheets.
Write only after `RESULTADO:` and after `JUSTIFICACION:`.

**Do not open the sheets with Excel or any spreadsheet.** They are plain text on
purpose, because the justifications carry commas, quotation marks and semicolons,
and a spreadsheet destroys them. Use Notepad, Notepad++ or VS Code, and save as
UTF-8.

---

## What to deliver

The two sheets, `hoja_r04_111.txt` and `hoja_r04_244.txt`, filled in and not
renamed, plus your incident note. Nothing else: the CSVs are not touched, the tool
takes care of that when it receives the sheets.

If at any point you felt the rule did not cover a case well, say so in the note.
That kind of observation is as useful as the coding itself.
