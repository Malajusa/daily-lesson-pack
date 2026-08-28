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

### Context provenance gate
- Apply `references/shared-class-context-contract.md`.
- A context-source record identifies the current source for date/term/week/day,
  timetable, Mathematics focus, English focus, lesson-status exception and
  printing quantity when printing is requested.
- The record must not cite chat memory, saved personal context, another
  account's Project context or an unstated standing preference as authority.
- Missing required context blocks classroom-ready release; it is queried rather
  than guessed.
- For Wednesday co-teacher mode, the supplied Wednesday timetable and explicit
  day-level Mathematics and English focus are present. Wednesday is not rejected
  merely because it sits outside the four-day overview.

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
- In a choice task, students select only the option; any concise rationale belongs on the answer slide.
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
- Multiple-choice options are grammatically parallel and similar enough in length, detail and tone that every distractor is plausible until the target rule is applied. Replace the item if a credible distractor cannot be written.
- A word described as `more precise` adds a clear, defensible semantic feature while preserving the original meaning. Formality, technicality or unfamiliarity alone is not precision.
- Reject debatable synonym rankings, including presenting `rotate` as automatically more precise than `turn` for a propeller. The supplied answer explanation must be sufficient; the teacher must not need to invent a semantic defence.
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
- The warm-up retrieves already taught knowledge rather than introducing a new procedure.
- Mathematical terminology, notation, diagrams, scales and representations are accurate.
- A prompt slide does not reveal its answer through completed working, colour or an already completed model.

### Main Mathematics lesson

Apply `references/universal-maths-instruction-canon.md` in full.

#### Planning and scope
- The Mathematics component acceptance record substantiates every required planning-contract check rather than recording a generic `PASS`.
- The curriculum concept and lesson boundary are explicit.
- The lesson is classified as concept introduction, procedure development, fluency development, reasoning, problem solving or review/assessment.
- Unless explicitly review, consolidation or extension, the lesson introduces one central new mathematical idea rather than several substantial new concepts.
- Focused prerequisite retrieval is distinct from the cumulative Mathematics warm-up.

#### Mathematical meaning and language
- A newly introduced procedure is grounded in quantities, units, properties or relationships before procedural shorthand is used.
- The explanation identifies what changes and what remains invariant where relevant.
- Accurate technical vocabulary is introduced with a plain-language explanation and is not replaced by vague labels such as `top number`, `bottom number`, `answer number` or `times number`.
- Notation is conventional, readable and internally consistent. Question numbering cannot be misread as part of a decimal, fraction, coefficient or mixed number.

#### Representations
- Every representation has a stated mathematical purpose and reveals the intended structure.
- Visuals, verbal explanations and equations represent the same quantities, units and relationships.
- The correspondence between representations is made explicit.
- Quantities, labels, scales, equal intervals, partitions, coordinates, dimensions, geometric properties, graph values and sample-space outcomes are verified as applicable.
- Decorative mathematical imagery does not substitute for a model.
- A photograph is not used as mathematical evidence unless its quantity, partition, scale and perspective are exact.
- Semantic colour is consistent across corresponding quantities and is not the only cue.

#### Teaching sequence and gradual release
- For a new or fragile concept, meaning and a complete model precede guided and independent work.
- During concept introduction or procedure development, students normally make an observable response after no more than two consecutive explanation/model slides unless an explicit instruction requires another structure.
- A `We do` slide genuinely requires student participation and does not already display the completed answer, final landing point, completed model or all working.
- Scaffolds fade deliberately rather than disappearing between a fully completed model and unsupported independent work.

#### Model-to-practice alignment
- The hardest independent task has a clear modelled precursor.
- Independent demand aligns in concept, operation or relationship, representation, number type, number of steps, strategy selection, language demand, reasoning demand and expected output.
- An unmodelled operation, representation, complexity or reasoning demand is either removed or explicitly identified as extension.

#### Task and answer integrity
- Every task states the action, mathematical focus, representation/resource where required and expected output.
- No vague or figurative instructional shorthand is used.
- A question slide does not reveal the answer through completed working, answer-coloured objects, final landing points, completed models or teaching-only cues.
- The answer addresses every command in the prompt, including any requirement to explain, compare, justify, label, prove, draw or write an equation.
- The requested strategy or representation is modelled on the answer slide.
- Valid alternative methods or answers are acknowledged where relevant.
- The primary answer and meaningful mathematical change are visually dominant.

