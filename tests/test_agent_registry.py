import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

class RegistryTests(unittest.TestCase):
    def test_control_plane_modules_exist(self):
        for name in ('agent_registry', 'agent_protocol', 'build_execution_plan'):
            self.assertIsNotNone(importlib.util.find_spec(name), name)

    def test_registry_load_and_legacy_compatibility(self):
        from agent_registry import AgentRegistry
        registry = AgentRegistry.load()
        legacy = json.loads((ROOT/'skills/registry.json').read_text())
        expected = {x['name'] for x in legacy['components']} - {'dlp-pack-qa'}
        self.assertEqual({a.id for a in registry.generators()}, expected)

    def test_registry_rejects_duplicate_ids_and_unknown_critic(self):
        from agent_registry import AgentRegistry, RegistryError
        payload = json.loads((ROOT/'skills/registry.v2.json').read_text())
        duplicate = copy.deepcopy(payload)
        duplicate['agents'].append(duplicate['agents'][0])
        with self.assertRaises(RegistryError):
            AgentRegistry(duplicate, root=ROOT)
        bad = copy.deepcopy(payload)
        next(a for a in bad['agents'] if a['id']=='dlp-maths-lesson')['post_generation_review'] = 'missing'
        with self.assertRaises(RegistryError):
            AgentRegistry(bad, root=ROOT)

    def test_registry_rejects_unknown_keys_and_path_escape(self):
        from agent_registry import AgentRegistry, RegistryError
        payload = json.loads((ROOT/'skills/registry.v2.json').read_text())
        payload['agents'][0]['parallelizble'] = True
        with self.assertRaises(RegistryError):
            AgentRegistry(payload, root=ROOT)
        del payload['agents'][0]['parallelizble']
        payload['agents'][0]['entrypoint'] = '../outside.py'
        with self.assertRaises(RegistryError):
            AgentRegistry(payload, root=ROOT)

    def test_all_schemas_are_valid_offline(self):
        from agent_protocol import schema_validator
        for path in (ROOT/'schemas').glob('*.schema.json'):
            validator = schema_validator(path)
            validator.check_schema(validator.schema)
        self.assertEqual(len(list((ROOT/'schemas').glob('*.schema.json'))), 11)

    def test_qa_is_explicit_only(self):
        text = (ROOT/'skills/dlp-pack-qa/agents/openai.yaml').read_text()
        self.assertIn('allow_implicit_invocation: false', text)
