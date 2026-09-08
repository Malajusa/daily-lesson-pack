# Daily Lesson Pack Build and Release Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository-owned Daily Lesson Pack build and release path mandatory for supported generation, so an ad-hoc PowerPoint cannot be promoted or described as classroom-ready without complete same-hash v3 evidence.

**Architecture:** Add a small fail-closed build runtime that validates resolved context and component ownership, stages a candidate artefact set, and delegates final certification to the existing `audit_release_bundle.py`. Keep pedagogical authoring in the component skills and canonical content records. Strengthen packaging, explicit panel ownership, semantic relationship metadata and regression coverage without changing Year 4/5 or Year 6 calibration.

**Tech Stack:** Python 3, `unittest`, `python-pptx`, existing `ContentSource`/pack-evidence/audit scripts, deterministic ZIP packaging.

**Spec:** `docs/superpowers/specs/2026-09-08-dlp-build-release-enforcement-design.md`

## Global constraints

- Existing `references/year-level-profiles/year-4-5.md` remains unchanged.
- Existing Year 6 pedagogical calibration remains unchanged.
- `scripts/audit_release_bundle.py` remains the sole classroom-ready release authority.
- Do not add deck-specific expected strings or one-off slide-count release scripts.
- The assembly/runtime layer must not become a new pedagogical author.
- Do not manufacture independent-review evidence when the host cannot provide it.
- Candidate artefacts may exist without independent review; released artefacts may not.

---

## Task 1: Add the fail-closed build runtime

**Files:**
- Create: `scripts/dlp_build_runtime.py`
- Create: `scripts/build_daily_pack.py`
- Create: `tests/test_build_runtime.py`
- Reference: `scripts/audit_pack_contract.py`
- Reference: `scripts/audit_release_bundle.py`
- Reference: `scripts/pack_evidence.py`

- [ ] **Step 1: Write failing runtime tests first**

Add tests covering:

1. a valid resolved context plus matching component record can be staged as a candidate;
2. an unresolved required context field blocks staging;
3. a missing scheduled component result blocks staging;
4. a component `FAIL` blocks staging;
5. a component/profile mismatch blocks staging;
6. no independent review evidence results in candidate-only status;
7. an existing candidate cannot be promoted by merely placing a hand-written `PASS` JSON beside it;
8. a deck mutated after the release audit cannot be promoted.

Run:

```bash
python -m unittest tests.test_build_runtime -v
```

Expected: FAIL because the runtime does not yet exist.

- [ ] **Step 2: Implement context and component validation helpers**

In `scripts/dlp_build_runtime.py`, implement focused pure helpers such as:

```python
def validate_request(request: dict) -> list[str]: ...
def validate_resolved_context(context: dict) -> list[str]: ...
def validate_component_record(context: dict, component_record: dict) -> list[str]: ...
```

Reuse the repository's schema-v2 expectations rather than inventing a parallel context model. At minimum verify:

- schema version and required context fields;
- no unresolved entries in required context;
- unique timetable instance IDs;
- every scheduled content instance has exactly one component result;
- owners and instance IDs match;
- all components use the active year profile;
- every component status is `PASS`;
- estimated minutes do not exceed the scheduled duration;
- a generation run ID exists.

- [ ] **Step 3: Implement candidate staging**

Add a function such as:

```python
def stage_candidate(
    run_root: Path,
    *,
    request_path: Path,
    context_path: Path,
    content_path: Path,
    component_record_path: Path,
    deck_path: Path,
    manifest_path: Path,
) -> dict: ...
```

It must:

- validate before copying;
- copy inputs into `build/<run-id>/candidate/`;
- preserve exact bytes and hashes;
- never write to `released/`;
- return an explicit `CANDIDATE` status and reasons if release evidence is absent.

- [ ] **Step 4: Implement release promotion through the existing authority only**

Add a promotion helper that:

