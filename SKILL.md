---
name: daily-lesson-pack
description: Generate and quality-assure timetable-aligned daily teacher lesson packs and Year 4/5 weekly mathematics packs, including classroom slides, printables, answers, briefings and evidence-backed release checks. Use when the user asks for today's, tomorrow's or a named day's teaching resources, lesson slides, worksheets, answer keys, Morning Work, a daily plan, or a Term/Week mathematics pack.
---

# Daily Lesson Pack

## Purpose

Create practical, classroom-ready resources for one school day or a complete Year 4/5 Mathematics week. Use the authoritative timetable, current calendar, source index, active unit plans, curriculum references and explicit lesson-status exceptions. Scheduling, delivery and persistent automation belong to the surrounding workflow in `references/automation-blueprint.md`.

## Modes

- **Daily:** teacher briefing, one coherent teaching deck, only necessary student printables and separate teacher answers.
- **Weekly Mathematics:** teacher plan first, then the deck, printables and answer key mapped to the actual weekly blocks.
- **Audit/revision:** inspect the supplied artefact at full size and run every applicable file-level check. Report artefact defects separately; missing package evidence blocks package release but does not prevent a useful audit.

Infer the mode from the request. Ask one concise question only when the ambiguity would materially change the package.

For a relief day, keep the authoritative timetable but make every teacher-led sequence self-contained for a relief teacher: explicit materials, scripts, answers, stopping points and independent alternatives. Keep teacher-facing preparation in the briefing or notes, not on the Morning Work slide. Preserve the specialist-subject boundary.

Morning Work uses the available arrival window before the first formal timetable block, up to 20–30 minutes. It must not consume the 08:30 lesson unless the authoritative timetable explicitly places it there. If the arrival duration is unavailable, provide a 10–15-minute accessible core plus extensions that carry independent work to 30 minutes, and record that conservative assumption without blocking the build.

## Required routing

Read the relevant planning sources:

- `references/source-index.md`, `planning-context.md`, `planning-state-schema.md` and `2026-term-3-timetable.yaml`.
- `references/output-spec.md` and `print-production-preferences.md`.
- `references/english-planning-rules.md` and `effective-printable-design.md` for English or printables.
- `references/mathematics-planning-rules.md`, `weekly-maths-pack-patterns.md`, `year-4-5-maths-overview.json` and `wa-maths-code-map.json` for Mathematics.
- `references/create-numeracy-flashcards-snapshot.md` whenever Mathematics is taught. This bundled v10 specification is authoritative for the Daily Lesson Pack mathematics warm-up. If the standalone `create-numeracy-flashcards` skill differs, the bundled 4 + 6 architecture and calibration rules take precedence within this skill.
- For Term 3 Year 4/5 daily packs on Monday, Tuesday, Thursday or Friday, also read `references/term-3-four-day-overview.json` and `references/term-3-four-day-overview.md`. Use the JSON for deterministic week/day lookup and the Markdown for explanatory rules.

Before constructing any teaching deck, read all of:

- `references/slide-deck-quality-standards.md`
- `references/semantic-colour-standard.md`
- `references/student-facing-instructions.md`
- `references/question-answer-slide-standard.md`
- `references/mathematical-visual-validation.md`
- `references/classroom-slide-archetypes.md`
- `references/daily-pack-quality-floor.md`
- `references/release-checklist-usage.md`
- `references/build-manifest-template.json`

Use the Presentations skill for PPTX work, and the Documents or PDF skill for those output types. The approved benchmark is `assets/daily-teaching-slides-quality-template.pptx`, extended by the approved archetype screenshots. Map slides by semantic role; do not adapt a visually similar but functionally incompatible slide.

For an existing-deck audit, export layout JSON, run `validate_slide_geometry.py`, then run `audit_teaching_deck.py --deck <deck> --geometry-report <report> --out <audit.json>`. Its `package_release_status` is always `not_assessed`; use the full build manifest only when judging package release.

## Source hierarchy and progression

Use sources in this order:

1. The user's current instruction.
2. A maintained status record when it records an exception.
3. Calendar and authoritative timetable.
4. Active unit and assessment plan.
5. For Term 3 Monday/Tuesday/Thursday/Friday daily planning, the four-day overview day lookup.
6. Other term/year overviews and curriculum maps.
7. Standing preferences and pedagogy.

