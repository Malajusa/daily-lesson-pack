---
name: daily-lesson-pack
description: Orchestrate timetable-aligned Daily Lesson Packs by resolving the day context, routing each teaching component to a specialised Daily Lesson Pack skill, assembling the outputs, and requiring independent QA before release.
---

# Daily Lesson Pack — Orchestrator

## Purpose

Coordinate a classroom-ready daily pack. Do not generate detailed subject content in this skill when a specialised component skill owns it.

The orchestrator owns:
- date, term, week and timetable resolution;
- source hierarchy and progression decisions;
- specialist-subject exclusions;
- component routing;
- cross-component consistency;
- final assembly, briefing and print plan;
- release only after `dlp-pack-qa` passes.

The specialised skills own the pedagogy, wording and slide rules for their component.

## Request routing

### Daily pack

Use this orchestrator for a named day's Daily Lesson Pack. Resolve the context, invoke the required components, assemble them, then run independent QA.

### Existing-pack audit or revision

Route the supplied Daily Lesson Pack directly through `dlp-pack-qa`. If it fails, send each defect only to the owning component skill, revise that component, rebuild the affected artefact, and re-run the complete applicable QA suite.

### Weekly Mathematics pack

A complete Term/Week Mathematics pack belongs to the standalone `weekly-maths-pack` skill. Route the request there rather than rebuilding weekly Mathematics logic inside this Daily Lesson Pack orchestrator. If direct skill routing is unavailable, use the standalone Weekly Maths Pack contract supplied in the environment; do not duplicate its full rules here.

## Source hierarchy

Use sources in this order:
1. the user's current instruction;
2. explicit maintained lesson-status exceptions;
3. connected calendar and authoritative timetable;
4. active unit/assessment plans;
5. current term/year overviews and curriculum maps;
6. standing teaching preferences and component-skill defaults.

Assume the previous scheduled lesson was covered sufficiently to advance unless an authoritative source explicitly records partial completion, cancellation or reteaching. Missing status is not evidence that a lesson was missed.

For the established Term 3 four-day overview, Monday, Tuesday, Thursday and Friday use the current overview's day-level Mathematics focus, Information Report toolkit stage and Shared Reading country as mandatory inputs when that overview is available. Resolve the Guided Reading timetable block and, where recorded, its authorised group name separately. Wednesday remains outside that four-day overview unless explicitly requested, while still remaining a valid timetable day.

Do not browse the public web to infer school dates or timetable events unless the user asks for verification.

## Mandatory visual exemplar

For every teaching deck, read `references/visual-exemplar-standard.md` and use
`assets/visual-exemplars/t3w6-tuesday-edited-visual-exemplar.pptx` as the
approved **visual-only** design source. Verify its SHA-256 before use. Preserve
its role-colour grammar, full-height left rail, compact eyebrow/title hierarchy,
primary/secondary panel structure, Trebuchet MS typography and efficient use of
the 16:9 canvas.

Do not inherit the exemplar's lesson wording, sequencing errors or superseded
pedagogy. The current orchestrator and component contracts remain authoritative
for content. If the exemplar conflicts with a current content rule, retain the
visual grammar and rebuild the content correctly.

## Scope boundary

Art, Japanese, Science, Music and Physical Education are specialist-led. Name their timetable block only. Do not generate lessons, slides, printables, answers, contingencies, preparation tasks or status capture for them.

`Student guided learning` is teacher-supervised but has no standing Daily Lesson Pack sequence. Name the block unless an authoritative current plan identifies the activity.

HASS requires a separate authoritative HASS plan or an explicit current user instruction. Do not invent HASS from country-reading contexts.

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

## Orchestration workflow

