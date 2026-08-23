# Panel Containment Regression Examples

## Purpose

Use these examples to prevent a recurring layout failure: readable text that crosses, touches or visually escapes the shaded/coloured panel that is meant to contain it.

## Test A — Mathematics Why footer

### Intended layout

A green `Why` footer contains:

`Why: What rule are you using?`

### Pass

- text is fully inside the green panel;
- top, bottom, left and right clearance are deliberate;
- nominal padding is at least about `0.15 in`;
- the footer height grows when the line wraps;
- the font remains within the role-based Why range.

### Fail

- the text box begins above the green panel;
- the final line extends below the green panel;
- the panel remains fixed while the font is enlarged;
- the text is shrunk to preserve the old footer height.

## Test B — All / Most / Some cards

### Intended layout

Three warm-up cards retain the established left-to-right structure. `All` has a one-line answer, `Most` has two lines and `Some` has a longer explanation.

### Pass

- all three texts remain fully contained;
- consistent internal padding is preserved;
- short content may use larger type;
- longer content may use more vertical space;
- the text boxes do not need identical heights.

### Fail

- identical internal geometry causes `Some` to cross its card boundary;
- one card has excessive blank space while another clips;
- a longer response is reduced below its role range solely to preserve equal card geometry.

## Test C — Shared Reading question panel

### Intended layout

A short paragraph is separated from one question in a shaded question panel.

### Pass

- the question panel expands for a wrapped two-line question;
- the question remains around the intended projected size;
- the panel has visible breathing room around the text.

### Fail

- the question wraps beyond the panel edge;
- the text box is wider or taller than the panel;
- the panel acts as a decorative strip rather than a responsive container.

## Automated acceptance

Run:

`python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`

The regression passes only when:

1. no high-confidence panel/text pair crosses its panel bounds;
2. all explicit panel/text pairs meet minimum nominal padding;
3. warnings from spatial pairing are inspected at full render size;
4. no render-level overflow or clipping is visible;
5. repairs expand/reflow containers before reducing student-facing font size.