"""Public checks for the bounded runbook fidelity contract."""

import json
from pathlib import Path
import re
import unittest


FIXTURE = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((FIXTURE / "contract.json").read_text(encoding="utf-8"))
RUNBOOK = Path.cwd() / "RUNBOOK.md"


def _text() -> str:
    return RUNBOOK.read_text(encoding="utf-8")


def _requirement_line(text: str, token: str) -> str:
    lines = [line.strip() for line in text.splitlines() if token in line]
    if len(lines) != 1:
        raise AssertionError(f"expected exactly one line containing {token!r}; found {len(lines)}")
    return lines[0]


class RunbookFidelityTests(unittest.TestCase):
    def test_required_sections_are_present(self) -> None:
        headings = re.findall(r"^##\s+(.+?)\s*$", _text(), flags=re.MULTILINE)
        self.assertEqual(headings, ["Purpose", "Before you begin", "Procedure", "Recovery and ownership"])

    def test_procedure_has_four_ordered_steps(self) -> None:
        text = _text()
        procedure = text.split("## Procedure", 1)[-1].split("## Recovery and ownership", 1)[0]
        steps = re.findall(r"^(\d+)\.\s+(.+)$", procedure, flags=re.MULTILINE)
        self.assertEqual([number for number, _ in steps], ["1", "2", "3", "4"])
        positions = [procedure.index(f"`{command}`") for command in CONTRACT["commands_in_order"]]
        self.assertEqual(positions, sorted(positions))

    def test_exact_tokens_are_preserved_once(self) -> None:
        text = _text()
        for token, count in CONTRACT["exact_token_counts"].items():
            with self.subTest(token=token):
                self.assertEqual(text.count(token), count)

    def test_commands_are_preserved_once_and_in_order(self) -> None:
        text = _text()
        positions = []
        for command in CONTRACT["commands_in_order"]:
            rendered = f"`{command}`"
            with self.subTest(command=command):
                self.assertEqual(text.count(rendered), 1)
            positions.append(text.index(rendered))
        self.assertEqual(positions, sorted(positions))

    def test_backup_is_mandatory_and_precedes_migration(self) -> None:
        text = _text()
        backup = _requirement_line(text, CONTRACT["commands_in_order"][0])
        self.assertRegex(backup, r"\bMUST\b")
        self.assertLess(
            text.index(CONTRACT["commands_in_order"][0]),
            text.index(CONTRACT["commands_in_order"][1]),
        )

    def test_connection_retry_keeps_permission_limit_condition_and_wait(self) -> None:
        line = _requirement_line(_text(), "E_CONN_RESET")
        self.assertRegex(line, r"\bMAY\b")
        self.assertRegex(line.lower(), r"\bonly if\b")
        self.assertRegex(line.lower(), r"\bonce\b")
        self.assertIn("30 s", line)

    def test_authentication_failure_keeps_retry_prohibition(self) -> None:
        line = _requirement_line(_text(), "E_AUTH_DENIED")
        self.assertRegex(line, r"\bMUST NOT\b")
        self.assertRegex(line.lower(), r"\bretr(?:y|ied)\b")

    def test_cleanup_remains_blocked_until_verification_succeeds(self) -> None:
        line = _requirement_line(_text(), CONTRACT["commands_in_order"][3])
        self.assertRegex(line, r"\bMUST NOT\b")
        self.assertRegex(line.lower(), r"\buntil\b")
        self.assertRegex(line.lower(), r"\bverification succeeds\b")


if __name__ == "__main__":
    unittest.main()
