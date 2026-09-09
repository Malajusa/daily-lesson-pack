# D02 implementation checkpoint

## Source and scope

Accepted base: `cf8bda191733c2b54feb2f4f30b5cd4ce7bd9d79`, current `main`
when cloned; clean working tree. Branch: `feat/d02-validated-profile-registry`.
Read-only GitHub search found open PRs #1 (older overview) and #9 (mass/narrative
QA fixture); neither supplies this registry. Their work was not changed.
Source VERSION is 3.9.0. RELEASE-PROVENANCE.json describes an earlier release
lineage, not proof of the active installed package. No installed upgrade occurred.

The original 72-item backlog, issue specifications, decisions and traceability
are preserved unchanged here. STATUS.json is the separate progress record.
This is one D02 foundation change. A01/A02 prerequisites are satisfied for this
bounded scope; the wider inventory and host-dependent M0 gates remain partial.
Choosing D02 first permits profile identity/maturity enforcement without claiming
that D01/D03 defaults or D08 point-of-need migration already work.

## Relevant capability inventory

| Capability | Baseline evidence | Classification and action |
|---|---|---|
| Profile sources | references/year-level-profiles/year-4-5.md and year-6.md | Implemented-unverified teaching calibration; teaching guidance and maturity labels preserved; Year 6 release paragraph reconciled |
| Profile discovery | audit_year_profile_context.SUPPORTED_PROFILES; both package builders' fixed lists | Partial; replaced by validated registry discovery |
| Profile status enforcement | audit_year_profile_context.main trusted supplied status | Partial; direct audit now rejects inconsistent maturity claims |
| Source freezing | build_execution_plan.freeze_context; test_execution_plan.py | Verified control-plane behaviour; registry hash added to provenance |
| Component handoff | agent_registry.references_for; agent_protocol.component_request | Verified synthetic runtime behaviour; registered profile metadata included |
| Packaging | build_chatgpt_package.py, package_component_skills.py, CI | Verified source/package closure; discovery now follows registry |
| Creator defaults/resolver | default-pack-profile.json holds architecture, not requested instructional defaults | Absent requested D01/D03 behaviour; next slice |
| Persistent settings | no verified private host backend in this session | Unsupported here; D04 remains blocked on A03 |
| Point-of-need task routing | agent_protocol.required_component_checks, audit_pack_contract, QA.B4081F2450, root/component contracts | Partial/incompatible: year-based checks remain; D08 migration required |
| Real agents and release | agent_adapter.JsonCommandAdapter, agent_orchestrator, agent_pipeline; synthetic tests | Control plane verified; live teaching-provider execution unverified |

Registry `calibrated` is the existing Year 4/5 source status, not a new classroom
validation. Domain evidence explicitly remains implemented-unverified. Year 6
is scaffold/candidate. Neither coverage nor curriculum anchor places learners.
Language/representation and retrieval guidance remain source references; this
slice does not invent structured retrieval bands or new subject pedagogy.

## A03: host and storage

This session provides a transient Linux checkout, Python execution, GitHub access
and a separate code-review agent. Those capabilities do not establish a configured
teaching-agent command, classroom PowerPoint rendering parity or a durable private
settings store. No persistence backend is selected or acknowledged as saved.
D04 must integrate one actual supported host/backend and test a fresh process.
The isolated Python environment here is only a test environment, not a skill host.

## A04/A06: diagnostic evidence and metrics

DIAGNOSTIC-SOURCES.json records hashes of the supplied source deck and review;
the 105-slide PPTX matches the supplied review's SHA-256. The deck and review
content are not added to this public change. They are diagnostic, not gold data.
Reported timings remain supplied-review evidence. Clipping on slides 15/35/59
was reported but not reproduced in the earlier substituted-font renders; no cause
or fix is claimed. Existing quarter-kilogram modelling and correct Writing
prompt/model order must be preserved. Minimal pedagogical fixtures, target
playback and a fixed classroom pilot remain pending.

The superseded patch validation is historical supplied evidence (corrupt at line
196), not a new execution of an unavailable patch. No old patch was applied.
Teacher preparation time, classroom duration, friction, manual corrections,
latency/cost of teaching agents and learning outcomes are unknown, not zero.

## Executed verification

The first default-interpreter run failed (116 discovered tests, 2 failures,
42 errors) because declared jsonschema/referencing dependencies were missing.
An isolated Python 3.12 environment with repository requirements and a compatible
typing_extensions was then used, including subprocesses launched with `-I`.
No repository dependency contract was weakened to accommodate the environment.

- Base: `python -m unittest discover -s tests -v`: 124 tests passed.
- New regression before implementation: 9 errors for missing registry module; reviewer regressions then reproduced three additional defects before repair.
- Focused after implementation: 11 tests passed after reviewer regressions.
- Full after implementation: 135 tests passed. One legacy mocked audit report was migrated to include the required normal release mode; the new candidate/missing-mode regressions remain negative controls.
- For both base and changed tree: `python scripts/build_chatgpt_package.py --out
  <scratch>/complete.zip` and `python scripts/package_component_skills.py --out
  <scratch>/components` succeeded.
- For both trees: `python scripts/audit_package_dependencies.py --skill-root
  <extracted-root>` passed for the complete package; the same command with
  `--component` passed for all eight component packages.

Fixtures are synthetic runtime metadata. No model-authored lesson, classroom
render, blind deck review, installed activation or learning improvement is claimed.

## Migration and rollback

The registry is a version-1 sidecar with its own schema. Existing run/context
schema version 2 and historical QA requirement IDs are unchanged. New v2 runs
bind the registry hash before execution; existing frozen plans must be rebuilt
because the canonical context gains registry provenance and derived metadata.
False maturity claims are rejected. Historical evidence is not rewritten or
recertified. Legacy audits may derive omitted status from authoritative metadata;
they may not invent a promotion.

Profile content edits require an explicit registry revision/hash update and
calibration evidence; stale sources fail package builds and runtime freezing.
Rollback is the previous source commit/package with its matching run evidence.
The release consumer now blocks candidate or missing profile mode. The earlier
Year 6 ad-hoc review exception requires an explicit evidence-backed source/registry
graduation; general QA success alone cannot promote it. No private settings schema
or data is changed. Built ZIPs are validation outputs,
not an installed or newly numbered accepted release.

Next dependency-ready work: D01 plus D03 after D02 review, followed by D08 once
A04's minimal diagnostic fixtures exist. D04 needs the actual A03 host/backend.

## Independent review

A separate read-only reviewer found three defects: candidate mode was not consumed
at release, wrong-kind registry provenance could bind a private file, and anchor
years could contradict profile identity. Each was reproduced by a regression and
repaired by the implementer. The same reviewer re-examined the repairs, independently
ran all 11 focused tests and reported no further material defects in this scope.
No review of generated teaching materials or installed runtime was performed.
