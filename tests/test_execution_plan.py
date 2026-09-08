import copy
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture

class PlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        from agent_registry import AgentRegistry
        self.registry=AgentRegistry.load()
        _,self.context=context_fixture(self.tmp.name)

    def test_repeated_maths_instances_each_require_critic(self):
        from build_execution_plan import freeze_context,build_execution_plan,validate_execution_plan
        context=freeze_context(self.context,self.registry,Path(self.tmp.name))
        plan=build_execution_plan(context,self.registry)
        self.assertEqual(plan,build_execution_plan(context,self.registry))
        nodes={n['id']:n for n in plan['nodes']}
        self.assertEqual(nodes['critic:instance-2']['depends_on'],['generate:instance-2'])
        self.assertEqual(nodes['critic:instance-3']['depends_on'],['generate:instance-3'])
        self.assertEqual(nodes['assemble']['depends_on'],['generate:instance-1','critic:instance-2','critic:instance-3'])
        self.assertEqual(len(nodes['release']['depends_on']),3)
        validate_execution_plan(context,plan,self.registry)

    def test_plan_cannot_omit_critic_or_release_review(self):
        from build_execution_plan import build_execution_plan,validate_execution_plan
        from agent_protocol import ProtocolError
        plan=build_execution_plan(self.context,self.registry)
        plan['nodes'][-1]['depends_on']=[]
        with self.assertRaises(ProtocolError):validate_execution_plan(self.context,plan,self.registry)

    def test_unfrozen_context_duplicate_instance_and_false_sources_fail(self):
        from build_execution_plan import freeze_context,build_execution_plan
        from agent_protocol import ProtocolError
        unfrozen=copy.deepcopy(self.context);unfrozen['frozen']=False
        with self.assertRaises(ProtocolError):build_execution_plan(unfrozen,self.registry)
        duplicate=copy.deepcopy(self.context);duplicate['timetable_instances'].append(duplicate['timetable_instances'][0])
        with self.assertRaises(ProtocolError):freeze_context(duplicate,self.registry,Path(self.tmp.name))
        (Path(self.tmp.name)/'request.json').write_text('changed')
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,Path(self.tmp.name))

    def test_wrong_weekday_and_missing_field_provenance_fail(self):
        from build_execution_plan import freeze_context
        from agent_protocol import ProtocolError
        self.context['day']['value']='Monday'
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,Path(self.tmp.name))
        self.context['day']['value']='Tuesday';self.context['english_focus']['source']='invented-source'
        with self.assertRaises(ProtocolError):freeze_context(self.context,self.registry,Path(self.tmp.name))
