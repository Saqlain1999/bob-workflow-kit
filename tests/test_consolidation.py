"""Consolidation tooling checks; never install into a real Bob home."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FINAL_RUNTIME_PROTOCOL_SOURCE = '083ed29533ca292fefa4784efac644f57de9735a'
REVIEWED_RUNTIME_PROTOCOL_PORT = 'e6c39afdc03d4a044788952eaa6b009eadbba393'
FINAL_RUNTIME_PROTOCOL_BLOBS = {
    'evals/qualifications/memory-runtime-trial-v1/README.md':
        '89607b6a2cbe8e2a36decbfdc252a65b39770c29',
    'evals/qualifications/memory-runtime-trial-v1/protocol.json':
        '1703a8b13a77b87c58b1bbcce2ae8204db3a9b5e',
    'evals/results/memory-runtime-trial-template.json':
        '29d653684b67fd59573540300f1265200b123731',
    'evals/scripts/validate_memory_trial.py':
        '1bc67c851c17b18f9ba084f64927b97f60e601bb',
    'evals/tests/test_memory_runtime_protocol.py':
        '66e60c5c1df79b820582fa7b54b29ca15b318d3c',
}


def git_blob_id(data):
    header = ('blob ' + str(len(data)) + '\0').encode('ascii')
    return hashlib.sha1(header + data).hexdigest()


def load(test, name):
    path = ROOT / 'tools' / (name + '.py')
    test.assertTrue(path.is_file(), name + ' is not implemented')
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConsolidationTests(unittest.TestCase):
    def test_open_pr_map_and_active_protocol_use_final_reviewed_source(self):
        mapping = json.loads((ROOT / 'docs/consolidation/open-pr-map.json').read_text(encoding='utf-8'))
        records = [item for item in mapping['pull_requests']
                   if item['repository'] == 'Saqlain1999/bob-workflow-evals'
                   and item['number'] == 14]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['headRefOid'], FINAL_RUNTIME_PROTOCOL_SOURCE)
        protocol = json.loads((ROOT / 'evals/qualifications/memory-runtime-trial-v1/protocol.json')
                              .read_text(encoding='utf-8'))
        self.assertEqual(protocol['schema_version'], 2)
        self.assertIn('shell_non_interactive', protocol['allowed_client_modes'])
        manifest = json.loads((ROOT / 'docs/consolidation/reviewed-evals-fork.json')
                              .read_text(encoding='utf-8'))
        self.assertEqual(manifest['reviewed_commit'], REVIEWED_RUNTIME_PROTOCOL_PORT)
        self.assertEqual(manifest['runtime_protocol_source'], FINAL_RUNTIME_PROTOCOL_SOURCE)
        for path, expected_blob in FINAL_RUNTIME_PROTOCOL_BLOBS.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob_id((ROOT / path).read_bytes()), expected_blob)

    @unittest.skipUnless(shutil.which('git') and (ROOT / '.git').exists(),
                         'Full Git checkout required for reviewed PR ancestry')
    def test_native_pr_heads_and_reviewed_runtime_port_are_ancestors(self):
        mapping = json.loads((ROOT / 'docs/consolidation/open-pr-map.json').read_text(encoding='utf-8'))
        expected_ancestors = [item for item in mapping['pull_requests']
                              if item['headRefOid'] != FINAL_RUNTIME_PROTOCOL_SOURCE]
        expected_ancestors.append({'repository': 'Saqlain1999/bob-workflow-kit',
                                   'number': 'reviewed-runtime-port',
                                   'headRefOid': REVIEWED_RUNTIME_PROTOCOL_PORT})
        for item in expected_ancestors:
            with self.subTest(repository=item['repository'], number=item['number']):
                result = subprocess.run(
                    ['git', '--no-replace-objects', 'merge-base', '--is-ancestor',
                     item['headRefOid'], 'HEAD'],
                    cwd=ROOT, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)

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
        self.assertEqual(checks[1]['command'][-1], 'evaluator')
        self.assertEqual(Path(checks[1]['command'][-2]), ROOT / 'tools/run_component_tests.py')
        self.assertEqual(checks[0]['command'][-1], 'installer')
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
