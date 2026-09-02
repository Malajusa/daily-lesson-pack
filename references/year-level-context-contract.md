# Year-level contextual base contract

## Purpose

The Daily Lesson Pack must separate **what is true of a year level** from **what is true of one teacher, class, timetable or school program**.

The year-level contextual base provides the stable developmental and curriculum-facing assumptions used to interpret a teacher's current timetable, overview and lesson focus. It must not contain a particular teacher's timetable, class size, term sequence, school routines, student names, local intervention programs or current lesson status.

The user's current timetable, Maths/English overviews, current unit sequence and explicit lesson-status information remain runtime inputs under `shared-class-context-contract.md`.

## Required year-level selection

Every Daily Lesson Pack run must resolve an active year-level profile before content generation.

Supported profile states are:

- a single year profile, such as `year-6`;
- an explicitly authored combined profile, such as `year-4-5`;
- `unresolved`, which blocks classroom-ready release.

Do not approximate an unsupported year by silently reusing another profile. Do not infer Year 6 pitch by merely making Year 4/5 numbers larger, passages longer or vocabulary harder.

## What belongs in a year-level profile

A year-level profile may define:

- expected prior knowledge and reasonable retrieval floor;
- expected student independence;
- reading load and syntactic complexity;
- vocabulary and technical-language expectations;
- mathematical number types, magnitudes and representational expectations;
- appropriate scaffolding and fading of support;
- expected response length and reasoning demand;
- warm-up retrieval pitch;
- typical misconceptions worth testing;
- developmental limits on task complexity;
- year-specific curriculum boundaries when supported by authoritative curriculum evidence;
- canonical examples and year-specific regression checks.

## What must not belong in a year-level profile

Do not store:

- a teacher's timetable;
- a school-specific term/week sequence;
- one class's Maths or English overview;
- class size or printing quantity;
- a particular writing unit tied to named weekdays;
- local assembly/specialist schedules;
- student names, diagnoses or assessment records;
- current lesson completion status;
- country/topic choices that come from one class's current unit.

These belong to the current-run user/school context.

## Source precedence

When resolving content pitch, use:

1. the user's explicit current instruction;
2. the user's current timetable/overview/unit sources for **what is being taught now**;
3. the active year-level profile for **how that content should be pitched and what prior knowledge may reasonably be retrieved**;
4. the universal component and QA contracts.

A current overview may narrow or sequence content, but it must not silently redefine the developmental expectations of the active year profile. Conversely, a year profile must not invent the current lesson focus when the supplied overview is more specific.

## Scope isolation rule

Apply a rule at the narrowest justified scope.

- Universal rendering/QA improvements belong in core references or component contracts.
- A Year 6 pitch correction belongs in `year-6.md` unless evidence shows it is universal.
- A Year 4/5 calibration correction belongs in `year-4-5.md` unless evidence shows it is universal.
- A teacher's local preference belongs in runtime user/school context unless deliberately promoted after broader validation.

Do not change one year-level profile merely to make another year-level profile work.

## Version-controlled calibration

Year-level profiles are protected baselines, not immutable files.

They may be deliberately improved when evidence supports a change. Any change to a year-level profile must:

1. state which profile is being changed;
2. leave other profiles unchanged unless there is separate evidence for them;
3. run the affected profile's regression checks;
4. run `examples/benchmarks/year-profile-isolation-regression.md` when core/component code or shared rules change;
5. fail release if the change causes a previously passing Year 4/5 benchmark to drift in pitch, task architecture or language without explicit authorisation.

## Component handoff

The orchestrator must pass each component:

- `active_year_profile`;
- the resolved year-level profile path/version;
- current lesson focus from user/school sources;
- curriculum boundary where available;
- any explicit user override.

Each content component must read the active profile before generation and treat year-specific wording in its own contract as subordinate to the active profile unless the wording is explicitly universal.

## QA acceptance

Final QA must fail if:

- the active year profile is unresolved;
- a component uses a different year profile from the orchestrator;
- a teacher's timetable or overview has been copied into a year-level profile;
- Year 6 generation relies on Year 4/5-specific calibration rules;
- a profile-specific change alters another year profile without explicit evidence and regression coverage.
