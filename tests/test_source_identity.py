import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

class SourceIdentityTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT/'scripts/package_identity.py').is_file(),'Source identity helper is missing')
        self.mod=importlib.import_module('package_identity')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.git('init','-q');self.git('config','user.name','Synthetic test');self.git('config','user.email','test@example.invalid')
        (self.root/'code.txt').write_text('source');self.git('add','code.txt');self.git('commit','-qm','Synthetic source fixture')
    def git(self,*args):
        return subprocess.run(['git','-C',str(self.root),*args],check=True,capture_output=True,text=True).stdout.strip()
    def test_clean_source_is_identified(self):
        self.assertEqual(self.mod.source_revision(self.root),self.git('rev-parse','HEAD'))
    def test_dirty_source_never_claims_a_clean_commit(self):
        (self.root/'code.txt').write_text('modified')
        self.assertIsNone(self.mod.source_revision(self.root))
    def test_nested_directory_does_not_inherit_parent_commit(self):
        child=self.root/'nested';child.mkdir()
        self.assertIsNone(self.mod.source_revision(child))
    def test_new_untracked_source_invalidates_identity(self):
        (self.root/'new.py').write_text('pass')
        self.assertIsNone(self.mod.source_revision(self.root))

if __name__=='__main__':unittest.main()
