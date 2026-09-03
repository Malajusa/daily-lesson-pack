# Component instance and time-budget contract

Component ownership is not scheduling identity. A day may contain two or more
instances owned by the same component skill. Each scheduled instance therefore
has a unique `id`, an `owner`, a start time, an available duration and a stated
purpose.

Use schema version 2 for the context and component-acceptance records.

```json
{
  "timetable_instances": [
    {
      "id": "maths-1",
      "owner": "dlp-maths-lesson",
      "start": "08:30",
      "duration_minutes": 60,
      "purpose": "explicit teaching and guided practice"
    },
    {
      "id": "maths-2",
      "owner": "dlp-maths-lesson",
      "start": "10:50",
      "duration_minutes": 60,
      "purpose": "independent application and exit evidence"
    }
  ]
}
```

The component-acceptance record repeats each scheduled instance and records one
evidence-bearing result for it. Repeated owners are valid; repeated instance
IDs are not.

Every instance must record:

- `instance_id`, matching the context record;
- `owner`;
- `status`;
- `estimated_minutes`, no greater than the scheduled duration;
- an `artefact` or `slide_range`;
- `checks`, with stable check IDs, `PASS`/`FAIL`, and concrete evidence.

The record also includes a top-level `generation_run_id`. Component checks are
completed before assembly; after assembly, add the final deck SHA-256 without
altering the check evidence. Independent semantic and visual reviews cite that
generation run and use different review run IDs.

A lesson split by recess, lunch or another timetable block must show a visible
breakpoint. Do not represent two scheduled Mathematics blocks as one
undifferentiated component merely because both use `dlp-maths-lesson`.

Before generation, prepare a slide/time budget for every instance. The budget
must account for student response time, discussion, transition and handling
resources—not just teacher talk. If estimated time exceeds available time,
reduce scope or ask for a decision before building the deck.

Component `PASS` is an input to independent QA, not evidence by itself. Freeform
strings such as `checked` or `all checks passed` are invalid.
