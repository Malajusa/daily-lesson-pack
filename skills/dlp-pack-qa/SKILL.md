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

### Year-level profile gate
- Apply `references/year-level-context-contract.md`.
- The context record identifies one active supported year-level profile and its path/version/status.
- Every content-component acceptance record uses the same active year profile as the orchestrator.
- The user's timetable, class size, current Maths/English overview and local weekly sequence remain runtime context; they are not treated as year-level calibration evidence merely because they were used for this pack.
- Fail cross-year leakage: a Year 6 component must not rely on Year 4/5-specific pitch rules or examples as authority, and a Year 4/5 component must not inherit Year 6-only assumptions unless an explicitly universal rule has been validated.
- A year-profile-specific change that could affect another year level must satisfy `examples/benchmarks/year-profile-isolation-regression.md`.
- If the active year profile is marked candidate/calibration-only, do not label the output an established classroom-ready baseline unless that profile's release conditions have been met for the pack.

### Context provenance gate
- Apply `references/shared-class-context-contract.md`.
- A context-source record identifies the current source for year level, date/term/week/day, timetable, Mathematics focus, English/literacy focus, lesson-status exception and printing quantity when printing is requested.
- The record distinguishes runtime user/school sources from the active year-level profile source.
- The record must not cite chat memory, saved personal context, another account's Project context or an unstated standing preference as authority for runtime facts.
- Missing required context blocks classroom-ready release; it is queried rather than guessed.
- Do not inherit another user's fixed class size, four-day overview, Wednesday arrangement, genre sequence or local timetable as a default.

### Component acceptance gate
- Apply `references/component-instance-contract.md` and require schema version 2.
- The context and acceptance records list every scheduled content instance with a unique ID, owner, start, duration and purpose.
- Repeated component owners are valid when instance IDs differ; repeated IDs are not.
- Every instance records `PASS`, the active year profile, estimated minutes, stable check IDs, concrete evidence and its artefact or slide range.
- The evidence record identifies the generation run and is bound to the audited deck SHA-256. Independent semantic and rendered-review records cite that generation run and use different review run IDs. Freeform strings such as `checked` are not evidence.
- A missing instance, time-budget overrun, missing evidence, duplicate instance result, profile mismatch or component `FAIL` blocks assembly and release.
- Component acceptance does not replace this independent whole-pack review.

### Sequence and scope
- Slide 1 is Morning Work when required.
- Every Morning Work instruction is executable from the projected slide using the response mode authorised by runtime classroom context; no task asks students to mark projected-only content.
- Morning Work is scannable at projection size: related tasks are grouped, the core is not padded with an unnecessary extension, and comfortable internal spacing remains after all content is placed.
- Timetable order is coherent.
- Distinct timetable blocks remain distinct component instances. A lesson resumed after a break has a visible breakpoint.
- Specialist subjects are timetable labels only under the current core contract unless an explicit authorised component says otherwise.
- No unauthorised specialist printables or generated lessons exist.
- Morning Work and Shared Reading use different texts.
- Mathematics warm-up remains separate from the main Mathematics lesson.

### Literacy warm-up
- 10 `Reminder -> Question -> Answer` sequences unless explicitly overridden.
- Every question contains all information needed to answer it and does not depend on another slide.
- Every question follows the active year-profile warm-up response contract; by default it requires one direct response only and the answer slide supplies the concise teaching explanation.
- In a choice task, students select only the option unless another response demand is explicitly authorised; any concise rationale normally belongs on the answer slide.
- Every reminder teaches the method with a different example and does not reveal the next answer.
- Every reminder places a concise applicable `Remember:` rule inside its yellow panel. A punctuation reminder uses a separate example with the target punctuation green, bold and at least 125% of the surrounding size.
- No spelling/Sound Waves replacement content unless explicitly authorised by an active profile contract.
- Every answer follows its question and the primary answer is visually dominant.
- Inserted punctuation or changed wording is immediately locatable through green, bold, enlarged treatment plus a textual cue; meaning does not rely on colour alone.
- Judge punctuation emphasis from the exported render as well as the PPTX text runs; intended styling that renders flat fails.
- Explanations teach the relevant rule and do not use generic statements such as `the answer matches the prompt`.
- Student language is immediate and appropriate to the active year profile.
- The question title and instruction name the exact operation demonstrated by the answer. A sentence-combination task must say `combine` or `join`; `write a sentence` is insufficient.
- Use accurate curriculum terminology with a plain-language explanation. Fail vague substitutions such as `linking word` when `conjunction` is the correct grammatical term.
- Put inverted commas around a literal word or phrase when it is being discussed as language, while leaving the same word unquoted when it operates normally inside an example sentence.
- Multiple-choice options are grammatically parallel and similar enough in length, detail and tone that every distractor is plausible for the active year profile until the target rule is applied. Replace the item if a credible distractor cannot be written.
- A word described as `more precise` adds a clear, defensible semantic feature while preserving the original meaning. Formality, technicality or unfamiliarity alone is not precision.
- Reject debatable synonym rankings, including presenting `rotate` as automatically more precise than `turn` for a propeller. The supplied answer explanation must be sufficient; the teacher must not need to invent a semantic defence.
- Each reminder, model, question, answer and explanation uses the same rule or convention.
- A list-comma reminder must not require a comma after every non-final item while its model or answer omits the optional comma before `and` or `or`.

