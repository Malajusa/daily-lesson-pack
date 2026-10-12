# Daily Lesson Pack regression baseline — 12 October 2026

## Baseline identity

This baseline audits the exact 3.10.0-rc.4 candidate at
`fa19e62af168a29e2cde8fcc680e86b00a1ef3e9`, the source identified by PR #18
as the basis of the installed Daily Lesson Pack Workflows 0.1.3 plugin.

The purpose of this pass is to distinguish historical failures that are already
contracted/tested from remaining enforcement gaps. The initial RED pass changed
no generation behaviour; this branch then implements only the gaps proven by
those regressions.

## Historical failure matrix at the pinned baseline

| Failure class | Current baseline evidence | Classification |
| --- | --- | --- |
| Missing lesson status causes invented reteaching | `term-week-day-planning-contract.md` defines exception-only status and `test_planning_hierarchy.py` checks the precedence contract. | COVERED |
| Chat memory supplies timetable/focus | `shared-class-context-contract.md`, `memory-independent-wednesday-regression.md` and `test_release_contract.py` prohibit memory-backed runtime facts. | COVERED |
| Morning Work loses approved composition/usability | Teacher-approved T3W8 exemplar is checksum-bound and referenced by `dlp-morning-work`; visual QA remains required. | COVERED AT CONTRACT/QA LEVEL |
| Literacy Reminder → Question → Answer drifts | `dlp-literacy-warmup` requires exactly matched R→Q→A sequences, self-contained questions and one student action/response. | COVERED AT CONTRACT LEVEL |
| Shared Reading answer/passage mismatch or text reuse | `dlp-shared-reading` requires immediate matched answers, paragraph-supported claims and no Morning Work/Guided Reading text reuse. | COVERED AT CONTRACT LEVEL |
| One-component request activates full-pack semantics | Runtime can stop after components, but root Request routing has no first-class component-only route. | RED |
| Standalone component context is forced to carry a briefing | `run-context.schema.json` requires both `deck` and `briefing` in `required_artifacts`. | RED |
| Direct build accepts unbound source labels | `freeze_context` validates hashed provenance, but `dlp_build_runtime.validate_resolved_context` does not require `source_provenance` or bind field sources to it. | RED |

## RED tranche

The executable RED suite captured only the three remaining gap classes:

1. root request routing must define a first-class `component-only` path and
   bind it to `--stop-after components`;
2. a component-only frozen context must be valid with `required_artifacts:
   ["deck"]` and no forced full-pack briefing;
3. direct finalisation must reject contexts without hashed source provenance
   and must bind resolved field sources to those records. The orchestration path
   remains stronger because it also re-hashes the referenced source files.

The RED sequence was verified in GitHub Actions before implementation:
- first clean baseline: 254 tests, exactly 3 intended failures;
- tightened baseline: 256 tests, exactly 4 intended failures and no errors.

## GREEN implementation

The branch now:
- adds first-class `component-only` request routing using
  `--stop-after components`;
- adds an explicit `request_scope` contract so component-only contexts may
  request a deck without weakening the normal Daily Pack briefing requirement;
- applies the canonical run-context schema on the direct runtime path and binds
  every resolved runtime source to explicit source provenance.

## Deliberate exclusions

This tranche does not rewrite the A→B→C planning hierarchy, lesson-status
policy, memory-independence rules, Morning Work exemplar, Literacy/Shared Reading
contracts or release QA. Those have existing controls and should only be changed
if a new executable regression demonstrates a remaining defect.

Rendered classroom quality and real host/provider execution remain separate
acceptance layers; deterministic source tests must not claim those have been
validated.
