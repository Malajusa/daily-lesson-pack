# Repo-Owned Visual Renderer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository deterministically generate the Daily Lesson Pack PPTX from canonical content records, enforce component-aware composition during generation, and block release of externally assembled decks by default.

**Architecture:** Add a typed render-model compiler between canonical content and PowerPoint geometry, then render that model through a small deterministic family of component-aware layouts. Emit a render manifest that binds slide roles, layout IDs, source block IDs and shape IDs to the generated deck; use that manifest in a new visual-composition audit and in release provenance so only repo-rendered decks are release-eligible.

**Tech Stack:** Python 3, `python-pptx`, `jsonschema`, existing repository audit/runtime modules, `pytest`/`unittest`-style tests already used by the repository.

**Spec:** `docs/superpowers/specs/2026-09-15-repo-owned-visual-renderer-design.md`

## Global Constraints

- Preserve the existing content ownership boundary: the renderer is a presentation compiler, not a pedagogy generator.
- Use a 16:9 canvas, full-height role-coloured left rail, Trebuchet MS, compact uppercase eyebrow, semantic role colours, and the approved visual exemplar grammar.
- Teacher-only directions must never appear on projected slides.
- Ordinary slides must not repeat date/term/week metadata unless navigation materially requires it.
- Reflow, merge, split and shorten-before-shrink must precede font reduction.
- Shared-reading/model paragraphs must use constrained measure and split rather than stretch full-width.
- Short answers and expressions must use the largest sensible type for their role.
- Morning Work with both Maths and Literacy must use broad grouped areas rather than a stacked generic-card treatment.
- Success criteria must render as scan-friendly checklist rows/groups rather than one undifferentiated bold block.
- Unsupported/ambiguous render content must fail closed with component, instance, source block and attempted-layout context.
- Existing typography, containment, exemplar, semantic, year-profile, source-hash and independent-review evidence remains mandatory.
- Repo-rendered decks are release-eligible only when all release evidence passes; externally assembled decks remain candidate-only.
- No pixel-perfect visual snapshots; use semantic/layout metadata and structural thresholds to avoid font-metric brittleness.

## File Structure

### New production files

- `scripts/slide_render_model.py` — typed render objects, canonical-content compiler, visibility classification and role/layout intent.
- `scripts/slide_renderer.py` — deterministic PowerPoint geometry, semantic colour/type primitives, component-aware layouts, source-shape binding.
- `scripts/render_daily_pack.py` — CLI that validates canonical inputs, compiles the render model, writes PPTX, and writes the render manifest.
- `scripts/audit_visual_composition.py` — deterministic structural audit for composition failure modes.

### Modified production files

- `scripts/dlp_build_runtime.py` — stage render-manifest provenance and require repo-renderer provenance before release promotion.
- `scripts/build_daily_pack.py` — accept `--render-manifest`; keep `--deck` compatibility but surface external-deck candidate status.
- `scripts/audit_release_bundle.py` — bind release to render manifest and new composition audit evidence.
- `references/qa-requirements.json` — register composition checks as release requirements.
- `references/qa-workflow-v3.md` — document the renderer/composition-audit stage.
- `references/slide-deck-quality-standards.md` — point generation to the renderer and composition audit.
- `SKILL.md` — make `render_daily_pack.py` the normal assembly path before staging/release.
- `.github/workflows/dlp-tests.yml` — ensure new renderer/composition tests are included by the existing test command and, where the workflow enumerates release audits, include the new audit.
- `scripts/build_chatgpt_package.py` / `scripts/package_component_skills.py` only if packaging allow-lists require explicit inclusion of new files.

### New tests

- `tests/test_slide_render_model.py`
- `tests/test_slide_renderer.py`
- `tests/test_render_daily_pack.py`
- `tests/test_visual_composition_audit.py`

### Modified tests

- `tests/test_build_runtime.py`
- `tests/test_release_contract.py`
- `tests/test_package_integrity.py`

---

### Task 1: Canonical render model and fail-closed visibility compiler

**Files:**
- Create: `scripts/slide_render_model.py`
- Create: `tests/test_slide_render_model.py`

