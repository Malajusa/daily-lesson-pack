# Maths Calibration and Responsive Progression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. For this particular change, native execution is recommended because the tasks share a small set of contracts; use the existing independent final-review workflow.

**Goal:** Generate worthwhile warm-up tiers and maths lessons that sustain learning when students understand immediately, with enforceable pedagogical review.

**Architecture:** Reuse component contracts, release-boundary JSON, canonical content, hash-bound reviews and package builders. Add precise teaching requirements and a small boundary-waiver correction. No new difficulty engine, evidence schema, settings store or competing QA service.

**Tech Stack:** Python, unittest, JSON contracts, Markdown skills, existing PPTX/rendering and package pipelines.

**Spec:** Embedded specification in section 1, derived from the teacher’s feedback and the investigation. It travels with this plan; no chat memory is required.

Revision 2 — 15 October 2026, Australia/Perth. Status: plan only; implementation not started. Checklist: [todo.md](todo.md). Intended repository destination at execution: `docs/superpowers/plans/2026-10-15-maths-calibration-and-progression.md`.

## Global Constraints

- “Warm-ups deliberately retrieve Year 3/4 foundations for the creator.” This existing decision describes emphasis, not a learner ceiling.
- “Enrolment year is not readiness.”
- “Never commit private classroom evidence or settings.”
- “Do not merge automatically or activate an installed skill as part of a source-only change.”
- Preserve five default Numeracy question/answer pairs, three separate ALL/MOST/SOME tasks and answer-slide-only WHY reasoning.
- Preserve predominantly Year 5 main teaching under existing creator defaults.
- Do not use speed, arbitrary percentages or slide counts as proxies for understanding.
- Scope is maths authoring, review, relevant release controls and packaging. Timetable, literacy, curriculum mapping and persistence remain outside this change.
- Newly authored examples remain candidates until reviewed; do not invent teacher approval or classroom outcomes.

## Review Focus

1. Vocal students answer quickly: collect independent evidence before advancing others. Task 4, R2.
2. Students solve the opening immediately: a substantial prepared route remains. Tasks 4/6, R1.
3. Students struggle or succeed with help: retain modelling and an independent recheck. Tasks 4/6, R3.
4. Inverse relationships cross tiers: reject trivial restatement without banning valid connections. Task 3, W1/W4.
5. A non-numeracy boundary is marked NA: reject the waiver while preserving legitimate unrelated NA decisions. Task 2.

---

## 1. Embedded specification and source baseline

**Calibration:** All stays accessible. Most retrieves worthwhile secure knowledge for the resolved class context. Some adds a specific demand in the same mathematical focus. Larger numbers or extra steps alone are insufficient. Warm-up tasks keep concise direct responses; do not introduce compulsory extended explanations on question slides.

**Responsive progression:** distinguish checking prerequisites from probing the intended learning. These may share one concise task if it exposes both. Prepare support, normal-teaching and advancement routes with exact task/slide destinations. Decisions use correctness, independence and application or explanation evidence, not speed alone.

**Review:** examine every warm-up pair and each maths block’s actual progression. Structural validity, review coverage, teaching quality and classroom effectiveness are separate claims.

Original deck SHA-256: `dc6a2685b1f08d2c06c0443b99a38adc3e0fb3d76592984ed27e3e9ad7d8246c`.

Observed evidence:
- Copies of slides 2–11 passed the standalone structural validator.
- Slide 6 pairs Most `6 × 8` with Some `48 ÷ 6`, a weak extension in the reported context.
- Slides 16–21 revisit the same L partitions. Notes allow 14 minutes to record partitions already explored.
- The teacher reports students identified the intended partitions immediately, leaving later slides without purpose.
- Maintained Week 1 planning already authorises complex figures and unfamiliar problems.
- Original generation/review records were unavailable; do not allege a particular pipeline or reviewer bypass.

Pinned repository baseline: `Malajusa/daily-lesson-pack` at `18aa531182e359e29833f63f5327d506c8451d4d`, inspected 15 October 2026. Recheck HEAD at execution and preserve later work. Read `AGENTS.md`, `docs/DEVELOPMENT.md` and `docs/implementation/DECISIONS.md` first. Installed copies and the attached handover are comparison outputs, not the development source.

Existing interfaces in `scripts/pack_evidence.py`:
- `release_boundary_rules(content)`: owner-specific boundary rules.
- `expected_checks(content, manifest, method)`: applicable instance checks.
- `requirements_digest(content)`: central/component contract hash.
- `audit_review(review_path, method, manifest_path, content_path, content, manifest, trace_path)`: results, bindings and receipt checks.

