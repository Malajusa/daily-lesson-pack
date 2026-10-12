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


    def _request_with_distinct_subject_sources(self, owner):
        from agent_registry import AgentRegistry
        from agent_protocol import component_request, sha256_file
        from build_execution_plan import freeze_context

        root = Path(self.tmp.name) / ("sources-" + owner)
        _, context = context_fixture(root, (owner,))
        english = root / "english-focus.json"
        mathematics = root / "mathematics-focus.json"
        english.write_text('{"focus":"Narrative"}\n', encoding="utf-8")
        mathematics.write_text('{"focus":"Mass"}\n', encoding="utf-8")
        context["english_focus"]["source"] = "english-focus.json"
        context["mathematics_focus"]["source"] = "mathematics-focus.json"
        context["source_provenance"].extend([
            dict(id="english-focus", kind="runtime_school_source",
                 path="english-focus.json", sha256=sha256_file(english)),
            dict(id="mathematics-focus", kind="runtime_school_source",
                 path="mathematics-focus.json", sha256=sha256_file(mathematics)),
        ])
        registry = AgentRegistry.load()
        frozen = freeze_context(context, registry, root)
        return frozen, component_request(
            frozen, frozen["timetable_instances"][0], registry, "projection-test"
        )

    def test_morning_work_provenance_omits_unprojected_subject_sources(self):
        _, envelope = self._request_with_distinct_subject_sources("dlp-morning-work")
        ids = {item["id"] for item in envelope["context"]["source_provenance"]}
        self.assertNotIn("english-focus", ids)
        self.assertNotIn("mathematics-focus", ids)

    def test_literacy_provenance_keeps_english_but_omits_mathematics(self):
        _, envelope = self._request_with_distinct_subject_sources("dlp-literacy-warmup")
        ids = {item["id"] for item in envelope["context"]["source_provenance"]}
        self.assertIn("english-focus", ids)
        self.assertNotIn("mathematics-focus", ids)

    def test_component_request_rejects_unbound_projected_field_source(self):
        from agent_protocol import component_request, ProtocolError
        from agent_registry import AgentRegistry

        root = Path(self.tmp.name) / "unbound-source"
        _, context = context_fixture(root, ("dlp-morning-work",))
        context["lesson_status"]["source"] = "unbound-status.json"
        registry = AgentRegistry.load()
        with self.assertRaises(ProtocolError):
            component_request(
                context, context["timetable_instances"][0], registry, "unbound-test"
            )

    def test_every_generator_keeps_governing_calibration(self):
        from agent_protocol import component_request
        from agent_registry import AgentRegistry
        from build_execution_plan import freeze_context

        registry = AgentRegistry.load()
        for agent in registry.generators():
            with self.subTest(agent=agent.id):
                root = Path(self.tmp.name) / ("calibration-" + agent.id)
                _, context = context_fixture(root, (agent.id,))
                frozen = freeze_context(context, registry, root)
                envelope = component_request(
                    frozen, frozen["timetable_instances"][0], registry,
                    "calibration-" + agent.id
                )
                self.assertEqual(
                    envelope["context"]["instructional_calibration"],
                    frozen["instructional_calibration"],
                )

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
