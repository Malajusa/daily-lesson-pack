"""Executable control-plane tests; synthetic agents are not teaching QA evidence."""
import asyncio
import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from agent_fixtures import component_result, context_fixture


def review_result(request):
    return dict(protocol_version=1, generation_run_id=request['generation_run_id'],
        invocation_id=request['invocation_id'], agent_id=request['agent_id'],
        context_sha256=request['context_sha256'], review_run_id=request['review_run_id'],
        reviewer=request['agent_id'], result_type='REVIEW', status='PASS',
        **request['bindings'], checks=[dict(**c, status='PASS', evidence=dict(
            observation='Synthetic independent control-plane check, not teaching quality.',
            citations=['component:'+request['instance']['id']] if request['instance'] else
                      [dict(artifact='deck',page=1,shape_id=1,quote='5')]))
            for c in request['expected_checks']], defects=[])


class RecordingAdapter:
    def __init__(self):
        self.calls=[]
        self.running=0
        self.peak=0
        self.break_once=False
        self.self_review=False
        self.fail_critic=False
        self.mutate=None

    async def invoke(self, *, agent_id, request):
        from agent_adapter import AgentExecution
        self.calls.append(copy.deepcopy(request))
        self.running+=1
        self.peak=max(self.peak,self.running)
        await asyncio.sleep(0.005)
        self.running-=1
        if self.mutate:
            self.mutate()
        generation=request['task_type'] in ('GENERATE_COMPONENT','REPAIR_COMPONENT')
        result=component_result(request) if generation else review_result(request)
        if generation and self.break_once:
            self.break_once=False
            result['component']['owner']='dlp-writing-lesson'
        if not generation and self.fail_critic:
            result['status']='FAIL'  # Invalid failure without check/defect evidence must block.
        actor='synthetic-generator' if generation or self.self_review else 'synthetic-reviewer'
        return AgentExecution(result,actor,'host-'+request['invocation_id'],'external-runner',
                              'Synthetic test execution '+request['invocation_id'])


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        from agent_registry import AgentRegistry
        from agent_orchestrator import DailyPackOrchestrator
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.request,self.context=context_fixture(self.root/'sources')
        self.registry=AgentRegistry.load()
        self.adapter=RecordingAdapter()
        self.runner=DailyPackOrchestrator(registry=self.registry,adapter=self.adapter,
                                          run_root=self.root/'run',max_parallelism=2)

    def run_pack(self,stop=True):
        return asyncio.run(self.runner.run(request=self.request,context=self.context,
                     source_root=self.root/'sources',stop_after_components=stop))

    def test_parallel_instances_have_separate_critics_and_v2_record(self):
        status=self.run_pack()
        self.assertEqual(status['status'],'COMPONENTS_VALIDATED', status)
        self.assertFalse(status['release_ready'])
        self.assertEqual(self.adapter.peak,2)
        self.assertEqual(len([c for c in self.adapter.calls if c['agent_id']=='maths-critic']),2)
        from agent_protocol import read_json
        record=read_json(Path(status['component_record']))
        self.assertEqual(len(record['components']),3)
        self.assertEqual(record['schema_version'],2)
        self.assertEqual(record['scheduled_instances'],self.context['timetable_instances'])
        self.assertFalse((self.root/'run/released').exists())

    def test_invalid_owner_retries_with_fresh_identity_and_retains_attempts(self):
        self.adapter.break_once=True
        status=self.run_pack()
        self.assertEqual(status['status'],'COMPONENTS_VALIDATED',status)
        repairs=[c for c in self.adapter.calls if c['task_type']=='REPAIR_COMPONENT']
        self.assertEqual(len(repairs),1)
        self.assertEqual(repairs[0]['instance']['id'],'instance-1')
        self.assertEqual(repairs[0]['defects'][0]['owner'],'dlp-morning-work')
        self.assertEqual(len(list((self.root/'run/results').glob('*-receipt.json'))),6)
        self.assertEqual(len(list((self.root/'run/requests').glob('*.json'))),6)

    def test_reviewer_actor_cannot_equal_generator(self):
        self.adapter.self_review=True
        status=self.run_pack()
        self.assertEqual(status['status'],'BLOCKED',status)
        self.assertIn('independent',status['reason'].lower())
        self.assertFalse((self.root/'run/assembly').exists())

    def test_critic_fail_without_defects_blocks_instead_of_self_certifying(self):
        self.adapter.fail_critic=True
        status=self.run_pack()
        self.assertEqual(status['status'],'BLOCKED',status)
        self.assertFalse((self.root/'run/assembly').exists())

    def test_changed_frozen_file_blocks(self):
        target=self.root/'run/context/context.json'
        self.adapter.mutate=lambda: target.write_text('{}')
        status=self.run_pack()
        self.assertEqual(status['status'],'BLOCKED',status)
        self.assertIn('changed',status['reason'].lower())

    def test_missing_assembler_never_reports_release(self):
        status=self.run_pack(stop=False)
        self.assertEqual(status['status'],'BLOCKED',status)
        self.assertIn('assembly',status['reason'].lower())
        self.assertFalse(status['release_ready'])

    def test_existing_run_directory_is_not_reused(self):
        (self.root/'run').mkdir()
        sentinel=self.root/'run/keep.txt'
        sentinel.write_text('preserve')
        with self.assertRaises((ValueError,FileExistsError)):
            self.run_pack()
        self.assertEqual(sentinel.read_text(),'preserve')


