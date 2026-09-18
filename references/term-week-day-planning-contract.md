# Term -> Week -> Day planning contract

## Purpose

This contract defines how Daily Lesson Pack resolves a daily teaching plan from
maintained curriculum planning without relying on chat memory or re-interpreting
the whole term on every run.

For daily content resolution, use this precedence after the user's current
explicit instruction:

1. an authoritative **lesson-status exception** for the relevant sequence;
2. the selected **weekly teaching overview** (Level B);
3. the selected **term overview** (Level A);
4. the **actual timetable** and current-run interruptions to place the resolved
   learning into Level C day blocks;
5. the active year-level profile and universal component canons for developmental
   pitch, pedagogy and presentation.

The timetable controls what can be taught and when. It does not silently rewrite
the selected weekly sequence. A direct current user instruction can override a
planning source for that run and must be recorded in provenance.

## The three levels

### Level A — term overview

Level A owns curriculum mapping, term-long sequencing, assessment timing and
major constraints. It answers **what must be taught across the term and when**.

Curriculum codes/content descriptions belong here when required. Level B should
not duplicate them unless a weekly exception genuinely depends on one.

### Level B — weekly teaching overview

Level B owns the timetable-agnostic teaching design for one week. It answers
**what students learn this week and in what instructional sequence**.

A Level B file should contain, where applicable:

- weekly purpose;
- English — Writing;
- English — Reading;
- Mathematics;
- HASS;
- Health;
- Digital Technologies;
- ordered lessons with focus, key teaching points, student task/output and
  essential resources;
- assessment/evidence;
- preparation/resources;
- end-of-week checkpoint;
- constraints.

Level B lessons are labelled by sequence, not weekday. Do not convert them to
Monday/Tuesday/etc. inside the weekly source.

### Level C — daily plan

Level C is generated for the requested day by combining the selected Level B
sequence with the actual timetable, interruptions and any lesson-status
exception. It answers **which weekly lessons occur in each real block today and
how they are taught**.

Level C may expand a referenced Level B lesson into learning intention, warm-up,
explicit teaching, worked examples, guided practice, independent work,
differentiation, resources, slides, printables and answers. It must not silently
replace the Level B focus with a different topic.

## Sequence resolution

When a weekly sequence has several lessons:

1. identify the relevant subject/block instances in the actual timetable;
2. map the week's ordered lessons to those instances in sequence;
3. apply any authoritative lesson-status exception before advancing;
4. if no exception exists, assume the preceding scheduled lesson was completed
   sufficiently to advance;
5. do not infer mastery merely because a lesson was planned or generated;
6. do not consume a later Level B lesson early simply to fill a gap.

**Missing status is not evidence** that a lesson was missed.

If the timetable does not provide enough capacity for every planned Level B
lesson, preserve the highest-priority learning and surface the mismatch rather
than silently compressing or dropping content.

## Lesson-status ledger

The portable repository may include an **exception-only** status ledger for a
selected plan. Routine completion does not need to be recorded.

Record an exception only when an authoritative source establishes that a
scheduled lesson was:

- partial;
- cancelled/missed;
- explicitly marked for reteaching;
- moved to another block.

A generated pack is not evidence that teaching occurred.

Status records must not contain student names, diagnoses, individual assessment
records or other private student data.

## Planning-source selection

A repository can contain more than one plan. A plan must be explicitly selected
by the current request, maintained class context or authorised creator default.
Do not apply a creator's dated term plan to another teacher merely because the
file is bundled.

For the selected plan:

- Level B outranks Level A for the week's instructional sequence;
- Level A constrains Level B's term scope and assessment deadlines;
- the actual timetable constrains Level C placement and available time;
- specialist exclusions in Level A remain exclusions unless explicitly changed.

## Provenance and release

The resolved context should record the selected Level A file, Level B file,
timetable source and any status exception in source provenance. When a planning
source is absent, contradictory or does not cover the requested date, fail
closed on the unresolved lesson focus rather than guessing from memory.

The human-facing DOCX may mirror the same plan for reading, printing and
annotation, but the DOCX is not required at runtime when the repository planning
files are present. Repository markdown is the machine-readable source.
