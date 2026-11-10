#!/usr/bin/env python3
"""Validate a manual Bob Workflow Kit live-trial record without executing Bob."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


SCHEMA_VERSION = 2
RECORD_TYPE = "manual_live_bob_trial"
STATUSES = {"not_run", "blocked", "incomplete", "completed"}
INTERACTIVE_INTERFACES = {"ide", "shell_interactive"}
TRUST_DECISIONS = {"trust_folder", "trust_parent", "ide_trusted_workspace"}
CLAIM_LEVELS = {"unexecuted", "installation_only", "loading_observed", "task_observed"}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def mapping(value, name, errors):
    if not isinstance(value, dict):
        errors.append(f"{name} must be an object")
        return {}
    return value


def require_string(value, name, errors):
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{name} must be a non-empty string")


def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if record.get("record_type") != RECORD_TYPE:
        errors.append(f"record_type must be {RECORD_TYPE}")

    status = record.get("status")
    if status not in STATUSES:
        errors.append("status must be not_run, blocked, incomplete, or completed")
    claim_level = record.get("claim_level")
    if claim_level not in CLAIM_LEVELS:
        errors.append("claim_level is unsupported")

    kit = mapping(record.get("kit"), "kit", errors)
    bob = mapping(record.get("bob"), "bob", errors)
    environment = mapping(record.get("environment"), "environment", errors)
    configuration = mapping(record.get("configuration"), "configuration", errors)
    installation = mapping(record.get("installation"), "installation", errors)
    task = mapping(record.get("task"), "task", errors)
    observations = mapping(record.get("workflow_observations"), "workflow_observations", errors)

    if status == "not_run":
        if claim_level != "unexecuted":
            errors.append("not_run requires claim_level unexecuted")
        if record.get("run_id") is not None or record.get("observed_at_utc") is not None:
            errors.append("not_run cannot carry execution identity")
        if configuration.get("live_bob_observed") not in (None, False):
            errors.append("not_run cannot claim live Bob observation")
        if installation.get("status") != "not_run":
            errors.append("not_run requires installation.status not_run")
        if task.get("manual_acceptance") != "not_assessed":
            errors.append("not_run requires manual_acceptance not_assessed")
        return errors

    require_string(record.get("run_id"), "run_id", errors)
    observed_at = record.get("observed_at_utc")
    require_string(observed_at, "observed_at_utc", errors)
    if isinstance(observed_at, str) and not observed_at.endswith("Z"):
        errors.append("observed_at_utc must be an explicit UTC timestamp ending in Z")

    require_string(kit.get("version"), "kit.version", errors)
    commit = kit.get("commit")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        errors.append("kit.commit must be a full lowercase 40-character Git commit")

    if bob.get("interface") not in INTERACTIVE_INTERFACES:
        errors.append("bob.interface must be ide or shell_interactive; bob run is excluded")
    require_string(bob.get("version"), "bob.version", errors)
    require_string(bob.get("mode"), "bob.mode", errors)

    for key in ("os", "python_version", "execution_host_type"):
        require_string(environment.get(key), f"environment.{key}", errors)

    if configuration.get("fresh_conversation") is not True:
        errors.append("executed trials require configuration.fresh_conversation true")
    if configuration.get("workspace_trust_decision") not in TRUST_DECISIONS:
        errors.append("executed trials require an explicit supported workspace trust decision")
    require_string(configuration.get("workspace_trust_evidence"),
                   "configuration.workspace_trust_evidence", errors)
    if configuration.get("live_bob_observed") is not True:
        errors.append("executed trials require configuration.live_bob_observed true")
    require_string(configuration.get("native_loading_evidence"),
                   "configuration.native_loading_evidence", errors)

    if status in {"blocked", "incomplete"}:
        if claim_level not in {"installation_only", "loading_observed"}:
            errors.append("blocked/incomplete results cannot claim task_observed")
        if claim_level == "loading_observed" and not (
                configuration.get("global_rule_observed_loaded") is True
                or configuration.get("global_skill_observed_loaded") is True):
            errors.append("loading_observed requires observed rule or skill loading")
        return errors

    if claim_level != "task_observed":
        errors.append("completed requires claim_level task_observed")
    if installation.get("status") != "healthy":
        errors.append("completed requires installation.status healthy")
    require_string(installation.get("doctor_evidence"),
                   "installation.doctor_evidence", errors)
    if configuration.get("global_rule_observed_loaded") is not True:
        errors.append("completed requires observed global rule loading")
    if configuration.get("global_skill_observed_loaded") is not True:
        errors.append("completed requires observed global skill loading")
    for key in ("id", "fixture_commit", "baseline_report", "candidate_report", "diff"):
        require_string(task.get(key), f"task.{key}", errors)
    if task.get("manual_acceptance") not in {"accepted", "rejected"}:
        errors.append("completed requires manual_acceptance accepted or rejected")
    for key in ("current_files_inspected", "historical_evidence_revalidated",
                "teammate_changes_preserved"):
        if observations.get(key) is not True:
            errors.append(f"completed requires workflow_observations.{key} true")
    require_string(observations.get("evidence_reference"),
                   "workflow_observations.evidence_reference", errors)
    return errors


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: validate_live_trial.py RECORD.json", file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, indent=2))
        return 1
    errors = validate(record)
    print(json.dumps({"valid": not errors, "status": record.get("status"),
                      "claim_level": record.get("claim_level"), "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