1. Resolve exact date, term, week, day, timetable and interruptions.
2. Resolve active sequence and explicit status exceptions.
3. For an overview-controlled Term 3 day, resolve the current overview fields before component generation.
4. Verify and load the approved visual-only exemplar, then build one shared context object containing only information the components need: lesson focus, curriculum boundary, authorised group/day allocation, current writing-toolkit stage, approved country contexts, time available and output constraints.
5. Route each required component to its specialised skill and require a component acceptance result before assembly.
6. Record the scheduled components and each component's `PASS` or `FAIL`, checks completed and artefact/slide range in a temporary component-acceptance record. Treat a missing record, missing scheduled component or unsubstantiated `PASS` as `FAIL`.
7. Block assembly until every scheduled content component records `PASS`. This gate does not replace independent final QA.
8. Keep Morning Work, Literacy warm-up and Shared Reading as genuinely distinct tasks and texts. Represent Guided Reading only in the timetable while its timetable-only setting remains active.
9. Keep the Mathematics warm-up separate from prerequisite checking and the main Mathematics lesson.
10. Assemble components in timetable order. Slide 1 is always Morning Work when Morning Work is required.
11. Create only useful printables. Prefer books, mini-whiteboards, oral work and manipulatives when a worksheet adds no value.
12. Create the teacher briefing and Monday weekly printing plan from the actual generated resources, not from assumptions.
13. Run the visual-exemplar audit, then send the complete assembled pack, visual audit and component-acceptance record to `dlp-pack-qa`.
14. If QA returns FAIL, route each defect back only to the owning component skill, revise, and re-run the full applicable QA suite. Do not patch unrelated components.
15. Release only after critical QA checks pass.

If actual printing is requested and copy quantity cannot be resolved from an authoritative source, treat quantity as unresolved rather than inventing it.

## Cross-component invariants

- Morning Work and Shared Reading must not reuse the same passage.
- Literacy warm-up uses 10 self-contained `Reminder -> Question -> Answer` sequences unless the user changes the count. A question must not depend on remembered content from another slide.
- Guided Reading is timetable-only for now: do not generate Guided Reading texts, prompts, teacher guides, transition tasks or instructional slides.
- A Guided Reading timetable label may use only `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon`, and only when that label comes from an authoritative current schedule. Never infer a group or display ability labels such as `very low`, `low`, `at level` or `above level`.
- Shared Reading must alternate each paragraph-and-question slide with its immediately following matched answer slide; answers are not revealed early on question slides.
- The writing lesson teaches the writing toolkit; country facts may provide context but cannot replace writing instruction.
- Student-facing instructions must state the action, mathematical/literacy focus, any required representation or resource, and the expected student output where applicable.
- When a task transforms supplied language, name the exact operation. For example, say `Combine the two sentences using the conjunction “because”`, not merely `Write a sentence`.
- Student-facing task language must use words students can act on immediately. Replace or explain teacher terminology such as `classification opening`; prefer concrete wording such as `topic sentence that tells the reader what the report is about`.
- Use accurate curriculum terminology and explain it in student-friendly language; do not replace a known grammatical term such as `conjunction` with a vague substitute such as `linking word`.
- Teacher preparation, timing, misconceptions and answers belong in the briefing or notes, not as clutter on student task slides.
- Warm-up slides use the established projected-readability and semantic-colour standards.
- No generic whiteboard footer is required on warm-up slides. The Mathematics green `Why` panel is instructional content, not a generic footer instruction.

## Assembly outputs

Daily mode normally produces:
- one coherent teaching deck;
- only necessary student printables;
- separate teacher answers where useful;
- a concise daily briefing;
- a Monday weekly printing plan when applicable.

For a relief day, keep the timetable but make teacher-led sequences self-contained: explicit materials, scripts, answers, stopping points and independent alternatives. Keep teacher-facing preparation out of Morning Work.

## Release rule

The orchestrator never self-certifies quality. `dlp-pack-qa` is the release authority.

Run the deterministic contract audit during final QA:

`python scripts/audit_pack_contract.py --deck <deck> --component-record <record.json> --out <report.json>`

If the user explicitly changes the default Literacy warm-up count, also pass `--literacy-count <n>` with the authorised count.

Run the mandatory visual-exemplar audit:

`python scripts/audit_visual_exemplar.py --deck <deck> --out <report.json>`

Any audit failure blocks release.