**Interfaces:**
- Consumes: validated `context: dict`, `content: dict`, `component_record: dict` from the existing runtime contracts.
- Produces: `compile_render_model(context: dict, content: dict, component_record: dict) -> RenderPack`.
- Produces types used by later tasks: `SlideRole`, `ComponentKind`, `BlockKind`, `Visibility`, `ContentBlock`, `ProjectionPolicy`, `SlideSpec`, `RenderPack`, `RenderModelError`.

- [ ] **Step 1: Write failing tests for standard field classification and teacher-only filtering**

```python
from slide_render_model import SlideRole, Visibility, compile_render_model


def test_shared_reading_compiles_paragraph_question_and_answer_without_teacher_note():
    context, content, components = render_fixture(
        owner="dlp-shared-reading",
        fields={
            "paragraph": "The storm rolled across the harbour.",
            "prompt": "What changed in the setting?",
            "answer": "The storm changed the harbour conditions.",
            "teacher_note": "Ask two students to justify before revealing.",
        },
    )
    pack = compile_render_model(context, content, components)

    assert [slide.role for slide in pack.slides] == [SlideRole.READING, SlideRole.ANSWER]
    assert all(block.visibility is Visibility.STUDENT for slide in pack.slides for block in slide.blocks)
    assert "Ask two students" not in " ".join(block.text for slide in pack.slides for block in slide.blocks)
```

- [ ] **Step 2: Run the new test and verify RED**

Run: `python -m pytest tests/test_slide_render_model.py::test_shared_reading_compiles_paragraph_question_and_answer_without_teacher_note -q`

Expected: import failure because `slide_render_model.py` does not exist.

- [ ] **Step 3: Implement the typed model and deterministic standard-field map**

Implement enums/dataclasses with these minimum signatures:

```python
class RenderModelError(ValueError):
    pass

class Visibility(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class SlideRole(str, Enum):
    REMINDER = "reminder"
    QUESTION = "question"
    ANSWER = "answer"
    MODEL = "model"
    READING = "reading"
    WORKED_EXAMPLE = "worked_example"
    SUCCESS_CRITERIA = "success_criteria"
    TRANSITION = "transition"
    MORNING_WORK = "morning_work"

@dataclass(frozen=True)
class ContentBlock:
    id: str
    source_task_id: str
    source_field: str
    kind: BlockKind
    visibility: Visibility
    text: str

@dataclass(frozen=True)
class SlideSpec:
    id: str
    instance_id: str
    component: ComponentKind
    role: SlideRole
    eyebrow: str
    title: str
    blocks: tuple[ContentBlock, ...]
    policy: ProjectionPolicy
    layout_hint: str

@dataclass(frozen=True)
class RenderPack:
    generation_run_id: str
    date_label: str
    slides: tuple[SlideSpec, ...]
```

Use a closed standard-field map for `prompt`, `answer`, `paragraph`, `why_prompt`, `why_answer`, `before`, `after`, `reminder`, `success_criteria`, and `teacher_note`. `teacher_note` is teacher-only and excluded from slide specs. Unknown fields fail unless the task supplies explicit `render_fields` metadata of the form:

```json
{
  "render_fields": {
    "worked_steps": {"visibility": "student", "kind": "worked_step", "role": "worked_example"}
  }
}
```

- [ ] **Step 4: Add failing tests for ambiguous/unknown fields and missing source IDs**

```python
def test_unknown_field_without_render_metadata_fails_closed():
    context, content, components = render_fixture(fields={"prompt": "Do it.", "answer": "Done.", "mystery": "???"})
    with pytest.raises(RenderModelError, match="mystery"):
        compile_render_model(context, content, components)


def test_missing_task_id_fails_with_instance_context():
    context, content, components = render_fixture()
    content["tasks"][0]["id"] = ""
    with pytest.raises(RenderModelError, match="instance-1"):
        compile_render_model(context, content, components)
```

- [ ] **Step 5: Run tests, implement minimal validation, and verify GREEN**

Run: `python -m pytest tests/test_slide_render_model.py -q`

Expected: all render-model tests PASS.

- [ ] **Step 6: Add role-specific compilation tests**

