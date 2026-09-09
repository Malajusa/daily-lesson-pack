# Daily Lesson Pack — complete implementation backlog

**72 bounded issues.** This backlog includes all retained idea families, using the latest teacher decisions. Items are proposed/unverified until audited; some source capabilities already exist. Use dependencies to choose work, not simply document order. E01/E03/E07 are cross-cutting early work and E04/E05 repeat at release checkpoints.

Feature enablement (`default_on`, `mandatory`, `controlled_rollout`, `opt_in`) is separate from implementation scope. Opt-in features remain part of the work; they are not silently enabled as teacher preferences.


# M0 — Establish the implementation baseline

Recover trustworthy source and evidence before editing; distinguish source code, installed package, host integration and classroom validation.

**Exit gate:** A pinned commit, capability/status inventory, host/storage decision, approved decision ledger, baseline metrics and executable known-failure fixtures are recorded.

| ID | Work item | Dependencies |
|---|---|---|
| A01 | Freeze decisions and supersessions | None |
| A02 | Pin and audit the real baseline; retire invalid patches | A01 |
| A03 | Choose and verify the deployment and persistence path | A02 |
| A04 | Capture the reviewed deck as a diagnostic regression | A02 |
| A05 | Establish bounded coding-agent work rules | A01, A02 |
| A06 | Measure a reproducible baseline and establish evaluation scaffolding | A02, A04 |

# A01 — Freeze decisions and supersessions

**Milestone:** M0 · **Owner:** integrator

**Depends on:** None

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Create a controlling decision ledger from this conversation. Later explicit teacher instructions override earlier proposals and briefs. Distinguish confirmed defaults, retained feature proposals, superseded variants and unresolved deployment facts.

## Likely touchpoints

`docs/implementation/DECISIONS.md`; `docs/implementation/TRACEABILITY.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Creator-first defaults, Year 5 direction, Year 3/4 retrieval, point-of-need teaching and remembered scoped overrides are explicit.
2. Every retained idea maps to an issue; numerical suggestions are not falsely labelled teacher-approved defaults.
3. Old runtime-only creator settings, forced recurring setup and year-based task streams are marked superseded.

## Traceability

decision log for implementation; requirements traceability; latest teacher instruction precedence.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# A02 — Pin and audit the real baseline; retire invalid patches

**Milestone:** M0 · **Owner:** repository auditor

**Depends on:** A01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Record the accepted Git SHA and dirty state; inspect open work before branching. Classify each backlog capability as absent, partial, implemented-unverified, verified or active. Archive earlier hand-written patches as superseded rather than applying them.

## Likely touchpoints

`docs/implementation/BASELINE.md`; `scripts/`; `tests/`; `dist/`; `RELEASE-PROVENANCE.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. The existing v2 patch is recorded as syntactically corrupt; no invalid patch is an input to implementation.
2. Source commit, installed ZIP/manifest and active-host version are distinguished.
3. Audit identifies controlling Markdown, Python checks, schema producers/consumers, packaging and test fixtures for each change.

## Traceability

repository truth audit; package provenance; contradiction and stale instruction audit.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# A03 — Choose and verify the deployment and persistence path

**Milestone:** M0 · **Owner:** runtime engineer

**Depends on:** A02

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Inspect the actual host before choosing a settings backend. Use persistent local storage for a local runner or an authenticated private store for a hosted runner. Select one real host path first; do not build every provider. Identify agent, critic, reviewer, assembly, render and storage capabilities.

## Likely touchpoints

`docs/implementation/HOST-CAPABILITIES.md`; `scripts/agent_adapter.py`; `scripts/agent_pipeline.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A new-session write/read probe succeeds on the selected backend, or persistence remains explicitly unsupported.
2. Actual host commands and independent execution capability are documented without credentials in the repository.
3. Unverified host facts are not filled using earlier assistant claims.

## Traceability

host capability manifest; provider-neutral adapters; real memory storage; deployment rather than prompt-only implementation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# A04 — Capture the reviewed deck as a diagnostic regression

**Milestone:** M0 · **Owner:** evaluation engineer

**Depends on:** A02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Extract minimal synthetic fixtures for pacing, task access, year-proxy differentiation, representation/coherence and render defects. Preserve the original review and artefact hash locally where appropriate. Do not promote the flawed deck to a gold standard.

## Likely touchpoints

`examples/benchmarks/`; `tests/fixtures/`; `docs/implementation/KNOWN-FAILURES.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Timing from the review is labelled supplied review evidence until authoritative timetable is recovered.
2. Clipping is tracked as reported and target-environment verification required, not assigned an invented root cause.
3. Existing quarter-kilogram modelling and correct writing prompt/model order are not incorrectly treated as absent.

## Traceability

classroom feedback regression; failure taxonomy seed; render environment reproduction; preserve correct content.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# A05 — Establish bounded coding-agent work rules

**Milestone:** M0 · **Owner:** integrator

**Depends on:** A01, A02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Define /change, /regress, /audit and /release roles; one implementer per bounded issue and an independent adversarial reviewer. Use isolated branches/worktrees and restrict files to owning contracts. Integrator controls shared schema merges.

## Likely touchpoints

`AGENTS.md`; `docs/DEVELOPMENT.md`; `.github/PULL_REQUEST_TEMPLATE.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Reviewer gets the issue, diff and evidence but not the implementer's private reasoning.
2. Each PR carries scope, dependencies, migration, negative tests, package impact and rollback.
3. Release agents cannot silently repair or fabricate PASS; no giant feature branch combines the roadmap.

## Traceability

root AGENTS.md; implementer and adversarial reviewer; coding-agent command modes; mutation boundaries for development.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# A06 — Measure a reproducible baseline and establish evaluation scaffolding

**Milestone:** M0 · **Owner:** evaluation engineer

**Depends on:** A02, A04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Define metrics before changes: teacher preparation, observed duration, copying/display friction, critical defects, recurrence, manual corrections, schema/routing/repair quality and available latency/token/cost data. Separate synthetic tests, live model evaluations and classroom evidence.

## Likely touchpoints

`evals/`; `tests/`; `docs/implementation/BASELINE-METRICS.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A baseline report records known values and unknowns without guessed costs or outcomes.
2. Known-good controls accompany injected failures; evaluations do not reward slide count alone.
3. The first-pilot scenario and review rubric are fixed before tuning.

## Traceability

agent behavioural eval harness; quality-adjusted outcomes; baseline metrics; known-good controls.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M1 — Make the skill yours by default, with real persistence

Ship the creator's confirmed preferences automatically while keeping calibration reusable and saved changes scoped and auditable.

**Exit gate:** A clean installation uses creator defaults; saved and dated overrides survive new sessions and updates; no learner placement depends on enrolment year.

| ID | Work item | Dependencies |
|---|---|---|
| D01 | Ship creator defaults automatically | A01, A02 |
| D02 | Create a profile registry and calibrated coverage model | A01, A02 |
| D03 | Resolve calibration and field-specific precedence once | D01, D02 |
| D04 | Implement durable private classroom settings | A03, D03 |
| D05 | Remember conversational overrides at the correct scope | D04 |
| D06 | Protect private state and authority to change it | D04, D05 |
| D07 | Version and migrate settings, profiles and context contracts together | D03, D04 |
| D08 | Replace year-based task routing in every controlling layer | D02, D03, A04 |
| D09 | Provide truthful defaults and safe missing-context behaviour | D03, D05 |
| D10 | Package and install the defaults-and-memory increment | D01, D02, D03, D04, D05, D06, D07, D08, D09 |

# D01 — Ship creator defaults automatically

**Milestone:** M1 · **Owner:** configuration engineer

**Depends on:** A01, A02

**Decision basis:** teacher_confirmed · **Proposed enablement:** default_on

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Create one authoritative non-sensitive built-in configuration: predominantly Year 5 main direction, Year 3/4 foundational retrieval, point-of-need differentiation and creator-first use. Missing classroom configuration selects it automatically. Do not invent jurisdiction codes, school dates, class sizes or resources.

## Likely touchpoints

`config/creator-defaults.json`; `references/default-pack-profile.json`; `SKILL.md`; `README.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A clean installation uses the creator direction without a setup wizard or preset activation.
2. Defaults are centralised, not copied as hard-coded assumptions into each content agent.
3. A missing configuration and a failed/corrupt configuration load have different outcomes; load failure does not silently reset defaults.

## Traceability

creator-first built-in defaults; no repeated onboarding; teacher preferences separated from universal pedagogy.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D02 — Create a profile registry and calibrated coverage model

**Milestone:** M1 · **Owner:** configuration engineer

**Depends on:** A01, A02

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Separate curriculum anchor, retrieval band, language/representation guidance, subject-specific calibration, jurisdiction mapping and maturity. Replace hard-coded profile discovery with a validated registry. Coverage is a support claim, not a learner ceiling.

## Likely touchpoints

`references/year-level-profiles/`; `schemas/year-level-profile.schema.json`; `scripts/audit_year_profile_context.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. All JSON examples validate including schema references; profile IDs, status, references and domain coverage agree.
2. Candidate/scaffold profiles remain labelled as such; existing Year 6 status is not silently promoted.
3. Subject-specific calibration can differ without assigning global student ability levels.

