"""Tiny append-only JSONL store used by the public fixture."""

import json
from pathlib import Path


class ReminderStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def records(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]

    def append(self, record: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(record, sort_keys=True) + "\n")
