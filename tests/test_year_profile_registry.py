"""Synthetic profile metadata checks, not evidence of classroom calibration."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


class YearProfileRegistryTests(unittest.TestCase):
    def setUp(self):
        from year_profile_registry import YearProfileRegistry
        self.registry = YearProfileRegistry.load()

    def test_registry_discovers_existing_profiles_without_promoting_year_six(self):
        self.assertEqual(self.registry.ids(), ('year-4-5', 'year-6'))
        self.assertEqual(self.registry.get('year-6')['status'], 'scaffold')
        self.assertEqual(self.registry.get('year-6')['release_mode'], 'candidate')
        self.assertEqual(self.registry.get('year-4-5')['status'], 'calibrated')

    def test_profile_sources_accept_windows_line_endings_for_digest_stability(self):
        from year_profile_registry import YearProfileRegistry
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ('references/year-level-profiles/registry.json',
                             'schemas/year-level-profile.schema.json'):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            for profile in self.registry.payload['profiles']:
                target = root / profile['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                source = (ROOT / profile['path']).read_bytes().replace(b'\r\n', b'\n')
                target.write_bytes(source.replace(b'\n', b'\r\n'))
            self.assertEqual(YearProfileRegistry.load(root).ids(), ('year-4-5', 'year-6'))

    def test_profile_results_are_isolated_copies(self):
        first = self.registry.get('year-4-5')
        first['domains']['mathematics']['status'] = 'scaffold'
        self.assertNotEqual(first, self.registry.get('year-4-5'))

    def test_invalid_or_duplicate_registry_entries_fail(self):
        from year_profile_registry import YearProfileRegistry
        from agent_protocol import ProtocolError
        for mutation in (
            lambda p: p['profiles'].append(copy.deepcopy(p['profiles'][0])),
            lambda p: p['profiles'][0].update(path='../outside.md'),
            lambda p: p['profiles'][0].update(status='invented'),
            lambda p: p['profiles'][0].update(learner_ceiling=5),
            lambda p: p['profiles'][1].update(release_mode='normal'),
            lambda p: p['profiles'][0]['domains']['mathematics'].update(source='references/missing.md'),
            lambda p: p['profiles'][0].update(sha256='0' * 64),
            lambda p: p['profiles'][0].update(status='scaffold', release_mode='candidate'),
            lambda p: p['profiles'][0]['curriculum_anchor'].update(years=[12]),
        ):
            payload = self.registry.payload
            mutation(payload)
            with self.subTest(payload=payload), self.assertRaises(ProtocolError):
                YearProfileRegistry(payload, root=ROOT)

    def test_subject_specific_maturity_is_separate_from_curriculum_and_enrolment(self):
        from year_profile_registry import YearProfileRegistry
        payload = self.registry.payload
        payload['profiles'][0]['domains']['mathematics']['status'] = 'scaffold'
        registry = YearProfileRegistry(payload, root=ROOT)
        self.assertEqual(registry.get('year-4-5')['domains']['literacy']['status'], 'declared-baseline')
        self.assertEqual(registry.release_mode('year-4-5'), 'candidate')
        self.assertNotIn('enrolment', registry.get('year-4-5'))

    def test_unknown_profile_and_false_maturity_fail(self):
        from agent_protocol import ProtocolError
        for active in (
            dict(value='year-7', resolved=True, source='references/year-level-profiles/year-7.md'),
            dict(value='year-6', resolved=True, source='references/year-level-profiles/year-6.md', status='calibrated'),
            dict(value='year-6', resolved=True, source='wrong.md', status='scaffold'),
        ):
            with self.subTest(active=active), self.assertRaises(ProtocolError):
                self.registry.validate_active(active)

    def test_freeze_uses_registry_and_binds_its_source(self):
        from agent_fixtures import context_fixture
        from agent_registry import AgentRegistry
        from agent_protocol import component_request, sha256_file
        from build_execution_plan import freeze_context
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(directory)
            agents = AgentRegistry.load()
            frozen = freeze_context(context, agents, Path(directory))
            self.assertEqual(frozen['active_year_profile']['status'], 'calibrated')
            self.assertTrue(any(s['path'] == 'references/year-level-profiles/registry.json'
                                and s['sha256'] == sha256_file(ROOT / s['path'])
                                for s in frozen['source_provenance']))
            request = component_request(frozen, frozen['timetable_instances'][0], agents, 'profile-test')
            self.assertIn('references/year-level-profiles/registry.json', [r['path'] for r in request['references']])
            self.assertEqual(context['source_provenance'], frozen['source_provenance'][:2])
            self.assertEqual(freeze_context(frozen, agents, Path(directory)), frozen)

    def test_freeze_rejects_stale_registry_binding(self):
        from agent_fixtures import context_fixture
        from agent_registry import AgentRegistry
        from agent_protocol import ProtocolError
        from build_execution_plan import freeze_context
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(directory)
            context['source_provenance'].append(dict(id='profile-registry', kind='repository_reference',
                path='references/year-level-profiles/registry.json', sha256='0' * 64))
            with self.assertRaises(ProtocolError):
                freeze_context(context, AgentRegistry.load(), Path(directory))

    def test_freeze_rejects_registry_source_from_private_root(self):
        from agent_fixtures import context_fixture
        from agent_registry import AgentRegistry
        from agent_protocol import ProtocolError, sha256_file
        from build_execution_plan import freeze_context
        with tempfile.TemporaryDirectory() as directory:
            _, context = context_fixture(directory)
            relative = 'references/year-level-profiles/registry.json'
            unrelated = Path(directory) / relative
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text('{"unrelated":"source"}')
            context['source_provenance'].append(dict(id='profile-registry', kind='runtime_school_source',
                path=relative, sha256=sha256_file(unrelated)))
            with self.assertRaises(ProtocolError):
                freeze_context(context, AgentRegistry.load(), Path(directory))

    def test_final_release_consumer_rejects_candidate_mode(self):
        # Isolate the release consumer with already-passing synthetic upstream
        # evidence; no mocked report is presented as an actual deck review.
        from unittest.mock import patch
        import audit_release_bundle as release
        from agent_protocol import sha256_file
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            deck = root / 'deck.pptx'
            deck.write_bytes(b'synthetic')
            manifest = dict(artifacts=[dict(role='deck', id='deck', path=deck.name)], bindings=[])
            paths = {}
            for name in ('contract', 'year-profile', 'typography', 'containment', 'visual',
                         'semantic-review', 'manifest', 'content', 'context-record', 'component-record',
                         'warning-ledger', 'visual-review', 'semantic-trace', 'visual-trace'):
                paths[name] = root / (name + '.json')
                paths[name].write_text(json.dumps(dict(status='PASS', artifact_sha256=sha256_file(deck),
                    execution_id='review-test', generation_run_id='generation-test', reviewer_actor='test')))
            args = ['audit_release_bundle', '--deck', str(deck), '--out', str(root / 'out.json')]
            for name, path in paths.items():
                args.extend(['--' + name, str(path)])
            for mode, expected in [('normal', 0), ('candidate', 1), (None, 1)]:
                report = dict(status='PASS', artifact_sha256=sha256_file(deck))
                if mode is not None:
                    report['release_mode'] = mode
                paths['year-profile'].write_text(json.dumps(report))
                with patch.object(sys, 'argv', args), \
                     patch.object(release, 'audit_pack', return_value=([], {'tasks': []}, manifest)), \
                     patch.object(release, 'audit_review', return_value=[]), \
                     patch.object(release.subprocess, 'run') as run, \
                     patch('builtins.print'):
                    run.return_value.returncode = 0
                    self.assertEqual(release.main(), expected)
                if expected:
                    self.assertTrue(any('profile' in f and 'release' in f
                        for f in json.loads((root / 'out.json').read_text())['failures']))

    def test_audit_rejects_year_six_maturity_spoof_and_accepts_scaffold(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            deck = root / 'deck.pptx'
            deck.write_bytes(b'synthetic hash fixture; not a presentation')
            components = root / 'components.json'
            components.write_text(json.dumps(dict(artifact_sha256=hashlib.sha256(deck.read_bytes()).hexdigest(),
                                                  scheduled_instances=[], components=[])))
            context = root / 'context.json'
            for status, expected in [('calibrated', 1), ('scaffold', 0)]:
                context.write_text(json.dumps(dict(active_year_profile=dict(value='year-6', resolved=True,
                    source='references/year-level-profiles/year-6.md', status=status))))
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/audit_year_profile_context.py'),
                    '--deck', str(deck), '--context-record', str(context), '--component-record', str(components)],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
                self.assertEqual(json.loads(result.stdout)['release_mode'], 'candidate')

    def test_complete_package_includes_validated_registry_dependencies(self):
        from build_chatgpt_package import build_file_map
        from year_profile_registry import PROFILE_REGISTRY_FILES
        _, files = build_file_map(ROOT)
        for path in PROFILE_REGISTRY_FILES:
            self.assertIn(path, files)
            self.assertIn('skills/dlp-pack-qa/' + path, files)


if __name__ == '__main__':
    unittest.main()