Cover:
- Morning Work groups tasks into `SlideRole.MORNING_WORK` specs and marks Maths/Literacy groups semantically.
- Shared Reading creates paragraph+question then matched answer.
- Short generic task creates question then answer.
- `success_criteria` creates `SlideRole.SUCCESS_CRITERIA` with one check block per criterion (newline-delimited input accepted; six items remain six blocks).
- `before`/`after` revision tasks compile to model/worked-example specs rather than generic question cards.

- [ ] **Step 7: Run focused and baseline tests**

Run:

```bash
python -m pytest tests/test_slide_render_model.py -q
python -m pytest tests/test_semantic_relationships.py tests/test_pack_evidence.py -q
```

Expected: all PASS.

- [ ] **Step 8: Commit Task 1**

```bash
git add scripts/slide_render_model.py tests/test_slide_render_model.py
git commit -m "feat: add canonical slide render model"
```

---

### Task 2: Deterministic role-aware PowerPoint renderer

**Files:**
- Create: `scripts/slide_renderer.py`
- Create: `tests/test_slide_renderer.py`

**Interfaces:**
- Consumes: `RenderPack` from Task 1.
- Produces: `render_presentation(pack: RenderPack, out_path: Path) -> RenderManifest`.
- Produces `RenderManifest.to_dict() -> dict` with `schema_version`, `renderer`, `renderer_version`, `deck_sha256` populated by the CLI after save, and per-slide `slide_id`, `instance_id`, `role`, `layout_id`, `source_blocks`, `shape_bindings`, `metadata_labels`.

- [ ] **Step 1: Write failing tests for visual grammar primitives**

```python
def test_question_slide_uses_blue_role_rail_trebuchet_and_dominant_prompt(tmp_path):
    deck_path = tmp_path / "deck.pptx"
    manifest = render_presentation(question_pack("Calculate 125 × 8."), deck_path)
    prs = Presentation(deck_path)
    slide = prs.slides[0]

    assert manifest.slides[0].layout_id == "question-primary-v1"
    assert has_full_height_rail(slide, rgb="005A9C")
    assert all_projected_text_uses_font(slide, "Trebuchet MS")
    assert font_size_for_source(slide, manifest, "task-1:prompt") >= 36
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m pytest tests/test_slide_renderer.py::test_question_slide_uses_blue_role_rail_trebuchet_and_dominant_prompt -q`

Expected: import failure for `slide_renderer`.

- [ ] **Step 3: Implement renderer constants and shape helpers**

Use exact semantic colours:

```python
ROLE_STYLE = {
    "reminder": {"panel": "FFF3BF", "accent": "D6A900"},
    "model": {"panel": "FFF3BF", "accent": "D6A900"},
    "worked_example": {"panel": "FFF3BF", "accent": "D6A900"},
    "question": {"panel": "EAF2F8", "accent": "005A9C"},
    "reading": {"panel": "EAF2F8", "accent": "005A9C"},
    "morning_work": {"panel": "EAF2F8", "accent": "005A9C"},
    "answer": {"panel": "EAF7EE", "accent": "1B7F3A"},
    "success_criteria": {"panel": "EAF7EE", "accent": "1B7F3A"},
    "transition": {"panel": "FFFFFF", "accent": "103A5E"},
}
```

Set widescreen dimensions with `prs.slide_width = Inches(13.333)` and `prs.slide_height = Inches(7.5)`. Add helpers that name source-bound shapes `DLP:<slide-id>:<block-id>` and return their shape IDs for the manifest.

- [ ] **Step 4: Add failing tests for each required layout family**

Tests must assert layout IDs and structural properties, not pixels:

```python
def test_morning_work_math_and_literacy_use_two_broad_areas(...):
    assert slide_manifest.layout_id == "morning-work-split-v1"
    assert set(slide_manifest.groups) == {"maths", "literacy"}
    assert broad_group_widths(slide, slide_manifest) >= (5.0, 5.0)


def test_short_answer_scales_larger_than_explanation(...):
    assert answer_font >= 44
    assert explanation_font <= answer_font - 6


def test_reading_paragraph_measure_is_constrained(...):
    assert paragraph_width <= Inches(8.2)
    assert question_top > paragraph_bottom


def test_success_criteria_render_as_separate_check_rows(...):
    assert len(shapes_named_with_prefix(slide, "DLP:check:")) == 6
```

