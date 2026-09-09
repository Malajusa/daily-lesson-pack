"""Exercise the current audit, never the archived vulnerable implementation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProfileReleaseBoundaryTests(unittest.TestCase):
    def audit(self, profile, status, source=None):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            deck = folder / 'hash-only.bin'
            deck.write_bytes(b'Profile-audit unit fixture, not a classroom deck.')
            active = {'value': profile, 'resolved': True, 'source': source or f'references/year-level-profiles/{profile}.md'}
            if status is not None:
                active['status'] = status
            (folder/'context.json').write_text(json.dumps({'active_year_profile': active}))
            (folder/'components.json').write_text(json.dumps({
                'artifact_sha256': hashlib.sha256(deck.read_bytes()).hexdigest(),
                'scheduled_instances': [], 'components': []}))
            result = subprocess.run([sys.executable, str(ROOT/'scripts/audit_year_profile_context.py'),
                '--deck', str(deck), '--context-record', str(folder/'context.json'),
                '--component-record', str(folder/'components.json')], capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_unknown_maturity_is_rejected(self):
        code, report = self.audit('year-6', 'banana')
        self.assertNotEqual(code, 0, report)
        self.assertEqual(report['status'], 'FAIL')

    def test_false_calibration_is_rejected(self):
        code, report = self.audit('year-6', 'calibrated')
        self.assertNotEqual(code, 0, report)

    def test_wrong_source_is_rejected(self):
        code, report = self.audit('year-4-5', 'calibrated', 'teacher-preferences.json')
        self.assertNotEqual(code, 0, report)

    def test_scaffold_remains_candidate(self):
        code, report = self.audit('year-6', 'scaffold')
        self.assertEqual(code, 0, report)
        self.assertEqual(report['release_mode'], 'candidate')

    def test_valid_profile_is_not_globally_blocked(self):
        code, report = self.audit('year-4-5', 'calibrated')
        self.assertEqual(code, 0, report)
        self.assertEqual(report['release_mode'], 'normal')
