"""Executable agent registry with fail-closed schema and relationship validation."""
from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path

from agent_protocol import ProtocolError, read_json, reference_record, safe_path, sha256_json, validate_json

ROOT = Path(__file__).resolve().parents[1]


class RegistryError(ProtocolError):
    pass


@dataclass(frozen=True)
class AgentDefinition:
    id: str
    kind: str
    role: str
    _raw: dict
    default_max_attempts: int

    @property
    def raw(self) -> dict:
        return copy.deepcopy(self._raw)

    @property
    def parallelizable(self) -> bool:
        return self._raw['invocation']['parallelizable']

    @property
    def max_attempts(self) -> int:
        return self._raw['invocation'].get('max_attempts', self.default_max_attempts)


class AgentRegistry:
    def __init__(self, payload: dict, *, root: Path = ROOT):
        self.root = Path(root).resolve()
        self._payload = copy.deepcopy(payload)
        try:
            validate_json(payload, self.root / 'schemas/registry-v2.schema.json')
            ids = [agent['id'] for agent in payload['agents']]
            if len(ids) != len(set(ids)):
                raise RegistryError('Duplicate agent IDs')
            default = payload['execution_defaults']['default_max_attempts']
            self._agents = {a['id']: AgentDefinition(a['id'], a['kind'], a['role'], copy.deepcopy(a), default)
                            for a in payload['agents']}
            self._validate_relationships()
        except (ProtocolError, OSError) as exc:
            raise RegistryError(str(exc)) from exc

    @classmethod
    def load(cls, registry_path: Path | None = None) -> 'AgentRegistry':
        path = Path(registry_path or ROOT / 'skills/registry.v2.json')
        return cls(read_json(path), root=path.resolve().parents[1])

    @property
    def payload(self) -> dict:
        return copy.deepcopy(self._payload)

    @property
    def sha256(self) -> str:
        return sha256_json(self._payload)

    def get(self, agent_id: str) -> AgentDefinition:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise RegistryError(f'Unknown agent: {agent_id}') from exc

    def generators(self) -> list[AgentDefinition]:
        return [a for a in self._agents.values() if a.role == 'generator']

    def _file(self, relative: str) -> None:
        if not safe_path(self.root, relative).is_file():
            raise RegistryError('Missing registered dependency: ' + relative)

    def _validate_relationships(self) -> None:
        for key in ('entrypoint', 'runtime_entrypoint'):
            self._file(self._payload['orchestrator'][key])
        for key, path in self._payload['protocol'].items():
            if key.endswith('_schema'):
                self._file(path)
        expected_roles = {'context-resolver':'context_resolver','pack-assembler':'assembler',
                          'semantic-reviewer':'pack_reviewer','visual-reviewer':'pack_reviewer',
                          'provenance-reviewer':'pack_reviewer','release-arbiter':'release_arbiter'}
        for name, role in expected_roles.items():
            if self.get(name).role != role:
                raise RegistryError(f'{name} must have role {role}')
        for agent in self._agents.values():
            raw = agent.raw
            self._file(raw['entrypoint'])
            if agent.role == 'generator':
                if agent.kind != 'skill' or not raw.get('accepts_instances') or not raw.get('repair_owner'):
                    raise RegistryError(f'{agent.id} must own instance generation and repair')
                if raw.get('mutation_scope') != ['components/{instance_id}/**']:
                    raise RegistryError('Generator mutation scope must be instance-only')
                if not raw.get('invocation', {}).get('fresh_context'):
                    raise RegistryError('Generators require fresh invocation context')
                inputs = raw['input']
                if not set(inputs['required_context']) <= set(inputs['context_projection']):
                    raise RegistryError('Required context is not projected')
                for path in inputs.get('mandatory_references', []):
                    self._file(path)
                for rule in inputs.get('conditional_references', []):
                    self._file(rule['path'])
                critic_id = raw.get('post_generation_review')
                if agent.id == 'dlp-maths-lesson' and not critic_id:
                    raise RegistryError('Mathematics requires a critic')
                if critic_id:
                    critic = self.get(critic_id)
                    if (critic.role != 'component_critic' or critic.raw.get('reviews_owner') != agent.id or
                            critic.raw.get('routes_defects_to') != agent.id):
                        raise RegistryError('Critic ownership/routing mismatch')
            if agent.role in ('component_critic', 'pack_reviewer'):
                if raw.get('may_mutate') is not False or raw['invocation']['implicit']:
                    raise RegistryError('Reviewers must be read-only and explicitly invoked')
                if agent.kind == 'reviewer' and not raw['invocation'].get('fresh_context'):
                    raise RegistryError('Model reviewers require fresh context')
            if raw.get('routes_defects_to') and self.get(raw['routes_defects_to']).role != 'generator':
                raise RegistryError('Defect destination must be a generator')
            if 'output' in raw:
                self._file(raw['output']['schema'])
            for path in raw.get('output_schemas', {}).values():
                self._file(path)
            if 'input' in raw:
                self._file(raw['input']['schema'])
            if raw.get('requirements_source'):
                self._file(raw['requirements_source'])

    def references_for(self, agent_id: str, context: dict) -> list[dict]:
        raw = self.get(agent_id).raw
        paths = [raw['entrypoint'], 'references/year-level-context-contract.md',
                 'references/shared-class-context-contract.md',
                 context['active_year_profile']['source']]
        inputs = (self.get(raw['reviews_owner']).raw['input'] if raw.get('reviews_owner')
                  else raw.get('input', {}))
        paths.extend(inputs.get('mandatory_references', []))
        for rule in inputs.get('conditional_references', []):
            condition = rule['when']
            entry = context.get(condition['field'], '')
            value = str(entry.get('value', '') if isinstance(entry, dict) else entry).lower()
            if (all(t.lower() in value for t in condition['contains_all']) and
                    any(t.lower() in value for t in condition['contains_any'])):
                paths.append(rule['path'])
        if raw.get('requirements_source'):
            paths.extend(('references/qa-workflow-v3.md', raw['requirements_source']))
        return [reference_record(self.root, path) for path in dict.fromkeys(paths)]