- [ ] **Step 5: Implement the seven deterministic layouts**

Create focused functions:

```python
render_morning_work_split(...)
render_question_primary(...)
render_answer_primary(...)
render_reading_measure(...)
render_worked_example(...)
render_success_criteria(...)
render_transition(...)
```

Layout selection must be a closed mapping from `SlideRole`/`layout_hint`, not an agentic heuristic. Use content-length thresholds only for typography/reflow decisions. Paragraph measure should target about 6.5–8.2 inches; if required 28pt text cannot fit at the maximum permitted panel height, return a split request handled by the renderer rather than shrinking below the policy floor.

- [ ] **Step 6: Implement split/reflow and content-sized panel behaviour**

Add deterministic helpers:

```python
choose_font_size(text: str, role: SlideRole, available_width: float, available_height: float) -> int
estimate_text_lines(text: str, width_inches: float, font_pt: int) -> int
split_paragraph_for_projection(text: str, *, max_chars: int = 520) -> tuple[str, ...]
panel_height_for_lines(lines: int, font_pt: int, *, min_height: float, max_height: float) -> float
```

Tests must prove:
- a one-word answer is at least 48pt when space allows;
- a two-line prompt does not sit in a full-height empty card;
- a long paragraph splits before dropping below 28pt;
- dense criteria remain separate rows.

- [ ] **Step 7: Verify renderer tests and existing slide audits**

Run:

```bash
python -m pytest tests/test_slide_renderer.py -q
python -m pytest tests/test_panel_ownership.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit Task 2**

```bash
git add scripts/slide_renderer.py tests/test_slide_renderer.py
git commit -m "feat: add deterministic lesson pack slide renderer"
```

---

### Task 3: Repository-owned render CLI and traceable render manifest

**Files:**
- Create: `scripts/render_daily_pack.py`
- Create: `tests/test_render_daily_pack.py`

**Interfaces:**
- CLI:

```text
python scripts/render_daily_pack.py \
  --context <context.json> \
  --content <content.json> \
  --component-record <component-record.json> \
  --out <candidate.pptx> \
  --render-manifest <render-manifest.json>
```

- Manifest schema: `schema_version: 1`, `renderer: "daily-lesson-pack"`, `renderer_version`, `context_sha256`, `content_sha256`, `component_record_sha256`, `deck_sha256`, and ordered `slides` from Task 2.

- [ ] **Step 1: Write failing end-to-end CLI test**

```python
def test_cli_builds_deck_and_same_hash_render_manifest(tmp_path):
    paths = write_renderer_fixture(tmp_path)
    result = subprocess.run([
        sys.executable, str(ROOT / "scripts" / "render_daily_pack.py"),
        "--context", str(paths.context),
        "--content", str(paths.content),
        "--component-record", str(paths.components),
        "--out", str(paths.deck),
        "--render-manifest", str(paths.render_manifest),
    ], capture_output=True, text=True)

    assert result.returncode == 0
    manifest = json.loads(paths.render_manifest.read_text())
    assert manifest["deck_sha256"] == sha256(paths.deck)
    assert manifest["content_sha256"] == sha256(paths.content)
```

- [ ] **Step 2: Run and verify RED**

Run: `python -m pytest tests/test_render_daily_pack.py::test_cli_builds_deck_and_same_hash_render_manifest -q`

Expected: FAIL because CLI does not exist.

- [ ] **Step 3: Implement CLI input validation and output writing**

Reuse `dlp_build_runtime.validate_resolved_context`, `validate_component_record`, and `pack_evidence.validate_content` rather than duplicating validation rules. Write the deck to a temporary sibling path, compute hash, then atomically replace the requested path and write the same-hash render manifest.

- [ ] **Step 4: Add failing tests for invalid/ambiguous inputs**

Cover:
- content schema != 3;
- content instances differ from context timetable instances;
- unknown render field without metadata;
- component record owner mismatch;
- output directory missing/unwritable.

Each failure must return non-zero and JSON stderr/stdout containing component/instance/source context where applicable.

- [ ] **Step 5: Run CLI tests and verify GREEN**

Run: `python -m pytest tests/test_render_daily_pack.py -q`

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add scripts/render_daily_pack.py tests/test_render_daily_pack.py
git commit -m "feat: add repository-owned pack render CLI"
```

