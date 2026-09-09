"""Host configuration is real input; model-generated authority is not authentication."""
import copy
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture
from agent_protocol import ProtocolError, sha256_file
from agent_registry import AgentRegistry
from build_execution_plan import freeze_context
from dlp_build_runtime import validate_resolved_context
from resolve_instructional_calibration import resolve
from teacher_context_store import SettingsStore

class HostSettingsBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.sources=Path(self.tmp.name)/'sources'
        self.request,self.context=context_fixture(self.sources)
        self.binding=dict(store=str(Path(self.tmp.name)/'private/settings.sqlite'),teacher='teacher',classroom='room')
        self.store=SettingsStore(Path(self.binding['store']))
        self.store.change('teacher','room',{'literacy_sequence_count':5},expected_revision=0,
                          scope={'kind':'standing'},authority={'kind':'teacher_request','source_id':'standing-request'})

    def prepare(self):
        mod=importlib.import_module('resolve_instructional_calibration')
        self.assertTrue(callable(getattr(mod,'prepare_host_context',None)),'Actual host settings preparation is missing')
        return mod.prepare_host_context(self.context,self.request,settings=self.binding,
            source_root=self.sources,request_source='request.json')

    def test_standing_settings_reach_frozen_component_context(self):
        context=self.prepare()
        frozen=freeze_context(context,AgentRegistry.load(),self.sources)
        self.assertEqual(frozen['warmup_counts']['literacy'],5)
        self.assertEqual(frozen['instructional_calibration']['settings_revision'],1)

    def test_explicit_request_wins_without_saving(self):
        self.request['instructional_overrides']={'literacy_sequence_count':3}
        path=self.sources/'request.json';path.write_text(json.dumps(self.request))
        self.context['source_provenance'][0]['sha256']=sha256_file(path)
        context=self.prepare()
        self.assertEqual(context['instructional_calibration']['values']['literacy_sequence_count'],3)
        self.assertEqual(self.store.read('teacher','room')['revision'],1)

    def test_unhashed_override_cannot_become_current_instruction(self):
        self.request['instructional_overrides']={'literacy_sequence_count':3}
        with self.assertRaises(ProtocolError):self.prepare()

    def test_corrupt_configured_store_cannot_fall_back(self):
        Path(self.binding['store']).write_bytes(b'corrupt')
        with self.assertRaises(ProtocolError):self.prepare()

    def test_private_binding_never_enters_agent_context(self):
        context=self.prepare()
        self.assertNotIn(self.binding['store'],json.dumps(context))
        self.assertNotIn('classroom',context['instructional_calibration'])

    def test_direct_staging_rejects_unbacked_count_override(self):
        self.context['warmup_counts']={'literacy':99}
        self.assertTrue(validate_resolved_context(self.context))

    def test_direct_staging_rejects_tampered_calibration(self):
        self.context['instructional_calibration']=resolve(on='2026-09-08')
        self.context['instructional_calibration']['profile']['release_mode']='banana'
        self.assertTrue(validate_resolved_context(self.context))

    def test_outside_curriculum_coverage_does_not_silently_promote(self):
        mod=importlib.import_module('resolve_instructional_calibration')
        self.assertTrue(callable(getattr(mod,'instructional_context_errors',None)),'Release calibration audit missing')
        calibration=resolve(on='2026-09-08',overrides={'main_curriculum_year':12},request_source='request.json')
        self.context.update(instructional_calibration=calibration,warmup_counts={'literacy':10,'numeracy':5})
        self.assertTrue(mod.instructional_context_errors(self.context,require_release=True))

if __name__=='__main__':unittest.main()
