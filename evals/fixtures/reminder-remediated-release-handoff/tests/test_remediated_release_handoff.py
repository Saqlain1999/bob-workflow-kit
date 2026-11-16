"""Trusted checks for release preparation after remediation and re-review."""

from dataclasses import fields
from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, Reminder, ReminderService
from notifier.store import ReminderStore


DUE = "2026-11-01T09:00:00Z"


class ReminderRemediatedReleaseHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="reminder-release-ready-")
        self.addCleanup(self.temporary.cleanup)
        self.store_path = Path(self.temporary.name) / "reminders.jsonl"
        self.store = ReminderStore(self.store_path)
        self.service = ReminderService(self.store)
        self.guide = (Path.cwd() / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.guide_lower = self.guide.lower()
        self.handoff = (Path.cwd() / "RELEASE_READINESS_HANDOFF.md").read_text(
            encoding="utf-8"
        )
        self.handoff_lower = self.handoff.lower()

    def assert_guide_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.guide_lower]
        self.assertEqual(missing, [], "missing guide terms: " + ", ".join(missing))

    def assert_handoff_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.handoff_lower]
        self.assertEqual(missing, [], "missing handoff terms: " + ", ".join(missing))

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

    def test_user_guide_has_required_sections_in_order(self) -> None:
        headings = [
            "## Availability", "## Current behavior", "## Operator guidance",
            "## Evidence limits",
        ]
        positions = [self.guide.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_user_guide_records_current_unreleased_behavior(self) -> None:
        self.assert_guide_terms(
            "unreleased", "owner isolation", "generic conflict",
            "same owner", "idempotency key", "no release artifact",
            "not deploy", "ready for release review",
        )
        self.assertNotIn("unresolved high", self.guide_lower)
        self.assertNotIn("release blocked", self.guide_lower)

    def test_handoff_has_required_sections_in_order(self) -> None:
        headings = [
            "## Candidate and evidence", "## Documentation and operations",
            "## Acceptance and finding disposition", "## Validation evidence",
            "## Release decision and limits", "## Recovery and next gate",
        ]
        positions = [self.handoff.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_current_review_supersedes_but_preserves_historical_gates(self) -> None:
        self.assert_handoff_terms(
            "REMEDIATION_REVIEW.md", "current", "ready for release preparation",
            "REVIEW_HANDOFF.md", "RELEASE_HANDOFF.md", "historical",
            "preserved", "not current conclusions",
        )

    def test_acceptance_and_findings_are_disposed(self) -> None:
        self.assert_handoff_terms(
            "AC-1", "AC-2", "AC-3", "AC-4", "REV-001", "High",
            "resolved", "REV-002", "Medium", "owner isolation",
            "generic conflict", "no open blocking finding",
        )

    def test_exact_current_validation_is_bounded(self) -> None:
        self.assert_handoff_terms(
            "python3 -m unittest discover -s tests -v", "12/12", "exit 0",
            "exact candidate", "complete diff", "trusted tests unchanged",
            "finite public checks", "not a general security proof",
        )

    def test_documentation_operations_and_rollback_are_truthful(self) -> None:
        self.assert_handoff_terms(
            "USER_GUIDE.md", "only", "RELEASE_READINESS_HANDOFF.md",
            "no release artifact", "no migration", "no rollback artifact",
            "previous supported version", "removal",
        )

    def test_exact_ready_for_review_decision_and_no_publication(self) -> None:
        self.assert_handoff_terms(
            "Decision: ready for release review", "does not authorize",
            "tag", "artifact", "deployment", "publication", "announcement",
        )
        self.assertNotIn("decision: ready for release\n", self.handoff_lower)
        self.assertNotIn("decision: release approved", self.handoff_lower)

    def test_claim_limits_remain_explicit(self) -> None:
        self.assert_handoff_terms(
            "process-safe concurrency", "not run", "production readiness",
            "compatibility", "performance", "compliance", "live Bob",
            "not established",
        )

    def test_stale_detection_stop_and_recovery_are_explicit(self) -> None:
        self.assert_handoff_terms(
            "stale", "source", "environment", "rerun", "stop if",
            "permission", "protected", "unrelated work", "return to",
            "implementation", "independent review", "release preparation",
        )


if __name__ == "__main__":
    unittest.main()
