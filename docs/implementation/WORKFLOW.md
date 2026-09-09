# Daily Lesson Pack — from brainstorming to an installed, tested skill

**Implementation workflow • 8 September 2026 • Creator-first**

**Status:** implementation handoff, not code changes, GitHub issues, a deployed package or a classroom release. The conversation is the requirements source. Public repository files were spot-checked; the source commit and actual host still need to be pinned and audited in M0.

## Start here

Use this document to control delivery. Use `DECISIONS.md` to resolve intent and supersessions, `BACKLOG.md` for readable issue scope and tests, `BACKLOG.json` for structured tracking, `TRACEABILITY.md` to find where an earlier idea went, and `CODING_AGENT_START.md` to begin in a repository-capable coding environment.

The backlog contains **72 bounded work items across eight milestones**. Multiple related brainstorming suggestions are consolidated into one implementation issue. Some capabilities already exist in source; audit them rather than rebuilding them. No item is claimed complete from the presence of a Markdown instruction.

The first useful increments are: (1) creator defaults and durable remembered overrides; (2) a creator-default pack with feasible planning and classroom-usability gates. Learning history, broader profiles, editing conveniences and advanced efficiency follow. They remain in scope; they do not delay the first usable delivery.

## 1. Product contract

The skill serves the creator first. It starts automatically with predominantly Year 5 main curriculum direction, deliberate Year 3/4 foundational retrieval and point-of-need differentiation. These are configurable defaults, not student attainment assumptions and not hard-coded universal year restrictions.

It remembers authorised changes using real private storage and the correct scope. Routine generation loads settings and valid sources without repeating setup. Other teachers may accept the defaults or recalibrate their own classrooms without changing the creator's configuration.

Non-sensitive preferences may ship. Student evidence, private school documents, credentials and identifying information do not ship.

Feature ideas that the teacher did not reject are in the backlog. Illustrative numbers and assistant recommendations are not automatically saved as permanent teacher preferences. For example, evaluate five Literacy sequences for the reviewed ten-minute block, but resolve the actual count from authorised policy and feasible activity timing.

The later creator-first requirement supersedes earlier briefs that made the creator select a preset or kept all preferences runtime-only. `DECISIONS.md` records the complete replacement ledger.

## 2. Establish what is real before editing

The earlier v2 patch fails a local Git syntax check with `error: corrupt patch at line 196`. `VALIDATION.json` records the command and file hash. Do not apply it or use its hand-counted diff as a starting point. Produce any future patch from actual tested Git changes.

The current repository already documents an opt-in v2 runtime, central QA coverage, host adapter contracts and canonical assembly/release boundaries [R1, R2]. It still contains runtime requirements for Year 4/Year 5 Mathematics pathways [R3]. Those are concrete integration points, not just wording to amend.

The current context contract separates maintained teacher context from year-level calibration [R4]. The required migration is to permit explicit automatically loaded persistent configuration without allowing hidden recall to supply factual lesson evidence.

During the pinned audit, classify each capability separately as:
`absent`, `partial`, `implemented-unverified`, `verified`, `installed`, or `observed-in-classroom`.

Keep implementation status distinct from workflow status. A pull request can be merged while the installed host still runs an older ZIP. The operator guide explicitly notes that source changes do not install or activate themselves [R2].

Do not infer the actual provider, durable storage, renderer, curriculum version or installed package from earlier assistant messages. Use the real environment. If a required host capability is missing, implement that integration in its owning issue; do not build months of prompt features on an unusable deployment path.

## 3. Target operating workflow

```text
Current request
      |
Load creator defaults + private classroom settings + valid planning sources
      |
Validate and persist authorised scoped changes
      |
Resolve curriculum/retrieval calibration, resources and optional learning state
      |
Freeze source-backed run-context snapshot
      |
Same specialists propose compact component plans
      |
Check elapsed time, teacher attention, resource access and learning dependencies
      |
Approve and freeze delivery plan
      |
Parallel specialised authoring with minimal relevant context
      |
Component validation + required independent Mathematics critic
      |
Canonical deck, teacher briefing and actual resources
      |
Deterministic checks + independent semantic/rendered/classroom review
      |
Batch defects -> owner-local repairs -> rebuild -> all applicable QA
      |
Existing repository release authority on exact candidate hashes
      |
Teacher uses accepted pack and optionally supplies brief feedback
      |
Teacher-confirmed events inform the next run; generation alone proves no learning
```

A run snapshot is immutable; students' instructional responses are not frozen. Later evidence creates a new snapshot. A short/no-tech route is part of the plan, not an improvised bypass of learning dependencies.