1. requires the complete release-evidence paths expected by `audit_release_bundle.py`;
2. invokes that script against the candidate deck and candidate evidence;
3. requires process return code `0`;
4. reads the generated release report and requires `status == "PASS"`;
5. requires `artifact_sha256` to match the candidate deck at promotion time;
6. requires `manifest_sha256` to match the candidate manifest;
7. only then creates `released/pack.pptx` and `released/release.json`.

The runtime must never create semantic/visual review receipts itself.

- [ ] **Step 5: Add the supported CLI**

`scripts/build_daily_pack.py` should be a thin CLI over the runtime, with inputs for request/context/content/component record/deck/manifest/output root and optional release evidence. It should print one machine-readable status summary:

- `CANDIDATE` when staged but not independently released;
- `RELEASED` only after the final audit passes;
- non-zero exit on invalid inputs or failed release.

The CLI is orchestration/finalisation, not a replacement lesson generator.

- [ ] **Step 6: Run focused tests**

```bash
python -m unittest tests.test_build_runtime -v
```

Expected: PASS.

---

## Task 2: Strengthen canonical semantic relationship validation

**Files:**
- Modify: `scripts/pack_evidence.py`
- Modify: `tests/test_pack_evidence.py`
- Reference: `references/qa-workflow-v3.md`

- [ ] **Step 1: Add failing tests**

Add fixtures proving that canonical tasks fail validation when:

- a `why_prompt` exists without `why_answer`;
- a `why_answer` exists without a declared `why_concept` relationship;
- a shared-reading task declares paragraph/question/answer fields but omits the paragraph-to-question-to-answer relationship metadata required by the new runtime schema;
- a relationship references a missing field or another task ID.

Also add passing fixtures for correctly related tasks.

Run:

```bash
python -m unittest tests.test_pack_evidence -v
```

Expected: new tests FAIL.

- [ ] **Step 2: Implement relationship validation without breaking legacy unrelated tasks**

Extend `validate_content()` so relationship metadata is required when the corresponding specialised fields are present. Do not force generic tasks that have no `why_*` or shared-reading relationship fields to invent irrelevant metadata.

Use explicit, inspectable keys, for example:

```json
"relationships": {
  "why": {"prompt_field": "why_prompt", "answer_field": "why_answer", "concept": "multiplication_strategy"},
  "reading": {"paragraph_field": "paragraph", "question_field": "prompt", "answer_field": "answer"}
}
```

Validate references and non-empty concepts. This supports independent review; it does not substitute for semantic judgement.

- [ ] **Step 3: Run evidence tests**

```bash
python -m unittest tests.test_pack_evidence -v
```

Expected: PASS.

---

## Task 3: Make panel/text ownership deterministic for new DLP layouts

**Files:**
- Modify: `references/panel-containment-standard.md`
- Modify: `scripts/audit_panel_containment.py`
- Modify: `tests/test_hardening_contract.py`

- [ ] **Step 1: Add failing explicit-ownership tests**

Create synthetic slides covering:

- an explicitly owned text shape fully contained in its panel — PASS;
- explicitly owned text crossing its panel — FAIL;
- explicitly owned text referring to a missing panel — FAIL;
- a DLP panel-driven slide where a meaningful DLP-tagged content shape is unowned while explicit ownership mode is in use — FAIL.

- [ ] **Step 2: Define the naming contract**

Document a compact naming scheme such as:

- panel: `DLP:panel:<owner-id>`;
- text: `DLP:main|panel=<owner-id>`;
- subordinate roles: `DLP:instruction|panel=<owner-id>`, `DLP:why|panel=<owner-id>`, etc.

Keep existing suffix/spatial heuristics for legacy decks, but explicit ownership outranks heuristics.

- [ ] **Step 3: Implement deterministic ownership parsing**

Update the containment audit to:

- build an explicit panel map;
- validate every explicit owner reference;
- hard-fail explicit containment and padding violations;
- hard-fail missing explicit panels;
- keep render-level visual review mandatory.

