---
name: daily-lesson-pack
description: Orchestrate timetable-aligned, year-profile-aware Daily Lesson Packs by resolving runtime teacher context, routing each teaching component to a specialised Daily Lesson Pack skill, assembling the outputs, and requiring independent QA before release.
---

# Daily Lesson Pack — Orchestrator

## Purpose

Coordinate a classroom-ready daily pack. Do not generate detailed subject content in this skill when a specialised component skill owns it.

The orchestrator owns:
- active year-level profile resolution;
- date, term, week and timetable resolution;
- separation of year-level context from teacher/school runtime context;
- source hierarchy and progression decisions;
- specialist-subject exclusions;
- component routing;
- cross-component consistency;
- final assembly, briefing and print plan;
- release only after `dlp-pack-qa` passes.

The specialised skills own the pedagogy, wording and slide rules for their component, interpreted through the active year-level profile.

## Request routing

### Daily pack

Use this orchestrator for a named day's Daily Lesson Pack. Resolve the active year profile and runtime teacher context, invoke the required components, assemble them, then run independent QA.

### Existing-pack audit or revision

Route the supplied Daily Lesson Pack directly through `dlp-pack-qa`. If it fails, send each defect only to the owning component skill, revise that component, rebuild the affected artefact, and re-run the complete applicable QA suite.

### Weekly Mathematics pack

A complete Term/Week Mathematics pack belongs to the standalone `weekly-maths-pack` skill. Route the request there rather than rebuilding weekly Mathematics logic inside this Daily Lesson Pack orchestrator. If direct skill routing is unavailable, use the standalone Weekly Maths Pack contract supplied in the environment; do not duplicate its full rules here.

## Context architecture

Before resolving a pack, read both:

- `references/year-level-context-contract.md`;
- `references/shared-class-context-contract.md`.

They serve different purposes and must not be collapsed.

### Year-level contextual base

The active year-level profile defines stable developmental and curriculum-facing calibration: expected prior knowledge, language load, reasonable task demand, independence, scaffolding and year-appropriate misconceptions/representations.

Supported year profiles must be explicitly authored under `references/year-level-profiles/`. Do not silently approximate an unsupported year by reusing another profile.

Current profiles include:

- `year-4-5` — established calibrated baseline;
- `year-6` — isolated calibration scaffold; follow its release-status rules until mature.

### User/school runtime context

The teacher supplies or connects the current timetable, Maths/English overviews, current sequence, interruptions, class/output constraints and lesson-status exceptions. These determine **what is being taught now and when**, not the definition of the year level.

A user's timetable, class size or overview must never be copied into a year-level profile merely because it was used to generate a pack.

## Source hierarchy

Use sources in this order:

1. the user's current explicit instruction;
2. current-run user/school context: timetable, overviews, unit plans, day-level focus and explicit status exceptions;
3. the active year-level profile for developmental/curriculum pitch;
4. connected calendar and authoritative school sources where available;
5. bundled universal component-skill defaults and instructional canons.

For **current lesson focus and local sequencing**, the user's current overview/program outranks the year-level profile.

For **developmental pitch**, the active year-level profile outranks historical examples from another year level or class.

Do not use chat memory, saved personal context, another account's Project context or an unstated standing preference as evidence for timetable facts, lesson focus, progression, copy quantity or classroom routines. A remembered detail may identify a question to ask, but it must not silently supply the answer. The repository package plus current-run sources must be sufficient to reproduce the pack in a clean account.

Assume the previous scheduled lesson was covered sufficiently to advance unless an authoritative runtime source explicitly records partial completion, cancellation or reteaching. Missing status is not evidence that a lesson was missed.

If a user's overview defines only some weekdays, do not invent the missing day's focus from another day or another user's historic sequence. Use the requested teacher's explicit day-level focus or another authoritative current-run source.

Do not browse the public web to infer school dates or timetable events unless the user asks for verification.

## Year-profile isolation rule

Apply changes at the narrowest justified scope.

- A Year 6 calibration correction belongs in `references/year-level-profiles/year-6.md` unless evidence shows it is universal.
- A Year 4/5 calibration correction belongs in `references/year-level-profiles/year-4-5.md` unless evidence shows it is universal.
- A teacher/school preference belongs in runtime context unless deliberately promoted after broader validation.
- A truly universal pedagogy, QA or rendering improvement belongs in the relevant shared component/core contract.

Year-level profiles are protected baselines, not immutable files. Deliberate improvements are allowed. Cross-year drift is not.

