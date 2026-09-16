# Numeracy warm-up release-boundary regression

Use this regression whenever `dlp-numeracy-warmup` generation, layout, review or release logic changes.

## Baseline failure captured

The prior warm-up contract allowed a question slide to contain `All`, `Most`, `Some` **and** a bottom `Why` reasoning prompt. That output must now fail release.

A question slide such as:

- All: `348 + 256 = ___`
- Most: `4,275 + 1,896 = ___`
- Some: `12,408 + 9,675 = ___`
- Why: `Why does 348 + 256 need regrouping in the ones column?`

is a **FAIL** because the question slide contains a fourth reasoning demand.

## Required passing pair

### Question slide

- exactly three student tasks;
- labels are `All`, `Most`, `Some`;
- no `Why` box;
- no reasoning/explanation prompt elsewhere on the slide;
- no fourth student task.

### Immediately following answer slide

- is the matched answer for that question slide;
- keeps `All`, `Most`, `Some` in the same order and positions;
- answers all three tasks;
- contains the bottom green `Why` panel with a concise mathematical explanation.

## Release-failing variations

Fail the component if any of these occur:

1. A question slide contains a `Why` box or any separate reasoning/explanation demand.
2. A slide appears between a question and its matched answer.
3. The answer slide swaps, omits or relocates the All / Most / Some tiers so the pair no longer mirrors cleanly.
4. One prompt is split into All / Most / Some answer-quality expectations rather than three separate questions.
5. The answer slide omits one tier answer.
6. The answer-slide `Why` panel contains only generic checking language such as `Check your answer` rather than mathematical reasoning.

## Evidence required

For every warm-up pair, record PASS evidence against:

- `NW.PROMPT.THREE_TIERS_ONLY`
- `NW.PAIR.ADJACENT`
- `NW.ANSWER.MIRROR`
- `NW.REASONING.ANSWER_ONLY`

Any missing result or any FAIL blocks `dlp-numeracy-warmup` component acceptance and therefore classroom-ready pack release.
