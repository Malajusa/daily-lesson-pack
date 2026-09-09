"""Only the supported explicit count grammar is automatic; ambiguous text is not saved."""
import importlib
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

class ConversationalOverrideTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT/'scripts/resolve_overrides.py').is_file(),'Conversational scope resolver missing')
        self.mod=importlib.import_module('resolve_overrides')
    def parse(self,text,**kwargs):
        return self.mod.propose_override(text,field='literacy_sequence_count',today='2026-09-09',**kwargs)
    def test_clear_standing_request(self):
        result=self.parse('Five from now on')
        self.assertEqual(result['scope'],{'kind':'standing'})
        self.assertEqual(result['values'],{'literacy_sequence_count':5})
    def test_tomorrow_is_local_calendar_date(self):
        self.assertEqual(self.parse('three tomorrow')['scope'],{'kind':'date','start':'2026-09-10','end':'2026-09-10'})
    def test_unit_request_requires_a_real_unit_identifier(self):
        self.assertEqual(self.parse('five for this unit')['status'],'NEEDS_CLARIFICATION')
        self.assertEqual(self.parse('five for this unit',unit_id='narrative')['scope'],{'kind':'unit','id':'narrative'})
    def test_lesson_request_requires_an_identifier(self):
        self.assertEqual(self.parse('three for this lesson',lesson_id='writing-1')['scope'],{'kind':'lesson','id':'writing-1'})
    def test_unspecified_scope_does_not_become_standing(self):
        self.assertEqual(self.parse('five')['status'],'NEEDS_CLARIFICATION')
    def test_unrelated_text_is_not_a_settings_command(self):
        self.assertEqual(self.parse('Create five questions about conjunctions')['status'],'NEEDS_CLARIFICATION')
    def test_explicit_dated_override(self):
        self.assertEqual(self.parse('use 4 on 2026-10-01')['scope']['start'],'2026-10-01')
    def test_unsafe_scope_or_invalid_count_is_not_proposed(self):
        for text in ('zero from now on','100 tomorrow','three for the class I mentioned'):
            self.assertEqual(self.parse(text)['status'],'NEEDS_CLARIFICATION')
    def test_apply_needs_actual_teacher_authority(self):
        from teacher_context_store import SettingsStore,SettingsError
        with tempfile.TemporaryDirectory() as tmp:
            store=SettingsStore(Path(tmp)/'settings.sqlite')
            with self.assertRaises(SettingsError):
                self.mod.apply_override(self.parse('five from now on'),store=store,teacher='t',classroom='c',
                    expected_revision=0,authority={'kind':'source_document','source_id':'attached-source'})
            self.assertFalse(store.path.exists())
            result=self.mod.apply_override(self.parse('five from now on'),store=store,teacher='t',classroom='c',
                    expected_revision=0,authority={'kind':'teacher_request','source_id':'actual-request'})
            self.assertEqual(result['revision'],1)

if __name__=='__main__':unittest.main()