## Traceability

profile sidecars and schema; profile capability/coverage manifests; subject overrides; validated coverage not allowed-year ceiling; candidate profile maturity.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D03 — Resolve calibration and field-specific precedence once

**Milestone:** M1 · **Owner:** configuration engineer

**Depends on:** D01, D02

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Resolve current instruction, applicable temporary overrides, saved preferences and creator defaults into source-backed settings. For timetable and actual lesson facts use current authoritative planning sources; preferences must not invent those facts. Feed the same resolution to all components.

## Likely touchpoints

`scripts/resolve_instructional_calibration.py`; `schemas/instructional-calibration.schema.json`; `references/year-level-context-contract.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Every resolved value carries source, revision and effective scope.
2. Changing profile changes calibration; changing enrolment alone does not select support.
3. New overview conflicts with saved standing direction are made explicit rather than silently choosing an unrelated day focus.

## Traceability

deterministic context resolver; frozen instructional_calibration; source precedence; teacher trust.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D04 — Implement durable private classroom settings

**Milestone:** M1 · **Owner:** runtime engineer

**Depends on:** A03, D03

**Decision basis:** teacher_confirmed · **Proposed enablement:** default_on

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Implement the selected durable backend with teacher/class isolation, revisioned writes, atomicity/concurrency handling, backup and actual read-after-write verification. Do not rely on conversational recall.

## Likely touchpoints

`scripts/teacher_context_store.py`; `schemas/classroom-settings.schema.json`; `private runtime storage (outside distributable)`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Settings persist after a fresh session or process, not merely within one conversation.
2. Concurrent updates cannot silently overwrite unrelated changes.
3. A failed write never produces a 'saved' acknowledgement; current-run application is reported separately.

## Traceability

teacher preference memory; persistent settings backend; versioned writes; truthful memory acknowledgements.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D05 — Remember conversational overrides at the correct scope

**Milestone:** M1 · **Owner:** runtime engineer

**Depends on:** D04

**Decision basis:** teacher_confirmed · **Proposed enablement:** default_on

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Interpret standing, dated, lesson, unit and progression instructions into proposed changes. Validate before committing. Clear ongoing instructions save automatically; temporary instructions expire by requested lesson date/unit. Ordinary task requests are not silently promoted to standing preferences.

## Likely touchpoints

`scripts/resolve_overrides.py`; `schemas/settings-change.schema.json`; `tests/test_settings_overrides.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. 'Five from now on', 'three tomorrow' and 'for this unit' produce distinct persistence semantics.
2. Expiration restores current underlying preferences, not an old snapshot; creator timezone is Australia/Perth unless changed.
3. Undo/show/forget/reset work with revision history; ambiguous high-impact scope asks only the necessary clarification.

## Traceability

scoped remembered overrides; natural-language settings changes; undo and explain; one-time setup only when genuinely needed.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D06 — Protect private state and authority to change it

**Milestone:** M1 · **Owner:** runtime engineer

**Depends on:** D04, D05

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Restrict persistent changes to authorised teacher requests. Agents may propose changes; source documents are data, not authority to issue settings commands. Exclude private state and credentials from packages; support deletion/export and minimal collection.

## Likely touchpoints

`scripts/teacher_context_store.py`; `references/shared-class-context-contract.md`; `scripts/build_chatgpt_package.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A hostile document cannot overwrite defaults or cause unrelated private data reads.
2. Teacher and class namespaces are isolated; another teacher cannot receive the creator's private learning records.
3. Package scans contain only approved non-sensitive defaults, never names, diagnoses, private overviews or secrets.

## Traceability

private/shared configuration separation; persistence security; no fabricated placements; authorised changes only.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D07 — Version and migrate settings, profiles and context contracts together

**Milestone:** M1 · **Owner:** configuration engineer

**Depends on:** D03, D04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Choose an explicit versioned sidecar or schema-version upgrade and migrate all producers, consumers, fixtures, handoffs and audits. Keep immutable run snapshots with settings/profile/source revisions; support compatible rollback and reject unknown future versions.

## Likely touchpoints

`schemas/`; `scripts/migrate_context.py`; `scripts/build_execution_plan.py`; `tests/fixtures/`; `docs/PROFILE_CALIBRATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. No new required field is introduced without executable production and fixture migration.
2. A settings or profile change makes a new run context and does not rewrite prior evidence.
3. Rollback preserves later authorised settings or performs an explicit compatible migration, never silent data loss.

## Traceability

versioned handoff schemas; atomic migration; context snapshot provenance; settings survive updates.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D08 — Replace year-based task routing in every controlling layer

**Milestone:** M1 · **Owner:** pedagogy/runtime engineer

**Depends on:** D02, D03, A04

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Remove mandatory Year 4/Year 5 pathways from prompts, Python check selection, QA and fixtures. Introduce point-of-need requirements using new semantic check IDs with explicit retirement mapping. Do not merely rename streams Support/Core/Challenge.

## Likely touchpoints

`skills/dlp-maths-lesson/SKILL.md`; `scripts/agent_protocol.py`; `scripts/audit_pack_contract.py`; `references/qa-requirements.json`; `references/component-instance-contract.md`; `skills/dlp-pack-qa/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A paired enrolment-only perturbation does not change task-specific support or challenge.
2. An advanced younger and prerequisite-needing older synthetic learner both receive evidence-appropriate responses.
3. An unknown-readiness run has diagnostic checks and conditional guidance, not invented groups or a global ability score.

## Traceability

universal point-of-need contract; enrolment invariance; no fixed ability streams; QA ID semantic migration.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D09 — Provide truthful defaults and safe missing-context behaviour

**Milestone:** M1 · **Owner:** configuration engineer

**Depends on:** D03, D05

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Distinguish optional history from essential runtime facts. Reuse valid saved timetable and direction; do not repeat supplied questions. With no learning history use diagnostics; with missing essential timetable/focus mark unresolved and resolve minimally. Do not infer mastery from scheduled advancement.

## Likely touchpoints

`references/shared-class-context-contract.md`; `SKILL.md`; `scripts/context_resolver.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. First use with valid defaults but no learner history is supported.
2. Unavailable required equipment or focus does not become an invented assumption.
3. Previously supplied settings load without repeated setup; materially stale planning sources are identified.

## Traceability

degraded mode; uncertainty mechanism; saved planning source validity; scheduling is not mastery.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# D10 — Package and install the defaults-and-memory increment

**Milestone:** M1 · **Owner:** release engineer

**Depends on:** D01, D02, D03, D04, D05, D06, D07, D08, D09

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Build the first usable increment for the selected host. Include all public schema/reference/runtime dependencies; keep host secrets private. Verify install identity and load/write settings in a new host session.

## Likely touchpoints

`scripts/build_chatgpt_package.py`; `scripts/package_component_skills.py`; `.github/workflows/dlp-tests.yml`; `docs/COMPONENT-SKILL-INSTALLATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Clean installed package—not repository checkout—resolves creator defaults and persisted overrides.
2. Corrupt/missing backend failures and class isolation are tested.
3. Manifest/commit of the active installation matches the accepted increment.

## Traceability

clean-install creator default regression; package dependency closure; actual activation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M2 — Complete the reliable agent execution path

Verify and extend the existing orchestration and release infrastructure; connect actual host executions and canonical assembly.

**Exit gate:** A real component run, critic, assembly and independent review complete through the repository path; missing integrations, stale evidence and exhausted budgets fail closed.

| ID | Work item | Dependencies |
|---|---|---|
| R01 | Verify and extend the executable registry and dependency graph | A02, D07 |
| R02 | Enforce minimum necessary context and instructions | R01, D03, D08 |
| R03 | Validate immutable handoffs and execution states | R01, D07 |
| R04 | Connect real agent executions and canonical assembly | A03, R02, R03 |
| R05 | Keep QA centralised, explicit and independent | R03, R04, D08 |
| R06 | Route bounded repairs to owners and invalidate evidence | R03, R05 |
| R07 | Enforce one release authority across every entry point | R04, R05, R06, D07 |

# R01 — Verify and extend the executable registry and dependency graph

**Milestone:** M2 · **Owner:** runtime engineer

**Depends on:** A02, D07

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Reuse existing registry roles and graph. Validate references, cycles, duplicates, repeated timetable instances, required barriers, max concurrency and role ownership. Derive compatibility discovery from one authority when feasible.

## Likely touchpoints

`skills/registry.v2.json`; `skills/registry.json`; `scripts/agent_registry.py`; `scripts/build_execution_plan.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Independent components can run concurrently; real content dependencies cannot be bypassed.
2. Repeated Mathematics blocks remain separate instances.
3. Registry changes cannot silently remove critic/review/release requirements.

