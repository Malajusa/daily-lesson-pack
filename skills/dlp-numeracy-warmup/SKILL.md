---
name: dlp-numeracy-warmup
description: Use when generating or reviewing the Daily Lesson Pack Mathematics warm-up for a supported year-level profile.
---

# DLP Numeracy Warm-up

## Mandatory evidence workflow (v3)

Read `references/qa-workflow-v3.md` and the applicable entries in
`references/qa-requirements.json` before generation or review. This workflow
governs release evidence and supersedes older run-ID-only independence checks
and report-only release commands below. Use `scripts/content_source.py` for
canonical task text and complete review coverage. Required checks cannot be
replaced by a broad component PASS. Only the complete-pack release command may
authorise classroom-ready output.

## Warm-up release boundaries

Read `references/release-boundaries.json` before generating or reviewing this
component. Its `NW.*` checks are **release-blocking invariants in addition to**
the shared QA requirements.

For every warm-up pair, record explicit PASS evidence for:

- `NW.PROMPT.THREE_TIERS_ONLY`
- `NW.PAIR.ADJACENT`
- `NW.ANSWER.MIRROR`
- `NW.REASONING.ANSWER_ONLY`

A missing result or any FAIL makes `dlp-numeracy-warmup` fail. Do not assemble,
label or release the pack as classroom-ready when this component has failed.
When repository benchmarks are available, use
`examples/benchmarks/numeracy-warmup-release-boundaries-regression.md` as the
regression case.

## Resolved instructional preferences

Read `references/creator-settings-contract.md` and use the orchestrator's frozen
`instructional_calibration` when present. Do not independently reload or save
private settings, change the requested warm-up count, or infer student attainment
from enrolment year. Legacy inputs use the documented public defaults, not hidden
chat memory. Existing final-artifact and independent-review gates still apply.

## Ownership

Own the Mathematics warm-up only. It is cumulative retrieval and does not replace the main lesson's prerequisite check, modelling, guided practice or exit assessment.

## Mandatory year-level context

Before generation, read `references/year-level-context-contract.md` and the active year-level profile supplied by the orchestrator.

The active profile controls expected prior knowledge, number types and magnitudes, appropriate retrieval floor, reasoning demand and the ceiling for `Some`. Do not use another year level's calibration merely because its examples are available.

## Sequence

Create exactly **5 question-and-answer pairs** (**10 slides total**) unless the current request or validated classroom profile explicitly changes the count.

Every question slide must be followed **immediately** by its matched answer slide. No reminder, model, transition, unrelated answer or other slide may sit between the pair.

Use this default daily mix:

1. Addition
2. Subtraction
3. Multiplication
4. Division
5. one rotating retrieval focus selected from `State it`, `Recognise it`,
   `Complete it`, `Apply it`, `Distinguish it` or cumulative retrieval.

Rotate the fifth focus across the week rather than expanding the daily deck to
include every category.

## All / Most / Some principle

On **question slides**, `All`, `Most` and `Some` must be **three separate questions/tasks of increasing complexity**. Never use one question where `All` is a partial answer, `Most` is the complete answer and `Some` is checking/explaining the same work.

- **All:** a genuinely accessible question essentially all students can attempt successfully within the active year profile.
- **Most:** a moderately more demanding independent question representing secure expected performance for the active profile.
- **Some:** a further extension that remains appropriate to the active profile; it should not leap automatically into the next year level.

A question slide contains **only those three student tasks**. It must not contain a `Why` box, reasoning prompt, explanation prompt or fourth student task.

On **answer slides**, preserve the same All / Most / Some order and positions and show the matched answer corresponding to each question.

`Most` represents success, not a consolation tier.

## Layout

### Question slide

- Use the established three-column All / Most / Some body layout.
- Show exactly one task in each tier.
- Do **not** place the green `Why` panel on the question slide.
- Do **not** place a reasoning or explanation demand elsewhere on the question slide as a workaround.

### Answer slide

- Mirror the preceding question slide's three-column All / Most / Some layout and tier positions.
- Supply the matched answer for all three tasks.
- Place the established green `Why` panel at the bottom **on the answer slide only**.
- The `Why` panel gives concise mathematical reasoning/explanation; it is not a fourth tier and must not contain generic checking language such as `Check your answer`.

No generic whiteboard-use footer is required.

## Content calibration

Apply the active year-level profile rather than hard-coding one class or year band.

- Questions 1-4 should sit near the accessible retrieval floor defined by the active profile while remaining worthwhile.
- Question 5 should retrieve the active profile's expected current/prior knowledge or earlier prerequisite knowledge.
- Do not force the warm-up to preview the day's lesson or next-year content merely to manufacture challenge.
- Difficulty should come from mathematically meaningful variation, not arbitrary larger numbers or extra steps.

For `year-4-5`, apply the specific calibration in `references/year-level-profiles/year-4-5.md`.
For `year-6`, apply `references/year-level-profiles/year-6.md` and treat the profile's current release status honestly.

Use proper fraction formatting with a vinculum/stacked fraction on student-facing slides.

## Presentation

Use Trebuchet MS and the shared projected-readability hierarchy. Every meaningful
student-facing prompt and answer in the three tier cards is at least **36 pt**.
The substantive answer-slide `Why` explanation is at least **28 pt**. Structural
labels may use the shared structural floor. A 36 pt heading does not compensate
for a smaller task. Keep colour restrained and semantic. Do not use red/amber/green
traffic-light coding for tiers. The green `Why` panel is reserved for answer-slide
reasoning.

## QA

Fail if:
- the active year-level profile is missing, unresolved or inconsistent with the orchestrator;
- content relies on another year profile's pitch without explicit authorisation;
- any question slide does not contain exactly three separate All / Most / Some tasks;
- any question slide contains a `Why` box, reasoning prompt, explanation prompt or fourth student task;
- any question slide is not followed immediately by its matched answer slide;
- any answer slide changes the All / Most / Some order or positions so the pair no longer mirrors cleanly;
- any answer slide omits or mismatches one of the three tier answers;
- any answer slide lacks the established bottom green `Why` reasoning/explanation panel;
- the answer-slide `Why` panel contains generic checking instructions instead of mathematical reasoning;
- `Some` is an unreasonable leap;
- there are not exactly five question/answer pairs under the default profile;
- text overflows a tier or answer-slide `Why` panel;
- fractions use a forward slash where stacked notation is practical.

The four `NW.*` release-boundary checks must all PASS for every pair before the
component can PASS.
