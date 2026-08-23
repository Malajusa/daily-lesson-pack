---
name: dlp-pack-qa
description: Independently quality-assure a complete Daily Lesson Pack and return PASS or FAIL with defects routed to the owning component.
---

# DLP Pack QA

## Role

This skill is independent from generation. It is the release authority. Do not silently repair content while reviewing; identify the owner and send the defect back to that component.

Return:
- `PASS` only when all critical checks pass;
- otherwise `FAIL` with component, slide/page, defect and required correction.

## Cross-pack checks

### Sequence and scope
- Slide 1 is Morning Work when required.
- Timetable order is coherent.
- Specialist subjects are timetable labels only.
- No specialist printables or generated lessons exist.
- Morning Work, Shared Reading and Guided Reading use different texts.
- Mathematics warm-up remains separate from the main Mathematics lesson.

### Literacy warm-up
- 10 question/answer pairs unless explicitly overridden.
- No spelling/Sound Waves replacement content.
- Every answer follows its question and the primary answer is visually dominant.
- Student language is immediate and age-appropriate.

### Shared Reading
- Exactly one short paragraph and one question per substantive slide.
- The question refers to that displayed paragraph.
- Paragraph/question separation is visually obvious.
- Text is projected at sensible size; split/shorten rather than shrink.

### Guided Reading
- Correct day/group level.
- Student text and teacher guide match.
- Different from Shared Reading.

### Writing
- Current toolkit feature is explicitly taught/applied.
- A model/joint construction is present where needed.
- Students produce writing demonstrating the feature.

### Numeracy warm-up
- 10 prompt/answer pairs unless explicitly overridden.
- Prompt slides contain three separate All / Most / Some questions, not three answer-quality expectations for one question.
- Green `Why` panel contains reasoning, not generic checking instructions.
- Question and answer slides match.

### Main Mathematics lesson
- Every task states action, mathematical focus, representation/resource where required, and expected output.
- No vague or figurative instructional shorthand.
- Worked examples and diagrams are mathematically correct.
- Primary answers are visually dominant.
- Exit evidence measures the intended concept.

## Visual QA

Apply the repository standards:
- `references/slide-deck-quality-standards.md`
- `references/semantic-colour-standard.md`
- `references/panel-containment-standard.md`

Where scripts are available, run:
- `python scripts/audit_slide_typography.py --deck <deck> --out <report.json>`
- `python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`

Automated checks are screening tools. Render and inspect the final deck at full size. A high-confidence overflow/containment failure blocks release.

## Regression rule

When revising after a FAIL, re-run the **entire** applicable checklist, not only the defect that triggered the revision. This prevents a fix in one area from breaking a previously passing requirement.
