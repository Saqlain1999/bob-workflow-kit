"""Trusted checks for bounded reminder implementation and recovery."""

from dataclasses import fields
from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, Reminder, ReminderService
from notifier.store import ReminderStore


DUE = "2026-11-01T09:00:00Z"


class ReminderImplementationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="reminder-implementation-")
        self.addCleanup(self.temporary.cleanup)
        self.store_path = Path(self.temporary.name) / "reminders.jsonl"
        self.store = ReminderStore(self.store_path)
        self.service = ReminderService(self.store)

    def test_calls_without_key_still_append_each_time(self) -> None:
        first = self.service.schedule("sam", "review", DUE)
        second = self.service.schedule("sam", "review", DUE)
        self.assertNotEqual(first.reminder_id, second.reminder_id)
        self.assertEqual(len(self.store.records()), 2)

    def test_conflicting_reuse_raises_without_append(self) -> None:
        self.service.schedule("sam", "review", DUE, "request-7")
        with self.assertRaises(IdempotencyConflict):
            self.service.schedule("sam", "changed", DUE, "request-7")
        self.assertEqual(len(self.store.records()), 1)

    def test_existing_record_without_key_remains_readable(self) -> None:
        self.store.append({
            "reminder_id": "legacy-1", "owner": "sam", "message": "legacy",
            "due_at": DUE,
        })
        self.assertEqual(
            self.service.list_for("sam"),
            [Reminder("legacy-1", "sam", "legacy", DUE)],
        )

    def test_handoff_records_current_evidence_and_limits(self) -> None:
        handoff = Path.cwd() / "IMPLEMENTATION_HANDOFF.md"
        self.assertTrue(handoff.is_file(), "IMPLEMENTATION_HANDOFF.md is required")
        text = handoff.read_text(encoding="utf-8")
        for heading in [
            "## Scope and current state", "## Reproduction and diagnosis",
            "## Changed files", "## Validation evidence", "## Remaining state",
            "## Stop and recovery",
        ]:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        for phrase in [
            "AC-1", "AC-2", "AC-3", "AC-4",
            "python3 -m unittest discover -s tests -v",
            "IMPLEMENTATION_CHECKPOINT.md", "stale", "TEAM_NOTES.md",
            "concurrent", "not run", "independent review",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

    def test_invalid_due_at_appends_nothing(self) -> None:
        with self.assertRaises(ValueError):
            self.service.schedule("sam", "review", "not-a-time", "request-7")
        self.assertEqual(self.store.records(), [])

    def test_public_reminder_fields_remain_exact(self) -> None:
        self.assertEqual(
            [field.name for field in fields(Reminder)],
            ["reminder_id", "owner", "message", "due_at"],
        )

    def test_retry_returns_original_without_duplicate(self) -> None:
        first = self.service.schedule("sam", "review", DUE, "request-7")
        second = self.service.schedule("sam", "review", DUE, "request-7")
        self.assertEqual(second, first)
        self.assertEqual(len(self.store.records()), 1)

    def test_retry_survives_new_service_instance(self) -> None:
        first = self.service.schedule("sam", "review", DUE, "request-7")
        resumed = ReminderService(ReminderStore(self.store_path))
        second = resumed.schedule("sam", "review", DUE, "request-7")
        self.assertEqual(second, first)
        self.assertEqual(len(self.store.records()), 1)

    def test_same_key_is_scoped_by_owner(self) -> None:
        first = self.service.schedule("sam", "review", DUE, "request-7")
        second = self.service.schedule("lee", "review", DUE, "request-7")
        self.assertNotEqual(first.reminder_id, second.reminder_id)
        self.assertEqual(len(self.store.records()), 2)

    def test_service_creation_does_not_rewrite_store(self) -> None:
        self.store.append({
            "reminder_id": "legacy-1", "owner": "sam", "message": "legacy",
            "due_at": DUE,
        })
        before = self.store_path.read_bytes()
        ReminderService(ReminderStore(self.store_path))
        self.assertEqual(self.store_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
