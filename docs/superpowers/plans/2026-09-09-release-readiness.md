# Daily Lesson Pack Release-readiness Workflow

> **For agentic workers:** Use Superpowers' executing-plans workflow, or genuine subagent-driven development where the host supports it. Execute one bounded issue at a time, with a failing regression, the smallest complete change, and independent review. This document is a proposed workflow, not implemented code or release evidence.

**Goal:** Deliver a verified creator-first Daily Lesson Pack installation that produces correct, feasible materials, blocks defective output and accurately reports its operational state.

**Architecture:** Complete the existing runtime and central release authority. Reconcile the existing creator-first roadmap, profile registry and blind benchmark. Prove the actual host and the exact installed package rather than create another orchestration or QA framework.

**Tech stack:** The repository's Python runtime, schemas, component skill contracts, package builders and GitHub Actions; one verified production host, renderer and private settings backend. Provider/backend identity is an audit result, not assumed here.

**Spec:** `docs/superpowers/specs/2026-09-09-release-readiness-design.md`.

**Prepared:** 9 September 2026, Australia/Perth.

## Global constraints

The design's Global constraints section applies in full. In particular: preserve creator-first settings, point-of-need teaching, profile isolation, actual independent reviews and the existing complete-pack release authority. Do not treat remembered facts, synthetic tests, a merged PR or a built ZIP as proof of deployment or classroom quality.

## 1. Rechecked starting point

Main was inspected at `c31f686fb75c3addbb47ccbd147ba6e11e488e55`. PR #11 is open, non-draft and currently reports mergeable; its head is `7cba2d72642dcc22cf8a8d1ea8e8a075ff0766ad`. PR #9 is open, draft and currently reports mergeable; its head is `529020f1e9c0bd33738e32000958baa12b9716a2`. These current mergeability results supersede the earlier assessment's conflict flags. They do not establish acceptance.

PR #11 includes the 72-item creator-first roadmap as well as the proposed profile-registry implementation. Preserve that decision ledger and backlog. Do not equate the presence of its 72 issue documents with 72 implemented features.

The prior assessment bundle records 125 passing tests on main and the isolated profile-audit defect. That is earlier evidence; this workflow has not rerun the full suite. Its historical probe uses a bundled copy of the old audit. A regression for the fix must exercise the new repository code, not rerun an unchanged historical copy and call the result a fix verification.

The inspected main branch reports `protected: false`; the ruleset listing including parent rulesets is empty. Treat enforcement of the release workflow as work to complete, subject to actual administrative capability. No repository settings were changed here.

Skill Craft did not appear in plugin discovery. This workflow uses the inspected repository and Superpowers guidance; it does not claim a separate Skill Craft audit.

## 2. Define release scope before implementation

### Creator release: required

The release must automatically load the creator's confirmed defaults, support real private scoped settings, follow authoritative current planning sources, and provide point-of-need differentiation. Its primary classroom context remains Year 4/5 with predominantly Year 5 teaching and deliberate Year 3/4 foundational retrieval. Those are planning defaults, not fixed learner ceilings or evidence of attainment.

Correctness, modelling-to-practice coherence, independent evidence, feasible timing, resource availability, readable final rendering, teacher briefing, required printables and genuine independent QA are release requirements. Preserve the approved morning-work exemplar; do not treat a visual exemplar as proof that a whole lesson is educationally sound.

### Assisted versus unattended

Assisted release still passes all material correctness, usability and evidence gates. It permits a teacher/operator to initiate a run, inspect a pilot, resolve genuine input gaps and restart a failed run. It is not a lower-quality release class.

Unattended release additionally proves the real scheduler, bounded execution/restart, duplicate prevention, observable failures and delivery. If those operational gates are incomplete, the label must explicitly remain assisted.

### Work retained for later releases

