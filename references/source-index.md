# Source Index

Use this registry to identify authoritative, active, companion, and superseded planning sources. Update it when the teacher provides a replacement.

## Current project

- Class: Year 4/5
- Jurisdiction: Western Australia
- School year: 2026
- Current planning term: Term 3

## Bundled operational sources

| Area | Source | Status | Notes |
|---|---|---|---|
| Current timetable | `references/2026-term-3-timetable.yaml` | Active companion | Machine-readable mapping derived from the teacher-supplied Term 3 timetable. A later teacher-supplied timetable overrides it. |
| Mathematics yearly sequence | `references/year-4-5-maths-overview.json` | Active companion | Structured 40-week Year 4/5 sequence and WA codes. |
| Term 3 four-day overview | `references/term-3-four-day-overview.json` | Active for Mon/Tue/Thu/Fri daily planning | Deterministic Term 3 week/day mathematics focus, Information Report toolkit stage and country-reading allocation. Wednesday is not controlled by this overview unless explicitly requested. |
| Term 3 four-day overview rules | `references/term-3-four-day-overview.md` | Active companion | Explanatory rules for the deterministic overview lookup. |
| Mathematics code descriptors | `references/wa-maths-code-map.json` | Active companion | WA Year 4/5 Mathematics code lookup. |
| Mathematics weekly method | `references/weekly-maths-pack-patterns.md` | Active | Weekly plan, slides, printables, differentiation, and assessment patterns. |
| Mathematics lookup | `scripts/maths_week_brief.py` | Active | Run before planning a specified term/week. |
| English curriculum | `references/wa-year-4-5-english-curriculum.md` | Active companion | Condensed operational Year 4/5 WA English reference. A later teacher-supplied curriculum file overrides it. |
| English pedagogy | `references/evidence-based-english-pedagogy.md` | Active | Evidence-based reading, writing, intervention, and block-design principles. |
| English unit sequence | `references/english-planning-rules.md` | Active | Revised Information Report sequence, shared-reading and guided-reading integration, and literacy-block rules. |
| RBPS guided reading | `references/rbps-guided-reading-framework.md` | Active | Operational summary of the teacher-supplied school guided-reading framework and reading-strategy materials. |
| Friday assembly cycle | `references/assembly-cycle.md` | Active | Odd weeks are Friday Literacy; even weeks are assembly at the undercover area by 8:35. |
| Slide standards | `references/slide-deck-quality-standards.md` | Active | Plan-to-slide alignment, Morning Work first-slide rule, LI/SC and readability requirements. |
| Daily pack quality floor | `references/daily-pack-quality-floor.md` | Active | Mandatory instructional, differentiation, cross-file and rendered-QA release gates. |
| Daily slide benchmark | `assets/daily-teaching-slides-quality-template.pptx` | Active template | Use its visual system as the minimum standard while applying the current first-slide and reading-package rules. |
| Daily lesson status | Maintained Sheet, file, or teacher update | Required | Interpret using `planning-state-schema.md`. |
| Calendar interruptions | Google Calendar or teacher-provided calendar | Required when available | Read before finalising a dated day plan. |

## Original teacher-supplied source names

Use these names when resolving attached or connected files:

- `2026 Term 3 timetable draft.pptx`
- `2026 year level overview 4-5(1).pdf`
- `curriculum.pdf`
- `Pasted text(1).txt`
- `SKM_C451i26073015550.pdf`
- `SKM_C451i26073015540.pdf`
- `2026-07-30_Daily-Teaching-Slides_Quarters-Corrected.pptx`

The bundled references are operational companions, not replacements for a later teacher update.

## Superseded sources

- `Pasted markdown(6).md` - original 20-lesson Information Report sequence. Do not use for lesson progression.
- Any Term 1 timetable when planning Term 3.
- The earlier Mathematics pack that skipped explicit partitioning instruction.
- The original 30 July daily deck reused unchanged: retain the approved visual system through the bundled template, but remove the decorative cover, make Morning Work first, and add the required shared/guided reading package.
- Conversation summaries that conflict with a later explicit teacher instruction or active source.
- Standalone weekly-maths-pack instructions that conflict with the integrated Mathematics references.

## Resolution rules

1. Prefer a current explicit teacher instruction over all earlier material.
2. Prefer an active source over an older similarly named source.
3. Use document content, not upload date alone, to determine currency.
4. A current calendar event overrides the normal timetable for that date.
5. A status record controls immediate progression; the unit overview controls sequence and intent.
6. For Term 3 Monday/Tuesday/Thursday/Friday daily packs, `term-3-four-day-overview.json` controls the day-level mathematics focus, Information Report toolkit stage and country allocations, subject to explicit current user/status exceptions. Wednesday remains governed by the timetable and active plans unless overview use is explicitly requested.
7. For Mathematics, the calendar week identifies the intended focus; absent contrary status, advance through the scheduled sequence rather than reteaching because status is missing.
8. Do not treat a prior-year or earlier-term prerequisite as secure without evidence.
9. Resolve Friday assembly by term-week parity before planning or generating slides.
10. HASS is not supplied by the four-day overview; use a separate authoritative HASS plan or explicit instruction if HASS resources are required.
11. If bundled JSON or Markdown conflicts with a later teacher-supplied overview or curriculum file, use the later source and update the operational companion before future packs.
