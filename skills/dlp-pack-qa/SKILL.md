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

### Component acceptance gate
- A component-acceptance record lists every scheduled content component.
- Every scheduled component records `PASS`, the checks completed and its artefact or slide range before assembly.
- A missing component, missing evidence, duplicate component record or component `FAIL` blocks assembly and release.
- Component acceptance does not replace this independent whole-pack review.

### Sequence and scope
- Slide 1 is Morning Work when required.
- Every Morning Work instruction is executable in students' books from the projected slide; no task asks students to mark projected-only content.
- Morning Work is scannable at projection size: related tasks are grouped, the core is not padded with an unnecessary extension, and comfortable internal spacing remains after all content is placed.
- Timetable order is coherent.
- Specialist subjects are timetable labels only.
- No specialist printables or generated lessons exist.
- Morning Work and Shared Reading use different texts.
- Mathematics warm-up remains separate from the main Mathematics lesson.

### Literacy warm-up
- 10 `Reminder -> Question -> Answer` sequences unless explicitly overridden.
- Every question contains all information needed to answer it and does not depend on another slide.
- Every question requires one direct response only; the answer slide supplies the concise teaching explanation. Fail an added `explain why`, `explain how you know` or `justify` demand unless the user explicitly requested reasoning.
- Every reminder teaches the method with a different example and does not reveal the next answer.
- Every reminder places a concise applicable `Remember:` rule inside its yellow panel. A punctuation reminder uses a separate example with the target punctuation green, bold and at least 125% of the surrounding size.
- No spelling/Sound Waves replacement content.
- Every answer follows its question and the primary answer is visually dominant.
- Inserted punctuation or changed wording is immediately locatable through green, bold, enlarged treatment plus a textual cue; meaning does not rely on colour alone.
- Judge punctuation emphasis from the exported render as well as the PPTX text runs; intended styling that renders flat fails.
- Explanations teach the relevant rule and do not use generic statements such as `the answer matches the prompt`.
- Student language is immediate and age-appropriate.
- The question title and instruction name the exact operation demonstrated by the answer. A sentence-combination task must say `combine` or `join`; `write a sentence` is insufficient.
- Use accurate curriculum terminology with a plain-language explanation. Fail vague substitutions such as `linking word` when `conjunction` is the correct grammatical term.
- Put inverted commas around a literal word or phrase when it is being discussed as language, while leaving the same word unquoted when it operates normally inside an example sentence.
- Each reminder, model, question, answer and explanation uses the same rule or convention.
- A list-comma reminder must not require a comma after every non-final item while its model or answer omits the optional comma before `and` or `or`.

### Shared Reading
- Uses a strict alternating question/answer sequence.
- Every question slide contains exactly one short paragraph and one question about that paragraph.
- Every answer slide immediately follows and matches only the preceding question slide.
- The complete model answer is visually dominant; any supporting evidence is concise and relevant.
- The question slide does not reveal the answer or teaching-only evidence cue when students are meant to locate it independently.
- Answer slides do not introduce a new paragraph, new question or unrelated content.
- Paragraph/question separation on question slides is visually obvious.
- Text is projected at sensible size; split/shorten rather than shrink.
- Every title, question and answer is supported by the displayed paragraph.
- Any inference follows from explicit clues in the paragraph and the model answer makes that connection clear.

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
- A controlled vocabulary model preserves the sentence's core proposition; a revision that adds several facts is labelled as elaboration.
- Comparison tables are split before their content becomes undersized.

### Numeracy warm-up
- 10 prompt/answer pairs unless explicitly overridden.
- Prompt slides contain three separate All / Most / Some questions, not three answer-quality expectations for one question.
- Green `Why` panel contains reasoning, not generic checking instructions.
- Question and answer slides match.
- No mathematical word is split inside the word across lines. Intentional line breaks may separate an equation from a complete word, but must not produce fragments such as `quarte` / `rs`.

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
- `../../references/visual-exemplar-standard.md`

### Visual-exemplar fidelity gate

Treat the approved edited Tuesday deck as a visual-only benchmark. Require the
assembled deck to retain:

- the full-height 16 px left rail on every projected slide;
- amber reminder/model slides, blue question/task slides and green
  answer/model slides;
- compact uppercase eyebrows plus a clear, larger slide title;
- a dominant main panel and deliberately subordinate cue, explanation or
  reasoning areas rather than a generic repeated navy frame;
- Trebuchet MS as the dominant teaching-deck typeface;
- comparable canvas use, padding, hierarchy and projected legibility.

Content and pedagogy must come from the current component contracts, not from
the exemplar. A deck that copies a documented exemplar content error fails even
when it looks faithful.

Where scripts are available, run:
- `python scripts/audit_pack_contract.py --deck <deck> --component-record <record.json> --out <report.json>`
- If the user explicitly changed the default Literacy warm-up count, add `--literacy-count <n>` with the authorised count.
- `python scripts/audit_slide_typography.py --deck <deck> --out <report.json>`
- `python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`
- `python scripts/audit_visual_exemplar.py --deck <deck> --out <report.json>`

Automated checks are screening tools. Render and inspect the final deck at full size. Any text that crosses or visually escapes its intended coloured, shaded or bordered panel blocks release. A filled instructional text panel with less than the required internal margin also blocks release. A panel-heavy deck receiving zero meaningful panel/text pair coverage fails the automated audit; do not treat that result as a clean geometry pass.

For Morning Work, also fail a slide that technically contains all text but is
visually crowded, repeats low-value chrome, or divides a short independent task
into too many competing cards. For warm-ups, inspect automatic wrapping at the
character level; a broken mathematical word is a release-blocking defect even
when the geometry scripts report no overflow.

## Classroom-feedback regression record

Use all regression records whenever a change affects the orchestrator, component skills, warm-up architecture, Guided Reading scope, Shared Reading structure, student-facing language, Mathematics instructional language, projected typography, semantic colour, panel containment or release QA:

- `examples/benchmarks/t3w6-monday-modular-regression.md`
- `examples/benchmarks/t3w6-tuesday-release-regression.md`
- `examples/benchmarks/t3w6-thursday-literacy-regression.md`

The PPTX referenced by `t3w6-tuesday-release-regression.md` remains rejected.
It is a different file from the later edited Tuesday visual exemplar. Reject
the old deck's documented failures while using the exact edited exemplar hash
listed in `../../references/visual-exemplar-standard.md` for visual fidelity.

## Regression rule

When revising after a FAIL, re-run the **entire** applicable checklist, not only the defect that triggered the revision. This prevents a fix in one area from breaking a previously passing requirement.