When a shared/core change could affect task demand, language, assumed prior knowledge or scaffolding, apply `examples/benchmarks/year-profile-isolation-regression.md` before release.

## Mandatory visual exemplar

For every teaching deck, read `references/visual-exemplar-standard.md` and use
`assets/visual-exemplars/t3w6-tuesday-edited-visual-exemplar.pptx` as the
approved **visual-only** design source. Verify its SHA-256 before use. Preserve
its role-colour grammar, full-height left rail, compact eyebrow/title hierarchy,
primary/secondary panel structure, Trebuchet MS typography and efficient use of
the 16:9 canvas.

Do not inherit the exemplar's lesson wording, year-level pitch, sequencing errors or superseded pedagogy. The current orchestrator, active year profile, component contracts, Mathematics canon and regression records remain authoritative for content.

## Mandatory Mathematics canon

For every main Mathematics lesson, `dlp-maths-lesson` must read and apply `references/universal-maths-instruction-canon.md` before generation. The component must complete the canon's internal planning contract and substantiate its Mathematics acceptance checks before assembly.

Mathematics warm-ups and Morning Work apply the canon's mathematical-accuracy, terminology, representation, question/answer and answer-integrity rules while remaining retrieval tasks rather than new teaching.

The universal Mathematics canon does not replace the active year profile or visual standards. Mathematics content must pass the year-level calibration, mathematical-instruction canon and shared projected-readability, semantic-colour and panel-containment standards.

## Scope boundary

Art, Japanese, Science, Music and Physical Education are specialist-led under the current core contract. Name their timetable block only unless the user explicitly supplies another authorised component contract. Do not generate lessons, slides, printables, answers, contingencies, preparation tasks or status capture for them by default.

`Student guided learning` is teacher-supervised but has no standing Daily Lesson Pack sequence. Name the block unless an authoritative current plan identifies the activity.

HASS requires a separate authoritative HASS plan or an explicit current user instruction. Do not invent HASS from reading contexts.

## Component routing

Route to these skills when the component is required:

- `dlp-morning-work`
- `dlp-literacy-warmup`
- `dlp-shared-reading`
- `dlp-guided-reading`
- `dlp-writing-lesson`
- `dlp-numeracy-warmup`
- `dlp-maths-lesson`
- `dlp-pack-qa`

If direct cross-skill invocation is unavailable, read and execute the corresponding bundled contract at `skills/<skill-name>/SKILL.md`. This fallback is mandatory; never silently substitute generic generation.

Every content-component handoff must include:

- `active_year_profile`;
- profile path/version/status;
- current lesson focus from runtime sources;
- curriculum boundary where available;
- relevant timetable/time constraint;
- explicit user overrides;
- source provenance required for QA.

## Orchestration workflow

1. Resolve the requested year level or combined year band from current-run user/school sources.
2. Load the matching profile under `references/year-level-profiles/`. If no supported profile exists, mark year profile `unresolved` and block classroom-ready release rather than borrowing another profile.
3. Resolve exact date, term, week, day, timetable and interruptions from the current run's supplied sources.
4. Resolve current Maths and English/literacy sequence, day-level focus and explicit status exceptions from the user's current sources.
5. Verify and load the approved visual-only exemplar.
6. Build one shared context object containing only information the components need: active year profile/path/status, runtime source provenance, lesson focus, curriculum boundary, authorised local allocation, time available and output constraints.
7. Route each required component to its specialised skill and require a component acceptance result before assembly. For `dlp-maths-lesson`, require the universal Mathematics planning contract and canon checks in the acceptance evidence.
8. Record the scheduled components and each component's `PASS` or `FAIL`, checks completed and artefact/slide range in a temporary component-acceptance record. Treat a missing record, missing scheduled component or unsubstantiated `PASS` as `FAIL`.
9. Block assembly until every scheduled content component records `PASS`. This gate does not replace independent final QA.
10. Keep Morning Work, Literacy warm-up and Shared Reading as genuinely distinct tasks and texts. Represent Guided Reading only according to the current Guided Reading component contract.
11. Keep the Mathematics warm-up separate from prerequisite checking and the main Mathematics lesson.
12. Assemble components in timetable order. Slide 1 is always Morning Work when Morning Work is required.
13. Create only useful printables. Prefer books, mini-whiteboards, oral work and manipulatives when a worksheet adds no value and when those response modes are authorised by runtime context.
14. Create the teacher briefing and any weekly printing plan from the actual generated resources and current-run quantities, not from another user's standing assumptions.
15. Send the complete assembled pack, context-source record, active year-profile record, presentation-audit evidence and component-acceptance record to `dlp-pack-qa`.
16. If QA returns FAIL, route each defect back only to the owning component skill, revise, and re-run the full applicable QA suite. Do not patch unrelated components.
17. Release only after critical QA checks pass and the active year profile's own release-status requirements are satisfied.

