"""Run calibration from extracted packages with no checkout import fallback."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_chatgpt_package import build_file_map

class InstallationCalibrationTests(unittest.TestCase):
    def test_complete_package_contains_runtime_dependencies(self):
        _,files=build_file_map(ROOT)
        for name in ('config/creator-defaults.json','scripts/teacher_context_store.py',
                     'scripts/resolve_instructional_calibration.py','schemas/instructional-calibration.schema.json'):
            self.assertIn(name,files, name+' missing from install package')

    def test_extracted_complete_package_resolves_defaults_in_isolation(self):
        _,files=build_file_map(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'installed';dest.mkdir()
            for relative,data in files.items():
                path=dest/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
            script="import sys,json;sys.path.insert(0,sys.argv[1]);from resolve_instructional_calibration import resolve;print(json.dumps(resolve(on='2026-09-09')['values']))"
            run=subprocess.run([sys.executable,'-I','-B','-c',script,str(dest/'scripts')],cwd=tmp,capture_output=True,text=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(json.loads(run.stdout)['main_curriculum_year'],5)

    def test_each_standalone_component_has_calibration_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            run=subprocess.run([sys.executable,str(ROOT/'scripts/package_component_skills.py'),'--out',tmp],capture_output=True,text=True,timeout=30)
            self.assertEqual(run.returncode,0,run.stderr)
            for package in Path(tmp).glob('dlp-*.zip'):
                with self.subTest(component=package.stem),zipfile.ZipFile(package) as archive:
                    names=set(archive.namelist())
                    for rel in ('config/creator-defaults.json','schemas/instructional-calibration.schema.json'):
                        self.assertIn(package.stem+'/'+rel,names)

if __name__=='__main__': unittest.main()
