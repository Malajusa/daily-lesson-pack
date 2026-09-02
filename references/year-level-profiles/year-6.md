# Year 6 contextual profile

Status: v0.1 scaffold — requires calibration evidence before classroom-ready Year 6 release

## Purpose

This profile is the dedicated contextual base for Year 6 Daily Lesson Packs. It must develop independently from the calibrated Year 4/5 profile.

The profile does **not** store a particular teacher's timetable, Maths overview, English overview, term sequence, class size or school routines. Those are runtime user/school inputs interpreted through this profile.

## Initial Year 6 principles

Until stronger Year 6 calibration evidence is added:

- retain the universal Daily Lesson Pack architecture, visual standards, component acceptance gates and Mathematics canon;
- use the teacher's supplied current overview/program to determine what is being taught now;
- do not derive Year 6 difficulty by simply increasing numbers, passage length, vocabulary rarity or number of steps from Year 4/5 examples;
- use accurate curriculum terminology with concise plain-language support rather than unnecessary simplification;
- permit greater independence and sustained reasoning only when the current task and supplied Year 6 evidence justify it;
- preserve projected readability rather than using smaller text merely because Year 6 students can read more;
- maintain explicit modelling and model-to-practice alignment for new or fragile concepts;
- keep warm-ups as retrieval rather than using Year 7 content as an automatic extension.

## Calibration evidence to add

Before this profile is treated as a mature classroom-ready baseline, add or verify evidence for:

- expected Year 6 prior knowledge and retrieval floor;
- mathematical number types, magnitudes and representations;
- appropriate independent task complexity and reasoning demand;
- literacy warm-up language and misconception quality;
- reading passage density, syntax and comprehension demand;
- writing-response expectations and scaffolding;
- expected student independence;
- year-specific curriculum boundaries using authoritative Western Australian curriculum sources;
- representative Year 6 teaching materials that demonstrate an appropriate pitch;
- Year 6 canonical examples and regression prompts.

## Runtime adaptation rule

A Year 6 user's timetable and overviews are required to resolve **current content**, not to define **Year 6 pedagogy**.

Examples:

- If an overview states `percentages`, use the overview to identify the current focus, then use this profile and authoritative curriculum context to calibrate the Year 6 demand.
- If another user states `angles`, do the same without requiring the first user's sequence or examples.
- Timetable order changes assembly only; it does not change the Year 6 instructional pitch.

## Isolation rule

Do not alter `year-4-5.md` while calibrating this profile unless separate evidence shows that a Year 4/5 improvement is warranted.

A Year 6-specific correction should normally be made here. If evidence demonstrates that a correction is universal, promote it deliberately to a shared component/core rule and run the Year 4/5 regression suite before release.

## Release status

This scaffold is sufficient to route and isolate Year 6 development, but it is not yet a claim that Year 6 content is fully calibrated.

Until the calibration evidence above is established, label Year 6 generated packs as **candidate/calibration output** rather than classroom-ready unless the generated pack has been specifically reviewed and passed against supplied Year 6 evidence and the full QA suite.
