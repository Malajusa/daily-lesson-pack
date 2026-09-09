# Release hardening candidate — 3.10.0-rc.1

Status: **implemented candidate; not an assisted or unattended release**.

Base source: `c31f686fb75c3addbb47ccbd147ba6e11e488e55`.
Integrated D02 source: `7cba2d72642dcc22cf8a8d1ea8e8a075ff0766ad`.
Development branch: `fix/release-readiness-20260909`, PR #12.
The accepted source identity for a built candidate is its CI `SOURCE_COMMIT.txt`
and matching package manifest, not this historical base hash.

## Implemented and directly testable

- D02's source-bound profile registry is integrated without changing the approved
  Year 4/5 profile or approved visual exemplars. Tests reproduce and reject false
  Year 6 calibration, an unknown maturity label and a wrong profile source, with
  valid normal/candidate controls.
- Creator defaults resolve automatically: main direction Year 5, deliberate
  Year 3/4 retrieval, point-of-need differentiation, Australian English and Perth
  timezone. Existing count defaults remain unchanged unless explicitly overridden.
- One field-specific resolver feeds a schema-validated, hash-bound calibration
  snapshot into frozen context, agent projections, component references and direct
  finalisation checks. Actual timetable/focus sources remain necessary.
- A SQLite backend outside the distributable implements isolated teacher/class
  namespaces, atomic compare-and-swap revisions, fresh-connection read-after-write,
  standing/date/unit/lesson/progression scope, history, undo, forget and reset.
  Corrupt, unknown-version and conflicting state fails rather than silently resets.
- Optional host settings integration reads the configured private store on each
  run. Current overrides require a matching actual request source. The database
  path and namespace are not sent to generators. The host must authenticate the
  teacher; namespace keys and source labels are not authentication or an OS sandbox.
- A bounded conversational parser supports count overrides and recognised scope
  phrases. Ambiguous input returns a clarification state; proposals alone do not
  write. This is not a claim of general natural-language settings interpretation.
- Mandatory Year 4/Year 5 task-path checks are replaced by readiness and
  point-of-need requirements across runtime and QA. The old QA requirement has an
  explicit retirement mapping; historical evidence is not recertified.
- Complete and eight component packages carry per-file manifests and, for clean
  Git builds, source commit identity. A verifier checks a trusted external ZIP
  digest and optional source SHA before extraction, rejecting altered content,
  duplicate/unsafe paths, symlinks and pre-existing install destinations.
- Dependency audits reject changed complete and component installs. Failed static
  checks prevent execution of installed runtime code. CI retains exact source,
  packages, receipts and full deterministic test logs, and tests repeat-build
  equality without overwriting historical tracked distribution archives.

## Verification classes

The new tests exercise actual Python/SQLite/schema/CLI/package behaviour, including
clean extracted-package imports with `python -I`, fresh-process persistence,
concurrent writes and negative controls. Existing instruction-preservation tests
remain in the suite and are not mislabelled model-behaviour tests.

The test-first evidence is retained with the implementation handover: original
failures were observed before the corresponding changes. For final test counts,
read the exact candidate's CI `tests.log`; do not transfer a passing count from a
previous source revision. Successful package verification means integrity and
technical dependency closure, not educational acceptance.

No separate model or human independently reviewed this candidate in this session.
Self-inspection and deterministic tests are not independent code or lesson review.

## Unmet release gates

| Workflow gate | Current evidence limit |
|---|---|
| W0 baseline/host identity | Source and test baselines recorded; the user's active installed skill and production host are not verified. |
| W1 profile/release boundaries | The bounded profile and new calibration checks are executable and covered by negative/positive tests. This does not certify a generated pack. |
| W2 blind benchmark | The exact original mass/narrative PPTX and full review were not recovered. PR #9 remains separate; no blind review ran. |
| W3 creator operation | Runtime/settings behaviour is tested locally and in clean package processes. Actual production-host authentication, private-volume durability, backup and session activation remain unverified. |
| W4 real route | Actual provider commands, independent reviewer executions and a conforming canonical lesson renderer remain unconfigured/unverified. |
| W5 classroom usability | Feasibility planning and classroom-material improvements from the L/C backlog remain unfinished; no new real pack or target-PowerPoint walkthrough is claimed. |
| W6 acceptance/install | Technical package evidence is produced. The full weekday/counterfactual acceptance matrix, native host activation, teacher pilot and operational rollback are not complete. |
| W7 unattended operation | No actual schedule, interrupted-run recovery or final delivery acceptance was executed. |

The historical fixture needs these exact sources, not a reconstruction:

- `assets/qa-regressions/t3w8-tuesday-mass-narrative-known-failure.pptx`:
  SHA-256 `f9321b698a7b6c497ea4908e24aa7a90abe57cf83a8171f844395aefecc30ccd`.
- Its preserved full `review.md`:
  SHA-256 `0b82054ac8572b83e204ccb8882025679a53b79a0f364488cee264b06f9a0965`.

The current uploaded archives and targeted Google Drive searches did not yield
those originals. Missing evidence has not been fabricated or replaced by a new
file with the same name. The original 72-item backlog remains authoritative;
`STATUS.json` records this candidate's bounded progress, not completion of every
retained feature.

## Host configuration and migration

See `references/creator-settings-contract.md` and `docs/AGENT-ORCHESTRATION.md`
for the actual supported commands and JSON settings binding. Configure the
backend on a real private durable volume before claiming cross-session host
persistence. Do not commit database files or teacher request sources.

This is settings schema 1, calibration sidecar schema 1, run-context schema 2.
New contexts include source-hashed defaults/calibration. Regenerate frozen plans
when these inputs change. Existing immutable reports are not rewritten. Legacy
context without calibration may use only the existing documented count defaults;
caller-edited counts cannot bypass the resolver.

Unknown settings versions fail closed. There is no claim that an older package
understands new private state. A production rollback must preserve a private
backup, select the earlier matching package and test state compatibility. Do not
silently delete or downgrade the live database. Forget/reset removes values from
queryable store history, not from unrelated external backups.

## Distribution and acceptance

Tracked ZIPs under `dist/` are historical. Do not label them as this candidate.
Use the candidate from the successful exact-source CI run. Verify its external
digest and manifest before installing into a clean directory. An expected checksum
must originate from a trusted release record, not merely from an untrusted ZIP.

A candidate manifest or technical PASS never replaces the existing complete-pack
release authority. Do not merge/activate this candidate as classroom-ready until
independent review and the applicable assisted-release gates are satisfied.
