# Repo-owned visual renderer design

Date: 2026-09-15
Status: proposed after teacher approval of the in-chat design
Base commit: `80fa9f7b49056f0e2ee2a1e83723930703e11647`

## Problem

The repository already defines strong visual requirements in `references/slide-deck-quality-standards.md` and `references/visual-exemplar-standard.md`, but the supported `scripts/build_daily_pack.py` path does not generate or assemble PowerPoint slides. It accepts a pre-existing PPTX, stages it, and optionally promotes it after audits.

That leaves a critical gap: a host can author a visually weak deck outside the repository, then rely on structural checks that do not fully prevent composition failures such as repeated giant cards, low information density, excessive line length, teacher-only notes on projected slides, flat answer hierarchy, or unstructured success-criteria lists.

The 2026-09-15 Daily Lesson Pack exposed this gap. It was readable and consistent, but compositionally generic and below the approved visual exemplar standard.

## Goal

Make the repository own the deterministic creation of the classroom PPTX from canonical pack records so the visual standards are enforced during generation, not only screened afterwards.

The renderer must preserve current content ownership and QA contracts. It is a presentation compiler, not a pedagogy generator.

## Non-goals

- Do not move lesson-content generation into the renderer.
- Do not infer missing lesson content from chat memory or historical decks.
- Do not clone exemplar slide content.
- Do not create a free-form design agent inside the renderer.
- Do not weaken existing release evidence, mathematical checks, year-profile checks, panel-containment checks, typography checks or independent rendered review.
- Do not require decorative images or illustrations for ordinary teaching slides.

## Recommended architecture

### 1. Canonical render model

Add a small typed render model owned by the repository, for example `scripts/slide_render_model.py`.

It should convert canonical content records into explicit student-facing slide specifications before any PowerPoint geometry is created. The core concepts are:

- `SlideRole`: `reminder`, `question`, `answer`, `model`, `reading`, `worked_example`, `success_criteria`, `transition`, `morning_work`.
- `Component`: Morning Work, Literacy Warm-up, Shared Reading, Guided Reading, Writing, Numeracy Warm-up, Mathematics.
- `ContentBlock`: heading, paragraph, task, answer, worked step, bullet/check item, diagram placeholder, teacher-only note.
- `ProjectionPolicy`: minimum font tier, preferred line length, maximum block count, whether splitting is permitted, and whether teacher-only content is prohibited.
- `LayoutHint`: semantic preference only, not raw coordinates.

The render model must reject ambiguous content rather than guessing whether a block is student-facing or teacher-facing.

### 2. Deterministic layout engine

Add `scripts/slide_renderer.py` as the core rendering library. It receives only validated render-model objects and produces PowerPoint geometry deterministically.

It must use the approved visual grammar:

- 16:9 canvas;
- full-height role-coloured rail at far left;
- Trebuchet MS as the dominant projected typeface;
- compact uppercase eyebrow plus larger plain-language title;
- semantic colour system from the visual exemplar standard;
- responsive content panels rather than one fixed card template.

The layout engine chooses from a deliberately small family of component-aware layouts.

#### Required layouts

1. **Morning Work split layout**
   - two broad working areas where both Maths and Literacy are present;
   - visually chunked task groups;
   - no detached extension footer;
   - every task executable in a student book;
   - content fitted by reflow/splitting before font reduction.

2. **Question / task layout**
   - dominant prompt or student action;
   - optional subordinate support cue;
   - short prompts scale larger than minimum size;
   - no oversized empty panel around a few words.

3. **Answer / successful model layout**
   - the actual answer is the dominant visual element;
   - explanation is secondary;
   - avoid bolding every line equally;
   - short answers grow materially larger when space permits.

4. **Reading / model paragraph layout**
   - constrained text measure rather than full-slide-width paragraphs;
   - paragraph and attached question visually separated;
   - split across slides when projected-size text cannot fit comfortably;
   - teacher instructions excluded from projected content.

