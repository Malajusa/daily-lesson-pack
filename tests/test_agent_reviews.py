import copy
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

class ReviewTests(unittest.TestCase):
    def fixture(self):
        expected=[{'check_id':'CHECK.ONE','target':'task-1'}]
        binding={key:'a'*64 for key in ('artifact_sha256','manifest_sha256','content_sha256','requirements_sha256')}
        request=dict(generation_run_id='test-run',invocation_id='test-inv',agent_id='semantic-reviewer',
          context_sha256='a'*64,review_run_id='test-review',bindings=binding,
          expected_checks=expected,task_type='REVIEW_PACK',instance=None)
        evidence=dict(observation='Synthetic review evidence for one canonical task.',
          citations=[dict(artifact='deck',page=1,shape_id=2,quote='5')])
        result=dict(protocol_version=1,result_type='REVIEW',status='PASS',reviewer='semantic-reviewer',
          **{k:request[k] for k in ('generation_run_id','invocation_id','agent_id','context_sha256','review_run_id')},
          **binding,checks=[dict(check_id='CHECK.ONE',target='task-1',status='PASS',evidence=evidence)],defects=[])
        content=dict(instances=[dict(id='instance-1',owner='dlp-morning-work')],
                     tasks=[dict(id='task-1',instance_id='instance-1')])
        manifest=dict(bindings=[dict(artifact='deck',page=1,record='task-1')])
        return request,result,content,manifest

    def test_review_rejects_missing_duplicate_stale_and_false_pass(self):
        from validate_agent_artifacts import validate_review_result
        from agent_protocol import ProtocolError
        request,result,content,manifest=self.fixture()
        validate_review_result(result,request,content,manifest)
        mutations=[lambda r:r.update(checks=[]),lambda r:r['checks'].append(copy.deepcopy(r['checks'][0])),
          lambda r:r.update(artifact_sha256='b'*64),lambda r:r.update(status='FAIL'),
          lambda r:r['checks'][0].update(status='FAIL')]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                bad=copy.deepcopy(result);mutate(bad)
                with self.assertRaises(ProtocolError):validate_review_result(bad,request,content,manifest)

    def test_defect_cannot_route_to_another_owner(self):
        from validate_agent_artifacts import route_defects
        from agent_protocol import ProtocolError
        _,_,content,manifest=self.fixture()
        defect=dict(defect_id='defect-1',owner='dlp-writing-lesson',instance_id='instance-1',
                    task_id='task-1',scope='task',severity='release_blocking')
        with self.assertRaises(ProtocolError):route_defects([defect],content,manifest)
        defect['owner']='dlp-morning-work'
        self.assertEqual(list(route_defects([defect],content,manifest)),['instance-1'])

    def test_visual_na_is_not_a_pass(self):
        from validate_agent_artifacts import validate_review_result
        from agent_protocol import ProtocolError
        request,result,content,manifest=self.fixture()
        request['agent_id']='visual-reviewer';result['agent_id']='visual-reviewer';result['reviewer']='visual-reviewer'
        result['checks'][0].update(status='NA',applicability_reason='Not applicable')
        with self.assertRaises(ProtocolError):validate_review_result(result,request,content,manifest)

    def test_page_defect_cannot_claim_an_unrelated_instance(self):
        from validate_agent_artifacts import route_defects
        from agent_protocol import ProtocolError
        _,_,content,manifest=self.fixture()
        content['instances'].append(dict(id='instance-2',owner='dlp-writing-lesson'))
        content['tasks'].append(dict(id='task-2',instance_id='instance-2'))
        defect=dict(defect_id='defect-page',owner='dlp-writing-lesson',scope='page',
                    instance_id='instance-2',artifact_id='deck',page=1,severity='release_blocking')
        with self.assertRaises(ProtocolError):route_defects([defect],content,manifest)

    def test_defect_scope_requires_its_canonical_target(self):
        from validate_agent_artifacts import route_defects
        from agent_protocol import ProtocolError
        _,_,content,manifest=self.fixture()
        defect=dict(defect_id='defect-task',owner='dlp-morning-work',scope='task',
                    instance_id='instance-1',severity='release_blocking')
        with self.assertRaises(ProtocolError):route_defects([defect],content,manifest)
