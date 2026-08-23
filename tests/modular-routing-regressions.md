# Modular Daily Lesson Pack routing regressions

Run these checks before merging a modular architecture change.

## 1. Ordinary daily pack

Prompt a normal teacher-led day containing Literacy and Mathematics.

PASS when:
- the root skill resolves context once;
- required components are delegated to their owners;
- Morning Work is slide 1;
- the Mathematics warm-up and Mathematics lesson remain separate;
- the assembled pack is reviewed by `dlp-pack-qa` before release.

## 2. Shared Reading isolation

Change only the Shared Reading paragraph-length requirement.

PASS when:
- only `dlp-shared-reading` requires behavioural revision;
- Literacy warm-up, numeracy warm-up and Mathematics lesson rules remain unchanged;
- full-pack QA still reruns after assembly.

## 3. Numeracy All / Most / Some regression

Generate a Mathematics warm-up prompt.

PASS when:
- `All`, `Most` and `Some` are three separate questions/tasks of increasing complexity;
- none of the tiers is merely a partial, complete or checked version of the same question;
- the answer slide gives three matched answers;
- `Why` remains reasoning in the green bottom panel.

## 4. Literacy warm-up length

Generate the Literacy warm-up with no explicit count override.

PASS when:
- there are 10 prompt slides and 10 immediately following answer slides;
- spelling/Sound Waves replacement content is absent;
- no generic whiteboard-use footer is added.

## 5. Shared Reading architecture

Generate Shared Reading.

PASS when each substantive slide has:
- one short paragraph;
- one question about that paragraph;
- obvious visual separation;
- projected-size text rather than a long paragraph compressed to fit.

## 6. Existing-pack audit

Request an audit of an existing Daily Lesson Pack artefact.

PASS when the root routes directly to `dlp-pack-qa`, reports defects by owning component and does not regenerate the whole pack without cause.

## 7. Weekly Mathematics request

Request a complete Term/Week Mathematics pack.

PASS when the request is routed to the standalone `weekly-maths-pack` skill/contract rather than being generated from Daily Lesson Pack component rules.

## 8. Specialist-subject boundary

Use a day containing Art, Japanese, Science, Music or Physical Education.

PASS when the block may be named in the timetable but no lesson, slides, printables, answers or contingency content are generated for the specialist subject.

## 9. QA regression after a repair

Introduce a known Shared Reading failure, run QA, repair it, then rerun QA.

PASS when:
- the defect is routed to `dlp-shared-reading` only;
- the entire applicable pack checklist reruns after the repair;
- the pack is not released because the original defect disappeared if a new defect has been introduced elsewhere.

## 10. Routing-unavailable fallback

Run in a host where child skills cannot be invoked directly.

PASS when the root reads the bundled `skills/<skill-name>/SKILL.md` contract and follows it, rather than falling back to generic unscoped generation.
