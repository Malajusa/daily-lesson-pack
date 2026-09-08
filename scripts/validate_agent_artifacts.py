#!/usr/bin/env python3
"""Validate exact review coverage, ownership and current-hash result envelopes."""
from __future__ import annotations

import argparse
import copy
from collections import defaultdict
from pathlib import Path

from agent_protocol import (ProtocolError, read_json, sha256_file, sha256_json,
                            validate_json, write_json_atomic)


def defect_instance(defect: dict, content: dict, manifest: dict) -> str | None:
    instances = {i['id']: i['owner'] for i in content['instances']}
    tasks = {t['id']: t['instance_id'] for t in content['tasks']}
    instance_id = defect.get('instance_id')
    required = {'instance': ('instance_id',), 'task': ('task_id',),
                'page': ('artifact_id', 'page'), 'pack': ()}
    if defect.get('scope') not in required or any(not defect.get(k) for k in required[defect['scope']]):
        raise ProtocolError('Defect scope requires its canonical target')
    if defect.get('task_id'):
        if defect['task_id'] not in tasks:
            raise ProtocolError('Defect names an unknown task')
        actual = tasks[defect['task_id']]
        if instance_id is not None and instance_id != actual:
            raise ProtocolError('Defect task and instance disagree')
        instance_id = actual
    if defect.get('page') is not None:
        if not defect.get('artifact_id'):
            raise ProtocolError('Page defect requires an artifact ID')
        bindings = [b for b in manifest.get('bindings', [])
                    if b.get('artifact') == defect['artifact_id'] and b.get('page') == defect['page']]
        if not bindings:
            raise ProtocolError('Defect cites an unknown or unbound artifact page')
        candidates = {tasks[b['record']] for b in bindings if b['record'] in tasks}
        if instance_id is not None and instance_id not in candidates:
            raise ProtocolError('Defect page does not belong to the claimed instance')
        if defect.get('task_id') and not any(b['record'] == defect['task_id'] for b in bindings):
            raise ProtocolError('Defect page does not contain the claimed task')
        if instance_id is None and len(candidates) == 1:
            instance_id = next(iter(candidates))
    if instance_id is not None and instance_id not in instances:
        raise ProtocolError('Defect names an unknown instance')
    expected_owner = instances[instance_id] if instance_id is not None else 'pack-assembler'
    if defect['owner'] != expected_owner:
        raise ProtocolError('Defect repair owner does not match canonical ownership')
    return instance_id


def route_defects(defects: list[dict], content: dict, manifest: dict) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    seen = set()
    for defect in defects:
        if defect['defect_id'] in seen:
            raise ProtocolError('Duplicate defect ID')
        seen.add(defect['defect_id'])
        instance = defect_instance(defect, content, manifest)
        if instance is None:
            raise ProtocolError('Pack-level or ambiguous defect requires explicit orchestrator disposition')
        grouped[instance].append(copy.deepcopy(defect))
    return dict(grouped)


def _defect_covers(defect: dict, target: str, instance: str | None) -> bool:
    page = f"{defect.get('artifact_id')}:{defect.get('page')}"
    return target in ('pack', instance, defect.get('task_id'), page)