## Traceability

registry as executable control plane; DAG execution; unique timetable instances; v1/v2 compatibility.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R02 — Enforce minimum necessary context and instructions

**Milestone:** M2 · **Owner:** runtime engineer

**Depends on:** R01, D03, D08

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Project only relevant approved settings, sources, calibration, plan and evidence into each agent. Mandatory references remain explicit; conditional references use validated rules. Specialists cannot reinterpret timetable or silently change settings.

## Likely touchpoints

`skills/registry.v2.json`; `scripts/agent_protocol.py`; `skills/*/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Every generator receives identical governing calibration bindings and its own instance.
2. Unrelated component content and private data are not supplied unnecessarily.
3. Missing required projected fields fail before paid generation rather than being silently skipped.

## Traceability

minimum viable context; mechanical prompt envelopes; mandatory/conditional references; reduced context drift.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R03 — Validate immutable handoffs and execution states

**Milestone:** M2 · **Owner:** runtime engineer

**Depends on:** R01, D07

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Verify schema/semantic identity checks, invocation states, unique attempts, hash bindings, atomic writes and confined file scopes. Receipts and transcripts come from the actual host; different labels alone do not prove independence.

## Likely touchpoints

`schemas/agent-request.schema.json`; `schemas/agent-result.schema.json`; `scripts/agent_protocol.py`; `scripts/agent_orchestrator.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Malformed, duplicate, stale, wrong-owner and path-escaping results are rejected.
2. PASS becomes stale after inputs change; retries use new invocation IDs and preserve old records.
3. Logical write scopes are not misrepresented as an operating-system sandbox.

## Traceability

request/result protocol; node state machine; immutable attempts; mutation boundaries; real observability.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R04 — Connect real agent executions and canonical assembly

**Milestone:** M2 · **Owner:** runtime engineer

**Depends on:** A03, R02, R03

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Connect the selected host to component agents, Mathematics critic and independent reviewers. Supply repository-conforming ContentSource assembly and final rendering. Verify actual credentials/config privately; no provider integration is assumed.

## Likely touchpoints

`scripts/agent_adapter.py`; `scripts/agent_pipeline.py`; `private host bridge`; `docs/AGENT-ORCHESTRATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Run a real component milestone first, then a real candidate pack with briefing.
2. No configuration, render or independent reviewer means no classroom-ready claim.
3. Synthetic adapters and assemblers remain test-only and cannot masquerade as classroom generation.

## Traceability

provider adapter; host integration; real renderer; components-first executable milestone.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R05 — Keep QA centralised, explicit and independent

**Milestone:** M2 · **Owner:** QA engineer

**Depends on:** R03, R04, D08

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Reuse one QA requirement registry, partitioning semantic, rendered and deterministic coverage. Retain an explicit Mathematics critic where required. Reviewers report evidence and defects; they do not edit content or invent a broad PASS.

## Likely touchpoints

`skills/dlp-pack-qa/SKILL.md`; `skills/dlp-pack-qa/agents/openai.yaml`; `references/qa-requirements.json`; `scripts/pack_evidence.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Expected targets are covered exactly once with evidence bound to candidate hashes.
2. QA cannot be invoked opportunistically in the generator context and count as independent.
3. Requirement method/owner changes are tested; no duplicate competing QA policy systems.

## Traceability

QA coordinator not giant reviewer; semantic/visual/provenance fan-out; explicit QA; Maths critic; central requirements.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R06 — Route bounded repairs to owners and invalidate evidence

**Milestone:** M2 · **Owner:** runtime engineer

**Depends on:** R03, R05

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Batch reviewer defects by canonical instance/owner, separate transport retries from repairs while sharing bounded budgets, and stop on unresolved pack-level ambiguity. Reuse untouched content; rebuild and rerun complete applicable QA after content changes.

## Likely touchpoints

`schemas/defect.schema.json`; `scripts/agent_orchestrator.py`; `scripts/agent_pipeline.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Multiple defects do not cause one rebuild per defect.
2. A literacy repair cannot silently rewrite writing or Mathematics.
3. Exhausted budgets, malformed reviews, missing defects for FAIL and stale accepted pointers leave an unreleased candidate.

## Traceability

structured defects; owner-local repair; bounded retry loop; complete QA invalidation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# R07 — Enforce one release authority across every entry point

**Milestone:** M2 · **Owner:** release engineer

**Depends on:** R04, R05, R06, D07

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Bind canonical content, plan, resource set, settings revision, renders and reviews to the delivered candidate. New plan checks must apply to direct finalisation as well as orchestration. Preserve package provenance and explicit warning disposition.

## Likely touchpoints

`scripts/build_daily_pack.py`; `scripts/dlp_build_runtime.py`; `scripts/audit_release_bundle.py`; `scripts/agent_pipeline.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A direct build invocation cannot bypass new policy requirements.
2. Changed content, plan, resources or renders invalidate dependent review and release.
3. Transport success and component PASS are never conflated with complete-pack release.

## Traceability

release arbiter deterministic; same-hash release; no bypass; candidate versus released distinction.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M3 — Approve a feasible instructional plan before full authoring

Turn teaching intent, prerequisite evidence, time, teacher attention and resources into an executable delivery plan.

**Exit gate:** Generation consumes an approved, hash-bound delivery plan; incompatible resources or infeasible essential scope cannot be hidden by a declared minute total.

| ID | Work item | Dependencies |
|---|---|---|
| L01 | Resolve lesson intent and a single learning claim | D03, D08, R02 |
| L02 | Create the pre-authoring delivery-plan contract and gate | L01, R01, R03 |
| L03 | Audit elapsed time and teacher attention | L02 |
| L04 | Model resources, setup, copying and display friction | L02 |
| L05 | Create dependency-safe short and technology-fallback lesson routes | L02, L03, L04 |
| L06 | Make diagnostic point-of-need responses explicit | D08, L01 |
| L07 | Resolve shared instructional threads before parallel authoring | L01, D03 |
| L08 | Track uncertainty and evidence-backed plan decisions | D09, L02, L06 |
| L09 | Offer lesson styles without changing pedagogical invariants | D05, L02 |

# L01 — Resolve lesson intent and a single learning claim

**Milestone:** M3 · **Owner:** pedagogy engineer

**Depends on:** D03, D08, R02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Operationalise existing lesson-mode guidance across components: introduce, consolidate, diagnose, intervene, extend or assess. State the essential learning claim and distinguish must-learn, must-practise and optional enrichment.

## Likely touchpoints

`references/universal-maths-instruction-canon.md`; `schemas/delivery-plan.schema.json`; `skills/*/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Changing intent changes modelling/evidence appropriately, not merely the heading.
2. Every activity has a learning, retrieval or necessary classroom-operation purpose.
3. No duplicate new Mathematics intent framework contradicts the existing canon.

## Traceability

teacher intent; single learning claim; essential versus optional enrichment; lesson purpose alignment.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L02 — Create the pre-authoring delivery-plan contract and gate

**Milestone:** M3 · **Owner:** runtime engineer

**Depends on:** L01, R01, R03

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Use existing specialists in a compact planning pass. Collect activity IDs, durations, task types, dependencies, groups/participants, attention, resources, display access and reveal conditions. Approve the combined plan before expensive full authoring; revised plans require new validation.

## Likely touchpoints

`schemas/delivery-plan.schema.json`; `scripts/build_delivery_plan.py`; `scripts/agent_orchestrator.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Schema-valid but semantically incomplete plans are rejected.
2. Full authoring cannot start before approved plan bindings exist.
3. Final canonical tasks map back to plan activities; unplanned additions require revalidation.

## Traceability

two-pass generation; lesson-budget planner; approved plan before slides; plan-to-content traceability.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L03 — Audit elapsed time and teacher attention

**Milestone:** M3 · **Owner:** runtime engineer

**Depends on:** L02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Account for reading, thinking, response, modelling, discussion, feedback, setup, transitions and contingency. Compute concurrent elapsed time correctly and enforce exclusive teacher/resource demands. Declared time totals are not proofs of realistic student work.

## Likely touchpoints