Keep broader profile calibration, richer learning history, advanced editing, model-routing optimisation and optional interface conveniences in the existing backlog. Mark each item's release allocation explicitly. Mandatory creator settings, accurate materials and the actual host integration cannot be deferred while claiming the creator workflow is complete.

Use the existing A/D/R/L/C/H/S/E IDs. The work packages below are release-coordination labels, not a replacement issue numbering system.

## 3. Development control loop

For every bounded issue:

- [ ] Read the controlling decision, current implementation and dependency evidence.
- [ ] Write the concrete failing regression or record an observable failing behavioural baseline. Verify that it fails for the intended reason, not a missing dependency.
- [ ] Make the smallest complete change across the affected producer, schema, consumer, audit, instructions, fixtures and package boundaries.
- [ ] Run the focused test and relevant regression suite. Preserve both the original failure and corrected result.
- [ ] Obtain an independent requirements review, then a code-quality/security review. The reviewer receives the issue, diff, sources and evidence, not a rehearsed conclusion.
- [ ] Correct findings and repeat affected verification. A repair is not accepted from the author's assertion alone.
- [ ] Reconcile against current main, verify the integrated revision, and merge only within authorised scope.
- [ ] Update the existing status register with exact commit/evidence references and remaining deployment gaps.

One integrator owns shared contracts, schema migrations and merge order. Implementers work in isolated worktrees. Parallelise only disjoint file ownership. If genuine separate agents are unavailable, execute the development tasks serially and arrange actual independent review; do not invent separate actors or review receipts.

## 4. Work packages and gates

### W0 — Establish the trustworthy baseline and deployment route

**Existing scope:** A01–A06; early E01/E03/E07 evaluation work.

**Read/maintain:** `docs/implementation/DECISIONS.md`, `BASELINE.md`, `STATUS.json`, `BACKLOG.json` from PR #11; `SKILL.md`; `docs/AGENT-ORCHESTRATION.md`; existing source/package provenance.

- [ ] Pin main and relevant PR heads; record the actual local worktree state before changing anything. Preserve unrelated user work.
- [ ] Reconcile PR #11's decision ledger with main's older runtime-only and year-pathway requirements. Record the planned retirement/migration instead of silently restoring superseded rules.
- [ ] Inventory source SHA, published package, installed location and active-host identity separately.
- [ ] Verify one real host's independent execution, canonical assembly, rendering, private storage and delivery capabilities. Prove a private write/read across fresh sessions without recording secrets.
- [ ] Run the existing suite and package audits from a clean checkout. Attribute existing failures before changing the skill.
- [ ] Preserve approved exemplars and diagnostic failures under their distinct classifications.

**Gate G0:** A pinned capability inventory and reproducible baseline exist. A required missing host capability becomes a named integration dependency, not an imagined installed service. Structural development may continue, but live/deployment acceptance remains blocked until the capability is real.

### W1 — Close profile and release-authority bypasses

**Existing scope:** D02 in PR #11, with applicable R/E hardening tests.

**Existing/PR touchpoints:** `references/year-level-profiles/registry.json`, `schemas/year-level-profile.schema.json`, `scripts/year_profile_registry.py`, `scripts/audit_year_profile_context.py`, `scripts/build_execution_plan.py`, `scripts/audit_release_bundle.py`, package builders and `tests/test_year_profile_registry.py`.

- [ ] Reproduce the supplied-maturity defect against the pinned baseline and turn it into a test of the current repository audit.
- [ ] Inspect PR #11's actual diff; bring it onto current main while preserving the approved morning-work exemplar and subsequent fixes.
- [ ] Bind profile identity, declared maturity and domain coverage to the authoritative bundled registry, profile source and provenance hashes. Reject caller-only promotion.
- [ ] Test unknown labels, false calibration, stale source hashes, missing domain evidence and wrong profile references. Include valid calibrated and valid candidate controls.
- [ ] Test every release route, including direct finalisation/audit calls; do not secure only the orchestrator wrapper.
- [ ] Build and inspect the complete and component packages with the same profile discovery source.
- [ ] Independently review the integrated change and only then accept/merge it.

