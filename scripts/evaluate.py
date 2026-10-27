#!/usr/bin/env python3
"""Prepare six small fixtures and collect offline public-test/state evidence."""

import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "tiny-ledger"
TASK_ID = "tiny-ledger-atomicity-v1"
EXPECTED_TEST_COUNT = 9
EXPECTED_FAILURE = (
    "test_ledger.LedgerTests.test_unknown_destination_leaves_balances_unchanged"
)

TASKS = {
    "tiny-ledger": {
        "id": TASK_ID, "fixture": FIXTURE, "entry": "ledger.py",
        "test_count": EXPECTED_TEST_COUNT, "failures": [EXPECTED_FAILURE],
    },
    "parcel-resume": {
        "id": "parcel-resume-v1", "fixture": ROOT / "fixtures" / "parcel-resume",
        "entry": "parcel/pricing.py", "test_count": 10,
        "failures": [
            "test_export.ExportTests.test_below_policy_threshold_is_charged",
            "test_pricing.PricingTests.test_below_policy_threshold_is_charged",
        ],
    },
    "technical-writing-fidelity": {
        "id": "technical-writing-fidelity-v1",
        "fixture": ROOT / "fixtures" / "technical-writing-fidelity",
        "entry": "RUNBOOK.md",
        "test_count": 8,
        "failures": [
            "test_runbook.RunbookFidelityTests.test_procedure_has_four_ordered_steps",
            "test_runbook.RunbookFidelityTests.test_required_sections_are_present",
        ],
        "protected_files": ["contract.json"],
        "allowed_candidate_changes": ["RUNBOOK.md"],
    },
    "project-planning-handoff": {
        "id": "project-planning-handoff-v1",
        "fixture": ROOT / "fixtures" / "project-planning-handoff",
        "entry": "DELIVERY_PLAN.md",
        "test_count": 10,
        "failures": [
            "test_delivery_plan.DeliveryPlanTests.test_architecture_compares_two_options_and_selects_one",
            "test_delivery_plan.DeliveryPlanTests.test_checkpoint_supports_stale_detection_resume_and_abort",
            "test_delivery_plan.DeliveryPlanTests.test_four_acceptance_criteria_cover_behavior_and_compatibility",
            "test_delivery_plan.DeliveryPlanTests.test_repository_evidence_names_current_files_and_observations",
            "test_delivery_plan.DeliveryPlanTests.test_risks_cover_conflict_data_compatibility_and_preservation",
            "test_delivery_plan.DeliveryPlanTests.test_slices_trace_every_criterion_to_files_and_validation",
            "test_delivery_plan.DeliveryPlanTests.test_unknowns_and_stop_conditions_remain_explicit",
        ],
        "protected_files": [
            "REQUEST.md", "notifier/service.py", "notifier/store.py", "project-tests.md",
        ],
        "allowed_candidate_changes": ["DELIVERY_PLAN.md"],
    },
    "reminder-implementation-debugging": {
        "id": "reminder-implementation-debugging-v1",
        "fixture": ROOT / "fixtures" / "reminder-implementation-debugging",
        "entry": "notifier/service.py",
        "test_count": 10,
        "failures": [
            "test_idempotency.ReminderImplementationTests.test_conflicting_reuse_raises_without_append",
            "test_idempotency.ReminderImplementationTests.test_handoff_records_current_evidence_and_limits",
            "test_idempotency.ReminderImplementationTests.test_retry_returns_original_without_duplicate",
            "test_idempotency.ReminderImplementationTests.test_retry_survives_new_service_instance",
        ],
        "protected_files": [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_CHECKPOINT.md",
            "TEAM_NOTES.md",
        ],
        "allowed_candidate_changes": [
            "IMPLEMENTATION_HANDOFF.md", "notifier/__init__.py",
            "notifier/service.py", "notifier/store.py",
        ],
    },
    "reminder-independent-review": {
        "id": "reminder-independent-review-v1",
        "fixture": ROOT / "fixtures" / "reminder-independent-review",
        "entry": "REVIEW_HANDOFF.md",
        "test_count": 10,
        "failures": [
            "test_review_report.ReminderReviewTests.test_acceptance_preservation_and_recovery_map",
            "test_review_report.ReminderReviewTests.test_current_state_and_stale_author_evidence",
            "test_review_report.ReminderReviewTests.test_decision_severity_and_limits",
            "test_review_report.ReminderReviewTests.test_independent_validation_records_both_reproductions",
            "test_review_report.ReminderReviewTests.test_rev_001_records_cross_owner_disclosure",
            "test_review_report.ReminderReviewTests.test_rev_002_records_conflict_data_exposure",
            "test_review_report.ReminderReviewTests.test_review_handoff_has_required_sections_in_order",
            "test_review_report.ReminderReviewTests.test_remediation_handoff_is_bounded_and_ordered",
        ],
        "protected_files": [
            "REQUEST.md", "DELIVERY_PLAN.md", "IMPLEMENTATION_HANDOFF.md",
            "TEAM_NOTES.md", "notifier/__init__.py", "notifier/service.py",
            "notifier/store.py",
        ],
        "allowed_candidate_changes": ["REVIEW_HANDOFF.md"],
    },
}
HANDOFF_FILES = {
    "CHECKPOINT.md", "handoff/historical-check.json", "handoff/preparation.json",
}
TEAMMATE_NOTE = (
    "\nTeammate note added after the checkpoint: the next documentation review "
    "is on Friday. Keep the existing examples' headings.\n"
)
DIAGNOSTIC_LIMIT_BYTES = 256 * 1024
WORKER_REPORT_LIMIT_BYTES = 512 * 1024
READ_CHUNK_BYTES = 16 * 1024
PROCESS_POLL_SECONDS = 0.02
PROCESS_STOP_GRACE_SECONDS = 1.0