`scripts/audit_classroom_delivery.py`; `tests/test_delivery_plan.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. An overfilled activity plan fails even when estimated_minutes claims it fits.
2. Independent simultaneous tasks may overlap; incompatible exclusive teacher activities do not.
3. A human/model reviewer evaluates task-duration plausibility separately from schedule arithmetic.

## Traceability

activity timing budgets; teacher-load audit; operability; time budget versus slide count.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L04 — Model resources, setup, copying and display friction

**Milestone:** M3 · **Owner:** runtime/pedagogy engineer

**Depends on:** L02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Record equipment availability, quantities, locations and setup/cleanup, printing and log-in costs, display/app changes and copying burden. Treat friction/screen-change metrics as diagnostic indicators initially, not universal thresholds.

## Likely touchpoints

`schemas/delivery-plan.schema.json`; `scripts/audit_classroom_delivery.py`; `schemas/classroom-settings.schema.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. One scale cannot support multiple exclusive concurrent uses.
2. Required printing/copies derive from authoritative resource/class data, not guessed counts.
3. Transcribing instructions or diagrams is distinguished from writing a learning response.

## Traceability

resource model; resource friction scoring; copying burden audit; screen-change budget; physical classroom constraints.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L05 — Create dependency-safe short and technology-fallback lesson routes

**Milestone:** M3 · **Owner:** pedagogy engineer

**Depends on:** L02, L03, L04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Define the minimum viable lesson and optional branches. Time reduction removes enrichment first and checks prerequisites; if essential learning cannot fit, narrow scope explicitly rather than compressing everything. Plan a board/briefing route for technology failure.

## Likely touchpoints

`schemas/delivery-plan.schema.json`; `skills/*/SKILL.md`; `references/delivery-plan-contract.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Removing a model cannot leave unsupported independent work in the short route.
2. A lost-time request produces a feasible alternate plan or an explicit scope blocker.
3. Fallback does not depend on the failed projector, unavailable equipment or duplicate full-slide printouts.

## Traceability

minimum viable lesson; essential versus enrichment; lost-time contingency; technology fallback planning.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L06 — Make diagnostic point-of-need responses explicit

**Milestone:** M3 · **Owner:** pedagogy engineer

**Depends on:** D08, L01

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Specify observable checks, conditional support, rechecks, fading and connected extension. Allow a time-bounded prerequisite goal when a shared task remains inaccessible. Keep routes in teacher guidance where possible rather than expanding every branch into slides.

## Likely touchpoints

`skills/dlp-maths-lesson/SKILL.md`; `skills/dlp-writing-lesson/SKILL.md`; `schemas/delivery-plan.schema.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Scaffolds address the diagnosed difficulty instead of lowering all task demands.
2. A learner can use one support while attempting demanding reasoning.
3. No-history plans give unassigned conditional routes; changing enrolment alone leaves them unchanged.

## Traceability

diagnostic differentiation; scaffold fading; diagnostic branching without deck branching; no fixed tiers; point-of-need interventions.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L07 — Resolve shared instructional threads before parallel authoring

**Milestone:** M3 · **Owner:** pedagogy engineer

**Depends on:** L01, D03

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Approve compact transfer targets across related components. Link Reading and Writing craft goals; connect relevant prerequisite checks to Mathematics without converting cumulative Numeracy retrieval into a compulsory lesson preview.

## Likely touchpoints

`scripts/build_delivery_plan.py`; `skills/registry.v2.json`; `skills/dlp-shared-reading/SKILL.md`; `skills/dlp-writing-lesson/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Related agents receive the same approved target and can still run concurrently.
2. A task must show how it supports the target, not merely share a theme.
3. Shared and Guided Reading remain distinct according to their owning contracts.

## Traceability

cross-component coherence; daily instructional threads; reading-to-writing transfer; retrieval distinct from prerequisite check.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L08 — Track uncertainty and evidence-backed plan decisions

**Milestone:** M3 · **Owner:** runtime/pedagogy engineer

**Depends on:** D09, L02, L06

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Log source-backed decisions, omissions, assumptions and conflicts at decision level. Use evidence availability and justified uncertainty rather than uncalibrated model confidence percentages. Missing optional evidence can trigger a diagnostic; material missing facts block the affected claim.

## Likely touchpoints

`schemas/decision-log.schema.json`; `scripts/build_delivery_plan.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. The teacher can inspect why a scaffold, retrieval item or omission exists.
2. No-prior-learning evidence cannot become a confident readiness assumption.
3. Low-evidence planning and disagreement trigger a relevant check or escalation, not automatic release.

## Traceability

decision provenance; teacher trust rule; confidence/uncertainty mechanism; confidence-calibrated escalation seed.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# L09 — Offer lesson styles without changing pedagogical invariants

**Milestone:** M3 · **Owner:** configuration/pedagogy engineer

**Depends on:** D05, L02

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Support lean, standard, high-support and relief-teacher styles as explicit options. They alter presentation and guidance density, not curriculum claims, student labels or mandatory evidence. Do not silently save an assistant-suggested style as the creator's preference.

## Likely touchpoints

`schemas/classroom-settings.schema.json`; `references/delivery-plan-contract.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A style swap retains the same governing objective and point-of-need access.
2. A lean pack does not remove necessary modelling or task instructions.
3. Relief mode adds usable teacher guidance within the same time/resource constraints.

## Traceability

pedagogical pack styles; lean versus high-support/relief; teacher delivery preferences.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M4 — Produce and release classroom-usable materials

Fix the reviewed failure classes and implement the retained authoring, display, accessibility, operability and quality controls.

**Exit gate:** A representative pack using creator defaults passes deterministic checks and independent semantic/rendered/classroom-delivery review for its exact artefacts, then is validated by the teacher for a pilot.

| ID | Work item | Dependencies |
|---|---|---|
| C01 | Generate coordinated student, teacher and resource outputs | L02, L07, R04 |
| C02 | Resolve warm-up quantity and selection from time and policy | D03, L02, L03 |
| C03 | Use purposeful representation progression and authentic measurement | L06, L04, C01 |
| C04 | Design meaningful variation and control unintended novelty | L01, L06, C03 |
| C05 | Stop authoring when the instructional purpose is satisfied | L01, L02, C04 |
| C06 | Make reading text-dependent and writing models appropriately sequenced | L07, C01 |
| C07 | Design inspectable responses and discriminating exit evidence | L01, L06 |
| C08 | Audit language and accessibility without lowering the intended concept | C01, D02 |
| C09 | Guarantee persistent task access | L04, C01 |
| C10 | Fix rendering and verify the actual playback environment | A04, C01, R04 |
| C11 | Improve visual navigation while preserving the approved grammar | C01, C09, C10 |
| C12 | Formalise intended answer-reveal states | L02, C01, C06 |
| C13 | Produce the minimum viable board/briefing fallback | L05, C01 |
| C14 | Detect redundancy and apply owner-approved compression | C02, C04, C05, C09, C12 |
| C15 | Gate classroom readiness on five independent dimensions | L03, L04, L08, C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, R07 |

# C01 — Generate coordinated student, teacher and resource outputs

**Milestone:** M4 · **Owner:** content/render engineer

**Depends on:** L02, L07, R04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Use canonical task/document IDs for projected text, teacher guide, answers and actual resources. Teacher guidance covers timing, noticing, diagnostic branches, advance/reveal points and optional adaptations. The assembler cannot invent pedagogical prose.

## Likely touchpoints

`scripts/content_source.py`; `schemas/component-result.schema.json`; `skills/*/SKILL.md`; `host assembly integration`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Deck, briefing and task resources agree on wording/data/answers through canonical references.
2. Required resources are present and included in release bindings.
3. Generation and review traces preserve task ownership across all deliverables.

## Traceability

two output channels; canonical ContentSource; teacher-facing guidance; real printables.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C02 — Resolve warm-up quantity and selection from time and policy

**Milestone:** M4 · **Owner:** pedagogy/runtime engineer

**Depends on:** D03, L02, L03

**Decision basis:** retained_proposal · **Proposed enablement:** controlled_rollout

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Resolve warm-up count once from authorised preferences and available time. Start the reviewed ten-minute literacy case with five sequences as a proposed, testable planning value, not a universal permanent preference. Use the configured retrieval band, maintain self-contained prompts and feedback, and reduce superficial cognitive switching.

## Likely touchpoints

`references/default-pack-profile.json`; `skills/dlp-literacy-warmup/SKILL.md`; `skills/dlp-numeracy-warmup/SKILL.md`; `scripts/audit_pack_contract.py`; `references/qa-requirements.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Ten-minute fixture with five appropriately brief sequences is reviewed for feasibility; thirty-slide overload is caught.
2. A longer or explicitly overridden block is not rejected solely for a different count.
3. Generation, deterministic audits and independent QA consume the same count/policy; cumulative Numeracy remains distinct from new teaching.

## Traceability

literacy overload correction; profile/time-resolved sequence counts; knowledge coherence; purposeful warmups; no universal slide target.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C03 — Use purposeful representation progression and authentic measurement

**Milestone:** M4 · **Owner:** Mathematics engineer

**Depends on:** L06, L04, C01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Connect representations, language and notation; use concrete/authentic instruments, approximate readings and units where the objective warrants them. Include practical work only with confirmed resources. Strengthen existing quarter-kilogram representation rather than duplicate it as though absent.

## Likely touchpoints

`skills/dlp-maths-lesson/SKILL.md`; `references/universal-maths-instruction-canon.md`; `examples/benchmarks/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Mass fixtures distinguish genuine instrument reading from number-line arithmetic.
2. Representations are mathematically exact or explicitly approximate as intended.
3. Equivalent quality tests cover at least one non-measurement concept; no mass-only hard-coding.

## Traceability

authentic instruments; hands-on resources; representation progression; meaning before procedure; decimal quantity representation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C04 — Design meaningful variation and control unintended novelty

**Milestone:** M4 · **Owner:** Mathematics/pedagogy engineer

**Depends on:** L01, L06, C03

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Specify what changes and stays invariant across examples; audit prerequisite modelling, unfamiliar notation, decimals, vocabulary, context and response format. Treat novelty as a reviewable design record, not a fabricated universal numerical budget.

## Likely touchpoints

`references/universal-maths-instruction-canon.md`; `skills/dlp-maths-lesson/SKILL.md`; `schemas/delivery-plan.schema.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Independent examples do not introduce unmodelled demand accidentally.
2. Fewer well-varied tasks distinguish understanding from imitation.
3. Difficulty caused by confusing wording or presentation is identified separately from intended conceptual challenge.

## Traceability

variation-design contract; example-boundary tests; novelty budget; desirable versus extraneous difficulty; model-to-practice alignment.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C05 — Stop authoring when the instructional purpose is satisfied

**Milestone:** M4 · **Owner:** pedagogy engineer

**Depends on:** L01, L02, C04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Require evidence that the intended concept, critical variation, guided response and independent check are covered; then stop. Additional examples need a stated purpose and budget. Slide count is an output, with 65–75 only a reviewed-pack revision reference.

## Likely touchpoints

`skills/*/SKILL.md`; `references/delivery-plan-contract.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A locally useful extra activity is rejected or made optional when it duplicates coverage or exceeds time.
2. Compression cannot lower fonts, remove essential practice or break answer separation just to meet a count.
3. The stop condition is observable coverage, not a model's generic 'complete' assertion.

