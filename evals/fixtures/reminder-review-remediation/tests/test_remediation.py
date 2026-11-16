"""Trusted checks for remediation after the independent reminder review."""

from dataclasses import fields
from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, Reminder, ReminderService
from notifier.store import ReminderStore


DUE = "2026-11-01T09:00:00Z"


class ReminderReviewRemediationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="reminder-remediation-")
        self.addCleanup(self.temporary.cleanup)
        self.store_path = Path(self.temporary.name) / "reminders.jsonl"
        self.store = ReminderStore(self.store_path)
        self.service = ReminderService(self.store)
        self.handoff = (Path.cwd() / "IMPLEMENTATION_HANDOFF.md").read_text(
            encoding="utf-8"
        )
        self.handoff_lower = self.handoff.lower()

    def assert_handoff_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.handoff_lower]
        self.assertEqual(missing, [], "missing handoff terms: " + ", ".join(missing))

    def test_rev_001_owner_isolation_is_remediated(self) -> None:
        sam = self.service.schedule("sam", "private-sam", DUE, "sam-1")
        lee = self.service.schedule("lee", "private-lee", DUE, "lee-1")
        self.assertEqual(self.service.list_for("sam"), [sam])
        self.assertEqual(self.service.list_for("lee"), [lee])

    def test_rev_002_conflict_message_is_generic(self) -> None:
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

    def test_handoff_has_required_sections_in_order(self) -> None:
        headings = [
            "## Scope and current state", "## Reproduction and diagnosis",
            "## Changed files", "## Validation evidence", "## Remaining state",
            "## Stop and recovery",
        ]
        positions = [self.handoff.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_handoff_maps_both_findings_to_current_remediation(self) -> None:
        self.assert_handoff_terms(
            "REV-001", "High", "owner isolation", 'record["owner"] == owner',
            "REV-002", "Medium", "generic conflict",
            "owner/key pair already has different content", "notifier/service.py",
        )
        source = (Path.cwd() / "notifier" / "service.py").read_text(encoding="utf-8")
        self.assertNotIn("deliberate review-fixture defects", source.lower())

    def test_handoff_records_exact_current_validation(self) -> None:
        self.assert_handoff_terms(
            "python3 -m unittest discover -s tests -v", "12/12", "exit 0",
            "current fixture", "complete diff", "trusted", "candidate tests",
        )

    def test_handoff_preserves_prior_gates_and_requires_new_review(self) -> None:
        self.assert_handoff_terms(
            "REVIEW_HANDOFF.md", "RELEASE_HANDOFF.md", "USER_GUIDE.md",
            "preserved", "historical", "release blocked", "fresh independent review",
            "do not carry", "ready for release review",
        )

    def test_handoff_records_scope_and_unrun_limits(self) -> None:
        self.assert_handoff_terms(
            "IMPLEMENTATION_HANDOFF.md", "only", "no dependency", "no migration",
            "process-safe concurrency", "not run", "live Bob", "not production ready",
        )

    def test_handoff_supports_stale_detection_and_safe_recovery(self) -> None:
        self.assert_handoff_terms(
            "stale", "rerun", "stop if", "permission", "preserve",
            "unrelated work", "independent review", "exact candidate",
        )


if __name__ == "__main__":
    unittest.main()
