"""Archive identity must be checked before extraction, not just after rebuilding."""
import hashlib
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import warnings
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

class PackageIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT/'scripts/verify_package_archive.py').is_file(),'Archive verifier missing')
        self.module=importlib.import_module('verify_package_archive')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.package=self.root/'package.zip'
        self.entries={'SKILL.md':b'---\nname: test-skill\n---\n','VERSION':b'candidate\n'}

    def build(self,*,duplicates=False,extra=None,alter_manifest=None):
        manifest={'version':'candidate','source_commit':'a'*40,'files':[
            dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()) for name,data in self.entries.items()]}
        if alter_manifest:alter_manifest(manifest)
        with zipfile.ZipFile(self.package,'w') as archive,warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            for name,data in self.entries.items():archive.writestr('test-skill/'+name,data)
            archive.writestr('test-skill/PACKAGE-MANIFEST.json',json.dumps(manifest))
            if duplicates:archive.writestr('test-skill/SKILL.md',b'changed')
            if extra:
                for name,data in extra:archive.writestr(name,data)
        return hashlib.sha256(self.package.read_bytes()).hexdigest()

    def test_valid_package_is_an_integrity_pass_not_release(self):
        digest=self.build()
        report=self.module.verify_archive(self.package,expected_sha256=digest,expected_source_commit='a'*40)
        self.assertEqual(report['status'],'PASS')
        self.assertIs(report['release_authorised'],False)

    def test_wrong_digest_blocks_before_extraction(self):
        self.build();destination=self.root/'install'
        with self.assertRaises(ValueError):self.module.extract_verified(self.package,destination,expected_sha256='0'*64)
        self.assertFalse(destination.exists())

    def test_wrong_source_identity_fails(self):
        digest=self.build()
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest,expected_source_commit='b'*40)

    def test_duplicate_archive_member_fails(self):
        digest=self.build(duplicates=True)
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest)

    def test_unsafe_and_case_colliding_paths_fail(self):
        for path in ('../outside','/absolute','test-skill/../outside','test-skill/CON','test-skill/SKILL.MD','test-skill/a\\b'):
            with self.subTest(path=path):
                digest=self.build(extra=[(path,b'data')])
                with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest)

    def test_duplicate_manifest_member_fails(self):
        digest=self.build(alter_manifest=lambda m:m['files'].append(m['files'][0]))
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest)

    def test_changed_contents_do_not_pass_declared_hash(self):
        digest=self.build(alter_manifest=lambda m:m['files'][0].update(sha256='0'*64))
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest)

    def test_undeclared_file_fails(self):
        digest=self.build(extra=[('test-skill/private.sqlite',b'secret')])
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=digest)

    def test_symlink_archive_entry_fails(self):
        digest=self.build()
        info=zipfile.ZipInfo('test-skill/link');info.create_system=3;info.external_attr=(0o120777<<16)
        with zipfile.ZipFile(self.package,'a') as archive:archive.writestr(info,'outside')
        with self.assertRaises(ValueError):self.module.verify_archive(self.package,expected_sha256=hashlib.sha256(self.package.read_bytes()).hexdigest())

    def test_existing_install_is_not_overwritten(self):
        digest=self.build();destination=self.root/'install';destination.mkdir();(destination/'keep').write_text('existing')
        with self.assertRaises((ValueError,FileExistsError)):
            self.module.extract_verified(self.package,destination,expected_sha256=digest)
        self.assertEqual((destination/'keep').read_text(),'existing')

    def test_valid_extract_preserves_exact_bytes(self):
        digest=self.build();destination=self.root/'install'
        self.module.extract_verified(self.package,destination,expected_sha256=digest)
        for name,data in self.entries.items():self.assertEqual((destination/'test-skill'/name).read_bytes(),data)

if __name__=='__main__':unittest.main()

class BuiltPackageIdentityTests(unittest.TestCase):
    def test_all_generated_packages_have_validatable_manifests(self):
        import subprocess
        from verify_package_archive import verify_archive
        with tempfile.TemporaryDirectory() as tmp:
            for script,output in [('build_chatgpt_package.py',str(Path(tmp)/'complete.zip')),
                                  ('package_component_skills.py',str(Path(tmp)/'components'))]:
                run=subprocess.run([sys.executable,str(ROOT/'scripts'/script),'--out',output],capture_output=True,text=True,timeout=30)
                self.assertEqual(run.returncode,0,run.stderr)
            packages=[Path(tmp)/'complete.zip',*sorted((Path(tmp)/'components').glob('dlp-*.zip'))]
            self.assertEqual(len(packages),9)
            for package in packages:
                with self.subTest(package=package.name):
                    report=verify_archive(package,expected_sha256=hashlib.sha256(package.read_bytes()).hexdigest())
                    self.assertEqual(report['status'],'PASS')

    def test_changed_install_is_not_executed_by_dependency_audit(self):
        from build_chatgpt_package import build_file_map,manifest
        from unittest.mock import patch
        from contextlib import redirect_stdout
        import audit_package_dependencies as audit
        version,files=build_file_map(ROOT);files['PACKAGE-MANIFEST.json']=manifest(version,files)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for relative,data in files.items():
                p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            (root/'scripts/agent_orchestrator.py').write_text('raise Exception("MUST NOT RUN")')
            with patch.object(sys,'argv',['audit','--skill-root',tmp]),patch.object(audit.subprocess,'run',return_value=type('Result',(),{'returncode':0,'stderr':''})()) as run,redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(),1)
                run.assert_not_called()

    def test_component_manifest_tampering_is_rejected_by_direct_audit(self):
        import subprocess
        import audit_package_dependencies as audit
        from unittest.mock import patch
        from contextlib import redirect_stdout
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            subprocess.run([sys.executable, str(ROOT/'scripts/package_component_skills.py'), '--out', str(path/'packages')], check=True, capture_output=True)
            with zipfile.ZipFile(path/'packages/dlp-morning-work.zip') as archive:
                archive.extractall(path/'installed')
            skill = path/'installed/dlp-morning-work'
            (skill/'scripts/teacher_context_store.py').write_text('# altered after build\n')
            with patch.object(sys, 'argv', ['audit', '--skill-root', str(skill), '--component']), redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(), 1)