def validate_review_result(result: dict, request: dict, content: dict, manifest: dict) -> None:
    validate_json(result, 'schemas/review-result.schema.json')
    for key in ('generation_run_id', 'invocation_id', 'agent_id', 'context_sha256', 'review_run_id'):
        if result[key] != request[key]:
            raise ProtocolError('Review identity mismatch: ' + key)
    if result['reviewer'] != request['agent_id']:
        raise ProtocolError('Reviewer identity mismatch')
    for key, value in request['bindings'].items():
        if result[key] != value:
            raise ProtocolError('Stale review binding: ' + key)
    expected = {(c['check_id'], c['target']) for c in request['expected_checks']}
    found = [(c['check_id'], c['target']) for c in result['checks']]
    if len(found) != len(set(found)) or set(found) != expected:
        raise ProtocolError('Review has missing, duplicate or unexpected checks')
    tasks = {t['id']: t for t in content['tasks']}
    failed = set()
    for check in result['checks']:
        if check['status'] == 'FAIL':
            failed.add((check['check_id'], check['target']))
        if check['status'] == 'NA':
            if (request['agent_id'] == 'visual-reviewer' or request['task_type'] == 'REVIEW_COMPONENT'
                    or not check.get('applicability_reason')):
                raise ProtocolError('Required visual/component check cannot be waived')
            if check['check_id'].startswith('TASK.') and (
                    check['check_id'] != 'TASK.DISTRACTORS' or tasks.get(check['target'], {}).get('options')):
                raise ProtocolError('Required task check cannot be waived')
        if request['task_type'] == 'REVIEW_PACK' and request['agent_id'] != 'provenance-reviewer':
            if not all(isinstance(c, dict) for c in check['evidence']['citations']):
                raise ProtocolError('Pack review requires structured final-artifact citations')
    covered, blocking, ids = set(), [], set()
    for defect in result['defects']:
        if defect['defect_id'] in ids:
            raise ProtocolError('Duplicate defect ID')
        ids.add(defect['defect_id'])
        if (defect['generation_run_id'] != result['generation_run_id'] or
                defect['review_run_id'] != result['review_run_id']):
            raise ProtocolError('Defect belongs to another review/run')
        instance = defect_instance(defect, content, manifest)
        if request['instance'] is not None and instance != request['instance']['id']:
            raise ProtocolError('Component critic cannot report defects for another instance')
        if defect['severity'] == 'release_blocking':
            keys = {key for key in failed if key[0] == defect['check_id'] and _defect_covers(defect, key[1], instance)}
            if not keys:
                raise ProtocolError('Blocking defect lacks a matching failed check')
            covered.update(keys)
            blocking.append(defect)
    if covered != failed:
        raise ProtocolError('Every failed review check needs a correctly routed blocking defect')
    if (result['status'] == 'PASS') != (not failed and not blocking):
        raise ProtocolError('Review status contradicts its check/defect results')


def export_release_review(result: dict, execution, *, method: str, generation_actors: set[str],
                          evidence_dir: Path) -> tuple[Path, Path]:
    """Preserve actual host metadata/transcript; translate to pack_evidence v3."""
    execution.validate_receipt()
    if not generation_actors or execution.actor in generation_actors:
        raise ProtocolError('Independent review must use a different actor from every generator')
    evidence_dir.mkdir(parents=True, exist_ok=True)
    review_path = evidence_dir / f'{method}_review.json'
    trace_path = evidence_dir / f'{method}_trace.json'
    transcript_path = evidence_dir / f'{method}_transcript.txt'
    checks = []
    for check in result['checks']:
        entry = dict(id=check['check_id'], subject=check['target'], result=check['status'],
                     observation=check['evidence']['observation'], citations=copy.deepcopy(check['evidence']['citations']))
        if check.get('applicability_reason'):
            entry['applicability_reason'] = check['applicability_reason']
        checks.append(entry)
    review = dict(schema_version=3, execution_id=execution.execution_id,
                  generation_run_id=result['generation_run_id'],
                  manifest_sha256=result['manifest_sha256'], content_sha256=result['content_sha256'],
                  requirements_sha256=result['requirements_sha256'], checks=checks)
    write_json_atomic(review_path, review, immutable=True)
    with transcript_path.open('x', encoding='utf-8', newline='') as stream:
        stream.write(execution.transcript)
    trace = dict(source=execution.source, execution_id=execution.execution_id,
                 reviewer_actor=execution.actor, generator_actor=sorted(generation_actors)[0],
                 generator_actors=sorted(generation_actors), review_sha256=sha256_file(review_path),
                 manifest_sha256=result['manifest_sha256'], transcript_path=transcript_path.name,
                 transcript_sha256=sha256_file(transcript_path))
    write_json_atomic(trace_path, trace, immutable=True)
    return review_path, trace_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--schema', type=Path, required=True)
    args = parser.parse_args()
    try:
        validate_json(read_json(args.file), args.schema)
        print('Schema valid. Identity, coverage and ownership still require the matching request/run.')
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