---

### Task 4: Visual composition audit for known weak patterns

**Files:**
- Create: `scripts/audit_visual_composition.py`
- Create: `tests/test_visual_composition_audit.py`

**Interfaces:**
- CLI: `python scripts/audit_visual_composition.py --deck <pptx> --render-manifest <json> --out <report.json>`.
- Report: `schema_version: 1`, `status: PASS|FAIL`, `artifact_sha256`, `render_manifest_sha256`, and `warnings` entries with `code`, `slide`, `layout_id`, `source_blocks`, `observation`.

- [ ] **Step 1: Write failing audit tests for each 2026-09-15 failure mode**

Codes must be stable:

```text
COMPOSITION.REPEATED_GEOMETRY
COMPOSITION.LOW_OCCUPANCY_PANEL
COMPOSITION.PARAGRAPH_MEASURE
COMPOSITION.DENSE_LIST
COMPOSITION.TEACHER_CONTENT
COMPOSITION.REPEATED_METADATA
COMPOSITION.FLAT_ANSWER_HIERARCHY
COMPOSITION.SUCCESS_CRITERIA_BLOCK
COMPOSITION.MORNING_WORK_GROUPING
```

Example:

```python
def test_rejects_six_bold_criteria_in_one_shape(tmp_path):
    deck, manifest = build_known_bad_success_criteria(tmp_path)
    report = audit_visual_composition(deck, manifest)
    assert "COMPOSITION.SUCCESS_CRITERIA_BLOCK" in warning_codes(report)
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_visual_composition_audit.py -q`

Expected: import failure because audit module does not exist.

- [ ] **Step 3: Implement actual-deck structural measurements**

Use `python-pptx` to inspect:
- shape positions/areas;
- text lengths and paragraph count;
- font sizes/bold proportions;
- repeated date/week regex matches;
- named renderer-bound shapes;
- role/layout/source metadata from render manifest.

Use normalised geometry signatures based on rounded `(left, top, width, height)` tuples for major content shapes. Only flag repeated geometry when three or more consecutive slides use near-identical signatures while manifest roles/layout IDs materially differ.

- [ ] **Step 4: Add passing tests for legitimate consistency**

Prove that:
- five question slides using the same question layout do not trigger repeated-geometry warnings;
- a deliberately sparse transition slide does not trigger low-occupancy warnings;
- repeated date metadata on the opening and explicit resumption slide is permitted;
- a six-row checklist passes.

- [ ] **Step 5: Run audit and renderer tests**

Run:

```bash
python -m pytest tests/test_visual_composition_audit.py tests/test_slide_renderer.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add scripts/audit_visual_composition.py tests/test_visual_composition_audit.py
git commit -m "feat: audit lesson pack visual composition"
```

---

### Task 5: Bind renderer provenance and composition evidence into staging/release

**Files:**
- Modify: `scripts/dlp_build_runtime.py`
- Modify: `scripts/build_daily_pack.py`
- Modify: `scripts/audit_release_bundle.py`
- Modify: `tests/test_build_runtime.py`
- Modify: `tests/test_release_contract.py`

**Interfaces:**
- `stage_candidate(..., render_manifest_path: Path | None = None)` stages `render-manifest.json` when supplied and writes `renderer_provenance` into candidate status.
- `promote_release(...)` requires a valid staged render manifest from `renderer == "daily-lesson-pack"` and same deck hash.
- `REQUIRED_RELEASE_EVIDENCE` gains `composition`.

- [ ] **Step 1: Write failing staging tests**

