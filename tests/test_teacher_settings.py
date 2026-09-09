"""Deterministic settings tests; fresh Python processes are not host activation."""
from __future__ import annotations
import importlib
from contextlib import closing
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

class TeacherSettingsTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT/'scripts/teacher_context_store.py').is_file(), 'Private settings backend is absent')
        self.store_module = importlib.import_module('teacher_context_store')
        self.resolver = importlib.import_module('resolve_instructional_calibration')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'private'/'settings.sqlite'
        self.store = self.store_module.SettingsStore(self.path)
        self.authority = {'kind': 'teacher_request', 'source_id': 'request-20260909'}

    def change(self, values, revision=0, scope=None, teacher='teacher-a', classroom='class-a'):
        return self.store.change(teacher, classroom, values, expected_revision=revision,
            authority=self.authority, scope=scope or {'kind':'standing'})

    def resolve(self, day='2026-09-09', **kwargs):
        state = self.store.read('teacher-a', 'class-a')
        return self.resolver.resolve(state=state, on=day, **kwargs)

    def test_absence_does_not_create_a_store(self):
        self.assertEqual(self.store.read('teacher-a','class-a')['revision'], 0)
        self.assertFalse(self.path.exists())

    def test_confirmed_defaults_load_without_setup(self):
        result = self.resolve()
        self.assertEqual(result['values']['main_curriculum_year'], 5)
        self.assertEqual(result['values']['retrieval_years'], [3,4])
        self.assertEqual(result['values']['differentiation_mode'], 'point-of-need')
        self.assertEqual(result['values']['active_year_profile'], 'year-4-5')
        self.assertNotIn('mathematics_focus', result['values'])

    def test_write_persists_in_a_new_process(self):
        self.change({'literacy_sequence_count':5})
        command = [sys.executable, str(ROOT/'scripts/teacher_context_store.py'), 'show',
                   '--store', str(self.path), '--teacher', 'teacher-a', '--classroom', 'class-a']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        state = json.loads(result.stdout)
        self.assertEqual(state['revision'],1)
        self.assertEqual(state['entries'][0]['values']['literacy_sequence_count'],5)

    def test_current_override_wins_without_becoming_standing(self):
        self.change({'literacy_sequence_count':5})
        self.assertEqual(self.resolve(overrides={'literacy_sequence_count':3}, request_source='today')['values']['literacy_sequence_count'],3)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],5)

    def test_date_scope_expires_to_latest_standing_value(self):
        self.change({'literacy_sequence_count':5})
        self.change({'literacy_sequence_count':3},1,{'kind':'date','start':'2026-09-10','end':'2026-09-10'})
        self.change({'literacy_sequence_count':7},2)
        self.assertEqual(self.resolve('2026-09-10')['values']['literacy_sequence_count'],3)
        self.assertEqual(self.resolve('2026-09-11')['values']['literacy_sequence_count'],7)

    def test_unit_and_lesson_scopes_do_not_leak(self):
        self.change({'literacy_sequence_count':4},scope={'kind':'unit','id':'narrative'})
        self.change({'literacy_sequence_count':2},1,{'kind':'lesson','id':'lesson-7'})
        self.assertEqual(self.resolve(unit_id='narrative')['values']['literacy_sequence_count'],4)
        self.assertEqual(self.resolve(unit_id='narrative',lesson_id='lesson-7')['values']['literacy_sequence_count'],2)
        self.assertEqual(self.resolve(unit_id='reports')['values']['literacy_sequence_count'],10)

    def test_namespaces_are_isolated(self):
        self.change({'literacy_sequence_count':5})
        self.assertEqual(self.store.read('teacher-b','class-a')['revision'],0)
        self.assertEqual(self.store.read('teacher-a','class-b')['revision'],0)

    def test_stale_revision_does_not_overwrite(self):
        self.change({'literacy_sequence_count':5})
        with self.assertRaises(self.store_module.SettingsError):
            self.change({'numeracy_prompt_answer_pairs':4},0)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],5)
        self.assertEqual(self.store.read('teacher-a','class-a')['revision'],1)

    def test_source_document_cannot_authorise_a_save(self):
        with self.assertRaises(self.store_module.SettingsError):
            self.store.change('teacher-a','class-a',{'literacy_sequence_count':5},expected_revision=0,
                authority={'kind':'source_document','source_id':'hostile-overview'},scope={'kind':'standing'})
        self.assertFalse(self.path.exists())

    def test_current_lesson_facts_are_not_preferences(self):
        for field in ('date','timetable','mathematics_focus','english_focus','student_attainment'):
            with self.subTest(field=field), self.assertRaises(self.store_module.SettingsError):
                self.change({field:'invented'})

    def test_invalid_values_rejected_before_any_write(self):
        for values in ({'literacy_sequence_count':True},{'main_curriculum_year':0},
                       {'retrieval_years':[3,3]}, {'active_year_profile':'year-99'},
                       {'differentiation_mode':'permanent-ability-streams'}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.change(values)
        self.assertFalse(self.path.exists())

    def test_corrupt_database_is_not_first_use(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_bytes(b'not SQLite')
        with self.assertRaises(self.store_module.SettingsError):
            self.store.read('teacher-a','class-a')

    def test_future_schema_version_is_rejected(self):
        import sqlite3
        self.change({'literacy_sequence_count':5})
        with closing(sqlite3.connect(self.path)) as conn, conn: conn.execute('PRAGMA user_version=99')
        with self.assertRaises(self.store_module.SettingsError): self.resolve()

    def test_write_failure_never_returns_saved(self):
        parent = Path(self.temp.name)/'not-a-directory'
        parent.write_text('occupied')
        broken = self.store_module.SettingsStore(parent/'settings.sqlite')
        with self.assertRaises(self.store_module.SettingsError):
            broken.change('t','c',{'literacy_sequence_count':5},expected_revision=0,
                          authority=self.authority,scope={'kind':'standing'})

    def test_undo_appends_a_new_revision(self):
        self.change({'literacy_sequence_count':5})
        self.change({'literacy_sequence_count':3},1)
        restored = self.store.undo('teacher-a','class-a',expected_revision=2,authority=self.authority)
        self.assertEqual(restored['revision'],3)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],5)

    def test_forget_removes_values_from_history(self):
        self.change({'literacy_sequence_count':5,'numeracy_prompt_answer_pairs':4})
        self.store.forget('teacher-a','class-a',['literacy_sequence_count'],expected_revision=1,authority=self.authority)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],10)
        self.assertEqual(self.resolve()['values']['numeracy_prompt_answer_pairs'],4)
        self.assertNotIn('literacy_sequence_count', json.dumps(self.store.history('teacher-a','class-a')))

    def test_profile_change_does_not_inherit_creator_retrieval_band(self):
        result = self.resolve(overrides={'active_year_profile':'year-6'},request_source='profile-change')
        self.assertEqual(result['values']['main_curriculum_year'],6)
        self.assertEqual(result['values']['retrieval_years'],[])
        self.assertEqual(result['profile']['release_mode'],'candidate')

    def test_all_values_have_provenance(self):
        self.change({'literacy_sequence_count':5})
        result = self.resolve()
        self.assertEqual(set(result['values']),set(result['provenance']))
        for record in result['provenance'].values():
            self.assertTrue(record['source'])
            self.assertIn('revision',record)
            self.assertIn('scope',record)

    def test_store_cannot_be_inside_distributable(self):
        with self.assertRaises(self.store_module.SettingsError):
            self.store_module.SettingsStore(ROOT/'private-settings.sqlite')

    def test_schema_validates_resolved_sidecar(self):
        from agent_protocol import validate_json
        validate_json(self.resolve(), ROOT/'schemas/instructional-calibration.schema.json')

    def test_tampered_snapshot_is_not_accepted_as_settings(self):
        state = self.store.read('teacher-a','class-a')
        state['schema_version']=99
        with self.assertRaises(ValueError): self.resolver.resolve(state=state,on='2026-09-09')

    def test_row_revision_must_match_payload_revision(self):
        import sqlite3
        self.change({'literacy_sequence_count':5})
        state=self.store.read('teacher-a','class-a');state['revision']=2
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE snapshots SET payload=?',(json.dumps(state),))
        with self.assertRaises(self.store_module.SettingsError):self.resolve()

    def test_duplicate_scope_field_is_corruption_not_tiebreak(self):
        self.change({'literacy_sequence_count':5})
        state=self.store.read('teacher-a','class-a')
        state['entries'].append(dict(state['entries'][0]))
        with self.assertRaises(self.store_module.SettingsError):
            self.resolver.resolve(state=state,on='2026-09-09')

    def test_concurrent_writers_do_not_lose_updates(self):
        from concurrent.futures import ThreadPoolExecutor
        self.change({'literacy_sequence_count':5})
        def change(value):
            try:
                self.change({'literacy_sequence_count':value},1)
                return 'saved'
            except self.store_module.SettingsError:
                return 'conflict'
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes=list(pool.map(change,[3,7]))
        self.assertEqual(sorted(outcomes),['conflict','saved'])
        self.assertEqual(self.store.read('teacher-a','class-a')['revision'],2)
        self.assertIn(self.resolve()['values']['literacy_sequence_count'],[3,7])

    def test_reset_cannot_resurrect_forgotten_fields(self):
        self.change({'literacy_sequence_count':5})
        self.store.reset('teacher-a','class-a',expected_revision=1,authority=self.authority)
        self.store.undo('teacher-a','class-a',expected_revision=2,authority=self.authority)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],10)

    def test_failed_first_revision_does_not_poison_new_store(self):
        with self.assertRaises(self.store_module.SettingsError):
            self.change({'literacy_sequence_count':5},7)
        self.change({'literacy_sequence_count':5},0)
        self.assertEqual(self.resolve()['values']['literacy_sequence_count'],5)

    def test_history_rejects_row_payload_revision_mismatch(self):
        import sqlite3
        self.change({'literacy_sequence_count':5})
        state=self.store.read('teacher-a','class-a');state['revision']=2
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('UPDATE snapshots SET payload=?',(json.dumps(state),))
        with self.assertRaises(self.store_module.SettingsError):
            self.store.history('teacher-a','class-a')

if __name__ == '__main__': unittest.main()
