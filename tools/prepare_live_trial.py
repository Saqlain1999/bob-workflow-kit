#!/usr/bin/env python3
"""Prepare a fail-closed live-trial record without running IBM Bob."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

if __package__:
    from tools import validate_live_trial
else:  # Direct execution places this file's directory, not the repository root, on sys.path.
    import validate_live_trial


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "live-trial-template.json"
VERSION = ROOT / "VERSION"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SCENARIOS = {"small_repair", "interruption_recovery"}


class PreparationError(ValueError):
    pass


def current_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "rev-parse", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise PreparationError(
            "Git history is unavailable; pass --kit-commit from the reviewed archive or release."
        ) from error
    commit = result.stdout.strip()
    if not COMMIT_RE.fullmatch(commit):
        raise PreparationError("Git returned an invalid kit commit identifier.")
    return commit


def build_record(*, task_id: str, scenario: str, kit_commit: str | None = None,
                 archive_sha256: str | None = None) -> dict:
    if not isinstance(task_id, str) or not task_id.strip():
        raise PreparationError("--task-id must be a non-empty value.")
    if scenario not in SCENARIOS:
        raise PreparationError("--scenario must be small_repair or interruption_recovery.")
    commit = current_git_commit() if kit_commit is None else kit_commit
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        raise PreparationError("--kit-commit must be a full lowercase 40-character Git commit.")
    if archive_sha256 is not None and not DIGEST_RE.fullmatch(archive_sha256):
        raise PreparationError("--archive-sha256 must be a lowercase 64-character SHA-256.")

    try:
        record = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        version = VERSION.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PreparationError("Cannot read the shipped trial template or VERSION.") from error
    if not version:
        raise PreparationError("VERSION must not be empty.")

    record["kit"].update({
        "version": version,
        "commit": commit,
        "archive_sha256": archive_sha256,
    })
    record["task"].update({"id": task_id.strip(), "scenario": scenario})
    errors = validate_live_trial.validate(record)
    if errors:
        raise PreparationError("Shipped template produced an invalid record: " + "; ".join(errors))
    return record


def write_new(path: Path, record: dict) -> None:
    path = Path(path)
    parent = path.parent
    if not parent.is_dir():
        raise PreparationError("The output parent directory must already exist.")
    data = json.dumps(record, indent=2, sort_keys=False) + "\n"
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise PreparationError("Refusing to overwrite an existing output path.") from error
    except OSError as error:
        raise PreparationError("Cannot create the requested output path.") from error
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--kit-commit")
    parser.add_argument("--archive-sha256")
    args = parser.parse_args(argv)
    try:
        record = build_record(
            task_id=args.task_id,
            scenario=args.scenario,
            kit_commit=args.kit_commit,
            archive_sha256=args.archive_sha256,
        )
        write_new(args.output, record)
    except PreparationError as error:
        print(json.dumps({"created": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({
        "created": True,
        "path": str(args.output),
        "status": record["status"],
        "kit_commit": record["kit"]["commit"],
        "scenario": record["task"]["scenario"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