Source inspection found an NW.-prefix-only rejection of NA in audit_review. Task 2 must reproduce the non-numeracy gap before changing it; no executed failing test is claimed yet.

## 2. File map and data flow

| File | Responsibility |
| --- | --- |
| `examples/benchmarks/maths-demand-progression-regression.md` (new) | Sanitised cases and teaching rubric |
| `skills/dlp-numeracy-warmup/SKILL.md` | Tier authoring |
| `skills/dlp-numeracy-warmup/references/release-boundaries.json` | Numeracy boundaries |
| `skills/dlp-maths-lesson/SKILL.md` | Responsive routes and progression |
| `skills/dlp-maths-lesson/references/release-boundaries.json` (new) | Main-lesson boundaries |
| `references/universal-maths-instruction-canon.md` | Modelling versus legitimate transfer |
| `skills/dlp-pack-qa/SKILL.md` | Reviewer coverage and evidence |
| `scripts/pack_evidence.py` | Generic non-waivable boundaries |
| `tests/test_release_boundary_waivers.py` (new) | Waiver/compatibility tests |
| `tests/test_numeracy_warmup_release_boundaries.py` | Extend existing boundary inventory |
| `tests/test_maths_progression_release_boundaries.py` (new) | Main boundary expansion/packages |
| `tests/test_pack_evidence.py` | Existing release integration tests |
| `scripts/build_chatgpt_package.py`, `scripts/package_component_skills.py` | Distribution dependency closure |
| `CHANGELOG.md` | Actual changes and limits |

Keep student task text in canonical task fields. Use existing canonical briefing documents and notes for tier rationales and route tables; cite final bound task IDs/slides in reviews. Do not add an evidence schema just for this change. Instance-level reviewers must explicitly cover every pair/task; software cannot independently prove their educational judgement.

## 3. Ordered implementation tasks

### Task 1: Establish sanitised acceptance cases

**Files:** Create `examples/benchmarks/maths-demand-progression-regression.md`.  
**Inputs:** section 1 evidence and maintained weekly plan. **Output:** W1–W4 and R1–R3.

- [ ] Record mathematical examples, source slide numbers and teacher feedback separately from interpretation. Do not commit the original classroom deck or private evidence.
- [ ] Define W1: original fact-family pair is structurally valid but pedagogically weak; W2: adding small graph counts is insufficient Some challenge in the reported class; W3: every pair needs a specific Most/Some demand rationale; W4: a suitably demanding inverse/missing-number task can be valid.
- [ ] Define R1: immediate independent understanding; R2: mixed readiness including vocal fast responses; R3: initial difficulty followed by supported success.
- [ ] Add a rubric covering accessible entry, worthwhile Most, meaningful Some, answer leakage, added task demand, usable routes, task substance and complete answers.
- [ ] Compare the record with the deck and source plan. Preserve the previously observed structural PASS without calling it teaching approval.

**Accept:** self-contained sanitised cases with no invented attainment/provenance.  
**Verify:** manual evidence comparison and mathematical review; no keyword tests for prose.  
**Depends:** none. **Commit suggestion:** `docs: capture maths demand and progression regression`.

### Task 2: Protect every registered component boundary

**Files:** Create `tests/test_release_boundary_waivers.py`; modify `scripts/pack_evidence.py`.  
**Consumes:** existing boundary/review interfaces. **Produces:** unchanged audit_review signature with generic waiver protection.

- [ ] Write `test_registered_non_numeracy_boundary_rejects_na`: inject a temporary maths boundary, create otherwise valid synthetic review evidence, set its result to NA with a reason, and assert a non-waivable-boundary error.
- [ ] Add `test_registered_boundary_fail_and_omission_rejected`, `test_registered_boundary_pass_accepted`, `test_numeracy_na_remains_rejected`, `test_unrelated_central_na_remains_allowed` and `test_unscheduled_owner_adds_no_checks`.
- [ ] Run `python -m unittest discover -s tests -p 'test_release_boundary_waivers.py' -v`. Expected initial failure: the non-numeracy NA case is accepted; record other actual baseline results.
- [ ] Replace prefix-specific logic with registered boundary keys for the relevant owner/instance. Preserve TASK. applicability, hashing and receipt checks.
- [ ] Rerun the focused command and `python -m unittest discover -s tests -p 'test_pack_evidence.py' -v`; expect all pass.

**Accept:** applicable registered boundaries require PASS regardless of prefix; unrelated legitimate NA remains allowed. Synthetic receipts remain labelled test fixtures.  
**Depends:** Task 1. **Commit suggestion:** `fix: reject waivers for all component boundaries`.

### Task 3: Strengthen warm-up calibration

