---
name: dlp-numeracy-warmup
description: Use when a teacher asks for a short Mathematics or numeracy warm-up, retrieval deck, All/Most/Some warm-up, or graph-reading warm-up for a supplied year level or planning context.
---

# DLP Numeracy Warm-up

## Output contract

Default output is exactly **5 adjacent question/answer pairs = 10 slides**:

`QUESTION 1 → ANSWER 1 → QUESTION 2 → ANSWER 2 → QUESTION 3 → ANSWER 3 → QUESTION 4 → ANSWER 4 → QUESTION 5 → ANSWER 5`

Every question slide has literal labels `ALL`, `MOST`, `SOME`, with one separate task under each. There is **no WHY content** on a question slide.

Every answer slide immediately follows its question, keeps `ALL`, `MOST`, `SOME` in the same order and positions, answers all three tasks, and adds one bottom green `WHY` panel containing concise mathematical reasoning.

A request such as “graphs toward the end” changes the **content of the final pairs**, not the number or ordering of slides. Unless the user specifies otherwise, Pairs 4 and 5 use graph reading.

## Mode selection

### Standalone mode — default for direct invocation

Use the year level, mixed-year band, topic and planning supplied by the user. User planning is the authority for what has been taught. Do not require a DLP orchestrator, private settings store or registered year profile.

If only a year level is supplied, pitch conservatively to that level/band using familiar prior knowledge. Do not claim verified curriculum alignment; state internally that curriculum alignment is unverified unless the user supplied curriculum/planning evidence.

### Orchestrated mode

Use this only when the caller supplies an actual DLP context with an active year-profile record. Then apply the supplied profile and parent pack release workflow. Do not switch to orchestrated mode merely because Year 4/5 or Year 6 examples exist in the package.

## Difficulty

`ALL` is the accessible entry point. `MOST` represents secure expected performance. `SOME` extends the same mathematical focus through meaningful complexity, representation or reasoning; it does not automatically jump a year level.

Within a pair, keep all three tiers on the same mathematical focus. Do not substitute three unrelated retrieval skills for All/Most/Some.

## Graph-reading contract

For graph pairs:

- `ALL` reads one value directly.
- `MOST` compares two values or finds a difference.
- `SOME` combines values, infers a missing value, or justifies a conclusion.
- Every exact answer must be visibly recoverable from the graph.
- Pictographs show an explicit key.
- Bar/column/line graphs show unit intervals needed by the questions, or an explicit statement such as `Each interval = 1`.
- Never ask students to infer an exact unmarked value from a sparse scale.

## Presentation

Use Trebuchet MS. Meaningful tier tasks and answers are at least **36 pt**. The `WHY` explanation is at least **28 pt**. Keep colour restrained and semantic. Use proper stacked fraction notation where practical.

When creating a PPTX, use the canonical header `NUMERACY WARM-UP n OF total • QUESTION` or `• ANSWER`. Where the presentation tool permits shape names, tag tier task/answer text `DLP:main` and the answer explanation `DLP:why`.

## Validation and release

Read `references/release-boundaries.json`. If Python execution is available, run:

`python scripts/validate_warmup_deck.py <deck.pptx> --expected-pairs 5`

Use the user-requested pair count instead of 5 only when they explicitly changed it. A validator FAIL blocks delivery as a finished standalone warm-up. If execution is unavailable, manually check the same contract and describe the result as unvalidated rather than claiming deterministic validation.

Standalone validator PASS means **component-ready**, not whole-pack classroom-ready. In orchestrated mode, the parent DLP release authority still controls whole-pack release.

## Common failures

- all questions followed by all answers;
- `1 / 2 / 3` instead of `ALL / MOST / SOME`;
- a `WHY` prompt on the question slide;
- no `WHY` explanation on the answer slide;
- unrelated skills used as the three tiers;
- graph values that cannot be read exactly from the displayed scale;
- shrinking task text below the minimum to make content fit.
