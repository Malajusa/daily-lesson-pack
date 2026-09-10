"""Repository-owned profile metadata; no learner placement or private settings.

Declared calibration is inherited source status, not a new validation claim.
Curriculum/retrieval preferences and scoped overrides belong to D01/D03.
"""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path

from agent_protocol import ProtocolError, read_json, safe_path, validate_json

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = 'references/year-level-profiles/registry.json'
SCHEMA_PATH = 'schemas/year-level-profile.schema.json'
PROFILE_REGISTRY_FILES = (REGISTRY_PATH, SCHEMA_PATH,
                          'scripts/year_profile_registry.py', 'scripts/agent_protocol.py')


def profile_source_sha256(path: Path) -> str:
    """Hash portable profile text, independent of a Windows CRLF checkout."""
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


class YearProfileRegistry:
    def __init__(self, payload: dict, *, root: Path = ROOT):
        self.root = Path(root).resolve()
        validate_json(payload, self.root / SCHEMA_PATH)
        self._payload = copy.deepcopy(payload)
        self._profiles = {}
        for profile in payload['profiles']:
            ident = profile['profile_id']
            if ident in self._profiles:
                raise ProtocolError('Duplicate year profile: ' + ident)
            if profile['path'] != f'references/year-level-profiles/{ident}.md':
                raise ProtocolError('Profile ID/path mismatch: ' + ident)
            if profile['curriculum_anchor']['years'] != [int(year) for year in ident.split('-')[1:]]:
                raise ProtocolError('Curriculum coverage disagrees with profile identity: ' + ident)
            path = safe_path(self.root, profile['path'])
            if not path.is_file() or profile_source_sha256(path) != profile['sha256']:
                raise ProtocolError('Missing or changed profile source: ' + ident)
            status_lines = [line for line in path.read_text(encoding='utf-8').splitlines()
                            if line.startswith('Status: ')]
            if len(status_lines) != 1 or profile['status'] not in status_lines[0].lower().split():
                raise ProtocolError('Profile status disagrees with source: ' + ident)
            if profile['status'] != 'calibrated' and profile['release_mode'] != 'candidate':
                raise ProtocolError('Uncalibrated profile cannot claim normal release: ' + ident)
            references = [profile['curriculum_anchor']['source'], profile['retrieval_guidance'],
                          profile['language_representation_guidance']]
            references.extend(d['source'] for d in profile['domains'].values())
            # Initial metadata deliberately cites each profile's own authored guidance.
            # Separate subject source files require an explicit future schema migration.
            if any(reference != profile['path'] for reference in references):
                raise ProtocolError('Calibration source must belong to the profile: ' + ident)
            if profile['jurisdiction_mapping'] is not None:
                raise ProtocolError('Jurisdiction mapping is unverified in registry version 1')
            self._profiles[ident] = copy.deepcopy(profile)

    @classmethod
    def load(cls, root: Path = ROOT) -> 'YearProfileRegistry':
        root = Path(root).resolve()
        try:
            return cls(read_json(root / REGISTRY_PATH), root=root)
        except (OSError, UnicodeError) as exc:
            raise ProtocolError('Cannot load profile registry: ' + str(exc)) from exc

    @property
    def payload(self) -> dict:
        return copy.deepcopy(self._payload)

    def ids(self) -> tuple[str, ...]:
        return tuple(self._profiles)

    def get(self, ident: str) -> dict:
        if not isinstance(ident, str) or ident not in self._profiles:
            raise ProtocolError('Unsupported active_year_profile: ' + str(ident))
        return copy.deepcopy(self._profiles[ident])

    def release_mode(self, ident: str) -> str:
        profile = self.get(ident)
        if any(d['status'] != 'declared-baseline' for d in profile['domains'].values()):
            return 'candidate'
        return profile['release_mode']

    def validate_active(self, active: dict) -> dict:
        if not isinstance(active, dict) or active.get('resolved') is not True:
            raise ProtocolError('active_year_profile is unresolved')
        profile = self.get(active.get('value'))
        if active.get('source') != profile['path']:
            raise ProtocolError('Active profile must reference its dedicated repository profile')
        authoritative = dict(status=profile['status'], profile_revision=profile['revision'],
                             release_mode=self.release_mode(profile['profile_id']))
        for key, value in authoritative.items():
            if key in active and active[key] != value:
                raise ProtocolError('Active profile ' + key + ' disagrees with registry')
        return {**copy.deepcopy(active), **authoritative}


def profile_reference_paths(root: Path = ROOT) -> tuple[str, ...]:
    registry = YearProfileRegistry.load(root)
    return tuple(registry.get(ident)['path'] for ident in registry.ids())
