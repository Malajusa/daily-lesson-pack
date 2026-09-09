# Coding-agent start brief

Read `DECISIONS.md`, `WORKFLOW.md` and `BACKLOG.json` before editing. These files define the requested change; they do not claim that the current repository already implements it.

## Objective

Make Daily Lesson Pack serve its creator by default: predominantly Year 5 main direction, deliberate Year 3/4 foundational retrieval, evidence-based point-of-need teaching, no repeated setup and genuinely remembered scoped overrides. Preserve optional sharing/recalibration, canonical assembly and independent release integrity.

The creator's later instructions supersede earlier generic-profile and runtime-only-default proposals. Do not apply the old point-of-need patch or profile-driven v2 patch. The latter is syntactically corrupt.

## First working session

1. Identify the accepted branch/commit, dirty state and relevant open work. Do not overwrite uncommitted user changes.
2. Audit A01–A06. For each backlog capability, record absent/partial/implemented-unverified/verified/installed with file, function and test evidence. Distinguish source from the active installed package.
3. Inspect the actual host and durable-state capabilities. Reuse existing provider/renderer integrations if present; do not fabricate receipts, PASS results, student evidence or storage success.
4. Run the pinned repository's baseline test/package workflow and report actual failures. Do not make unrelated fixes silently.
5. Establish `AGENTS.md` and decision/traceability records with the smallest appropriate changes.
6. Select the first dependency-ready implementation issue, normally creator defaults/profile resolution followed by durable settings and removal of year-based pathways. Implement one complete vertical slice per PR, splitting only where each smaller slice has its own meaningful test.
7. Add a failing regression, make the smallest complete change, run tests, request independent review and record packaging/activation implications.

Do not stop at producing another generic design document when the required source and host capabilities are available. Do not attempt the whole roadmap in one branch. If a capability cannot be verified, record the concrete blocker and continue only with independent safe work.

## Required implementation rules

Use confirmed creator preferences automatically. Do not silently convert assistant suggestions such as exact slide limits, lesson style or heuristic weights into permanent teacher preferences.

Point-of-need migration includes Python check selection, generator contracts, QA requirements, schemas/producers/consumers, fixtures and packaging. Renaming year-labelled slides is insufficient.

Persistence uses explicit private, revisioned storage. Distinguish absent first-use settings from a read failure. A write failure must not produce 'saved'. Unit/date overrides expire to current underlying defaults; current sources still govern actual timetable/lesson facts.

No ordinary generator may mutate another component, persistent teacher settings or release state. Reviewers report defects; they do not repair content. Keep independent review and hash-bound release on all finalisation paths.

Use a versioned sidecar or explicit schema-version migration; do not add required fields without updating all producers/consumers and tests. Preserve accepted correct content and historical evidence.

Treat time, slide count, novelty, copying and friction measures appropriately: arithmetic/resource invariants can be deterministic; human response-time and learnability need independent review. Do not invent empirical thresholds.

Private records and credentials do not enter packages. Temporary working directories are not a security sandbox. The actual host is responsible for the relevant isolation and credentials.

## PR evidence template

**Issue and behaviour:** ID, user-visible change and explicit non-goals.

**Baseline:** accepted commit, controlling contracts/functions and baseline observations.

**Diff:** files changed and why this is the smallest complete change.

**Tests:** regression before/after, relevant negative cases, commands and actual results. A prose benchmark is not an executed test.

**Migration:** format versions, settings/history compatibility and rollback.

**Independent review:** reviewer findings and dispositions; the reviewer sees issue + diff + evidence, not the implementer's private reasoning.

**Packaging and deployment:** dependencies included, private data excluded, built manifest, activation steps and new-session smoke result when applicable.

**Limitations:** precisely what remains unverified or blocked.

**Status:** distinguish implemented, verified, packaged, installed and classroom-observed.

## Definition of success for the first increment

In the actual supported host, a clean or new session loads creator defaults without setup; an ongoing override persists after a verified write; a one-day override expires correctly; failed storage is honestly reported; and changing only synthetic enrolment year cannot change support/challenge recommendations. The active package is identified by manifest/commit.

A successful first increment does not establish that all teaching materials are classroom-ready. Follow M3/M4 planning and artefact gates before making that claim.
