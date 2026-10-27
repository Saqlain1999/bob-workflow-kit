"""Exercise component gates on disposable suites, never recursively check all."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('quality_check_all', ROOT / 'tools/check_all.py')
assert spec is not None and spec.loader is not None
check_all = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_all)

PASSING = 'import unittest\nclass Example(unittest.TestCase):\n    def test_ok(self):\n        pass\n'


class QualityGateTests(unittest.TestCase):
    def run_fixture(self, component, files):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'tests').mkdir()
            for name, content in files.items():
                (root / 'tests' / name).write_text(content, encoding='utf-8')
            check = next(c for c in check_all.checks(ROOT) if c['name'] == component)
            report = root / 'evidence.json'
            result = subprocess.run(check['command'] + ['--report', str(report)],
                                    cwd=root, env=check_all.test_environment({}),
                                    capture_output=True, text=True, timeout=20)
            evidence = json.loads(report.read_text(encoding='utf-8'))
            return result, evidence

    def test_mandatory_suites_have_real_counts(self):
        for component, names in [('installer', ('test_installer', 'test_consolidation')),
                                 ('evaluator', ('test_evaluate', 'test_parcel_resume'))]:
            with self.subTest(component=component):
                result, evidence = self.run_fixture(component, {
                    name + '.py': PASSING for name in names})
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(evidence['all_successful'])
                self.assertGreater(evidence['tests_run'], 0)
                self.assertEqual(evidence['tests_discovered'], evidence['tests_run'])
                for name in names:
                    self.assertGreater(evidence['required_modules'][name], 0)

    def test_each_required_module_must_exist_and_contain_tests(self):
        for component, names in [('installer', ('test_installer', 'test_consolidation')),
                                 ('evaluator', ('test_evaluate', 'test_parcel_resume'))]:
            for missing in names:
                for replacement in (None, '# empty module\n'):
                    with self.subTest(component=component, missing=missing, empty=replacement):
                        files = {name + '.py': PASSING for name in names if name != missing}
                        if replacement is not None:
                            files[missing + '.py'] = replacement
                        result, evidence = self.run_fixture(component, files)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertFalse(evidence['all_successful'])
                        self.assertEqual(evidence['required_modules'][missing], 0)

    def test_discovery_keeps_component_root_importable(self):
        result, evidence = self.run_fixture('installer', {
            '../component_support.py': 'VALUE = 1\n',
            'test_installer.py': 'import component_support\n' + PASSING,
            'test_consolidation.py': PASSING})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertGreater(evidence['tests_run'], 0)

    def test_zero_discovery_fails(self):
        result, evidence = self.run_fixture('installer', {})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(evidence['tests_discovered'], 0)
        self.assertFalse(evidence['all_successful'])

    def test_child_test_failures_and_import_errors_propagate(self):
        for broken in (PASSING.replace('pass', 'self.fail("deliberate")'),
                       PASSING.replace('pass', 'raise RuntimeError("deliberate")'),
                       'raise ImportError("deliberate")\n', 'not valid python!\n'):
            with self.subTest(broken=broken):
                result, evidence = self.run_fixture('installer', {
                    'test_installer.py': PASSING, 'test_consolidation.py': PASSING,
                    'test_extra.py': broken})
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(evidence['all_successful'])

    def test_extra_discovered_tests_are_run_and_counted(self):
        result, evidence = self.run_fixture('installer', {
            'test_installer.py': PASSING, 'test_consolidation.py': PASSING,
            'test_extra.py': PASSING})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(evidence['tests_run'], 3)  # This fixture only, not a repository total.

    def test_cli_contract_and_environment_allowlist(self):
        checks = check_all.checks(ROOT, require_history=True)
        self.assertIn('--require-history', checks[3]['command'])
        env = check_all.test_environment({'PATH': 'example', 'TMPDIR': 'scratch',
                                          'SECRET_TOKEN': 'synthetic',
                                          'OPENAI_API_KEY': 'synthetic'})
        self.assertNotIn('SECRET_TOKEN', env)
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertEqual(env['TMPDIR'], 'scratch')
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/check_all.py'),
                                 '--list', '--require-history'], capture_output=True,
                                text=True, env=check_all.test_environment({}), timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 5)

    def test_missing_installer_cannot_pass_on_consolidation_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'tests').mkdir()
            (root / 'tests/test_consolidation.py').write_text(PASSING, encoding='utf-8')
            check = check_all.checks(ROOT)[0]
            result = subprocess.run(check['command'], cwd=root,
                                    env=check_all.test_environment({}),
                                    capture_output=True, text=True, timeout=20)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
