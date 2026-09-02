# Year-profile isolation regression

## Purpose

Prevent calibration work for one year level from silently changing the instructional pitch of another year level.

Run this regression whenever:

- a year-level profile changes;
- a shared component contract changes in a way that can affect task demand, language, scaffolding or assumed prior knowledge;
- the orchestrator's context routing or source precedence changes;
- a year-specific rule is promoted to a universal rule.

## Test A — Same topic, different profiles

Use one common topic that can legitimately occur in both profiles, with equivalent current-run overview wording.

Generate or inspect a candidate component once with `year-4-5` and once with `year-6`.

PASS only if:

- both runs preserve the same universal slide architecture and QA requirements;
- each run follows its own active year profile;
- Year 6 is not produced by mechanically increasing numbers, text length or step count;
- Year 4/5 does not inherit Year 6-only vocabulary, assumptions or demand;
- neither run imports the other profile's explicit calibration statements.

## Test B — Year 6 development must not alter Year 4/5 baseline

After any Year 6-specific change, rerun at least one established Year 4/5 benchmark for each affected component.

Minimum affected-component set:

- Literacy warm-up -> relevant Tuesday/Thursday literacy regression;
- Numeracy warm-up -> Tuesday release regression;
- Shared Reading -> Tuesday release regression;
- Main Mathematics -> universal Mathematics canon regression plus the applicable Year 4/5 benchmark;
- Morning Work -> Monday/Tuesday benchmark as applicable.

PASS only if the Year 4/5 output remains materially equivalent or deliberately improved under an explicitly documented Year 4/5 change.

## Test C — Runtime source separation

Provide two hypothetical Year 6 users with different timetables and overviews.

PASS only if:

- timetable differences change sequencing/assembly, not year-level pedagogy;
- overview differences change the current lesson focus, not the stored Year 6 developmental assumptions;
- neither user's timetable, class size or weekly sequence is written into the Year 6 profile;
- the generated context record distinguishes runtime user/school sources from the year-level profile source.

## Test D — No false portability

Attempt a clean-account run using a supported year profile plus newly supplied user/school context.

FAIL if the system requires hidden chat memory, a previous teacher's timetable, a previous class's overview or an unstated class-size default to reach the intended pitch.

## Release rule

Any profile-isolation failure blocks release of the architectural change. Fix the narrowest responsible scope rather than weakening another year profile.
