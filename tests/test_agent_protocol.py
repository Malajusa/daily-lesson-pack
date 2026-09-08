import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture, component_result

class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        from agent_registry import AgentRegistry
        from build_execution_plan import freeze_context
        from agent_protocol import component_request
        self.registry=AgentRegistry.load()
        self.request,self.context=context_fixture(self.tmp.name)
        self.context=freeze_context(self.context,self.registry,Path(self.tmp.name))
        self.envelope=component_request(self.context,self.context['timetable_instances'][0],self.registry,'invocation-1')

    def test_projection_omits_unrelated_subject_context(self):
        self.assertNotIn('english_focus',self.envelope['context'])
        self.assertNotIn('timetable',self.envelope['context'])
        self.assertEqual(self.envelope['instance']['id'],'instance-1')

    def test_projection_cannot_mutate_context(self):
        self.envelope['context']['active_year_profile']['value']='other'
        self.assertEqual(self.context['active_year_profile']['value'],'year-4-5')

    def test_valid_result_maps_to_existing_component_contract(self):
        from agent_protocol import validate_component_result, aggregate_components
        result=component_result(self.envelope)
        validate_component_result(result,self.envelope,self.context)
        record,content=aggregate_components(self.context,[result],require_complete=False)
        self.assertEqual(record['schema_version'],2)
        self.assertEqual(content['schema_version'],3)
        self.assertEqual(record['scheduled_instances'],self.context['timetable_instances'])
        self.assertEqual(record['components'][0]['checks'][0]['result'],'PASS')
        self.assertEqual(content['tasks'][0]['fields']['answer'],'5')

    def test_result_identity_time_and_check_bypasses_fail(self):
        from agent_protocol import validate_component_result, ProtocolError
        mutations=[lambda r:r.update(generation_run_id='old-run'),
          lambda r:r.update(invocation_id='other-invocation'),
          lambda r:r['component'].update(owner='dlp-writing-lesson'),
          lambda r:r['component'].update(active_year_profile='year-6'),
          lambda r:r['component'].update(estimated_minutes=31),
          lambda r:r['component'].update(estimated_minutes=True),
          lambda r:r['component'].update(checks=[]),
          lambda r:r['component']['checks'][0].update(status='FAIL'),
          lambda r:r['component']['content']['tasks'][0].update(instance_id='instance-2')]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                result=component_result(self.envelope);mutation(result)
                with self.assertRaises(ProtocolError):validate_component_result(result,self.envelope,self.context)

    def test_paths_and_duplicate_json_keys_are_rejected(self):
        from agent_protocol import safe_path,read_json,ProtocolError
        for path in ('../escape','/absolute','C:/escape','folder\\escape','a/../escape'):
            with self.subTest(path=path),self.assertRaises(ProtocolError):safe_path(Path(self.tmp.name),path)
        p=Path(self.tmp.name)/'duplicate.json';p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ProtocolError):read_json(p)

    def test_immutable_write_refuses_overwrite(self):
        from agent_protocol import write_json_atomic,ProtocolError
        p=Path(self.tmp.name)/'attempt.json';write_json_atomic(p,{'a':1},immutable=True)
        with self.assertRaises(ProtocolError):write_json_atomic(p,{'a':2},immutable=True)
        self.assertEqual(json.loads(p.read_text()),{'a':1})
