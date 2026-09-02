---
name: dlp-numeracy-warmup
description: Generate the Daily Lesson Pack Mathematics warm-up as cumulative retrieval using separate All, Most and Some questions of increasing complexity.
---

# DLP Numeracy Warm-up

## Ownership

Own the Mathematics warm-up only. It is cumulative retrieval and does not replace the main lesson's prerequisite check, modelling, guided practice or exit assessment.

## Mandatory year-level context

Before generation, read `references/year-level-context-contract.md` and the active year-level profile supplied by the orchestrator.

The active profile controls expected prior knowledge, number types and magnitudes, appropriate retrieval floor, reasoning demand and the ceiling for `Some`. Do not use another year level's calibration merely because its examples are available.

## Sequence

Create exactly **10 prompt-and-answer pairs** (20 slides) unless the user explicitly changes the count, in this order:
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. State it
6. Recognise it
7. Complete it
8. Apply it
9. Distinguish it
10. Cumulative retrieval

Every prompt is followed immediately by its matched answer slide.

## All / Most / Some principle

On **prompt slides**, `All`, `Most` and `Some` must be **three separate questions/tasks of increasing complexity**. Never use one question where `All` is a partial answer, `Most` is the complete answer and `Some` is checking/explaining the same work.

- **All:** a genuinely accessible question essentially all students can attempt successfully within the active year profile.
- **Most:** a moderately more demanding independent question representing secure expected performance for the active profile.
- **Some:** a further extension that remains appropriate to the active profile; it should not leap automatically into the next year level.

On **answer slides**, show the answer corresponding to each of the three questions.

`Most` represents success, not a consolation tier.

## Layout

- Use the same three-column All / Most / Some body layout on question and answer slides.
- Keep `Why` in the established green panel at the bottom: a reasoning prompt on the question slide and concise reasoning/explanation on the answer slide.
- Do not turn `Why` into a fourth body card.
- Do not use a generic `Check your answer` message in place of mathematical reasoning.
- No generic whiteboard-use footer is required.

## Content calibration

Apply the active year-level profile rather than hard-coding one class or year band.

- Questions 1-4 should sit near the accessible retrieval floor defined by the active profile while remaining worthwhile.
- Questions 5-10 should mainly retrieve the active profile's expected current/prior knowledge and earlier prerequisite knowledge.
- Do not force the warm-up to preview the day's lesson or next-year content merely to manufacture challenge.
- Difficulty should come from mathematically meaningful variation, not arbitrary larger numbers or extra steps.

For `year-4-5`, apply the specific calibration in `references/year-level-profiles/year-4-5.md`.
For `year-6`, apply `references/year-level-profiles/year-6.md` and treat the profile's current release status honestly.

Use proper fraction formatting with a vinculum/stacked fraction on student-facing slides.

## Presentation

Use Trebuchet MS and the shared projected-readability hierarchy. Main instructional content is normally at least 36 pt; use larger type when space allows. Keep colour restrained and semantic. Do not use red/amber/green traffic-light coding for tiers. The green `Why` panel is reserved for reasoning.

## QA

Fail if:
- the active year-level profile is missing, unresolved or inconsistent with the orchestrator;
- content relies on another year profile's pitch without explicit authorisation;
- any prompt uses one question split into quality tiers rather than three questions;
- `Some` is an unreasonable leap;
- answer slides do not match the three prompts;
- the green `Why` panel contains generic checking instructions instead of reasoning;
- text overflows a tier or `Why` panel;
- fractions use a forward slash where stacked notation is practical.
