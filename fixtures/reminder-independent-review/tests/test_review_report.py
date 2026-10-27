"""Trusted checks for the bounded independent-review handoff."""

from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, ReminderService
from notifier.store import ReminderStore


DUE = "2026-11-01T09:00:00Z"


class ReminderReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="reminder-review-")
        self.addCleanup(self.temporary.cleanup)
        self.store = ReminderStore(Path(self.temporary.name) / "reminders.jsonl")
        self.service = ReminderService(self.store)
        self.report = (Path.cwd() / "REVIEW_HANDOFF.md").read_text(encoding="utf-8")
        self.lower = self.report.lower()

    def assert_report_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.lower]
        self.assertEqual(missing, [], "missing review terms: " + ", ".join(missing))

    def test_seeded_cross_owner_disclosure_is_reproducible(self) -> None:
        self.service.schedule("sam", "private-sam", DUE, "sam-1")
        lee = self.service.schedule("lee", "private-lee", DUE, "lee-1")
        self.assertEqual(self.service.list_for("sam"), [lee])

    def test_seeded_conflict_exposes_stored_data_is_reproducible(self) -> None:
        original = self.service.schedule("sam", "quarterly-secret", DUE, "request-7")
        with self.assertRaises(IdempotencyConflict) as caught:
            self.service.schedule("sam", "changed", DUE, "request-7")
        message = str(caught.exception)
        self.assertIn("quarterly-secret", message)
        self.assertIn(original.reminder_id, message)
        self.assertEqual(len(self.store.records()), 1)

    def test_review_handoff_has_required_sections_in_order(self) -> None:
        headings = [
            "## Contract and reviewed state", "## Independent validation",
            "## Findings", "## Acceptance and preservation map",
            "## Decision and limits", "## Remediation and recovery",
        ]
        positions = [self.report.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_current_state_and_stale_author_evidence(self) -> None:
        self.assert_report_terms(
            "IMPLEMENTATION_HANDOFF.md", "stale", "current", "10/10",
            "not independent", "notifier/service.py", "diff is unavailable",
        )

    def test_rev_001_records_cross_owner_disclosure(self) -> None:
        self.assert_report_terms(
            "REV-001", "confirmed defect", "high", "high confidence",
            "ReminderService.list_for", 'record["owner"] != owner',
            "cross-owner", "data exposure", "AC-1",
            "test_seeded_cross_owner_disclosure_is_reproducible",
            "change the comparison", "blocking",
        )

    def test_rev_002_records_conflict_data_exposure(self) -> None:
        self.assert_report_terms(
            "REV-002", "confirmed defect", "medium", "high confidence",
            "ReminderService.schedule", "record!r", "exception",
            "message", "reminder_id", "AC-2",
            "test_seeded_conflict_exposes_stored_data_is_reproducible",
            "generic conflict", "blocking",
        )

    def test_independent_validation_records_both_reproductions(self) -> None:
        self.assert_report_terms(
            "python3 -m unittest discover -s tests -v", "10/10", "exit 0",
            "two seeded defects", "current fixture", "trusted",
        )

    def test_decision_severity_and_limits(self) -> None:
        self.assert_report_terms(
            "decision: changes required", "high", "medium",
            "reachability", "impact", "process-concurrent", "not run",
            "not compliance", "not deployment approval", "does not prove",
            "no other vulnerabilities",
        )

    def test_acceptance_preservation_and_recovery_map(self) -> None:
        self.assert_report_terms(
            "AC-1", "AC-2", "AC-3", "AC-4", "REQUEST.md",
            "DELIVERY_PLAN.md", "TEAM_NOTES.md", "preserved",
            "only REVIEW_HANDOFF.md", "source changes invalidate",
        )

    def test_remediation_handoff_is_bounded_and_ordered(self) -> None:
        rev_001 = self.report.find("REV-001")
        rev_002 = self.report.find("REV-002")
        self.assertGreaterEqual(rev_001, 0)
        self.assertGreater(rev_002, rev_001)
        self.assert_report_terms(
            "implementation stage", "notifier/service.py", "trusted tests",
            "owner isolation", "exception text", "rerun",
            "stop if", "permission", "do not edit",
        )


if __name__ == "__main__":
    unittest.main()