```python
def test_repo_rendered_candidate_records_renderer_provenance(tmp_path):
    staged = stage_valid_candidate(tmp_path, with_render_manifest=True)
    status = json.loads((tmp_path / "candidate" / "candidate-status.json").read_text())
    assert status["renderer_provenance"] == "repo-rendered"


def test_external_deck_candidate_is_not_release_eligible(tmp_path):
    staged = stage_valid_candidate(tmp_path, with_render_manifest=False)
    assert staged["release_ready"] is False
    assert staged["renderer_provenance"] == "external"
```

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m pytest tests/test_build_runtime.py -q`

Expected: failures because render-manifest provenance is not supported.

- [ ] **Step 3: Implement staging provenance and same-hash validation**

Validate render manifest:

```python
if render_manifest.get("renderer") != "daily-lesson-pack": ...
if render_manifest.get("deck_sha256") != sha256(deck_path): ...
if render_manifest.get("content_sha256") != sha256(content_path): ...
if render_manifest.get("context_sha256") != sha256(context_path): ...
```

Copy it to `candidate/render-manifest.json` only when valid. External decks remain stageable but candidate status must say they are not release-eligible under current policy.

- [ ] **Step 4: Write failing release tests for external deck and missing composition evidence**

```python
def test_promote_release_refuses_candidate_without_repo_render_manifest(...):
    result = promote_release(candidate, released, complete_evidence_without_render_manifest)
    assert result["status"] == "CANDIDATE"
    assert "repo-rendered" in result["reason"]


def test_required_release_evidence_includes_composition():
    assert "composition" in REQUIRED_RELEASE_EVIDENCE
```

- [ ] **Step 5: Update release-audit command contract**

Add CLI arguments in `audit_release_bundle.py`:

```text
--render-manifest <candidate/render-manifest.json>
--composition <evidence/composition.json>
```

Require both reports to match the current deck hash and render-manifest hash, and require composition status PASS.

- [ ] **Step 6: Update `build_daily_pack.py` CLI**

Add optional `--render-manifest`. Pass it into staging. When `--release-evidence-dir` is supplied for an external deck, do not attempt promotion; return candidate status with the explicit unsupported-policy reason.

- [ ] **Step 7: Run runtime/release tests**

Run:

```bash
python -m pytest tests/test_build_runtime.py tests/test_release_contract.py -q
```

Expected: PASS.

- [ ] **Step 8: Commit Task 5**

```bash
git add scripts/dlp_build_runtime.py scripts/build_daily_pack.py scripts/audit_release_bundle.py tests/test_build_runtime.py tests/test_release_contract.py
git commit -m "feat: bind release to repo renderer provenance"
```

---

### Task 6: Register renderer and composition QA in canonical workflow/docs

**Files:**
- Modify: `references/qa-requirements.json`
- Modify: `references/qa-workflow-v3.md`
- Modify: `references/slide-deck-quality-standards.md`
- Modify: `SKILL.md`
- Modify: `.github/workflows/dlp-tests.yml`

**Interfaces:**
- New pack-level QA requirement IDs:

```text
PACK.RENDERER.PROVENANCE
PACK.VISUAL.COMPOSITION
```

- [ ] **Step 1: Write failing contract tests before docs/config changes**

Add to `tests/test_release_contract.py`:

```python
def test_qa_registry_requires_renderer_provenance_and_composition():
    ids = {row["id"] for row in json.loads((ROOT / "references" / "qa-requirements.json").read_text())["requirements"]}
    assert {"PACK.RENDERER.PROVENANCE", "PACK.VISUAL.COMPOSITION"} <= ids


def test_skill_names_render_daily_pack_as_normal_assembly_entrypoint():
    text = (ROOT / "SKILL.md").read_text()
    assert "scripts/render_daily_pack.py" in text
    assert "repo-rendered" in text.lower()
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_release_contract.py -q`

Expected: new assertions FAIL.

- [ ] **Step 3: Update QA registry and workflow**

Register `PACK.RENDERER.PROVENANCE` as a pack semantic/contract requirement and `PACK.VISUAL.COMPOSITION` as a deterministic visual screening requirement. Document the order:

```text
canonical records -> render_daily_pack.py -> composition/typography/containment/exemplar audits -> independent rendered review -> build_daily_pack.py promotion
```

Make explicit that the composition audit screens but does not replace independent visual review.

- [ ] **Step 4: Update SKILL generation contract**

Replace the old implication that a host may independently assemble a deck before `build_daily_pack.py` with the preferred path:

```text
component/content records -> render_daily_pack.py -> build_daily_pack.py
```

Keep external `--deck` compatibility described only as candidate/migration behaviour.

- [ ] **Step 5: Update CI only as needed**

If `.github/workflows/dlp-tests.yml` already runs `pytest` across all tests, do not duplicate commands. If it explicitly enumerates audit contract files, add `audit_visual_composition.py` and renderer import/CLI checks there.

- [ ] **Step 6: Run contract tests**

Run:

```bash
python -m pytest tests/test_release_contract.py tests/test_hardening_contract.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit Task 6**

