# T3W8 Tuesday bypass known-failure regression

## Purpose

This record captures the failure class exposed by the Tuesday Term 3 Week 8 pack request where the normal Daily Lesson Pack workflow could be bypassed by treating a request for a PowerPoint/Python script as permission to generate a deck outside the repository runtime. It is a release regression, not a content exemplar.

Use this benchmark whenever routing, generation entry points, packaging, component acceptance, presentation QA or release certification changes.

## Failure class A — unsupported generation path

FAIL when a Daily Lesson Pack is authored by an ad-hoc presentation script instead of the repository runtime and component contracts.

PASS only when:
- the request is resolved through the Daily Lesson Pack orchestrator;
- a request for a Python script still invokes the repository runtime rather than recreating lesson generation independently;
- current runtime sources remain authoritative for date, week, timetable, lesson focus and overrides;
- the resulting artefacts remain candidates until complete independent release evidence exists;
- no deck is described as classroom-ready merely because a generator completed successfully.

## Failure class B — Morning Work drift

The observed failure demonstrated why Morning Work must not be treated as generic filler.

PASS only when Morning Work:
- remains independent revision rather than new teaching;
- includes cumulative arithmetic retrieval across the four operations where that is the authorised numeracy revision contract;
- includes appropriate mathematical vocabulary retrieval;
- keeps literacy revision focused on already-taught grammar and punctuation;
- is executable directly from the projected slide without requiring the teacher to teach missing background knowledge;
- remains visually scannable and comfortably contained.

## Failure class C — Numeracy warm-up contract

PASS only when:
- the default warm-up contains five prompt/answer pairs, not an arbitrary expanded set;
- each prompt contains genuinely separate All, Most and Some tasks;
- every meaningful task and primary answer is at least 36 pt;
- substantive `Why` text remains at least 28 pt and actually explains the mathematical relationship rather than giving a generic checking instruction;
- question slides do not reveal their own answers;
- answer slides fully match the requested representation, reasoning or calculation.

## Failure class D — Literacy warm-up quality

PASS only when:
- each item is self-contained and asks for one clear response unless an override authorises more;
- reminder, question and answer all teach the same grammatical or punctuation rule;
- a multiple-choice distractor is plausible enough that the target rule, not superficial length or wording, distinguishes the answer;
- sentence-combination tasks explicitly say to combine or join the supplied sentences;
- technical terms such as conjunction and pronoun are used accurately and explained in student-friendly language;
- punctuation or wording changes are visually locatable on the answer slide without relying on colour alone.

## Failure class E — Shared Reading integrity

PASS only when Shared Reading:
- uses the authorised current reading focus and year-profile pitch;
- presents one short paragraph and one question on each question slide;
- immediately follows each question slide with its matched answer slide;
- does not reveal the answer on the question slide;
- keeps paragraph, question and answer semantically aligned;
- maintains projected readability instead of shrinking dense text to fit.

## Failure class F — timetable and runtime fidelity

PASS only when:
- the exact requested day is resolved from current runtime sources;
- the timetable determines component order and repeated lesson instances;
- lesson focus comes from the supplied current overview/program or explicit user override;
- missing essential runtime context blocks classroom-ready release rather than being filled from memory;
- specialist blocks remain timetable labels unless an authorised component contract explicitly allows more.

## Failure class G — release evidence

A rendered PPTX is not release evidence.

PASS only when:
- every scheduled component instance has evidence-bearing acceptance records;
- the final deck hash is bound to those records;
- deterministic contract, profile, typography, containment and visual checks apply to the same artefact;
- independent semantic and rendered review records use separate reviewer/run identities;
- all unresolved warnings block release;
- `scripts/audit_release_bundle.py` returns PASS for the exact deck and manifest being delivered.

## Required regression use

When this benchmark applies, review the complete pack rather than checking only the originally observed defect. Any recurrence of the unsupported generation path, Morning Work drift, warm-up contract failure, weak distractor, pronoun/terminology error, Shared Reading mismatch, runtime/timetable substitution or missing release evidence is a release-blocking failure.