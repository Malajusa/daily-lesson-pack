# Numeracy warm-up release-boundary regression

Use this regression whenever `dlp-numeracy-warmup` generation, layout, packaging, review or release logic changes.

## Captured failures

The following historical output shapes must fail:

1. `Q1 Q2 Q3 Q4 Q5 ... A1 A2 A3 A4 A5 ...` rather than adjacent question/answer pairs.
2. Tier labels `1 / 2 / 3` rather than literal `ALL / MOST / SOME`.
3. A question slide with `ALL / MOST / SOME` plus a bottom `WHY` reasoning demand.
4. An answer slide without a bottom `WHY` mathematical explanation.
5. A column/bar graph labelled only at sparse values such as `0, 5, 10` when questions require exact unmarked values such as 4, 7 or 9.
6. Meaningful tier task/answer text below 36 pt or answer-slide WHY explanation below 28 pt.

## Required default deck

Exactly ten slides:

`QUESTION 1 → ANSWER 1 → QUESTION 2 → ANSWER 2 → QUESTION 3 → ANSWER 3 → QUESTION 4 → ANSWER 4 → QUESTION 5 → ANSWER 5`

### Question slide

- canonical header `NUMERACY WARM-UP n OF 5 • QUESTION`;
- literal `ALL`, `MOST`, `SOME` labels;
- one separate task beneath each label;
- no `WHY` label or reasoning/explanation demand;
- meaningful tier text at least 36 pt.

### Immediately following answer slide

- canonical matched `• ANSWER` header;
- `ALL`, `MOST`, `SOME` in the same order and positions;
- matched answer for each task;
- one bottom `WHY` label with concise mathematical explanation at least 28 pt.

## Graph reading

When graphs are requested toward the end, the default interpretation is Pairs 4 and 5. Within each graph pair:

- `ALL` reads one value directly;
- `MOST` compares two values or finds a difference;
- `SOME` combines values, infers, or justifies;
- pictographs expose a key;
- numeric graphs expose the unit interval needed for every exact answer.

Do not infer that `0, 5, 10` alone authorises reading exact intermediate values unless the unit interval is otherwise visibly explicit.

## Required evidence

Every warm-up instance requires PASS evidence for:

- `NW.PAIR.COUNT`
- `NW.PROMPT.THREE_TIERS_ONLY`
- `NW.PAIR.ADJACENT`
- `NW.ANSWER.MIRROR`
- `NW.REASONING.ANSWER_ONLY`
- `NW.GRAPH.EXACT_SCALE`
- `NW.PRESENTATION.FONT_FLOOR`

The standalone validator must also reject the captured structural failures. Any missing boundary result or FAIL blocks component-ready status and whole-pack release when embedded in Daily Lesson Pack.
