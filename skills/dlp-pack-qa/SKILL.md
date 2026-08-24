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
- Every Morning Work instruction is executable in students' books from the projected slide; no task asks students to mark projected-only content.
- Timetable order is coherent.
- Specialist subjects are timetable labels only.
- No specialist printables or generated lessons exist.
- Morning Work and Shared Reading use different texts.
- Mathematics warm-up remains separate from the main Mathematics lesson.

### Literacy warm-up
- 10 `Reminder -> Question -> Answer` sequences unless explicitly overridden.
- Every question contains all information needed to answer it and does not depend on another slide.
- Every reminder teaches the method with a different example and does not reveal the next answer.
- No spelling/Sound Waves replacement content.
- Every answer follows its question and the primary answer is visually dominant.
- Inserted punctuation or changed wording is immediately locatable through green, bold, enlarged treatment plus a textual cue; meaning does not rely on colour alone.
- Explanations teach the relevant rule and do not use generic statements such as `the answer matches the prompt`.
- Student language is immediate and age-appropriate.

### Shared Reading
- Uses a strict alternating question/answer sequence.
- Every question slide contains exactly one short paragraph and one question about that paragraph.
- Every answer slide immediately follows and matches only the preceding question slide.
- The complete model answer is visually dominant; any supporting evidence is concise and relevant.
- The question slide does not reveal the answer or teaching-only evidence cue when students are meant to locate it independently.
- Answer slides do not introduce a new paragraph, new question or unrelated content.
- Paragraph/question separation on question slides is visually obvious.
- Text is projected at sensible size; split/shorten rather than shrink.

### Guided Reading
- Guided Reading appears only as a timetable block.
- No Guided Reading text, teacher guide, prompts, transition task or instructional slide is generated.
- Any displayed group is taken from an authoritative schedule and is exactly `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon`.
- No ability descriptor, country label or inferred group name appears.

### Writing
- Current toolkit feature is explicitly taught/applied.
- A model/joint construction is present where needed.
- Students produce writing demonstrating the feature.
- Student-facing wording uses familiar, actionable language; necessary technical terms are defined before use.
- Technical-word substitutions preserve meaning and the explanation states the exact information added.
- Comparison tables are split before their content becomes undersized.

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

Automated checks are screening tools. Render and inspect the final deck at full size. Any text that crosses or visually escapes its intended coloured, shaded or bordered panel blocks release. A filled instructional text panel with less than the required internal margin also blocks release.

## Classroom-feedback regression record

Use `examples/benchmarks/t3w6-monday-modular-regression.md` as a diagnostic record whenever a change affects the orchestrator, component skills, warm-up architecture, Guided Reading scope, Shared Reading structure, student-facing language, Mathematics instructional language, projected typography, semantic colour, panel containment or release QA.

The referenced PPTX is not an approved quality floor. Reject its documented failures and require the current acceptance characteristics unless a later explicit teacher instruction deliberately changes them.

## Regression rule

When revising after a FAIL, re-run the **entire** applicable checklist, not only the defect that triggered the revision. This prevents a fix in one area from breaking a previously passing requirement.
