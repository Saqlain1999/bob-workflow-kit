"""Offline safety tests; every writable Bob root is an explicit temporary path."""

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import runpy
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tools import bob_workflow as kit


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "tools" / "bob_workflow.py"


def snapshot(root):
    """Capture contents and mtimes; reads may update atime, which is excluded."""
    if not root.exists():
        return None
    result = {}
    for path in [root, *sorted(root.rglob("*"))]:
        info = path.lstat()
        value = os.readlink(path) if path.is_symlink() else (path.read_bytes() if path.is_file() else None)
        result[path.relative_to(root).as_posix()] = (info.st_mode, info.st_mtime_ns, value)
    return result


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="bob-workflow-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "bob"
        self.payload = self.base / "payload"
        self.files = {
            kit.RULE: b"# Local coding workflow\nKeep evidence with each change.\n",
            kit.SKILL: b"---\nname: work-large-codebase\ndescription: Work in bounded steps with evidence.\n---\nRead the project before editing.\n",
            "skills/work-large-codebase/references/change.md": b"Run the repository's documented checks.\n",
            "skills/work-large-codebase/templates/checkpoint.md": b"# Checkpoint\nRevision and scope:\n",
        }
        for relative, data in self.files.items():
            path = self.payload / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def write_unrelated(self):
        paths = {
            "settings.json": b'{"private":"unchanged"}\n',
            "AGENTS.md": b"Existing user instructions.\n",
            "rules/my-rule.md": b"Existing rule.\n",
            "skills/my-skill/SKILL.md": b"Existing skill.\n",
            "hooks.json": b'{"hooks":{}}\n',
            "workflow-kit/user-note.txt": b"Do not remove.\n",
        }
        for value, data in paths.items():
            path = self.root / value
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return paths

    def cli(self, command):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), command, "--bob-home", str(self.root)],
            cwd=self.base, text=True, capture_output=True, timeout=15, check=False,
        )

    def assert_error(self, code, function, *args):
        with self.assertRaises(kit.KitError) as caught:
            function(*args)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def test_import_and_help_do_not_resolve_home_or_write_target(self):
        with mock.patch.object(Path, "home", side_effect=AssertionError("Home must not be resolved")):
            runpy.run_path(str(SCRIPT), run_name="installer_import_test")
            with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as caught:
                kit.main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        self.assertFalse(self.root.exists())

    def test_preview_and_doctor_leave_absent_root_absent(self):
        with mock.patch.object(Path, "home", side_effect=AssertionError("Explicit root required")):
            self.assertEqual(kit.preview(self.root, self.payload)["status"], "ready")
            self.assertEqual(kit.doctor(self.root, self.payload)["status"], "not_installed")
        self.assertFalse(self.root.exists())

    def test_read_only_commands_preserve_existing_tree_bytes_and_mtimes(self):
        self.write_unrelated()
        kit.install(self.root, self.payload)
        before = snapshot(self.root)
        self.assertTrue(kit.preview(self.root, self.payload)["files_valid"])
        diagnosis = kit.doctor(self.root, self.payload)
        self.assertTrue(diagnosis["files_valid"])
        self.assertTrue(diagnosis["client_loading_not_tested"])
        self.assertEqual(snapshot(self.root), before)

    def test_round_trip_preserves_unrelated_bytes_and_shared_directories(self):
        unrelated = self.write_unrelated()
        original_mtimes = {name: (self.root / name).stat().st_mtime_ns for name in unrelated}
        result = kit.install(self.root, self.payload)
        self.assertEqual(result["status"], "installed")
        for name, data in self.files.items():
            self.assertEqual((self.root / name).read_bytes(), data)
        self.assertFalse((self.root / kit.JOURNAL).exists())
        self.assertTrue(kit.doctor(self.root, self.payload)["ok"])
        self.assertEqual(kit.uninstall(self.root)["status"], "uninstalled")
        for name, data in unrelated.items():
            self.assertEqual((self.root / name).read_bytes(), data)
            self.assertEqual((self.root / name).stat().st_mtime_ns, original_mtimes[name])
        self.assertFalse((self.root / "skills/work-large-codebase").exists())
        self.assertTrue((self.root / "rules").is_dir())
        self.assertTrue((self.root / "workflow-kit").is_dir())

    def test_reinstall_is_byte_and_mtime_identical_no_op(self):
        kit.install(self.root, self.payload)
        before = snapshot(self.root)
        self.assertEqual(kit.install(self.root, self.payload)["status"], "unchanged")
        self.assertEqual(snapshot(self.root), before)

    def test_uninstall_twice_is_safe(self):
        kit.install(self.root, self.payload)
        kit.uninstall(self.root)
        before = snapshot(self.root)
        self.assertEqual(kit.uninstall(self.root)["status"], "not_installed")
        self.assertEqual(snapshot(self.root), before)

    def test_unowned_collision_even_identical_is_rejected_before_writing(self):
        target = self.root / kit.RULE
        target.parent.mkdir(parents=True)
        target.write_bytes(self.files[kit.RULE])
        before = snapshot(self.root)
        self.assertEqual(kit.preview(self.root, self.payload)["status"], "conflicts")
        self.assert_error("conflicts", kit.install, self.root, self.payload)
        self.assertEqual(snapshot(self.root), before)

    def test_local_edit_blocks_install_and_entire_uninstall(self):
        kit.install(self.root, self.payload)
        (self.root / kit.SKILL).write_bytes(b"User's revised skill.\n")
        before = snapshot(self.root)
        self.assert_error("local_changes", kit.install, self.root, self.payload)
        self.assert_error("modified_files", kit.uninstall, self.root)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse(kit.doctor(self.root, self.payload)["files_valid"])

    def test_moved_edited_file_is_preserved_and_uninstall_can_finish(self):
        kit.install(self.root, self.payload)
        target = self.root / kit.SKILL
        target.write_bytes(b"My customization.\n")
        backup = self.base / "my-custom-skill.md"
        target.rename(backup)
        result = kit.uninstall(self.root)
        self.assertIn(kit.SKILL, result["previously_missing"])
        self.assertEqual(backup.read_bytes(), b"My customization.\n")

    def test_changed_source_requires_uninstall_then_install(self):
        kit.install(self.root, self.payload)
        before = snapshot(self.root)
        (self.payload / kit.RULE).write_bytes(b"# Updated source rule\n")
        self.assert_error("upgrade_requires_uninstall", kit.install, self.root, self.payload)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse(kit.doctor(self.root, self.payload)["payload_matches_installation"])
        kit.uninstall(self.root)
        kit.install(self.root, self.payload)
        self.assertEqual((self.root / kit.RULE).read_bytes(), b"# Updated source rule\n")

    def test_invalid_payload_frontmatter_and_extra_paths_are_rejected(self):
        skill = self.payload / kit.SKILL
        for data in (b"No front matter", b"---\nname: wrong\ndescription: desc\n---\nBody", b"---\nname: work-large-codebase\n---\nBody"):
            with self.subTest(data=data):
                skill.write_bytes(data)
                self.assert_error("invalid_skill", kit.install, self.root, self.payload)
                self.assertFalse(self.root.exists())
        skill.write_bytes(self.files[kit.SKILL])
        (self.payload / "settings.json").write_text("{}", encoding="utf-8")
        self.assert_error("invalid_path", kit.install, self.root, self.payload)
        self.assertFalse(self.root.exists())

    def test_traversal_and_unauthorized_manifest_paths_are_rejected_read_only(self):
        kit.install(self.root, self.payload)
        manifest_path = self.root / kit.MANIFEST
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        outside = self.base / "outside.txt"
        outside.write_bytes(b"Keep me.\n")
        for value in ("../outside.txt", "/tmp/outside", "rules/../settings.json", "settings.json", "skills/work-large-codebase/references/../../other.md", "rules\\other.md"):
            with self.subTest(path=value):
                record = json.loads(json.dumps(original))
                record["files"][value] = kit.digest(outside.read_bytes())
                manifest_path.write_text(json.dumps(record), encoding="utf-8")
                before = snapshot(self.root)
                self.assert_error("invalid_path", kit.uninstall, self.root)
                self.assertEqual(snapshot(self.root), before)
                self.assertEqual(outside.read_bytes(), b"Keep me.\n")

    def test_invalid_manifest_hash_schema_and_directory_ownership(self):
        kit.install(self.root, self.payload)
        manifest_path = self.root / kit.MANIFEST
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        records = []
        for key, value in (("schema_version", True), ("created_dirs", [".."])):
            record = json.loads(json.dumps(original))
            record[key] = value
            records.append(record)
        record = json.loads(json.dumps(original))
        record["files"][kit.RULE] = "not-a-hash"
        records.append(record)
        record = json.loads(json.dumps(original))
        del record["files"][kit.SKILL]
        records.append(record)
        for record in records:
            with self.subTest(record=record):
                manifest_path.write_text(json.dumps(record), encoding="utf-8")
                before = snapshot(self.root)
                self.assert_error("invalid_manifest", kit.uninstall, self.root)
                self.assertEqual(snapshot(self.root), before)

    def make_symlink(self, link, target, *, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Symlinks unavailable on this test host: {error}")

    def test_symlinked_root_and_destination_parent_are_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.make_symlink(self.root, outside, directory=True)
        self.assert_error("symlink_target", kit.install, self.root, self.payload)
        self.root.unlink()
        self.root.mkdir()
        self.make_symlink(self.root / "rules", outside, directory=True)
        before = snapshot(outside)
        self.assert_error("symlink_path", kit.install, self.root, self.payload)
        self.assertEqual(snapshot(outside), before)
        self.assertFalse((self.root / kit.MANIFEST).exists())

    def test_symlinked_payload_and_installed_file_are_rejected(self):
        source = self.payload / kit.RULE
        source.unlink()
        outside = self.base / "outside.md"
        outside.write_bytes(self.files[kit.RULE])
        self.make_symlink(source, outside)
        self.assert_error("symlink_payload", kit.install, self.root, self.payload)
        source.unlink()
        source.write_bytes(self.files[kit.RULE])
        kit.install(self.root, self.payload)
        target = self.root / kit.RULE
        target.unlink()
        self.make_symlink(target, outside)
        self.assert_error("symlink_path", kit.uninstall, self.root)
        self.assertTrue((self.root / kit.SKILL).is_file())
        self.assertEqual(outside.read_bytes(), self.files[kit.RULE])

    def test_windows_reparse_point_is_rejected_without_symlink_mode(self):
        self.root.mkdir()
        rules = self.root / "rules"
        rules.mkdir()
        real_lstat = kit._lstat

        def reparse(path):
            if path == rules:
                return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_file_attributes=0x400)
            return real_lstat(path)

        with mock.patch.object(kit, "_lstat", side_effect=reparse):
            self.assert_error("symlink_path", kit.install, self.root, self.payload)
        self.assertFalse((self.root / kit.MANIFEST).exists())

    def test_mid_install_write_failure_rolls_back(self):
        unrelated = self.write_unrelated()
        real_create = kit._atomic_create

        def fail(root, value, data, written, temporary):
            if value == kit.SKILL:
                raise OSError("Injected write failure")
            return real_create(root, value, data, written, temporary)

        with mock.patch.object(kit, "_atomic_create", side_effect=fail):
            error = self.assert_error("install_failed", kit.install, self.root, self.payload)
        self.assertTrue(error.details["rolled_back"])
        self.assertFalse((self.root / kit.JOURNAL).exists())
        for value in self.files:
            self.assertFalse((self.root / value).exists())
        for value, data in unrelated.items():
            self.assertEqual((self.root / value).read_bytes(), data)

    def test_atomic_publication_then_exception_or_interrupt_is_tracked(self):
        real_link = kit.os.link
        for failure in (OSError, KeyboardInterrupt):
            with self.subTest(failure=failure.__name__):
                def interrupted_link(source, destination, **kwargs):
                    real_link(source, destination, **kwargs)
                    if Path(destination).relative_to(self.root).as_posix() == kit.RULE:
                        raise failure("Injected after destination creation")

                with mock.patch.object(kit.os, "link", side_effect=interrupted_link):
                    code = "interrupted" if failure is KeyboardInterrupt else "install_failed"
                    error = self.assert_error(code, kit.install, self.root, self.payload)
                self.assertTrue(error.details["rolled_back"])
                self.assertFalse((self.root / kit.JOURNAL).exists())
                self.assertFalse((self.root / kit.RULE).exists())
                self.assertEqual(list(self.root.rglob("*.tmp")), [])

    def test_temp_cleanup_failure_after_publish_rolls_back_destination(self):
        real_unlink = Path.unlink
        failed = False

        def fail_once(path, *args, **kwargs):
            nonlocal failed
            if path.name.startswith("stage-") and (self.root / kit.RULE).exists() and not failed:
                failed = True
                raise PermissionError("Injected staging cleanup failure")
            return real_unlink(path, *args, **kwargs)

        with mock.patch.object(Path, "unlink", fail_once):
            error = self.assert_error("install_failed", kit.install, self.root, self.payload)
        self.assertTrue(failed)
        self.assertTrue(error.details["rolled_back"])
        self.assertFalse((self.root / kit.RULE).exists())
        self.assertFalse((self.root / kit.JOURNAL).exists())
        self.assertEqual(list(self.root.rglob("*.tmp")), [])

    def test_incomplete_rollback_keeps_journal_and_uninstall_recovers(self):
        real_create = kit._atomic_create
        real_unlink = Path.unlink

        def fail_create(root, value, data, written, temporary):
            if value == kit.SKILL:
                raise OSError("Injected write failure")
            return real_create(root, value, data, written, temporary)

        def fail_unlink(path, *args, **kwargs):
            if path == self.root / kit.RULE:
                raise PermissionError("Injected rollback deletion failure")
            return real_unlink(path, *args, **kwargs)

        with mock.patch.object(kit, "_atomic_create", side_effect=fail_create), mock.patch.object(Path, "unlink", fail_unlink):
            error = self.assert_error("install_failed", kit.install, self.root, self.payload)
        self.assertFalse(error.details["rolled_back"])
        self.assertEqual(error.details["recovery_journal"], kit.JOURNAL)
        self.assertTrue((self.root / kit.JOURNAL).is_file())
        self.assertEqual(kit.preview(self.root, self.payload)["status"], "recovery_needed")
        self.assertEqual(kit.uninstall(self.root)["status"], "recovered")
        self.assertFalse((self.root / kit.RULE).exists())
        self.assertFalse((self.root / kit.JOURNAL).exists())

    def test_real_process_exit_leaves_actionable_journal(self):
        # os._exit bypasses exception cleanup, representing a killed installer.
        code = """
import os
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from tools import bob_workflow as kit
original = kit._atomic_create
def stop(root, value, data, written, temporary):
    original(root, value, data, written, temporary)
    if value == kit.RULE:
        os._exit(77)
kit._atomic_create = stop
kit.install(Path(sys.argv[2]), Path(sys.argv[3]))
"""
        result = subprocess.run([sys.executable, "-B", "-c", code, str(REPOSITORY), str(self.root), str(self.payload)],
                                cwd=self.base, capture_output=True, timeout=15, check=False)
        self.assertEqual(result.returncode, 77, result.stderr)
        self.assertEqual(kit.doctor(self.root, self.payload)["status"], "recovery_needed")
        self.assert_error("recovery_needed", kit.install, self.root, self.payload)
        self.assertEqual(kit.uninstall(self.root)["status"], "recovered")
        self.assertFalse((self.root / kit.RULE).exists())

    def test_uninstall_deletion_failure_retains_metadata_for_retry(self):
        kit.install(self.root, self.payload)
        real_unlink = Path.unlink

        def fail(path, *args, **kwargs):
            if path == self.root / kit.SKILL:
                raise PermissionError("Injected unlink failure")
            return real_unlink(path, *args, **kwargs)

        with mock.patch.object(Path, "unlink", fail):
            self.assert_error("uninstall_incomplete", kit.uninstall, self.root)
        self.assertTrue((self.root / kit.MANIFEST).is_file())
        self.assertEqual(kit.uninstall(self.root)["status"], "uninstalled")

    def test_cli_exit_codes_and_json_evidence(self):
        for command, expected_code, expected_status in (("preview", 0, "ready"), ("doctor", 1, "not_installed"),
                                                       ("install", 0, "installed"), ("doctor", 0, "healthy"),
                                                       ("install", 0, "unchanged"), ("uninstall", 0, "uninstalled")):
            with self.subTest(command=command, status=expected_status):
                result = self.cli(command)
                self.assertEqual(result.returncode, expected_code, result.stderr or result.stdout)
                output = json.loads(result.stdout)
                self.assertEqual(output["status"], expected_status)
                self.assertTrue(output["client_loading_not_tested"])
        path = self.root / kit.RULE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"Unowned.\n")
        result = self.cli("install")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["error"]["code"], "conflicts")

    def test_shipped_payload_is_valid(self):
        self.assertEqual(kit.VERSION, (REPOSITORY / "VERSION").read_text(encoding="utf-8").strip())
        actual = kit.load_payload(REPOSITORY / "payload")
        self.assertIn(kit.RULE, actual)
        self.assertIn(kit.SKILL, actual)
        self.assertTrue(all(value.startswith(("rules/", "skills/")) for value in actual))


if __name__ == "__main__":
    unittest.main()
