"""Deliberately incomplete local adapter for the bob-project-memory-v1 task."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class RevisionConflict(RuntimeError):
    pass


class BackendUnavailable(RuntimeError):
    pass


class ProjectMemory:
    """A tiny file-backed adapter whose starting implementation has known gaps."""

    def __init__(self, root: Path, backend_available: bool = True) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "memory.json"
        self.temporary_path = self.root / "memory.json.tmp"
        self.backend_available = backend_available
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.state_path.exists():
            return {"records": {}, "history": {}, "index": []}
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self.state_path.write_text(
            json.dumps(self._data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _validate_identifier(value: str) -> None:
        if not value:
            raise ValueError("identifier must not be empty")

    @classmethod
    def _storage_key(cls, project: str, key: str) -> str:
        cls._validate_identifier(project)
        cls._validate_identifier(key)
        return key

    def put(
        self,
        project: str,
        key: str,
        value: str,
        source_hash: str,
        expected_revision: Optional[int] = None,
    ) -> Dict[str, Any]:
        storage_key = self._storage_key(project, key)
        previous = self._data["records"].get(storage_key)
        revision = 1 if previous is None else int(previous["revision"]) + 1
        record = {
            "project": project,
            "key": key,
            "value": value,
            "source_hash": source_hash,
            "revision": revision,
            "trust": "trusted",
        }
        self._data["records"][storage_key] = record
        self._data["history"][storage_key] = [record]
        if storage_key not in self._data["index"]:
            self._data["index"].append(storage_key)
        self._save()
        return dict(record)

    def recall(
        self, project: str, key: str, current_source_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        storage_key = self._storage_key(project, key)
        record = self._data["records"].get(storage_key)
        if record is None:
            return {"status": "missing", "repository_evidence": "projects/" + project + "/EVIDENCE.md"}
        result = dict(record)
        result["status"] = "current"
        return result

    def history(self, project: str, key: str) -> List[Dict[str, Any]]:
        storage_key = self._storage_key(project, key)
        return [dict(item) for item in self._data["history"].get(storage_key, [])]

    def promote(
        self, project: str, key: str, sanitized_summary: str
    ) -> Dict[str, Any]:
        source = self.recall(project, key)
        return self.put(
            "shared-lessons", key, source.get("value", ""),
            source.get("source_hash", "unknown"),
        )

    def delete(self, project: str, key: str) -> None:
        storage_key = self._storage_key(project, key)
        self._data["records"].pop(storage_key, None)
        self._save()

    def list_project(self, project: str) -> List[str]:
        prefix = project + ":"
        return sorted(item[len(prefix):] if item.startswith(prefix) else item for item in self._data["index"])