## 4. Delivery sequence and exit gates

### M0 — Establish the baseline (A01–A06)

**Outcome:** one trustworthy source of implementation truth.

Record the decisions, pin the accepted Git commit, inspect relevant open work, compare source/package/host identities, run the existing suite, inspect failed patches, and map controlling contracts. Verify the actual host can run the proposed agents, render canonical artefacts and persist private state.

Turn the review into minimal diagnostic fixtures. Preserve the distinction between reported timing, supplied artefact structure and unverified runtime provenance. The reported heading clipping must be checked in the relevant rendering environment; do not manufacture a root cause. Existing correct content must be protected.

Set up the issue board, coding-agent rules and baseline metrics. Curate initial good controls as well as failures. Record unknowns rather than guessing.

**Gate:** the capability inventory, host/storage decision, decision ledger, test baseline and regression fixtures exist. If tests already fail, attribute failures before unrelated fixes; do not report a clean baseline.

**Teacher involvement:** no repeated explanation of known preferences. Only a genuine missing deployment permission or source needs a targeted resolution.

### M1 — Make defaults and memory work (D01–D10)

**Outcome:** the installed skill starts as the creator wants and remembers authorised changes.

Ship one creator-default configuration automatically selected on clean use. Create a profile registry and resolver that separate main curriculum direction, retrieval emphasis, subject calibration, locale/jurisdiction coverage and point-of-need teaching. Do not turn supported coverage into a learner ceiling.

Implement private settings on one real host/backend first. Use field-specific precedence:
current explicit instruction, relevant temporary override, saved classroom preference, creator default. Current timetable and lesson facts still need valid sources; a preference cannot invent them.

Support ordinary-language standing, dated, unit and progression instructions. Acknowledge saving only after successful storage. Expiry returns to the latest underlying preference, not an old snapshot. Support show, undo, forget and reset. Distinguish first-use absence from a failed/corrupt store.

Remove year-labelled task pathways from prompts, Python checks, QA, schemas/examples and tests together. Use new requirement semantics and explicit retirement mapping, rather than changing a check's meaning while pretending old evidence certifies it.

Version the data change and migrate writers, readers, fixtures and packages together. Validate actual schemas, references, examples and round trips. Preserve private state through upgrades.

**Gate:** in a fresh installed session, creator defaults load with no preset selection; ongoing changes persist; one-day overrides expire correctly; another class is isolated; storage failure is honestly reported; point-of-need invariance holds.

**First useful delivery:** this increment can be installed before broader authoring changes. It is not proof of new classroom quality by itself.

### M2 — Complete reliable real-agent execution (R01–R07)

**Outcome:** verified execution, not a collection of plausible prompt files.

Audit and reuse the current registry, DAG, schema validation, invocation states, independent critic, semantic/visual review, deterministic provenance checks and bounded owner-local repairs. Complete gaps rather than create parallel competing frameworks.

Give each agent only the approved context and references it needs. Python owns instance identity, scheduling barriers, mutation scope validation, retries, hashes and release eligibility. Agent outputs are validated handoffs, not unconstrained authoritative prose.

Connect actual host invocations with real receipts and transcripts. An alternate run ID or YAML flag is not proof of independent review. The host's trust and security boundary must be explicit; logical write scopes are not an OS sandbox.

Use the component-only milestone first. Then connect actual canonical assembly and full renders with briefing and required resources. Synthetic assemblers and fake agents remain test fixtures.

Preserve complete applicable QA after content repair. A partial-content regeneration is not permission to reuse stale review. The release path must also protect direct finalisation calls, not just one orchestrator entry point.

**Gate:** a real representative candidate passes the intended execution path, while missing integration, stale evidence, wrong owners, omitted checks, exhausted attempts and release bypass cases fail closed.

### M3 — Plan a feasible lesson before full authoring (L01–L09)

**Outcome:** the plan determines the content, rather than content expansion determining the lesson.

Resolve the instructional intent and one clear learning claim. Identify must-learn, must-practise and optional enrichment. Use specialists in a compact planning pass; no new planning-agent swarm is needed.

The delivery-plan contract records activities, durations, dependencies, responses, teacher attention, resources, access, reveal conditions and essential/optional status. Count setup, reading/thinking, responses, discussion, feedback, transitions and contingency. Model elapsed concurrent time correctly.

Specify point-of-need checks, targeted support, rechecks, fading and connected challenge. No supplied learning history means conditional guidance, not fabricated placements. A time-bounded prerequisite goal may be appropriate when the shared task remains inaccessible.

