# User/school runtime context and memory-independence contract

## Purpose

This contract defines the **runtime context** a teacher supplies so the Daily Lesson Pack can adapt to that teacher's timetable, current overviews and school sequence without relying on hidden chat memory.

It is deliberately separate from `year-level-context-contract.md`.

- Runtime context answers: **What is this class teaching now, when, and under what local constraints?**
- The active year-level profile answers: **What is an appropriate developmental and curriculum-facing pitch for this year level?**
- The pack profile answers: **What stable slide counts and release behaviours apply across supported profiles?**

Load `default-pack-profile.json` as the bundled architecture profile. A current
user instruction may override a profile field for that run, but the resolved
value and source must be written to the context record.

A teacher's timetable or overview must never become the definition of a year-level profile.

## Runtime context fields

Resolve these from the current request, current-run files, connected authoritative sources or an explicitly selected reusable user/school context file:

1. active year level or explicitly authored combined year band;
2. exact date, term, week and day;
3. that teacher's timetable for the requested day, including interruptions;
4. current Mathematics overview/topic and day-level focus;
5. current English/literacy overview/toolkit stage and day-level focus where applicable;
6. any explicit lesson-status exception from the preceding scheduled lesson;
7. current class size or printing quantity when printing is requested;
8. any local scope changes, specialist blocks or school-specific routines that materially affect the pack.

Do not require the same timetable, overview format, term sequence or class size from different users.

## No bundled class defaults as year-level assumptions

Represent each teaching block using `component-instance-contract.md`. Repeated
subject owners are not merged. Every instance has a unique ID, start time,
duration and purpose before component generation begins.

Assume the preceding scheduled lesson was completed sufficiently to advance
unless an explicit status exception says it was partial, cancelled or requires
reteaching.

Do not treat any of the following as universal or year-level defaults:

- mixed Year 4/5 enrolment;
- a fixed class size or `29 copies` rule;
- one school's timetable;
- a four-day Monday/Tuesday/Thursday/Friday overview;
- a fixed Information Report unit;
- a particular Shared Reading country sequence;
- one teacher's Wednesday arrangement;
- a school-specific assembly or specialist schedule.

These may be used only when they are supplied or explicitly selected as current runtime context for that user/class.

## Source hierarchy for runtime facts

Use runtime facts in this order:

1. the user's current explicit instruction;
2. current-run timetable/overview/unit files;
3. explicitly selected maintained user/school context;
4. connected calendar or authoritative school source;
5. older local planning only when it is clearly still current.

Chat memory, saved personal context and another account's Project context may help identify what to look for, but must not silently supply timetable facts, lesson focus, class size, copy quantity or local routines.

## Progression rule

Assume the preceding scheduled lesson was completed sufficiently to advance unless an authoritative runtime source records partial completion, cancellation or required reteaching.

If an overview defines a day-level sequence, follow that sequence. If it does not define a requested day, use the teacher's supplied current focus rather than inventing a bridge from another day.

## Missing-input behaviour

If a required runtime field is unavailable or contradictory:

1. resolve it from another authoritative current-run source where possible;
2. otherwise ask one concise question that resolves the highest-impact ambiguity;
3. do not guess from chat memory or an older generated deck;
4. do not release the pack as classroom-ready until the ambiguity is resolved;
5. record the source used for each resolved field in the temporary context-source record supplied to final QA.

When printing is requested and quantity is not supplied or otherwise authoritative, treat it as unresolved rather than inheriting another user's class size.

## Clean-account acceptance condition

The skill is portable only when a fresh account with no relevant memory can produce the intended pack using:

- the installed repository release;
- an active year-level profile;
- that user's current timetable;
- that user's Maths and English/literacy overviews or explicit day-level focus;
- any required lesson-status exception;
- any local class/output constraints needed for the requested artefacts.

If the same supplied inputs produce materially weaker pedagogy, visual design or QA in a clean account, treat that as a skill defect rather than a missing-memory issue.

## Privacy boundary

Do not store student names, diagnoses, assessment records or other personal student information in the portable runtime-context contract or year-level profiles.
