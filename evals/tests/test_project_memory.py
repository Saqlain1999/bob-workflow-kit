"""Integration and negative controls for the project-memory fixture."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate.py"


class ProjectMemoryFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="project-memory-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.workspace = self.directory / "candidate"
        prepared = self.invoke("prepare", "--output", self.workspace)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)

    def invoke(self, command: str, *arguments: object) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), command, "--task", "project-memory", *map(str, arguments)],
            cwd=str(ROOT), env=environment, text=True, capture_output=True,
            timeout=15, check=False,
        )

    def candidate(self):
        result = self.invoke("candidate", "--workspace", self.workspace)
        return result, json.loads(result.stdout)

    def repair(self) -> None:
        path = self.workspace / "memory_adapter.py"
        source = path.read_text(encoding="utf-8")
        replacements = {
            '        self.state_path.write_text(\n            json.dumps(self._data, indent=2, sort_keys=True) + "\\n",\n            encoding="utf-8",\n        )':
            '        self.temporary_path.write_text(\n            json.dumps(self._data, indent=2, sort_keys=True) + "\\n",\n            encoding="utf-8",\n        )\n        self.temporary_path.replace(self.state_path)',
            '        if not value:\n            raise ValueError("identifier must not be empty")':
            '        if not value or value in {".", ".."} or "/" in value or "\\\\" in value:\n            raise ValueError("identifier must be one safe path segment")',
            '        return key\n\n    def put(': '        return project + ":" + key\n\n    def put(',
            '        previous = self._data["records"].get(storage_key)\n        revision = 1 if previous is None else int(previous["revision"]) + 1':
            '        if not self.backend_available:\n            raise BackendUnavailable("Memory unavailable; use projects/" + project + "/EVIDENCE.md")\n        previous = self._data["records"].get(storage_key)\n        current_revision = 0 if previous is None else int(previous["revision"])\n        if expected_revision is not None and expected_revision != current_revision:\n            raise RevisionConflict("expected revision does not match current revision")\n        revision = current_revision + 1',
            '            "trust": "trusted",': '            "trust": "untrusted_data",',
            '        self._data["history"][storage_key] = [record]':
            '        self._data["history"].setdefault(storage_key, []).append(record)',
            '        storage_key = self._storage_key(project, key)\n        record = self._data["records"].get(storage_key)\n        if record is None:':
            '        storage_key = self._storage_key(project, key)\n        if not self.backend_available:\n            raise BackendUnavailable("Memory unavailable; use projects/" + project + "/EVIDENCE.md")\n        record = self._data["records"].get(storage_key)\n        if record is None:',
            '        result = dict(record)\n        result["status"] = "current"\n        return result':
            '        result = dict(record)\n        if current_source_hash is not None and current_source_hash != record["source_hash"]:\n            result.update({"status": "stale", "current_source_hash": current_source_hash, "recorded_source_hash": record["source_hash"]})\n        else:\n            result["status"] = "current"\n        return result',
            '        return self.put(\n            "shared-lessons", key, source.get("value", ""),\n            source.get("source_hash", "unknown"),\n        )':
            '        promoted = self.put(\n            "shared-lessons", key, sanitized_summary,\n            source.get("source_hash", "unknown"),\n        )\n        storage_key = self._storage_key("shared-lessons", key)\n        self._data["records"][storage_key]["trust"] = "sanitized_summary"\n        self._data["history"][storage_key][-1]["trust"] = "sanitized_summary"\n        self._save()\n        promoted["trust"] = "sanitized_summary"\n        return promoted',
            '        self._data["records"].pop(storage_key, None)\n        self._save()':
            '        self._data["records"].pop(storage_key, None)\n        self._data["history"].pop(storage_key, None)\n        self._data["index"] = [item for item in self._data["index"] if item != storage_key]\n        self._save()',
            '        return sorted(item[len(prefix):] if item.startswith(prefix) else item for item in self._data["index"])':
            '        return sorted(item[len(prefix):] for item in self._data["index"] if item.startswith(prefix) and item in self._data["records"])',
        }
        for old, new in replacements.items():
            self.assertEqual(source.count(old), 1, old)
            source = source.replace(old, new)
        source = source.replace('or "/" in value', 'or ":" in value or "/" in value')
        source = source.replace(
            '        cls._validate_identifier(project)',
            '        if project not in {"project-alpha", "project-beta", "shared-lessons"}:\n'
            '            raise ValueError("unknown project scope")\n'
            '        cls._validate_identifier(project)',
        )
        source = source.replace(
            '        prefix = project + ":"',
            '        self._storage_key(project, "validation")\n        prefix = project + ":"',
        )
        source = source.replace(
            '        previous = self._data["records"].get(storage_key)',
            '        self._data = self._load()  # Sequential independent-instance freshness only.\n'
            '        previous = self._data["records"].get(storage_key)',
        )
        save_start = source.index('    def _save(')
        save_end = source.index('    @staticmethod', save_start)
        source = source[:save_start] + '''    def _save(self) -> None:
        try:
            self.temporary_path.write_text(
                json.dumps(self._data, indent=2, sort_keys=True) + "\\n",
                encoding="utf-8",
            )
            self.temporary_path.replace(self.state_path)
        except OSError:
            self._data = self._load()
            raise
        finally:
            self.temporary_path.unlink(missing_ok=True)

''' + source[save_end:]
        path.write_text(source, encoding="utf-8")
        (self.workspace / "MEMORY_HANDOFF.md").write_text(
            """# Memory handoff