Record equipment quantities, printing, copying and switching friction. Agree compact Reading/Writing transfer targets before parallel authoring. Preserve Numeracy as cumulative retrieval rather than forcing every item to preview the main Mathematics lesson.

Build dependency-safe shorter and no-tech routes. When time cannot support the essential goal, narrow scope explicitly. Do not divide every duration by two or remove the model while keeping unsupported independent practice.

Keep plan decisions and material uncertainty source-backed. Lean, standard, high-support and relief styles are configurable delivery choices, not changes to accuracy or readiness rules.

**Gate:** full authoring is blocked until the plan is approved. The assembled tasks must match it; additional demands require revalidation. Schedule arithmetic is checked by code; task-duration plausibility still needs independent judgement.

### M4 — Deliver classroom-usable materials (C01–C15)

**Outcome:** a creator-default pack that addresses the reviewed failure classes.

Generate canonical student display, teacher guidance and actual resources together. Use stable task/document IDs so briefing, slides, answers and sheets cannot drift. Every independent activity must retain access to needed instructions and data.

Resolve warm-up counts once from time and policy. Review the ten-minute case with five purposeful sequences rather than automatically demanding ten topics. Improve Morning Work load where the activity schedule requires it. Do not suppress deliberate foundational retrieval merely because it is not today's main topic.

For Mathematics, use purposeful representations, authentic instruments when appropriate, approximate readings, suitable units and feasible hands-on resources. Preserve existing correct conceptual explanations. Implement controlled variation and example-boundary checks so unfamiliar notation, language or arithmetic does not introduce unplanned demands. Apply cross-concept tests.

Improve Reading/Writing transfer and text dependency while preserving the strong writing sequence. Protect independent drafting with explicit hold points. Design responses and exits that reveal understanding and support conditions, not just participation or completion.

Control authoring expansion with coverage-based stopping rules. Review novelty, cognitive switching and extraneous difficulty as task-specific issues, not arbitrary universal scores.

Fix target-environment rendering, effective readability and accessibility. Add purposeful navigation and consolidated practice without decorative bloat. Formalise intended prompt/attempt/check/reveal/feedback states while acknowledging static PowerPoint cannot enforce elapsed thinking time.

Run redundancy checks and owner-approved compression; semantic changes reopen appropriate planning and QA. Produce the minimal board/briefing contingency without duplicating a printed deck.

Extend central QA across correctness, learnability, deliverability, accessibility and operability. The activity walkthrough asks what teacher and learners do, what each can see, what resources are available and whether time is credible. A good mathematical answer is not a complete classroom-readiness check.

**Gate:** exact final artefacts, plan, resources and reviews satisfy repository release requirements, then the teacher reviews the pack for a limited pilot. Report any unresolved rendering or source uncertainty, not invented fixes.

**Second useful delivery:** the first creator-default classroom-usability upgrade. Do not wait for every advanced history or sharing feature to reach this point.

### M5 — Learn from teacher-confirmed evidence (H01–H09)

**Outcome:** better successive-day planning without an obligatory student database.

Introduce optional instructional state separate from preferences. Record planned, taught, attempted, assisted, independent and transfer evidence distinctly. Each observation has a source, skill/task, date and assistance condition.

Accept cheap post-lesson feedback for timing, completion, difficulty and continuing misconceptions. Append events; allow corrections without rewriting history. A generated pack cannot mark itself taught or declare student mastery.

Add retrieval history and a configurable selection policy using recency, outcomes, importance, relevance and interference. Spacing/interleaving intervals and weights are proposals to evaluate, not universal scientific constants. Missing history must not prevent a sensible cold start.

Maintain misconception evidence, a small validated concept dependency graph and cautious rules for maintaining or fading support. Start with actually covered concept families rather than constructing an enormous assumed curriculum graph.

Expose why items, supports or omissions exist using sources and decision records—not hidden chain of thought. Run multi-day synthetic sequences, including guided-to-independent success, transfer, missed lessons, conflicts and enrolment-only changes.

**Gate:** the system responds appropriately to new evidence and keeps uncertainty visible. It does not infer global ability, numerical ZPD, or independent mastery from assisted performance. No-history use remains supported.

### M6 — Improve editing, sharing and efficiency (S01–S09)

**Outcome:** the remaining portability and productivity features, without eroding creator-first use.

Separate verified curriculum-jurisdiction mapping from universal concepts, and locale conventions from pedagogy. Add other profiles as candidates with real per-domain coverage evidence. Optional recalibration and a small control interface are for convenience, not forced onboarding.

