# Daily Lesson Pack release-readiness design

Date: 9 September 2026, Australia/Perth.
Status: proposed release design. No implementation, merge, installation or release is claimed.
Repository: Malajusa/daily-lesson-pack.
Inspected main: c31f686fb75c3addbb47ccbd147ba6e11e488e55.

## Goal

Make the existing creator-first Daily Lesson Pack usable through a verified installed host, with correct and feasible materials, independent review of actual final artefacts, truthful release decisions and a tested rollback. Preserve the existing roadmap rather than replace it with a new product architecture.

## Scope

The first release target is the creator's existing Year 4/5 classroom workflow: predominantly Year 5 main teaching, deliberate Year 3/4 foundational retrieval, and evidence-based point-of-need support and challenge. Other profiles retain their actual documented maturity; a new profile is not calibrated by relabelling it. Authorised settings must persist privately and routine use must reuse valid configuration without repeated setup. Timetable and lesson facts still require authoritative sources.

These requirements are recorded in PR #11's decision ledger and implementation workflow. They are requirements to preserve, not proof that the functionality exists on main.

## Global constraints

- Reuse the existing orchestrator, component skills, canonical content model and complete-pack release authority.
- Keep curriculum/profile maturity separate from student attainment and task support.
- Do not restore compulsory Year 4/Year 5 task streams or permanent ability streams under new names.
- Preserve approved exemplars within their approved scope; visual approval does not certify all pedagogy.
- Ship confirmed non-sensitive defaults, not private classroom evidence, credentials or personal source documents.
- Use real private storage for authorised persistent settings; acknowledge a save only after it succeeds.
- Missing material facts, failed storage, missing providers and incomplete reviews must not become fabricated defaults or PASS evidence.
- Reviews must come from genuine independent executions and bind to the exact final artefacts.
- Every content repair invalidates applicable assembly/review evidence; only unchanged, independently validated evidence may be reused under an explicit dependency rule.
- The first operational recovery implementation may restart safely from a new run. Automatic checkpoint resume is not a prerequisite when restart, bounded retries, duplicate prevention and honest failure reporting meet the supported service contract.
- No new agents, provider expansion or large refactor unless an existing boundary cannot deliver a required capability.
- Preserve all 72 existing backlog items and their IDs. Deferral must be explicit; it is not cancellation.
- Distinguish implemented, verified, packaged, installed, activated and classroom-observed status.
- Do not claim unattended operation until an actual scheduler, failure path and delivery mechanism have been tested.

## Architecture

Current request -> creator defaults/private settings/valid sources -> frozen source-backed context -> feasible component plans -> existing specialist authoring -> component checks and independent Mathematics critic -> canonical assembly and full renders -> deterministic and independent semantic/visual/classroom-usability checks -> bounded owner-local repair -> existing final release audit -> verified delivery.

Development uses one integrator, bounded implementers, independent code review and independent output evaluation. These are work responsibilities, not additional installed production agents.

## Release boundaries

An assisted release requires all instructional, factual, material-access and evidence-integrity gates, exact-package clean-install validation, and human pilot acceptance. Assistance is not permission to skip QA. An unattended release adds tested scheduling, recoverable execution, duplicate prevention and failure notification. Additional year profiles and advanced history/efficiency features remain separately scoped.

## Evidence

The release record ties together source SHA, package digest, installed file manifest, host configuration fingerprint without secrets, schemas/QA versions, model/runtime identity where available, inputs, final artefact hashes, actual reviews, deterministic test results, installation/activation proof, pilot disposition and rollback evidence.

The evidence chain documents provenance; hashes and generated receipts alone do not prove that a model behaved correctly or that students learnt.