If actual printing is requested and copy quantity cannot be resolved from an authoritative runtime source, treat quantity as unresolved rather than inventing it.

If any required runtime input in `references/shared-class-context-contract.md` is unresolved, ask one concise question and block classroom-ready release. Do not use remembered context to fill the gap.

If the active year-level profile itself is marked calibration/candidate-only, generated output may be reviewed and refined, but must not be labelled as an established classroom-ready baseline until the profile's release conditions are met.

## Cross-component invariants

- Every content component uses the same active year-level profile as the orchestrator.
- Morning Work and Shared Reading must not reuse the same passage.
- Literacy warm-up uses 10 self-contained `Reminder -> Question -> Answer` sequences unless the user changes the count. A question must not depend on remembered content from another slide.
- Guided Reading follows its own current component contract and authorised schedule; never infer ability labels from the year profile.
- Shared Reading must alternate each paragraph-and-question slide with its immediately following matched answer slide; answers are not revealed early on question slides.
- The writing lesson teaches the current writing focus supplied by the user's overview; a historical class genre or weekday progression is not a universal default.
- Student-facing instructions must state the action, mathematical/literacy focus, any required representation or resource, and the expected student output where applicable.
- When a task transforms supplied language, name the exact operation. For example, say `Combine the two sentences using the conjunction “because”`, not merely `Write a sentence`.
- Student-facing task language must be understandable within the active year profile. Accurate technical terminology is retained and explained rather than replaced by vague substitutes.
- Teacher preparation, timing, misconceptions and answers belong in the briefing or notes, not as clutter on student task slides.
- Warm-up slides use the established projected-readability and semantic-colour standards.
- No generic whiteboard footer is required unless the user explicitly requests one. The Mathematics green `Why` panel is instructional content, not a generic footer instruction.
- The main Mathematics lesson must apply the complete universal Mathematics canon, including meaning before procedure, purposeful representation, genuine guided practice, model-to-practice alignment and complete answer modelling.
- Mathematics warm-ups and Morning Work must remain retrieval while still using exact mathematics, precise terminology and non-revealing question slides.
- A Mathematics question requiring a model, explanation, comparison, justification, proof, label or equation must have an answer slide that demonstrates every requested element.

## Assembly outputs

Daily mode normally produces:
- one coherent teaching deck;
- only necessary student printables;
- separate teacher answers where useful;
- a concise daily briefing;
- a weekly printing plan when requested/applicable and supported by current-run quantities.

For a relief day, keep the timetable but make teacher-led sequences self-contained: explicit materials, scripts, answers, stopping points and independent alternatives. Keep teacher-facing preparation out of Morning Work.

## Release rule

The orchestrator never self-certifies quality. `dlp-pack-qa` is the release authority.

Run the deterministic contract audit during final QA:

`python scripts/audit_pack_contract.py --deck <deck> --context-record <context.json> --component-record <record.json> --out <report.json>`

If the user explicitly changes the default Literacy warm-up count, also pass `--literacy-count <n>` with the authorised count.

Run the projected-readability and panel-containment audits on the final deck:

- `python scripts/audit_slide_typography.py --deck <deck> --out <report.json>`
- `python scripts/audit_panel_containment.py --deck <deck> --out <report.json>`
- `python scripts/audit_visual_exemplar.py --deck <deck> --out <report.json>`

Apply the existing classroom-feedback regression records whenever the affected components change. Treat those records as approved Year 4/5 benchmarks where their content is Year 4/5-specific; do not use them as Year 6 pitch sources.

Apply `examples/benchmarks/memory-independent-wednesday-regression.md` whenever context routing, source precedence, overview handling, timetable resolution or packaging changes.

Apply `examples/benchmarks/year-profile-isolation-regression.md` whenever year-profile routing, a year profile, or a shared rule that can affect pitch changes.

For any change affecting Mathematics pedagogy, representations, task architecture or QA, also apply `examples/benchmarks/universal-maths-canon-regression.md` to at least two different concept families before release.

Any audit or applicable regression failure blocks release.