Assume the previous scheduled lesson was covered sufficiently to advance unless an authoritative source explicitly records partial completion, cancellation or reteaching. Missing status is not evidence that a lesson was missed. For the Term 3 four-day overview, Monday normally follows the preceding Friday, Tuesday follows Monday, Thursday follows Tuesday and Friday follows Thursday. Wednesday remains a valid Daily Lesson Pack day from the authoritative timetable, but it is outside the four-day overview unless the user explicitly requests the overview to be applied. Do not browse the public web to infer school dates or timetable events unless the user asks.

## Scope boundary

Art, Japanese, Science, Music and Physical Education are specialist-led. Name their timetable block only. Never generate their lesson, slides, printables, contingency, preparation, answers or status capture, and never include them in the printing plan.

`Student guided learning` is teacher-supervised but has no standing lesson sequence in this skill. Name the block only unless a connected authoritative plan identifies its current activity; do not invent a lesson to fill it.

HASS is outside the Term 3 four-day overview. Do not invent HASS content from the overview, country-reading allocation or Information Report toolkit. A Tuesday HASS block may be planned only from a separate authoritative HASS plan or an explicit current user instruction; otherwise name the block and flag that its source plan is unavailable.

## Core planning workflow

1. Resolve the exact date, term/week, source index and authoritative day map.
2. For Term 3 Monday, Tuesday, Thursday or Friday, resolve the week/day in `references/term-3-four-day-overview.json`. Use its mathematics topic, WA code, day-level mathematics focus, Information Report toolkit component and daily stage, Shared Reading country, Guided Reading country and guided-reading group as mandatory planning inputs. Apply explicit user/status exceptions, but do not silently substitute another sequence. Wednesday uses the normal timetable and active plans unless the user explicitly requests overview use.
3. Apply explicit lesson-status exceptions; otherwise advance normally.
4. Remove specialist subjects from resource generation.
5. Keep Morning Work, Literacy warm-up, shared reading and guided reading as distinct functions with genuinely different passages.
6. Match the next lesson fragment to each teacher-led block. Give each lesson a visible student-friendly Learning Intention and 2–4 observable Success Criteria.
7. For Mathematics, run `python scripts/maths_week_brief.py --term <n> --week <n>`, identify the actual concept, then choose representations. A supporting number line does not become the lesson topic.
8. Generate the Mathematics warm-up through `create-numeracy-flashcards` when direct routing is supported, while enforcing the bundled v10 specification. Otherwise follow `references/create-numeracy-flashcards-snapshot.md` directly. Keep this cumulative 4 + 6 retrieval routine separate from the main Mathematics prerequisite check and lesson sequence.
9. Reuse an approved resource only when it meets the current intention. Reconstruct incompatible mathematical visuals and build clean content slides when no archetype fits.
10. Write the teacher plan and shared source data before generating slides, printables and answers. Generate repeated questions, diagrams and keys from that shared data.
11. Before slide generation, define the semantic-colour mapping required by the lesson: which concept, quantity, category, current step or reasoning panel each non-neutral colour represents. Use `references/semantic-colour-standard.md`; do not invent decorative colour roles.
12. Create only resources that improve learning; prefer books, mini-whiteboards, oral work or manipulatives when a printable adds no value.
13. Build, render, inspect, validate and release through the evidence workflow below.

If actual printing is requested, an unknown copy quantity is blocking. If printing is not requested, create a digital master and record the quantity as unresolved without blocking the resource build.

## Daily construction rules

### Morning Work

The first slide is always titled `Morning Work` and contains only the student task: numbered retrieval, substantive application, explanation/improvement and a meaningful extension. Do not place a decorative cover, date/week banner, timetable, routine, assembly logistics, `Get ready`, `Get out`, `You need` or materials list on it. Students already know the normal set-up. State a response location only when it is part of the task or differs from the established routine; put preparation and materials in the briefing or speaker notes. Supply work matched to the actual arrival window, normally up to 20–30 minutes. On an assembly morning, shorten the task to the available time and place the 8:35/location reminder in the briefing and a later transition slide, never on slide 1.

### Literacy warm-up

Where Literacy is teacher-led, create exactly five alternating response/answer pairs after Morning Work. Responses take about 20–45 seconds and produce visible work. Exclude spelling, phonics and Sound Waves content. Every answer immediately follows its question and presents the complete primary answer in bold, visually dominant body text with a brief why-explanation.

