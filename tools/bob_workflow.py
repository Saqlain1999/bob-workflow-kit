#!/usr/bin/env python3
"""Install a small rules/skills payload without executing Bob or editing settings.

All filesystem operations receive an explicit Bob configuration root. Only the
CLI resolves the user's default home. Upgrades deliberately require uninstalling
the unchanged previous installation first; unowned or edited files are never
overwritten. An interrupted initial install leaves a journal that ``uninstall``
can roll back after the user has stopped any still-running installer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from typing import Any


VERSION = "0.1.0-alpha.7"
SCHEMA_VERSION = 1
METADATA = "workflow-kit"
MANIFEST = f"{METADATA}/manifest.json"
JOURNAL = f"{METADATA}/journal.json"
RULE = "rules/bob-workflow-kit.md"
SKILL = "skills/work-large-codebase/SKILL.md"
TECHNICAL_COMMUNICATION_SKILL = "skills/write-clear-technical-content/SKILL.md"
PROJECT_PLANNING_SKILL = "skills/plan-project-change/SKILL.md"
IMPLEMENTATION_SKILL = "skills/implement-and-debug-change/SKILL.md"
REVIEW_SKILL = "skills/review-and-secure-change/SKILL.md"
RELEASE_SKILL = "skills/document-and-prepare-release/SKILL.md"
SKILLS = {
    "work-large-codebase": SKILL,
    "write-clear-technical-content": TECHNICAL_COMMUNICATION_SKILL,
    "plan-project-change": PROJECT_PLANNING_SKILL,
    "implement-and-debug-change": IMPLEMENTATION_SKILL,
    "review-and-secure-change": REVIEW_SKILL,
    "document-and-prepare-release": RELEASE_SKILL,
}
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_METADATA_BYTES = 1024 * 1024


class KitError(Exception):
    def __init__(self, code: str, message: str, *, paths: list[str] | None = None,
                 details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.paths = paths or []
        self.details = details or {}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _redirected(info: os.stat_result) -> bool:
    # Junctions and other Windows reparse points need not be S_ISLNK.
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _root(path: Path) -> Path:
    """Validate an explicitly supplied root; never infer a user home here."""
    path = Path(path)
    if not path.is_absolute():
        raise KitError("invalid_target", "The Bob configuration root must be absolute.")
    info = _lstat(path)
    if info and _redirected(info):
        raise KitError("symlink_target", "Pass a real directory, not a symlink or reparse point, as --bob-home.")
    if info and not stat.S_ISDIR(info.st_mode):
        raise KitError("invalid_target", "The Bob configuration root is not a directory.")
    resolved = path.resolve()
    if resolved == Path(resolved.anchor):
        raise KitError("invalid_target", "A filesystem root cannot be a Bob configuration root.")
    return resolved


def _relative(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise KitError("invalid_path", "A managed path must be a nonempty relative string.")
    path = PurePosixPath(value)
    if (path.is_absolute() or str(path) != value or
            any(part in (".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", part)
                for part in path.parts)):
        raise KitError("invalid_path", "Unsafe managed path.", paths=[value])
    return path


def _payload_path(value: str) -> PurePosixPath:
    path = _relative(value)
    allowed = value == RULE
    if len(path.parts) >= 3 and path.parts[0] == "skills" and path.parts[1] in SKILLS:
        allowed |= len(path.parts) == 3 and path.parts[2] == "SKILL.md"
        allowed |= len(path.parts) >= 4 and path.parts[2] in ("references", "templates")
    if not allowed:
        raise KitError("invalid_path", "Path is outside this kit's managed payload.", paths=[value])
    return path


def _checked(root: Path, value: str, *, directory: bool = False) -> Path:
    """Reject symlinked managed paths and non-directory parent components."""
    relative = _relative(value)
    root_info = _lstat(root)
    if root_info and (_redirected(root_info) or not stat.S_ISDIR(root_info.st_mode)):
        raise KitError("invalid_target", "The configuration root changed or redirects elsewhere.")
    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        info = _lstat(current)
        if info is None:
            continue
        if _redirected(info):
            raise KitError("symlink_path", "Refusing a symlink or reparse point in a managed path.", paths=[value])
        must_be_directory = index < len(relative.parts) - 1 or directory
        if must_be_directory and not stat.S_ISDIR(info.st_mode):
            raise KitError("invalid_path", "A managed parent is not a directory.", paths=[value])
        if not must_be_directory and not stat.S_ISREG(info.st_mode):
            raise KitError("invalid_path", "A managed file is not a regular file.", paths=[value])
    return current


def _read(path: Path, limit: int = MAX_FILE_BYTES) -> bytes:
    info = path.lstat()
    if _redirected(info) or not stat.S_ISREG(info.st_mode) or info.st_size > limit:
        raise KitError("invalid_file", "Expected a bounded regular file.", paths=[str(path)])
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise KitError("invalid_file", "File exceeds the permitted size.", paths=[str(path)])
    return data


def _validate_skill(data: bytes, expected_name: str) -> None:
    """Validate the intentionally minimal front matter shipped by this kit."""
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise KitError("invalid_skill", "SKILL.md needs YAML front matter.")
    end = lines.index("---", 1)
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        value = value.strip()
        if not separator or key not in ("name", "description") or key in fields or not value:
            raise KitError("invalid_skill", "Use one-line name and description front matter.")
        if value.startswith(("'", '"')):
            if len(value) < 2 or value[-1] != value[0]:
                raise KitError("invalid_skill", "Unterminated front matter string.")
            value = value[1:-1]
        if not value or value in ("|", ">", "|-", ">-"):
            raise KitError("invalid_skill", "Front matter values must be nonempty one-line scalars.")
        fields[key] = value
    if fields.get("name") != expected_name or not fields.get("description"):
        raise KitError("invalid_skill", "The skill name must match its directory and include a description.")
    if not "\n".join(lines[end + 1:]).strip():
        raise KitError("invalid_skill", "SKILL.md needs instructions after the front matter.")


def load_payload(payload_root: Path) -> dict[str, bytes]:
    payload_root = _root(payload_root)
    if not payload_root.is_dir():
        raise KitError("missing_payload", "The source payload directory is missing.")
    files: dict[str, bytes] = {}
    def entries(directory: Path):
        for path in sorted(directory.iterdir()):
            info = path.lstat()
            if _redirected(info):
                raise KitError("symlink_payload", "Payload symlinks and reparse points are not supported.",
                               paths=[path.relative_to(payload_root).as_posix()])
            yield path
            if stat.S_ISDIR(info.st_mode):
                yield from entries(path)

    for path in entries(payload_root):
        relative = path.relative_to(payload_root).as_posix()
        if path.is_symlink():
            raise KitError("symlink_payload", "Payload symlinks are not supported.", paths=[relative])
        if path.is_dir():
            _relative(relative)
            continue
        _payload_path(relative)
        data = _read(_checked(payload_root, relative))
        if not data.decode("utf-8").strip():
            raise KitError("invalid_payload", "Payload files must contain UTF-8 text.", paths=[relative])
        files[relative] = data
    required = {RULE, *SKILLS.values()}
    if not required <= set(files):
        raise KitError("missing_payload", "The payload must include the global rule and every packaged SKILL.md.")
    for name, value in SKILLS.items():
        _validate_skill(files[value], name)
    return files


def _allowed_directories(files: dict[str, Any]) -> set[str]:
    result = {METADATA}
    for value in files:
        for parent in PurePosixPath(value).parents:
            if str(parent) != ".":
                result.add(str(parent))
    return result


def _validate_record(record: Any) -> dict[str, Any]:
    if (not isinstance(record, dict) or set(record) != {
            "schema_version", "kit_version", "files", "created_dirs"} or
            type(record["schema_version"]) is not int or record["schema_version"] != SCHEMA_VERSION or
            not isinstance(record["kit_version"], str) or not record["kit_version"] or
            not isinstance(record["files"], dict) or not record["files"] or
            not isinstance(record["created_dirs"], list)):
        raise KitError("invalid_manifest", "Invalid installation manifest or journal schema.")
    if not {RULE, *SKILLS.values()} <= set(record["files"]):
        raise KitError("invalid_manifest", "Metadata must identify the rule and every packaged SKILL.md.")
    for value, expected_hash in record["files"].items():
        _payload_path(value)
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise KitError("invalid_manifest", "Invalid managed file hash.", paths=[value])
    dirs = record["created_dirs"]
    if any(not isinstance(value, str) for value in dirs):
        raise KitError("invalid_manifest", "Invalid created directory list.")
    if len(set(dirs)) != len(dirs) or not set(dirs) <= _allowed_directories(record["files"]):
        raise KitError("invalid_manifest", "Directory ownership escapes the managed payload.")
    return record


def _read_record(root: Path, value: str) -> dict[str, Any] | None:
    path = _checked(root, value)
    if _lstat(path) is None:
        return None
    try:
        return _validate_record(json.loads(_read(path, MAX_METADATA_BYTES)))
    except (ValueError, UnicodeError) as error:
        raise KitError("invalid_manifest", "Cannot parse installation metadata.", paths=[value]) from error


def _metadata(root: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    manifest = _read_record(root, MANIFEST)
    journal = _read_record(root, JOURNAL)
    if manifest and journal and manifest != journal:
        raise KitError("metadata_conflict", "The manifest and interrupted-install journal disagree.")
    return manifest, journal


def _changes(root: Path, record: dict[str, Any]) -> dict[str, list[str]]:
    changed: list[str] = []
    missing: list[str] = []
    for value, expected_hash in record["files"].items():
        path = _checked(root, value)
        if _lstat(path) is None:
            missing.append(value)
        elif digest(_read(path)) != expected_hash:
            changed.append(value)
    for value in record["created_dirs"]:
        _checked(root, value, directory=True)
    return {"modified": changed, "missing": missing}


def _result(command: str, root: Path, status: str, *, ok: bool = True, **extra: Any) -> dict[str, Any]:
    return {"ok": ok, "command": command, "status": status, "kit_version": VERSION,
            "bob_home": str(root), "client_loading_not_tested": True, **extra}


def _preview(root: Path, payload: dict[str, bytes]) -> dict[str, Any]:
    manifest, journal = _metadata(root)
    if journal:
        return _result("preview", root, "recovery_needed", ok=False, journal=JOURNAL,
                       next_action="Stop any active installer, then run uninstall to roll back the journal.")
    if manifest:
        changes = _changes(root, manifest)
        same = manifest["kit_version"] == VERSION and manifest["files"] == {
            value: digest(data) for value, data in payload.items()}
        clean = not changes["modified"] and not changes["missing"]
        status = "unchanged" if same and clean else ("local_changes" if not clean else "upgrade_requires_uninstall")
        return _result("preview", root, status, ok=same and clean, files_valid=clean,
                       payload_valid=True, changes=changes)
    collisions = [value for value in payload if _lstat(_checked(root, value)) is not None]
    return _result("preview", root, "conflicts" if collisions else "ready", ok=not collisions,
                   payload_valid=True, create=list(payload), conflicts=collisions,
                   metadata_to_create=[MANIFEST, JOURNAL], files_valid=None)


def preview(bob_home: Path, payload_root: Path) -> dict[str, Any]:
    return _preview(_root(bob_home), load_payload(payload_root))


def _atomic_create(root: Path, value: str, data: bytes, written: dict[str, tuple[bytes, int, int]],
                   temporary: dict[str, bytes]) -> None:
    """Publish complete bytes atomically without replacing any existing file.

    Hard links provide create-if-absent semantics. Staging stays outside Bob's
    auto-loaded rules and skills. Unsupported filesystems fail safely.
    """
    path = _checked(root, value)
    staging_dir = _checked(root, METADATA, directory=True)
    descriptor, staging_name = tempfile.mkstemp(prefix="stage-", suffix=".tmp", dir=staging_dir)
    staging = Path(staging_name)
    temporary[staging.relative_to(root).as_posix()] = data
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _checked(root, value)
        info = staging.lstat()
        if not info.st_ino:
            raise KitError("unsupported_filesystem", "File identity is unavailable for safe atomic creation.")
        # Register identity BEFORE publishing: interruption can occur after
        # os.link creates the destination but before that call returns.
        written[value] = (data, info.st_dev, info.st_ino)
        os.link(staging, path, follow_symlinks=False)
    finally:
        try:
            staging.unlink()
            temporary.pop(staging.relative_to(root).as_posix(), None)
        except FileNotFoundError:
            temporary.pop(staging.relative_to(root).as_posix(), None)


def _remove_empty_dirs(root: Path, values: list[str]) -> list[str]:
    retained: list[str] = []
    for value in sorted(values, key=lambda item: (item.count("/"), item), reverse=True):
        try:
            path = _checked(root, value, directory=True)
            path.rmdir()
        except FileNotFoundError:
            continue
        except (OSError, KitError):
            # Shared/nonempty or newly symlinked directories are retained.
            retained.append(value)
    return retained


def install(bob_home: Path, payload_root: Path) -> dict[str, Any]:
    root = _root(bob_home)
    payload = load_payload(payload_root)
    plan = _preview(root, payload)
    if not plan["ok"]:
        raise KitError(plan["status"], "Installation preflight failed; no payload files were changed.",
                       paths=plan.get("conflicts", []), details={"preview": plan})
    if plan["status"] == "unchanged":
        return _result("install", root, "unchanged", files_valid=True, payload_valid=True)
    directories = _allowed_directories(payload)
    created_dirs = [value for value in sorted(directories) if _lstat(_checked(root, value, directory=True)) is None]
    record = {"schema_version": SCHEMA_VERSION, "kit_version": VERSION,
              "files": {value: digest(data) for value, data in payload.items()}, "created_dirs": created_dirs}
    record_bytes = (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")
    written: dict[str, tuple[bytes, int, int]] = {}
    temporary: dict[str, bytes] = {}
    try:
        root.mkdir(parents=True, exist_ok=True)
        _checked(root, METADATA, directory=True).mkdir(exist_ok=True)
        _atomic_create(root, JOURNAL, record_bytes, written, temporary)
        for value in sorted(directories, key=lambda item: (item.count("/"), item)):
            _checked(root, value, directory=True).mkdir(exist_ok=True)
        for value, data in payload.items():
            _atomic_create(root, value, data, written, temporary)
        _atomic_create(root, MANIFEST, record_bytes, written, temporary)
        _checked(root, JOURNAL).unlink()
    except BaseException as error:
        remaining: list[str] = []
        # Any unpublished staging file is ours, even if an interrupted write
        # contains only a prefix. Its bytes never entered an auto-loaded path.
        for value in temporary:
            try:
                path = _checked(root, value)
                if _lstat(path) is not None:
                    path.unlink()
            except (OSError, KitError):
                remaining.append(value)
        # Remove the journal last: it remains available if cleanup is incomplete.
        for value, (data, device, inode) in reversed(list(written.items())):
            if value == JOURNAL:
                continue
            try:
                path = _checked(root, value)
                info = _lstat(path)
                if info is not None:
                    if (info.st_dev, info.st_ino) != (device, inode) or _read(path) != data:
                        remaining.append(value)
                    else:
                        path.unlink()
            except (OSError, KitError):
                remaining.append(value)
        if not remaining and JOURNAL in written:
            try:
                path = _checked(root, JOURNAL)
                info = _lstat(path)
                if info is not None:
                    if (info.st_dev, info.st_ino) != written[JOURNAL][1:] or _read(path) != record_bytes:
                        remaining.append(JOURNAL)
                    else:
                        path.unlink()
            except (OSError, KitError):
                remaining.append(JOURNAL)
        retained_dirs = _remove_empty_dirs(root, created_dirs)
        code = "interrupted" if isinstance(error, KeyboardInterrupt) else "install_failed"
        raise KitError(code, "Installation failed; inspect rollback status before retrying.",
                       paths=remaining, details={"rolled_back": not remaining,
                       "retained_directories": retained_dirs,
                       "recovery_journal": JOURNAL if remaining and JOURNAL in written else None,
                       "next_action": "Stop any active installer, preserve listed files, and run uninstall; leftover stage files may require manual cleanup." if remaining else "Retry install after resolving the reported cause.",
                       "cause": type(error).__name__}) from error
    return _result("install", root, "installed", files_valid=True, payload_valid=True,
                   installed=list(payload), manifest=MANIFEST, upgrade_policy="uninstall_then_install")


def doctor(bob_home: Path, payload_root: Path) -> dict[str, Any]:
    root = _root(bob_home)
    payload = load_payload(payload_root)
    manifest, journal = _metadata(root)
    record = manifest or journal
    if record is None:
        return _result("doctor", root, "not_installed", ok=False, payload_valid=True, files_valid=None)
    changes = _changes(root, record)
    valid = not changes["modified"] and not changes["missing"]
    return _result("doctor", root, "recovery_needed" if journal else ("healthy" if valid else "local_changes"),
                   ok=valid and journal is None, payload_valid=True, files_valid=valid,
                   changes=changes, installed_version=record["kit_version"],
                   payload_matches_installation=record["kit_version"] == VERSION and record["files"] == {
                       value: digest(data) for value, data in payload.items()},
                   journal=JOURNAL if journal else None)


def uninstall(bob_home: Path) -> dict[str, Any]:
    root = _root(bob_home)
    manifest, journal = _metadata(root)
    record = manifest or journal
    if record is None:
        return _result("uninstall", root, "not_installed", removed=[])
    changes = _changes(root, record)
    if changes["modified"]:
        raise KitError("modified_files", "Uninstall stopped before deletion; preserve or move edited files and retry.",
                       paths=changes["modified"], details={"changes": changes})
    removed: list[str] = []
    try:
        for value, expected_hash in record["files"].items():
            path = _checked(root, value)
            if _lstat(path) is None:
                continue
            if digest(_read(path)) != expected_hash:
                raise KitError("modified_files", "A managed file changed during uninstall.", paths=[value])
            path.unlink()
            removed.append(value)
        for value, expected_record in ((JOURNAL, journal), (MANIFEST, manifest)):
            if expected_record is not None:
                if _read_record(root, value) != expected_record:
                    raise KitError("metadata_conflict", "Metadata changed during uninstall.", paths=[value])
                _checked(root, value).unlink()
    except (OSError, KitError) as error:
        raise KitError("uninstall_incomplete", "Uninstall stopped; inspect removed files and retry using retained metadata.",
                       details={"removed": removed, "cause": type(error).__name__}) from error
    retained_dirs = _remove_empty_dirs(root, record["created_dirs"])
    return _result("uninstall", root, "recovered" if journal else "uninstalled", removed=removed,
                   previously_missing=changes["missing"], retained_directories=retained_dirs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline Bob Workflow Kit installer; no Bob or network calls.")
    parser.add_argument("command", choices=("preview", "install", "doctor", "uninstall"))
    parser.add_argument("--bob-home", metavar="PATH", help="Bob configuration root (default: the current user's ~/.bob).")
    args = parser.parse_args(argv)
    # This is the only place where the user's home may be resolved.
    root = Path(args.bob_home).expanduser().absolute() if args.bob_home else Path.home() / ".bob"
    payload = Path(__file__).resolve().parents[1] / "payload"
    try:
        if args.command == "uninstall":
            result = uninstall(root)
        else:
            result = {"preview": preview, "install": install, "doctor": doctor}[args.command](root, payload)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    except (KitError, OSError, UnicodeError) as error:
        info = {"code": error.code, "message": str(error), "paths": error.paths,
                **error.details} if isinstance(error, KitError) else {
                    "code": "filesystem_error", "message": str(error)}
        print(json.dumps(_result(args.command, root, "error", ok=False, error=info), indent=2, sort_keys=True))
        return 130 if isinstance(error, KitError) and error.code == "interrupted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
