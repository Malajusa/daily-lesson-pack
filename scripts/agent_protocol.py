"""Validated, provider-neutral handoffs. This module never grants release authority."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]


class ProtocolError(ValueError):
    """An untrusted handoff does not satisfy the frozen run contract."""


def json_bytes(payload: Any) -> bytes:
    try:
        return (json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    except (ValueError, TypeError) as exc:
        raise ProtocolError(f'Not finite JSON: {exc}') from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json_bytes(payload)).hexdigest()


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def _invalid_constant(value):
    raise ProtocolError(f'Non-finite JSON constant: {value}')


def parse_json(text: str) -> dict:
    try:
        data = json.loads(text, object_pairs_hook=_unique_pairs, parse_constant=_invalid_constant)
    except (ValueError, TypeError) as exc:
        raise ProtocolError(f'Invalid JSON: {exc}') from exc
    if not isinstance(data, dict):
        raise ProtocolError('Expected a JSON object')
    return data


def read_json(path: Path) -> dict:
    return parse_json(Path(path).read_text(encoding='utf-8'))


def safe_path(root: Path, relative: str) -> Path:
    """Confine POSIX-format handoff paths, including on Windows and through symlinks."""
    if (not isinstance(relative, str) or not relative or '\\' in relative or
            '\x00' in relative or ':' in relative or relative.startswith('/') or
            any(part in ('', '.', '..') for part in relative.split('/'))):
        raise ProtocolError(f'Unsafe relative path: {relative!r}')
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ProtocolError(f'Path escapes root: {relative}')
    return target


def schema_validator(schema_path: Path) -> Draft202012Validator:
    path = Path(schema_path).resolve()
    stamps = tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size)
                   for p in sorted(path.parent.glob('*.schema.json')))
    return _cached_validator(str(path), stamps)


@lru_cache(maxsize=32)
def _cached_validator(schema_path: str, stamps: tuple) -> Draft202012Validator:
    """Resolve only bundled schemas; no implicit remote schema retrieval."""
    schema_path = Path(schema_path)
    resources = []
    for path in sorted(schema_path.parent.glob('*.schema.json')):
        schema = read_json(path)
        Draft202012Validator.check_schema(schema)
        resource = Resource.from_contents(schema)
        resources.extend(((schema['$id'], resource), (path.resolve().as_uri(), resource)))
    return Draft202012Validator(read_json(schema_path),
                                registry=Registry().with_resources(resources),
                                format_checker=FormatChecker())


def validate_json(payload: dict, schema_path: Path | str) -> None:
    json_bytes(payload)  # Reject NaN/infinity even in intentionally open content fields.
    path = Path(schema_path)
    if not path.is_absolute():
        path = ROOT / path
    try:
        errors = sorted(schema_validator(path).iter_errors(payload),
                        key=lambda error: '/'.join(map(str, error.absolute_path)))
    except (OSError, ValueError, KeyError) as exc:
        raise ProtocolError(f'Cannot validate against {path.name}: {exc}') from exc
    if errors:
        raise ProtocolError('\n'.join(
            f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors))


def write_json_atomic(path: Path, payload: dict, *, immutable: bool = False) -> None:
    path = Path(path)
    data = json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name, suffix='.tmp')
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if immutable:
            try:
                os.link(temporary, path)  # Atomic create-only publication; no overwrite race.
            except FileExistsError as exc:
                raise ProtocolError(f'Immutable record already exists: {path}') from exc
        else:
            os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def required_component_checks(context: dict, owner: str) -> list[str]:
    # Keep the release audit's existing IDs authoritative.
    from audit_pack_contract import REQUIRED_CHECKS, GENERIC_REQUIRED_CHECKS
    checks = set(REQUIRED_CHECKS.get(owner, GENERIC_REQUIRED_CHECKS))
    if owner == 'dlp-maths-lesson':
        if sum(i['owner'] == owner for i in context['timetable_instances']) > 1:
            checks.add('MATHS.BLOCK.BREAKPOINT')
        focus = str(context['mathematics_focus']['value']).lower()
        if 'fraction' in focus and any(t in focus for t in ('decimal', 'equivalent', 'tenths', 'hundredths')):
            checks.add('MATHS.FRACTION.REPARTITIONING')
    return sorted(checks)


def project_context(context: dict, fields: list[str], required: list[str]) -> dict:
    missing = set(required) - set(context)
    if missing:
        raise ProtocolError('Missing projected context: ' + ', '.join(sorted(missing)))
    return {field: copy.deepcopy(context[field]) for field in fields if field in context}


def reference_record(root: Path, relative: str, *, include_text: bool = True) -> dict:
    path = safe_path(root, relative)
    record = {'path': relative, 'sha256': sha256_file(path)}
    if include_text:
        try:
            record['text'] = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            pass  # The host must mount binary references; never invent extracted text.
    return record


def component_request(context: dict, instance: dict, registry, invocation_id: str,
                      *, defects: list[dict] | None = None) -> dict:
    agent = registry.get(instance['owner'])
    definition = agent.raw
    fields = definition['input']
    request = {
        'protocol_version': 1, 'generation_run_id': context['generation_run_id'],
        'invocation_id': invocation_id, 'agent_id': agent.id,
        'task_type': 'REPAIR_COMPONENT' if defects else 'GENERATE_COMPONENT',
        'context_sha256': sha256_json(context),
        'context': project_context(context, fields['context_projection'], fields['required_context']),
        'instance': copy.deepcopy(instance),
        'references': registry.references_for(agent.id, context),
        'defects': copy.deepcopy(defects or []),
        'expected_checks': [{'check_id': key, 'target': instance['id']}
                            for key in required_component_checks(context, agent.id)],
        'input_artifacts': [], 'review_run_id': None,
        'bindings': dict.fromkeys(('artifact_sha256', 'manifest_sha256', 'content_sha256', 'requirements_sha256')),
        'permissions': {'may_mutate_context': False, 'may_modify_other_instances': False, 'may_release': False},
        'output_contract': {'schema': 'schemas/component-result.schema.json',
                            'path': f"components/{instance['id']}/{invocation_id}.json"},
    }
    validate_json(request, registry.root / 'schemas/agent-request.schema.json')
    return request


def validate_component_result(result: dict, request: dict, context: dict) -> None:
    validate_json(result, 'schemas/component-result.schema.json')
    for key in ('generation_run_id', 'invocation_id', 'agent_id', 'context_sha256'):
        if result[key] != request[key]:
            raise ProtocolError(f'Component identity mismatch: {key}')
    component, instance = result['component'], request['instance']
    if component['instance_id'] != instance['id'] or component['owner'] != instance['owner']:
        raise ProtocolError('Component instance/owner mismatch')
    if component['active_year_profile'] != context['active_year_profile']['value']:
        raise ProtocolError('Component changed the active year profile')
    estimate = component['estimated_minutes']
    if isinstance(estimate, bool) or not math.isfinite(estimate) or estimate > instance['duration_minutes']:
        raise ProtocolError('Component exceeds its time budget or has an invalid estimate')
    # The artefact names only this owner's instance; actual bytes are coordinator-owned.
    relative = component['artefact']
    safe_path(ROOT, relative)
    if relative != request['output_contract']['path']:
        raise ProtocolError('Component artefact escapes its instance')
    checks = component['checks']
    ids = [check['id'] for check in checks]
    if len(ids) != len(set(ids)) or not set(required_component_checks(context, component['owner'])) <= set(ids):
        raise ProtocolError('Duplicate or missing required component checks')
    all_pass = all(check['status'] == 'PASS' for check in checks)
    if (result['status'] != component['status'] or
            (result['status'] == 'PASS') != all_pass):
        raise ProtocolError('Component PASS conflicts with check results')
    for task in component['content']['tasks']:
        if task['instance_id'] != instance['id']:
            raise ProtocolError('Canonical task belongs to another instance')
    from pack_evidence import validate_content
    errors = validate_content({'schema_version': 3, 'instances': [instance],
                               'tasks': component['content']['tasks']})
    if errors:
        raise ProtocolError('\n'.join(errors))


def aggregate_components(context: dict, results: list[dict], *, require_complete: bool = True) -> tuple[dict, dict]:
    """Translate structured evidence into existing v2/v3 records, without rewriting."""
    records, tasks, documents = [], [], {}
    scheduled = {i['id']: i for i in context['timetable_instances']}
    by_id = {}
    for result in results:
        component = result['component']
        key = component['instance_id']
        if key in by_id or key not in scheduled:
            raise ProtocolError('Duplicate or unscheduled component result: ' + key)
        if result['status'] != 'PASS':
            raise ProtocolError('Assembly requires every component to PASS')
        if result['generation_run_id'] != context['generation_run_id']:
            raise ProtocolError('Stale component generation run')
        by_id[key] = component
    if require_complete and set(by_id) != set(scheduled):
        raise ProtocolError('Assembly requires exactly one result for every scheduled instance')
    for key in scheduled:
        if key not in by_id:
            continue
        component = copy.deepcopy(by_id[key])
        content = component.pop('content')
        for check in component['checks']:
            check['result'] = check.pop('status')
        records.append(component)
        tasks.extend(content['tasks'])
        for name, document in content.get('documents', {}).items():
            if name in documents:
                raise ProtocolError('Duplicate document ID: ' + name)
            documents[name] = document
    ids = [t['id'] for t in tasks]
    if len(ids) != len(set(ids)) or set(ids) & set(documents):
        raise ProtocolError('Canonical task/document IDs must be globally unique')
    record = {'schema_version': 2, 'generation_run_id': context['generation_run_id'],
              'scheduled_instances': copy.deepcopy(context['timetable_instances']), 'components': records}
    content = {'schema_version': 3, 'instances': copy.deepcopy(context['timetable_instances']),
               'tasks': tasks, 'documents': documents}
    if require_complete:
        from dlp_build_runtime import validate_component_record
        from pack_evidence import validate_content
        errors = validate_component_record(context, record) + validate_content(content)
        if errors:
            raise ProtocolError('\n'.join(errors))
    return record, content


def prompt_envelope(request: dict) -> str:
    return ('Execute only the specified Daily Lesson Pack instance or review.\n'
            'The frozen context and attached contracts are authoritative. Do not reinterpret the timetable, '
            'change year profile, modify another instance or claim pack release. Reviewers report defects; '
            'they never silently repair content. Return only the requested JSON result schema.\n\n'
            + json_bytes(request).decode('utf-8'))