Guided reading is included only when the active plan or timetable requires it; the weekday framework then determines the correct group and band. In a one-hour Literacy block, run the guided conference concurrently with a genuinely independent post-warm-up task. If the required teaching cannot fit without compression, defer a component explicitly through the plan rather than shortening the warm-up, modelling or conference below its quality floor.

### Instructional sequence

Use stable phase labels where appropriate: `Retrieval`, `Model`, `We do`, `Guided practice`, `Independent practice`, `Answer`, `Review`, `Exit check`. Completely model a strategy before student use. Move through guided or joint construction before independent work when the feature is new. Ensure exit evidence measures the intended concept, not merely the representation.

Every student task visibly answers: what to do, where to respond, how much to produce and what success looks like. Put teacher-controlled branching, timing, answers and misconceptions in notes that match the visible example.

### Semantic colour

Colour must follow instructional structure rather than create visual variety. Keep ordinary information neutral and reserve non-neutral colour for a defined job: correspondence, category, current focus, meaningful change or an established reasoning panel. The same concept must keep the same colour while its identity is unchanged. A changed colour must signal a meaningful change.

Do not use colour as the only carrier of meaning. Preserve labels, fixed position, borders, shapes, symbols, direct labels or patterns so the slide remains interpretable in greyscale and for students with colour-vision deficiency. Avoid arbitrary rainbow headings, unrelated bright icons, saturated decorative backgrounds and low-contrast pastel treatments.

For worked examples, diagrams, charts and text-to-visual links, use the same restrained colour to connect corresponding information. Do not colour every step. When students are expected to identify the relationship independently, reduce teaching-only colour cues from `Model` to `We do` to `Independent practice` and assessment.

### Mathematics warm-up

Whenever the day includes a Mathematics lesson, include a separate Mathematics warm-up immediately before the main Mathematics section unless the user explicitly omits it. Use the bundled v10 Create Numeracy Flashcards specification as the authority; direct skill routing may generate content, but it may not replace or weaken these local requirements.

Create exactly 10 prompt-and-answer pairs, for exactly 20 warm-up slides, in this order:

1. Addition
2. Subtraction
3. Multiplication
4. Division
5. State it
6. Recognise it
7. Complete it
8. Apply it
9. Distinguish it
10. Cumulative retrieval

Immediately follow each prompt with its corresponding answer. Do not interleave the warm-up with main-lesson instruction. Questions 1–4 are short, year-level-appropriate calculations based on curriculum expectations. Questions 5–10 draw cumulatively from the current Mathematics Rules Worth Memorising PP–Year 10 source, an equivalent user-supplied memorisation spine, and appropriate prior-year knowledge. Do not preview later-year content merely to create challenge or force the warm-up to match the day's lesson topic.

For the established mixed Year 4/5 class, make Questions 1–4 accessible to Year 4 while still worthwhile for Year 5. Extend through the answer hierarchy rather than making the prompt inaccessible. Draw Questions 5–10 mainly from Year 4/5 and earlier knowledge.

Every answer slide uses exactly `All`, `Most` and `Some`:

- `All`: a genuinely accessible and mathematically safe foothold.
- `Most`: the concise, fully correct target response using precise year-level language.
- `Some`: a modest extension through a familiar explanation, condition, example, non-example, inverse check or connection, without automatically advancing to the next year level.

Treat `Most` as success. Put the complete primary answer in visually prominent bold text. Use a vinculum or properly stacked fraction rather than a forward slash on student-facing slides.

Use one fixed visual hierarchy for every Mathematics warm-up pair. On both the prompt and answer slide, `All`, `Most` and `Some` are the three main left-to-right body columns, with `Most` as the expected secure response. On prompt slides, the columns contain calibrated student tasks that map directly to the three response levels. On answer slides, they contain the matched responses. Put the `Why` reasoning prompt on the question slide and the concise `Why` explanation on the answer slide inside the green footer box. Do not use a fourth `Why` body card, and do not replace the green-footer `Why` content with a generic instruction such as `Check your answer`.

If colour is used to distinguish `All`, `Most` and `Some`, keep the labels and fixed positions primary and use only restrained, consistent accents or tints. Do not use red/amber/green traffic-light coding. The established green `Why` footer is a semantic reasoning signal and must not be reused for unrelated decoration.

The warm-up is cumulative retrieval only. It does not replace lesson-specific prerequisite checking, explicit reteaching, modelling, guided practice, independent application or exit assessment. Identify the 10-question warm-up separately in the daily briefing.

### Mathematics