## Traceability

generation stopping rules; anti-bloat; slide count follows pedagogy; must learn/practise/optional.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C06 — Make reading text-dependent and writing models appropriately sequenced

**Milestone:** M4 · **Owner:** English pedagogy engineer

**Depends on:** L07, C01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Connect Shared Reading questions to the approved craft/comprehension target, preserve answers supported by displayed text and paragraph/question constraints, and retain Writing's modelling/joint/independent/revision sequence. Add teacher holds before independent model reveals.

## Likely touchpoints

`skills/dlp-shared-reading/SKILL.md`; `skills/dlp-guided-reading/SKILL.md`; `skills/dlp-writing-lesson/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Reading questions require the actual text, not generic background knowledge.
2. The reading-to-writing transfer is explicit without adding unnecessary sequences.
3. Independent model answers follow and are held until student attempts; correct existing ordering is preserved.

## Traceability

text dependency; author craft focus; Reading/Writing coherence; protect writing sequence; drafting hold.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C07 — Design inspectable responses and discriminating exit evidence

**Milestone:** M4 · **Owner:** pedagogy/evaluation engineer

**Depends on:** L01, L06

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Map models/tasks/exits to the learning claim; record response mode and opportunity to respond. Distinguish participation, completion and learning evidence. Use error patterns to discriminate misconceptions where justified; record assistance rather than a universal numerical ability ladder.

## Likely touchpoints

`skills/*/SKILL.md`; `schemas/delivery-plan.schema.json`; `evals/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Watching, copying or turn-and-talk is not automatically counted as evidence of independent mastery.
2. Exit questions can reveal the target misconception and its alternatives with cautious interpretation.
3. Teacher guidance explains what response to inspect and what it warrants next.

## Traceability

opportunity to respond; participation versus learning; misconception discrimination; assessment alignment; evidence support conditions.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C08 — Audit language and accessibility without lowering the intended concept

**Milestone:** M4 · **Owner:** accessibility/pedagogy engineer

**Depends on:** C01, D02

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Review language complexity separately from mathematical demand; support vocabulary while preserving accurate terminology. Check contrast, non-colour cues, accessible reading order, image descriptions, projected readability and print accessibility as appropriate to actual outputs.

## Likely touchpoints

`references/slide-deck-quality-standards.md`; `skills/*/SKILL.md`; `scripts/audit_classroom_delivery.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Simplifying language does not silently change the mathematical goal.
2. Colour is not the sole carrier of meaning; a print-safe pathway remains legible.
3. Accessibility claims specify what was actually checked rather than asserting universal compliance.

## Traceability

language-demand analyser; hard accessibility checks; reading order and alternative descriptions; projector/print accessibility.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C09 — Guarantee persistent task access

**Milestone:** M4 · **Owner:** runtime/render engineer

**Depends on:** L04, C01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Validate access throughout independent activity, not just the presence of tasks. Use readable shared tasks, concurrent optional support, or supplied resources. Do not recreate year streams or accept copying instructions as the default access solution.

## Likely touchpoints

`schemas/delivery-plan.schema.json`; `scripts/audit_classroom_delivery.py`; `host assembly integration`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Advancing to another task cannot remove required instructions from active learners without an actual alternative.
2. Resource references resolve to complete matching tasks and quantities.
3. Dual layouts pass rendered legibility, not merely geometric containment.

## Traceability

projection-state contract; persistent instructions; mixed-readiness task access; remove copying workaround.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C10 — Fix rendering and verify the actual playback environment

**Milestone:** M4 · **Owner:** render engineer

**Depends on:** A04, C01, R04

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Reproduce reported clipping using target software/fonts and actual final renders. Record substitutions and limitations. Fix owning layout/template code when reproduced; do not blame mathematical content or claim source geometry proves a clean render.

## Likely touchpoints

`references/panel-containment-standard.md`; `references/slide-deck-quality-standards.md`; `host rendering integration`; `tests/render-fixtures/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Rendered fixtures catch clipped headings, safe margins and effective text size.
2. Review covers actual final artefacts and relevant environment, not only a surrogate render.
3. Unreproduced original clipping remains documented; no fabricated root cause or unsupported claim of repair.

## Traceability

clipped heading repair; target-environment renders; font substitution evidence; rendered not source QA.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C11 — Improve visual navigation while preserving the approved grammar

**Milestone:** M4 · **Owner:** render/pedagogy engineer

**Depends on:** C01, C09, C10

**Decision basis:** retained_proposal · **Proposed enablement:** controlled_rollout

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Introduce purposeful section/resumption cues, consolidated practice layouts and optional simultaneous task/support layouts. Preserve semantic colours, whitespace and readability. Avoid decorative variety or dividers that add useless clicking.

## Likely touchpoints

`references/visual-exemplar-standard.md`; `host layout library`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Navigation improves without adding avoidable pacing load.
2. Layout variation preserves approved visual standards and canonical content.
3. Consolidation cannot reveal an answer or make one group's task disappear.

## Traceability

visual repetition correction; section dividers/resumption markers; consolidated practice; dual-path layouts without fixed grouping.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C12 — Formalise intended answer-reveal states

**Milestone:** M4 · **Owner:** runtime/pedagogy engineer

**Depends on:** L02, C01, C06

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Represent prompt, student attempt, teacher check, reveal and feedback as intended states. Validate order and hold notes. Static slides can communicate but cannot enforce elapsed time; any interactive enforcement needs a genuinely capable host.

## Likely touchpoints

`schemas/delivery-plan.schema.json`; `host assembly integration`; `skills/*/SKILL.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. No prompt includes its hidden answer prematurely.
2. Independent writing/retrieval has explicit teacher advance conditions.
3. Documentation distinguishes static intent from enforced interaction and does not claim students were prevented from seeing an answer.

## Traceability

formal reveal state transition; answer integrity; think-time and feedback; honest static PowerPoint limits.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C13 — Produce the minimum viable board/briefing fallback

**Milestone:** M4 · **Owner:** content engineer

**Depends on:** L05, C01

**Decision basis:** retained_proposal · **Proposed enablement:** controlled_rollout

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Deliver the planned emergency route with a concise key model, task, answers and exit check, linked to canonical content. Include only authorised minimal resources; do not produce a redundant printed deck.

## Likely touchpoints

`skills/*/SKILL.md`; `host briefing renderer`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A reviewer can execute the core lesson without the projector.
2. Fallback and main pack answers remain consistent.
3. Reduced-time and no-tech routes do not assume incompatible equipment.

## Traceability

technology failure fallback; teacher-load reduction; minimum viable lesson delivery.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C14 — Detect redundancy and apply owner-approved compression

**Milestone:** M4 · **Owner:** runtime/pedagogy engineer

**Depends on:** C02, C04, C05, C09, C12

**Decision basis:** retained_proposal · **Proposed enablement:** controlled_rollout

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Compare structural and semantic overlap within/across components, distinguish useful deliberate retrieval from duplication, and propose consolidation. Route content changes to owners; apply layout-only merges only when bindings, visibility and reveal order remain valid.

## Likely touchpoints

`scripts/audit_content_redundancy.py`; `scripts/agent_orchestrator.py`; `host assembly integration`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Morning Work/Numeracy duplication is reviewed without eliminating intentional cumulative retrieval.
2. Compression never rewrites accepted canonical pedagogy behind the owner's back.
3. A semantic/content change reopens affected planning and all applicable pack QA.

## Traceability

content redundancy detector; instructional compression pass; fewer slides without loss; owner preservation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# C15 — Gate classroom readiness on five independent dimensions

**Milestone:** M4 · **Owner:** QA engineer

**Depends on:** L03, L04, L08, C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, R07

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Add evidence for correctness, learnability, deliverability, accessibility and operability to the existing QA policy. Require an activity walkthrough: teacher action, learner action, visible resources and credible timing. Separate deterministic invariants from judgement and heuristic warnings.

## Likely touchpoints

`references/qa-requirements.json`; `skills/dlp-pack-qa/SKILL.md`; `scripts/audit_classroom_delivery.py`; `scripts/audit_release_bundle.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A mathematically accurate pack fails classroom-ready status for material access, pacing or rendering failures.
2. Teacher overrides can adjust preferences or waive permitted warnings with provenance, not waive wrong answers, missing evidence or critical access defects.
3. All new requirement IDs have complete expected coverage and exact artefact/plan/resource bindings.