class SyntheticPipeline:
    """Only tests scheduling. Intentionally cannot claim RELEASED."""
    def __init__(self):
        self.assemblies=0
        self.release_calls=0

    async def assemble(self, **kwargs):
        import shutil
        from agent_pipeline import Candidate
        from agent_protocol import write_json_atomic
        self.assemblies+=1
        root=kwargs['run_root']/'assembly'/f"revision-{kwargs['revision']}"/'candidate'
        root.mkdir(parents=True)
        for name in ('request','context','content'):
            shutil.copy2(kwargs[name+'_path'],root/(name+'.json'))
        shutil.copy2(kwargs['component_record_path'],root/'component-record.json')
        (root/'pack.pptx').write_bytes(b'Synthetic non-PPTX, cannot pass real release')
        write_json_atomic(root/'manifest.json',{'schema_version':3,'revision':kwargs['revision'],
          'bindings':[dict(artifact='deck',page=1,record='instance-1-task')]})
        return Candidate(root,kwargs['revision'])

    def snapshot(self,candidate):
        from agent_protocol import sha256_file
        return {p:sha256_file(p) for p in candidate.root.iterdir() if p.is_file()}

    def review_inputs(self,candidate):
        return []

    def expected(self,candidate,method):
        return [dict(check_id='CHECK.ONE',target='instance-1-task')]

    async def provenance(self,candidate,request):
        return review_result(request)

    async def release(self,*args,**kwargs):
        self.release_calls+=1
        return {'status':'CANDIDATE','reason':'Synthetic test pipeline cannot release teaching artefacts.'}


class RepairAdapter(RecordingAdapter):
    def __init__(self, *, persistent=False):
        super().__init__()
        self.rounds=0
        self.persistent=persistent
        self.last_defect=None

    async def invoke(self, *, agent_id,request):
        from agent_adapter import AgentExecution
        execution=await super().invoke(agent_id=agent_id,request=request)
        if agent_id!='semantic-reviewer':
            return execution
        self.rounds+=1
        if self.rounds>1 and not self.persistent:
            return execution
        result=execution.result
        result['status']='FAIL'
        result['checks'][0]['status']='FAIL'
        self.last_defect=dict(defect_id='def-'+request['invocation_id'],
            generation_run_id=request['generation_run_id'],review_run_id=request['review_run_id'],
            check_id='CHECK.ONE',severity='release_blocking',owner='dlp-morning-work',scope='task',
            instance_id='instance-1',task_id='instance-1-task',
            description='Synthetic owner-specific defect to test routing.',
            evidence={'observation':'Synthetic failure for complete-QA invalidation test.',
                      'citations':[dict(artifact='deck',page=1,shape_id=1,quote='5')]},
            required_correction='Repair only the first morning-work instance in this synthetic test.')
        result['defects']=[self.last_defect]
        return AgentExecution(result,execution.actor,execution.execution_id,execution.source,execution.transcript)


class RepairLoopTests(unittest.TestCase):
    setUp=OrchestratorTests.setUp
    run_pack=OrchestratorTests.run_pack

    def test_pack_defects_repair_only_owner_and_rerun_every_review(self):
        self.adapter=RepairAdapter()
        self.runner.adapter=self.adapter
        pipeline=SyntheticPipeline()
        self.runner.pipeline=pipeline
        status=self.run_pack(stop=False)
        self.assertEqual(status['status'],'CANDIDATE',status)
        self.assertEqual(pipeline.assemblies,2)
        self.assertEqual(pipeline.release_calls,1)
        self.assertEqual(status['attempts'],{'instance-1':2,'instance-2':1,'instance-3':1})
        repairs=[c for c in self.adapter.calls if c['task_type']=='REPAIR_COMPONENT']
        self.assertEqual(len(repairs),1)
        self.assertEqual(repairs[0]['defects'][0]['defect_id'],self.adapter.last_defect['defect_id'])
        self.assertEqual(len([c for c in self.adapter.calls if c['agent_id']=='visual-reviewer']),2)
        from agent_protocol import read_json
        events=read_json(self.root/'run/plan/state.json')['events']
        invalidated={e['node'] for e in events if e['to']=='STALE'}
        self.assertTrue({'assemble','qa:semantic-reviewer','qa:visual-reviewer','qa:provenance-reviewer'}<=invalidated)
        self.assertEqual(len(list((self.root/'run/assembly').glob('revision-*'))),2)

    def test_repeated_pack_defect_exhausts_budget_without_release(self):
        self.runner.adapter=RepairAdapter(persistent=True)
        pipeline=SyntheticPipeline();self.runner.pipeline=pipeline
        status=self.run_pack(stop=False)
        self.assertEqual(status['status'],'CANDIDATE',status)
        self.assertIn('budget exhausted',status['reason'])
        self.assertEqual(pipeline.assemblies,2)
        self.assertEqual(pipeline.release_calls,0)
        self.assertEqual(status['attempts']['instance-1'],2)

    def test_protocol_retry_and_pack_repair_share_one_budget(self):
        self.runner.adapter=RepairAdapter();self.runner.adapter.break_once=True
        pipeline=SyntheticPipeline();self.runner.pipeline=pipeline
        status=self.run_pack(stop=False)
        self.assertEqual(status['attempts']['instance-1'],2)
        self.assertIn('budget exhausted',status['reason'])
        self.assertEqual(pipeline.assemblies,1)
        self.assertEqual(pipeline.release_calls,0)