```bash
git add references/qa-requirements.json references/qa-workflow-v3.md references/slide-deck-quality-standards.md SKILL.md .github/workflows/dlp-tests.yml tests/test_release_contract.py
git commit -m "docs: make repo renderer the canonical pack assembly path"
```

---

### Task 7: Regression pack proving the visual fixes end-to-end

**Files:**
- Modify: `tests/test_render_daily_pack.py`
- Modify: `tests/test_visual_composition_audit.py`
- Create: `examples/benchmarks/repo-renderer-visual-regression.md`

**Interfaces:**
- Synthetic fixture must include: Morning Work Maths+Literacy+extension; short question/answer; shared-reading paragraph; long model paragraph; six criteria; worked maths example; teacher-only note; repeated metadata attempt; mixed component sequence.

- [ ] **Step 1: Write a failing end-to-end regression test**

```python
def test_renderer_regression_pack_catches_2026_09_15_failure_modes_without_emitting_them(tmp_path):
    paths = write_full_visual_regression_fixture(tmp_path)
    run_renderer(paths)
    report = run_composition_audit(paths.deck, paths.render_manifest)

    assert report["status"] == "PASS"
    assert no_teacher_only_text(paths.deck)
    assert ordinary_slide_date_metadata_count(paths.deck) == 0
    assert morning_work_layout(paths.render_manifest) == "morning-work-split-v1"
    assert success_criteria_shape_count(paths.deck, paths.render_manifest) == 6
    assert max_reading_measure(paths.deck, paths.render_manifest) <= Inches(8.2)
```

- [ ] **Step 2: Run test and verify RED against incomplete implementation**

Run: `python -m pytest tests/test_render_daily_pack.py::test_renderer_regression_pack_catches_2026_09_15_failure_modes_without_emitting_them -q`

Expected: FAIL on whichever required property is not yet satisfied; do not weaken assertions to make it pass.

- [ ] **Step 3: Make the smallest renderer/audit repairs needed for GREEN**

Only adjust production behaviour corresponding to the failing assertion. Keep all earlier tests green.

- [ ] **Step 4: Run automated PowerPoint audits on the generated fixture**

From the test fixture or an explicit generated temp deck, run:

```bash
python scripts/audit_slide_typography.py --deck <fixture-deck> --dispositions <empty-ledger.json> --out <typography.json>
python scripts/audit_panel_containment.py --deck <fixture-deck> --out <containment.json>
python scripts/audit_visual_composition.py --deck <fixture-deck> --render-manifest <render-manifest.json> --out <composition.json>
```

Expected: no unresolved blocking finding attributable to the renderer fixture.

- [ ] **Step 5: Document the regression benchmark**

`examples/benchmarks/repo-renderer-visual-regression.md` must state the synthetic nature of the fixture, enumerate the failure modes it guards, and explicitly say it is not lesson-content evidence.

- [ ] **Step 6: Run all renderer-focused tests**

Run:

