#!/usr/bin/env python3
"""Audit declared interactive lesson coverage; never certify teaching quality.

Input: {source_sha256, expected_lessons: [id], lessons: [{id, goal, title,
success_criteria: [text], concept_boundary, representation_purpose, exit_task,
scenes: [{id, role, prompt, explanation, notation, representation, states: [id]}]}],
reviews: [{lesson_id, scene_id, state_id, source_sha256, domain, observation, evidence}]}.
Roles meaning/model/guided require correspondence fields. Independent/transfer
tasks may deliberately withhold diagrams. Reviews are declarations for coverage,
not authenticated independent execution receipts or semantic proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

DOMAINS = ('mathematics', 'instruction', 'visual', 'software')

def audit(record: dict, source: bytes) -> dict:
    issues: list[dict] = []
    def fail(code: str, where: str):
        issues.append({'code': code, 'location': where})
    actual_hash = hashlib.sha256(source).hexdigest()
    if record.get('source_sha256') != actual_hash:
        fail('SOURCE_BINDING', 'source_sha256')
    expected = record.get('expected_lessons', [])
    lessons = record.get('lessons', [])
    ids = [lesson.get('id') for lesson in lessons]
    valid_ids = all(isinstance(value, str) and value.strip() for value in [*expected, *ids])
    if not expected or not valid_ids or len(set(expected)) != len(expected) or sorted(ids) != sorted(expected):
        fail('INVENTORY', 'lessons')
    review_keys: set[tuple] = set()
    for lesson in lessons:
        lid = lesson.get('id', '')
        if not isinstance(lid, str) or not lid.strip():
            fail('LESSON_ID', str(lid))
            lid = str(lid)
        goal_value = lesson.get('goal')
        goal = goal_value.strip() if isinstance(goal_value,str) else ''
        if not goal or goal.casefold().rstrip('.') == str(lesson.get('title','')).casefold().rstrip('.'):
            fail('AUTHORED_GOAL', lid)
        for field in ('concept_boundary', 'representation_purpose', 'exit_task'):
            if not isinstance(lesson.get(field),str) or not lesson[field].strip():
                fail('PLANNING_FIELD', lid + '.' + field)
        criteria = lesson.get('success_criteria')
        if not isinstance(criteria, list) or not criteria or any(not isinstance(c,str) or not c.strip() for c in criteria):
            fail('SUCCESS_CRITERIA', lid)
        scenes = lesson.get('scenes', [])
        scene_ids = [scene.get('id') for scene in scenes]
        if not scenes or len(set(scene_ids)) != len(scene_ids):
            fail('SCENE_INVENTORY', lid)
        for scene in scenes:
            sid = scene.get('id', '')
            if not isinstance(sid,str) or not sid.strip():
                fail('SCENE_ID', lid)
                sid = str(sid)
            if scene.get('role') not in ('meaning','model','guided','independent','transfer','misconception','finish'):
                fail('SCENE_ROLE', lid + '/' + sid)
            if scene.get('role') in ('meaning', 'model', 'guided'):
                for field in ('prompt', 'explanation', 'notation', 'representation'):
                    if not isinstance(scene.get(field),str) or not scene[field].strip():
                        fail('TEACHING_STATE', lid + '/' + sid + '.' + field)
            states=scene.get('states', [])
            if not isinstance(states,list) or not states or any(not isinstance(state,str) or not state.strip() for state in states) or len(set(states))!=len(states) or 'entry' not in states:
                fail('STATE_INVENTORY', lid + '/' + sid)
                states=[]
            review_keys.update((lid, sid, state, domain) for state in states for domain in DOMAINS)
    declared = set()
    for review in record.get('reviews', []):
        key = (review.get('lesson_id'), review.get('scene_id'), review.get('state_id'), review.get('domain'))
        if key not in review_keys or key in declared:
            fail('REVIEW_IDENTITY', '/'.join(str(v) for v in key))
        if review.get('source_sha256') != actual_hash:
            fail('STALE_REVIEW', '/'.join(str(v) for v in key))
        if not review.get('observation') or not review.get('evidence'):
            fail('REVIEW_EVIDENCE', '/'.join(str(v) for v in key))
        declared.add(key)
    missing = sorted(review_keys - declared)
    return {'structure': 'FAIL' if issues else 'PASS', 'issues': issues,
            'lessons': len(lessons), 'scenes': sum(len(l.get('scenes', [])) for l in lessons),
            'source_sha256': actual_hash, 'missing_review_coverage': missing,
            'teaching_quality': 'UNVERIFIED',
            'scope': 'Structural coverage only. Declared reviews do not prove independent judgement or classroom readiness.'}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = audit(json.loads(args.contract.read_text(encoding='utf-8')), args.source.read_bytes())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('missing_review_coverage', 'issues')}))
    return 1 if result['issues'] or result['missing_review_coverage'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
