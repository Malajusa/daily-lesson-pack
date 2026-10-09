import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_interactive_lesson_contract import audit, DOMAINS

class InteractiveContractTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT/'examples/benchmarks/interactive-maths-regression.json').read_text())
        self.record = copy.deepcopy(self.fixture['valid'])
        self.source = self.fixture['source'].encode()

    def test_valid_structure_is_not_teaching_acceptance(self):
        result = audit(self.record, self.source)
        self.assertEqual(result['structure'], 'PASS')
        self.assertEqual(result['teaching_quality'], 'UNVERIFIED')
        self.assertEqual(len(result['missing_review_coverage']), 4)

    def test_faulty_authored_contracts(self):
        for fault in self.fixture['faults']:
            with self.subTest(fault['name']):
                record = copy.deepcopy(self.record)
                record['lessons'][0][fault['field']] = fault['value']
                self.assertIn(fault['code'], [i['code'] for i in audit(record,self.source)['issues']])

    def test_teaching_state_requires_actual_fields(self):
        for field in ('prompt','explanation','notation','representation'):
            with self.subTest(field):
                record = copy.deepcopy(self.record)
                del record['lessons'][0]['scenes'][0][field]
                self.assertEqual(audit(record,self.source)['structure'],'FAIL')

    def test_missing_identity_role_and_null_fields_fail(self):
        for field,value,code in [('id',None,'SCENE_ID'),('role',None,'SCENE_ROLE'),('role','modle','SCENE_ROLE'),('prompt',None,'TEACHING_STATE')]:
            with self.subTest(field=field,value=value):
                record=copy.deepcopy(self.record)
                record['lessons'][0]['scenes'][0][field]=value
                self.assertIn(code,[i['code'] for i in audit(record,self.source)['issues']])
        self.record['lessons'][0]['concept_boundary']=None
        self.assertIn('PLANNING_FIELD',[i['code'] for i in audit(self.record,self.source)['issues']])

    def test_independent_task_can_omit_scaffold(self):
        scene = self.record['lessons'][0]['scenes'][0]
        scene.update(role='independent',representation='',notation='1500 g = ? kg')
        self.assertEqual(audit(self.record,self.source)['structure'],'PASS')

    def test_entry_and_reveal_state_coverage(self):
        self.record['lessons'][0]['scenes'][0]['states']=['final']
        self.assertIn('STATE_INVENTORY',[i['code'] for i in audit(self.record,self.source)['issues']])
        self.record['lessons'][0]['scenes'][0]['states']=['entry','reveal-1']
        self.assertEqual(len(audit(self.record,self.source)['missing_review_coverage']),8)

    def test_omitted_or_duplicate_lesson_is_detected(self):
        for lessons in ([], self.record['lessons']*2):
            record = {**self.record,'lessons':lessons}
            self.assertIn('INVENTORY',[i['code'] for i in audit(record,self.source)['issues']])

    def test_changed_source_invalidates_review(self):
        self.record['reviews'] = [{'lesson_id':'mass','scene_id':'meaning','state_id':'entry','domain':'visual',
            'source_sha256':self.record['source_sha256'],'observation':'Inspected front-face margins.',
            'evidence':'fixture-render'}]
        result = audit(self.record,self.source+b' revised')
        self.assertIn('SOURCE_BINDING',[i['code'] for i in result['issues']])
        self.assertIn('STALE_REVIEW',[i['code'] for i in result['issues']])

    def test_invalid_lesson_identifiers_cannot_match_inventory(self):
        for identifier in ('', '  ', None, 7):
            with self.subTest(identifier=identifier):
                record = copy.deepcopy(self.record)
                record['expected_lessons'] = [identifier]
                record['lessons'][0]['id'] = identifier
                result = audit(record, self.source)
                self.assertEqual(result['structure'], 'FAIL')
                self.assertIn('LESSON_ID', [issue['code'] for issue in result['issues']])
                self.assertIn('INVENTORY', [issue['code'] for issue in result['issues']])

    def test_all_declared_reviews_still_do_not_certify_quality(self):
        self.record['reviews'] = [{'lesson_id':'mass','scene_id':'meaning','state_id':'entry','domain':domain,
            'source_sha256':self.record['source_sha256'],'observation':'Fixture observation.',
            'evidence':'fixture-evidence'} for domain in DOMAINS]
        result = audit(self.record,self.source)
        self.assertEqual(result['missing_review_coverage'],[])
        self.assertEqual(result['teaching_quality'],'UNVERIFIED')

if __name__ == '__main__':
    unittest.main()