**Gate G1:** The `banana`/false-calibration class cannot produce a normal classroom release. Valid candidates remain explicitly candidates, valid authorised profiles still function, and profile changes do not silently alter the established creator pitch.

### W2 — Restore and validate the blind benchmark

**Existing scope:** PR #9, A04, A06 and E03.

**Touchpoints:** `examples/benchmarks/t3w8-tuesday-mass-narrative-known-failure/`; the exact referenced `assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx`; `scripts/run_blind_qa_regression.py`; `tests/test_t3w8_mass_narrative_qa_fixture.py`.

- [ ] Recover the exact original deck and full human review from trusted source material. Verify the README's declared SHA-256 values. Do not silently replace either with a reconstruction.
- [ ] Keep source identity and the historical wrong-day defect intact. Renaming a file cannot repair the historical fixture.
- [ ] Verify that the original review supports each expected finding and distinguish required findings, advisory observations and false-positive guards.
- [ ] Restore fixture-integrity, scorer and isolation tests. Those tests are not a live review.
- [ ] Run the actual reviewer in a fresh isolated environment that cannot read the review, oracle, benchmark instructions naming defects or the generator's conclusions. The parent scorer loads the oracle only after the review output is finalised.
- [ ] Inspect the runner's real file/network permissions: a temporary working directory alone is not an information barrier.
- [ ] Add approved positive controls and held-out defective variants. Use the morning-work exemplar only for its approved scope; curate a full-pack positive control separately.
- [ ] Record every trial, including misses and spurious findings. Do not retain only a successful retry.

**Gate G2a:** Original artefacts and fixture integrity are complete; otherwise the historical benchmark is explicitly blocked.

**Gate G2b:** With the real host from W4, the blind reviewer returns the expected refusal, detects all locked required findings and avoids the named false positives. Positive controls are not falsely blocked. Additional unexpected findings require evidence-based adjudication, not automatic dismissal because they are absent from the oracle.

### W3 — Implement the creator's settings and point-of-need contract

**Existing scope:** D01 and D03–D10; D02 comes from W1.

**Touchpoints:** Existing creator/default profile and shared-context contracts, `SKILL.md`, component contracts, runtime context schemas, persistent settings producer/reader and central QA requirements. Use the existing issue-specific paths after checking them; proposed paths are not evidence that files already exist.

- [ ] Automatically select the confirmed non-sensitive creator defaults.
- [ ] Implement one private, versioned settings backend on the verified host. Separate settings from teaching observations and from factual planning sources.
- [ ] Support authorised standing, one-day, date-range and unit overrides with explicit scope, provenance and expiry. Save acknowledgements require successful storage.
- [ ] Test fresh-session persistence, another teacher/class, failed writes, corrupt storage, expiry, undo/reset and upgrade/rollback compatibility.
- [ ] Replace compulsory Year 4/Year 5 pathway requirements across prompts, producers, schema/check identifiers, QA expectations and fixtures together.
- [ ] Use task-specific evidence to offer support, prerequisite intervention and challenge. No evidence means conditional guidance, not fabricated learner placements.
- [ ] Preserve default curriculum/retrieval direction while allowing authorised different profiles and teacher configuration.
- [ ] Test paired inputs where only enrolment year changes: that change alone must not force a different demand. Test changed instructional evidence separately: appropriate support should then change.

**Gate G3:** In a fresh installed session, defaults load without repeated setup; authorised settings persist truthfully and privately; profiles/classes remain isolated; point-of-need behaviour replaces year streams throughout code and QA. A renamed compulsory three-tier stream is not acceptance.

### W4 — Complete one real production route

**Existing scope:** R01–R07, A03 and the required L/C runtime interfaces.

