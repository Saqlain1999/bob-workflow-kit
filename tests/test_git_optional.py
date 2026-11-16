"""The Python-only ZIP journey must not require a Git executable."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OptionalGitTests(unittest.TestCase):
    def test_git_object_store_cases_explicitly_skip_without_git(self):
        probe = """
import io, json, shutil, sys, unittest
sys.path.insert(0, 'tests')
import test_provenance_gate
suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_provenance_gate.ProvenanceTests)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(json.dumps({'git_found': bool(shutil.which('git')), 'tests_run': result.testsRun,
                  'skipped': len(result.skipped), 'errors': len(result.errors),
                  'failures': len(result.failures)}))
sys.exit(0 if result.wasSuccessful() else 1)
"""
        with tempfile.TemporaryDirectory() as empty_path:
            env = {key: os.environ[key] for key in
                   ('HOME', 'TMPDIR', 'LANG', 'SYSTEMROOT', 'WINDIR') if key in os.environ}
            env['PATH'] = empty_path
            completed = subprocess.run([sys.executable, '-B', '-c', probe], cwd=ROOT,
                                       env=env, capture_output=True, text=True, timeout=30)
        report = json.loads(completed.stdout)
        self.assertFalse(report['git_found'])
        self.assertEqual(completed.returncode, 0, report)
        self.assertGreater(report['tests_run'], 0)
        self.assertEqual(report['skipped'], report['tests_run'])
        self.assertEqual(report['errors'], 0)
        self.assertEqual(report['failures'], 0)
