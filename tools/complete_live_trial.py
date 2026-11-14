#!/usr/bin/env python3
"""Record a completed interactive Bob trial without editing its prepared source."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

if __package__:
    from tools import prepare_live_trial
    from tools import record_live_trial
    from tools import validate_live_trial
else:  # Direct execution places this file's directory on sys.path.
    import prepare_live_trial
    import record_live_trial
    import validate_live_trial


MANUAL_ACCEPTANCE = {"accepted", "rejected"}


class CompletionError(ValueError):
    pass


def _required(value: str | None, option: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompletionError(f"{option} must be a non-empty value.")
    return value.strip()


def build_result(
        prepared: dict, *, run_id: str, observed_at_utc: str,
        bob_interface: str, bob_version: str, bob_mode: str,
        os_name: str, python_version: str, execution_host_type: str,
        workspace_trust_decision: str, workspace_trust_evidence: str,
        native_loading_evidence: str, doctor_evidence: str,
        fixture_commit: str, baseline_report: str, candidate_report: str,
        diff: str, manual_acceptance: str, workflow_evidence_reference: str,
        first_confusing_step: str, limitations_and_redactions: str,
        fresh_conversation_confirmed: bool, live_bob_observed: bool,
        rule_loaded: bool, skill_loaded: bool,
        current_files_inspected: bool, historical_evidence_revalidated: bool,
        teammate_changes_preserved: bool,
        interruption_type: str | None = None, handoff_read: bool = False,
        current_state_reconciled: bool = False,
        stale_historical_evidence_detected: bool = False,
        relevant_checks_rerun: bool = False, checkpoint_updated: bool = False,
        unrelated_changes_preserved: bool = False,
        recovery_evidence_reference: str | None = None,
        model_if_observed: str | None = None,
        same_name_project_override: str | None = None,
        other_workflows_or_rules: str | None = None,
        manual_interventions: str | None = None,
        failed_or_abandoned_attempts: str | None = None) -> dict:
    errors = validate_live_trial.validate(prepared)
    if errors:
        raise CompletionError("The prepared record is invalid: " + "; ".join(errors))
    if prepared.get("status") != "not_run" or prepared.get("claim_level") != "unexecuted":
        raise CompletionError("The input must be an unexecuted not_run record.")
    if not fresh_conversation_confirmed:
        raise CompletionError("--fresh-conversation-confirmed is required.")
    if not live_bob_observed:
        raise CompletionError("--live-bob-observed is required.")
    if not rule_loaded or not skill_loaded:
        raise CompletionError("Completion requires --rule-loaded and --skill-loaded.")
    for value, option in (
            (current_files_inspected, "--current-files-inspected"),
            (historical_evidence_revalidated, "--historical-evidence-revalidated"),
            (teammate_changes_preserved, "--teammate-changes-preserved")):
        if not value:
            raise CompletionError(f"{option} is required.")
    if manual_acceptance not in MANUAL_ACCEPTANCE:
        raise CompletionError("--manual-acceptance must be accepted or rejected.")

    scenario = prepared.get("task", {}).get("scenario")
    recovery_flags = {
        "--handoff-read": handoff_read,
        "--current-state-reconciled": current_state_reconciled,
        "--stale-historical-evidence-detected": stale_historical_evidence_detected,
        "--relevant-checks-rerun": relevant_checks_rerun,
        "--checkpoint-updated": checkpoint_updated,
        "--unrelated-changes-preserved": unrelated_changes_preserved,
    }
    if scenario == "small_repair":
        if (interruption_type is not None or recovery_evidence_reference is not None
                or any(recovery_flags.values())):
            raise CompletionError("A small_repair cannot record interruption-recovery evidence.")
    elif scenario == "interruption_recovery":
        if interruption_type not in validate_live_trial.INTERRUPTION_TYPES:
            raise CompletionError("An interruption_recovery requires --interruption-type.")
        missing = [option for option, observed in recovery_flags.items() if not observed]
        if missing:
            raise CompletionError("Interruption recovery requires " + ", ".join(missing) + ".")
        _required(recovery_evidence_reference, "--recovery-evidence-reference")
    else:
        raise CompletionError("The prepared task scenario is unsupported.")

    record = deepcopy(prepared)
    record.update({
        "status": "completed",
        "claim_level": "task_observed",
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
        "global_rule_observed_loaded": True,
        "global_skill_observed_loaded": True,
        "same_name_project_override": same_name_project_override,
        "other_workflows_or_rules": other_workflows_or_rules,
        "native_loading_evidence": _required(
            native_loading_evidence, "--native-loading-evidence"),
    })
    record["installation"].update({
        "status": "healthy",
        "doctor_evidence": _required(doctor_evidence, "--doctor-evidence"),
    })
    record["task"].update({
        "fixture_commit": _required(fixture_commit, "--fixture-commit"),
        "baseline_report": _required(baseline_report, "--baseline-report"),
        "candidate_report": _required(candidate_report, "--candidate-report"),
        "diff": _required(diff, "--diff"),
        "manual_acceptance": manual_acceptance,
    })
    record["workflow_observations"].update({
        "current_files_inspected": True,
        "historical_evidence_revalidated": True,
        "teammate_changes_preserved": True,
        "evidence_reference": _required(
            workflow_evidence_reference, "--workflow-evidence-reference"),
    })
    if scenario == "small_repair":
        record["recovery_observations"].update({"status": "not_applicable"})
    else:
        record["recovery_observations"].update({
            "status": "observed",
            "interruption_type": interruption_type,
            "handoff_read": True,
            "current_state_reconciled": True,
            "stale_historical_evidence_detected": True,
            "relevant_checks_rerun": True,
            "checkpoint_updated": True,
            "unrelated_changes_preserved": True,
            "evidence_reference": _required(
                recovery_evidence_reference, "--recovery-evidence-reference"),
        })
    errors = validate_live_trial.validate(record)
    if errors:
        raise CompletionError("Completed result is invalid: " + "; ".join(errors))
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
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
    parser.add_argument("--doctor-evidence", required=True)
    parser.add_argument("--fresh-conversation-confirmed", action="store_true")
    parser.add_argument("--live-bob-observed", action="store_true")
    parser.add_argument("--rule-loaded", action="store_true")
    parser.add_argument("--skill-loaded", action="store_true")
    parser.add_argument("--fixture-commit", required=True)
    parser.add_argument("--baseline-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--diff", required=True)
    parser.add_argument("--manual-acceptance", required=True,
                        choices=sorted(MANUAL_ACCEPTANCE))
    parser.add_argument("--current-files-inspected", action="store_true")
    parser.add_argument("--historical-evidence-revalidated", action="store_true")
    parser.add_argument("--teammate-changes-preserved", action="store_true")
    parser.add_argument("--workflow-evidence-reference", required=True)
    parser.add_argument("--interruption-type",
                        choices=sorted(validate_live_trial.INTERRUPTION_TYPES))
    parser.add_argument("--handoff-read", action="store_true")
    parser.add_argument("--current-state-reconciled", action="store_true")
    parser.add_argument("--stale-historical-evidence-detected", action="store_true")
    parser.add_argument("--relevant-checks-rerun", action="store_true")
    parser.add_argument("--checkpoint-updated", action="store_true")
    parser.add_argument("--unrelated-changes-preserved", action="store_true")
    parser.add_argument("--recovery-evidence-reference")
    parser.add_argument("--same-name-project-override")
    parser.add_argument("--other-workflows-or-rules")
    parser.add_argument("--first-confusing-step", required=True)
    parser.add_argument("--limitations-and-redactions", required=True)
    parser.add_argument("--manual-interventions")
    parser.add_argument("--failed-or-abandoned-attempts")
    args = parser.parse_args(argv)

    try:
        prepared = record_live_trial.load_prepared(args.input)
        result = build_result(
            prepared,
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
            doctor_evidence=args.doctor_evidence,
            fresh_conversation_confirmed=args.fresh_conversation_confirmed,
            live_bob_observed=args.live_bob_observed,
            rule_loaded=args.rule_loaded,
            skill_loaded=args.skill_loaded,
            fixture_commit=args.fixture_commit,
            baseline_report=args.baseline_report,
            candidate_report=args.candidate_report,
            diff=args.diff,
            manual_acceptance=args.manual_acceptance,
            current_files_inspected=args.current_files_inspected,
            historical_evidence_revalidated=args.historical_evidence_revalidated,
            teammate_changes_preserved=args.teammate_changes_preserved,
            workflow_evidence_reference=args.workflow_evidence_reference,
            interruption_type=args.interruption_type,
            handoff_read=args.handoff_read,
            current_state_reconciled=args.current_state_reconciled,
            stale_historical_evidence_detected=args.stale_historical_evidence_detected,
            relevant_checks_rerun=args.relevant_checks_rerun,
            checkpoint_updated=args.checkpoint_updated,
            unrelated_changes_preserved=args.unrelated_changes_preserved,
            recovery_evidence_reference=args.recovery_evidence_reference,
            same_name_project_override=args.same_name_project_override,
            other_workflows_or_rules=args.other_workflows_or_rules,
            first_confusing_step=args.first_confusing_step,
            limitations_and_redactions=args.limitations_and_redactions,
            manual_interventions=args.manual_interventions,
            failed_or_abandoned_attempts=args.failed_or_abandoned_attempts,
        )
        prepare_live_trial.write_new(args.output, result)
    except (CompletionError, record_live_trial.RecordingError,
            prepare_live_trial.PreparationError) as error:
        print(json.dumps({"created": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({
        "created": True,
        "path": str(args.output),
        "status": result["status"],
        "claim_level": result["claim_level"],
        "run_id": result["run_id"],
        "scenario": result["task"]["scenario"],
        "kit_commit": result["kit"]["commit"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
