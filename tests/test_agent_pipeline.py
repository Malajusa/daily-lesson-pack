import asyncio
import copy
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from agent_fixtures import context_fixture,component_result


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        from agent_registry import AgentRegistry
        from agent_protocol import component_request,aggregate_components,write_json_atomic
        from build_execution_plan import freeze_context
        from agent_pipeline import RepositoryPipeline
        request,context=context_fixture(self.root/'sources',('dlp-morning-work',))
        registry=AgentRegistry.load();context=freeze_context(context,registry,self.root/'sources')
        req=component_request(context,context['timetable_instances'][0],registry,'test-invocation')
        record,content=aggregate_components(context,[component_result(req)])
        self.inputs={}
        for name,value in dict(request=request,context=context,content=content,component_record=record).items():
            path=self.root/(name+'.json');write_json_atomic(path,value);self.inputs[name+'_path']=path
        self.pipeline=RepositoryPipeline([sys.executable,str(ROOT/'tests/agent_test_assembler.py')])

    def stage(self):
        return asyncio.run(self.pipeline.assemble(run_root=self.root/'run',revision=1,**self.inputs))

    def test_stages_all_artifacts_and_renders_via_existing_runtime(self):
        from agent_protocol import read_json,sha256_file
        from pack_evidence import audit_pack
        candidate=self.stage()
        manifest=read_json(candidate.root/'manifest.json')
        self.assertTrue((candidate.root/'briefing.pptx').is_file())
        self.assertEqual(len(list((candidate.root/'renders').glob('*.png'))),4)
        self.assertEqual(audit_pack(candidate.root/'manifest.json',candidate.root/'content.json',candidate.root/'context.json')[0],[])
        self.assertEqual(read_json(candidate.root/'component-record.json')['artifact_sha256'],sha256_file(candidate.root/'pack.pptx'))
        self.assertEqual(read_json(candidate.root/'candidate-status.json')['status'],'CANDIDATE')
        self.assertFalse((self.root/'run/released').exists())
        inputs=self.pipeline.review_inputs(candidate)
        self.assertFalse(any(Path(i['path']).name=='component-record.json' for i in inputs))
        self.assertTrue(any(Path(i['path']).name=='briefing.pptx' for i in inputs))

    def test_missing_render_stale_hash_and_path_escape_block(self):
        from agent_protocol import ProtocolError,read_json,write_json_atomic
        from agent_pipeline import manifest_payloads
        candidate=self.stage();path=candidate.root/'manifest.json';original=read_json(path)
        mutations=[lambda m:m['renders'].pop(),lambda m:m['renders'][0].update(sha256='0'*64),
                   lambda m:m['artifacts'][0].update(path='../pack.pptx')]
        for change in mutations:
            bad=copy.deepcopy(original);change(bad);write_json_atomic(path,bad)
            with self.assertRaises(ProtocolError):manifest_payloads(candidate.root)
        write_json_atomic(path,original)

    def test_missing_host_receipts_cannot_release(self):
        candidate=self.stage()
        with self.assertRaises((KeyError,ValueError)):
            asyncio.run(self.pipeline.release(candidate,{},generation_actors={'synthetic-generator'},run_root=self.root/'run'))
        self.assertFalse((self.root/'run/released').exists())

    def test_runtime_receipt_translation_preserves_host_transcript(self):
        from agent_adapter import AgentExecution
        from agent_protocol import read_json,sha256_file
        from validate_agent_artifacts import export_release_review
        candidate=self.stage()
        value=dict(generation_run_id='test-generation',checks=[],**candidate.hashes())
        execution=AgentExecution(value,'actual-test-reviewer','actual-test-execution','external-runner','raw\r\ntranscript\n')
        path,trace=export_release_review(value,execution,method='semantic',generation_actors={'test-author'},evidence_dir=self.root/'evidence')
        receipt=read_json(trace)
        transcript=self.root/'evidence'/receipt['transcript_path']
        self.assertEqual(transcript.read_bytes(),b'raw\r\ntranscript\n')
        self.assertEqual(receipt['review_sha256'],sha256_file(path))
        self.assertEqual(receipt['execution_id'],'actual-test-execution')
        self.assertEqual(receipt['generator_actors'],['test-author'])


class CommandAdapterTests(unittest.TestCase):
    def test_real_subprocess_adapter_returns_actual_host_wrapper(self):
        from agent_adapter import JsonCommandAdapter
        code='import json,sys; q=json.load(sys.stdin); print(json.dumps(dict(result=q,receipt=dict(actor="test-host",execution_id="execution-1",source="external-runner"),transcript="raw test transcript")))'
        adapter=JsonCommandAdapter({'test-agent':[sys.executable,'-c',code]})
        execution=asyncio.run(adapter.invoke(agent_id='test-agent',request={'test':True}))
        self.assertEqual(execution.result,{'test':True})
        self.assertEqual(execution.actor,'test-host')

    def test_timeout_is_bounded_and_shell_string_is_rejected(self):
        from agent_adapter import run_json_command
        from agent_protocol import ProtocolError
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(TimeoutError):
                asyncio.run(run_json_command([sys.executable,'-c','import time; time.sleep(2)'],{},cwd=Path(directory),timeout=.02))
            with self.assertRaises(ProtocolError):
                asyncio.run(run_json_command('echo test',{},cwd=Path(directory)))


class ReleaseBridgeTests(unittest.TestCase):
    setUp=PipelineTests.setUp
    stage=PipelineTests.stage

    def test_real_final_audit_rejects_synthetic_teaching_pack(self):
        from agent_adapter import AgentExecution
        from agent_protocol import read_json
        candidate=self.stage()
        manifest=read_json(candidate.root/'manifest.json')
        reviews={}
        for method,agent in [('semantic','semantic-reviewer'),('visual','visual-reviewer')]:
            checks=[]
            for target in self.pipeline.expected(candidate,method):
                subject=target['target']
                binding=manifest['bindings'][0]
                if method=='visual':
                    artifact,page=subject.rsplit(':',1)
                    binding=next(b for b in manifest['bindings'] if b['artifact']==artifact and b['page']==int(page))
                citation={k:binding[k] for k in ('artifact','page','shape_id')}
                if method=='semantic':citation['quote']='Calculate 2 + 3.'
                checks.append(dict(**target,status='PASS',evidence={'observation':'Synthetic review for release-refusal integration testing only.',
                                                                 'citations':[citation]}))
            result=dict(generation_run_id='test-generation-20260908',checks=checks,**candidate.hashes())
            execution=AgentExecution(result,'synthetic-'+agent,'test-'+method,'external-runner',
                                     'Synthetic execution; this is not live pedagogical review.')
            reviews[agent]=(result,execution)
        result=asyncio.run(self.pipeline.release(candidate,reviews,generation_actors={'synthetic-author'},run_root=self.root/'run'))
        self.assertEqual(result['status'],'CANDIDATE',result)
        report=read_json(candidate.root/'release-audit.json')
        self.assertEqual(report['status'],'FAIL')
        self.assertTrue(report['failures'])
        self.assertFalse((self.root/'run/released').exists())
