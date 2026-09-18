# Term → Week → Day planning regression

## Purpose

Prove that a selected maintained term plan can drive a Daily Lesson Pack without
re-reading a long human-facing document, inventing weekday sequencing or relying
on chat memory.

## Test context

Use the bundled plan `planning/2026/term-4/` and explicitly select plan ID
`2026-t4-year-4-5-room-11`.

Provide:

- a requested date/day within Term 4 2026;
- the actual timetable for that day, including interruptions;
- the active Year 4/5 profile;
- no lesson-status exception unless the test case explicitly supplies one.

Do not provide conversation history or manually restate the weekly lesson focus.

## Pass conditions

- The requested week is resolved to its `weeks/week-XX.md` Level B source.
- The Level B sequence controls current lesson focus before the Level A term
  overview is consulted for broader scope/assessment constraints.
- The actual timetable controls Level C placement and available time without
  rewriting the Level B instructional sequence.
- Missing lesson status is treated as no exception: the preceding scheduled
  lesson is assumed sufficiently complete to advance.
- A supplied partial/cancelled/reteach exception takes precedence over normal
  progression and is recorded in source provenance.
- The generated day plan references the selected weekly lesson/focus and expands
  it through the owning component skill rather than inventing a replacement topic.
- Curriculum codes remain a Level A compliance concern and are not mechanically
  repeated through every Level B lesson.
- The bundled Room 11 plan is not silently applied to a different teacher/class
  merely because it exists in the installation.
- Specialist Science remains excluded from classroom lesson generation under
  this selected plan.
- Weeks 3–4 respect the reduced swimming capacity; Week 6 keeps the Narrative
  assessment fixed; Week 7 remains the assessment-evidence deadline.

## Fail conditions

- Chat memory supplies the lesson focus.
- The term overview overrides a more specific weekly sequence without an
  authoritative current instruction.
- Weekday labels are invented inside Level B.
- The generator repeats a previous lesson because status is absent.
- A generated pack is treated as proof that the lesson was taught.
- A timetable gap causes a later weekly lesson to be consumed early without an
  explicit planning decision.
- The dated creator plan is treated as a universal year-level default.
