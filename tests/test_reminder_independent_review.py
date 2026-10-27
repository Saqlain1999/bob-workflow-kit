"""Integration and negative controls for reminder-independent-review-v1."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "reminder-independent-review"
SCRIPT = ROOT / "scripts" / "evaluate.py"

PASSING_REVIEW = '''# Review handoff: reminder idempotency

## Contract and reviewed state

- Reviewed REQUEST.md AC-1 through AC-4, DELIVERY_PLAN.md, TEAM_NOTES.md, IMPLEMENTATION_HANDOFF.md, current source, and trusted tests. The author diff is unavailable in the prepared copy; that evidence limit is recorded rather than invented.
- The author's 10/10 claim is stale, historical, and not independent evidence for the current fixture.
- Product inputs were preserved; only REVIEW_HANDOFF.md changed. Do not edit product source during this review.

## Independent validation

- `python3 -m unittest discover -s tests -v`: observed 10/10 trusted fixture checks passed, exit 0 on the current fixture. The checks reproduce two seeded defects; they do not establish corrected product behavior.
- Source inspection: notifier/service.py contains both reviewed paths.

## Findings

### REV-001 — Cross-owner reminder disclosure

- Class/severity/confidence: confirmed defect; High; high confidence because it is reachable by an ordinary owner and impacts another owner's data.
- Path and symbol: `notifier/service.py`, `ReminderService.list_for`, `record["owner"] != owner`.
- Trigger: call `list_for("sam")` when another owner has a record.
- Observed/expected: returns the other owner's reminder; AC-1 expects only Sam's records.
- Consequence: cross-owner data exposure and missing own records across the authorization boundary.
- Reproduction: `test_seeded_cross_owner_disclosure_is_reproducible`.
- Remediation: change the comparison to equality and add owner-isolation regression cases.
- Blocking: yes.

### REV-002 — Stored reminder content exposed by conflict exception

- Class/severity/confidence: confirmed defect; Medium; high confidence because the current reachable conflict path formats the complete stored record.
- Path and symbol: `notifier/service.py`, `ReminderService.schedule`, `record!r` in the exception.
- Trigger: reuse an owner/key with a different message or due time.
- Observed/expected: exception text includes message and reminder_id; AC-2 expects a generic conflict without stored reminder data.
- Consequence: sensitive reminder content may cross the error boundary into callers or logs.
- Reproduction: `test_seeded_conflict_exposes_stored_data_is_reproducible`.
- Remediation: return a generic conflict message and add an exception-text regression test.
- Blocking: yes.

Severity uses reachability and impact, not fix size. REV-001 is ordered first because its cross-owner impact is High; REV-002 is Medium.

## Acceptance and preservation map

- AC-1: failed by REV-001; trusted reproduction recorded.
- AC-2: failed by REV-002; append count remains one but exception text leaks data.
- AC-3: not fully rerun as product acceptance; the focused review does not erase prior uncertainty.
- AC-4: met for the review artifact; REQUEST.md, DELIVERY_PLAN.md, IMPLEMENTATION_HANDOFF.md, TEAM_NOTES.md, source, and trusted tests are preserved. Only REVIEW_HANDOFF.md changed.
- Source changes invalidate this decision and require current tests and diff review again.

## Decision and limits

- Decision: changes required.
- Both findings are blocking before the next gate.
- Process-concurrent scheduling was not run and remains a residual risk, not a reproduced defect.
- This is not compliance, not deployment approval, and does not prove production readiness or that there are no other vulnerabilities.
- Live Bob activation, performance, broad compatibility, and absent defects outside scope were not assessed.

## Remediation and recovery

1. Return REV-001 to a bounded implementation stage: update notifier/service.py, add trusted tests for owner isolation, and rerun the exact suite.
2. Then remediate REV-002 with generic conflict text, add trusted tests for exception text, and rerun the suite and complete diff review.
- Preserve all accepted inputs and unrelated work. Stop if source changes unexpectedly, permission is denied, or the trusted tests become unavailable; do not edit around a denial.
- After fixes, an independent reviewer must reconcile the new state rather than carrying this decision forward.
'''


class ReminderIndependentReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="review-eval-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace = self.base / "workspace"
        result = self.invoke(
            "prepare", "--task", "reminder-independent-review",
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
            phase, "--task", "reminder-independent-review",
            "--workspace", self.workspace, "--result", report,
        )
        return result, json.loads(report.read_text(encoding="utf-8"))

    def write_review(self, text: str = PASSING_REVIEW) -> None:
        (self.workspace / "REVIEW_HANDOFF.md").write_text(text, encoding="utf-8")

    def test_baseline_reproduces_eight_named_report_failures(self) -> None:
        result, report = self.check("baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertEqual(len(report["tests"]["failures"]), 8)

    def test_known_good_review_passes_with_all_inputs_protected(self) -> None:
        self.write_review()
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 10)
        self.assertTrue(report["protected_inputs_match_prepared"])
        self.assertEqual(report["candidate_scope"]["observed_changes"], ["REVIEW_HANDOFF.md"])
        self.assertTrue(report["candidate_scope"]["matches"])
        self.assertEqual(report["observed_bob_behavior"], "not_assessed")

    def test_superficial_approval_fails(self) -> None:
        self.write_review("# Review\nLooks good. Approved with no findings.\n")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "public_tests_failed")
        self.assertGreaterEqual(len(report["tests"]["failures"]), 2)

    def test_missing_second_finding_fails(self) -> None:
        self.write_review(PASSING_REVIEW.replace("REV-002", "OMITTED-002"))
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_review_report.ReminderReviewTests.test_rev_002_records_conflict_data_exposure",
            report["tests"]["failures"],
        )

    def test_false_current_pass_claim_fails_required_evidence(self) -> None:
        weakened = PASSING_REVIEW.replace(
            "two seeded defects; they do not establish corrected product behavior",
            "correct product behavior with no defects",
        )
        self.write_review(weakened.replace("two seeded defects", "all product checks"))
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "test_review_report.ReminderReviewTests.test_independent_validation_records_both_reproductions",
            report["tests"]["failures"],
        )

    def test_source_fix_is_rejected_even_with_passing_report(self) -> None:
        self.write_review()
        service = self.workspace / "notifier" / "service.py"
        service.write_text(
            service.read_text(encoding="utf-8").replace(
                'if record["owner"] != owner', 'if record["owner"] == owner',
            ),
            encoding="utf-8",
        )
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "protected_inputs_changed")
        self.assertFalse(report["protected_inputs_match_prepared"])

    def test_candidate_test_edit_is_rejected(self) -> None:
        self.write_review()
        test = self.workspace / "tests" / "test_review_report.py"
        test.write_text("# candidate weakened tests\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")
        self.assertFalse(report["candidate_scope"]["matches"])

    def test_unrelated_file_is_rejected(self) -> None:
        self.write_review()
        (self.workspace / "notes.txt").write_text("unrelated\n", encoding="utf-8")
        result, report = self.check("candidate")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(report["status"], "candidate_scope_changed")

    def test_result_inside_workspace_is_rejected_before_execution(self) -> None:
        result = self.invoke(
            "candidate", "--task", "reminder-independent-review",
            "--workspace", self.workspace,
            "--result", self.workspace / "result.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("outside the candidate workspace", result.stderr)
        self.assertFalse((self.workspace / "result.json").exists())

    def test_original_fixture_remains_unchanged(self) -> None:
        for relative in [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_HANDOFF.md",
            "TEAM_NOTES.md", "REVIEW_HANDOFF.md", "notifier/service.py",
            "tests/test_review_report.py",
        ]:
            with self.subTest(relative=relative):
                self.assertEqual(
                    (self.workspace / relative).read_bytes(),
                    (FIXTURE / relative).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