## Traceability

classroom walkthrough QA; five release dimensions; teacher override audit; deterministic versus semantic checks; warning disposition.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M5 — Adapt across days using teacher-confirmed learning evidence

Add optional learning state, purposeful retrieval and feedback without inventing mastery or requiring a student database.

**Exit gate:** Multi-day evaluations respond appropriately to supported versus independent evidence, changing misconceptions and retrieval history; no-history use remains supported.

| ID | Work item | Dependencies |
|---|---|---|
| H01 | Introduce optional instructional state separate from settings | D04, D06, D07, L06 |
| H02 | Append teacher-confirmed events and version learning snapshots | H01, D05 |
| H03 | Make post-lesson feedback inexpensive and useful | H02, A06 |
| H04 | Build a configurable retrieval scheduler | H02, C02 |
| H05 | Maintain a task-specific misconception ledger | H02, C07 |
| H06 | Build a modest evidence-backed concept dependency graph | H01, L06, C04 |
| H07 | Use evidence conditions to adapt and fade support | H02, H05, H06, L06 |
| H08 | Expose an instructional decision and slide/task provenance graph | L08, C01, H04, H05, H06 |
| H09 | Run longitudinal adaptation evaluations | H03, H04, H05, H06, H07, H08 |

# H01 — Introduce optional instructional state separate from settings

**Milestone:** M5 · **Owner:** runtime/pedagogy engineer

**Depends on:** D04, D06, D07, L06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Record concept-specific previously taught, current focus, not-yet-taught, supplied observations, misconceptions and support conditions. Keep configuration stable and learning state changing. Class/skill level is sufficient initially; names and student databases are not prerequisites.

## Likely touchpoints

`schemas/instructional-state.schema.json`; `scripts/update_instructional_state.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. No-history runs retain diagnostics and do not block solely for absent learner records.
2. Planned, taught, attempted, supported success, independent success and transfer are distinct.
3. Global attainment labels are not inferred from isolated answers.

## Traceability

lesson-state model; instructional-state.json; optional learning history; evidence not task completion.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H02 — Append teacher-confirmed events and version learning snapshots

**Milestone:** M5 · **Owner:** runtime engineer

**Depends on:** H01, D05

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Append sourced dated observations with teacher authority and support conditions. Agents can propose interpretations but cannot record mastery merely from generation. Corrections supersede events explicitly; each next run uses an identifiable snapshot.

## Likely touchpoints

`scripts/update_instructional_state.py`; `schemas/learning-event.schema.json`; `private runtime storage`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Generating or releasing a pack creates no false 'taught' or 'mastered' record.
2. Supported success does not automatically trigger independent mastery.
3. Editing later observations does not rewrite earlier pack evidence.

## Traceability

append-only learning evidence; teacher-confirmed state updates; immutable history; no manufactured mastery.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H03 — Make post-lesson feedback inexpensive and useful

**Milestone:** M5 · **Owner:** teacher-experience engineer

**Depends on:** H02, A06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Provide concise timing, difficulty, completion, changed activities and misconception feedback. Accept ordinary language as well as optional controls. Save observations at their stated granularity and distinguish class feedback from individual evidence.

## Likely touchpoints

`scripts/teacher_feedback.py`; `schemas/teacher-feedback.schema.json`; `teacher host interface`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A brief teacher note updates the appropriate event without requiring a full assessment form.
2. Completion/cancellation affects progression; timing feedback does not invent ability.
3. The teacher can inspect, correct and remove saved feedback.

## Traceability

post-lesson feedback loop; cheap classroom feedback; progression exceptions; teacher control over evidence.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H04 — Build a configurable retrieval scheduler

**Milestone:** M5 · **Owner:** pedagogy/runtime engineer

**Depends on:** H02, C02

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Select previously taught skills using recency, independent/supported outcomes, importance, interference and curricular relevance. Use configurable spacing/interleaving intervals with documented rationale, not unsupported universal forgetting claims. Cold start follows authorised overview and retrieval band.

## Likely touchpoints

`scripts/select_retrieval.py`; `schemas/retrieval-policy.schema.json`; `private retrieval history`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Recently insecure skills and long-unretrieved secure skills are considered for different reasons.
2. Weights, intervals and overrides are visible and testable; missing results are not guessed.
3. Question count and selected items fit the activity budget and do not turn retrieval into new teaching.

## Traceability

retrieval history; retrieval selection engine; spacing/interleaving policy; forgetting policy; cumulative retrieval.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H05 — Maintain a task-specific misconception ledger

**Milestone:** M5 · **Owner:** pedagogy/runtime engineer

**Depends on:** H02, C07

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Track source, concept, observed error pattern, support used, last check and active/resolved/uncertain state. Use cautious teacher-reviewed interpretations rather than asserting a diagnosis from a single wrong answer.

## Likely touchpoints

`schemas/misconception.schema.json`; `scripts/update_instructional_state.py`; `scripts/select_retrieval.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Active misconceptions influence relevant diagnostics and practice.
2. Evidence can reduce checking frequency and allow scaffold fading.
3. Resolved status requires appropriate evidence, not the agent's own corrected answer.

## Traceability

misconception ledger; error discrimination; misconception recurrence; targeted reteaching.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H06 — Build a modest evidence-backed concept dependency graph

**Milestone:** M5 · **Owner:** pedagogy engineer

**Depends on:** H01, L06, C04

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Represent the dependencies required by validated concept families first; link difficulties to a prerequisite rather than dropping a learner to a whole year level. Separate concepts from jurisdiction codes and capture sources, caveats and maturity.

## Likely touchpoints

`references/concept-dependencies/`; `scripts/resolve_prerequisites.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Scale-reading failure can distinguish interval structure, endpoint difference and unit knowledge.
2. Cycles, unsupported dependencies and missing mappings are flagged.
3. The graph is not treated as a complete cognitive model or as authority to invent learner mastery.

## Traceability

concept dependency graph; targeted prerequisite repair; concepts separate from curriculum codes.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H07 — Use evidence conditions to adapt and fade support

**Milestone:** M5 · **Owner:** pedagogy engineer

**Depends on:** H02, H05, H06, L06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Choose maintain, recheck, fade, intervene, consolidate or extend using task-specific evidence and teacher-authorised rules. Preserve uncertainty where evidence is sparse. Do not implement a universal 0–5 ability/ZPD score.

## Likely touchpoints

`scripts/build_delivery_plan.py`; `schemas/instructional-state.schema.json`; `evals/longitudinal/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Guided success alone does not remove all support.
2. Independent success can justify fading and later transfer checks.
3. A need in one skill does not lower unrelated demands or permanently label the learner.