**Files:** Modify numeracy SKILL.md, numeracy release-boundaries.json, `tests/test_numeracy_warmup_release_boundaries.py` and Task 1 benchmark.  
**Consumes:** W1–W4. **Produces:** `NW.CALIBRATION`, `NW.DEMAND.PROGRESSION`, `NW.TIER.INDEPENDENCE`.

- [ ] Extend the existing BOUNDARY_IDS and expected_checks tests with the three IDs. Run its unittest module via discovery; expect missing-ID failures.
- [ ] Define boundary statements/evidence for class-context pitch, pair-by-pair added demand and avoiding a neighbouring tier supplying the answer.
- [ ] Require a concise briefing table per pair: focus/prior-learning basis, Most demand, Some’s added demand and answer-leakage check. Keep three student tasks.
- [ ] Add candidate arithmetic and graph replacements with exact answers/rationales. Preserve All, familiar taught knowledge and direct responses. Do not prohibit inverse relationships, small numbers or justified fluency practice generally.
- [ ] Run `python -m unittest discover -s tests -p 'test_numeracy_warmup_release_boundaries.py' -v`; expect pass.
- [ ] Teaching-review W1–W4 and replacements. Record reasons; software tests establish contract coverage, not difficulty.

**Accept:** all five pairs have defensible demand and retrieval purpose.  
**Depends:** Tasks 1–2. **Commit suggestion:** `feat: require defensible numeracy tier progression`.

### Task 4: Make progression respond to understanding

**Files:** Modify maths SKILL.md and universal maths canon; create maths release-boundaries.json and `tests/test_maths_progression_release_boundaries.py`; extend Task 1 benchmark.  
**Consumes:** R1–R3 and Task 2 protection. **Produces:** `MATHS.OPENING.DIAGNOSTIC`, `MATHS.TASK.PROGRESSION`, `MATHS.ADVANCE.ROUTE`, `MATHS.TASK.SUFFICIENCY`.

- [ ] Write failing expected_checks tests for these IDs across two scheduled maths blocks, plus an unrelated-owner exclusion case.
- [ ] Add a fail_closed component boundary contract and authoring rules. Require a route table with evidence, teacher action, destination task/slide and skipped models.
- [ ] For substantial tasks state added demand, estimated duration, hints and exact answers or valid-solution criteria. Repetition is allowed where deliberate practice is justified.
- [ ] Specify R1: bypass demonstrated work; R2: collect independent responses and use concurrent support/advance tasks; R3: model identified difficulty, then independently recheck.
- [ ] Prepare a synthetic stepped outline with vertices `(0,0),(8,0),(8,2),(5,2),(5,4),(3,4),(3,6),(0,6)`. Candidate advancement: partition into three rectangles in two ways; compare them. Further challenge: examine whether two rectangles can suffice. Verify all diagrams/solutions; do not require numerical area calculation.
- [ ] Clarify modelling: new concepts require teaching; unfamiliar applications of established ideas can be independent transfer or labelled extension. Do not demonstrate every problem-solving pathway in advance.
- [ ] Run `python -m unittest discover -s tests -p 'test_maths_progression_release_boundaries.py' -v`; expect functional tests pass. Walk through R1–R3 and repair infeasible routes.

**Accept:** immediate understanding leads to substantial prepared mathematics, while supported learners retain access. The teacher can follow routes without inventing missing tasks.  
**Depends:** Tasks 1–2. **Commit suggestion:** `feat: author maths progression from readiness evidence`.

### Task 5: Make pedagogical review decisive

**Files:** Modify QA SKILL.md, `tests/test_release_boundary_waivers.py`, `tests/test_pack_evidence.py` and Task 1 benchmark.  
**Consumes:** new boundaries and hash-bound semantic review. **Produces:** review instructions and release-regression evidence.

- [ ] Require reviewer observations to name every warm-up pair and examine each maths block’s opening, substantial tasks, challenge and exit; cite final bound tasks/slides.
- [ ] Require R1–R3 walkthroughs. Reject a generic assertion that differentiation exists; assess whether task substance fits its planned duration.
- [ ] Add `test_new_pedagogical_fail_blocks_review`, `test_missing_new_pedagogical_check_blocks_review` and `test_changed_boundary_invalidates_old_requirements_digest` using isolated fixture contracts.
- [ ] Extend the existing release integration pattern: supplied structural PASS reports cannot rescue a failed/missing pedagogical check.
- [ ] Run the two affected test modules; expect pass. Reuse component boundaries rather than duplicating the same checks in the central register.

**Accept:** named pedagogical failures change release eligibility. State the limit: software enforces review records/bindings; independent reviewers judge the teaching.  
**Depends:** Tasks 2–4. **Commit suggestion:** `test: enforce maths pedagogical review at release`.