5. **Worked example layout**
   - one clear worked surface with ordered steps;
   - enough space for mathematical notation or modelled writing;
   - supporting explanation subordinate to the worked content.

6. **Success criteria / checklist layout**
   - individual criteria as spaced checklist rows or grouped checks;
   - no wall-of-bold-text treatment;
   - each criterion visually scannable from the back of the room.

7. **Transition / resumption layout**
   - lightweight section marker for timetable breaks or component changes;
   - no unnecessary repeated date/week metadata on ordinary slides.

### 3. Composition rules

The renderer must enforce these rules before export:

- Teacher-only directions never appear on projected slides. They remain in briefing artefacts or speaker notes where supported.
- Date / term / week metadata appears only where it materially aids navigation, such as the opening slide or explicit resumption slides.
- Paragraph text has a maximum preferred line length and must not span the full useful width merely because space exists.
- Main panels size to content and instructional role; they do not automatically consume the full body region.
- Reflow, merge, split and shorten-before-shrink behaviour follows `references/slide-deck-quality-standards.md`.
- Dense lists must be structurally grouped; six or more substantial criteria cannot be rendered as one undifferentiated bold text block.
- Short answers and expressions use the largest sensible type within the role hierarchy.
- Multiple consecutive slides may share visual grammar, but not identical geometry when their content type differs.
- Component transitions should be visually recognisable without inventing a new colour system.

### 4. Rendering CLI

Add `scripts/render_daily_pack.py` as the supported PPTX assembly entry point.

Proposed interface:

```text
python scripts/render_daily_pack.py \
  --context <context.json> \
  --content <content.json> \
  --component-record <component-record.json> \
  --out <candidate.pptx> \
  --render-manifest <render-manifest.json>
```

The CLI must:

1. validate the canonical inputs;
2. compile them to the render model;
3. select deterministic layouts;
4. generate the PPTX;
5. emit a render manifest containing layout IDs, slide roles, source block IDs and renderer version;
6. fail closed on unsupported or ambiguous content.

### 5. Integration with `build_daily_pack.py`

Update the supported workflow so repository-owned rendering is the normal path.

The preferred flow becomes:

```text
canonical component/content records
        -> render_daily_pack.py
        -> candidate PPTX + render manifest
        -> build_daily_pack.py
        -> audits / independent review
        -> release
```

For compatibility, `build_daily_pack.py` may continue accepting an externally supplied `--deck`, but an external deck must be clearly marked in provenance. It must not be silently treated as equivalent to a repo-rendered deck.

Release policy:

- repo-rendered decks: eligible for release if all existing evidence passes;
- externally assembled decks: candidate-only unless a separate explicit legacy/external-deck policy is added and independently approved later.

This prevents the current generator gap from remaining the default path while avoiding an abrupt break for diagnostic or migration workflows.

### 6. Visual composition audit

Add a deterministic screening audit, for example `scripts/audit_visual_composition.py`.

It should flag, at minimum:

- long runs of near-identical slide geometry despite differing semantic roles;
- oversized low-occupancy panels;
- paragraphs rendered beyond the preferred measure;
- dense undifferentiated lists;
- teacher-only content on projected slides;
- unnecessary repeated date/week metadata;
- answer slides where all content has effectively equal emphasis;
- success-criteria slides rendered as one large text block;
- Morning Work that lacks the required broad-area grouping when both Maths and Literacy are present.

This audit is a screen, not a replacement for independent rendered visual review.

### 7. Regression fixtures

Add regression coverage based on repository-owned fixtures rather than today's lesson wording.

Required fixtures:

- Morning Work with Maths + Literacy + extension;
- short question and one-word/one-number answer;
- shared-reading paragraph + question + matched answer;
- long model paragraph requiring constrained measure or split;
- six-item success-criteria list;
- worked mathematics example;
- teacher-only instruction attached to otherwise student-facing content;
- repeated metadata attempt;
- mixed component sequence that would expose repeated identical geometry.

