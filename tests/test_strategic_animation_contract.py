"""Protect animation-review coverage and portable dependency closure."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_chatgpt_package import build_file_map
from pack_evidence import expected_checks

REFERENCE = 'references/strategic-animation-standard.md'
BENCHMARK = 'examples/benchmarks/strategic-animation-regression.md'


class StrategicAnimationContractTests(unittest.TestCase):
    def test_review_coverage_includes_stages_and_exported_pages(self):
        content = {'instances': [], 'tasks': []}
        manifest = {'artifacts': [
            {'id': 'deck', 'pages': 2}, {'id': 'student', 'pages': 1}]}
        semantic = expected_checks(content, manifest, 'semantic')
        visual = expected_checks(content, manifest, 'visual')
        self.assertIn(('QA.ANIM.PLAN', 'pack'), semantic)
        self.assertIn(('QA.ANIM.EVIDENCE', 'pack'), semantic)
        self.assertIn(('QA.ANIM.EXPORT', 'student:1'), visual)
        for page in ('deck:1', 'deck:2', 'student:1'):
            self.assertIn(('QA.ANIM.STATES', page), visual)
        old_review = semantic - {('QA.ANIM.EVIDENCE', 'pack')}
        self.assertTrue(semantic - old_review,
                        'A review without playback-evidence coverage cannot be complete')

    def test_complete_package_supplies_animation_dependencies(self):
        _, files = build_file_map(ROOT)
        for path in (REFERENCE, BENCHMARK,
                     'skills/dlp-maths-lesson/' + REFERENCE,
                     'skills/dlp-writing-lesson/' + REFERENCE,
                     'skills/dlp-pack-qa/' + REFERENCE,
                     'skills/dlp-pack-qa/' + BENCHMARK):
            source = REFERENCE if path.endswith(REFERENCE) else BENCHMARK
            self.assertEqual(files[path], (ROOT / source).read_bytes())

    def test_standalone_components_keep_local_references(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run([sys.executable, str(ROOT / 'scripts/package_component_skills.py'),
                            '--out', temp], check=True, capture_output=True)
            for name in ('dlp-maths-lesson', 'dlp-writing-lesson', 'dlp-pack-qa'):
                with zipfile.ZipFile(Path(temp) / (name + '.zip')) as archive:
                    self.assertEqual(archive.read(name + '/' + REFERENCE),
                                     (ROOT / REFERENCE).read_bytes())
                    package = json.loads(archive.read(name + '/PACKAGE.json'))
                    self.assertIn(REFERENCE, package['shared_references'])
            with zipfile.ZipFile(Path(temp) / 'dlp-numeracy-warmup.zip') as archive:
                skill = archive.read('dlp-numeracy-warmup/SKILL.md').decode()
                self.assertNotIn(REFERENCE, skill,
                                 'Standalone warm-up must not acquire an unavailable dependency')
