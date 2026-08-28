# Daily Lesson Pack — Development Workflow

## Source of truth

This repository is the authoritative source. Develop from the current accepted
branch, validate the complete repository tree, then build installation packages
from a tagged commit. Installed copies and conversation attachments are outputs,
not sources of truth.

Stable shared-class context belongs in
`references/shared-class-context-contract.md`. Do not depend on a developer's or
teacher's chat memory for behaviour that another account must reproduce.

## Rule precedence

When updating the skill:

1. Preserve the latest explicit user decision.
2. Treat later deliberate changes as superseding contradictory older rules.
3. Do not use an older ZIP, archived copy or remembered version to overwrite newer behaviour.
4. If two current rules genuinely conflict and precedence cannot be established, surface the conflict rather than silently choosing one.

## Recommended change process

### 1. Define the behaviour change

State what is wrong with the current output and what observable behaviour should change.

### 2. Locate the controlling instructions

Identify the relevant section or sections of `SKILL.md` and any supporting files. Avoid broad rewrites when a precise change will suffice.

### 3. Make the smallest complete change

Update all instructions necessary to make the behaviour consistent, including dependent rules and quality checks.

### 4. Add or update a regression example

A useful regression case should contain:

- the prompt or classroom context;
- the behaviour being tested;
- the required outcome;
- known failure modes to check for.

### 5. Review for contradictions

Before accepting a change, check that it does not unintentionally conflict with:

- timetable/day-selection rules;
- lesson progression rules;
- literacy warm-up requirements;
- shared/guided reading separation;
- mathematics clarity requirements;
- printable and backup requirements;
- curriculum authority rules;
- output-format requirements;
- previously accepted deliberate exceptions.

### 6. Validate representative outputs

Test at least one normal day and, where the change affects them, relevant variants such as Monday weekly printing, relief coverage, mathematics-heavy lessons or differentiated reading.

### 7. Record and merge

Describe the accepted behaviour change in `CHANGELOG.md`, review the diff, then merge to `main`.

### 8. Package and clean-context test

When context routing, source precedence or packaging changes:

1. run `examples/benchmarks/memory-independent-wednesday-regression.md`;
2. validate the complete package dependency closure;
3. build the installation ZIP from the accepted repository state;
4. install or unpack it into a clean location and validate it again;
5. tag the accepted commit only after these checks pass.

## Commit guidance

Prefer focused commits such as:

- `Clarify mathematics task language`
- `Add term-overview progression rule`
- `Fix literacy warm-up answer sequencing`
- `Preserve separate shared and guided reading texts`

Avoid commits that combine unrelated skill changes.

## Versioning

Use Git history and tags for recoverability. A version label should identify an accepted skill state, not merely a work-in-progress edit.

## Regression library

The `examples/` directory is intended for compact benchmark cases. It should describe expected behaviour rather than store large generated teaching packs unless a particular artefact is essential to the test.