Preserve teacher edits using stable content IDs and explicit locks. Detect conflicts with changed sources or answers; locks cannot exempt incorrect content from QA. Provide partial regeneration that preserves untouched components but rebuilds and reviews the changed pack correctly.

Introduce quality-budget routing only after baseline evaluations exist. Use deterministic code where appropriate, suitable authoring models and required independent judgement. Escalate concrete disagreements with bounded extra review, not universal duplication or majority voting over facts.

Present metrics for routing, schema validity, acceptance, defects, false positives, repairs, recurrence, latency and costs when known. Connect them to teacher-observed usefulness rather than raw generation throughput.

**Gate:** new profiles, models, edits, overrides and sharing pathways are demonstrably isolated. Unsupported capabilities remain labelled. Efficiency changes have measured evidence and can remain opt-in if benefit is unclear.

### M7 — Evaluate, install, observe and improve (E01–E07)

**Outcome:** accepted work actually runs in the teacher's environment and has a feedback loop.

This is a cross-cutting track, not testing postponed until the end. E01, E03 and E07 begin early; E04/E05 are repeated at useful milestone checkpoints.

Maintain unit, schema, semantic, integration, negative/bypass, package, clean-install, model and artefact tests. Use paired counterfactuals that change only enrolment, intent, time, resources, profile, evidence or override scope.

Keep approved exemplars separate from known failures and held-out tests. Compare against the creator baseline, not identical LLM phrasing. Do not claim observed learning gains from synthetic pass rates.

Package the exact accepted commit, verify complete and component dependency closure, install it in a clean location, activate the exact version in the host and run a new-session smoke test. Record the active manifest and preserve a tested rollback path with state compatibility.

Pilot the creator workflow and collect brief actual observations. Convert each material failure into an owned defect and minimal executable regression with a passing control. Track recurrence by release.

**Gate:** each feature is verified and activated, still experimental with stated evidence limits, or explicitly blocked/superseded. None is silently forgotten because the roadmap is long.

## 5. How to run work with coding agents

Use a board with:
`Backlog -> Baseline classified -> Ready -> Implementing -> Independent review -> Packaged/installed trial -> Accepted`.
Track a separate blocked flag with the exact unmet dependency. Do not label a source-only change deployed.

One integrator owns the decision ledger and shared contracts. One implementing agent owns one bounded issue in an isolated worktree. A separate reviewer sees the issue, diff, test outputs and relevant source—not the implementer's private reasoning. An evaluation role checks the resulting behaviour and artefacts. Roles may run serially if the host does not provide multiple actual agents.

The issue cycle is:
1. Read decisions; inspect current controlling files and dependency statuses.
2. Write a failing regression or explicit observable baseline before the behavioural change.
3. Implement the smallest complete vertical slice: source data, schema, producer, consumer, instructions, audit, fixtures and packaging as applicable.
4. Run relevant tests and the existing repository CI/package checks. Record actual outputs and failures.
5. Independent review checks contradictions, scope, source authority, data safety and bypass paths.
6. Integrator merges only after required evidence; rebuild from the accepted state and activate in the real host.
7. Confirm observed behaviour and update the issue with commit/package/test/install evidence.

Tests and docs are part of the same work, not follow-up promises. Never silently weaken an audit to make a new format pass.

Parallelism is useful after shared contracts settle. Profile/default work and known-failure fixtures can proceed on separate paths. Do not have several agents edit the same context schema, registry or QA registry simultaneously. Rendering, English coherence and state scheduling can run in parallel once their contracts and dependencies are merged. The JSON backlog encodes issue-level dependencies; a validation checks that they exist and are acyclic.

## 6. Definition of done

A work item is complete only when all applicable conditions are met:

- The teacher-visible behaviour and non-goals are explicit.
- Current source/contract ownership is identified and conflicting rules are deliberately reconciled.
- Runtime code actually consumes the new configuration/plan/evidence; a JSON example alone is insufficient.
- Schemas, example values, references, producers, consumers, migrations and fixtures agree.
- Positive and negative tests run, with actual outputs recorded.
- Independent review checks the result, not a self-certified assertion.
- Required files are in complete and affected component packages; private data is not.
- A new-session test uses the installed target version where the change affects runtime.
- Feature changes include rollback and settings/history compatibility.
- A teaching-material claim has the required exact-artefact review evidence; classroom benefit is labelled observed only after use.

Repository commands currently present in CI include [R6]:

