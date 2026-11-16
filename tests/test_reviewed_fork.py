"""Keep reviewed active forks distinct from immutable original-source provenance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('fork_verifier', ROOT / 'tools/verify_consolidation.py')
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


@unittest.skipUnless(shutil.which('git'), 'Git required for original-object controls')
class ReviewedForkTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'evals').mkdir()
        (self.root / 'evals/example.py').write_bytes(b'print("fixture")\n')
        self.git('init', '-q')
        self.git('add', 'evals')
        self.commit()
        commit = self.git('rev-parse', 'HEAD').strip()
        blob = self.git('rev-parse', 'HEAD:evals/example.py').strip()
        self.doc = {'prefix': 'evals', 'reviewed_commit': commit, 'files': [
            {'destination': 'evals/example.py', 'git_blob': blob, 'mode': '100644',
             'sha256': hashlib.sha256((self.root / 'evals/example.py').read_bytes()).hexdigest()}]}
        self.map = self.root / 'docs/consolidation/reviewed-evals-fork.json'
        self.map.parent.mkdir(parents=True)
        raw = (json.dumps(self.doc, indent=2) + '\n').encode()
        self.map.write_bytes(raw)
        patcher = mock.patch.object(VERIFIER, 'REVIEWED_FORK_DIGEST',
                                    hashlib.sha256(raw).hexdigest(), create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL)

    def commit(self):
        self.git('-c', 'user.name=Fork Probe', '-c', 'user.email=probe@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')

    def check(self):
        self.assertTrue(hasattr(VERIFIER, 'verify_reviewed_fork'))
        return VERIFIER.verify_reviewed_fork(self.root)

    def test_exact_recorded_fork_passes(self):
        errors, report = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(report['reviewed_files'], 1)

    def test_mutated_manifest_cannot_bless_changed_destination(self):
        path = self.root / 'evals/example.py'
        path.write_bytes(b'changed')
        self.doc['files'][0]['sha256'] = hashlib.sha256(b'changed').hexdigest()
        self.map.write_text(json.dumps(self.doc), encoding='utf-8')
        self.assertTrue(self.check()[0])

    def test_unrecorded_worktree_change_is_rejected(self):
        (self.root / 'evals/example.py').write_bytes(b'changed')
        self.assertTrue(self.check()[0])

    def test_extra_committed_source_file_is_rejected(self):
        (self.root / 'evals/extra.py').write_bytes(b'pass\n')
        self.git('add', 'evals')
        self.commit()
        self.assertTrue(self.check()[0])

    def test_zip_mode_checks_content_without_claiming_git_proof(self):
        with mock.patch.object(VERIFIER, 'git', side_effect=FileNotFoundError('git')):
            errors, report = self.check()
        self.assertEqual(errors, [])
        self.assertIn('unverified', report['history'])


if __name__ == '__main__':
    unittest.main()