#### Variation, misconceptions and demand
- Practice uses purposeful variation rather than random surface changes.
- Examples and non-examples differ in a mathematically meaningful way.
- Any misconception uses plausible student reasoning and the correction identifies the mistaken assumption, violated property/relationship and correct reasoning.
- A calculation, reasoning task and problem-solving task are labelled according to their actual demand.
- A routine worded calculation is not presented as problem solving solely because it has a context.

#### Exit evidence
- Exit evidence measures the intended mathematical concept rather than only the ability to copy a representation or follow a displayed procedure.
- The exit task does not introduce a new conceptual demand.

Any failure in this section blocks release and is routed to `dlp-maths-lesson`.

## Visual QA

Apply the repository standards:
- `references/universal-maths-instruction-canon.md` for Mathematics content;
- `references/slide-deck-quality-standards.md`;
- `references/semantic-colour-standard.md`;
- `references/panel-containment-standard.md`;
- `references/visual-exemplar-standard.md`.

### Visual-exemplar fidelity gate

Treat the checksum-verified edited Tuesday deck as a visual-only benchmark.
Require the assembled deck to retain:

- the full-height role-coloured left rail on every projected slide;
- amber reminder/model slides, blue question/task slides and green
  answer/successful-model slides;
- compact uppercase eyebrows plus a clear, larger slide title;
- a dominant main panel with deliberately subordinate cues or explanations;
- Trebuchet MS as the dominant teaching-deck typeface;
- comparable canvas use, padding, hierarchy and projected legibility.

Content and pedagogy must come from the current component contracts,
Mathematics canon and regression records. Copying a documented exemplar content
error fails even when the deck looks faithful.

Where scripts are available, run:
- `python scripts/audit_pack_contract.py --deck <deck> --context-record <context.json> --component-record <record.json> --out <report.json>`;
- if the user explicitly changed the default Literacy warm-up count, add `--literacy-count <n>` with the authorised count;
- `python scripts/audit_slide_typography.py --deck <deck> --out <report.json>`;
- `python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`;
- `python scripts/audit_visual_exemplar.py --deck <deck> --out <report.json>`.

Automated checks are screening tools. Render and inspect the final deck at full size. Any text that crosses or visually escapes its intended coloured, shaded or bordered panel blocks release. A filled instructional text panel with less than the required internal margin also blocks release. A panel-heavy deck receiving zero meaningful panel/text pair coverage fails the automated audit; do not treat that result as a clean geometry pass.

For Morning Work, also fail a slide that technically contains all text but is visually crowded, repeats low-value chrome, or divides a short independent task into too many competing cards. For warm-ups, inspect automatic wrapping at the character level; a broken mathematical word is a release-blocking defect even when the geometry scripts report no overflow.

## Classroom-feedback regression record

Use all relevant regression records whenever a change affects the orchestrator, component skills, warm-up architecture, Guided Reading scope, Shared Reading structure, student-facing language, Mathematics instructional language, mathematical representations, projected typography, semantic colour, panel containment or release QA:

- `examples/benchmarks/t3w6-monday-modular-regression.md`;
- `examples/benchmarks/t3w6-tuesday-release-regression.md`;
- `examples/benchmarks/t3w6-thursday-literacy-regression.md`;
- `examples/benchmarks/universal-maths-canon-regression.md`;
- `examples/benchmarks/memory-independent-wednesday-regression.md`.

For a change affecting Mathematics pedagogy, representations, task architecture or QA, test at least two representative prompts from different concept families in `universal-maths-canon-regression.md`. A change fails if it improves one concept family while breaking the universal requirements in another.

The Tuesday record is an approved minimum standard for Morning Work, Literacy warm-up and Shared Reading architecture, with explicit Literacy exclusions. Retain its approved characteristics while rejecting the unclear combine instruction, multiple-response prompts, weak distractors and contestable precision claim documented in that record.

## Regression rule

When revising after a FAIL, re-run the **entire** applicable checklist, not only the defect that triggered the revision. This prevents a fix in one area from breaking a previously passing requirement.