```bash
python -m pytest tests/test_slide_render_model.py tests/test_slide_renderer.py tests/test_render_daily_pack.py tests/test_visual_composition_audit.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit Task 7**

```bash
git add scripts/slide_render_model.py scripts/slide_renderer.py tests/test_render_daily_pack.py tests/test_visual_composition_audit.py examples/benchmarks/repo-renderer-visual-regression.md
git commit -m "test: lock visual renderer regression contract"
```

---

### Task 8: Package integrity, full verification and distribution rebuild

**Files:**
- Modify: `scripts/build_chatgpt_package.py` only if packaging allow-list omits new renderer/audit files.
- Modify: `scripts/package_component_skills.py` only if shared runtime files are explicitly enumerated.
- Modify: `tests/test_package_integrity.py`
- Regenerate: `dist/chatgpt/daily-lesson-pack.zip`
- Regenerate component archives only if their package contents intentionally include the shared renderer/runtime.

**Interfaces:**
- Packaged ChatGPT skill must contain the renderer CLI, render model, renderer library, composition audit, updated contracts and tests required by package verification.

- [ ] **Step 1: Write failing package-integrity assertions**

```python
def test_chatgpt_package_contains_repo_renderer_and_composition_audit():
    names = packaged_names()
    assert "scripts/render_daily_pack.py" in names
    assert "scripts/slide_render_model.py" in names
    assert "scripts/slide_renderer.py" in names
    assert "scripts/audit_visual_composition.py" in names
```

- [ ] **Step 2: Run package test and verify RED if allow-lists are incomplete**

Run: `python -m pytest tests/test_package_integrity.py -q`

Expected: FAIL only if package builders need updates; if it passes because builders already include all `scripts/`, keep the production builders unchanged.

- [ ] **Step 3: Make the minimal packaging change and rebuild distributions**

Run repository-owned package commands already documented by the project, including at minimum:

```bash
python scripts/build_chatgpt_package.py
python scripts/verify_package_archive.py dist/chatgpt/daily-lesson-pack.zip
```

Run `python scripts/package_component_skills.py` only when Task 8 inspection shows the component bundles intentionally carry shared renderer/runtime files.

- [ ] **Step 4: Run the complete automated test suite**

Run: `python -m pytest -q`

Expected: zero failures.

- [ ] **Step 5: Run package and release-hardening verification**

Run the repository commands referenced by `.github/workflows/dlp-tests.yml` and `docs/DEVELOPMENT.md` that are not already covered by `pytest`, especially archive verification and dependency/package audits.

Expected: zero failures/errors.

- [ ] **Step 6: Inspect git diff and generated archive identity**

Run:

```bash
git status --short
git diff --check
git diff --stat
git diff --name-only
sha256sum dist/chatgpt/daily-lesson-pack.zip
```

Confirm there are no unrelated changes and the rebuilt archive is the only intended binary regeneration unless component bundles were deliberately rebuilt.

- [ ] **Step 7: Commit verified distribution**

```bash
git add scripts tests references SKILL.md .github examples dist/chatgpt/daily-lesson-pack.zip
git commit -m "feat: ship repo-owned Daily Lesson Pack renderer"
```

- [ ] **Step 8: Fresh verification before completion claim**

Run again after the final commit:

```bash
python -m pytest -q
git diff HEAD^ --check
```

Record the exact test count and exit codes before reporting completion.

---

## Plan Self-Review

### Spec coverage

- Canonical render model and ambiguity failure: Task 1.
- Seven required deterministic layout families: Task 2.
- Teacher-only filtering, metadata suppression, line measure, largest-sensible type and content-sized panels: Tasks 1–2 and regression Task 7.
- Render CLI and manifest: Task 3.
- Composition audit covering every named failure mode: Task 4.
- External-deck candidate-only release policy and render-manifest provenance: Task 5.
- QA/release workflow and skill documentation: Task 6.
- Synthetic regression fixture covering the 2026-09-15 visual failures without depending on that lesson content: Task 7.
- Packaging/rebuild/full-suite verification: Task 8.

### Placeholder scan

No `TBD`, `TODO`, deferred implementation, generic “add tests”, or undefined “similar to Task N” steps are permitted in this plan.

### Type/interface consistency

- Task 1 produces `RenderPack` consumed by Task 2.
- Task 2 produces render-manifest data consumed by Task 3.
- Task 3 serialises the render manifest consumed by Tasks 4–5.
- Task 4 produces `composition.json`, added to `REQUIRED_RELEASE_EVIDENCE` in Task 5.
- Task 5 changes release/staging contracts; Task 6 registers/document them; Tasks 7–8 verify and package them.