- [ ] **Step 4: Run containment/hardening tests**

```bash
python -m unittest tests.test_hardening_contract -v
```

Expected: PASS.

---

## Task 4: Enforce the supported path in the skill and package

**Files:**
- Modify: `SKILL.md`
- Modify: `agents/openai.yaml`
- Modify: `scripts/build_chatgpt_package.py`
- Modify: `scripts/audit_package_dependencies.py`
- Modify: `tests/test_release_contract.py`

- [ ] **Step 1: Write failing packaging/contract tests**

Add assertions that:

- root package contains `scripts/build_daily_pack.py` and `scripts/dlp_build_runtime.py`;
- complete package validation fails if either required runtime file is removed;
- the orchestrator states that ad-hoc `python-pptx`, PptxGenJS, LibreOffice or equivalent generators are not authorised substitutes;
- the agent default prompt explicitly requires the repository-owned build/release path;
- a request for “PowerPoint as a Python script” is defined as a wrapper around the runtime, not permission to recreate the system.

- [ ] **Step 2: Add the anti-bypass section to `SKILL.md`**

Place it near the mandatory evidence workflow/request routing. Require:

- repository runtime for Daily Lesson Pack generation;
- component fallback when direct skill invocation is unavailable;
- candidate-only output when independent QA cannot run;
- classroom-ready wording only for same-hash final release PASS;
- no independent presentation generator as a substitute.

- [ ] **Step 3: Update ChatGPT agent metadata**

Change `agents/openai.yaml` default prompt to explicitly invoke the repository-owned build/release pipeline and prohibit an ad-hoc deck generator.

- [ ] **Step 4: Package the runtime**

Add the build runtime, its focused tests and the new regression benchmark to `ROOT_RUNTIME_FILES`. Include runtime files in `dlp-pack-qa` only where QA/package closure requires them; do not duplicate unnecessary authoring code into every component package.

- [ ] **Step 5: Strengthen package dependency validation**

For a complete package, require the two runtime files and verify that `scripts/dlp_build_runtime.py` can be imported from the installed tree. A missing or non-importable mandatory runtime makes the installation invalid.

- [ ] **Step 6: Run release-contract tests**

```bash
python -m unittest tests.test_release_contract -v
```

Expected: PASS.

---

## Task 5: Add the 8 September bypass regression and route it into QA

**Files:**
- Create: `examples/benchmarks/t3w8-tuesday-bypass-known-failure.md`
- Modify: `SKILL.md`
- Modify: `skills/dlp-pack-qa/SKILL.md`
- Modify: `scripts/build_chatgpt_package.py`
- Modify: `scripts/package_component_skills.py`
- Modify: `tests/test_release_contract.py`
- Modify: `tests/modular-routing-regressions.md`

- [ ] **Step 1: Create the benchmark**

Record that a candidate must be rejected for any of these defect classes:

- Morning Work content overlaps or escapes its panel;
- Morning Work pre-teaches the new Maths procedure rather than appropriate retrieval;
- Numeracy Q1–4 cease to be cumulative arithmetic retrieval because the day's new topic replaces them;
- meaningful warm-up task/answer text is below the 36 pt floor;
- a generic or concept-mismatched `Why` answer is reused;
- multiple-choice distractors are implausible;
- pronoun/reference wording has more than one defensible referent;
- a shared-reading model answer does not directly answer the matched question;
- a writing/maths lesson sub-focus is selected without authoritative runtime sequence evidence;
- timetable order is assembled without resolved provenance;
- a `.pptx` is delivered without complete v3 release evidence.

- [ ] **Step 2: Make the benchmark a QA/package input**

Add it wherever the T3W7 known-failure benchmark is currently routed for build/QA/package regression.

- [ ] **Step 3: Add routing regression wording**

Extend `tests/modular-routing-regressions.md` with an anti-bypass case: requesting a `.pptx` or Python generator must still use the repository runtime and may only return a candidate when release evidence is incomplete.

