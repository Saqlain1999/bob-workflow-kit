"""Integration and negative controls for reminder-remediated-review-v1."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "reminder-remediated-review"
SCRIPT = ROOT / "scripts" / "evaluate.py"

PASSING_REVIEW = '''# Remediation re-review handoff

## Reviewed state and evidence

- I independently reconciled the exact candidate with REQUEST.md, DELIVERY_PLAN.md, IMPLEMENTATION_HANDOFF.md, historical REVIEW_HANDOFF.md, USER_GUIDE.md, historical RELEASE_HANDOFF.md, TEAM_NOTES.md, current source, and trusted tests.
- The read-only first pass confirmed that REVIEW_HANDOFF.md and RELEASE_HANDOFF.md remain preserved historical records of the pre-remediation candidate. Product source, candidate tests, accepted inputs, and the remediation implementation handoff were not changed by this review.
- The complete remediation diff was inspected before the decision below.

## Finding dispositions

- REV-001 — High — resolved in this exact candidate. `ReminderService.list_for` uses `record["owner"] == owner`; `test_rev_001_owner_isolation_remains_fixed` demonstrates owner isolation for two owners.
- REV-002 — Medium — resolved in this exact candidate. The conflict path uses the generic conflict `owner/key pair already has different content`; `test_rev_002_conflict_message_remains_generic` demonstrates that stored message and reminder ID do not cross the error boundary.
- No new blocking finding was identified in the bounded reviewed scope. This is not a claim that findings are absent outside that scope.

## Validation evidence

- `python3 -m unittest discover -s tests -v`: observed 12/12 trusted checks, exit 0, on the exact candidate.
- The complete remediation diff and current implementation handoff were inspected. Candidate tests were unchanged. Retry, restart, owner-scoped keys, no-append conflicts, unkeyed calls, legacy records, invalid dates, and public fields remain covered by current evidence.

## Decision and limits

- Decision: ready for release preparation.
- This is not release approval and does not authorize a tag, artifact, deployment, publication, or announcement.
- Process-safe concurrency was not run. Packaging, compatibility, performance, production readiness, compliance, a general security proof, deployment, and live Bob were not established.

## Recovery and next gate

Hand this exact candidate and review to a separate documentation/release-preparation stage. Keep REVIEW_HANDOFF.md and RELEASE_HANDOFF.md preserved as historical evidence. Stop if permission is denied, a protected input, source, or trusted test changes, or a check fails. Preserve unrelated work. Mark this evidence stale after any source or environment change, rerun the exact suite, inspect the new diff, and resume from the last verified state.
'''


class ReminderRemediatedReviewIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="remediated-review-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        result = self.invoke(
            "prepare", "--task", "reminder-remediated-review", "--output", self.workspace,
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
            phase, "--task", "reminder-remediated-review",
            "--workspace", self.workspace, "--result", report,
        )
        return result, json.loads(report.read_text(encoding="utf-8"))

    def write_good(self) -> None:
        (self.workspace / "REMEDIATION_REVIEW.md").write_text(
            PASSING_REVIEW, encoding="utf-8"
        )

    def test_baseline_reproduces_six_named_review_failures(self) -> None:
        result, report = self.check("baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 12)
        self.assertEqual(len(report["tests"]["failures"]), 6)

    def test_known_good_review_passes_and_preserves_exact_candidate(self) -> None:
        self.write_good()
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 12)
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(
            report["candidate_scope"]["observed_changes"],
            ["REMEDIATION_REVIEW.md"],
        )
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")

    def test_superficial_approval_is_rejected(self) -> None:
        (self.workspace / "REMEDIATION_REVIEW.md").write_text(
            "# Remediation re-review handoff\n\nEverything looks good. Approved.\n",
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "public_tests_failed")

    def test_missing_rev_002_disposition_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "REMEDIATION_REVIEW.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("REV-002", "second finding"),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_remediated_review.ReminderRemediatedReviewTests.test_review_disposes_rev_002_with_current_evidence",
            report["tests"]["failures"],
        )

    def test_false_current_validation_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "REMEDIATION_REVIEW.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("12/12", "11/12"),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_remediated_review.ReminderRemediatedReviewTests.test_review_records_exact_current_validation",
            report["tests"]["failures"],
        )

    def test_source_edit_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "notifier" / "service.py"
        path.write_text(path.read_text(encoding="utf-8") + "\n# review edit\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")

    def test_historical_review_edit_is_rejected(self) -> None:
        self.write_good()
        path = self.workspace / "REVIEW_HANDOFF.md"
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
        test = self.workspace / "tests" / "test_remediated_review.py"
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
            "candidate", "--task", "reminder-remediated-review",
            "--workspace", self.workspace, "--result", self.workspace / "result.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the candidate workspace", result.stderr)

    def test_original_fixture_remains_unchanged(self) -> None:
        for relative in [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_HANDOFF.md",
            "REVIEW_HANDOFF.md", "TEAM_NOTES.md", "USER_GUIDE.md",
            "RELEASE_HANDOFF.md", "REMEDIATION_REVIEW.md",
            "notifier/service.py", "tests/test_remediated_review.py",
        ]:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (self.workspace / relative).read_bytes(),
                    (FIXTURE / relative).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
