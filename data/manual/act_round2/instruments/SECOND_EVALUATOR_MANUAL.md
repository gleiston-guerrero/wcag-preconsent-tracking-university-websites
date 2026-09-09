# Second evaluator's manual — ACT recoding

*Versión en español: [SECOND_EVALUATOR_MANUAL_ES.md](SECOND_EVALUATOR_MANUAL_ES.md)*

Study of accessibility and privacy on university websites. You are asked to code
**independently** three accessibility criteria on the home pages of fifteen
universities.

Independently means: **do not consult earlier codings, nor other evaluators'
results, nor the draft of the article.** Your coding is compared with another to
measure the degree of agreement, and that agreement is only worth anything if the
two were done separately.

Estimated time: about two hours for the collection, plus the time for the
judgement decisions, which are explained in a second document.

---

## What is evaluated

Three WCAG 2.2 success criteria, which is also the international standard
ISO/IEC 40500:2025:

| Criterion | Name |
|---|---|
| **1.1.1** | Non-text content |
| **1.4.3** | Contrast (minimum) |
| **2.4.4** | Link purpose (in context) |

The coding is anchored in the W3C **ACT rules**, whose format has been a W3C
Recommendation since February 2026. The outcome vocabulary is *applicable*,
*passed*, *failed*, *inapplicable*. **There is no intermediate category**: an
element passes or fails.

The unit of coding is **the element**, not the site. A criterion is not satisfied
at a site if any applicable element fails.

---

## Before you start

1. Use **Google Chrome** or **Microsoft Edge**, on a desktop or laptop computer.
   A phone will not do.
2. Work in a **normal window**, not a private one, and with the window maximised.
   The window size affects which elements are visible.
3. **Do not use a VPN.** The measurement must be taken from your usual connection.
4. **Do not install ad blockers or accessibility extensions.** If you already have
   them, disable them: they alter the page being measured.

---

## Procedure, site by site

Repeat these six steps for each of the fifteen addresses in the list.

**1. Open the address** in a new tab and wait for the page to load completely.

**2. If a cookie notice appears, close it.** Choose the option that rejects, or
the one that simply closes. If the notice offers only "Accept", accept it and
**make a note of it**. Wait a few seconds after closing it: some notices take a
while to disappear.

This matters: with the notice on top, the text it covers is not visible and would
fall outside the measurement.

**3. Open the developer tools** with the **F12** key and go to the **Console** tab.

**4. Paste the script** `act_recode_evaluator2.js` in full and press Enter.

The first time, Chrome will block the paste and ask you to type a confirmation
phrase. If your Chrome is in Spanish, type `permitir pegado`; if it is in English,
`allow pasting`. Press Enter. A syntax error will appear: that is normal, the
browser registers the authorisation anyway. Paste the script again.

**Before the first run**, change this line in the script:

```javascript
const EVALUADOR = 'R03';   // <-- PUT YOUR EVALUATOR CODE HERE
```

Always use the same code on all fifteen sites. **Do not write your name**: the
coding is published and evaluators are identified by code.

**5. Wait for it to finish.** It takes between twenty seconds and a minute. You
will see a few summary lines in the console and a CSV file will download.

**6. Check the name of the downloaded file.**

- If it ends in `_ok.csv`, correct.
- If it ends in **`_MODALABIERTO.csv`**, the cookie notice was still open. Close
  it properly and run it again. Delete the incorrect file.

The script leaves the summary line on the clipboard, and it also **accumulates all
the lines from earlier runs**: when you finish the last site, the clipboard holds
all fifteen at once and you only need to paste them once into a text document.

The accumulation lives in the browser's tools tab. If you close the browser
halfway, it is lost: paste what you have before closing. It is not serious,
because every CSV carries the same data inside it, in the columns `dialog_state`,
`cmp_containers`, `cmp_excluded_elements` and `script_version`.

The console will also show a table of the sites completed so far, so that you know
at all times which ones are left.

---

## The fifteen sites

Seven from an international benchmark group and eight from the Ecuadorian census.
Do them in this order.

```
https://www.berkeley.edu
https://www.ucl.ac.uk
https://www.cornell.edu
https://nus.edu.sg
https://www.northwestern.edu
https://www.manchester.ac.uk
https://hkust.edu.hk/
https://unesum.edu.ec
https://usecipol.edu.ec
https://www.iaen.edu.ec
https://www.ulvr.edu.ec
https://www.utpl.edu.ec
https://www.ups.edu.ec
https://www.indoamerica.edu.ec
https://ecotec.edu.ec
```

Sites with a known cookie notice, so that you are forewarned: **NUS**, which
offers only "Accept"; **Northwestern**; **Manchester**; and **ECOTEC**.

---

## What the script does and what it does not

It decides on its own everything the ACT rule defines mechanically: which element
is applicable, the contrast of 1.4.3 with its ratio and its threshold, whether an
image has an accessible name and whether a link has one.

It leaves marked as **REVISAR** the rows where the rule refers to human judgement:
whether an image's name is descriptive, whether a link is understood with its
context, and whether links with identical names serve an equivalent purpose.

**Do not fill in those rows yet.** You will be given a second document with the
decision criteria and the exact subset you must resolve.

---

## What to deliver

When you finish the fifteen sites:

1. The **fifteen CSV files**, without renaming them.
2. The **fifteen summary lines** `ACT|v5`, pasted in one go from the clipboard
   into a text document.
3. A **brief note** with any incident: sites that did not load, notices that only
   allowed acceptance, pages that changed while you were measuring, or anything
   that caught your attention.

That note matters. If a site behaved oddly, it is better to know it than to
discover it when comparing the numbers.

---

## Warnings

**Do not modify the downloaded CSVs.** If you think there is an error, note it in
the incident note and leave it as it is.

**Do not run the script twice on the same site** unless the first run came out
with `_MODALABIERTO`. If you do, keep both and say so: pages change between runs
and that variation is itself a datum.

**Do not consult anyone** who has coded these sites before, and do not ask about
the expected results, until you have delivered your complete coding.
