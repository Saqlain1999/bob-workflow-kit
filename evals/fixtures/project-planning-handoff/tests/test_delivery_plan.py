"""Public checks for the bounded requirements/architecture handoff."""

from pathlib import Path
import re
import unittest


PLAN = Path.cwd() / "DELIVERY_PLAN.md"


def _text() -> str:
    return PLAN.read_text(encoding="utf-8")


class DeliveryPlanTests(unittest.TestCase):
    def test_required_sections_are_present_in_order(self) -> None:
        headings = re.findall(r"^##\s+(.+?)\s*$", _text(), flags=re.MULTILINE)
        self.assertEqual(headings, [
            "Request and boundary", "Repository evidence", "Acceptance criteria",
            "Architecture decision", "Implementation slices", "Risks and handoffs",
            "Durable checkpoint", "Evidence limits",
        ])

    def test_request_constraints_and_non_goals_are_preserved(self) -> None:
        text = _text()
        for phrase in [
            "Python standard library", "Reminder", "old records", "do not implement",
            "rewrite the store during startup",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

    def test_repository_evidence_names_current_files_and_observations(self) -> None:
        text = _text()
        paths = ["REQUEST.md", "notifier/service.py", "notifier/store.py", "project-tests.md"]
        self.assertEqual([path for path in paths if path not in text], [])
        self.assertGreaterEqual(len(re.findall(r"\bObserved\b", text)), 4)
        self.assertIn("append", text)
        self.assertIn("newline-delimited JSON", text)

    def test_four_acceptance_criteria_cover_behavior_and_compatibility(self) -> None:
        text = _text().split("## Acceptance criteria", 1)[1].split("## Architecture decision", 1)[0]
        ids = re.findall(r"\bAC-[1-4]\b", text)
        for identifier in ["AC-1", "AC-2", "AC-3", "AC-4"]:
            self.assertIn(identifier, ids)
        for phrase in [
            "same owner", "same key", "original reminder", "IdempotencyConflict",
            "different owners", "new service instance", "existing records",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

    def test_architecture_compares_two_options_and_selects_one(self) -> None:
        text = _text()
        self.assertRegex(text, r"(?im)^.*Option A.*$")
        self.assertRegex(text, r"(?im)^.*Option B.*$")
        self.assertRegex(text, r"(?im)^.*Selected (option|design).*$")
        for concept in ["compatibility", "rollback", "revisit"]:
            self.assertIn(concept, text.lower())

    def test_slices_trace_every_criterion_to_files_and_validation(self) -> None:
        text = _text()
        slices = text.split("## Implementation slices", 1)[1].split("## Risks and handoffs", 1)[0]
        identifiers = ["AC-1", "AC-2", "AC-3", "AC-4"]
        self.assertEqual([identifier for identifier in identifiers if identifier not in slices], [])
        self.assertIn("notifier/service.py", slices)
        self.assertIn("notifier/store.py", slices)
        self.assertIn("tests/", slices)
        self.assertIn("python3 -m unittest discover -s tests -v", slices)

    def test_risks_cover_conflict_data_compatibility_and_preservation(self) -> None:
        section = _text().split("## Risks and handoffs", 1)[1].split("## Durable checkpoint", 1)[0]
        phrases = ["concurrent", "partial", "existing records", "unrelated work"]
        self.assertEqual([phrase for phrase in phrases if phrase not in section.lower()], [])

    def test_checkpoint_supports_stale_detection_resume_and_abort(self) -> None:
        section = _text().split("## Durable checkpoint", 1)[1].split("## Evidence limits", 1)[0]
        phrases = [
            "inspected state", "first safe implementation action", "commands still to run",
            "stale", "resume", "abort",
        ]
        self.assertEqual([phrase for phrase in phrases if phrase not in section.lower()], [])

    def test_unknowns_and_stop_conditions_remain_explicit(self) -> None:
        text = _text()
        self.assertRegex(text, r"(?im)^.*Unknown.*$")
        self.assertIn("stop", text.lower())
        self.assertIn("approval", text.lower())

    def test_evidence_limit_does_not_claim_future_success(self) -> None:
        section = _text().split("## Evidence limits", 1)[1]
        for phrase in ["does not prove", "implementation", "tests", "live"]:
            self.assertIn(phrase, section.lower())
