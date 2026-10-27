"""Offline provenance regressions using actual, disposable Git object stores."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('provenance_verifier', ROOT / 'tools/verify_consolidation.py')
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Offline Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.autocrlf', 'false')
        for name, data in [('first.txt', b'original\r\n'), ('nested/second.txt', b'second\n')]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.git('add', '.')
        self.git('commit', '-qm', 'Original source')
        commit = self.git('rev-parse', 'HEAD').strip()
        files = []
        for record in self.git('ls-tree', '-r', 'HEAD').splitlines():
            meta, name = record.split('\t')
            mode, _, blob = meta.split()
            data = (self.root / name).read_bytes()
            destination = self.root / 'imported' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            files.append({'source_path': name, 'destination': 'imported/' + name,
                          'sha256': hashlib.sha256(data).hexdigest(),
                          'git_blob': blob, 'source_mode': mode})
        self.manifest = {'schema_version': 1, 'kit_base': commit,
                         'sources': [{'repository': 'fixture/source', 'source_commit': commit,
                                      'prefix': 'imported', 'files': files}]}
        # Fixture trust anchors are captured before any test mutates the manifest.
        anchor = mock.patch.object(VERIFIER, 'SOURCE_ANCHORS',
                                   {'fixture/source': (commit, 'imported')}, create=True)
        anchor.start()
        self.addCleanup(anchor.stop)
        base = mock.patch.object(VERIFIER, 'KIT_BASE_ANCHOR', commit, create=True)
        base.start()
        self.addCleanup(base.stop)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout

    def errors(self, manifest=None, required=True):
        return VERIFIER.verify_history(self.root, manifest or self.manifest, required)[0]

    def test_omitting_a_whole_source_is_not_valid_provenance(self):
        second = copy.deepcopy(self.manifest['sources'][0])
        second.update(repository='fixture/second', prefix='second-import')
        for entry in second['files']:
            entry['destination'] = 'second-import/' + entry['source_path']
        complete = copy.deepcopy(self.manifest)
        complete['sources'].append(second)
        anchors = dict(VERIFIER.SOURCE_ANCHORS)
        anchors['fixture/second'] = (second['source_commit'], second['prefix'])
        with mock.patch.object(VERIFIER, 'SOURCE_ANCHORS', anchors):
            self.assertEqual(self.errors(complete), [])
            self.assertTrue(self.errors(self.manifest))

    def test_substituting_a_complete_ancestor_source_is_rejected(self):
        substituted = copy.deepcopy(self.manifest)
        source = substituted['sources'][0]
        source.update(repository='fixture/not-an-original-import', prefix='regenerated')
        for entry in source['files']:
            entry['destination'] = 'regenerated/' + entry['source_path']
            path = self.root / entry['destination']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((self.root / entry['source_path']).read_bytes())
        self.assertEqual(VERIFIER.verify_files(self.root, substituted), [])
        self.assertTrue(self.errors(substituted))

    def test_source_prefix_relocation_cannot_redefine_import_identity(self):
        altered = copy.deepcopy(self.manifest)
        source = altered['sources'][0]
        source['prefix'] = 'elsewhere'
        for entry in source['files']:
            entry['destination'] = 'elsewhere/' + entry['source_path']
        self.assertTrue(self.errors(altered))

    def test_complete_original_inventory_passes(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(VERIFIER.verify_files(self.root, self.manifest), [])

    def test_empty_and_truncated_inventories_fail(self):
        for inventory in [[], self.manifest['sources'][0]['files'][:1]]:
            manifest = copy.deepcopy(self.manifest)
            manifest['sources'][0]['files'] = inventory
            self.assertTrue(self.errors(manifest))

    def test_rehashed_modified_destination_cannot_redefine_original(self):
        entry = self.manifest['sources'][0]['files'][0]
        (self.root / entry['destination']).write_bytes(b'forged')
        entry['sha256'] = hashlib.sha256(b'forged').hexdigest()
        self.assertEqual(VERIFIER.verify_files(self.root, self.manifest), [])
        self.assertTrue(self.errors())

    def test_wrong_blob_mode_prefix_and_destination_fail(self):
        for field, value in [('git_blob', '0' * 40), ('source_mode', '100755'),
                             ('destination', 'elsewhere/first.txt')]:
            manifest = copy.deepcopy(self.manifest)
            manifest['sources'][0]['files'][0][field] = value
            with self.subTest(field=field):
                self.assertTrue(self.errors(manifest))
        manifest = copy.deepcopy(self.manifest)
        manifest['sources'][0]['prefix'] = 'elsewhere'
        self.assertTrue(self.errors(manifest))

    def test_duplicate_source_paths_and_destinations_fail(self):
        manifest = copy.deepcopy(self.manifest)
        manifest['sources'][0]['files'].append(copy.deepcopy(manifest['sources'][0]['files'][0]))
        errors = self.errors(manifest)
        self.assertTrue(any('duplicate source path' in error for error in errors))
        self.assertTrue(any('Duplicate destination' in error for error in errors))
        manifest = copy.deepcopy(self.manifest)
        manifest['sources'].append(copy.deepcopy(manifest['sources'][0]))
        self.assertTrue(self.errors(manifest))

    def test_unsafe_or_noncanonical_paths_fail(self):
        for value in ['', '/absolute', '../escape', 'a/../b', './a', 'a//b', 'a\\b', 'a/', 'a\x00b']:
            for field in ['prefix', 'source_path', 'destination']:
                manifest = copy.deepcopy(self.manifest)
                target = manifest['sources'][0] if field == 'prefix' else manifest['sources'][0]['files'][0]
                target[field] = value
                with self.subTest(field=field, value=value):
                    self.assertTrue(self.errors(manifest))

    def test_malformed_schema_fails_without_raising(self):
        for manifest in [None, [], {}, {'sources': []},
                         dict(self.manifest, sources=[None]),
                         dict(self.manifest, kit_base='bad')]:
            with self.subTest(manifest=manifest):
                errors, _ = VERIFIER.verify_history(self.root, manifest, True)
                self.assertTrue(errors)
        for field, value in [('files', None), ('files', [None]), ('repository', ''),
                             ('source_commit', None), ('prefix', 42)]:
            manifest = copy.deepcopy(self.manifest)
            manifest['sources'][0][field] = value
            self.assertTrue(self.errors(manifest))

    def test_extra_inventory_entry_fails(self):
        entry = copy.deepcopy(self.manifest['sources'][0]['files'][0])
        entry.update(source_path='extra.txt', destination='imported/extra.txt')
        self.manifest['sources'][0]['files'].append(entry)
        self.assertTrue(self.errors())

    def test_actual_archive_checks_only_bundled_manifest(self):
        archive = self.root / 'archive'
        archive.mkdir()
        errors, status = VERIFIER.verify_history(archive, self.manifest, False)
        self.assertEqual(errors, [])
        self.assertIn('bundled manifest only', status)
        self.assertTrue(VERIFIER.verify_history(archive, self.manifest, True)[0])

    def test_git_blob_read_failure_is_not_success(self):
        original = VERIFIER.subprocess.run

        def fail_blob(command, **kwargs):
            if 'cat-file' in command:
                raise subprocess.CalledProcessError(128, command)
            return original(command, **kwargs)

        with mock.patch.object(VERIFIER.subprocess, 'run', side_effect=fail_blob):
            self.assertTrue(self.errors(required=False))

    def test_source_and_kit_ancestry_are_required(self):
        unrelated = self.git('commit-tree', self.git('rev-parse', 'HEAD^{tree}').strip(),
                             '-m', 'Unrelated root').strip()
        for target in ['kit_base', 'source_commit']:
            manifest = copy.deepcopy(self.manifest)
            if target == 'kit_base':
                manifest[target] = unrelated
            else:
                manifest['sources'][0][target] = unrelated
            self.assertTrue(self.errors(manifest))

    def test_archive_fallback_is_explicit_and_require_history_fails(self):
        with mock.patch.object(VERIFIER.subprocess, 'run', side_effect=FileNotFoundError('git')):
            errors, status = VERIFIER.verify_history(self.root, self.manifest, False)
            self.assertEqual(errors, [])
            self.assertIn('bundled manifest only', status)
            self.assertTrue(self.errors(required=True))
            manifest = copy.deepcopy(self.manifest)
            manifest['sources'][0]['files'] = []
            self.assertTrue(self.errors(manifest, required=False))

    def test_git_inventory_failure_is_not_archive_success(self):
        original = VERIFIER.subprocess.run

        def fail_tree(command, **kwargs):
            if 'ls-tree' in command:
                raise subprocess.CalledProcessError(128, command)
            return original(command, **kwargs)

        with mock.patch.object(VERIFIER.subprocess, 'run', side_effect=fail_tree):
            self.assertTrue(self.errors(required=False))

    def test_cli_binds_history_before_destination_check(self):
        entry = self.manifest['sources'][0]['files'][0]
        (self.root / entry['destination']).write_bytes(b'forged')
        entry['sha256'] = hashlib.sha256(b'forged').hexdigest()
        manifest_path = self.root / 'docs/consolidation/source-map.json'
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(json.dumps(self.manifest), encoding='utf-8')
        with mock.patch.object(VERIFIER, 'ROOT', self.root), \
                mock.patch.object(sys, 'argv', ['verify_consolidation', '--require-history']), \
                mock.patch('builtins.print') as output:
            self.assertEqual(VERIFIER.main(), 1)
        self.assertTrue(json.loads(output.call_args[0][0])['errors'])


if __name__ == '__main__':
    unittest.main()
