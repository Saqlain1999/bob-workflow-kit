"""Integration and negative controls for remediated release preparation."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "reminder-remediated-release-handoff"
SCRIPT = ROOT / "scripts" / "evaluate.py"

PASSING_GUIDE = '''# Reminder idempotency candidate

## Availability

This corrected candidate is unreleased and ready for release review. There is no release artifact and it must not deploy before separate authorization.

## Current behavior

- Owner isolation keeps `list_for(owner)` limited to that owner's records.
- Reusing an idempotency key with different content for the same owner raises a generic conflict without stored reminder content.
- Same-content retries survive restart; unkeyed calls and the public Reminder fields remain compatible in the bounded fixture.

## Operator guidance

Continue using the previous supported version. There is no migration, removal command, or rollback artifact because this candidate has not been released. If later release review rejects the candidate, retain the previous version and return the exact state to implementation and independent review.

## Evidence limits

The finite public checks and current review support a ready for release review handoff. They do not establish broad compatibility, performance, production readiness, process-safe concurrency, a general security proof, or live Bob behavior.
'''

PASSING_HANDOFF = '''# Release readiness handoff: reminder idempotency

## Candidate and evidence

- Candidate: exact remediated and independently re-reviewed fixture state.
- `REMEDIATION_REVIEW.md` is the current review and records `ready for release preparation` with REV-001 and REV-002 resolved.
- Historical `REVIEW_HANDOFF.md` and `RELEASE_HANDOFF.md` are preserved evidence of the pre-remediation candidate, not current conclusions.
- The complete diff was inspected; product source and trusted tests are unchanged in this stage.

## Documentation and operations

- Only `USER_GUIDE.md` and `RELEASE_READINESS_HANDOFF.md` changed.
- The guide documents corrected but unreleased behavior and current evidence limits.
- There is no release artifact, no migration, no removal command, and no rollback artifact. Continue using the previous supported version until separately authorized.

## Acceptance and finding disposition

- AC-1: passed in current evidence; REV-001 High is resolved by equality-based owner isolation and its trusted behavior check.
- AC-2: passed in current evidence; REV-002 Medium is resolved by the generic conflict and its exception-boundary check.
- AC-3: passed in current evidence for same-content retry and restart behavior.
- AC-4: preserved; accepted inputs, historical records, source, trusted tests, and unrelated work are unchanged.
- No open blocking finding remains in the bounded current review scope.

## Validation evidence

- `python3 -m unittest discover -s tests -v`: observed 12/12 trusted checks, exit 0, on the exact candidate.
- The complete diff and current re-review were inspected; trusted tests unchanged.
- These finite public checks are not a general security proof.
- Process-safe concurrency was not run. Broad compatibility, performance, packaging, production readiness, compliance, deployment, and live Bob were not established.

## Release decision and limits

- Decision: ready for release review.
- This decision does not authorize a release, tag, artifact, deployment, publication, or announcement.
- It is not production readiness, deployment approval, compliance evidence, or proof that other defects are absent.

## Recovery and next gate

Hand this exact state to human release review. Mark the evidence stale after any source, trusted-test, review, or environment change; rerun the exact suite and inspect the new complete diff. Stop if permission is denied, a protected input changes, or a check fails. Preserve unrelated work. Return to bounded implementation and independent review before release preparation if a blocker appears.
'''


class ReminderRemediatedReleaseHandoffIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="remediated-release-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        result = self.invoke(
            "prepare", "--task", "reminder-remediated-release-handoff",
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
            phase, "--task", "reminder-remediated-release-handoff",
            "--workspace", self.workspace, "--result", report,
        )
        return result, json.loads(report.read_text(encoding="utf-8"))

    def write_good(self) -> None:
        (self.workspace / "USER_GUIDE.md").write_text(PASSING_GUIDE, encoding="utf-8")
        (self.workspace / "RELEASE_READINESS_HANDOFF.md").write_text(
            PASSING_HANDOFF, encoding="utf-8"
        )

    def test_baseline_reproduces_ten_named_release_failures(self) -> None:
        result, report = self.check("baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 12)
        self.assertEqual(len(report["tests"]["failures"]), 10)

    def test_known_good_handoff_passes_and_preserves_exact_candidate(self) -> None:
        self.write_good()
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 12)
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(
            report["candidate_scope"]["observed_changes"],
            ["RELEASE_READINESS_HANDOFF.md", "USER_GUIDE.md"],
        )
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")

    def test_release_approval_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "RELEASE_READINESS_HANDOFF.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Decision: ready for release review", "Decision: release approved",
            ),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_remediated_release_handoff.ReminderRemediatedReleaseHandoffTests.test_exact_ready_for_review_decision_and_no_publication",
            report["tests"]["failures"],
        )

    def test_missing_current_review_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "RELEASE_READINESS_HANDOFF.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "REMEDIATION_REVIEW.md", "an earlier review",
            ),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_remediated_release_handoff.ReminderRemediatedReleaseHandoffTests.test_current_review_supersedes_but_preserves_historical_gates",
            report["tests"]["failures"],
        )

    def test_false_current_validation_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "RELEASE_READINESS_HANDOFF.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("12/12", "11/12"),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_remediated_release_handoff.ReminderRemediatedReleaseHandoffTests.test_exact_current_validation_is_bounded",
            report["tests"]["failures"],
        )

    def test_source_edit_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "notifier" / "service.py"
        path.write_text(path.read_text(encoding="utf-8") + "\n# release edit\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")

    def test_current_review_edit_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "REMEDIATION_REVIEW.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nrewritten\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")

    def test_historical_release_edit_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "RELEASE_HANDOFF.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("release blocked", "ready"),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")

    def test_candidate_test_edit_is_rejected(self) -> None:
        self.write_good()
        test = self.workspace / "tests" / "test_remediated_release_handoff.py"
        test.write_text("# weakened\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")

    def test_unrelated_file_is_rejected(self) -> None:
        self.write_good()
        (self.workspace / "notes.txt").write_text("unrelated\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")

    def test_result_inside_workspace_is_rejected(self) -> None:
        result = self.invoke(
            "candidate", "--task", "reminder-remediated-release-handoff",
            "--workspace", self.workspace, "--result", self.workspace / "result.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the candidate workspace", result.stderr)

    def test_original_fixture_remains_unchanged(self) -> None:
        for relative in [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_HANDOFF.md",
            "REVIEW_HANDOFF.md", "RELEASE_HANDOFF.md", "REMEDIATION_REVIEW.md",
            "TEAM_NOTES.md", "USER_GUIDE.md", "RELEASE_READINESS_HANDOFF.md",
            "notifier/service.py", "tests/test_remediated_release_handoff.py",
        ]:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (self.workspace / relative).read_bytes(),
                    (FIXTURE / relative).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
