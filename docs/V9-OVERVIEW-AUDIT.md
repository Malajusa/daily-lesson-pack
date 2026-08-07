# v9 overview update audit

Audit date: 2026-08-07

Compared the authoritative installed snapshot (`VERSION` = `2.0.0-chatgpt`) with `Daily-Lesson-Pack-v9-Overview-Update.zip`.

## Conclusion

The installed skill contains **some v9 behaviour, but not the complete v9 overview update**. Treat the v9 update as **partially applied**. Do not overwrite the installed baseline until the missing v9 rules are deliberately merged and regression-tested.

## Present in the installed skill

- Default progression: assume the previous scheduled lesson was sufficiently completed unless an authoritative exception says otherwise; missing status is not evidence of a missed lesson.
- Term 3 mathematics weekly topics and WA codes are available through `references/year-4-5-maths-overview.json`.
- Guided-reading weekday bands exist: Monday very low, Tuesday low, Wednesday at level, Thursday above level, Friday approximately Year 9/high.
- An Information Report unit/toolkit sequence exists in `references/english-planning-rules.md`.
- Morning Work, Shared Reading and Guided Reading are required to use genuinely different passages/functions.

## Missing or materially different from v9

- `references/term-3-four-day-overview.md` and `.json` are absent from the installed skill and its required-reference routing.
- The deterministic Monday/Tuesday/Thursday/Friday day-level mathematics arc is absent. The installed timetable still treats Wednesday as a normal mathematics/literacy planning day.
- The v9 rule that Wednesday is outside the four-day overview unless explicitly requested is absent.
- The weekly Information Report toolkit component with Monday analyse / Tuesday explicitly teach / Thursday apply / Friday edit-consolidate-publish is absent as a deterministic term-week lookup.
- Country allocations for Shared and Guided Reading are absent. The installed skill does not enforce Europe/Africa/North America/South America selection or different assigned countries per day.
- The v9 pre-export checks tied specifically to the four-day overview are absent.
- The v9 tests for Term 3 Week 5 Monday and Tuesday are not part of the installed regression matrix.
- HASS appears in the timetable and automation references; there is no v9-specific rule preventing HASS generation from the four-day overview.

## Recommended merge

Create a separate change from this baseline that adds the two overview references, routes them from `SKILL.md`, incorporates the v9 source-index addendum, and adds the two v9 regression fixtures. Preserve newer installed rules where they do not conflict. Resolve the Wednesday/timetable conflict explicitly rather than silently replacing one rule with the other.
