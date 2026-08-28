# Shared-class context and memory-independence contract

## Purpose

This contract lets either teacher generate the same-quality Daily Lesson Pack
for the shared classroom without relying on either account's chat memory.

The repository package plus the sources supplied for the current run are the
complete authority. Chat memory, saved personal context and another account's
Project files are not lesson sources.

## Stable shared-class defaults

- Mixed Year 4/5 classroom using the Western Australian curriculum.
- Morning Work is projected while students record every response in books.
- Morning Work is independent retrieval and application, not new teaching.
- The normal warm-up response routine uses mini-whiteboards; do not add a
  generic whiteboard footer to slides.
- Student-facing materials use Australian English.
- Art, Japanese, Science, Music and Physical Education are specialist-led and
  appear as timetable labels only.
- Guided Reading is timetable-only under the current component contract.
- HASS content requires an authoritative HASS plan or an explicit current
  instruction.
- When a printing plan is requested, the current shared-class default is 29
  student sets: 27 students plus 2 spares. A current explicit quantity
  overrides this default.

Do not include student names, diagnoses, assessment records or other personal
student information in this repository contract.

## Required inputs for each daily run

Resolve these from the current request or files available to the current run:

1. exact date, term, week and day;
2. that teacher's timetable for the requested day, including interruptions;
3. current Mathematics overview/topic and day-level focus;
4. current English overview/toolkit stage and day-level focus;
5. any explicit lesson-status exception from the preceding scheduled day;
6. any current change to class size, output scope or printing quantity.

Assume the preceding scheduled lesson was completed sufficiently to advance
unless an explicit status exception says it was partial, cancelled or requires
reteaching.

## Wednesday co-teacher mode

Wednesday is a valid Daily Lesson Pack day for the teacher who shares this
classroom.

- Use the supplied Wednesday timetable as authoritative.
- Use the supplied Wednesday Mathematics and English focus. If the shared
  overview has no Wednesday row, the teacher's explicit Wednesday focus is the
  required bridge between Tuesday and Thursday.
- Do not duplicate Tuesday or consume Thursday's planned focus unless the
  supplied Wednesday focus explicitly requires it.
- Apply the same class, pedagogy, visual, component and QA standards used on
  other days.
- Include a concise completion/exit-evidence handover for Thursday's teacher.

## Missing-input behaviour

If a required input is unavailable or contradictory:

1. ask one concise question that resolves the highest-impact ambiguity;
2. do not guess from chat memory or an older generated deck;
3. do not release the pack as classroom-ready until the ambiguity is resolved;
4. record the source used for each resolved field in the temporary context
   source record supplied to final QA.

Use `../examples/context-record-wednesday.json` as the field structure for the
temporary record. Replace its example values and source labels with the actual
current-run sources.

## Clean-account acceptance condition

The skill is portable only when a fresh account with no relevant memory can
produce the intended pack using:

- the installed repository release;
- the shared Maths and English overviews;
- the requested day's timetable and focus;
- any explicit lesson-status exception.

If the same inputs produce materially weaker pedagogy, visual design or QA in a
clean account, treat that as a skill defect rather than a missing-memory issue.
