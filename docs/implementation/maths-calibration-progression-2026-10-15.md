# Maths calibration and responsive progression — implementation

The authoring and review changes are implemented as an unreleased candidate.
Warm-ups now require worthwhile Most tasks, a specific increase in Some demand,
and answers that are independent of neighbouring tiers. Main lessons now probe
the intended learning immediately and prepare substantial support, normal and
advance routes. Required pedagogical failures cannot be waived or rescued by
passing structural reports.

The production source and package build are bound to
`67c85b32a5be9a78dc0edb1ed047f5e3b72b91c7`, based on
`18aa531182e359e29833f63f5327d506c8451d4d`. Subsequent handoff commits record
evidence and candidate snapshots; they do not change that tested runtime.

## Changes and verification

| Plan task | Result |
| --- | --- |
| 1. Sanitised acceptance cases | W1–W4 and R1–R3 recorded; the private classroom deck is excluded from Git. |
| 2. Component boundary protection | Registered owner/instance/method checks reject NA regardless of ID prefix; unrelated legitimate NA remains valid. |
| 3. Warm-up calibration | Three new semantic boundaries; a rationale for every pair; direct responses and five question/answer pairs retained. |
| 4. Responsive progression | Four new maths boundaries; individual opening evidence, exact destinations, substantial advancement and fresh independent rechecks. |
| 5. Pedagogical review | Per-pair/per-block judgement and three readiness walkthroughs; missing/failed/stale checks block eligibility. |
| 6. Controlled samples | Five baseline/revised consumers each, shapes and addition examples, canonical specs, diagrams, complete answers, task cards and independent content review. Rendered-slide acceptance remains blocked. |
| 7. Packages and candidate | Complete plus eight component archives verified; preserved plugin update/full snapshots prepared, reviewed and not uploaded. |

The clean original source passed 260 tests with one existing skip. The final
source passes **277 tests, one existing skip**. This includes executed failing
regressions before fixes for boundary waivers, missing contracts, package closure
and panel-role typography. Full-suite evidence is separate from reviewer-run
focused suites. The existing skip is not silently counted as a pass.

Exact complete and standalone archives passed the existing archive verifier and
dependency audit, including isolated QA boundary enforcement without siblings.
The final plugin resource tree also passed its dependency audit. All five sample
PPTXs (three teacher decks and two student-card decks) passed typography and
panel containment with no unresolved warnings; the ten-slide warm-up passed its
standalone structural validator. Native timing XML is encoded on 19 shape and
one addition slide. XML presence does not demonstrate playback.

## Independent teaching review

A fresh reviewer examined source, mathematical answers, actual task substance,
routes, package bytes and final PPTX assets/text. The raw comparison produced
**0/5 complete warm-up content passes at baseline versus 4/5 revised**. The fifth
revised candidate repeated a faulty fruit-category redistribution story from the
source benchmark. Both benchmark and a separately labelled candidate were
repaired and independently rechecked; the raw result remains a failure. This is
bounded synthetic evidence, not a classroom trial or statistical efficacy claim.

All five revised shape sequences supplied sustained R1/R2/R3 routes at content
level, compared with none of the five baseline sequences meeting the complete
route criterion. Some baseline support and exits were already sound. The
addition strategy sample provides a second concept family and complete
constrained-construction solutions. Its advance criterion was corrected to
accept either mathematically justified strategy preference. Shape answer views
were repaired to include labelled pieces, requested comparisons and the corrected
line model, rather than generic captions or answers only in teacher notes.

The applicable universal-canon cases were reviewed across both concept families.
Year-profile registry tests and memory-independent package/context checks pass.
Full paired Year 4/5 versus Year 6 consumer generation and a full Wednesday
teaching-pack release were not performed. The common teaching goal and readiness
routes remain independent of enrolment-year ability assumptions.

## Plugin candidate and rollout

