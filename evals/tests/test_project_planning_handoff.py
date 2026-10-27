"""Integration and negative-control tests for project-planning-handoff-v1."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "project-planning-handoff"
SCRIPT = ROOT / "scripts" / "evaluate.py"

PASSING_PLAN = """# Delivery plan: reminder idempotency

## Request and boundary

- Outcome: add caller-supplied idempotency without implementing it in this planning task.
- Constraints: Python standard library only; preserve public Reminder fields; keep old records readable; do not rewrite the store during startup.
- Non-goals: do not implement source changes or add a service.
- Authorization: stop on denied approval or a requested change outside DELIVERY_PLAN.md.

## Repository evidence

- Observed — REQUEST.md: the same owner and same key with identical content returns the original reminder.
- Observed — notifier/service.py: schedule currently creates a UUID and calls append for every request.
- Observed — notifier/store.py: the store is append-only newline-delimited JSON and records() reads every record.
- Observed — project-tests.md: the project command is python3 -m unittest discover -s tests -v.
- Inferred: a record-compatible optional key can persist across a new service instance.
- Unknown: expected concurrency level; stop for a product decision if process-safe guarantees are required.

## Acceptance criteria

- AC-1: Given the same owner and same key with identical message and due_at, a retry returns the original reminder and appends no duplicate.
- AC-2: Given the same owner and same key with different content, scheduling raises IdempotencyConflict.
- AC-3: Given different owners using the same key, each owner can schedule independently; behavior survives a new service instance over the same store.
- AC-4: Given existing records without a key, reads still succeed and public Reminder fields remain compatible.

## Architecture decision

- Option A: add an optional idempotency envelope to new JSON records and scan records by owner/key before append.
- Option B: maintain a separate sidecar index keyed by owner/key.
- Selected option: Option A, because it fits current small-file reads and avoids cross-file partial update compatibility risk.
- Consequences and rollback: linear lookup cost; old records omit the optional envelope; rollback ignores the added storage field.
- Revisit trigger: revisit for measured scale or concurrent multi-process scheduling.

## Implementation slices

| Slice | Files | Change | Criteria | Validation |
| --- | --- | --- | --- | --- |
| 1 | notifier/store.py | preserve optional idempotency data and old records | AC-3, AC-4 | python3 -m unittest discover -s tests -v |
| 2 | notifier/service.py | match owner/key/content and raise conflicts | AC-1, AC-2, AC-3 | tests/ exact retry, conflict, owner, and restart cases |
| 3 | tests/ and docs | add compatibility and release handoff coverage | AC-1, AC-2, AC-3, AC-4 | python3 -m unittest discover -s tests -v |

Stop before edits if approval is denied or required behavior exceeds the stated file-store boundary.

## Risks and handoffs

- Concurrent processes can race between scan and append; confirm the required guarantee before claiming safety.
- A partial final line already affects the current store reader; do not broaden recovery silently.
- Existing records and public Reminder compatibility need regression coverage.
- Preserve unrelated work and user data; rollback must not rewrite the store.
- Documentation/release handoff must describe the optional key, conflict, compatibility, and remaining concurrency limit.

## Durable checkpoint

- Inspected state: REQUEST.md, notifier/service.py, notifier/store.py, and project-tests.md in this prepared workspace.
- Stale evidence: any change to those files, repository instructions, or status requires reinspection.
- First safe implementation action: add failing tests for AC-1 through AC-4.
- Commands still to run: git status --short and python3 -m unittest discover -s tests -v.
- Resume: recheck status and evidence, then begin the first failing test.
- Abort: stop on denied approval, changed scope, or unresolved concurrency requirements.

## Evidence limits

This plan does not prove implementation, tests, security, performance, compatibility, or live agent behavior.
"""


class ProjectPlanningHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="planning-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        result = self.invoke("prepare", "--task", "project-planning-handoff", "--output", self.workspace)
        self.assertEqual(result.returncode, 0, result.stderr)

    def invoke(self, *arguments: object) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, arguments)],
            cwd=self.base, text=True, capture_output=True, timeout=20, check=False,
        )

    def check(self, phase: str) -> tuple[subprocess.CompletedProcess, dict]:
        report = self.base / f"{phase}.json"
        result = self.invoke(
            phase, "--task", "project-planning-handoff",
            "--workspace", self.workspace, "--result", report,
        )
        return result, json.loads(report.read_text(encoding="utf-8"))

    def test_baseline_reproduces_seven_named_failures(self) -> None:
        result, report = self.check("baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertEqual(len(report["tests"]["failures"]), 7)

    def test_known_good_plan_passes_without_claiming_design_correctness(self) -> None:
        (self.workspace / "DELIVERY_PLAN.md").write_text(PASSING_PLAN, encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(report["candidate_scope"]["observed_changes"], ["DELIVERY_PLAN.md"])
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["manual_acceptance"], "not_assessed")
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")

    def test_missing_acceptance_trace_fails(self) -> None:
        weakened = PASSING_PLAN.replace("AC-4: Given", "Compatibility: Given")
        (self.workspace / "DELIVERY_PLAN.md").write_text(weakened, encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_delivery_plan.DeliveryPlanTests.test_four_acceptance_criteria_cover_behavior_and_compatibility",
            report["tests"]["failures"],
        )

    def test_missing_stale_evidence_fails(self) -> None:
        weakened = PASSING_PLAN.replace("Stale evidence:", "Refresh note:")
        (self.workspace / "DELIVERY_PLAN.md").write_text(weakened, encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_delivery_plan.DeliveryPlanTests.test_checkpoint_supports_stale_detection_resume_and_abort",
            report["tests"]["failures"],
        )

    def test_source_change_is_rejected_even_when_plan_passes(self) -> None:
        (self.workspace / "DELIVERY_PLAN.md").write_text(PASSING_PLAN, encoding="utf-8")
        source = self.workspace / "notifier" / "service.py"
        source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")
        self.assertFalse(report["protected_inputs_match_prepared"])

    def test_unrelated_change_is_rejected(self) -> None:
        (self.workspace / "DELIVERY_PLAN.md").write_text(PASSING_PLAN, encoding="utf-8")
        (self.workspace / "notes.txt").write_text("extra\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertFalse(report["candidate_scope"]["matches"])

    def test_original_fixture_remains_unchanged(self) -> None:
        self.assertEqual(
            (self.workspace / "REQUEST.md").read_bytes(),
            (FIXTURE / "REQUEST.md").read_bytes(),
        )
        self.assertEqual(
            (self.workspace / "notifier" / "service.py").read_bytes(),
            (FIXTURE / "notifier" / "service.py").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
