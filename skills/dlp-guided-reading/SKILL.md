---
name: dlp-guided-reading
description: Represent the scheduled Guided Reading block and authorised Alpha-Epsilon group name in a Daily Lesson Pack timetable without generating Guided Reading materials.
---

# DLP Guided Reading

## Current scope

Guided Reading is **timetable-only for now**.

When Guided Reading is scheduled:

- show the block in the timetable or day-at-a-glance;
- use only the group name supplied by an authoritative current timetable or plan;
- permit only `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon` as group labels;
- if no authorised group is available, display `Guided Reading` without guessing a group.

Do not generate:

- a Guided Reading title or transition slide;
- student texts or passages;
- vocabulary support;
- teacher prompts or expected responses;
- comprehension or inference questions;
- extended responses;
- independent class tasks tied to the Guided Reading block;
- country labels or ability descriptors.

## Group-language boundary

Never display labels such as `very low`, `low`, `below level`, `at level`, `above level`, reading age or year-level complexity. Do not infer that `Alpha` through `Epsilon` maps to a particular ability order.

## QA

Fail if:

- any Guided Reading instructional slide or material is generated;
- any group label other than `Alpha`, `Beta`, `Gamma`, `Delta` or `Epsilon` appears;
- an allowed label was guessed rather than taken from an authoritative schedule;
- a country or ability description is presented as the group name;
- the scheduled Guided Reading block is omitted from the timetable.
