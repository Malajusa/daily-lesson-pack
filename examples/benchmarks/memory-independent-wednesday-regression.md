# Memory-independent Wednesday regression

## Purpose

Prove that the shared-class Wednesday teacher can generate the intended Daily
Lesson Pack in a fresh account with no relevant chat memory.

## Test context

Provide only:

- the installed tagged repository release;
- the shared Maths and English overviews;
- an explicit Wednesday date, timetable and day-level Maths/English focus;
- either an explicit Tuesday status exception or no exception.

Do not provide conversation history, saved personal context, an earlier pack or
another teacher's Project files.

## Pass conditions

- Wednesday is treated as a valid shared-class teaching day.
- The supplied Wednesday timetable and focus are used without inventing a row
  in the four-day overview.
- In the absence of a Tuesday exception, Tuesday is assumed sufficiently
  completed to advance.
- No Tuesday content is duplicated and no Thursday focus is consumed unless the
  Wednesday focus explicitly requires it.
- The stable shared-class routines come from
  `references/shared-class-context-contract.md`, not memory.
- The full component, Mathematics, visual and release QA suite runs.
- The teaching deck matches the checksum-verified visual-only exemplar while
  rejecting its superseded lesson content.
- The briefing includes a concise completion/exit-evidence handover for
  Thursday.

## Fail conditions

- The generator cites or depends on remembered preferences not present in the
  installed package or current inputs.
- Missing essential information is guessed rather than queried.
- Wednesday is rejected merely because it is outside the four-day overview.
- A conditional or improvised pack is labelled classroom-ready.
- The output loses either the later educational canon or the approved visual
  standard.