### Task 6: Demonstrate improvement with controlled samples

**Outputs:** governed sample specs/reviews in the execution workspace; compact sanitised findings in the benchmark.  
**Consumes:** Tasks 3–5. **Produces:** warm-up comparison and two-concept progression evidence.

- [ ] Freeze the same synthetic context for baseline/revised comparisons, including taught-knowledge assumptions and available minutes. Do not invent real attainment.
- [ ] Generate the five-pair warm-up, responsive shape sequence and one addition-strategy sequence, rather than another full-day pack.
- [ ] Use canonical tasks, actual diagrams/answers, supported build/review paths and native reveals where needed.
- [ ] Give a fresh reviewer the criteria and artefacts without generator verdicts. Randomise before/after labels where practical.
- [ ] Record structural, pedagogical, rendered and playback results separately. Exercise R1–R3, independent transfer and answer completeness.
- [ ] Apply `examples/benchmarks/universal-maths-canon-regression.md` and `examples/benchmarks/year-profile-isolation-regression.md`. After repairs run `python -m unittest discover -s tests -v`.

**Accept:** original weaknesses fail teaching review and revised samples satisfy it across both concept families without removing support. Missing reviewer/playback evidence stays pending; two samples do not prove general classroom effectiveness.  
**Depends:** Task 5. **Commit suggestion:** `docs: record bounded maths teaching regression evidence`.

### Task 7: Package and hand off the exact candidate

**Files:** Modify both package builders, `tests/test_maths_progression_release_boundaries.py` and `CHANGELOG.md`. Update version/provenance only under existing release policy.  
**Consumes:** accepted source and Task 6 evidence. **Produces:** complete/standalone candidates and accurate implementation report.

- [ ] Add exact dependency entries for the new maths boundary contract and benchmark to both builders. Test complete and component ZIP inclusion using the existing numeracy package-test pattern.
- [ ] Run `python scripts/build_chatgpt_package.py --out dist/chatgpt/maths-progression-candidate.zip` and `python scripts/package_component_skills.py --out dist/component-skills`; expect successful archives.
- [ ] Rerun component boundary tests and the full unittest suite. Verify exact archives and unpacked roots with existing package/dependency services. Apply the memory-independent Wednesday benchmark because packaging changes.
- [ ] Inspect the installed-plugin/source diff. Preserve its renderer overlay and unrelated later changes; do not overwrite these with a newly built source package.
- [ ] Prepare a targeted plugin-update candidate using the supported plugin update workflow. Report unresolved overlay conflicts. A source ZIP is not an installed plugin.
- [ ] Report source commit, candidate hashes, checks, independent review, rollout/rollback and concrete blockers. Use focused commits and final independent branch review; no automatic merge or activation.
- [ ] Prepare three classroom questions for ordinary use: Were Most/Some worthwhile? Could students advance without waiting? What still required improvisation?

**Accept:** all new dependencies reach complete and affected component packages; source, candidate and installed states are distinguishable. Classroom confirmation is separate.  
**Depends:** Task 6. **Commit suggestion:** `build: distribute maths calibration and progression contracts`.

## 4. Checkpoints and rollout

After Tasks 1–3: baseline, boundary protection and tier calibration. After Tasks 4–5: actual support/advance routes and release eligibility. After Tasks 6–7: sample and package evidence.

Recommended execution: native implementation using superpowers:executing-plans, then independent final review under the repository’s /audit workflow. The planning self-review is performed by the planner, without subagent dispatch.

At execution use a feature branch or isolated worktree, preserve unrelated unfinished work, and reconcile any source drift from the pinned baseline before altering interfaces. No implementation, merge or installation is authorised merely by producing this revised plan.

Rollback: revert focused source commits and rebuild from the previous accepted commit. Roll back an installed plugin only if a real update occurred and its exact previous version was retained. Do not rewrite previously frozen reviews.

## 5. Definition of done and planner self-review

- [ ] W1–W4/R1–R3 map to authoring, semantic requirements and explicit verification.
- [ ] Structural checks remain intact; applicable missing/failed/waived boundaries block release.
- [ ] Five warm-up pairs and both concept-family lessons have actual review evidence.
- [ ] Support, transfer, challenge and answer integrity survive; no equation of speed with mastery.
- [ ] Full tests, relevant benchmarks, package checks and independent final review refer to the exact candidate.
- [ ] No private evidence is committed or installation, independence, playback or classroom success fabricated.

Revision 2 self-review completed: all three goals map to Tasks 3–5; all five Review Focus conditions have owners; source interfaces and builder flags were inspected; new IDs and files are specified; package overlays and privacy are addressed. Implementation tests, sample acceptance and classroom confirmation remain unexecuted.

