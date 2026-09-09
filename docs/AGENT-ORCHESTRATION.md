# Daily Lesson Pack agent orchestration v2

## What this adds

`skills/registry.v2.json` is the executable control plane. The existing v1
registry remains the installation/discovery interface. Seven generator skills,
a Mathematics critic, two model-based pack reviewers and deterministic runtime
actors form a dependency graph. Logical roles are not claims that new hosted
skills or provider connections have been installed.

The runtime keeps context/component-record schema 2 and content/manifest schema
3. It uses the existing component validators, `pack_evidence.expected_checks`,
`stage_candidate` and `promote_release`. Only the existing complete release audit
can return RELEASED. This source change does not replace checked-in installation
ZIPs or activate itself in already-installed hosts.

## Installation and input preparation

Use Python 3.10 or newer and install the repository requirements:

```sh
python -m pip install -r requirements.txt
```

The host first resolves the teacher's requested date, timetable, year profile,
subject focuses, lesson status and any explicit overrides. It supplies a schema-1
request, and a schema-2 context matching `schemas/run-context.schema.json`.
This runtime validates and freezes resolved facts; it does not infer a timetable
or curriculum boundary from arbitrary source documents.

Required context additions are `generation_run_id`, `frozen: true`, a nonempty
`source_provenance` array of real SHA-256 hashes and `required_artifacts` including
`deck` and `briefing`. Each instance includes a safe unique ID, owner, HH:mm start,
positive duration and purpose. Required resolved fields must cite a source ID or
path listed in provenance. Year-profile source paths must point to the dedicated
repository profile; profile content must not be replaced by teacher context.
Repository references/year profiles resolve under the repository. User/runtime
source paths resolve under `--sources`. Context schema 2 remains compatible;
the added constraints apply at the v2 boundary.

Validate the frozen context and dependency plan without invoking any models:

```sh
python scripts/build_execution_plan.py --context runtime/context.json --sources runtime --out runs/plan-check
```

The output directory must be new. A deterministic plan is separate from mutable
execution state. A modified plan is rejected even when its syntax is valid.

## Host integration

There are two supported integration points: the `AgentAdapter` Python protocol,
and `JsonCommandAdapter`, which invokes explicitly configured argv lists with
JSON on stdin/stdout. There is no built-in paid API integration and no provider
credentials are requested, stored or installed. The trusted host implements
its provider/skill invocation using fresh contexts.

A host configuration has three execution keys and an optional private `settings` binding:

```json
{
  "agents": {},
  "assembly_command": null,
  "timeout_seconds": 300
}
```

The empty configuration is intentionally fail-closed, not a runnable mock.
Populate `agents` with an argv list for every scheduled generator and required
reviewer. For example, an operator's own adapter could be configured as
`["python", "/absolute/path/to/host_bridge.py", "--agent", "dlp-maths-lesson"]`.
The same bridge can handle multiple roles, but the review executions/actors must
be genuinely independent of every generation actor. All command paths should be
absolute: agent processes run in fresh temporary working directories. Commands
are not shell strings.

Each command receives `agent-request.schema.json`: identity, frozen context
hash/projection, actual instance, reference hashes/text, required check targets,
defects for repairs, input artifact paths and an exact output contract. The
component's `artefact` must equal that invocation's `output_contract.path`.
The coordinator, not the agent, publishes result files.

The host returns a wrapper with exactly `result`, `receipt`, and `transcript`:

```json
{
  "result": {"protocol_version": 1},
  "receipt": {
    "actor": "actual-host-actor",
    "execution_id": "actual-host-execution-id",
    "source": "external-runner"
  },
  "transcript": "raw transcript captured by the host"
}
```

Only the wrapper is illustrated above: `result` must be a complete component or
review result conforming to the named JSON schema. Identity and transcript come
from the actual host execution, not an LLM asked to invent them. Different strings
alone do not prove real independence. Receipts are auditable provenance, not
cryptographic proof; the host remains part of the trust boundary. Runtime
provenance review is executed locally and needs no configured agent command.

Run the first milestone:

```sh
python scripts/agent_orchestrator.py --request runtime/request.json --context runtime/context.json --sources runtime --config runtime/host.json --out runs/my-run --stop-after components
```

Exit 0 plus `COMPONENTS_VALIDATED` means every scheduled instance and required
Mathematics critic passed the handoff gates. It is not a deck or a classroom
release. Other failures exit nonzero and preserve evidence. A run directory is
single-use; start a new run after changing context or host configuration.

## Canonical assembly

This baseline repository does not contain a general-purpose pedagogical lesson
renderer. Supply `assembly_command` for the trusted host's repository-conforming
builder; otherwise the run stops before assembly. Do not substitute an ad-hoc
presentation writer to evade component or QA contracts.