Status: contract checks passed
Allowed changes: memory_adapter.py and MEMORY_HANDOFF.md
Project isolation: project-qualified keys; shared promotion is explicit and sanitized.
Source freshness: caller-supplied token mismatch marks stale; evidence hashing is manual.
Revision conflicts: sequential stale independent instances refused; concurrent CAS is not qualified.
Deletion: direct, history, and index entries are removed; external backups are outside this fixture.
Backend outage: Boolean recall simulation points to evidence; no real fallback read or all-operation outage claim.
Promotion provenance: summary/trust checks only; source project/key/revision provenance remains manual.
Live Bob evidence: not assessed
Production evidence: not assessed
""",
            encoding="utf-8",
        )

    def test_prepared_baseline_reproduces_exact_named_failures(self) -> None:
        result = self.invoke("baseline", "--workspace", self.workspace)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["task_id"], "bob-project-memory-v1")
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 17)
        self.assertEqual(len(report["tests"]["failures"]), 14)
        self.assertEqual(report["tests"]["errors"], [])
        self.assertTrue(report["protected_inputs_match_prepared"])

    def test_known_good_control_passes_with_only_two_allowed_files_changed(self) -> None:
        self.repair()
        result, report = self.candidate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 17)
        self.assertTrue(report["tests"]["successful"])
        self.assertEqual(
            report["candidate_scope"]["observed_changes"],
            ["MEMORY_HANDOFF.md", "memory_adapter.py"],
        )
        self.assertTrue(report["candidate_scope"]["only_allowed_changes"])
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")
        self.assertEqual(report["model_calls_made_by_helper"], 0)

    def test_partial_repair_without_handoff_remains_a_non_pass(self) -> None:
        self.repair()
        (self.workspace / "MEMORY_HANDOFF.md").write_bytes(
            (ROOT / "fixtures" / "bob-project-memory" / "MEMORY_HANDOFF.md").read_bytes()
        )
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_memory_adapter.ProjectMemoryContractTests.test_handoff_records_required_decisions_without_claiming_live_bob",
            report["tests"]["failures"],
        )

    def test_protected_contract_edit_is_rejected_even_if_behavior_passes(self) -> None:
        self.repair()
        contract = self.workspace / "contract.json"
        contract.write_text(contract.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(report["tests"]["successful"])
        self.assertEqual(report["status"], "protected_inputs_changed")

    def test_test_or_unrelated_file_edit_is_out_of_scope(self) -> None:
        self.repair()
        test_file = self.workspace / "tests" / "test_memory_adapter.py"
        test_file.write_text("# weakened\n", encoding="utf-8")
        (self.workspace / "unrelated.txt").write_text("extra\n", encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(report["tests"]["successful"])
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertFalse(report["candidate_scope"]["only_allowed_changes"])

    def test_process_local_only_control_fails_distinct_process_recall(self) -> None:
        self.repair()
        path = self.workspace / "memory_adapter.py"
        source = path.read_text(encoding="utf-8")
        start = source.index('    def _load(')
        end = source.index('    @staticmethod', start)
        source = source[:start] + '''    def _load(self):
        return _PROCESS_DATA.setdefault(str(self.root), {"records": {}, "history": {}, "index": []})

    def _save(self):
        pass

''' + source[end:]
        path.write_text('_PROCESS_DATA = {}\n' + source, encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_memory_adapter.ProjectMemoryContractTests.test_distinct_writer_reader_processes_recall_committed_value",
            report["tests"]["failures"],
        )

    def test_result_output_inside_candidate_is_rejected(self) -> None:
        result = self.invoke(
            "candidate", "--workspace", self.workspace,
            "--result", self.workspace / "candidate-result.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the candidate workspace", result.stderr)
        self.assertFalse((self.workspace / "candidate-result.json").exists())


if __name__ == "__main__":
    unittest.main()