**Existing touchpoints:** `scripts/agent_orchestrator.py`, `scripts/agent_adapter.py`, `scripts/build_execution_plan.py`, `scripts/build_daily_pack.py`, `scripts/content_source.py`, `skills/registry.v2.json`, existing schemas and the actual host integration.

- [ ] Use real host executions and captured receipts/transcripts, not model-invented actor IDs.
- [ ] First prove component-only operation with the required independent Mathematics critic. `COMPONENTS_VALIDATED` is not a released pack.
- [ ] Connect the host's repository-conforming assembler and renderer. Audit an existing conforming builder before writing another one.
- [ ] Produce the deck, briefing and every context-required resource from canonical records with stable ownership and identifiers. The assembler may not invent new instructional prose.
- [ ] Render every final slide/page, record actual hashes and run complete binding checks.
- [ ] Execute independent semantic and visual review of the final candidate, plus deterministic provenance checks and explicit classroom-usability targets.
- [ ] Repair only owning components within the existing cumulative attempt budget; rebuild and repeat complete applicable pack QA on changed artefacts.
- [ ] Inject missing configuration, unavailable provider, renderer failure, malformed output, missing checks, stale review hashes and attempt exhaustion.

**Gate G4:** One real representative candidate completes the full path, including separate repeated Mathematics instances, while injected failures remain unreleased with actionable evidence. A synthetic adapter pass cannot satisfy this gate.

### W5 — Resolve classroom-usability blockers before candidate freeze

**Existing scope:** Release-critical L01–L09 and C01–C15 work. Audit which requirements already function; do not rebuild them indiscriminately. Record any nonblocking later allocation explicitly in the existing backlog.

**Touchpoints:** Existing specialist skills, canonical content/plan contracts, central `references/qa-requirements.json`, `references/qa-workflow-v3.md`, existing content/binding audits and applicable tests.

- [ ] Before full authoring, produce a compact plan that includes elapsed time, teacher attention, task dependencies, accessible instructions/data, resources and meaningful student responses.
- [ ] Count reading/thinking, modelling, responses, feedback, setup and transitions. Check schedule arithmetic in code; independently review the plausibility of activity timings.
- [ ] Check that modelling supports the actual independent task, fresh examples test transfer, and practice/exit evidence aligns to the taught goal.
- [ ] Preserve retrieval's purpose rather than making every warm-up preview the day's topic. Resolve activity counts from authorised policy and feasible time, not an invented global count.
- [ ] Check meaningful Mathematics representations, units, instruments and answer correctness; verify Reading/Writing text dependency and task alignment.
- [ ] Ensure required task information stays available when the teacher moves on. Provide actual required resources, not unsupported instructions to find or print unspecified materials.
- [ ] Review final rendered task hierarchy, wrapping and projection readability in the target environment. Do not infer native PowerPoint correctness solely from a substitute renderer.
- [ ] Walk through teacher and student actions. Record whether resources and teacher attention make the activity workable.
- [ ] Convert each material failure into a minimal executable or observed-behaviour regression with an acceptable control.

**Gate G5:** No unresolved error materially affects accuracy, learning access, independent evidence, timing, required resources or readability. Stylistic preferences may be logged; material correctness and evidence integrity cannot be waived by relabelling them warnings.

### W6 — Freeze, package, clean-install and run acceptance

**Existing scope:** E01/E03/E04/E05/E07 and existing packaging work.

**Touchpoints:** `.github/workflows/dlp-tests.yml`, package builders/audits, `VERSION`, `README.md`, `CHANGELOG.md`, `RELEASE-PROVENANCE.json`; existing installation documentation; proposed release-readiness evidence/report extensions.