Tests should assert both semantic output and layout metadata from the render manifest.

Where practical, render-level comparison should use structural thresholds rather than pixel-perfect snapshots so legitimate font-metric differences do not create brittle failures.

## Data flow

```text
component skills
    -> canonical content records
    -> render-model compiler
    -> deterministic layout selector
    -> PowerPoint renderer
    -> render manifest
    -> existing typography / containment / exemplar / semantic audits
    -> new composition audit
    -> independent rendered review
    -> release authority
```

The renderer must not mutate canonical lesson content. If content cannot be rendered at the required projected quality, rendering fails with a specific defect that routes back to the owning component or assembler.

## Error handling

Fail closed on:

- unclassified student-facing versus teacher-only content;
- unsupported content block types;
- content that cannot fit at required projected size after permitted reflow/splitting;
- missing source IDs needed for traceability;
- invalid semantic colour/layout role mapping;
- missing or checksum-invalid approved exemplar when exemplar-bound checks are required;
- render output lacking a matching render manifest.

Errors should identify component, instance ID, source block ID, attempted layout and repair category so the orchestrator can route the defect correctly.

## Testing strategy

Implementation must be test-driven.

### Unit tests

- render-model validation;
- student/teacher visibility filtering;
- layout selection by semantic role;
- font-tier selection;
- paragraph-measure decisions;
- panel sizing and occupancy heuristics;
- success-criteria grouping;
- repeated metadata suppression;
- geometry-diversity audit logic.

### Integration tests

- canonical content -> PPTX + render manifest;
- renderer output passes existing typography and panel-containment audits;
- approved visual grammar is retained;
- externally supplied deck remains distinguishable in provenance;
- unsupported/ambiguous input fails closed.

### Regression tests

- approved visual exemplar remains authoritative for visual grammar;
- Morning Work benchmark remains authoritative for that component;
- known weak composition patterns are rejected;
- current release pipeline continues to validate source hashes and evidence binding.

## Migration

1. Add renderer and tests without removing the existing external-deck staging interface.
2. Update `SKILL.md`, development docs and release workflow docs to make repo rendering the preferred supported generation path.
3. Add render-manifest provenance to candidate staging.
4. Add composition audit to CI and release evidence.
5. Mark external-deck release as unsupported/candidate-only unless a later policy explicitly authorises it.
6. Rebuild packaged ChatGPT/component distributions after all tests pass.

## Success criteria

The change is complete when:

- the repo can deterministically generate the PPTX from canonical content records;
- Morning Work uses the approved broad-area layout rather than a stacked generic card;
- question, answer, paragraph/model, worked-example and success-criteria slides use distinct role-appropriate composition;
- teacher-only instructions do not appear on projected slides;
- ordinary slides no longer repeat date/week metadata without purpose;
- paragraphs use constrained measure or are split rather than stretched across the canvas;
- answer hierarchy visually emphasises the answer rather than every line;
- success criteria are rendered as a scan-friendly checklist structure;
- the new composition audit catches the 2026-09-15 failure modes;
- existing release evidence remains fail-closed;
- the full automated test suite passes;
- the packaged skill/distribution is rebuilt from the verified source.

## Rejected approaches

### QA-only hardening

Adding only more checks would improve detection but leave visual composition outside repository generation. It would continue to rely on an external generator to make the right design decisions and then repair failures after the fact.

### Exemplar/template cloning

Cloning a small set of exemplar slides would be deterministic but brittle. It risks turning the approved visual grammar into fixed geometry, which conflicts with the repository's own responsive-container and largest-sensible-type rules.

### Free-form design agent

An agent choosing arbitrary slide designs would reduce determinism, increase review burden and recreate the same drift problem at another layer. The renderer should make bounded semantic layout decisions, not improvise presentation design.
