# Projected Readability Regression Examples

## Purpose

Use these examples to prevent two recurring failures:

1. shrinking meaningful student-facing text to preserve a template; and
2. leaving large unused slide areas while the instructional content remains unnecessarily small.

The examples test hierarchy, not uniform font sizing.

## Test A — Mathematics warm-up answer

### Content

- `All` label
- answer: `84`
- `Most` label
- answer: `7 × 12 = 84`
- `Some` label
- answer: `12 × 7 = 84, so 84 ÷ 7 = 12`
- green `Why` footer: `How can the inverse help you check?`

### Expected hierarchy

- `84` may be 48–60 pt because it is short and the panel has room.
- `7 × 12 = 84` should normally be around 36–44 pt.
- the longer `Some` response may be around 30–36 pt.
- `All / Most / Some` labels may be around 24–30 pt.
- the `Why` question should normally be around 28–34 pt.

### Pass condition

The three responses are not forced to the same font size. Each uses the largest sensible size for its role and length while maintaining a clear hierarchy.

### Fail examples

- every element fixed at 36 pt even when a one-number answer could be much larger;
- `Why` reduced to 18–22 pt to preserve the footer height;
- a 24 pt `Some` response surrounded by large unused card space;
- all three answer panels kept identical in geometry when one needs more room and another needs less;
- shrinking content before reducing margins or rewriting a long explanation.

## Test B — Literacy warm-up

### Content

Main prompt: `Which word is the verb?`

Sentence: `The eagle circled above the cliff.`

Supporting instruction: `Write the verb only.`

### Expected hierarchy

- main prompt: at least 36 pt, normally 36–44 pt;
- sentence: large enough to be a primary reading object, commonly 34–42 pt;
- supporting instruction: clearly subordinate but still projected comfortably, commonly 28–32 pt.

### Pass condition

The student can immediately see the prompt and sentence from the back of the room. The support instruction is smaller but not fine print.

### Fail examples

- prompt at 36 pt but sentence at 24 pt despite ample space;
- support instruction at 18 pt because the template reserves a small footer;
- excessive decorative margins that force the sentence into a narrow box.

## Test C — Shared Reading

### Content

Paragraph of 3–4 concise sentences with one question below it.

### Expected hierarchy

- paragraph: usually 28–32 pt;
- question: usually 30–36 pt;
- clear separation between paragraph and question;
- the paragraph and question together should use the body area deliberately.

### Fail examples

- paragraph at 22–24 pt while the lower half of the slide is empty;
- paragraph placed in a narrow left card purely because the template expects a second unused card;
- question squeezed into a thin footer at a much smaller size than the paragraph.

## Regression acceptance criteria

A test slide passes only when:

1. the main warm-up instructional element reaches at least 36 pt;
2. supporting text is sized according to role rather than forced to match the main element;
3. meaningful secondary text is not treated as fine print;
4. short content grows when space allows;
5. the layout is reflowed before text is shrunk;
6. unused space has an instructional purpose rather than being a side-effect of rigid geometry;
7. full-size visual inspection confirms comfortable back-of-room readability.
