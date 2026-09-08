#!/usr/bin/env python3
"""Freeze already-resolved teacher context and build a deterministic execution DAG.

This is not an LLM curriculum resolver. Missing or contradictory source facts
must be resolved by the host before this boundary, never guessed here.
"""
from __future__ import annotations

import argparse
import copy
from datetime import date
from pathlib import Path

from agent_protocol import (ProtocolError, read_json, safe_path, sha256_file,
                            sha256_json, validate_json, write_json_atomic)
from agent_registry import AgentRegistry


def source_path(source: dict, registry: AgentRegistry, source_root: Path) -> Path:
    root = registry.root if source['kind'] in ('year_profile', 'repository_reference') else source_root
    return safe_path(root, source['path'])


def freeze_context(context: dict, registry: AgentRegistry, source_root: Path) -> dict:
    frozen = copy.deepcopy(context)
    frozen['frozen'] = True
    validate_json(frozen, registry.root / 'schemas/run-context.schema.json')
    from dlp_build_runtime import validate_resolved_context, REQUIRED_CONTEXT_FIELDS
    errors = validate_resolved_context(frozen)
    profile = frozen['active_year_profile']['value']
    expected_profile = f'references/year-level-profiles/{profile}.md'
    if frozen['active_year_profile']['source'] != expected_profile:
        errors.append('Active profile must reference its dedicated repository profile')
    safe_path(registry.root, expected_profile)
    try:
        resolved_date = date.fromisoformat(frozen['date']['value'])
        if resolved_date.strftime('%A') != frozen['day']['value']:
            errors.append('Resolved weekday does not match date')
    except (TypeError, ValueError):
        errors.append('Resolved date must be a real ISO date')
    sources = frozen['source_provenance']
    ids = [s['id'] for s in sources]
    paths = [s['path'] for s in sources]
    if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
        errors.append('Duplicate source provenance IDs or paths')
    for name in REQUIRED_CONTEXT_FIELDS:
        if frozen[name]['source'] not in set(ids) | set(paths):
            errors.append(f'{name} does not cite a hashed source')
    for source in sources:
        path = source_path(source, registry, Path(source_root))
        if not path.is_file() or sha256_file(path) != source['sha256']:
            errors.append('Missing or changed source: ' + source['path'])
    for instance in frozen['timetable_instances']:
        if registry.get(instance['owner']).role != 'generator':
            errors.append('Timetable owner is not a generator: ' + instance['owner'])
    if errors:
        raise ProtocolError('\n'.join(errors))
    return frozen


def build_execution_plan(context: dict, registry: AgentRegistry) -> dict:
    validate_json(context, registry.root / 'schemas/run-context.schema.json')
    nodes, completion = [], []
    seen = set()
    for instance in context['timetable_instances']:
        if instance['id'] in seen:
            raise ProtocolError('Duplicate timetable instance: ' + instance['id'])
        seen.add(instance['id'])
        owner = registry.get(instance['owner'])
        if owner.role != 'generator':
            raise ProtocolError('Timetable owner is not a generator')
        node_id = 'generate:' + instance['id']
        nodes.append(dict(id=node_id, type='generate', agent=owner.id, instance_id=instance['id'],
                          depends_on=[], state='PENDING'))
        critic = owner.raw.get('post_generation_review')
        if critic:
            critic_id = 'critic:' + instance['id']
            nodes.append(dict(id=critic_id, type='review', agent=critic, instance_id=instance['id'],
                              depends_on=[node_id], state='BLOCKED'))
            completion.append(critic_id)
        else:
            completion.append(node_id)
    nodes.append(dict(id='assemble', type='assemble', agent='pack-assembler',
                      depends_on=completion, state='BLOCKED'))
    reviews = []
    for reviewer in ('semantic-reviewer', 'visual-reviewer', 'provenance-reviewer'):
        node_id = 'qa:' + reviewer
        nodes.append(dict(id=node_id, type='review', agent=reviewer, depends_on=['assemble'], state='BLOCKED'))
        reviews.append(node_id)
    nodes.append(dict(id='release', type='release', agent='release-arbiter', depends_on=reviews, state='BLOCKED'))
    plan = dict(schema_version=1, generation_run_id=context['generation_run_id'],
                context_sha256=sha256_json(context), registry_sha256=registry.sha256, nodes=nodes)
    validate_json(plan, registry.root / 'schemas/execution-plan.schema.json')
    return plan


def validate_execution_plan(context: dict, plan: dict, registry: AgentRegistry) -> None:
    validate_json(plan, registry.root / 'schemas/execution-plan.schema.json')
    if plan != build_execution_plan(context, registry):
        raise ProtocolError('Execution plan differs from the frozen context/registry DAG')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--context', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        registry = AgentRegistry.load()
        context = freeze_context(read_json(args.context), registry, args.sources)
        args.out.mkdir(parents=True, exist_ok=False)
        write_json_atomic(args.out/'context.json', context, immutable=True)
        write_json_atomic(args.out/'execution-plan.json', build_execution_plan(context, registry), immutable=True)
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Plan rejected: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
