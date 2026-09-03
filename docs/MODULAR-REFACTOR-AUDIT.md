# Daily Lesson Pack modular refactor audit

## Finding

The Daily Lesson Pack has crossed the point where one monolithic `SKILL.md` is the most reliable architecture.

The current `main` skill mixes orchestration, timetable logic, source hierarchy, Morning Work, two warm-up systems, Shared Reading, Guided Reading, writing pedagogy, Mathematics pedagogy, printable rules, slide design, colour, geometry and release QA. A correction intended for one component can therefore alter unrelated output.

## Repository integrity problem

The current root `SKILL.md` also routes to numerous files that are not present in the repository. At the time of this refactor, `references/` contains only:
- `panel-containment-standard.md`
- `semantic-colour-standard.md`
- `slide-deck-quality-standards.md`

The monolith still names many absent files, including planning, output, curriculum-map and QA references. Historical validation material already noted that earlier packages did not contain every referenced file. The modular refactor therefore does **not** invent missing historical content.

## Refactor principle

Split by ownership, not by arbitrary file size.

A component should become its own skill when it can reasonably be requested, tested and revised independently.

## New ownership map

| Component | Owner |
|---|---|
| Date/week/timetable/source hierarchy | `daily-lesson-pack` orchestrator |
| Morning Work | `dlp-morning-work` |
| Literacy warm-up | `dlp-literacy-warmup` |
| Shared Reading | `dlp-shared-reading` |
| Guided Reading | `dlp-guided-reading` |
| Writing lesson | `dlp-writing-lesson` |
| Mathematics warm-up | `dlp-numeracy-warmup` |
| Main Mathematics lesson | `dlp-maths-lesson` |
| Independent release QA | `dlp-pack-qa` |

## Rules intentionally centralised

Only cross-component invariants remain in the orchestrator: text separation, specialist exclusions, sequence, assembly, output scope and QA routing.

Slide readability, colour and panel-containment standards remain shared repository standards because they apply across several components.

## Latest feedback incorporated

This refactor explicitly captures later classroom requirements that are not fully represented in the current monolith:
- Literacy warm-up doubled to 10 prompt/answer pairs.
- Mathematics All / Most / Some prompts are three separate questions of increasing complexity, not one task with progressively complete answers.
- Warm-ups do not need a generic whiteboard footer.
- Shared Reading uses one short paragraph plus one clearly separated question per slide.
- The current role-based Trebuchet MS projected-readability standard is preserved rather than forcing every element to exactly the same size.

## Subsequent correction in 3.7.0

The original refactor preserved 10 Mathematics prompt/answer pairs (20 slides)
without validating that inherited value against the classroom standard. The
T3W7 Thursday regression exposed this as a requirements failure. Version 3.7.0
restores five prompt/answer pairs (10 slides total), stores the value in the
machine-readable pack profile and tests it deterministically.

## Failure isolation

The QA skill returns defects to the owner only. Example:

`Shared Reading paragraph too dense` -> `dlp-shared-reading`

It must not trigger a rewrite of the numeracy warm-up, writing sequence or Mathematics lesson.

After the owner revises the defect, full QA runs again to detect regressions.

## Migration strategy

1. Introduce component skills and fallback contracts without deleting current shared QA files.
2. Replace root `SKILL.md` with orchestration-only logic.
3. Run a representative Daily Lesson Pack through the modular branch.
4. Compare against current quality standards and recent classroom feedback.
5. Only after regression testing, merge the modular branch into `main`.
6. Recover or recreate genuinely required planning references from authoritative source documents in a separate migration; do not keep dangling filenames in production instructions.

## Expected benefit

The main gain is failure isolation. Changes to Shared Reading, warm-up calibration or Mathematics language can be tested and versioned independently. The parent skill becomes easier to reason about, while QA becomes stable even when generators evolve.
