import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture,component_result


class IntegrationTests(unittest.TestCase):
    def test_existing_runtime_checks_context_generation_identity(self):
        from dlp_build_runtime import validate_component_record
        from agent_registry import AgentRegistry
        from agent_protocol import aggregate_components,component_request
        with tempfile.TemporaryDirectory() as directory:
            _,context=context_fixture(Path(directory),('dlp-morning-work',))
            registry=AgentRegistry.load()
            request=component_request(context,context['timetable_instances'][0],registry,'test-invocation')
            record,_=aggregate_components(context,[component_result(request)])
            self.assertEqual(validate_component_record(context,record),[])
            record['generation_run_id']='wrong-generation'
            self.assertTrue(any('generation_run_id' in e for e in validate_component_record(context,record)))

    def test_runtime_owners_come_from_validated_registry(self):
        import dlp_build_runtime
        from agent_registry import AgentRegistry
        self.assertTrue(hasattr(dlp_build_runtime,'load_content_components'))
        self.assertEqual(dlp_build_runtime.load_content_components(),{a.id for a in AgentRegistry.load().generators()})

    def test_complete_package_contains_v2_runtime_schemas_and_contracts(self):
        from build_chatgpt_package import build_file_map
        _,files=build_file_map(ROOT)
        required=['scripts/agent_orchestrator.py','scripts/agent_adapter.py','scripts/agent_registry.py',
          'scripts/agent_protocol.py','scripts/agent_pipeline.py','scripts/agent_state.py',
          'scripts/build_execution_plan.py','scripts/validate_agent_artifacts.py',
          'skills/registry.v2.json','requirements.txt','agents/maths-critic.md']
        for path in required:
            self.assertIn(path,files)
        self.assertIn('schemas/year-level-profile.schema.json', files)
        self.assertEqual(len([p for p in files if p.startswith('schemas/')]), 10)
        self.assertIn('skills/registry.json',files)

    def test_package_validator_requires_new_runtime(self):
        from audit_package_dependencies import MANDATORY_RUNTIME_FILES
        self.assertIn('scripts/agent_orchestrator.py',MANDATORY_RUNTIME_FILES)
