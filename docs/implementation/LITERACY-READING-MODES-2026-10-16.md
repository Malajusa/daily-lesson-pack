# Optional literacy checks and whole-text comprehension

Bounded source update from main f5415fd10a444838a9d56a56ffb0a25525c2494b.

## Ownership

Malajusa/daily-lesson-pack owns the Workflows component contracts and canonical
contract audit. Installed Workflows 0.2.3 also contains deliberate private
portable-execution and renderer overlays. Deploy only a three-way reconciled
partial update preserving those overlays. Portable 1.0.0 is a separate,
self-contained package with its own generation ownership; it is not changed by
this source update. No linked Portable git source was found in its inspected
manifest or scoped repository search. Do not overwrite it with Workflows.

## Validation

- 300 tests completed, OK with one existing skipped test, including 23 new
  positive/negative tests. The initially missing isolated-Python jsonschema
  dependency was supplied in a task-specific verification environment; no
  global/security/network settings were changed.
- Complete package plus eight standalone packages passed archive identity checks.
- Four synthetic example decks passed the contract audit: ten supported literacy
  items (30 slides), mixed optional checks/retry (9), paragraph-local (2) and
  whole-text (13). The examples are regression demonstrations, not a full day.
- Current installed renderer used unchanged. All four renders passed its rendered
  inspector, typography and containment checks. Contact sheets and selected
  individual slides were inspected; the complete one-page source PDF was also
  visually inspected. Rendering uses Nimbus Sans in place of unavailable
  Trebuchet MS; PowerPoint playback was not tested. Layout solver low-fill
  diagnostics were reviewed against readable full-width task/answer panels;
  final rendered inspectors reported no warnings.
- A separate reviewer inspected the exact source diff, actual rendered examples,
  source/inference content and raw test evidence. Reported selection-source,
  feedback-identity and think-aloud-type defects were repaired with negative
  regressions. Final bounded review found no remaining merge-blocking defect.

## Migration and rollback

Legacy supported and paragraph-local decks keep their existing headers and need
no new notes records. Selected new modes require the notes evidence specified
in references/literacy-reading-modes.md. Rebuild both complete and component
packages so the audit helper/reference/QA registry remain dependency-closed.
Updated QA requirements intentionally require fresh review coverage; old pack
PASS records do not release newly authored content.

Rollback by reverting this bounded source commit and rebuilding from the accepted
revision. For the installed Workflows package, retain the pre-update release and
use its existing private update workflow; do not change sharing or Portable.

## Limits

No pupil data or classroom trial was used. Source availability in the packet is
not proof that pupils received the handout. No live new-account generation,
classroom effectiveness or complete-pack release is asserted. Merge evidence,
CI and actual installed release readback must be recorded separately after those
actions succeed; this file does not pre-claim them.
