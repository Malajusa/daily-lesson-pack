# Repository work

Read `docs/DEVELOPMENT.md` and the controlling product decisions in
`docs/implementation/DECISIONS.md`. Keep the supplied backlog and dependencies;
record actual progress separately from its original handoff status.

- `/change`: one implementer owns one bounded issue; integrate its code, schemas,
  consumers, package dependencies and meaningful positive/negative regressions.
- `/regress`: use synthetic fixtures and distinguish executable checks from
  live-agent, rendered-artefact and classroom evidence.
- `/audit`: a separate reviewer examines the issue, diff and test evidence, with
  no implementer private reasoning. Report defects; the implementer owns repairs.
- `/release`: verify the exact candidate with existing release services. Do not
  repair content while reviewing it or manufacture execution/PASS records.

Use feature branches and preserve unrelated work. The integrator owns shared
schema changes. Do not merge automatically or activate an installed skill as
part of a source-only change. Document migration/rollback, package checks,
independent review and concrete host blockers in each PR.

Never commit private classroom evidence or settings. The portable defaults and
the user's private state have separate ownership and release requirements.