### Shared Reading
- Uses a strict alternating question/answer sequence.
- Every question slide contains exactly one short paragraph and one question about that paragraph.
- Passage density, syntax, vocabulary support and comprehension demand are appropriate to the active year profile; a higher year is not created merely by lengthening text or making words obscure.
- Every answer slide immediately follows and matches only the preceding question slide.
- The complete model answer is visually dominant; any supporting evidence is concise and relevant.
- The question slide does not reveal the answer or teaching-only evidence cue when students are meant to locate it independently.
- Answer slides do not introduce a new paragraph, new question or unrelated content.
- Paragraph/question separation on question slides is visually obvious.
- Text is projected at sensible size; split/shorten rather than shrink.
- Every title, question and answer is supported by the displayed paragraph.
- Any inference follows from explicit clues in the paragraph and the model answer makes that connection clear.

### Guided Reading
- Guided Reading follows the current Guided Reading component contract.
- Under the current timetable-only setting, no Guided Reading text, teacher guide, prompts, transition task or instructional slide is generated.
- Any displayed group is taken from an authoritative current schedule and is exactly `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon` where that naming system is active.
- No ability descriptor, inferred group name or year-profile-derived ability label appears.

### Writing
- Current writing/English overview, not a historical hard-coded weekday spine, supplies the current genre/toolkit feature and sequence.
- Current toolkit feature is explicitly taught/applied.
- A model/joint construction is present where needed.
- Students produce writing demonstrating the feature.
- Writing load, independence and scaffolding are appropriate to the active year profile.
- Student-facing wording uses familiar, actionable language; necessary technical terms are defined before use.
- Technical-word substitutions preserve meaning and the explanation states the exact information added.
- A controlled vocabulary model preserves the sentence's core proposition; a revision that adds several facts is labelled as elaboration.
- Comparison tables are split before their content becomes undersized.

### Numeracy warm-up
- 5 prompt/answer pairs (10 slides total) unless the validated profile or current request explicitly overrides the count.
- Prompt slides contain three separate All / Most / Some questions, not three answer-quality expectations for one question.
- The active year profile determines reasonable retrieval floor, number types/magnitudes and the ceiling for `Some`.
- `Some` does not automatically jump into the next year level.
- Green `Why` panel contains reasoning, not generic checking instructions.
- Question and answer slides match.
- No mathematical word is split inside the word across lines. Intentional line breaks may separate an equation from a complete word, but must not produce fragments such as `quarte` / `rs`.
- The warm-up retrieves already taught knowledge rather than introducing a new procedure.
- Mathematical terminology, notation, diagrams, scales and representations are accurate.
- A prompt slide does not reveal its answer through completed working, colour or an already completed model.
- Every meaningful tier task or answer is at least 36 pt; substantive `Why` text is at least 28 pt. Inspect each element rather than the slide maximum.

### Main Mathematics lesson

Apply `references/universal-maths-instruction-canon.md` in full and verify consistency with the active year-level profile.
Apply `references/fraction-equivalence-standard.md` when equivalence or fraction-decimal conversion is taught.

#### Planning and scope
- The Mathematics component acceptance record substantiates every required planning-contract check rather than recording a generic `PASS`.
- The active year profile is recorded before the curriculum concept and lesson boundary.
- The curriculum concept and lesson boundary agree with the current user/school Maths source.
- The lesson is classified as concept introduction, procedure development, fluency development, reasoning, problem solving or review/assessment.
- Unless explicitly review, consolidation or extension, the lesson introduces one central new mathematical idea rather than several substantial new concepts.
- Focused prerequisite retrieval is distinct from the cumulative Mathematics warm-up.
- Year 6 demand is not produced by mechanically enlarging Year 4/5 numbers, text length or step count.
- Each Mathematics timetable block has its own instance ID, purpose and feasible time estimate.
- Mixed Year 4/5 instruction states a common central idea and provides substantive Year 4 and Year 5 pathways. An inactive year level receives an authorised prerequisite/consolidation bridge, not the other year's outcome by implication.

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
- Fraction equivalence is shown through the original partition, repartitioning of every part, the invariant amount and the multiplicative relationship. A finished hundred grid alone fails.

#### Teaching sequence and gradual release
- For a new or fragile concept, meaning and a complete model precede guided and independent work.
- During concept introduction or procedure development, students normally make an observable response after no more than two consecutive explanation/model slides unless an explicit instruction or active profile requires another structure.
- A `We do` slide genuinely requires student participation and does not already display the completed answer, final landing point, completed model or all working.
- Scaffolds fade deliberately rather than disappearing between a fully completed model and unsupported independent work.

