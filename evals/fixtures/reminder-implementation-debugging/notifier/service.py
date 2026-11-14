"""Interrupted reminder idempotency implementation."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import uuid

from .store import ReminderStore


@dataclass(frozen=True)
class Reminder:
    reminder_id: str
    owner: str
    message: str
    due_at: str


class IdempotencyConflict(ValueError):
    """The owner/key pair already identifies different reminder content."""


class ReminderService:
    def __init__(self, store: ReminderStore) -> None:
        self.store = store

    def schedule(
        self, owner: str, message: str, due_at: str,
        idempotency_key: str | None = None,
    ) -> Reminder:
        datetime.fromisoformat(due_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        reminder = Reminder(str(uuid.uuid4()), owner, message, due_at)
        record = asdict(reminder)
        if idempotency_key is not None:
            record["_idempotency_key"] = idempotency_key
        self.store.append(record)
        return reminder

    def list_for(self, owner: str) -> list[Reminder]:
        return [
            Reminder(**{name: record[name] for name in Reminder.__dataclass_fields__})
            for record in self.store.records()
            if record["owner"] == owner
        ]
