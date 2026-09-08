# Daily Lesson Pack Build and Release Enforcement Design

Date: 2026-09-08
Status: approved design awaiting implementation plan
Branch: `enforce-dlp-build-release-pipeline-20260908`

## Problem

The repository defines strong component contracts and a fail-closed v3 QA/release model, but it does not force every Daily Lesson Pack generation request through one executable build path. An agent can still bypass the orchestrator, write an ad-hoc PowerPoint generator, and return the resulting `.pptx` without producing the context, canonical content, component evidence, renders, independent reviews or final release record required by the repository.

The 2026-09-08 Tuesday pack exposed this gap. The deck contained visible Morning Work overflow, undersized warm-up text, a numeracy warm-up that became mass pre-teaching rather than cumulative retrieval, mismatched `Why` explanations, weak or ambiguous literacy items, and a shared-reading model answer that did not directly answer its question. These defects were already prohibited by existing contracts; the build path simply failed to enforce those contracts.

## Goal

Make repository bypasses structurally difficult and make release of a bypassed Daily Lesson Pack impossible through the supported skill/runtime.

A Daily Lesson Pack must not be considered deliverable merely because a PowerPoint file exists. The exact deck must pass the repository-owned build and release pipeline before it can be presented as classroom-ready.

## Non-goals

- Do not redesign the approved visual exemplar.
- Do not change the established Year 4/5 instructional pitch.
- Do not change Year 6 calibration except where shared build infrastructure applies without altering pedagogy.
- Do not replace existing component contracts or `qa-workflow-v3.md`; enforce them.
- Do not introduce deck-specific expected strings or slide-count hacks as release gates.
- Do not make the assembler a new source of pedagogical content.

## Architecture

### 1. One supported build entry point

Add `scripts/build_daily_pack.py` as the supported executable entry point for Daily Lesson Pack generation.

Its responsibility is orchestration, not authoring. It must:

1. load and validate a structured request;
2. resolve runtime context and the active year profile;
3. produce a canonical resolved context record;
4. require scheduled component payloads from the registered component owners;
5. produce canonical `content.json` using the v3 content-source schema;
6. assemble the PowerPoint only from canonical content/component payloads;
7. render every slide;
8. build the manifest and bindings;
9. run deterministic audits;
10. require independent semantic and visual review evidence when a release is requested;
11. invoke `audit_release_bundle.py` for the exact final deck;
12. copy/promote only a passing artefact into the released output set.

The build entry point must fail closed when required context, component content, evidence or release dependencies are missing.

### 2. Candidate versus released artefacts

Use an explicit output lifecycle:

```text
build/<run-id>/
  candidate/
    pack.pptx
    context.json
    content.json
    component-record.json
    manifest.json
    renders/
    reports/
  released/
    pack.pptx
    release.json
```

The candidate PowerPoint is not classroom-ready.

Only a successful final release audit may populate `released/`. The release record must bind to the exact deck SHA-256 and manifest SHA-256.

If independent review cannot be executed, the workflow may retain a candidate but must not promote it or describe it as released/classroom-ready.

### 3. Structured request and context resolution

Add a repository-owned request/context contract, implemented as JSON validation helpers under `scripts/` or a focused runtime module.

The resolved context must contain at minimum:

- requested date/day;
- active year profile and profile path/status;
- timetable instances in teaching order;
- current user-supplied/runtime sources and provenance;
- explicit overrides;
- current Maths focus/sequence;
- current writing genre/focus/sequence;
- reading focus/text type where applicable;
- warm-up counts;
- output-role requirements;
- unresolved fields.

Required unresolved fields block release. The resolver must not silently fill them from chat memory.

### 4. Component-owned canonical payloads

Each scheduled content component must provide a structured payload tied to its `instance_id` and registered owner.

The assembler must not invent or rewrite pedagogical content. It may only consume validated component/canonical fields.

At minimum each component payload records:

- `instance_id`;
- `owner`;
- active year profile;
- component status;
- canonical task IDs;
- prompts/models/answers/explanations required for assembly;
- task operation metadata;
- demand metadata;
- component acceptance evidence required by the v3 workflow.

For choice tasks, canonical data must retain plausible misconception and rejection-reason metadata. For revision tasks, preserve before/after propositions as already required by v3.

### 5. Content-source-only assembly

The builder/assembler must import `ContentSource` from `scripts/content_source.py` and populate final artefacts from canonical fields.

Direct hard-coded lesson text in the assembly layer is prohibited. Layout helpers may contain structural labels where authorised, but student task/model/answer text must come from canonical records.

Requests such as “create the PowerPoint as a Python script” change the requested interface, not the Daily Lesson Pack workflow. Any produced Python entry script must call the repository runtime rather than recreate lesson generation and QA in an independent script.

### 6. Explicit layout ownership

Strengthen panel-containment evidence by making panel/text relationships explicit in generated PowerPoint shape metadata/naming.

