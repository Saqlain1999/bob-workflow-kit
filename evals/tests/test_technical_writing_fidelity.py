"""Controls for the bounded technical-writing fidelity exercise."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate.py"
FIXTURE = ROOT / "fixtures" / "technical-writing-fidelity"
PASSING_RUNBOOK = """# Orbit cache migration runbook

## Purpose

Move the Orbit cache to v2.4.1.

## Before you begin

You MUST create and keep the backup at `/var/lib/orbit/backups/current.tar`.

## Procedure

1. You MUST create the backup with `orbitctl backup --output /var/lib/orbit/backups/current.tar`.
2. After the backup succeeds, run `orbitctl migrate --target v2.4.1 --max-memory 2.5 GiB`.
3. Run `orbitctl verify --target v2.4.1`.
4. You MUST NOT run `orbitctl cleanup --target v2.4.1` until verification succeeds.

## Recovery and ownership

- If migration returns E_CONN_RESET, you MAY retry once, but only if you wait 30 s first.
- If migration returns E_AUTH_DENIED, you MUST NOT retry it.
- The on-call engineer owns rollback approval.
"""


class TechnicalWritingFidelityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="writing-fidelity-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.workspace = self.directory / "candidate"
        prepared = self.invoke("prepare", "--output", self.workspace)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)

    def invoke(self, command: str, *arguments: object) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT),
                command,
                "--task",
                "technical-writing-fidelity",
                *map(str, arguments),
            ],
            cwd=str(ROOT),
            env=environment,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )

    def candidate(self):
        result = self.invoke("candidate", "--workspace", self.workspace)
        return result, json.loads(result.stdout)

    def test_baseline_reproduces_only_the_two_structure_failures(self) -> None:
        result = self.invoke("baseline", "--workspace", self.workspace)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 8)
        self.assertEqual(
            sorted(report["tests"]["failures"]),
            [
                "test_runbook.RunbookFidelityTests.test_procedure_has_four_ordered_steps",
                "test_runbook.RunbookFidelityTests.test_required_sections_are_present",
            ],
        )
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertIsNone(report["candidate_scope"]["observed_changes"])
        self.assertIsNone(report["candidate_scope"]["matches"])

    def test_known_rewrite_passes_without_claiming_semantic_equivalence(self) -> None:
        (self.workspace / "RUNBOOK.md").write_text(PASSING_RUNBOOK, encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 8)
        self.assertEqual(report["tests"]["failures"], [])
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(report["candidate_scope"]["observed_changes"], ["RUNBOOK.md"])
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["manual_acceptance"], "not_assessed")
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")
        self.assertEqual(report["model_calls_made_by_helper"], 0)

    def test_weaker_permission_and_missing_condition_fail(self) -> None:
        weakened = PASSING_RUNBOOK.replace("you MAY retry once, but only if", "retry once after")
        (self.workspace / "RUNBOOK.md").write_text(weakened, encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "public_tests_failed")
        self.assertIn(
            "test_runbook.RunbookFidelityTests.test_connection_retry_keeps_permission_limit_condition_and_wait",
            report["tests"]["failures"],
        )

    def test_removed_negation_fails(self) -> None:
        weakened = PASSING_RUNBOOK.replace("you MUST NOT retry it", "retry it")
        (self.workspace / "RUNBOOK.md").write_text(weakened, encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_runbook.RunbookFidelityTests.test_authentication_failure_keeps_retry_prohibition",
            report["tests"]["failures"],
        )

    def test_reordered_commands_fail(self) -> None:
        reordered = PASSING_RUNBOOK.replace(
            "1. You MUST create the backup with `orbitctl backup --output /var/lib/orbit/backups/current.tar`.\n"
            "2. After the backup succeeds, run `orbitctl migrate --target v2.4.1 --max-memory 2.5 GiB`.",
            "1. Run `orbitctl migrate --target v2.4.1 --max-memory 2.5 GiB`.\n"
            "2. You MUST create the backup with `orbitctl backup --output /var/lib/orbit/backups/current.tar`.",
        )
        (self.workspace / "RUNBOOK.md").write_text(reordered, encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_runbook.RunbookFidelityTests.test_commands_are_preserved_once_and_in_order",
            report["tests"]["failures"],
        )

    def test_contract_change_is_rejected_even_when_runbook_passes(self) -> None:
        (self.workspace / "RUNBOOK.md").write_text(PASSING_RUNBOOK, encoding="utf-8")
        contract = self.workspace / "contract.json"
        contract.write_text(contract.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(report["tests"]["successful"])
        self.assertEqual(report["status"], "protected_inputs_changed")
        self.assertFalse(report["protected_inputs_match_prepared"])

    def test_unrelated_workspace_change_is_rejected_even_when_checks_pass(self) -> None:
        (self.workspace / "RUNBOOK.md").write_text(PASSING_RUNBOOK, encoding="utf-8")
        (self.workspace / "scratch.txt").write_text("unrelated\n", encoding="utf-8")
        result, report = self.candidate()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(report["tests"]["successful"])
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertEqual(
            report["candidate_scope"]["observed_changes"],
            ["RUNBOOK.md", "scratch.txt"],
        )
        self.assertFalse(report["candidate_scope"]["matches"])

    def test_candidate_result_cannot_change_the_verified_workspace(self) -> None:
        destination = self.workspace / "candidate-result.json"
        result = self.invoke(
            "candidate", "--workspace", self.workspace, "--result", destination
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the candidate workspace", result.stderr)
        self.assertFalse(destination.exists())

    def test_original_fixture_remains_unchanged(self) -> None:
        self.assertEqual(
            (self.workspace / "contract.json").read_bytes(),
            (FIXTURE / "contract.json").read_bytes(),
        )
        self.assertEqual(
            (self.workspace / "RUNBOOK.md").read_bytes(),
            (FIXTURE / "RUNBOOK.md").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