class _BoundedTextBuffer(io.TextIOBase):
    """Retain at most limit UTF-8 bytes while counting discarded output."""

    def __init__(self, limit: int) -> None:
        super().__init__()
        self.limit = limit
        self.bytes_seen = 0
        self._buffer = bytearray()

    @property
    def exceeded(self) -> bool:
        return self.bytes_seen > self.limit

    def write(self, value: str) -> int:
        if not isinstance(value, str):
            raise TypeError("text output must be str")
        encoded = value.encode("utf-8", errors="replace")
        self.bytes_seen += len(encoded)
        remaining = self.limit - len(self._buffer)
        if remaining > 0:
            self._buffer.extend(encoded[:remaining])
        return len(value)

    def getvalue(self) -> str:
        return bytes(self._buffer).decode("utf-8", errors="replace")


def _stop_process(process: subprocess.Popen) -> None:
    """Terminate and reap the direct worker; descendants are not contained."""
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=PROCESS_STOP_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def _run_bounded_process(
    command: List[str], cwd: str, environment: Dict[str, str], timeout: float,
    limit: int = DIAGNOSTIC_LIMIT_BYTES,
) -> Dict[str, Any]:
    """Run a process while draining both diagnostic pipes into fixed budgets."""
    process = subprocess.Popen(
        command, cwd=cwd, env=environment,
        # Raw pipes avoid BufferedReader's lock: closing a buffered pipe can
        # wait forever for a reader whose inherited writer is still open.
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0,
    )
    captures = {"stdout": bytearray(), "stderr": bytearray()}
    totals = {"stdout": 0, "stderr": 0}
    exceeded = set()
    exceeded_event = threading.Event()

    def drain(channel: str, pipe: Any) -> None:
        try:
            while True:
                chunk = pipe.read(READ_CHUNK_BYTES)
                if not chunk:
                    break
                totals[channel] += len(chunk)
                remaining = limit - len(captures[channel])
                if remaining > 0:
                    captures[channel].extend(chunk[:remaining])
                if totals[channel] > limit:
                    exceeded.add(channel)
                    exceeded_event.set()
        except (OSError, ValueError):
            # The parent may close a pipe after reaping a worker whose
            # descendants kept the inherited write end open.
            pass

    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    for thread in threads:
        thread.start()

    deadline = time.monotonic() + timeout
    timed_out = False
    while process.poll() is None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            _stop_process(process)
            break
        exceeded_event.wait(min(PROCESS_POLL_SECONDS, remaining))
        if exceeded_event.is_set():
            _stop_process(process)
            break

    process.wait()
    capture_incomplete = []
    for channel, thread, pipe in zip(("stdout", "stderr"), threads, (process.stdout, process.stderr)):
        thread.join(PROCESS_STOP_GRACE_SECONDS)
        if thread.is_alive():
            capture_incomplete.append(channel)
        else:
            pipe.close()

    # Even unbuffered pipe closure can wait for a reader blocked on Windows.
    # A live daemon reader therefore retains its pipe until the short-lived
    # helper exits or the uncontained descendant closes the inherited writer.
    # Return bounded snapshots now and make incomplete capture a hard non-pass.

    return {
        "returncode": process.returncode,
        "stdout": bytes(captures["stdout"]).decode("utf-8", errors="replace"),
        "stderr": bytes(captures["stderr"]).decode("utf-8", errors="replace"),
        "bytes_seen": dict(totals),
        "limit_bytes_per_channel": limit,
        "limit_exceeded_channels": sorted(exceeded),
        "capture_incomplete_channels": capture_incomplete,
        "timed_out": timed_out,
    }