Meaningful panel-contained text must have an identifiable owning panel. The containment audit should prefer deterministic owner relationships and fail when required student-facing text is unowned on panel-driven slide templates.

The existing geometry audit remains a screening layer; rendered visual review remains mandatory.

### 7. Semantic relationship metadata

Canonical task records should preserve relationships needed to review alignment, including:

- question ↔ answer;
- `Why` prompt ↔ `Why` answer and concept;
- reminder ↔ question operation;
- model ↔ independent task target;
- shared-reading paragraph ↔ question ↔ model answer.

This does not replace independent semantic review. It gives the reviewer and deterministic audits stronger evidence and prevents generic explanations from being reused across unrelated tasks without detection.

### 8. Anti-bypass skill contract

Update the root `SKILL.md` with a mandatory supported-generation-path section:

- Daily Lesson Pack generation must use the repository-owned build runtime.
- An ad-hoc `python-pptx`, PptxGenJS, LibreOffice or other independent presentation generator is not an authorised substitute.
- Direct cross-skill invocation failure requires the repository fallback/component contracts, not generic generation.
- A `.pptx` may be returned as classroom-ready only when the current release record passes for that exact deck hash.
- A candidate may be supplied only when clearly labelled as unreleased/review-pending.

Update `agents/openai.yaml` so the default prompt explicitly instructs the agent to use the repository-owned build and release pipeline and not substitute an ad-hoc presentation generator.

### 9. Package enforcement

Update `scripts/build_chatgpt_package.py` to include the new runtime/build files in the root installation package and, where necessary, the QA component package.

Update `scripts/audit_package_dependencies.py` so a complete Daily Lesson Pack installation fails validation when the mandatory build runtime is absent or non-importable.

The packaged skill must include enough executable runtime to follow the supported path rather than only describing it.

## Release gates

The final release decision remains owned by `scripts/audit_release_bundle.py`.

The supported build entry point must treat that command as mandatory for release and must not duplicate a weaker parallel release decision.

A released deck requires, for the exact artefact hash:

- resolved context record;
- canonical `content.json`;
- component record;
- manifest and bindings;
- complete renders;
- deterministic contract/year-profile/typography/containment/visual-exemplar audits;
- independent semantic review + execution trace;
- independent rendered visual review + execution trace;
- final `audit_release_bundle.py` PASS.

Any mutation after review invalidates the release evidence and requires rebuilding/re-reviewing.

## Regression protection

Add a new known-failure benchmark based on the 2026-09-08 bypassed Tuesday output. It should require rejection of at least these defect classes:

- Morning Work text overlapping or escaping its panel;
- Morning Work pre-teaching a new Maths procedure rather than remaining appropriate retrieval;
- numeracy warm-up Questions 1–4 being replaced by the new lesson topic rather than cumulative arithmetic retrieval;
- meaningful warm-up prompt/answer text below the required 36 pt floor;
- generic or concept-mismatched `Why` answers;
- implausible multiple-choice distractors;
- ambiguous pronoun/reference questions;
- shared-reading model answers that do not directly answer the matched question;
- lesson sub-focus/sequence selected without authoritative runtime evidence;
- deck assembly without resolved timetable provenance;
- delivery without complete v3 release evidence.

Add end-to-end tests proving that release fails when:

1. a PPTX exists without canonical/context/evidence files;
2. one scheduled component is missing or failed;
3. required context remains unresolved;
4. independent review receipts are missing;
5. the deck changes after review;
6. the manifest deck differs from the audited deck;
7. the build runtime is absent from a packaged skill;
8. an ad-hoc candidate has no successful release record.

## Implementation boundaries

The first implementation should focus on enforcing the supported path and release boundary, not on creating another large pedagogical engine.

Reuse existing contracts and scripts wherever possible:

- `scripts/content_source.py`;
- `scripts/pack_evidence.py`;
- `scripts/audit_pack_contract.py`;
- `scripts/audit_year_profile_context.py`;
- `scripts/audit_slide_typography.py`;
- `scripts/audit_panel_containment.py`;
- `scripts/audit_visual_exemplar.py`;
- `scripts/audit_release_bundle.py`;
- component registry and component `SKILL.md` contracts.

Where the ChatGPT host cannot actually execute an independent reviewer, the runtime must terminate at candidate status rather than manufacture review evidence.

## Success criteria

The change is complete when:

1. there is one documented and packaged supported Daily Lesson Pack build command;
2. the supported command cannot promote a pack to released status without the complete v3 release evidence;
3. the skill explicitly prohibits ad-hoc presentation generators as a substitute for the supported runtime;
4. the ChatGPT package contains and validates the runtime;
5. candidate and released outputs are distinct;
6. the 2026-09-08 failure classes are represented in regression coverage;
7. existing Year 4/5 calibration and component contracts remain intact;
8. repository tests pass, including deliberately faulty release fixtures.