Keep retrieval, readiness and prerequisite teaching distinct. Model at least one correct worked example from start to finish. For fraction comparison, teach strategy selection: same denominator, same numerator, equivalence, benchmark to one-half, distance from one and mixed/improper renaming; explain when a strategy is inconclusive. Differentiate through representation, reasoning and abstraction rather than only more questions.

Create a mathematical-visual specification before drawing. Verify all claims computationally, generate coordinates deterministically and inspect each final diagram at full size. Never broadly replace text on a slide containing a diagram or relabel an inherited visual.
For overview-controlled Term 3 days, the weekly mathematics topic and WA code in the four-day overview must agree with the Year 4/5 mathematics overview. The four-day overview supplies the day-level focus. Confirm the correct term/week/day, weekly topic/code, day-level focus and continuity before resource generation; task slides must not reveal answers and answer slides must model the strategy requested.


### Reading and writing

Count only substantive shared-text slides towards the 250-word minimum. Display the complete text at projected size across coherent sections with genuine subheadings. Keep first-reading comprehension and second-reading analysis separate, and make every referenced word or passage visible. Model the complete target product, annotate its required features, complete joint construction when needed, and protect independent writing time. Enforce the scheduled guided-reading level and word-count band, and match teacher guides exactly.

When colour links a Shared Reading question to a word, phrase or textual feature, use the same restrained colour for the correspondence and leave unrelated vocabulary neutral. Paragraph/question separation must remain clear through spacing, panel structure and typography without relying on colour alone. Do not highlight so much text that the cue loses meaning, and remove teaching-only evidence highlights when students are expected to locate evidence independently.

On Term 3 overview-controlled days, writing is a cumulative Information Report toolkit. Use the overview's named toolkit component and daily stage: Monday analyse/introduce, Tuesday explicitly teach, Thursday apply in drafting or revision, Friday edit/consolidate/publish. The lesson must name the component, teach or apply it explicitly, include a model/worked example when needed and require a student product demonstrating the component. Country fact collection cannot replace writing instruction.

On those same days, Shared Reading and Guided Reading use the countries assigned by the overview. They must be different countries; Morning Work must use a third independent passage/context and must not pre-teach either reading passage. Shared Reading is a whole-class comprehension/information-text lesson. Guided Reading must include a student text plus teacher prompts, expected responses, vocabulary support, literal comprehension, inference and an appropriate extended response. The overview-controlled guided-reading groups are Monday very low, Tuesday low, Thursday above level and Friday approximately Year 9 complexity. Wednesday retains the normal at-level allocation when guided reading is scheduled.


### Printables

Generate slides, student tasks and teacher answers from the same source data. Mirror wording, numbering and diagrams; keep answers separate; include alternative reasoning, misconceptions and next teaching moves. A4 pages must be greyscale-safe, readable at 100% and provide task-specific response space. Keep unresolved quantities and specialist subjects out of every student file.

## Weekly Mathematics workflow

1. Resolve term/week and run `maths_week_brief.py`.
2. Treat its topic and codes as the curriculum boundary, adjusted only by explicit status evidence.
3. Map one coherent learning arc to the actual Mathematics blocks, including separated blocks.
4. Diagnose the prerequisite chain from current evidence; do not infer weakness from missing status.
5. Design a shared Year 4/5 launch, appropriate differentiated pathways and a common reflection.
6. Build teacher plan → slides → necessary printables → teacher answers from shared source data.
7. Complete the same evidence-backed release gate as daily mode.

## Mandatory evidence-backed release

### Mathematics warm-up stop check

For every pack containing Mathematics, do not release/export until all applicable checks pass:

- exactly 10 Mathematics warm-up prompts and 10 paired answer slides are present;
- Questions 1–4 are Addition, Subtraction, Multiplication and Division in that order and are appropriate to the nominated year level;
- Questions 5–10 are State it, Recognise it, Complete it, Apply it, Distinguish it and Cumulative retrieval in that order;
- Questions 5–10 use the memorisation spine cumulatively without adding later-year content merely for difficulty;
- every prompt has one unambiguous student action and every answer immediately follows its prompt;
- every prompt and answer slide uses the same three-column `All` / `Most` / `Some` body, with the matched `Why` prompt or explanation in the green footer;
- every answer slide contains `All`, `Most` and `Some` at the required calibration;
- answers are mathematically correct, visually prominent and use vinculum/proper fraction formatting;
- the warm-up remains separate from the lesson prerequisite check and main teaching sequence.

