"""Trusted checks for independent review of the remediated reminder state."""

from dataclasses import fields
from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, Reminder, ReminderService
from notifier.store import ReminderStore


DUE = "2026-11-01T09:00:00Z"


class ReminderRemediatedReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="reminder-rereview-")
        self.addCleanup(self.temporary.cleanup)
        self.store_path = Path(self.temporary.name) / "reminders.jsonl"
        self.store = ReminderStore(self.store_path)
        self.service = ReminderService(self.store)
        self.review = (Path.cwd() / "REMEDIATION_REVIEW.md").read_text(
            encoding="utf-8"
        )
        self.review_lower = self.review.lower()

    def assert_review_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.review_lower]
        self.assertEqual(missing, [], "missing review terms: " + ", ".join(missing))

    def test_rev_001_owner_isolation_remains_fixed(self) -> None:
        sam = self.service.schedule("sam", "private-sam", DUE, "sam-1")
        lee = self.service.schedule("lee", "private-lee", DUE, "lee-1")
        self.assertEqual(self.service.list_for("sam"), [sam])
        self.assertEqual(self.service.list_for("lee"), [lee])

    def test_rev_002_conflict_message_remains_generic(self) -> None:
        original = self.service.schedule("sam", "quarterly-secret", DUE, "request-7")
        with self.assertRaises(IdempotencyConflict) as caught:
            self.service.schedule("sam", "changed", DUE, "request-7")
        self.assertEqual(str(caught.exception), "owner/key pair already has different content")
        self.assertNotIn("quarterly-secret", str(caught.exception))
        self.assertNotIn(original.reminder_id, str(caught.exception))

    def test_conflicting_reuse_appends_nothing(self) -> None:
        self.service.schedule("sam", "review", DUE, "request-7")
        with self.assertRaises(IdempotencyConflict):
            self.service.schedule("sam", "changed", DUE, "request-7")
        self.assertEqual(len(self.store.records()), 1)

    def test_same_content_retry_survives_restart(self) -> None:
        first = self.service.schedule("sam", "review", DUE, "request-7")
        resumed = ReminderService(ReminderStore(self.store_path))
        self.assertEqual(resumed.schedule("sam", "review", DUE, "request-7"), first)
        self.assertEqual(len(self.store.records()), 1)

    def test_same_key_remains_isolated_by_owner(self) -> None:
        first = self.service.schedule("sam", "review", DUE, "request-7")
        second = self.service.schedule("lee", "review", DUE, "request-7")
        self.assertNotEqual(first.reminder_id, second.reminder_id)
        self.assertEqual(len(self.store.records()), 2)

    def test_compatibility_and_public_contract_are_preserved(self) -> None:
        first = self.service.schedule("sam", "review", DUE)
        second = self.service.schedule("sam", "review", DUE)
        self.assertNotEqual(first.reminder_id, second.reminder_id)
        self.store.append({
            "reminder_id": "legacy-1", "owner": "sam", "message": "legacy",
            "due_at": DUE,
        })
        self.assertIn(Reminder("legacy-1", "sam", "legacy", DUE), self.service.list_for("sam"))
        with self.assertRaises(ValueError):
            self.service.schedule("sam", "invalid", "not-a-time", "invalid-1")
        self.assertEqual(
            [field.name for field in fields(Reminder)],
            ["reminder_id", "owner", "message", "due_at"],
        )

    def test_review_has_required_sections_in_order(self) -> None:
        headings = [
            "## Reviewed state and evidence", "## Finding dispositions",
            "## Validation evidence", "## Decision and limits",
            "## Recovery and next gate",
        ]
        positions = [self.review.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_review_disposes_rev_001_with_current_evidence(self) -> None:
        self.assert_review_terms(
            "REV-001", "High", "resolved", "owner isolation",
            'record["owner"] == owner', "test_rev_001_owner_isolation_remains_fixed",
        )

    def test_review_disposes_rev_002_with_current_evidence(self) -> None:
        self.assert_review_terms(
            "REV-002", "Medium", "resolved", "generic conflict",
            "owner/key pair already has different content",
            "test_rev_002_conflict_message_remains_generic",
        )

    def test_review_records_exact_current_validation(self) -> None:
        self.assert_review_terms(
            "python3 -m unittest discover -s tests -v", "12/12", "exit 0",
            "exact candidate", "complete remediation diff", "candidate tests",
        )

    def test_review_decision_preserves_limits(self) -> None:
        self.assert_review_terms(
            "ready for release preparation", "not release approval",
            "no new blocking finding", "bounded reviewed scope",
            "process-safe concurrency", "not run", "security proof",
            "production readiness", "live Bob",
        )
        self.assertNotIn("ready for release review", self.review_lower)

    def test_review_supports_stale_detection_and_safe_recovery(self) -> None:
        self.assert_review_terms(
            "REVIEW_HANDOFF.md", "RELEASE_HANDOFF.md", "historical",
            "preserved", "stale", "rerun", "stop if", "permission",
            "protected", "unrelated work", "release preparation",
        )


if __name__ == "__main__":
    unittest.main()
