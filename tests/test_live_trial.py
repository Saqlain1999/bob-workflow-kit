"""Fail-closed controls for the manual live-Bob trial record."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools import validate_live_trial as validator


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs/live-trial-template.json"


def completed_record():
    record = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    record.update({
        "status": "completed",
        "claim_level": "task_observed",
        "run_id": "public-ledger-001",
        "observed_at_utc": "2026-11-10T08:00:00Z",
    })
    record["kit"].update({"version": "0.1.0-alpha.7",
                          "commit": "e6f9beea5b0624a9369e32b8513910da0f0f0539"})
    record["bob"].update({"interface": "shell_interactive", "version": "recorded-version",
                          "mode": "agent"})
    record["environment"].update({"os": "Linux", "python_version": "3.12.14",
                                  "execution_host_type": "local-disposable"})
    record["configuration"].update({
        "fresh_conversation": True,
        "workspace_trust_decision": "trust_folder",
        "workspace_trust_evidence": "Interactive trust dialog accepted for fixture only.",
        "live_bob_observed": True,
        "global_rule_observed_loaded": True,
        "global_skill_observed_loaded": True,
        "native_loading_evidence": "Skills picker and activation event recorded.",
    })
    record["installation"].update({"status": "healthy", "doctor_evidence": "healthy"})
    record["task"].update({
        "id": "tiny-ledger",
        "scenario": "small_repair",
        "fixture_commit": "public-fixture-revision",
        "baseline_report": "9 tests; 1 expected failure",
        "candidate_report": "9 tests passed",
        "diff": "ledger.py only",
        "manual_acceptance": "accepted",
    })
    record["workflow_observations"].update({
        "current_files_inspected": True,
        "historical_evidence_revalidated": True,
        "teammate_changes_preserved": True,
        "evidence_reference": "public result bundle",
    })
    record["recovery_observations"].update({"status": "not_applicable"})
    return record


def recovery_record():
    record = completed_record()
    record["task"].update({"id": "parcel-resume-v1",
                           "scenario": "interruption_recovery"})
    record["recovery_observations"].update({
        "status": "observed",
        "interruption_type": "constructed_handoff",
        "handoff_read": True,
        "current_state_reconciled": True,
        "stale_historical_evidence_detected": True,
        "relevant_checks_rerun": True,
        "checkpoint_updated": True,
        "unrelated_changes_preserved": True,
        "evidence_reference": "public action record and acceptance checklist",
    })
    return record


class LiveTrialValidationTests(unittest.TestCase):
    def test_shipped_template_is_valid_not_run_and_unchanged(self):
        before = TEMPLATE.read_bytes()
        record = json.loads(before)
        self.assertEqual(validator.validate(record), [])
        self.assertEqual(TEMPLATE.read_bytes(), before)

    def test_complete_interactive_trial_is_accepted(self):
        self.assertEqual(validator.validate(completed_record()), [])

    def test_complete_recovery_trial_is_accepted(self):
        self.assertEqual(validator.validate(recovery_record()), [])

    def test_noninteractive_shell_is_rejected(self):
        record = completed_record()
        record["bob"]["interface"] = "shell_non_interactive"
        self.assertTrue(any("bob run is excluded" in error for error in validator.validate(record)))

    def test_missing_identity_trust_or_live_observation_is_rejected(self):
        base = completed_record()
        mutations = [
            ("run", lambda value: value.update(run_id=None)),
            ("host", lambda value: value["environment"].update(os=None)),
            ("trust", lambda value: value["configuration"].update(workspace_trust_decision=None)),
            ("observation", lambda value: value["configuration"].update(live_bob_observed=False)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                record = deepcopy(base)
                mutate(record)
                self.assertTrue(validator.validate(record))

    def test_completed_status_cannot_overclaim_missing_evidence(self):
        base = completed_record()
        mutations = [
            ("loading", lambda value: value["configuration"].update(global_skill_observed_loaded=False)),
            ("doctor-status", lambda value: value["installation"].update(status="blocked")),
            ("doctor-evidence", lambda value: value["installation"].update(
                doctor_evidence=None)),
            ("candidate", lambda value: value["task"].update(candidate_report=None)),
            ("preservation", lambda value: value["workflow_observations"].update(
                teammate_changes_preserved=False)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                record = deepcopy(base)
                mutate(record)
                self.assertTrue(validator.validate(record))

    def test_recovery_claim_requires_each_observation(self):
        base = recovery_record()
        mutations = [
            ("status", lambda value: value["recovery_observations"].update(status="partial")),
            ("type", lambda value: value["recovery_observations"].update(
                interruption_type=None)),
            ("handoff", lambda value: value["recovery_observations"].update(
                handoff_read=False)),
            ("current-state", lambda value: value["recovery_observations"].update(
                current_state_reconciled=False)),
            ("stale-evidence", lambda value: value["recovery_observations"].update(
                stale_historical_evidence_detected=False)),
            ("checks", lambda value: value["recovery_observations"].update(
                relevant_checks_rerun=False)),
            ("checkpoint", lambda value: value["recovery_observations"].update(
                checkpoint_updated=False)),
            ("preservation", lambda value: value["recovery_observations"].update(
                unrelated_changes_preserved=False)),
            ("evidence", lambda value: value["recovery_observations"].update(
                evidence_reference=None)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                record = deepcopy(base)
                mutate(record)
                self.assertTrue(validator.validate(record))

    def test_small_repair_cannot_be_labelled_as_observed_recovery(self):
        record = completed_record()
        record["recovery_observations"].update({"status": "observed"})
        self.assertTrue(validator.validate(record))

    def test_blocked_result_cannot_overclaim_observed_recovery(self):
        record = recovery_record()
        record.update(status="blocked", claim_level="loading_observed")
        record["recovery_observations"]["checkpoint_updated"] = False
        self.assertTrue(any("checkpoint_updated" in error
                            for error in validator.validate(record)))

    def test_blocked_result_stays_bounded(self):
        record = completed_record()
        record.update(status="blocked", claim_level="installation_only")
        self.assertEqual(validator.validate(record), [])
        record["claim_level"] = "task_observed"
        self.assertTrue(validator.validate(record))

    def test_cli_is_read_only(self):
        record = completed_record()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            before = path.read_bytes()
            self.assertEqual(validator.main([str(path)]), 0)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
