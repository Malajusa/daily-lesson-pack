# Slide Deck Quality Standards

## Purpose

Classroom slides are projected teaching surfaces, not desktop documents. Visual quality is judged by what a student at the back of the room can comfortably read, locate and understand. Attractive composition is insufficient if important content is undersized or if large usable areas remain empty while student-facing text is small.

## Core design rule

Build in this order:

1. instructional content and intended thinking;
2. required projected readability;
3. visual hierarchy and representation;
4. layout and spacing;
5. decorative treatment, only if it still improves the slide.

Do **not** start with a fixed template and shrink text until the content fits. If content does not fit at an appropriate projected size, rewrite, reflow, enlarge the relevant region, remove non-essential material or split the content across slides.

## Projected readability hierarchy

Typography is role-based rather than uniform. Different sizes should communicate instructional hierarchy.

### Warm-up slides

Use Trebuchet MS for the established Literacy and Mathematics warm-up system unless an explicit user instruction overrides it.

| Role | Typical projected size | Guidance |
| --- | ---: | --- |
| Main question or main answer | **36–44 pt** | 36 pt is the normal minimum. This should be one of the most visually dominant elements. |
| Short key mathematical expression, answer or target word | **36–52+ pt** | Increase when content is short; do not leave a one-word or one-number response tiny inside a large panel. |
| All / Most / Some task or response | **30–36 pt** | Strong secondary content. Use the largest sensible size that the panel supports. |
| Why question or explanation | **28–34 pt** | Clearly readable and substantive, but subordinate to the main task. |
| All / Most / Some labels | **24–30 pt** | Navigation labels, not the main learning content. |
| Small structural labels | **22–26 pt** | Use only when genuinely secondary. Do not use this tier for instructions, questions, explanations or content students must read closely. |

These are **hierarchy targets, not a command to make every element the same size**. The generator should actively vary size according to role, length and available space.

### Warm-up minimum expectations

- The main instructional element must be at least 36 pt.
- Meaningful supporting student-facing text should normally remain at or above 28 pt.
- Text below 24 pt on a projected warm-up slide is a presumptive failure unless it is genuinely incidental and not required for the student task.
- A short response, symbol or expression should normally grow beyond the minimum when space allows.
- The `Why` footer is not fine print. Its reasoning prompt/explanation must be sized as meaningful student content.
- `All`, `Most` and `Some` labels may be smaller than the tasks beneath them because they are navigational labels.

### Shared Reading

Shared Reading must be designed for whole-class projection.

- Paragraph/body text: usually 28–32 pt.
- The single question attached to the paragraph: usually 30–36 pt.
- The question and paragraph must be clearly separated by spacing, panel structure and hierarchy.
- If the paragraph cannot fit comfortably at projected size, shorten or split it. Do not shrink the paragraph to preserve a one-slide layout.

### Mathematics teaching slides

- Main worked mathematics, equations, number lines and representations: usually 30–40+ pt equivalent visual scale.
- Main student task/question: usually 32–40 pt.
- Supporting explanation: usually 26–32 pt.
- Labels attached to diagrams: usually 22–28 pt, increased where the label itself is important to the reasoning.

### Other instructional slides

A title may be smaller than a short mathematical answer or key concept if that better communicates the hierarchy. Typography should reflect what students need to notice, not a rigid template hierarchy.

## Largest sensible type rule

Passing a minimum font-size threshold is not enough.

For every important student-facing element, ask:

> Could this content be materially larger without harming separation, hierarchy or representation?

If yes, enlarge it.

A slide can therefore fail even when all text technically clears its minimum threshold. Examples:

- a 36 pt one-word answer inside a very large empty answer panel;
- a 28 pt question occupying only one corner of a large card;
- a small fraction model surrounded by unused canvas;
- a paragraph compressed into a narrow column while half the slide is empty;
- large decorative cards whose actual instructional text is comparatively tiny.

## Space utilisation standard

Whitespace is purposeful only when it improves focus, separation or comprehension. Unused space is not automatically a virtue.

### Required behaviour

- Let important content expand into available space.
- Prefer one or two large teaching surfaces when the slide contains one or two major ideas.
- Do not preserve three-card or multi-card layouts when fewer, larger regions would project better.
- Do not use oversized containers with undersized contents.
- Reduce excessive margins before reducing student-facing font size.
- Expand diagrams, worked examples and answer text when they are the instructional focus.
- Use blank space to separate ideas, not merely because a template reserves it.

### Indicative body-area use

For ordinary instructional slides, the main teaching content will often occupy roughly 70–90% of the useful body region. This is an indicative design range, not a fixed pass/fail percentage. A deliberately sparse retrieval slide may use less; a dense shared text slide may use more. The reviewer must judge whether unused space is helping cognition or simply forcing content to remain too small.

## Rewrite/reflow before shrink

When content is too dense, use this repair order:

1. shorten wording without losing the instructional meaning;
2. remove duplicated or teacher-facing text;
3. enlarge or merge content regions;
4. reduce unnecessary margins and decoration;
5. split the material across slides;
6. only then reduce a secondary font within its appropriate role range.

Never solve a layout problem by shrinking the main warm-up question/answer below 36 pt or by turning meaningful supporting text into fine print.

## Warm-up visual hierarchy checks

For every Literacy and Mathematics warm-up slide:

1. Identify the main student-facing element.
2. Confirm it is at least 36 pt and visually dominant.
3. Identify secondary task/explanation text and confirm it is deliberately subordinate but still comfortably projected.
4. Confirm labels are smaller only because their role is navigational.
5. Check whether any short answer, key word or expression should be enlarged beyond 36 pt.
6. Inspect the slide for unused space that could support larger content.
7. Confirm no text was shrunk merely to preserve a fixed card geometry.

## Full-size projection test

A slide fails visual QA if any of these is true:

- a student at the back of the classroom would need to strain to read meaningful content;
- the most important information is not among the largest or most salient elements;
- meaningful secondary text has been treated as fine print;
- important content could clearly be enlarged by using currently empty space;
- a fixed template has forced content into unnecessarily small regions;
- the slide contains large empty zones without an instructional reason while relevant text or visuals remain undersized;
- labels, examples or reasoning prompts are too small to function during whole-class teaching.

## QA questions

Every rendered slide must pass all three questions:

1. **Projected readability:** Can a student at the back of the classroom comfortably read every element required for the task?
2. **Hierarchy:** Is the most important information among the largest and clearest elements on the slide?
3. **Space:** Has the available slide area been used deliberately to make the learning easier to see?

A `no` to any one question requires revision.

## Automated typography audit

Run `python scripts/audit_slide_typography.py --deck <deck> --out <report.json>` on final PPTX builds when the script is available.

The automated audit is a screening tool, not a substitute for full-size human inspection. It should flag:

- warm-up slides whose largest instructional text is below 36 pt;
- student-facing text below the projected readability floor;
- unusually small secondary text on otherwise spacious slides;
- slides with low body-content occupancy combined with relatively small text;
- likely cases where a fixed layout has preserved empty space at the expense of readable content.

Automated warnings must be inspected rather than dismissed. A visual reviewer may justify an exception only when the smaller element is genuinely incidental or the unused space has a clear instructional purpose.
