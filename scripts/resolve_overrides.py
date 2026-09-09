#!/usr/bin/env python3
"""Interpret a small explicit count/scope grammar without guessing standing intent.

This is not a general language interpreter. The host identifies the setting field
from the actual teacher conversation; unsupported or ambiguous phrasing requires
clarification. Source-document text never authorises a persistent write.
"""
from __future__ import annotations
import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import re
from teacher_context_store import SettingsStore, SettingsError, validate_scope, validate_values

WORDS = dict(zip(('one two three four five six seven eight nine ten eleven twelve thirteen fourteen '
                  'fifteen sixteen seventeen eighteen nineteen twenty').split(), range(1, 21)))
FIELDS = {'literacy_sequence_count', 'numeracy_prompt_answer_pairs'}


def propose_override(text: str, *, field: str, today: str, unit_id: str | None = None,
                     lesson_id: str | None = None, progression_id: str | None = None) -> dict:
    unclear = {'status': 'NEEDS_CLARIFICATION', 'reason': 'Specify the count, setting and explicit duration of the change.'}
    if field not in FIELDS or not isinstance(text, str):
        return unclear
    normal = ' '.join(text.lower().strip().rstrip('.').split())
    match = re.fullmatch(r'(?:please )?(?:set |use )?(\d+|[a-z]+)(?: (.+))?', normal)
    if not match or not match[2]:
        return unclear
    token, scope_text = match.groups()
    count = int(token) if token.isdigit() else WORDS.get(token)
    try:
        values = {field: count}
        validate_values(values)
        local_day = date.fromisoformat(today)
        if scope_text in ('from now on', 'as the default', 'ongoing'):
            scope = {'kind': 'standing'}
        elif scope_text in ('today', 'tomorrow'):
            day = local_day + timedelta(days=scope_text == 'tomorrow')
            scope = {'kind': 'date', 'start': day.isoformat(), 'end': day.isoformat()}
        elif re.fullmatch(r'on \d{4}-\d{2}-\d{2}', scope_text):
            day = date.fromisoformat(scope_text[3:])
            scope = {'kind': 'date', 'start': day.isoformat(), 'end': day.isoformat()}
        else:
            names = {'for this unit': ('unit', unit_id), 'for this lesson': ('lesson', lesson_id),
                     'for this progression': ('progression', progression_id)}
            if scope_text not in names:
                return unclear
            kind, identifier = names[scope_text]
            if not identifier:
                return {'status': 'NEEDS_CLARIFICATION', 'reason': 'A real ' + kind + ' identifier is required.'}
            scope = {'kind': kind, 'id': identifier}
        validate_scope(scope)
    except (ValueError, TypeError):
        return unclear
    return {'status': 'PROPOSED', 'values': values, 'scope': scope,
            'persistent_write_authorised': False}


def apply_override(proposal: dict, *, store: SettingsStore, teacher: str, classroom: str,
                   expected_revision: int, authority: dict) -> dict:
    if proposal.get('status') != 'PROPOSED':
        raise SettingsError('Ambiguous or unsupported instruction must not be saved')
    return store.change(teacher, classroom, proposal['values'], scope=proposal['scope'],
                        expected_revision=expected_revision, authority=authority)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', required=True)
    parser.add_argument('--field', required=True)
    parser.add_argument('--today', required=True, help="Teacher's actual local ISO date, resolved using the saved timezone")
    for name in ('unit-id', 'lesson-id', 'progression-id'):
        parser.add_argument('--' + name)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--store', type=Path)
    parser.add_argument('--teacher')
    parser.add_argument('--classroom')
    parser.add_argument('--expected-revision', type=int)
    parser.add_argument('--teacher-authorised', action='store_true')
    parser.add_argument('--source-id')
    args = parser.parse_args()
    try:
        proposal = propose_override(args.text, field=args.field, today=args.today, unit_id=args.unit_id,
                                    lesson_id=args.lesson_id, progression_id=args.progression_id)
        if args.apply:
            if args.store is None:
                raise SettingsError('An actual private store is required; no save occurred')
            authority = {'kind': 'teacher_request' if args.teacher_authorised else 'untrusted', 'source_id': args.source_id}
            result = apply_override(proposal, store=SettingsStore(args.store), teacher=args.teacher,
                                    classroom=args.classroom, expected_revision=args.expected_revision, authority=authority)
        else:
            result = proposal
        print(json.dumps(result, indent=2))
        return 1 if result.get('status') == 'NEEDS_CLARIFICATION' else 0
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