## Traceability

evidence quality conditions; responsive scaffold fading; gradual responsibility; no numeric ZPD ladder.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H08 — Expose an instructional decision and slide/task provenance graph

**Milestone:** M5 · **Owner:** runtime/teacher-experience engineer

**Depends on:** L08, C01, H04, H05, H06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Connect activities/tasks/slides to learning claims, prerequisites, misconceptions, sources, retrieval history, supports and essential/optional status. Answer why included/omitted/changed without exposing private model reasoning.

## Likely touchpoints

`schemas/decision-log.schema.json`; `scripts/explain_pack.py`; `teacher host interface`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A teacher can trace a specific slide to an authorised goal or operational need.
2. Decisions reference actual sources/events rather than plausible invented explanations.
3. Regeneration and compression preserve or explicitly update those links.

## Traceability

instructional decision log; slide provenance graph; why included/omitted/scaffolded; teacher trust.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# H09 — Run longitudinal adaptation evaluations

**Milestone:** M5 · **Owner:** evaluation engineer

**Depends on:** H03, H04, H05, H06, H07, H08

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Use multi-day synthetic cases for misconception, supported success, independent success, new transfer, missed lesson and conflicting observations. Compare with a no-history baseline and preserve held-out sequences.

## Likely touchpoints

`evals/longitudinal/`; `tests/test_instructional_state.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. The agent changes support in response to evidence rather than repeating reminders indefinitely.
2. Enrolment-only changes remain invariant throughout the sequence.
3. Reported adaptation quality is measured in evaluations; no classroom outcome is invented.

## Traceability

multi-day simulation; longitudinal agent evaluations; adaptive quality metrics.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M6 — Improve editing, sharing and quality-adjusted efficiency

Add the remaining portability and productivity capabilities without regressing the creator's default experience.

**Exit gate:** Personalisation, edits, partial regeneration, model routing and profile additions are measured and isolated; unsupported coverage and savings are never fabricated.

| ID | Work item | Dependencies |
|---|---|---|
| S01 | Separate curriculum jurisdiction and locale adapters | D02, D03, H06 |
| S02 | Add additional profiles with explicit capability maturity | D02, S01 |
| S03 | Offer optional recalibration and a small control interface | D05, D10, S01, S02 |
| S04 | Preserve teacher edits and locks through regeneration | C01, D06, R07 |
| S05 | Provide user-facing partial regeneration | S04, R06, C15 |
| S06 | Allocate model effort using measured quality risk | R04, R05, A06, C15 |
| S07 | Escalate bounded disagreements rather than reviewing everything twice | R05, L08, S06 |
| S08 | Build an evidence-backed metrics view | A06, H03, H09, S06 |
| S09 | Make sharing, backup and upgrades explicit and safe | D06, D07, S01, S02, S03 |

# S01 — Separate curriculum jurisdiction and locale adapters

**Milestone:** M6 · **Owner:** configuration/pedagogy engineer

**Depends on:** D02, D03, H06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Map validated concepts to jurisdiction/version identifiers separately from pedagogy. Configure spelling, terminology, dates, units, punctuation and contextual conventions. Verify specific curriculum references during implementation; do not derive statutory mapping from the brainstorming.

## Likely touchpoints

`references/curriculum-mappings/`; `references/locales/`; `schemas/year-level-profile.schema.json`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Swapping locale does not change mathematical meaning or readiness rules.
2. Unknown/outdated mappings are labelled unsupported, not silently approximated.
3. The creator's selected direction remains the default and is regression-protected.

## Traceability

jurisdiction separation; curriculum mapping adapters; localisation beyond curriculum.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S02 — Add additional profiles with explicit capability maturity

**Milestone:** M6 · **Owner:** configuration/pedagogy engineer

**Depends on:** D02, S01

**Decision basis:** teacher_confirmed · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Add candidate calibration for other year bands only with actual domain guidance and examples. Mature domains independently where justified; preserve scaffold labels until evidenced. Test creator-default isolation for every added profile.

## Likely touchpoints

`references/year-level-profiles/`; `evals/profile-isolation/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A new profile does not silently inherit creator-specific content assumptions.
2. Candidate/experimental domains cannot claim full calibration merely because files exist.
3. A justified advanced/prerequisite task is governed by evidence and validated scope, not an enrolment ceiling.

## Traceability

Year 2/3 and other profile expansion; profile coverage manifests; per-domain maturity; shareability without default regression.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S03 — Offer optional recalibration and a small control interface

**Milestone:** M6 · **Owner:** teacher-experience engineer

**Depends on:** D05, D10, S01, S02

**Decision basis:** teacher_confirmed · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Expose curriculum direction, retrieval policy, resources, lesson style and printing/display preferences. A colleague may accept creator defaults or request recalibration; extract supplied facts and ask only missing essentials. Generated profiles remain candidates until reviewed.

## Likely touchpoints

`teacher host interface`; `docs/PROFILE_CALIBRATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. The creator is never forced through a wizard to activate their own defaults.
2. A colleague's setup does not change the shipped baseline or creator's private configuration.
3. Show settings, reset, undo, scope and validity are understandable without repository knowledge.

## Traceability

calibration wizard; teacher control panel; one-time optional onboarding; sharing with personalisation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S04 — Preserve teacher edits and locks through regeneration

**Milestone:** M6 · **Owner:** runtime/content engineer

**Depends on:** C01, D06, R07

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Use stable canonical IDs and explicit locks/overrides for tasks, wording and notes. Detect conflicts with changed goals, answers or sources; preserve edits where valid and require disposition for conflicts. Locked content is still subject to accuracy and QA.

## Likely touchpoints

`scripts/merge_teacher_edits.py`; `schemas/teacher-edit.schema.json`; `host editing interface`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Regeneration does not silently erase teacher work.
2. A teacher-locked incorrect answer or stale reference cannot bypass release checks.
3. Each edit has provenance and future regeneration preserves ownership and mappings.

## Traceability

teacher edit preservation; teacher_locked; stable content IDs; conflict-aware regeneration.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S05 — Provide user-facing partial regeneration

**Milestone:** M6 · **Owner:** runtime/teacher-experience engineer

**Depends on:** S04, R06, C15

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Support requests such as 'revise Maths only'. Regenerate only selected owners and dependent content, preserve unaffected canonical records and teacher edits, but rebuild and repeat complete applicable QA for the changed final artefacts.

## Likely touchpoints

`scripts/agent_orchestrator.py`; `teacher host interface`; `scripts/agent_pipeline.py`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Unrelated content is byte-/ID-stable where appropriate; pedagogical dependencies are not ignored.
2. The workflow does not claim partial QA is sufficient after changed final content.
3. Scope and retained edits are explained in a concise change summary.

## Traceability

partial regeneration; local repairs as teacher workflow; unchanged-component preservation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S06 — Allocate model effort using measured quality risk

**Milestone:** M6 · **Owner:** runtime/evaluation engineer

**Depends on:** R04, R05, A06, C15

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Route deterministic work to code, routine authoring to suitable models and demanding conceptual/release judgement to stronger or independent reasoning. Use held-out evaluation and real cost/latency data; maintain required critic and review independence.

## Likely touchpoints

`skills/registry.v2.json`; `scripts/agent_adapter.py`; `evals/model-routing/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Lower-cost routing does not degrade critical defect recall or mandatory quality gates.
2. Missing pricing/usage data is reported unknown, not zero.
3. No extra agents are added merely to reach a role count; deployments retain bounded budgets.

## Traceability

quality budget; cost/latency optimisation; selective reasoning; avoid agent inflation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S07 — Escalate bounded disagreements rather than reviewing everything twice

**Milestone:** M6 · **Owner:** QA/runtime engineer

**Depends on:** R05, L08, S06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Use concrete discrepancies between deterministic evidence, generator claims and independent review to trigger a targeted second review. Record uncertainty, owner and escalation budget; unresolved conflict remains a candidate. Do not replace mandatory independent release review.

## Likely touchpoints

