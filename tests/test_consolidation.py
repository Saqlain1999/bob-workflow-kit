"""Consolidation tooling checks; never install into a real Bob home."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(test, name):
    path = ROOT / 'tools' / (name + '.py')
    test.assertTrue(path.is_file(), name + ' is not implemented')
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConsolidationTests(unittest.TestCase):
    def test_imported_files_are_checked_by_content_not_a_success_marker(self):
        module = load(self, 'verify_consolidation')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'source.txt').write_bytes(b'original')
            manifest = {'sources': [{'files': [{'destination': 'source.txt',
                         'sha256': hashlib.sha256(b'original').hexdigest()}]}]}
            self.assertEqual(module.verify_files(root, manifest), [])
            (root / 'source.txt').write_bytes(b'changed')
            self.assertTrue(module.verify_files(root, manifest))

    def test_import_manifest_cannot_read_outside_the_checkout(self):
        module = load(self, 'verify_consolidation')
        with tempfile.TemporaryDirectory() as tmp:
            for name in ['../outside', '/absolute', 'evals/../../outside']:
                manifest = {'sources': [{'files': [{'destination': name, 'sha256': '0' * 64}]}]}
                self.assertTrue(module.verify_files(Path(tmp), manifest))

    def test_combined_check_lists_real_component_commands(self):
        module = load(self, 'check_all')
        checks = module.checks(ROOT, require_history=False)
        self.assertEqual([check['name'] for check in checks],
                         ['installer', 'evaluator', 'catalogue', 'provenance', 'links'])
        self.assertEqual(checks[1]['cwd'], ROOT / 'evals')
        self.assertIn('unittest', checks[1]['command'])
        self.assertEqual(checks[2]['cwd'], ROOT / 'docs/resources/catalogue')
        self.assertTrue(all(check['command'][0] == sys.executable for check in checks))

    def test_component_environment_does_not_propagate_provider_credentials(self):
        module = load(self, 'check_all')
        env = module.test_environment({'PATH': '/bin', 'HOME': '/home/test',
                                      'BOB_API_KEY': 'synthetic', 'VAULT_TOKEN': 'synthetic',
                                      'OPENAI_API_KEY': 'synthetic', 'TMPDIR': '/scratch'})
        self.assertNotIn('BOB_API_KEY', env)
        self.assertNotIn('VAULT_TOKEN', env)
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertEqual(env['TMPDIR'], '/scratch')
        self.assertEqual(env['PYTHONDONTWRITEBYTECODE'], '1')

    def test_list_mode_does_not_run_component_suites(self):
        load(self, 'check_all')
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/check_all.py'), '--list'],
                                cwd=ROOT, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 5)


if __name__ == '__main__':
    unittest.main()
