# T3W6 Monday Modular Regression Benchmark

## Status

**Approved classroom-quality benchmark** for the modular Daily Lesson Pack architecture.

The benchmark was generated from the modular branch on 23 August 2026 and reviewed positively by the teacher before merge.

Reference artefact:
- file name: `T3W6_Monday_Daily_Lesson_Pack_Modular_Regression.pptx`
- slide count: **72**
- SHA-256: `46477f17937b55db6dc31a8c70558df0af0b56dd647d21fb84a72ef1d73dccce`

The PPTX itself is not duplicated in the source tree. This fixture records the approved structural and instructional characteristics that future builds must preserve or improve.

## Purpose

Use this benchmark when changing the orchestrator, any Daily Lesson Pack component skill, slide-quality rules, colour rules, containment rules or cross-component QA.

Do not require future packs to reproduce the benchmark's exact wording or content. Compare **quality, clarity, architecture and instructional function**.

## Approved characteristics

### Morning Work
- Slide 1 is immediately usable Morning Work rather than a cover or set-up slide.
- The task combines retrieval, application/improvement and extension.
- Students can begin independently.

### Literacy warm-up
- Exactly 10 prompt/answer pairs in this benchmark.
- Every answer immediately follows its prompt.
- Questions are short, student-friendly and high leverage.
- Primary answers are visually dominant.
- No generic whiteboard footer is used.

### Shared Reading
- Each substantive slide displays one short paragraph and one question about that paragraph.
- Paragraph and question are visually distinct.
- Text remains suitable for whole-class projection rather than being compressed to preserve a long passage.
- Questions vary in comprehension purpose and remain student-friendly.

### Guided Reading
- Uses a separate text from Shared Reading.
- The Monday text is pitched to the very-low group.
- Teacher prompts and expected responses match the student text.

### Writing
- The lesson explicitly teaches/applies the scheduled Information Report toolkit feature: subject-specific vocabulary.
- The writing task requires a student product that demonstrates the feature rather than substituting country research for writing instruction.

### Mathematics warm-up
- Uses 10 prompt/answer pairs in the current architecture.
- Every prompt has three **separate** questions labelled All, Most and Some.
- All is genuinely accessible, Most is secure expected performance, and Some is a modest appropriate extension.
- The three tiers are not partial/complete/explain versions of one question.
- The green Why panel is used for mathematical reasoning, not a generic checking instruction.
- Question and answer slides match.

### Mathematics lesson
- Topic integrity is maintained: equivalent fractions are the concept; representations support rather than replace the concept.
- The sequence includes readiness, complete modelling, connection between representations, We Do, guided practice, misconception discussion, independent practice and exit evidence.
- Student tasks explicitly state the action and required output.
- Mathematical language is literal and student-friendly rather than vague or conversational shorthand.

### Visual quality
- Projected readability takes priority over preserving fixed card layouts.
- Important content uses available slide space.
- Colour is restrained and instructional.
- Panels contain their text with deliberate padding.
- The deck is visually consistent without making every slide mechanically identical.

## Regression pass criteria

A future representative Daily Lesson Pack passes this benchmark when:

1. all component-specific QA checks pass;
2. none of the approved characteristics above regress;
3. the pack remains at least as clear and classroom-usable as this benchmark when inspected slide-by-slide at full size;
4. a fix in one component does not degrade an unrelated component;
5. any deliberate departure is supported by a later explicit teacher instruction.

## Required use

Run this benchmark after changes to:
- `SKILL.md` orchestrator routing;
- any `skills/dlp-*/SKILL.md` component;
- warm-up architecture or calibration;
- Shared Reading structure;
- Mathematics instructional language;
- projected typography, semantic colour or panel containment;
- release QA.

The benchmark is a **quality floor, not a frozen template**. Future outputs may improve on it.