"""Current reminder behavior before idempotency support."""

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


class ReminderService:
    def __init__(self, store: ReminderStore) -> None:
        self.store = store

    def schedule(self, owner: str, message: str, due_at: str) -> Reminder:
        datetime.fromisoformat(due_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        reminder = Reminder(str(uuid.uuid4()), owner, message, due_at)
        self.store.append(asdict(reminder))
        return reminder

    def list_for(self, owner: str) -> list[Reminder]:
        return [
            Reminder(**record)
            for record in self.store.records()
            if record["owner"] == owner
        ]
