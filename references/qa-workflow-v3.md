# Evidence-based pack release, version 3

## Authority and applicability

`references/qa-requirements.json` is the authoritative release coverage register.
Its stable IDs preserve the existing QA requirements; component prose explains
how to meet them. A requirement is never satisfied merely because its checklist
entry exists. The independent reviewer must evaluate its actual meaning.
Read the register entries for the scheduled owners before authoring. Resolve
the active year profile separately; do not change Year 4/5 or Year 6 pitch.
Each context record declares `required_artifacts`, using roles `deck`, `briefing`,
`student`, `answers`, `printing_plan` as applicable to the current request.
The explicit context and timetable determine omissions; absence is not an
authorised override. Scheduled warm-ups retain their normal counts. Unscheduled
warm-ups require zero slides, without a user override.

## Single content source

Before rendering, create `content.json` with `schema_version: 3`, `instances`
copied exactly from resolved context `timetable_instances`, and `tasks`.
Every student task/model pair has a unique ID, `instance_id`, `operation`,
and `fields` containing the exact `prompt` and complete `answer` strings.
Store reminders, explanations, before/after passages and other teaching text
as additional named fields. `documents` maps IDs to objects with `fields` for
briefing and print-plan text. All delivered text comes from these records.

Tasks also carry `demands` (unique `id`, `action`, exact `answer_quote`).
Choice tasks carry `options` (`text`, boolean `correct`; each distractor includes
`misconception` and `rejection_reason`). Revision tasks carry `fields.before`,
`fields.after` and `propositions` with exact `before_quote` and `after_quote`.
The reviewer independently enumerates original claims, including qualifications
such as “valuable”, and verifies the map is exhaustive and meaning-preserving.
Matching a quoted fragment alone does not establish semantic equivalence.
A response override needs `response_override_source`, citing actual current
authorisation, which the independent reviewer verifies against context.

Import `ContentSource` from `scripts/content_source.py` in every builder.
Use `source.text(task_id, field)` to populate both the PPTX and the PDFs.
Never paraphrase the prompt/answer again for a printable. For a deliberately
adapted representation, define it as a separate task with explicit review.
Retain rich text and exact mathematical diagrams; do not flatten them to prose.
Tag subordinate PPTX shapes `DLP:instruction`, `DLP:explanation`, `DLP:cue`, or
`DLP:why`; tag main content `DLP:main`. Main warm-up content retains its 36 pt
minimum; supporting instructional text has a 28 pt floor. Role assignments are
subject to visual review. Do not relabel main content to evade its floor.
For mathematical diagrams or tables, bind their accompanying exact field text
and require independent visual representation checks; text equality alone
does not verify a quantity, partition, scale or drawing.

## Complete-pack manifest

After final layout/export, create `manifest.json` with schema version 3,
`content_sha256`, `context_sha256`, and `artifacts` entries:
`id`, `role`, `path` relative to the manifest, `sha256`, `pages`.
Declare every delivered file. The manifest also holds `bindings`, created using
`source.bind(artifact_id, record_id, field, page, shape_id=...)` for PPTX or
`bbox=[x0,y0,x1,y1]` for PDFs (points). Each region must extract exactly the
canonical field, except normalised whitespace/Unicode compatibility characters.
Text split across frames needs distinct canonical fields, not a partial match.
Every page must be bound. Every task prompt/answer must be bound in the deck,
and respectively the student/answer PDFs when those files are required.
No ad-hoc “expected answer” script can replace these final-file comparisons.

Render every final slide and PDF page. Add `renders` entries containing
`artifact`, `page`, `path`, `sha256`, and `artifact_sha256` to the manifest.
Freeze content, artefacts, renders and manifest before review. Any change to
them invalidates review and requires rebuilding affected files and rerunning
the complete applicable release command.

## Executed independent review

Use a fresh review agent/process with this skill, resolved context, canonical
content, final artefacts/renders and the register. Do not supply generator PASS
assertions or desired conclusions. Reading the QA skill in the generator's own
thread is not independent review. If no independent execution facility exists,
deliver a candidate with review pending; never fabricate independence.

Generate UNREVIEWED checklist skeletons with:
`python scripts/content_source.py --content content.json --manifest manifest.json --method semantic --out semantic.json`
and again with `--method visual`. The register expands pack, owner-instance,
task and every-artefact-page scopes. Review every entry. Record `PASS`, `FAIL`
or justified `NA`, `observation`, and exact `citations` containing `artifact`,
`page`, `shape_id`/`bbox`, and `quote`. Visual checks cite the rendered page.
NA requires an `applicability_reason` and source citation; it cannot excuse an
observed defect. Every page requires visual PASS. Keep source evidence detailed
enough to verify facts preserved, demands answered and distractors plausible.

The host captures the actual independent execution receipt, never the generator:
`source` (`collaboration`, `external-runner`, or `human-review`), `execution_id`,
`reviewer_actor`, `generator_actor`, `review_sha256`, `manifest_sha256`,
`transcript_path` relative to the receipt, `transcript_sha256`. Save the raw
host invocation/completion transcript. Receipt and review share execution_id.
The review carries manifest/content/requirements hashes; it does not use the
legacy evidence-string or run-ID-only schema.
Different labels alone never count as independent execution. These receipts
make provenance inspectable; local JSON cannot cryptographically authenticate
the host. A deployment needing that guarantee must use host-signed receipts.

## Release command

Run `scripts/audit_release_bundle.py` with its existing report-path arguments
plus `--manifest`, `--content`, `--context-record`, `--component-record`,
`--warning-ledger`, `--visual-review`, `--semantic-trace` and `--visual-trace`.
The command validates complete-pack evidence first, then runs the repository
audits itself and overwrites report outputs. It does not trust supplied PASS
files. Warning dispositions remain individually required. Semantic checks and
visual page coverage are required even when structural audits pass.
Only its final PASS for the current manifest permits “classroom-ready”.
Report any unfinished gate accurately; counts of checks are not evidence of
educational quality. Do not reuse an earlier pack's release decision.

Run `python -m unittest discover -s tests -v` after changes to these controls.
Keep both valid and deliberately faulty fixtures. Changes to pedagogy also
require the existing concept-family and year-profile regression benchmarks.