- [ ] **Step 4: Run release-contract tests**

```bash
python -m unittest tests.test_release_contract -v
```

Expected: PASS.

---

## Task 6: Add end-to-end release-boundary tests

**Files:**
- Modify: `tests/test_build_runtime.py`
- Modify: `tests/test_pack_evidence.py` where the existing complete-pack fixture is reusable

- [ ] **Step 1: Test incomplete ad-hoc candidates**

Verify no promotion for:

1. PPTX with no canonical/context/evidence files;
2. missing scheduled component;
3. unresolved required context;
4. missing semantic or visual review receipt;
5. missing manifest render coverage;
6. manifest deck different from candidate deck;
7. post-review deck mutation.

- [ ] **Step 2: Test the positive promotion path**

Use the existing synthetic complete-pack fixture or an equivalent controlled fixture. Mock only the external process boundary where necessary; still require that the runtime validates the generated release report's exact deck and manifest hashes before copying into `released/`.

- [ ] **Step 3: Run focused suites**

```bash
python -m unittest tests.test_build_runtime tests.test_pack_evidence -v
```

Expected: PASS.

---

## Task 7: Version and document the enforced runtime

**Files:**
- Modify: `VERSION`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `docs/DEVELOPMENT.md`
- Modify: `RELEASE-PROVENANCE.json`
- Modify: `tests/test_release_contract.py`
- Modify: `docs/superpowers/specs/2026-09-08-dlp-build-release-enforcement-design.md`

- [ ] **Step 1: Bump to 3.9.0**

Set `VERSION` to `3.9.0`.

- [ ] **Step 2: Update provenance**

Use the accepted pre-change main commit `01b5bd0f81e627e2ee3eb7bd84987ad6dcd90539` as the base lineage for this release and add the build/release enforcement work as a reconciled source/contribution. Preserve existing provenance rather than replacing it.

- [ ] **Step 3: Update docs**

Document:

```bash
python scripts/build_daily_pack.py ...
```

as the supported generation/finalisation path; explain candidate versus released artefacts and the independent-review boundary. Update README current-version wording and development workflow.

- [ ] **Step 4: Mark the approved design implemented only after verification**

Change the design status from `approved design awaiting implementation plan` to `implemented and verified` only after Task 8 succeeds.

- [ ] **Step 5: Update release-contract version tests**

Expect `3.9.0` and the new provenance base commit.

---

## Task 8: Full verification and package integrity

**Files:**
- Verify all modified files
- No new behavioural changes in this task

- [ ] **Step 1: Run the complete test suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests PASS.

- [ ] **Step 2: Build the complete ChatGPT package**

```bash
python scripts/build_chatgpt_package.py --out dist/chatgpt/daily-lesson-pack.zip
```

Expected: package builds successfully and includes the mandatory runtime.

- [ ] **Step 3: Validate a clean unpacked package**

Unpack to a temporary directory and run:

```bash
python scripts/audit_package_dependencies.py --skill-root <unpacked>/daily-lesson-pack
```

Expected: `PASS`.

Then deliberately remove `scripts/build_daily_pack.py` from a scratch copy and rerun the same validator.

Expected: `FAIL` identifying the missing mandatory runtime.

- [ ] **Step 4: Build component packages**

```bash
python scripts/package_component_skills.py
```

Expected: packages build successfully and `dlp-pack-qa` contains the new regression input where required.

- [ ] **Step 5: Inspect the branch diff**

Confirm:

- Year 4/5 and Year 6 profile files are unchanged;
- no pedagogical component rules were accidentally weakened;
- only the repository runtime can promote to `released/`;
- release still delegates to `audit_release_bundle.py`;
- no generated review receipt or fake PASS path exists.

- [ ] **Step 6: Request code review before integration**

Use the code-review workflow on the completed branch. Address verified defects, rerun the complete test/package verification, then prepare the branch for merge to `main`.
