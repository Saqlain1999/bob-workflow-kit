#!/usr/bin/env python3
"""Record a blocked or incomplete interactive Bob trial without editing its source."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

if __package__:
    from tools import prepare_live_trial
    from tools import validate_live_trial
else:  # Direct execution places this file's directory on sys.path.
    import prepare_live_trial
    import validate_live_trial


RESULT_STATUSES = {"blocked", "incomplete"}
CLAIM_LEVELS = {"installation_only", "loading_observed"}
INSTALLATION_STATUSES = {"not_run", "blocked", "healthy"}


class RecordingError(ValueError):
    pass


def _required(value: str | None, option: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordingError(f"{option} must be a non-empty value.")
    return value.strip()


def load_prepared(path: Path) -> dict:
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RecordingError("Cannot read the prepared live-trial record.") from error
    errors = validate_live_trial.validate(record)
    if errors:
        raise RecordingError("The input record is invalid: " + "; ".join(errors))
    if record.get("status") != "not_run" or record.get("claim_level") != "unexecuted":
        raise RecordingError("The input must be an unexecuted not_run record.")
    return record


def build_result(
        prepared: dict, *, status: str, claim_level: str, run_id: str,
        observed_at_utc: str, bob_interface: str, bob_version: str, bob_mode: str,
        os_name: str, python_version: str, execution_host_type: str,
        workspace_trust_decision: str, workspace_trust_evidence: str,
        native_loading_evidence: str, installation_status: str,
        first_confusing_step: str, limitations_and_redactions: str,
        fresh_conversation_confirmed: bool, live_bob_observed: bool,
        rule_loaded: bool = False, skill_loaded: bool = False,
        doctor_evidence: str | None = None, model_if_observed: str | None = None,
        manual_interventions: str | None = None,
        failed_or_abandoned_attempts: str | None = None) -> dict:
    if validate_live_trial.validate(prepared):
        raise RecordingError("The prepared record is invalid.")
    if prepared.get("status") != "not_run" or prepared.get("claim_level") != "unexecuted":
        raise RecordingError("The input must be an unexecuted not_run record.")
    if status not in RESULT_STATUSES:
        raise RecordingError("--status must be blocked or incomplete.")
    if claim_level not in CLAIM_LEVELS:
        raise RecordingError("--claim-level must be installation_only or loading_observed.")
    if installation_status not in INSTALLATION_STATUSES:
        raise RecordingError("--installation-status must be not_run, blocked, or healthy.")
    if not fresh_conversation_confirmed:
        raise RecordingError("--fresh-conversation-confirmed is required.")
    if not live_bob_observed:
        raise RecordingError("--live-bob-observed is required.")
    if claim_level == "loading_observed" and not (rule_loaded or skill_loaded):
        raise RecordingError("loading_observed requires --rule-loaded or --skill-loaded.")
    if claim_level == "installation_only" and (rule_loaded or skill_loaded):
        raise RecordingError("Use loading_observed when recording rule or skill loading.")
    if installation_status == "healthy" and not doctor_evidence:
        raise RecordingError("healthy installation status requires --doctor-evidence.")

    record = deepcopy(prepared)
    record.update({
        "status": status,
        "claim_level": claim_level,
        "run_id": _required(run_id, "--run-id"),
        "observed_at_utc": _required(observed_at_utc, "--observed-at-utc"),
        "first_confusing_step": _required(first_confusing_step, "--first-confusing-step"),
        "limitations_and_redactions": _required(
            limitations_and_redactions, "--limitations-and-redactions"),
        "manual_interventions": manual_interventions,
        "failed_or_abandoned_attempts": failed_or_abandoned_attempts,
    })
    record["bob"].update({
        "interface": bob_interface,
        "version": _required(bob_version, "--bob-version"),
        "mode": _required(bob_mode, "--bob-mode"),
        "model_if_observed": model_if_observed,
    })
    record["environment"].update({
        "os": _required(os_name, "--os"),
        "python_version": _required(python_version, "--python-version"),
        "execution_host_type": _required(execution_host_type, "--execution-host-type"),
    })
    record["configuration"].update({
        "fresh_conversation": True,
        "workspace_trust_decision": workspace_trust_decision,
        "workspace_trust_evidence": _required(
            workspace_trust_evidence, "--workspace-trust-evidence"),
        "live_bob_observed": True,
        "global_rule_observed_loaded": rule_loaded,
        "global_skill_observed_loaded": skill_loaded,
        "native_loading_evidence": _required(
            native_loading_evidence, "--native-loading-evidence"),
    })
    record["installation"].update({
        "status": installation_status,
        "doctor_evidence": doctor_evidence,
    })
    errors = validate_live_trial.validate(record)
    if errors:
        raise RecordingError("Recorded result is invalid: " + "; ".join(errors))
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--status", required=True, choices=sorted(RESULT_STATUSES))
    parser.add_argument("--claim-level", required=True, choices=sorted(CLAIM_LEVELS))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--observed-at-utc", required=True)
    parser.add_argument("--bob-interface", required=True,
                        choices=sorted(validate_live_trial.INTERACTIVE_INTERFACES))
    parser.add_argument("--bob-version", required=True)
    parser.add_argument("--bob-mode", required=True)
    parser.add_argument("--model-if-observed")
    parser.add_argument("--os", required=True)
    parser.add_argument("--python-version", required=True)
    parser.add_argument("--execution-host-type", required=True)
    parser.add_argument("--workspace-trust-decision", required=True,
                        choices=sorted(validate_live_trial.TRUST_DECISIONS))
    parser.add_argument("--workspace-trust-evidence", required=True)
    parser.add_argument("--native-loading-evidence", required=True)
    parser.add_argument("--installation-status", required=True,
                        choices=sorted(INSTALLATION_STATUSES))
    parser.add_argument("--doctor-evidence")
    parser.add_argument("--fresh-conversation-confirmed", action="store_true")
    parser.add_argument("--live-bob-observed", action="store_true")
    parser.add_argument("--rule-loaded", action="store_true")
    parser.add_argument("--skill-loaded", action="store_true")
    parser.add_argument("--first-confusing-step", required=True)
    parser.add_argument("--limitations-and-redactions", required=True)
    parser.add_argument("--manual-interventions")
    parser.add_argument("--failed-or-abandoned-attempts")
    args = parser.parse_args(argv)

    try:
        prepared = load_prepared(args.input)
        result = build_result(
            prepared,
            status=args.status,
            claim_level=args.claim_level,
            run_id=args.run_id,
            observed_at_utc=args.observed_at_utc,
            bob_interface=args.bob_interface,
            bob_version=args.bob_version,
            bob_mode=args.bob_mode,
            model_if_observed=args.model_if_observed,
            os_name=args.os,
            python_version=args.python_version,
            execution_host_type=args.execution_host_type,
            workspace_trust_decision=args.workspace_trust_decision,
            workspace_trust_evidence=args.workspace_trust_evidence,
            native_loading_evidence=args.native_loading_evidence,
            installation_status=args.installation_status,
            doctor_evidence=args.doctor_evidence,
            fresh_conversation_confirmed=args.fresh_conversation_confirmed,
            live_bob_observed=args.live_bob_observed,
            rule_loaded=args.rule_loaded,
            skill_loaded=args.skill_loaded,
            first_confusing_step=args.first_confusing_step,
            limitations_and_redactions=args.limitations_and_redactions,
            manual_interventions=args.manual_interventions,
            failed_or_abandoned_attempts=args.failed_or_abandoned_attempts,
        )
        prepare_live_trial.write_new(args.output, result)
    except (RecordingError, prepare_live_trial.PreparationError) as error:
        print(json.dumps({"created": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({
        "created": True,
        "path": str(args.output),
        "status": result["status"],
        "claim_level": result["claim_level"],
        "run_id": result["run_id"],
        "kit_commit": result["kit"]["commit"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
