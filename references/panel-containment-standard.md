# Panel Containment and Responsive Container Standard

## Purpose

Shaded, coloured and bordered panels are containers for instructional content. Their geometry must respond to the content they contain. A panel is not successful merely because the text is readable somewhere on the slide; the associated text must sit clearly and completely within the intended panel with deliberate internal padding.

This standard applies to warm-up cards, `Why` footers, answer panels, definition boxes, worked-example callouts, shared-reading question panels, writing-model panels and any other shaded/coloured/bordered region that visually claims to contain student-facing text.

## Core rule

**The container must fit the content. Do not force the content to fit a fixed container.**

When a panel contains or visually owns text:

- the text box must be fully inside the panel bounds;
- the text must have deliberate padding from every panel edge;
- no line of text may touch, cross or visually escape the panel boundary;
- the panel must expand or reflow before the text is reduced below its role-appropriate projected size;
- the slide must still pass the projected-readability hierarchy in `slide-deck-quality-standards.md`.

## Required internal padding

For ordinary classroom panels, target approximately `0.15–0.25 in` of clear internal padding on all sides.

Use the larger end of the range for:

- long questions or explanations;
- `Why` reasoning panels;
- rounded rectangles where corner curvature reduces usable space;
- panels projected at distance;
- panels with thick borders.

A smaller value may be justified only for very short labels or compact structural elements. Meaningful student-facing content must never sit flush against a panel edge.

## Geometric containment

For a text box assigned to a panel, its nominal bounds must satisfy:

- `text_left >= panel_left + padding`
- `text_top >= panel_top + padding`
- `text_right <= panel_right - padding`
- `text_bottom <= panel_bottom - padding`

These conditions are necessary but not sufficient. PowerPoint wrapping, paragraph spacing, font metrics and line-height can still create visual overflow inside a technically contained text box, so rendered inspection remains mandatory.

## Responsive container behaviour

Panel geometry must respond to content length and role.

### Required behaviour

1. Determine the projected font size from instructional role first.
2. Estimate the text region required at that size.
3. Size the panel around that region plus padding.
4. Reflow neighbouring panels or reduce unnecessary margins if more space is needed.
5. Shorten wording without losing the learning intent when the panel remains too dense.
6. Split the content across slides if needed.
7. Reduce a secondary font only as a last resort and only within its role-appropriate range.

### Prohibited behaviour

Do not:

- hard-code a footer height and then enlarge the text until it crosses the footer boundary;
- keep three equal cards when one needs substantially more vertical space than the others;
- preserve decorative margins while text touches panel edges;
- place a text box partly outside a coloured panel and rely on the shared background to hide the problem;
- shrink a `Why` explanation or answer merely because the coloured container was built too small;
- allow a panel label to sit inside while the substantive content sits outside the panel;
- use clipping or hidden overflow as a layout solution.

## Repeated panel systems

Repeated layouts must be responsive rather than merely duplicated.

### Mathematics warm-up `Why` footer

The green `Why` footer is a semantic reasoning panel. Its height must be derived from:

- the required role-based font size of the `Why` prompt/explanation;
- the number of wrapped lines;
- paragraph spacing;
- top and bottom padding.

The footer may become taller on a slide with a longer explanation. It must not force the reasoning text above or below the green area.

### All / Most / Some cards

The three cards share a stable left-to-right structure, but their internal text regions do not need identical dimensions when content length differs. Preserve the overall three-column architecture while allowing:

- different text-box heights;
- different vertical alignment where appropriate;
- short answers to grow;
- longer responses to use more vertical area;
- card padding to remain consistent.

Do not make the panels visually identical at the expense of legibility or containment.

### Shared Reading and writing panels

When a paragraph, model or question sits inside a panel, the text region should normally expand with the content. If a 3–4 sentence paragraph cannot fit with projected-size text and padding, shorten or split it rather than making the panel act as a fixed crop window.

## Panel-to-text ownership

Every panel should have a clear relationship to the text it contains.

During generation, record panel/text ownership explicitly where possible. For example:

- `why_panel` → `why_text`
- `all_panel` → `all_task`
- `most_panel` → `most_task`
- `some_panel` → `some_task`
- `question_panel` → `question_text`

Named or otherwise traceable panel/text pairs are preferable to relying on visual proximity alone because they permit deterministic geometric QA.

If explicit ownership metadata is unavailable, use spatial pairing only as a heuristic and require human inspection of every flagged case.

## Automated containment audit

Run:

`python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`

The script is a screening and blocking geometry check. It should:

- identify likely filled/shaded panel shapes;
- pair text boxes with the smallest plausible panel underneath them;
- detect text boxes that cross panel boundaries;
- detect text boxes that violate minimum internal padding;
- report suspected panel/text pairs for full-size review;
- distinguish hard geometric failures from ambiguous heuristic matches.

A hard geometric failure blocks release.

## Render-level inspection

After the geometry audit, inspect the final rendered slide at full size. A slide fails even if the nominal bounds pass when:

- wrapped text visually crosses the panel edge;
- glyphs, fractions or equations appear clipped;
- descenders or superscripts sit uncomfortably close to the boundary;
- line spacing makes the last line collide with the panel edge;
- the panel appears to stop before the text does;
- the text looks visually detached from the panel that is meant to contain it.

## Repair order

When containment fails, repair in this order:

1. enlarge the panel;
2. move/reflow the panel and its neighbours;
3. reduce excessive internal or external margins while preserving minimum padding;
4. shorten the text;
5. split the content or slide;
6. only then reduce a secondary font within its permitted role range.

Do not fix panel overflow by shrinking the main warm-up element below 36 pt or turning meaningful supporting content into fine print.

## Release stop check

A teaching deck fails panel-containment QA if any of the following is true:

- a text box extends outside the shaded/coloured/bordered panel it belongs to;
- required internal padding is absent on any edge;
- a panel's fixed geometry forces meaningful text below its readability role range;
- wrapped or rendered text visually escapes or clips at the panel boundary;
- repeated panels use rigid geometry that causes one or more instances to overflow;
- the `Why` reasoning text is not fully contained within its green panel;
- a panel/text pair cannot be confidently verified after an automated warning.

No panel-containment failure may be waived merely because the text remains readable against the slide background.