- [ ] Integrate W1–W5 changes and run complete deterministic tests. Separate string/contract-preservation tests from observed-behaviour and live tests in the report.
- [ ] Build the candidate package once from the pinned accepted source. Record its digest and file manifest, including component packages intended for distribution.
- [ ] Verify existing published/checked-in archives before overwriting them during a build. Either publish CI-built release assets as authority, or require tracked archives to match the accepted build. Do not leave two competing distribution truths.
- [ ] Install the candidate into a clean location/session with no checkout fallback or hidden conversation memory. Verify package manifest, active skill identity and dependency closure.
- [ ] Run the acceptance matrix below through that installed candidate; retain every candidate and repair history with exact source/output bindings.
- [ ] Verify the actual target renderer, downloadable/openable outputs and colleague-context isolation.
- [ ] Obtain a limited teacher pilot review of the accepted final materials. Record real observations separately from model judgement. Do not claim learning improvements from test results.
- [ ] Test rollback with compatible private state, without overwriting unrelated skills or silently discarding settings.
- [ ] Publish the same tested package bytes, download them again and verify their identity. Activate and verify the intended installed version.

**Gate G6:** Exact-source, exact-package, clean-install and actual-host acceptance evidence exists. Every material acceptance case passes; none is hidden as skipped, cancelled or unexecuted. The assisted release may be declared only for its verified profile/host scope. Any correction produces a new candidate and invalidates affected evidence.

### W7 — Prove unattended operation separately

**Existing scope:** R/E reliability work; add bounded operational tasks to the existing backlog where not already represented.

- [ ] Exercise the actual scheduling mechanism with a controlled test trigger. A schedule description or chat promise is not an executed schedule.
- [ ] Make interrupted runs remain unreleased. Initially use a new run with source revalidation and bounded full restart where safe; do not build complex resume merely to achieve a label.
- [ ] Test interruption after authoring, assembly and review, including a content change before restart.
- [ ] Prevent duplicate publication using a stable logical request identity plus attempt-specific execution IDs.
- [ ] Test expired credentials, provider failure, renderer failure and exhausted retries. Never silently substitute a lower-quality provider or a previous day's pack.
- [ ] Surface a precise failed/blocked status through the actual available delivery/notification channel. Preserve diagnostics without leaking private sources.
- [ ] Confirm the scheduled output is the same hash-bound artefact that was released and can actually be retrieved/opened.

**Gate G7:** The real scheduled path either produces the correctly reviewed artefacts once, or reports failure honestly without a false success. Until then, retain the assisted-only label. Checkpoint resume may follow later, with explicit source and evidence revalidation.

## 5. Acceptance matrix

The suggested repeated-run sampling below is an engineering acceptance policy, not a scientifically established reliability threshold or a new permanent teaching preference.

| Case | Required observable result |
|---|---|
| Historical mass/narrative fixture | Exact original hash; independent blind refusal; all locked required findings found; false-positive guards respected. |
| Valid positive control | No invented release blocker; all applicable coverage and provenance requirements still checked. |
| Five ordinary weekday packs | Correct supplied dates/timetables/focus, all scheduled instances and required materials; no invented missing-day facts. Use five complete source-backed cases, not assumed school schedules. |
| Two repeated Mathematics blocks | Separate identities, purposes, records and outputs; neither silently omitted or merged. |
| Isolated morning-work request | Only the requested component; preserve approved visual standard and applicable pedagogical constraints. |
| Colleague's Wednesday context | Correct colleague inputs without inheriting creator-private facts or changing creator settings. |
| Clean session | The installed package and authorised sources suffice; no hidden memory or checkout dependency. |
| Persistent override | Real save/read across sessions, correct expiry and scope; failed storage is reported as failure. |
| Enrolment-only counterfactual | No forced change in task demand from enrolment label alone. |
| Evidence-change counterfactual | Appropriate conditional support/challenge responds to task-specific evidence without inventing global ability. |
| False Year 6 calibration | Caller assertion cannot promote a scaffold; candidate limitations remain visible. |
| Python-script request | Actual host trace follows the repository runtime; no independent ad-hoc generation/release path. |
| Missing timetable/current focus | Request remains blocked or clearly unresolved; no guessed classroom-ready pack. |
| Deliberate answer/transfer/task-goal error | Independent QA detects the concrete error with artefact evidence and refuses release. |
| Clipped primary instruction or missing resource | Final-render/access review identifies the specific obstruction, without claiming unrelated slides are broken. |
| Missing, stale or generator-authored QA | Rejected by evidence gates, including direct finalisation paths. |
| Content repair | Rebuild and applicable new reviews are required; prior candidate PASS is not reused. |
| Missing provider, failed render, exhausted attempts | Explicit unreleased failure, preserved diagnostics, no fabricated or synthetic production PASS. |
| Package/active-install mismatch | Release/deployment claim blocked until the mismatch is resolved. |
| Upgrade and rollback | Exact versions are observable; private state remains compatible or is safely migrated/restored. |
| Scheduled interruption/duplicate attempt | For unattended certification, correct single delivery or explicit failure, never duplicate or stale release. |

