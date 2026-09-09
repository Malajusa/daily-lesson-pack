# Controlling decisions and superseded variants

Prepared 8 September 2026. This is the implementation authority distilled from the conversation, not a record of completed code changes.

## Confirmed teacher requirements

| ID | Governing decision | Implementation consequence |
|---|---|---|
| DEC-01 | The creator's needs take priority over generic shareability. | Ship and select creator defaults automatically. Protect that workflow on every change. |
| DEC-02 | Main teaching is predominantly Year 5 for the creator. | Centralise this as the built-in curriculum direction; do not scatter Year 5 assumptions in universal agents. |
| DEC-03 | Warm-ups deliberately retrieve Year 3/4 foundations for the creator. | Configure a typical retrieval emphasis, not an exclusive band or a learner ceiling. Earlier prerequisites and ready-learner challenge remain possible. |
| DEC-04 | Enrolment year is not readiness. | Select task-specific support and challenge using evidence; remove year-based pathway checks in code, prompts and QA. |
| DEC-05 | The skill should remember requested changes. | Use a real private, versioned store with truthful write acknowledgements and scope/expiry semantics. |
| DEC-06 | Routine use should not repeat setup. | Load known defaults, saved settings and valid sources automatically; ask only for genuinely missing material facts. |
| DEC-07 | Sharing must remain possible across different year levels. | Allow optional isolated recalibration and explicit profile/domain maturity without changing creator defaults. |
| DEC-08 | Implement the retained brainstorming, not another unbounded feature discussion. | Every retained capability is allocated to a bounded issue, acceptance test and milestone; later ideas do not block initial useful delivery. |

## Retained proposals are features, not invented permanent preferences

The latest request brings unopposed feature ideas into implementation scope. It does not establish that every earlier illustrative number, algorithm weight, label or sample JSON value is an approved permanent personal setting.

Five literacy sequences are a proposed starting policy for the reviewed ten-minute block. Implement the policy consistently and evaluate the actual tasks. Do not turn it into an unconditional global rule or represent it as an explicit saved teacher preference without an instruction.

Likewise, 65–75 slides is a historical revision target for that pack, not a release threshold. Lean style, print avoidance, exact retrieval intervals, novelty thresholds and friction cut-offs remain configurable proposals. Use measured evidence and teacher direction rather than silently promoting them.

## Replacements: implement the right-hand version only

| Earlier proposal | Governing replacement |
|---|---|
| Keep the creator's settings runtime-only or require selecting their preset. | Creator's confirmed, non-sensitive defaults ship selected; private facts stay separate. |
| Make everybody complete formal setup before use. | Creator uses defaults immediately; other teachers can accept them or opt into recalibration. |
| Reask curriculum/direction on every run. | Reuse explicit saved configuration and valid planning sources; resolve only missing or conflicting facts. |
| Never remember preferences because memory is unreliable. | Reject unrecorded recall, but support authorised persistent settings with real storage and provenance. |
| Split Mathematics into Year 4 and Year 5 pathways. | Common direction with evidence-based support, prerequisite intervention, practice and challenge. |
| Rename fixed year/ability streams Support/Core/Challenge. | Conditional resources and teaching responses, not permanent membership or compulsory three-tier tasks. |
| Use a profile's allowed year range as a learner ceiling. | Validate the skill's curriculum coverage; use evidence and authorised scope for support/extension. |
| Change the Literacy default to five everywhere. | Resolve count from authorised preferences, timetable and task feasibility; test the reviewed ten-minute case with five. |
| Release only decks inside a universal slide-count limit. | Release based on executable delivery, access and learning evidence; counts are diagnostic signals. |
| Create many additional agents or competing QA systems. | Reuse specialists and central QA; add deterministic services and selective independent review where warranted. |
| Different review IDs or a YAML flag alone prove independence. | Require actual independent executions, transcripts/receipts and correct evidence bindings. |
| Freeze classroom groups because run context is frozen. | Freeze run provenance; learner support can change with later evidence recorded in new snapshots. |
| Use a universal 0–5 evidence/ZPD/ability score. | Record what happened, the skill/task, assistance, independence and transfer conditions. |
| Assume planned or scheduled teaching establishes mastery. | Distinguish planned, taught, attempted, supported success and independent evidence. |
| Let compression rewrite accepted content or skip QA. | Route semantic changes to owners, revalidate the plan, rebuild and rerun applicable independent review. |
| Recheck only one failed check after a content change. | Reuse untouched content, but rerun complete applicable pack QA against the changed final artefacts. |
| Static PowerPoint enforces student think time. | Encode order/teacher hold points; enforcement exists only if the actual host supports it. |
| Prior patch files are apply-ready implementations. | The supplied v2 patch fails Git syntax parsing; rebuild from a pinned checkout with executable code and tests. |
| Earlier brief says creator defaults must never ship. | Superseded by the later explicit creator-first default requirement. |
| Teacher overrides can waive every check. | Overrides may adjust authorised preferences or permitted warnings; accuracy, material access and evidence integrity remain required. |

## Deliberately not assumed

No live host integration, persistence backend, installed package identity, current school timetable, curriculum jurisdiction/version, new profile calibration, student attainment, root cause of the reported clipping, or classroom improvement is assumed from prior assistant descriptions.

Authoritative current sources are needed for factual planning. Default direction cannot invent the current lesson, number of print copies or equipment availability. The original deck and its review are diagnostic evidence, not proof of what runtime produced them.

## Changing this ledger

Changes require a later explicit teacher instruction or a clearly recorded implementation decision that does not contradict those instructions. Record the change, affected issues, migration and new tests. Do not restore a superseded idea merely because it is easier to implement.
