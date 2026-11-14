"""Load the workspace's delivery policy without caching it."""

import json
from pathlib import Path


def read_policy():
    path = Path(__file__).resolve().parents[1] / "policy.json"
    return json.loads(path.read_text(encoding="utf-8"))
