"""Trusted checks for the bounded reminder release handoff."""

from pathlib import Path
import tempfile
import unittest

from notifier import IdempotencyConflict, ReminderService
from notifier.store import ReminderStore

DUE = "2026-11-01T09:00:00Z"


class ReminderReleaseHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path.cwd()
        self.release = (root / "RELEASE_HANDOFF.md").read_text(encoding="utf-8")
        self.guide = (root / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.release_lower = self.release.lower()
        self.guide_lower = self.guide.lower()

    def assert_release_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.release_lower]
        self.assertEqual(missing, [], "missing release terms: " + ", ".join(missing))

    def assert_guide_terms(self, *terms: str) -> None:
        missing = [term for term in terms if term.lower() not in self.guide_lower]
        self.assertEqual(missing, [], "missing guide terms: " + ", ".join(missing))

    def test_seeded_cross_owner_disclosure_remains_reproducible(self) -> None:
        with tempfile.TemporaryDirectory(prefix="release-owner-") as directory:
            service = ReminderService(ReminderStore(Path(directory) / "reminders.jsonl"))
            service.schedule("sam", "private-sam", DUE, "sam-1")
            lee = service.schedule("lee", "private-lee", DUE, "lee-1")
            self.assertEqual(service.list_for("sam"), [lee])

    def test_seeded_conflict_exposure_remains_reproducible(self) -> None:
        with tempfile.TemporaryDirectory(prefix="release-conflict-") as directory:
            store = ReminderStore(Path(directory) / "reminders.jsonl")
            service = ReminderService(store)
            original = service.schedule("sam", "quarterly-secret", DUE, "request-7")
            with self.assertRaises(IdempotencyConflict) as caught:
                service.schedule("sam", "changed", DUE, "request-7")
            self.assertIn("quarterly-secret", str(caught.exception))
            self.assertIn(original.reminder_id, str(caught.exception))

    def test_release_handoff_has_required_sections_in_order(self) -> None:
        headings = [
            "## Candidate and contract", "## Documentation changes",
            "## Acceptance and review disposition", "## Validation evidence",
            "## Release decision and limits", "## Recovery and next gate",
        ]
        positions = [self.release.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_user_guide_has_required_sections_in_order(self) -> None:
        headings = [
            "## Availability", "## Intended behavior", "## Known blocking issues",
            "## Operator guidance", "## Evidence limits",
        ]
        positions = [self.guide.find(heading) for heading in headings]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_candidate_state_and_stale_evidence(self) -> None:
        self.assert_release_terms(
            "current fixture", "complete diff", "IMPLEMENTATION_HANDOFF.md",
            "REVIEW_HANDOFF.md", "stale", "10/10", "not release evidence",
            "notifier/service.py",
        )

    def test_acceptance_and_finding_disposition(self) -> None:
        self.assert_release_terms(
            "AC-1", "AC-2", "AC-3", "AC-4", "REV-001", "High",
            "REV-002", "Medium", "unresolved", "blocking",
        )

    def test_current_validation_is_bounded(self) -> None:
        self.assert_release_terms(
            "python3 -m unittest discover -s tests -v", "12/12", "exit 0",
            "reproduce two seeded defects", "do not establish corrected",
            "live Bob", "not run",
        )

    def test_exact_blocked_decision_and_no_publication(self) -> None:
        self.assert_release_terms(
            "decision: release blocked", "no tag", "no artifact", "no deployment",
            "no announcement", "do not publish",
        )
        self.assertNotIn("decision: ready for release review", self.release_lower)

    def test_release_status_and_claim_limits(self) -> None:
        self.assert_release_terms(
            "not production ready", "not deployment approval", "not compliance",
            "does not prove", "compatibility", "performance",
        )

    def test_documentation_records_unreleased_behavior(self) -> None:
        self.assert_guide_terms(
            "unreleased", "do not deploy", "intended behavior", "AC-1", "AC-2",
            "REV-001", "REV-002", "release blocked",
        )
        self.assertNotIn("ready for production", self.guide_lower)

    def test_known_issues_preserve_security_boundaries(self) -> None:
        self.assert_guide_terms(
            "cross-owner", "data exposure", "conflict", "stored reminder",
            "do not use", "private", "no safe upgrade", "no rollback artifact",
        )

    def test_recovery_returns_to_implementation_and_review(self) -> None:
        self.assert_release_terms(
            "implementation stage", "owner isolation", "generic conflict",
            "trusted regression", "independent review", "rerun", "stop if",
            "permission", "preserve",
        )


if __name__ == "__main__":
    unittest.main()
