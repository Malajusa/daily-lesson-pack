# T3W8 Tuesday mass/narrative known-failure QA regression

## Classification

**Known-failure QA fixture. Expected release decision: FAIL.**

**DO NOT USE AS A CONTENT EXEMPLAR. DO NOT USE AS A VISUAL EXEMPLAR.**

This case exists to calibrate `dlp-pack-qa` against a polished-looking Daily Lesson Pack that contains genuine strengths alongside release-blocking runtime, instructional and assessment defects. It is a regression oracle, not a model to imitate.

## Immutable source artefacts

- Candidate deck: `assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx`
- Candidate deck SHA-256: `f9321b698a7b6c497ea4908e24aa7a90abe57cf83a8171f844395aefecc30ccd`
- Full human critical review: `review.md`
- Full review SHA-256: `0b82054ac8572b83e204ccb8882025679a53b79a0f364488cee264b06f9a0965`
- Machine-readable oracle: `expected-findings.json`
- Blind reviewer context: `blind-request-context.md`

Do not edit the deck or the preserved review in place. If either source artefact must change, create a new case with a new identifier and hashes so historical regression evidence remains reproducible.

## Purpose

This fixture tests whether QA can identify defects that are easy to miss when a deck is visually competent and broadly on-topic. The reviewer must distinguish actual release blockers from acceptable or successful parts of the pack.

The complete human review remains authoritative for this fixture. The distilled checks below are its regression contract, not a replacement for the preserved review.

## Required findings

A successful QA reviewer must return `FAIL` and identify all release-significant findings below.

### 1. Wrong requested day

The request was for Tuesday 8 September 2026, while the deck presents Monday 7 September 2026. Renaming the file alone would not fix the underlying runtime error.

### 2. Unresolved timetable/runtime context

The deck itself records that timetable allocation and class-band context were not verified and proceeds as an untimed teaching sequence. Missing essential runtime context must block a finished/classroom-ready release.

### 3. Independent Mathematics repeats worked values

The Year 4 independent conversion task on slide 34 reuses both values already demonstrated in the teaching sequence:

- `1 kg 600 g`, previously shown as `1,600 g` on slide 27;
- `2 kg 80 g`, previously worked through on slides 19–20.

Independent practice should provide fresh evidence of transfer, not rely entirely on recalled worked examples.

### 4. Independent Mathematics evidence is too thin

Relative to a 28-slide, 45–55 minute main Mathematics sequence, each pathway has only a small amount of explicitly independent practice before the exit check. QA should distinguish this from the valid guided responses elsewhere in the lesson: the defect is insufficient independent evidence, not an absence of student participation.

### 5. Essential Mathematics instructions have the wrong hierarchy

On slides 36 and 38, the directions that define the task and required evidence are visually subordinate, 26 pt and internally treated as supporting explanation. They are primary student instructions and should receive task-level hierarchy.

### 6. One writing prompt does not clearly obstruct the goal

On slide 90, `Return a library book / Its final page begins writing a message to you` introduces an unusual event but does not necessarily create the lesson's defined complication: a problem that gets in the way of the character's goal.

### 7. Joint-writing scenario has a plausibility distraction

Slides 88–89 describe a gust tearing a parcel from Kai's grip and sliding it under a locked office door. This is a smaller quality defect, but QA should notice that the physical setup can distract from the intended writing feature.

### 8. Writing exit evidence is misaligned

Slide 94 checks whether students can show a character reaction through action. That is useful but secondary to the lesson's central goal–complication relationship. Exit evidence should directly test whether the complication obstructs the character's goal.

### 9. Delivery overstated completion

The artefact was presented as `today's PowerPoint` even though its date was wrong and essential runtime context remained unresolved. The original delivery did disclose that independent QA was pending, so QA must not falsely claim that an independent PASS was fabricated.

## Advisory observations retained from the full review

These are useful quality observations but are not scored as equivalent to the required findings above:

- the selected Mathematics focus is specifically kilogram–gram conversion/comparison rather than the whole topic of mass; that focus could be valid if current sequencing authorised it;
- the shared narrative leaves the grandfather's initials undeveloped and never shows Mara's crucial new ending;
- exact native PowerPoint wrapping remained unverified because the local renderer substituted fonts for Trebuchet MS.

## False-positive guards

QA must not manufacture defects merely to ensure a FAIL. In particular:

- five Numeracy prompt/answer pairs are correct under the current repository contract; do not demand ten because an older exemplar used ten;
- do not describe the whole presentation as visually broken or claim widespread clipping when the observed hierarchy problem is specific;
- the Literacy warm-up is generally successful and structurally follows the required reminder–question–answer architecture;
- the Shared Reading is generally successful and uses six matched paragraph/question/answer pairs with correct alternation.

Individual defects remain valid if supported by evidence; these guards prevent broad claims contradicted by the preserved review.

## Blind regression protocol

The live regression must run `dlp-pack-qa` **blind** against the exact deck hash above.

The reviewer receives only:

1. a temporary repository workspace containing the current `dlp-pack-qa` skill and normal repository standards;
2. the exact candidate deck copied to `input/deck.pptx`;
3. `blind-request-context.md` copied to `input/request-context.md`;
4. neutral output-format instructions.

The temporary workspace must exclude this case directory, the original QA-regression asset path, the preserved review, the machine oracle and the regression test that names the expected findings. The oracle is loaded only by the parent scorer after the reviewer has completed its review.

A configured live runner writes structured JSON findings. `scripts/run_blind_qa_regression.py` then compares those findings with `expected-findings.json` and fails if a required finding is missed, the verdict is not `FAIL`, or a known false positive is asserted.

## Runner protocol

Set `DLP_PACK_QA_RUNNER` to a command that launches an independent reviewer process. The harness supplies these environment variables to that process:

- `DLP_QA_WORKSPACE`
- `DLP_QA_DECK`
- `DLP_QA_SKILL`
- `DLP_QA_REQUEST_CONTEXT`
- `DLP_QA_REVIEW_INSTRUCTIONS`
- `DLP_QA_OUTPUT`

The runner must execute the review independently, use `skills/dlp-pack-qa/SKILL.md` as its QA contract, and write the requested JSON document to `DLP_QA_OUTPUT`.

An ordinary unit-test run verifies fixture integrity, blindness construction and oracle scoring without pretending that a model review occurred. The live integration test is enabled only when an independent runner is explicitly configured.

## When this regression is mandatory

Run this case whenever a change affects any of the following:

- `dlp-pack-qa` semantic review;
- runtime/date/timetable fidelity;
- Mathematics independent-practice quality or model-to-practice transfer;
- projected instruction hierarchy or role tagging;
- narrative goal/complication alignment;
- writing exit evidence;
- release/candidate wording or QA calibration.

The test is designed to protect judgement quality as well as defect recall: detecting every expected defect while inventing broad false positives is still a failed regression.