The assembly command receives `ASSEMBLE_CANONICAL_PACK`, an output directory,
context/content/component-record paths, the root skill and ContentSource module
paths, and explicit no-rewrite/no-release permissions. It must preserve those
input bytes and return `{"status":"PASS"}` only after creating:

- `pack.pptx` and every other context-required deliverable, including the briefing;
- `manifest.json` schema 3 binding every delivered text element to canonical
  content, with actual file hashes and page counts;
- a genuine final render for every page of every deliverable, recorded in
  `manifest.renders` with artifact ID/page/file path/hash and artifact hash.

The canonical content contains tasks and optional `documents`. Put all visible
headings, reminders, labels and briefing text into those records during component
creation; the assembler cannot invent unreviewed prose. Use ContentSource to
read fields exactly. Shared metadata/document IDs must be unique across owners.

All artifact/render paths must be confined relative paths. The bridge retains
all declared files when calling the existing candidate staging function, then
runs the existing complete-pack binding audit. Each rebuild gets a separate
`assembly/revision-N/candidate` directory. Component records gain the actual deck
hash only after assembly; the original generation results remain unchanged.

## Independent QA, defects and repairs

Semantic and visual requests receive the final canonical content, artifacts and
renders, not generator component PASS assertions. Exact targets come from the
existing central QA registry's coverage planner. Every request binds the deck,
manifest, canonical content and QA-requirements hashes. A result must cover every
expected target exactly once and support observations with final-artifact
citations. Missing checks, stale hashes, contradictory PASS/FAIL or a FAIL without
an actionable defect are rejected. The deterministic provenance check supplements,
not replaces, the existing final repository audits.

Batch all reviewer defects before repair. Canonical task/instance ownership must
agree with the named repair owner. Only affected instances regenerate. Initial
generation, malformed-output retries, Mathematics-critic repairs and pack repairs
share the registry's cumulative per-instance attempt limit (default two).
Any content repair invalidates assembly and all applicable pack QA, not merely
the check that failed. New reviews require fresh host executions and current
hashes. Prior attempts and revisions are preserved.

Pack-level or ambiguous defects stop for explicit disposition; the runtime does
not guess which component to rewrite. Warnings are not silently waived. A run
with warnings but no blocking defects remains a candidate for disposition.
There is no automatic resume/import of partial state in this version.

For release, actual review envelopes are mechanically translated to existing v3
review files. Real host transcripts and hash-bound traces are preserved. The
existing release authority reruns its deterministic audits, checks complete
independent evidence and decides whether to promote. `UNREVIEWED` files created
for those audits are output slots, never assertions of PASS. Final typography
warnings still require legitimate dispositions. Omit `--stop-after components`
only after the host supports assembly and genuine independent review.

## Evidence and operational limits

`requests/`, `results/`, `components/`, `reviews/`, `defects/` and revision-specific
assembly/evidence directories retain immutable records. `plan/state.json`,
`metrics.json`, accepted pointers and `run-status.json` are coordinator state.
Pinned context, sources, reference files, results and final artifacts are
rehashed at boundaries. Timing, attempts, failure reasons and available token
counts are recorded; transport RETURNED is not acceptance PASS. Token costs and
classroom outcomes are not guessed when the host provides no such data.

Temporary working directories and logical ownership validation are **not an
operating-system security sandbox**. Configured commands are trusted code; use
an isolated runner for untrusted executables. Network access and process-tree
isolation belong to the host. Never point runtime sources at unrelated private
files or fabricate hashes/receipts to make a gate pass.

## Verification

```sh
python -m unittest discover -s tests -v
python scripts/build_chatgpt_package.py --out /tmp/daily-lesson-pack.zip
```

New tests use explicitly synthetic agents and a synthetic binding-only assembler.
Those fixtures must never be configured as production hosts or represented as
pedagogical/visual QA. Tests exercise concurrency, state transitions, malformed
handoffs, cumulative repairs, canonical staging, rendered-file coverage and
release refusal. A successful test run does not establish a real model's
teaching quality or complete a live provider integration.

## Creator configuration integration

Read `references/creator-settings-contract.md`. An optional `settings` object has
exactly `store`, `teacher` and `classroom`; the trusted host chooses an actual
private durable location and authenticated namespace. The CLI loads it before
freezing every fresh context. Request-only `instructional_overrides` and explicit
`instructional_scope` are verified against the actual request source and do not
become standing preferences. A corrupted configured store blocks the run.

No settings database is supplied, installed or activated by these source changes.
The host still needs genuine teaching/review commands and canonical assembly.