For stochastic evaluation, use all available held-out cases and repeat at least the known-failure review, a full-pack case and the clean-session/override case in three fresh executions. Record every execution. A material failure fails the candidate; investigate and fix rather than rerun until green. This sample demonstrates acceptance on those cases only, not a statistical guarantee of universal reliability.

## 6. CI and release enforcement

Keep fast schema/unit/contract/bypass tests on every relevant PR. Add package integrity, dependency and clean-install checks. Run real-agent and target-renderer acceptance on release candidates and on changes affecting those behaviours; absent credentials or runners block that acceptance rather than become synthetic success.

Use uniquely named required checks and a release-readiness summary that executes even when prerequisites fail. It must explicitly require successful evidence-producing jobs for the same candidate; missing/skipped/neutral/cancelled results do not count as release acceptance. Preserve tests of the aggregator itself, including a skipped prerequisite.

Require PRs and relevant checks for main, restrict routine bypass, and invalidate stale approvals when code changes. Configure genuine independent human approvals where eligible reviewers exist; an AI report submitted under the author's identity is not another person's GitHub approval. An authorised administrator must apply settings unavailable to the current connector, and their absence remains visible rather than claimed fixed.

Build once, test that package, and promote those exact bytes. GitHub's download-artifact digest mismatch is documented as a warning, so add an explicit fatal comparison of the actual release-file digest. Do not treat a UI warning as a fail-closed release gate. Verify expected digest metadata comes from the trusted accepted build, not a replacement value supplied beside an untrusted ZIP.

Pin the runtime/dependency environment used for acceptance and record provider/model/renderer identity where available. A material change to the active host or provider configuration requires an impact assessment and relevant live revalidation.

## 7. Efficient sequencing and ownership

```text
W0: baseline + decision reconciliation + host feasibility
       |
       +--> W1: profile/release hardening ----> W3: settings + point-of-need
       |
       +--> W2: recover fixtures + blind-runner construction
       |
       +--> W4: actual host, component smoke, canonical assembly
                       |
                W3/W5 integration: feasible instructional materials
                       |
             W2 live benchmark + W1/W3/W4/W5 verification
                       |
       W6: freeze package -> clean install -> acceptance -> pilot
                       |
          assisted release of the exact tested package
                       |
       W7: real scheduler and failure/delivery proof -> unattended label
```

W2 preparation can run in parallel with W1 and host discovery. W3 and W4 may proceed concurrently only where interface contracts and file ownership are agreed. The integrator serialises schema and central QA changes. Live G2b needs the real reviewer host; W6 cannot pass with only G2a fixture/scorer tests.

A practical development allocation is one integrator, a runtime/profile implementer, a settings/instructional implementer and an evaluation/package implementer, with independent review executions. These roles may be serial and need not become extra production agents.

## 8. Required release record

