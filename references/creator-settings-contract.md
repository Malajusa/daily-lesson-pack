# Creator defaults and authorised settings

## Authority and first use

The automatically selected public defaults are predominantly Year 5 main
curriculum direction, deliberate Year 3/4 foundational retrieval, point-of-need
differentiation, Australian English and Australia/Perth. These are preferences,
not claims about enrolment, individual attainment or verified curriculum coverage.
`config/creator-defaults.json` is the machine-readable source. The existing
architecture still supplies ten Literacy sequences and five Numeracy pairs unless
an authorised preference changes the count. Five Literacy sequences for one
particular reviewed lesson is not a newly imposed universal default.

The precedence for each supported field is current explicit instruction, relevant
scoped override, standing classroom preference, then public default. A temporary
override expires to the latest standing preference, not to the value that happened
to exist when that temporary override was created. Lesson scope is more specific
than dated scope; dated scope outranks unit/progression scope. Overlapping scopes
at the same specificity use the latest authorised revision.

The supported persisted fields are active year profile, main curriculum year,
retrieval years, differentiation mode, locale, timezone, Literacy sequence count
and Numeracy pair count. Date, timetable, focus, class size, printing quantities,
student names, diagnoses and attainment are not preferences in this store. Current
lesson facts still require their own valid sources. A locale choice does not
certify another jurisdiction's curriculum.

## Real storage, not conversational recall

The trusted host configures `settings` in its private host JSON with exactly
`store`, `teacher` and `classroom`. The store must be on a private durable volume
outside the repository and installed package. Namespace identifiers are supplied
by the authenticated host, not inferred from student material. No database or
private binding is distributed in skill packages.

The orchestrator CLI loads that namespace for each fresh run. An absent first-use
database means no saved overrides. An unreadable, corrupt or future-version store
is an error; do not substitute defaults and call the load successful. A fresh
Python process test proves process persistence, not persistence of a transient
ChatGPT container or activation in an external host.

A minimal host binding looks like this; replace the illustrative values in the
host's private configuration, not in this repository:

```json
{"settings":{"store":"/private/dlp/settings.sqlite","teacher":"teacher-id","classroom":"class-id"}}
```

The existing agent-command and assembly-command fields remain required for actual
production execution. Configuring settings does not configure a teaching model,
renderer, scheduler or delivery channel.

## Authorised operations

Use `scripts/teacher_context_store.py` with `show` or `export` for the current
namespace snapshot. For `change`, `undo`, `forget` or `reset`, supply the current
`--expected-revision`, the actual teacher request's `--source-id`, and the trusted
host's `--teacher-authorised` assertion. The last flag is **not authentication**;
the host must enforce identity, authority, OS permissions and command permissions.
Generators and attached documents must not receive this write capability.

`change` accepts a JSON `--values` object and one explicit JSON `--scope`:

- `{"kind":"standing"}` persists until superseded, forgotten or reset.
- `{"kind":"date","start":"2026-09-10","end":"2026-09-10"}` applies to the inclusive date interval.
- `{"kind":"unit","id":"unit-id"}`, lesson or progression scope applies only when the same explicit identifier is supplied for the requested run.

Only acknowledge a save after the transaction commits and a new connection reads
back that exact revision. A stale expected revision fails rather than overwriting
a concurrent change. Undo appends a revision. Forget removes the selected fields
from queryable history too, so undo cannot resurrect them; reset does this for all
supported preferences. Export returns the current snapshot, not an undeclared
backup of the host's database. Secure deletion from OS snapshots/backups is the
host operator's responsibility.

`scripts/resolve_overrides.py` recognises a deliberately bounded grammar for the
two warm-up count fields: for example, `five from now on`, `three tomorrow`,
`use 4 on 2026-10-01`, and `five for this unit`. The host supplies the field, the
teacher's actual local date and any required scope identifier. Bare counts,
missing unit identifiers and unsupported phrasing return `NEEDS_CLARIFICATION`.
Do not claim general natural-language coverage or guess a standing scope. Its
read-only proposal does not grant write authority. `--apply` also requires the
same real-store, revision and teacher-authority inputs as a structured change.

## Frozen execution and independent QA

For current-run changes, put `instructional_overrides` in the actual hashed
request JSON. Explicit scope selection belongs in `instructional_scope`, using
`unit_id`, `lesson_id` or `progression_id`. The CLI verifies the request against
its source file, loads settings without modifying them, and writes an immutable
private calibration sidecar. Credentials, database paths and namespace bindings
are not projected to teaching agents.

`schemas/instructional-calibration.schema.json` version 1 is a sidecar to context
schema 2. Every resolved value has source, revision and scope. Creator defaults,
architecture defaults and profile metadata are hash-bound. A source-backed
sidecar determines warm-up counts; a caller cannot substitute a different count
at finalisation. Current profile selection must agree across calibration and the
frozen context. Changing profile does not carry creator-only retrieval bands into
the new profile. Unsupported main-curriculum coverage remains a candidate rather
than silently becoming a calibrated classroom release.

All generators and reviewers receive the same calibration. They may not save
preferences, invent prior achievement or replace conditional support with fixed
year/ability membership. `MATHS.POINT_OF_NEED` and `MATHS.READINESS.CHECK` replace
the retired Year 4/Year 5 pathway checks. The central QA requirement has a new ID;
old review evidence does not certify its new meaning. Requirements presence and
runtime check coverage do not, by themselves, prove a model's teaching judgement.

## Upgrade and rollback

Keep private storage outside versioned installation directories. Back up the
private store through the host's controlled process before an upgrade; do not add
it to a portable archive. Unknown database/schema versions fail closed. This
candidate adds SQLite schema 1, so there is no historical private schema migration
to claim. Earlier package versions that do not read this store must not reset or
rewrite it. Rollback compatibility and active-host behaviour require a real host
trial. Previously frozen runs and reviews are not rewritten during an upgrade.