`scripts/agent_orchestrator.py`; `references/qa-requirements.json`; `evals/disagreement/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Conflicting timing/answer/representation judgements create a focused issue and evidence request.
2. A majority vote cannot overrule a demonstrable mathematical or provenance failure.
3. Agent-reported confidence alone cannot automatically waive checks.

## Traceability

agent disagreement trigger; selective redundancy; confidence-calibrated escalation; bounded second review.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S08 — Build an evidence-backed metrics view

**Milestone:** M6 · **Owner:** evaluation engineer

**Depends on:** A06, H03, H09, S06

**Decision basis:** retained_proposal · **Proposed enablement:** opt_in

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Summarise first-pass acceptance, schema validity, routing/owner accuracy, defect recall/false positives, repair outcomes, recurrence, runtime/critical path, tokens/cost where available and teacher-observed usability. Prioritise released useful packs over raw slide throughput.

## Likely touchpoints

`scripts/summarise_run_metrics.py`; `evals/reports/`; `teacher/developer reports`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Metrics distinguish automated, model-review and teacher-observed evidence.
2. Quality-adjusted cost uses real denominators and does not fabricate regression-free classroom outcomes.
3. Reports permit comparisons against the creator baseline and held-out cases.

## Traceability

agent eval dashboard; critical-path metrics; quality-adjusted cost; failure recurrence monitoring.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# S09 — Make sharing, backup and upgrades explicit and safe

**Milestone:** M6 · **Owner:** release/configuration engineer

**Depends on:** D06, D07, S01, S02, S03

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Document defaults, optional configuration, supported capabilities, private state location, export/reset, version changes and host requirements. Verify new dependencies in full and individual packages. Do not distribute private learning history or personal source documents.

## Likely touchpoints

`scripts/build_chatgpt_package.py`; `scripts/package_component_skills.py`; `docs/PROFILE_CALIBRATION.md`; `docs/COMPONENT-SKILL-INSTALLATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. A colleague can install, inspect defaults and configure a class without developer assumptions.
2. Creator settings survive upgrades and another teacher's changes.
3. Unsupported host/profile features remain labelled rather than promised.

## Traceability

shareable installation; teacher preference portability; safe export and reset; package upgrade isolation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---


# M7 — Close the evaluation, installation and classroom feedback loop

Graduate features using held-out evidence and actual installation, monitor outcomes and retain a rollback path.

**Exit gate:** The accepted package is identified in the target host, regressions are tracked, saved settings survive rollback/upgrade, and observed classroom outcomes inform the next bounded changes.

| ID | Work item | Dependencies |
|---|---|---|
| E01 | Run layered regression and integration tests continuously | A05, A06 |
| E02 | Execute counterfactual and stress-case evaluations | C15, H09, D05, E01 |
| E03 | Maintain approved gold examples and held-out cases | A04, A06 |
| E04 | Package, activate and verify each accepted milestone | D10, R07, C15, E01 |
| E05 | Pilot the creator workflow before broader sharing | C15, E04, A06 |
| E06 | Close the defect-to-regression improvement loop | E05, H03, S08 |
| E07 | Protect creator defaults across the full roadmap | D10, E01 |

# E01 — Run layered regression and integration tests continuously

**Milestone:** M7 · **Owner:** evaluation/release engineer

**Depends on:** A05, A06

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

From the first PR, run unit/schema/semantic-negative, integration, package/clean-install and relevant model/artefact tests. At final graduation run all layers against the pinned candidate. Do not substitute prose benchmark files for executed tests.

## Likely touchpoints

`.github/workflows/dlp-tests.yml`; `tests/`; `evals/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Each schema example and migration round-trip validates.
2. Direct finalisation bypasses, malformed/forged evidence and stale artefacts are negative tests.
3. Mathematics changes cover more than one concept family; unrelated component regressions are checked.

## Traceability

automated tests every PR; schemas plus semantic validation; clean-install tests; cross-concept regressions.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E02 — Execute counterfactual and stress-case evaluations

**Milestone:** M7 · **Owner:** evaluation engineer

**Depends on:** C15, H09, D05, E01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Perturb one input at a time: enrolment, profile, intent, available time, resource removal, supported/independent evidence, locked edits and expired overrides. Include unrelated-profile and no-history controls; avoid overfitting all prompts to the original mass lesson.

## Likely touchpoints

`evals/counterfactual/`; `evals/stress/`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Only relevant output decisions change under each perturbation.
2. Halved time does not halve every activity or remove dependencies blindly.
3. Missing equipment produces an authorised alternative or explicit blocker, not a fictitious resource.

## Traceability

counterfactual QA; metamorphic tests; robustness across resource/time/profile changes.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E03 — Maintain approved gold examples and held-out cases

**Milestone:** M7 · **Owner:** evaluation/pedagogy engineer

**Depends on:** A04, A06

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Curate teacher-approved exemplars for pacing, instruction, access and presentation across components and mature profiles. Separate visual-only exemplars, known-failure artefacts, training/calibration examples and held-out evaluation cases.

## Likely touchpoints

`examples/gold/`; `evals/held-out/`; `docs/implementation/EVALUATION.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. The flawed 105-slide deck cannot become the minimum quality floor.
2. Agents use exemplars for calibration without copying private or stale curriculum content.
3. Success on known fixtures is checked against held-out cases before broad release.

## Traceability

gold-standard lesson corpus; teacher-approved quality targets; held-out evals; visual-only versus pedagogical exemplar.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E04 — Package, activate and verify each accepted milestone

**Milestone:** M7 · **Owner:** release engineer

**Depends on:** D10, R07, C15, E01

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

For each milestone, identify the candidate commit, build/verify packages, install in a clean location, activate the exact version in the target host, and run a fresh-session smoke test. Keep the previous working release and compatible state backup.

## Likely touchpoints

`scripts/build_chatgpt_package.py`; `scripts/package_component_skills.py`; `RELEASE-PROVENANCE.json`; `target host`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Merged code, built package and active host are separate recorded states.
2. Installation manifest matches the tested commit; stale registered skills are detected.
3. Rollback is rehearsed without erasing teacher settings or altering historical evidence.

## Traceability

actual installation and activation; release provenance; upgrade/rollback; fresh-session smoke test.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E05 — Pilot the creator workflow before broader sharing

**Milestone:** M7 · **Owner:** teacher/evaluation engineer

**Depends on:** C15, E04, A06

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

At the M4 usable-pack milestone, independently review a representative creator-default pack, then teacher-approve a limited classroom pilot. Record actual preparation, pacing, task access, resource friction and needed corrections. Repeat pilot for later material changes.

## Likely touchpoints

`docs/implementation/PILOT.md`; `private teacher feedback`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. No candidate is used as a claimed approved pack without exact-artefact release evidence and teacher review.
2. Observed classroom results are distinguished from model predictions and unit-test success.
3. The creator's needs govern acceptance; support for additional profiles does not delay known classroom defect fixes.

## Traceability

creator-first classroom pilot; real-world feedback; teacher acceptance; observe usefulness.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E06 — Close the defect-to-regression improvement loop

**Milestone:** M7 · **Owner:** integrator/evaluation engineer

**Depends on:** E05, H03, S08

**Decision basis:** retained_proposal · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Classify every material review finding using stable failure categories, add a minimal reproducer and positive control, route to the owner, implement and rerun checks. Track recurrence by release. Replace vague 'make better' instructions with evidence-bearing changes.

## Likely touchpoints

`examples/benchmarks/`; `evals/reports/`; `CHANGELOG.md`; `issue backlog`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. PACING.OVERLOAD, ACCESS.TASK_NOT_PERSISTENT, DIFFERENTIATION.YEAR_PROXY, VISUAL.CLIPPING and other observed classes are traceable.
2. A resolved issue has a passing regression and deployed version reference.
3. A feature without measured benefit can remain disabled or be simplified without hiding its status.

## Traceability

failure taxonomy; continuous feedback to regression; recurrence tracking; evidence-based feature graduation.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

# E07 — Protect creator defaults across the full roadmap

**Milestone:** M7 · **Owner:** evaluation engineer

**Depends on:** D10, E01

**Decision basis:** teacher_confirmed · **Proposed enablement:** mandatory

**Current implementation:** unverified; audit first. This may extend or verify existing code rather than require a new subsystem.

## Scope

Run creator-default invariants on every shared change. Test behavioural properties, not identical LLM wording. Verify no repeated onboarding, no year-based placement, persistent override semantics, no cross-class leakage and no unintended assistant-suggestion promotion.

## Likely touchpoints

`evals/creator-defaults/`; `tests/test_profile_isolation.py`; `docs/implementation/DECISIONS.md`

*Paths are proposed touchpoints, not a guarantee that every named file exists.*

## Acceptance tests

1. Every additional profile, provider or workflow retains the creator's expected defaults.
2. A feature proposal becomes a permanent preference only through teacher instruction, not agent inference.
3. Final traceability review marks every issue verified/deployed, still experimental, superseded with reason, or blocked with explicit evidence.

## Traceability

default regression protection; complete roadmap traceability; creator priority over generic framework.

## Completion evidence

Attach the pinned commit/diff, actual regression results, independent review, schema/migration impact, package checks, and installation/activation evidence where relevant. Record remaining limitations explicitly. A declaration in Markdown, a mock agent PASS or a merged but uninstalled change is not sufficient.

---