The private plugin remains version **0.2.0**, release
`pluginrel_6acef568fc38819186b69a00e1a7fd98`. The prepared **0.2.1** candidate
contains resource version **3.10.0-rc.5**. It retains all 407 original files,
adds seven and changes 39 paths in total, with zero deletions. Independent byte
comparison confirmed the renderer overlay, wrapper skills, default prompts and
HTML-control QA supplement survive. The update ZIP is exactly the byte delta;
the full ZIP is a preserved review snapshot. No plugin activation or merge occurred.

The update candidate must use the observed release ID as a conflict guard. If
the installed release has changed, retrieve and reconcile its current source
before upload. Do not substitute the complete source package for the plugin:
it lacks the plugin-specific renderer overlay. The archive identities and
check reports are recorded in the companion evidence JSON.

**Concrete host blocker:** LibreOffice was absent. A private, checksum-verified
runtime was assembled without a system installation, but startup raises
`com::sun::star::uno::DeploymentException`. No full-slide PDF/PNG rendering or
PowerPoint/Keynote playback was completed. The samples therefore remain
candidates; no visual or classroom-ready release is claimed. Perform final
rendered inspection, native reveal playback and the normal independent release
workflow on a compatible host before classroom release or plugin rollout.

Rollback: revert the focused source commits and rebuild from the previous
accepted revision. No installed rollback is needed because no activation
occurred. Retain original frozen evidence rather than rewriting its verdicts.

## Execution decisions and remaining evidence

Package dependency edits preceded sample generation so test consumers could
resolve their contracts. Declared Python dependencies were installed in a
private environment before baseline comparison. Fresh skill consumers tested
behaviour while one independent final reviewer examined the implementation;
they did not share production edits. Labels were visible and a reference-path
harness clarification occurred, so the consumer comparison is not blinded or
perfectly controlled.

The original plan is retained as historical handoff. A narrow additional fix
was necessary when the current renderer appended `|panel=...` to text-role
names: the typography audit now parses the role before the ownership suffix.
Positive and negative regressions preserve the existing 28-point support and
36-point warm-up main floors. This does not alter the renderer overlay itself.

Ordinary classroom follow-up remains separate:

1. Were Most and Some worthwhile for the pupils who chose them?
2. Could pupils who demonstrated the learning advance without waiting?
3. What still required improvisation?

See the independent review and evidence JSON alongside this report. Candidate
sample files include a teacher briefing with exact final slide/card destinations;
answers remain outside the student-card presentation notes.

## Publication status — initial attempt

The branch and all source/candidate changes are committed locally. Automatic
approval review rejected the attempted push to Malajusa/daily-lesson-pack because
it treated the destination as unverified and the payload as potentially private.
No GitHub push or draft PR was completed. The exact reviewed branch and candidate
are preserved for user review; publication requires explicit approval. This is
separate from the plan’s prohibition on automatic merge or plugin activation.

## Publication after approval — 15 October 2026

The user explicitly approved publication. Native Git authentication was unavailable,
so the connected GitHub service published a snapshot commit, `10e0c82e6eab86bab7a661a37e9e8d7b9f28347c`,
whose tree is byte-identical to reviewed local commit `ec9881a586a71b0c26504b6a3e71cc05179343c5`
(tree `41af24f7c8e502a55ed1837514979be3baefda00`). A following handoff commit adds only this publication
record, the candidate README and the original reviewed Git history bundle.

The snapshot has a new commit ID because the connected service creates commits.
The original tested source `67c85b32a5be9a78dc0edb1ed047f5e3b72b91c7` and focused
commits remain recoverable from `dist/plugins/maths-calibration-reviewed-history.bundle`,
with base `18aa531182e359e29833f63f5327d506c8451d4d` already present in this repository.
Package source bindings and frozen reviews therefore retain their original identities.
The published branch is `codex/maths-calibration-progression-20261015`.
A draft PR is prepared for review; no merge or plugin activation is authorised.