def _read_bounded(path: Path, limit: int) -> Tuple[bytes, bool]:
    with path.open("rb") as source:
        content = source.read(limit + 1)
    return content[:limit], len(content) > limit


def _resource_limit(
    report: Dict[str, Any], channel: str, limit: int, excerpt: Optional[str] = None,
    bytes_seen: Optional[int] = None,
) -> None:
    report["status"] = "resource_limit_exceeded"
    report["error"] = "Public-test worker exceeded a retained diagnostic limit"
    report["resource_limit"] = {
        "channel": channel,
        "limit_bytes": limit,
        "bytes_seen": bytes_seen,
    }
    if excerpt:
        report["resource_limit"]["bounded_excerpt"] = excerpt


def _task(name: str) -> Dict[str, Any]:
    if name not in TASKS:
        raise ValueError("Unknown task: " + name)
    return TASKS[name]


def _inside(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _file_hash(path: Path) -> Optional[str]:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _test_hash(directory: Path) -> Optional[str]:
    if not directory.is_dir():
        return None
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*.py")):
        digest.update(path.relative_to(directory).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _snapshot(directory: Path) -> Dict[str, str]:
    """Include new files too; only known handoff files/caches/VCS are omitted."""
    files = {}
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    def walk_error(error: OSError) -> None:
        raise error

    for current, directories, names in os.walk(directory, followlinks=False, onerror=walk_error):
        directories[:] = sorted(name for name in directories if name not in {".git", "__pycache__"})
        for name in directories + sorted(names):
            path = Path(current) / name
            relative = path.relative_to(directory).as_posix()
            if relative in HANDOFF_FILES:
                continue
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & reparse_flag:
                raise ValueError("Workspace state cannot include redirected paths: " + relative)
            if stat.S_ISDIR(metadata.st_mode):
                continue
            if not stat.S_ISREG(metadata.st_mode):
                raise ValueError("Workspace state requires regular files: " + relative)
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(files.items()))


def _state_hash(files: Dict[str, str]) -> str:
    encoded = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _protected_files(task_name: str, historical: bool = False) -> Dict[str, bytes]:
    fixture = _task(task_name)["fixture"]
    if task_name != "parcel-resume":
        return {
            name: (fixture / name).read_bytes()
            for name in _task(task_name).get("protected_files", [])
        }
    policy = (fixture / "policy.json").read_bytes()
    notes = (fixture / "TEAM_NOTES.md").read_bytes()
    if not historical:
        values = json.loads(policy)
        values["free_delivery_min_cents"] = 7500
        policy = (json.dumps(values, indent=2) + "\n").encode("utf-8")
        notes += TEAMMATE_NOTE.encode("utf-8")
    return {"policy.json": policy, "TEAM_NOTES.md": notes}


def _expected_state(task_name: str, historical: bool = False) -> Dict[str, str]:
    expected = _snapshot(_task(task_name)["fixture"])
    for name, content in _protected_files(task_name, historical).items():
        expected[name] = hashlib.sha256(content).hexdigest()
    return dict(sorted(expected.items()))


def _validate_timeout(timeout: float) -> None:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Timeout must be finite and positive")


def prepare(output: Path, task_name: str = "tiny-ledger", timeout: float = 30.0) -> Dict[str, Any]:
    task = _task(task_name)
    fixture = task["fixture"]
    _validate_timeout(timeout)
    output = output.resolve()
    if _inside(output, (ROOT / "fixtures").resolve()):
        raise ValueError("Prepare a workspace outside the original fixture")
    if output.exists():
        raise ValueError("Output already exists; choose a new run directory")
    shutil.copytree(fixture, output, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    report = {
        "schema_version": 1,
        "task_id": task["id"],
        "status": "workspace_prepared",
        "workspace": str(output),
        "source_sha256": _file_hash(output / task["entry"]),
        "public_tests_sha256": _test_hash(fixture / "tests"),
        "model_calls_made_by_helper": 0,
    }
    if task_name != "parcel-resume":
        return report
    try:
        historical, exit_code = check(output, "historical", timeout, task_name)
        if exit_code:
            raise ValueError("Historical fixture check failed; no resume workspace prepared: " + historical["status"])
        handoff = output / "handoff"
        handoff.mkdir()
        (handoff / "historical-check.json").write_text(json.dumps(historical, indent=2) + "\n", encoding="utf-8")
        before = historical["workspace_state"]["after"]
        template = (ROOT / "tasks" / "parcel-resume" / "CHECKPOINT_TEMPLATE.md").read_text(encoding="utf-8")
        replacements = {
            "{{OBSERVED_AT}}": historical["observed_at_utc"],
            "{{STATE_SHA256}}": _state_hash(before),
            "{{PYTHON_VERSION}}": historical["environment"]["python_version"],
        }
        for old, new in replacements.items():
            template = template.replace(old, new)
        (output / "CHECKPOINT.md").write_text(template, encoding="utf-8")
        for name, content in _protected_files(task_name).items():
            (output / name).write_bytes(content)
        after = _snapshot(output)
        if after != _expected_state(task_name):
            raise ValueError("Prepared workspace does not match the deterministic interruption state")
        report.update({
            "scenario": "constructed_interruption_not_an_agent_run",
            "checkpoint": "CHECKPOINT.md",
            "historical_check": "handoff/historical-check.json",
            "historical_check_is_current": before == after,
            "historical_state_sha256": _state_hash(before),
            "prepared_state_sha256": _state_hash(after),
            "prepared_state_files": after,
            "changed_since_checkpoint": sorted(name for name in set(before) | set(after) if before.get(name) != after.get(name)),
            "protected_files": sorted(_protected_files(task_name)),
            "manual_acceptance": "not_assessed",
            "observed_bob_behavior": "not_assessed",
        })
        (handoff / "preparation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return report
    except BaseException:
        # Only this newly created disposable copy is removed, never prior work.
        shutil.rmtree(output)
        raise


def _worker(workspace: Path, report_path: Path, task_name: str = "tiny-ledger") -> None:
    """Run trusted tests against the candidate in a separate Python process."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(workspace.resolve()))
    suite = unittest.TestLoader().discover(str(_task(task_name)["fixture"] / "tests"), pattern="test_*.py")
    output = _BoundedTextBuffer(DIAGNOSTIC_LIMIT_BYTES)
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    report = {
        "tests_run": result.testsRun,
        "failures": [test.id() for test, _ in result.failures],
        "errors": [test.id() for test, _ in result.errors],
        "skipped": [test.id() for test, _ in result.skipped],
        "expected_failures": [test.id() for test, _ in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
        "successful": result.wasSuccessful(),
        "output": output.getvalue(),
    }
    if output.exceeded:
        report["resource_limit"] = {
            "channel": "unittest_output",
            "limit_bytes": DIAGNOSTIC_LIMIT_BYTES,
            "bytes_seen": output.bytes_seen,
        }
    report_path.write_text(json.dumps(report), encoding="utf-8")


def check(workspace: Path, phase: str, timeout: float, task_name: str = "tiny-ledger") -> Tuple[Dict[str, Any], int]:
    task = _task(task_name)
    fixture = task["fixture"]
    workspace = workspace.resolve()
    if not workspace.is_dir() or not (workspace / task["entry"]).is_file():
        raise ValueError("Workspace must contain " + task["entry"])
    if phase not in {"baseline", "candidate", "historical"}:
        raise ValueError("Unknown check phase")
    _validate_timeout(timeout)

    before = _snapshot(workspace)
    expected = _expected_state(task_name, historical=phase == "historical")
    canonical_source = _file_hash(fixture / task["entry"])
    source = _file_hash(workspace / task["entry"])
    canonical_tests = _test_hash(fixture / "tests")
    workspace_tests = _test_hash(workspace / "tests")
    protected = _protected_files(task_name, historical=phase == "historical")
    report: Dict[str, Any] = {
        "schema_version": 1,
        "record_type": "offline_public_test_check",
        "task_id": task["id"],
        "phase": phase,
        "status": "runner_error",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "python_executable": sys.executable,
        },
        "helper_sha256": _file_hash(Path(__file__).resolve()),
        "fingerprints": {
            "original_source_sha256": canonical_source,
            "candidate_source_sha256": source,
            "trusted_public_tests_sha256": canonical_tests,
            "workspace_tests_sha256": workspace_tests,
            "source_matches_original": source == canonical_source,
            "workspace_tests_match_original": workspace_tests == canonical_tests,
            "expected_state_sha256": _state_hash(expected),
            "candidate_state_before_sha256": _state_hash(before),
            "candidate_state_after_sha256": None,
        },
        "workspace_state": {
            "scope": "All regular workspace files, including new files; excludes CHECKPOINT.md, handoff/historical-check.json, handoff/preparation.json, .git/, and __pycache__/",
            "before": before, "after": None, "stable_during_check": None,
            "changed_during_check": [],
        },
        "protected_inputs": {
            name: {"expected_sha256": hashlib.sha256(content).hexdigest(), "before_sha256": before.get(name), "after_sha256": None}
            for name, content in protected.items()
        },
        "protected_inputs_match_prepared": None if not protected or phase == "historical" else False,
        "candidate_scope": {
            "allowed_changes": task.get("allowed_candidate_changes"),
            "observed_changes": None,
            "matches": None,
        },
        "trusted_tests_stable_during_check": None,
        "test_duration_seconds": None,
        "tests": None,
        "manual_acceptance": "not_assessed",
        "observed_bob_behavior": "not_assessed",
        "model_calls_made_by_helper": 0,
    }
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="bob-eval-") as temporary:
        worker_report = Path(temporary) / "tests.json"
        command = [
            sys.executable, "-B", str(Path(__file__).resolve()), "_run-tests",
            str(workspace), str(worker_report), task_name,
        ]
        report["test_command"] = command
        report["test_working_directory"] = str(workspace)
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment.pop("PYTHONPATH", None)
        try:
            completed = _run_bounded_process(
                command, str(workspace), environment, timeout,
            )
            if completed["timed_out"]:
                report["error"] = "Public-test worker exceeded the configured timeout"
                return report, 2
            if completed["limit_exceeded_channels"]:
                channels = completed["limit_exceeded_channels"]
                channel = "worker_" + "+".join(channels)
                excerpts = "\n".join(
                    name + ":\n" + completed[name] for name in channels
                )
                _resource_limit(
                    report, channel, completed["limit_bytes_per_channel"], excerpts,
                    max(completed["bytes_seen"][name] for name in channels),
                )
                return report, 2
            if completed["capture_incomplete_channels"]:
                report["error"] = (
                    "Public-test worker diagnostic pipes remained open after the direct worker exited: "
                    + ", ".join(completed["capture_incomplete_channels"])
                )
                return report, 2
            if completed["returncode"] != 0 or not worker_report.is_file():
                report["error"] = "Public-test worker did not produce a valid result"
                report["worker_stdout"] = completed["stdout"]
                report["worker_stderr"] = completed["stderr"]
                return report, 2
            encoded_report, report_exceeded = _read_bounded(
                worker_report, WORKER_REPORT_LIMIT_BYTES,
            )
            if report_exceeded:
                _resource_limit(
                    report, "worker_report", WORKER_REPORT_LIMIT_BYTES,
                    encoded_report.decode("utf-8", errors="replace"),
                )
                return report, 2
            tests = json.loads(encoded_report.decode("utf-8"))
            if isinstance(tests, dict) and isinstance(tests.get("resource_limit"), dict):
                details = tests["resource_limit"]
                _resource_limit(
                    report,
                    str(details.get("channel", "unittest_output")),
                    int(details.get("limit_bytes", DIAGNOSTIC_LIMIT_BYTES)),
                    tests.get("output") if isinstance(tests.get("output"), str) else None,
                    details.get("bytes_seen") if type(details.get("bytes_seen")) is int else None,
                )
                return report, 2
            list_fields = ("failures", "errors", "skipped", "expected_failures", "unexpected_successes")
            if (
                not isinstance(tests, dict)
                or type(tests.get("tests_run")) is not int
                or tests["tests_run"] < 0
                or type(tests.get("successful")) is not bool
                or not isinstance(tests.get("output"), str)
                or any(not isinstance(tests.get(key), list) or not all(isinstance(item, str) for item in tests[key]) for key in list_fields)
            ):
                raise ValueError("Malformed public-test worker result")
            report["tests"] = tests
            if completed["stdout"]:
                report["candidate_stdout"] = completed["stdout"]
            if completed["stderr"]:
                report["candidate_stderr"] = completed["stderr"]
        except (json.JSONDecodeError, OSError, UnicodeDecodeError, ValueError) as error:
            report["error"] = "Public-test worker failed: " + str(error)
            return report, 2
        finally:
            report["test_duration_seconds"] = round(time.perf_counter() - started, 6)

    after = _snapshot(workspace)
    state_stable = before == after
    trusted_tests_stable = canonical_tests == _test_hash(fixture / "tests")
    report["workspace_state"].update({
        "after": after, "stable_during_check": state_stable,
        "changed_during_check": sorted(name for name in set(before) | set(after) if before.get(name) != after.get(name)),
    })
    report["fingerprints"]["candidate_state_after_sha256"] = _state_hash(after)
    report["trusted_tests_stable_during_check"] = trusted_tests_stable
    for name, details in report["protected_inputs"].items():
        details["after_sha256"] = after.get(name)
    protected_valid = all(before.get(name) == after.get(name) == hashlib.sha256(content).hexdigest() for name, content in protected.items())
    if protected and phase != "historical":
        report["protected_inputs_match_prepared"] = protected_valid
    if not state_stable or not trusted_tests_stable:
        report["status"] = "workspace_changed_during_check" if not state_stable else "trusted_tests_changed_during_check"
        report["error"] = "Verification inputs changed; the test outcome is not evidence for a stable current state"
        return report, 2

    candidate_scope_valid = True
    allowed_candidate_changes = task.get("allowed_candidate_changes")
    if phase == "candidate" and allowed_candidate_changes is not None:
        original = _expected_state(task_name)
        observed_changes = sorted(
            name
            for name in set(original) | set(before)
            if original.get(name) != before.get(name)
        )
        candidate_scope_valid = set(observed_changes).issubset(allowed_candidate_changes)
        report["candidate_scope"].update({
            "observed_changes": observed_changes,
            "matches": candidate_scope_valid,
        })

    complete_suite = (
        tests["tests_run"] == task["test_count"]
        and not tests["errors"]
        and not tests["skipped"]
        and not tests["expected_failures"]
        and not tests["unexpected_successes"]
    )
    if phase == "historical":
        valid = complete_suite and tests["successful"] and not tests["failures"] and before == expected and protected_valid
        report["status"] = "historical_tests_passed" if valid else "unexpected_historical_state"
    elif phase == "baseline":
        valid = (
            complete_suite
            and sorted(tests["failures"]) == sorted(task["failures"])
            and source == canonical_source
            and workspace_tests == canonical_tests
            and (task_name == "tiny-ledger" or before == expected)
            and protected_valid
        )
        report["status"] = "expected_baseline_failure" if valid else "unexpected_baseline"
    else:
        valid = (
            complete_suite
            and not tests["failures"]
            and tests["successful"]
            and protected_valid
            and candidate_scope_valid
        )
        report["status"] = (
            "public_tests_passed"
            if valid
            else "protected_inputs_changed"
            if not protected_valid
            else "candidate_scope_changed"
            if not candidate_scope_valid
            else "public_tests_failed"
        )
    return report, 0 if valid else 1


def _validate_output(path: Optional[Path], workspace: Optional[Path] = None) -> Optional[Path]:
    if path is None:
        return None
    resolved = path.resolve()
    if _inside(resolved, (ROOT / "fixtures").resolve()):
        raise ValueError("Result output must be outside the original fixture")
    if workspace is not None and _inside(resolved, workspace.resolve()):
        raise ValueError("Result output must be outside the candidate workspace so recording it does not change the verified state")
    if resolved.exists():
        raise ValueError("Result file already exists; choose a new filename")
    return resolved


def main(argv: Optional[List[str]] = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments and arguments[0] == "_run-tests":
        if len(arguments) not in {3, 4}:
            return 2
        _worker(Path(arguments[1]), Path(arguments[2]), arguments[3] if len(arguments) == 4 else "tiny-ledger")
        return 0

    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare", help="Copy the original to a new workspace")
    prepare_parser.add_argument("--output", required=True, type=Path)
    prepare_parser.add_argument("--task", choices=TASKS, default="tiny-ledger")
    prepare_parser.add_argument("--timeout", type=float, default=30.0)
    for phase in ("baseline", "candidate"):
        subparser = commands.add_parser(phase, help="Collect " + phase + " public-test evidence")
        subparser.add_argument("--workspace", required=True, type=Path)
        subparser.add_argument("--result", type=Path)
        subparser.add_argument("--timeout", type=float, default=30.0)
        subparser.add_argument("--task", choices=TASKS, default="tiny-ledger")
    args = parser.parse_args(arguments)
    try:
        if args.command == "prepare":
            report = prepare(args.output, args.task, args.timeout)
            result_path = None
            exit_code = 0
        else:
            state_bound_tasks = {
                "parcel-resume", "technical-writing-fidelity", "project-planning-handoff",
                "reminder-implementation-debugging", "reminder-independent-review",
            }
            result_path = _validate_output(
                args.result, args.workspace if args.task in state_bound_tasks else None
            )
            report, exit_code = check(args.workspace, args.command, args.timeout, args.task)
        encoded = json.dumps(report, indent=2) + "\n"
        if result_path is not None:
            result_path.parent.mkdir(parents=True, exist_ok=True)
            with result_path.open("x", encoding="utf-8") as output:
                output.write(encoded)
            print(json.dumps({"status": report["status"], "result_file": str(result_path)}))
        else:
            print(encoded, end="")
        return exit_code
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "helper_error", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
