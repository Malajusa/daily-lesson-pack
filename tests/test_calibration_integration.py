"""Calibration reaches real runtime boundaries, rather than only a helper test."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture
from agent_registry import AgentRegistry
from agent_protocol import ProtocolError, sha256_file, component_request, required_component_checks
from build_execution_plan import freeze_context
from resolve_instructional_calibration import resolve

class CalibrationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.sources=Path(self.tmp.name)
        _,self.context=context_fixture(self.sources)
        self.registry=AgentRegistry.load()

    def test_default_calibration_is_frozen_automatically(self):
        result=freeze_context(self.context,self.registry,self.sources)
        self.assertIn('instructional_calibration',result)
        self.assertEqual(result['instructional_calibration']['values']['main_curriculum_year'],5)

    def test_defaults_are_source_hashed(self):
        result=freeze_context(self.context,self.registry,self.sources)
        self.assertIn('config/creator-defaults.json',[s['path'] for s in result['source_provenance']])

    def test_missing_profile_uses_creator_default_not_an_invented_profile(self):
        del self.context['active_year_profile']
        result=freeze_context(self.context,self.registry,self.sources)
        self.assertEqual(result['active_year_profile']['value'],'year-4-5')

    def test_missing_timetable_is_still_blocked(self):
        del self.context['timetable']
        with self.assertRaises(ProtocolError): freeze_context(self.context,self.registry,self.sources)

    def test_all_generators_receive_the_same_calibration(self):
        frozen=freeze_context(self.context,self.registry,self.sources)
        for index,instance in enumerate(frozen['timetable_instances']):
            request=component_request(frozen,instance,self.registry,f'invocation-{index}')
            self.assertIn('instructional_calibration',request['context'])
            self.assertEqual(request['context']['instructional_calibration'],frozen['instructional_calibration'])

    def test_caller_only_calibration_is_rejected(self):
        self.context['instructional_calibration']=resolve(on='2026-09-08')
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,self.sources)

    def test_hashed_sidecar_is_used_and_controls_counts(self):
        calibration=resolve(on='2026-09-08',overrides={'literacy_sequence_count':5},request_source='request.json')
        file=self.sources/'calibration.json';file.write_text(json.dumps(calibration))
        self.context['instructional_calibration']=calibration
        self.context['calibration_source']='calibration.json'
        self.context['source_provenance'].append(dict(id='calibration-source',path='calibration.json',
            kind='runtime_school_source',sha256=sha256_file(file)))
        frozen=freeze_context(self.context,self.registry,self.sources)
        self.assertEqual(frozen['warmup_counts']['literacy'],5)
        file.write_text('{}')
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,self.sources)

    def test_mismatched_count_cannot_bypass_resolved_preference(self):
        self.context['warmup_counts']={'literacy':99}
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,self.sources)

    def test_legacy_paths_are_not_required_on_any_profile(self):
        for profile in ('year-4-5','year-6'):
            context=copy.deepcopy(self.context);context['active_year_profile']['value']=profile
            checks=required_component_checks(context,'dlp-maths-lesson')
            self.assertNotIn('MATHS.YEAR4.PATHWAY',checks)
            self.assertNotIn('MATHS.YEAR5.PATHWAY',checks)
            self.assertIn('MATHS.POINT_OF_NEED',checks)
            self.assertIn('MATHS.READINESS.CHECK',checks)

    def test_enrolment_only_change_does_not_change_checks(self):
        checks=[]
        for year in (3,4,5,6):
            context=copy.deepcopy(self.context);context['enrolment_year']=year
            checks.append(required_component_checks(context,'dlp-maths-lesson'))
        self.assertTrue(all(value==checks[0] for value in checks))

    def test_default_freeze_is_idempotent_when_profile_was_omitted(self):
        del self.context['active_year_profile']
        first=freeze_context(self.context,self.registry,self.sources)
        self.assertEqual(freeze_context(first,self.registry,self.sources),first)

    def test_missing_resolved_value_is_a_protocol_failure(self):
        from resolve_instructional_calibration import validate_calibration
        calibration=resolve(on='2026-09-08')
        del calibration['values']['timezone'];del calibration['provenance']['timezone']
        with self.assertRaises(ProtocolError):validate_calibration(calibration)

    def test_unknown_provenance_scope_is_rejected(self):
        from resolve_instructional_calibration import validate_calibration
        calibration=resolve(on='2026-09-08')
        calibration['provenance']['timezone']['scope']={'kind':'invented'}
        with self.assertRaises(ProtocolError):validate_calibration(calibration)

if __name__=="__main__":unittest.main()