Record the accepted source SHA; release/package version and digest; distributed file manifest; active installation path/identity; host fingerprint without secrets; supported profile/domain scope; schema and QA contract versions; actual test commands and results; frozen input hashes; all candidate output/render hashes; independent review receipts/transcripts; failed attempts and repairs; pilot acceptance/dispositions; unresolved nonblocking limitations; rollback proof; and whether unattended operation is verified.

For each existing backlog item, retain separate implementation and operational status. Suggested progression is `absent -> partial -> implemented-unverified -> verified -> packaged -> installed -> activated`, with classroom observation recorded separately. Do not force evidence into a linear label when only one dimension is known.

## 9. Current commands confirmed in the inspected operator guide/workflow

These are existing commands, not a claim that they were executed in this planning turn. Run them from the appropriate pinned checkout after authorised implementation. Use an isolated environment and a new output directory for each runtime run.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build_chatgpt_package.py --out /tmp/daily-lesson-pack-candidate.zip
python scripts/package_component_skills.py --out /tmp/dlp-component-candidates
```

After supplying real request/context/source/host files conforming to the documented schemas:

```sh
python scripts/build_execution_plan.py --context runtime/context.json --sources runtime --out runs/plan-check
python scripts/agent_orchestrator.py --request runtime/request.json --context runtime/context.json --sources runtime --config runtime/host.json --out runs/component-check --stop-after components
python scripts/agent_orchestrator.py --request runtime/request.json --context runtime/context.json --sources runtime --config runtime/host.json --out runs/full-acceptance
```

A components-only exit of zero is not a pack release. New profile, persistence, behavioural, install and operational regressions described above must be implemented and evidenced; do not invent command outputs for tests that do not yet exist.

## 10. Sources and evidence boundaries

Live GitHub reads used for this workflow:

- Main identity and protection summary: https://api.github.com/repos/Malajusa/daily-lesson-pack/branches/main
- Rulesets including parents: https://api.github.com/repos/Malajusa/daily-lesson-pack/rulesets?includes_parents=true
- PR #11 metadata and changed files: https://github.com/Malajusa/daily-lesson-pack/pull/11
- PR #9 metadata and changed files: https://github.com/Malajusa/daily-lesson-pack/pull/9
- Main contracts: https://github.com/Malajusa/daily-lesson-pack/blob/c31f686fb75c3addbb47ccbd147ba6e11e488e55/SKILL.md
- Operator guide: https://github.com/Malajusa/daily-lesson-pack/blob/c31f686fb75c3addbb47ccbd147ba6e11e488e55/docs/AGENT-ORCHESTRATION.md
- Existing CI: https://github.com/Malajusa/daily-lesson-pack/blob/c31f686fb75c3addbb47ccbd147ba6e11e488e55/.github/workflows/dlp-tests.yml
- Creator-first decisions: https://github.com/Malajusa/daily-lesson-pack/blob/7cba2d72642dcc22cf8a8d1ea8e8a075ff0766ad/docs/implementation/DECISIONS.md
- Existing roadmap workflow: https://github.com/Malajusa/daily-lesson-pack/blob/7cba2d72642dcc22cf8a8d1ea8e8a075ff0766ad/docs/implementation/WORKFLOW.md
- Existing backlog: https://github.com/Malajusa/daily-lesson-pack/blob/7cba2d72642dcc22cf8a8d1ea8e8a075ff0766ad/docs/implementation/BACKLOG.md
- Blind fixture protocol: https://github.com/Malajusa/daily-lesson-pack/blob/529020f1e9c0bd33738e32000958baa12b9716a2/examples/benchmarks/t3w8-tuesday-mass-narrative-known-failure/README.md

Primary documentation checked for release-control recommendations:

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/actions/tutorials/store-and-share-data

The supplied `Daily_Lesson_Pack_Assessment_Evidence_2026-09-09.zip` was read as prior diagnostic evidence. Its full-suite result and isolated probe are not new test runs. Original PPTX/review recovery, live teaching-pack generation, a fresh full test run, installation inspection, GitHub mutations and classroom observation were not performed in this planning task.