A Daily Lesson Pack containing Mathematics fails pre-export QA if this warm-up is missing, shortened, reordered, replaced by generic arithmetic or absorbed into the main lesson.

### Semantic colour stop check

For every pack containing teaching slides, do not release/export until all applicable checks pass:

- every non-neutral colour has a defined instructional role or a necessary visual-system role;
- the same concept, quantity, category or representation keeps the same colour while its identity is unchanged;
- no colour is changed merely for variety between slides;
- ordinary information remains visually neutral enough for the intended signal to stand out;
- no essential distinction depends on colour alone;
- normal text meets at least `4.5:1` contrast, large text at least `3:1`, and meaningful graphical objects/boundaries generally meet `3:1` where applicable;
- the final render remains interpretable in greyscale and, where tooling allows, under red–green colour-vision-deficiency simulation;
- teaching-only colour cues are reduced when independent or uncued performance is the intended outcome;
- the green `Why` treatment is reserved for reasoning and is not repurposed decoratively;
- the deck contains no arbitrary rainbow coding, saturated competing decoration, red/green-only status coding or low-contrast pastel text.

If any essential distinction disappears without hue, the slide fails semantic-colour QA and must be revised before release.

### Term 3 four-day overview stop check

For Monday, Tuesday, Thursday and Friday Term 3 packs, do not release/export until all applicable checks pass:

- term/week/day lookup matches the four-day overview;
- Wednesday has not been treated as part of the overview unless explicitly requested;
- mathematics topic, WA code and day-level focus match the overview and the weekly mathematics authority;
- writing matches the scheduled toolkit component and daily stage;
- Shared and Guided Reading countries match the overview and differ from each other;
- guided-reading level matches the overview day;
- Morning Work, Shared Reading and Guided Reading are independent;
- no HASS lesson/printable has been invented from the overview;
- previous lessons were assumed complete unless an explicit exception says otherwise.


A package is not complete because files exist. Follow `references/daily-pack-quality-floor.md` and `release-checklist-usage.md`.

1. Initialise the 184-item per-pack checklist before construction:
   `python scripts/quality_checklist.py init --scope daily_release --out <build>/qa/daily-release-checklist.json`
2. Create the build manifest, mathematical-visual specification, semantic-colour mapping, render evidence, geometry report, cross-file checks, note-alignment checks and visual-QA ledger described in `references/output-spec.md`.
3. Render the final file after its most recent edit. Store SHA-256 hashes for the deck and every render.
4. Inspect every slide individually at full size in four separate passes: mathematical accuracy, instructional clarity, visual presentation and cross-file consistency. The contact sheet is supplementary sequence evidence only.
5. Complete a separate structured educational-quality review for Morning Work and every teacher-led lesson, covering source/curriculum alignment, accuracy, age pitch, cognitive load, learning value, differentiation and evidence of learning. Review the whole sequence, not isolated attractive slides.
6. Complete a holistic visual-quality review of the final rendered deck against the benchmark, covering hierarchy, projected readability, spacing, consistency, purposeful visuals, semantic colour, colour-accessibility robustness and layout variety. Any weak, generic, cluttered, sparse, decorative-colour-heavy or unresolved slide fails.
7. Compare every full-size slide with the benchmark and archetypes. Any slide worse in classroom clarity fails.
8. Fill every checklist entry with `pass` evidence or a justified `not_applicable` reason. A human failure always blocks release.
9. Run:
   - `python scripts/quality_checklist.py validate --scope daily_release --checklist <build>/qa/daily-release-checklist.json`
   - `python scripts/validate_math_visuals.py --spec <build>/qa/math-visuals.json` when visuals are present
   - `python scripts/validate_slide_geometry.py --layout-dir <layout-dir> --deck <deck> --out <build>/qa/geometry.json`
   - `python scripts/validate_daily_pack.py --pack-dir <build> --manifest <build>/qa/build-manifest.json`
10. Release only when every gate passes and no inspection is unresolved. On failure, keep the failure report, do not present the package as classroom-ready and state plainly that full QA was not completed.

## Final response

Lead with whether the pack passed release. Then list the schedule, created files, print quantities, preparation, assumptions and the next status question for teacher-led sequences only. If a gate failed, list the failed checks and the repair needed instead of handing over a purportedly finished package.

For regression work, follow `references/regression-test-matrix.md` and validate all 14 regression entries in fresh evaluation contexts. Retain the Thursday non-examples as forbidden outcomes.