```sh
python -m unittest discover -s tests -v
python scripts/build_chatgpt_package.py --out dist/chatgpt/daily-lesson-pack.zip
python scripts/package_component_skills.py --out dist/component-skills
```

These are not the whole release gate. Use the pinned CI's unpacked dependency audits, target-host tests and independent final-material checks too. Do not replace the repository workflow with an ad-hoc renderer.

## 7. Acceptance scenarios that span the whole product

| Scenario | Required behaviour |
|---|---|
| Creator uses a new installation. | Confirmed defaults load automatically without preset activation. |
| 'Use five from now on', followed by a new session. | The ongoing setting persists after a verified write. |
| 'Use three tomorrow.' | The dated exception affects the requested local lesson date only. |
| A default changes while an exception is active. | Expiry reveals the current default, not an obsolete snapshot. |
| Same task evidence, different enrolment year. | Instructional recommendation does not change solely because of enrolment. |
| No learner history. | Conditional diagnostics are available; no student placement is invented. |
| Reduced time. | Optional work is removed safely or essential scope is revised explicitly. |
| Missing resource or conflicting single display. | An actual alternative is supplied or the conflict remains unresolved. |
| Teacher edits only Mathematics. | Unrelated accepted content/locks are preserved; changed artefacts receive fresh applicable QA. |
| Supported success then independent success across days. | Support decisions respond to the evidence conditions without manufactured mastery. |
| Another teacher configures a new profile. | Creator defaults/private state remain unchanged. |
| Upgrade, storage failure or rollback. | Settings remain coherent; no false 'saved' or silent reset. |
| Content or plan changes after review. | Stale evidence cannot authorise release. |

## 8. Track completion without measuring the wrong thing

Track coverage of decisions and testable retained features, plus teacher-observed usefulness. Suggested metric families are implementation coverage, first-pass agent acceptance, wrong-owner/schema errors, defect recall and false positives, repair success, recurrence, teacher preparation/corrections, pacing and access friction, and measured execution cost/latency.

Do not equate fewer slides with better learning, a passed unit suite with classroom readiness, or a reviewer score with an observed learning outcome. Where the host does not supply usage/cost information, record unknown rather than zero.

A feature can be implemented but kept opt-in while evaluation continues. That is different from silently dropping it. The backlog records decision basis and proposed enablement separately.

## 9. Immediate next action

Open the accepted repository in an authenticated coding environment and provide this bundle. Begin with `CODING_AGENT_START.md`: reconcile decisions, pin the source, inventory real capabilities, verify the host/storage path and run baseline tests. Then select the first dependency-ready issue and deliver one complete slice.

Do not request another generic architecture proposal. Ask for a capability inventory with file/function/test evidence and the first reviewable implementation PR. Do not apply the earlier patch or attempt all 72 issues in one commit.

## Sources and evidence limits

The conversation is the authority for desired behaviour, not a claim about current implementation. The following public main-branch files were read on 8 September 2026. They are not a pinned checkout; M0 must record the accepted commit before coding. No live repository test suite, host generation or GitHub modification was performed while preparing this workflow.

- **[R1] Root skill** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/SKILL.md`. Documents opt-in v2 orchestration, source-frozen context and the repository-owned release boundary.
- **[R2] Agent orchestration operator guide** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/docs/AGENT-ORCHESTRATION.md`. Distinguishes logical roles from installed providers; requires host execution and canonical assembly. Source changes do not activate installed copies.
- **[R3] Protocol implementation** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/scripts/agent_protocol.py`. required_component_checks still adds MATHS.YEAR4.PATHWAY and MATHS.YEAR5.PATHWAY for the mixed profile.
- **[R4] Runtime context contract** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/references/shared-class-context-contract.md`. Allows explicitly selected maintained context and excludes private student data from portable contracts; current memory rules need deliberate migration for saved configuration.
- **[R5] Development workflow** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/docs/DEVELOPMENT.md`. Uses latest teacher decisions, smallest complete changes, regressions, package checks and clean-context verification.
- **[R6] CI workflow** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/.github/workflows/dlp-tests.yml`. Runs unittest discovery, complete/component package builds and unpacked dependency audits.
- **[R7] Complete-package builder** — `https://raw.githubusercontent.com/Malajusa/daily-lesson-pack/main/scripts/build_chatgpt_package.py`. Enumerates profile/shared dependencies; new calibration files need packaging integration, not just repository presence.

Local evidence: `VALIDATION.json` records a fresh syntax check of the previous v2 patch and validation of this backlog's dependency graph. It is not a skill-runtime or classroom-release certificate.