#### Model-to-practice alignment
- The hardest independent task has a clear modelled precursor.
- Independent demand aligns in concept, operation or relationship, representation, number type, number of steps, strategy selection, language demand, reasoning demand and expected output.
- Independent demand remains appropriate to the active year profile.
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
- Any misconception uses plausible student reasoning for the active year profile and the correction identifies the mistaken assumption, violated property/relationship and correct reasoning.
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
- `references/component-instance-contract.md`.
- `references/fraction-equivalence-standard.md` where applicable.

### Visual-exemplar fidelity gate

Treat the checksum-verified edited Tuesday deck as a visual-only benchmark.
Require the assembled deck to retain:

- the full-height role-coloured left rail on every projected slide;
- amber reminder/model slides, blue question/task slides and green answer/successful-model slides;
- compact uppercase eyebrows plus a clear, larger slide title;
- a dominant main panel with deliberately subordinate cues or explanations;
- Trebuchet MS as the dominant teaching-deck typeface;
- comparable canvas use, padding, hierarchy and projected legibility.

Content and pedagogy must come from the current active year profile, component contracts, Mathematics canon and regression records. Copying a documented exemplar content error or Year 4/5-specific pitch into Year 6 fails even when the deck looks faithful.

Where scripts are available, run:
- `python scripts/audit_pack_contract.py --deck <deck> --context-record <context.json> --component-record <record.json> --out <report.json>`;
- `python scripts/audit_year_profile_context.py --deck <deck> --context-record <context.json> --component-record <record.json> --out <year-profile-report.json>`;
- if the user explicitly changed the default Literacy warm-up count, add `--literacy-count <n>` with the authorised count;
- `python scripts/audit_slide_typography.py --deck <deck> --dispositions <warning-ledger.json> --out <report.json>`;
- `python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`;
- `python scripts/audit_visual_exemplar.py --deck <deck> --review-record <visual-review.json> --out <report.json>`;
- `python scripts/audit_release_bundle.py --deck <deck> --contract <contract.json> --year-profile <year-profile-report.json> --typography <typography.json> --containment <containment.json> --visual <visual.json> --semantic-review <semantic-review.json> --out <release.json>`.

Automated checks are screening tools. Render and inspect the final deck at full size. The visual screening audit cannot certify its own manual checks: it requires a separate evidence-bearing review record from an independent reviewer. Any text that crosses or visually escapes its intended coloured, shaded or bordered panel blocks release. A filled instructional text panel with less than the required internal margin also blocks release. A panel-heavy deck receiving zero meaningful panel/text pair coverage fails the automated audit; do not treat that result as a clean geometry pass.

Every automated warning is unresolved until a ledger entry identifies its slide,
code, decision, evidence, reviewer and run ID and is bound to the deck hash.
Batch statements such as `all unused-space notices are intentional` fail.
Repository-owned generic audits are the only automated release gates; reject
generated one-off scripts with hard-coded slide totals or exact answer strings.

For Morning Work, also fail a slide that technically contains all text but is visually crowded, repeats low-value chrome, or divides a short independent task into too many competing cards. For warm-ups, inspect automatic wrapping at the character level; a broken mathematical word is a release-blocking defect even when the geometry scripts report no overflow.

## Classroom-feedback and profile regression records

Use all relevant regression records whenever a change affects the orchestrator, component skills, warm-up architecture, Guided Reading scope, Shared Reading structure, student-facing language, Mathematics instructional language, mathematical representations, projected typography, semantic colour, panel containment, year-profile routing or release QA:

- `examples/benchmarks/t3w6-monday-modular-regression.md`;
- `examples/benchmarks/t3w6-tuesday-release-regression.md`;
- `examples/benchmarks/t3w6-thursday-literacy-regression.md`;
- `examples/benchmarks/universal-maths-canon-regression.md`;
- `examples/benchmarks/memory-independent-wednesday-regression.md`;
- `examples/benchmarks/year-profile-isolation-regression.md`;
- `examples/benchmarks/t3w7-thursday-known-failure.md`.

Treat Year 4/5 classroom-feedback records as Year 4/5 calibration evidence where their content is year-specific. Their visual and universal architecture lessons may apply more broadly only when the relevant shared rule says so.

For a change affecting Mathematics pedagogy, representations, task architecture or QA, test at least two representative prompts from different concept families in `universal-maths-canon-regression.md`. A change fails if it improves one concept family while breaking the universal requirements in another.

The Tuesday record is an approved minimum standard for Year 4/5 Morning Work, Literacy warm-up and Shared Reading architecture, with explicit Literacy exclusions. Retain its approved Year 4/5 characteristics while rejecting the unclear combine instruction, multiple-response prompts, weak distractors and contestable precision claim documented in that record. Do not treat its Year 4/5 content pitch as the Year 6 standard.

## Regression rule

When revising after a FAIL, re-run the **entire** applicable checklist, not only the defect that triggered the revision. This prevents a fix in one area or year profile from breaking a previously passing requirement elsewhere.
