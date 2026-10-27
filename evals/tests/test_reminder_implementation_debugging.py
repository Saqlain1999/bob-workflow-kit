"""Integration and negative-control tests for reminder-implementation-debugging-v1."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "reminder-implementation-debugging"
SCRIPT = ROOT / "scripts" / "evaluate.py"

PASSING_SERVICE = '''"""Completed bounded reminder idempotency behavior."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import uuid

from .store import ReminderStore


@dataclass(frozen=True)
class Reminder:
    reminder_id: str
    owner: str
    message: str
    due_at: str


class IdempotencyConflict(ValueError):
    """The owner/key pair already identifies different reminder content."""


class ReminderService:
    def __init__(self, store: ReminderStore) -> None:
        self.store = store

    def schedule(
        self, owner: str, message: str, due_at: str,
        idempotency_key: str | None = None,
    ) -> Reminder:
        datetime.fromisoformat(due_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        if idempotency_key is not None:
            for record in self.store.records():
                if record["owner"] != owner or record.get("_idempotency_key") != idempotency_key:
                    continue
                reminder = Reminder(**{
                    name: record[name] for name in Reminder.__dataclass_fields__
                })
                if reminder.message == message and reminder.due_at == due_at:
                    return reminder
                raise IdempotencyConflict("owner/key pair already has different content")
        reminder = Reminder(str(uuid.uuid4()), owner, message, due_at)
        record = asdict(reminder)
        if idempotency_key is not None:
            record["_idempotency_key"] = idempotency_key
        self.store.append(record)
        return reminder

    def list_for(self, owner: str) -> list[Reminder]:
        return [
            Reminder(**{name: record[name] for name in Reminder.__dataclass_fields__})
            for record in self.store.records()
            if record["owner"] == owner
        ]
'''

PASSING_HANDOFF = """# Implementation handoff: reminder idempotency

## Scope and current state

- Outcome: complete AC-1, AC-2, AC-3, and AC-4 in the bounded reminder service.
- Inspected the request, plan, source, tests, TEAM_NOTES.md, and IMPLEMENTATION_CHECKPOINT.md.
- The checkpoint's historical smoke was stale; current evidence replaced it.

## Reproduction and diagnosis

- Baseline command: `python3 -m unittest discover -s tests -v`, exit 1 with four failures.
- Observed cause: the partial schedule path stored keys but never matched retries or rejected conflicts.

## Changed files

- `notifier/service.py`: match owner/key and return or raise for AC-1 through AC-4.
- `IMPLEMENTATION_HANDOFF.md`: preserve current implementation evidence.
- Protected request, plan, checkpoint, tests, and TEAM_NOTES.md remain unchanged.

## Validation evidence

- `python3 -m unittest discover -s tests -v`: Observed 10/10 passed, exit 0 on the final state.
- Complete diff: manually inspected. Independent review and security assessment were not run.

## Remaining state

- Known failures: none in the focused suite.
- Unrun checks: process-concurrent scheduling, performance, deployment, and live Bob behavior.
- The scan-and-append sequence is not concurrent-process safe.

## Stop and recovery

- Resume by checking current status and rerunning the exact focused command if source or tests changed.
- Stop if protected inputs changed, scope expands, or permission is denied.
"""


class ReminderImplementationDebuggingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="implementation-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        result = self.invoke(
            "prepare", "--task", "reminder-implementation-debugging",
            "--output", self.workspace,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def invoke(self, *arguments: object) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, arguments)],
            cwd=self.base, text=True, capture_output=True, timeout=20, check=False,
        )

    def check(self, phase: str) -> tuple[subprocess.CompletedProcess, dict]:
        report = self.base / f"{phase}.json"
        result = self.invoke(
            phase, "--task", "reminder-implementation-debugging",
            "--workspace", self.workspace, "--result", report,
        )
        return result, json.loads(report.read_text(encoding="utf-8"))

    def repair(self, service: str = PASSING_SERVICE, handoff: str = PASSING_HANDOFF) -> None:
        (self.workspace / "notifier" / "service.py").write_text(service, encoding="utf-8")
        (self.workspace / "IMPLEMENTATION_HANDOFF.md").write_text(handoff, encoding="utf-8")

    def test_baseline_reproduces_four_named_failures(self) -> None:
        result, report = self.check("baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertEqual(len(report["tests"]["failures"]), 4)

    def test_known_good_repair_passes_with_protected_inputs(self) -> None:
        self.repair()
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(
            report["candidate_scope"]["observed_changes"],
            ["IMPLEMENTATION_HANDOFF.md", "notifier/service.py"],
        )
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["manual_acceptance"], "not_assessed")
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")

    def test_missing_handoff_fails_even_when_behavior_is_repaired(self) -> None:
        (self.workspace / "notifier" / "service.py").write_text(
            PASSING_SERVICE, encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_idempotency.ReminderImplementationTests.test_handoff_records_current_evidence_and_limits",
            report["tests"]["failures"],
        )

    def test_weakened_conflict_behavior_fails(self) -> None:
        weakened = PASSING_SERVICE.replace(
            'raise IdempotencyConflict("owner/key pair already has different content")',
            "return reminder",
        )
        self.repair(service=weakened)
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_idempotency.ReminderImplementationTests.test_conflicting_reuse_raises_without_append",
            report["tests"]["failures"],
        )

    def test_protected_plan_change_is_rejected(self) -> None:
        self.repair()
        plan = self.workspace / "DELIVERY_PLAN.md"
        plan.write_text(plan.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")
        self.assertFalse(report["protected_inputs_match_prepared"])

    def test_candidate_test_edit_is_rejected_even_when_trusted_tests_pass(self) -> None:
        self.repair()
        candidate_test = self.workspace / "tests" / "test_idempotency.py"
        candidate_test.write_text("# weakened candidate copy\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertTrue(report["tests"]["successful"])
        self.assertFalse(report["candidate_scope"]["matches"])

    def test_unrelated_change_is_rejected(self) -> None:
        self.repair()
        (self.workspace / "notes.txt").write_text("unrelated\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertFalse(report["candidate_scope"]["matches"])

    def test_original_fixture_remains_unchanged(self) -> None:
        for relative in [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_CHECKPOINT.md",
            "TEAM_NOTES.md", "notifier/service.py", "tests/test_idempotency.py",
        ]:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (self.workspace / relative).read_bytes(),
                    (FIXTURE / relative).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
