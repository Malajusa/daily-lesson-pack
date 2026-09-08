# Agent orchestration v2

Approved basis: the user's attached implementation proposal, supplied with the
instruction to implement it against `Malajusa/daily-lesson-pack` on 8 September
2026. Baseline: `5c7f1f7c4eb6321c6dc9732b7b903a48c17b0244`.

## Contract

Add an executable control plane above, not instead of, the existing candidate
and release pipeline. Retain context/component-record schema 2 and
content/manifest schema 3. Retain the v1 skill registry and all calibrated
pedagogy. Models author and judge; Python routes, validates and gates.

The v2 registry owns role definitions, context projections, references,
concurrency, attempt limits, critics and repair destinations. Nine offline
Draft 2020-12 schemas validate its handoffs. Resolved, source-hashed context and
the deterministic DAG are immutable; mutable execution state is separate.
Each timetable instance remains distinct even when owners repeat.

Generation is bounded-parallel. Component identities, task ownership, required
checks, profiles, time budgets and run hashes must agree. Mathematics requires
an independent component critic before assembly. Every attempt, including an
invalid or failed response, is retained. One per-instance attempt budget covers
initial generation, protocol retries, critic repairs and whole-pack repairs.

Assembly produces the canonical records deterministically and uses the existing
runtime. Semantic and rendered-visual review fan out alongside deterministic
pack auditing. Coverage comes from `pack_evidence.expected_checks`, not a second
QA register. Reviews must bind to all current hashes, have exact check coverage,
carry real host execution receipts and use actors distinct from every author.
Reviewers return defects without modifying content. Defects are checked against
actual ownership and batched by instance; a content repair invalidates all pack
reviews. Ambiguous/pack-level defects stop for explicit disposition, not a broad
rewrite. Only `promote_release` and its existing release audit can release.

## Necessary corrections to the illustrative proposal

* The existing final component audit also requires `scheduled_instances` and
  uses check `result`, not `status`. The adapter maps structured evidence without
  an LLM rewrite and preserves existing required check IDs.
* Plan hashes are actually populated and validated. JSON flags alone do not
  enforce immutability: requests are copied and pinned files are rehashed.
* A FAIL review with no defects cannot imply PASS. Every failed check needs a
  correctly routed blocking defect; missing/duplicate checks fail validation.
* Attempt limits are cumulative, never reset by entering a repair loop.
* There is no general pedagogical deck renderer in this baseline repository.
  Supply a trusted assembly command using ContentSource, or stop after validated
  components. The implementation does not invent a replacement slide renderer.
* Staging must retain every manifest-declared deliverable and render, not only
  pack.pptx. The bridge validates and copies these before auditing.
* Host adapters, not model-authored fields, supply execution identity and raw
  transcripts. Receipts are auditable provenance, not cryptographic proof.

## Provider and security boundary

A Python AgentAdapter and a JSON/stdin/stdout command adapter are supported.
Commands are explicit trusted host configuration; no provider credentials,
model subscriptions or external jobs are configured by this change. A separate
assembly command provides final files from canonical content. No shell string
execution is used. Local commands are trusted code: logical ownership checks
and temporary working directories are not an operating-system sandbox. A host
requiring adversarial process isolation must supply it.

Release remains fail-closed when an assembler, real independent review,
rendered page, warning disposition or required evidence is unavailable. A
component-only result is never a candidate deck and never classroom-ready.
