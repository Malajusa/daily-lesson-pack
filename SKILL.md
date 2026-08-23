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

## Source hierarchy

Use sources in this order:
1. the user's current instruction;
2. explicit maintained lesson-status exceptions;
3. connected calendar and authoritative timetable;
4. active unit/assessment plans;
5. term/year overviews and curriculum maps;
6. standing teaching preferences and component-skill defaults.

Assume the previous scheduled lesson was covered sufficiently to advance unless an authoritative source explicitly records partial completion, cancellation or reteaching. Missing status is not evidence that a lesson was missed.

Do not browse the public web to infer school dates or timetable events unless the user asks for verification.

## Scope boundary

Art, Japanese, Science, Music and Physical Education are specialist-led. Name their timetable block only. Do not generate lessons, slides, printables, answers, contingencies, preparation tasks or status capture for them.

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
3. Build one shared context object containing only information the components need: lesson focus, curriculum boundary, group/day allocation, current writing-toolkit stage, approved country contexts, time available and output constraints.
4. Route each required component to its specialised skill.
5. Keep Morning Work, Literacy warm-up, Shared Reading and Guided Reading as genuinely distinct tasks and texts.
6. Keep the Mathematics warm-up separate from prerequisite checking and the main Mathematics lesson.
7. Assemble components in timetable order. Slide 1 is always Morning Work when Morning Work is required.
8. Create only useful printables. Prefer books, mini-whiteboards, oral work and manipulatives when a worksheet adds no value.
9. Create the teacher briefing and Monday weekly printing plan from the actual generated resources, not from assumptions.
10. Send the complete assembled pack to `dlp-pack-qa`.
11. If QA returns FAIL, route each defect back only to the owning component skill, revise, and re-run QA. Do not patch unrelated components.
12. Release only after critical QA checks pass.

## Cross-component invariants

- Morning Work, Shared Reading and Guided Reading must not reuse the same passage.
- Shared Reading and Guided Reading must use different country texts on overview-controlled days.
- The writing lesson teaches the writing toolkit; country facts may provide context but cannot replace writing instruction.
- Student-facing instructions must state the action, mathematical/literacy focus, any required representation or resource, and the expected student output where applicable.
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
