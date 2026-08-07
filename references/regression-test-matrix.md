# Regression test matrix

Maintain the 14 `regression` entries in `release-checklist.json`. Record a dated result, fixture or prompt, output location, evaluator context, evidence and defect links for every scenario.

## Required scenarios

1. Re-run the failed Thursday request exactly and compare every slide with the stronger Tuesday exemplar set.
2. A day with two separated Mathematics blocks.
3. A day with no Mathematics.
4. Monday's weekly printing workflow.
5. An assembly morning.
6. An explicit incomplete-lesson exception.
7. A relief day.
8. Every scheduled guided-reading level and word-count band.
9. Number lines, bar models, arrays, measurement diagrams and graphs.
10. Default progression when the previous lesson is assumed completed.
11. Specialist-subject exclusion across all files.
12. Blind full-size comparison against the Tuesday clarity exemplars.
13. Fresh evaluator contexts that cannot see the intended corrections.
14. The retained Thursday non-examples must be rejected.

Passing one scenario does not imply the whole regression scope passes. Use `quality_checklist.py validate --scope regression` only after all 14 entries carry current evidence.

## Term 3 four-day overview fixtures

These fixtures are mandatory evidence for the relevant existing regression scenarios; they do **not** increase the 14-entry release-checklist scope:

- `tests/term-3-week-5-monday-test.md` — default progression, equivalent-fractions day focus, Information Report elaboration toolkit, Kenya/Finland separation and very-low guided reading.
- `tests/term-3-week-5-tuesday-test.md` — Tuesday progression, equivalent-fractions generation, explicit elaboration teaching, Costa Rica/Barbados separation and low guided reading.

Both fixtures must pass in a fresh evaluator context whenever the Term 3 four-day overview, source hierarchy, English planning rules or mathematics progression rules change.

A Wednesday regression check must also confirm that Wednesday remains a valid timetable day while receiving **no four-day-overview allocation** unless the user explicitly requests it.
