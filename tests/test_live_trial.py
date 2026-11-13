"""Fail-closed controls for the manual live-Bob trial record."""

from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tools import prepare_live_trial as preparer
from tools import record_live_trial as recorder
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


class LiveTrialPreparationTests(unittest.TestCase):
    def test_prepared_record_binds_checkout_without_claiming_execution(self):
        commit = "1" * 40
        with mock.patch.object(preparer, "current_git_commit", return_value=commit):
            record = preparer.build_record(task_id="parcel-resume-v1",
                                           scenario="interruption_recovery")
        self.assertEqual(record["status"], "not_run")
        self.assertEqual(record["claim_level"], "unexecuted")
        self.assertEqual(record["kit"]["commit"], commit)
        self.assertEqual(record["kit"]["version"],
                         preparer.VERSION.read_text(encoding="utf-8").strip())
        self.assertEqual(record["task"]["id"], "parcel-resume-v1")
        self.assertEqual(record["task"]["scenario"], "interruption_recovery")
        self.assertIsNone(record["configuration"]["live_bob_observed"])
        self.assertEqual(validator.validate(record), [])

    def test_explicit_archive_identity_is_preserved(self):
        record = preparer.build_record(task_id="tiny-ledger", scenario="small_repair",
                                       kit_commit="2" * 40, archive_sha256="3" * 64)
        self.assertEqual(record["kit"]["commit"], "2" * 40)
        self.assertEqual(record["kit"]["archive_sha256"], "3" * 64)
        self.assertEqual(record["recovery_observations"]["status"], "not_assessed")
        self.assertEqual(validator.validate(record), [])

    def test_archive_without_explicit_commit_fails_closed(self):
        with mock.patch.object(preparer, "current_git_commit",
                               side_effect=preparer.PreparationError("history unavailable")):
            with self.assertRaises(preparer.PreparationError):
                preparer.build_record(task_id="tiny-ledger", scenario="small_repair")

    def test_invalid_identity_or_task_is_rejected(self):
        cases = [
            {"task_id": "", "scenario": "small_repair", "kit_commit": "1" * 40},
            {"task_id": "task", "scenario": "unknown", "kit_commit": "1" * 40},
            {"task_id": "task", "scenario": "small_repair", "kit_commit": "short"},
            {"task_id": "task", "scenario": "small_repair", "kit_commit": "1" * 40,
             "archive_sha256": "not-a-digest"},
        ]
        for values in cases:
            with self.subTest(values=values), self.assertRaises(preparer.PreparationError):
                preparer.build_record(**values)

    def test_write_refuses_overwrite_and_preserves_template(self):
        template_before = TEMPLATE.read_bytes()
        record = preparer.build_record(task_id="tiny-ledger", scenario="small_repair",
                                       kit_commit="4" * 40)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trial.json"
            preparer.write_new(path, record)
            created = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(created, record)
            with self.assertRaises(preparer.PreparationError):
                preparer.write_new(path, record)
        self.assertEqual(TEMPLATE.read_bytes(), template_before)

    def test_cli_creates_valid_record_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trial.json"
            arguments = ["--output", str(path), "--task-id", "tiny-ledger",
                         "--scenario", "small_repair", "--kit-commit", "5" * 40]
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(preparer.main(arguments), 0)
            self.assertEqual(validator.validate(json.loads(path.read_text(encoding="utf-8"))), [])
            before = path.read_bytes()
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(preparer.main(arguments), 1)
            self.assertEqual(path.read_bytes(), before)


class LiveTrialRecordingTests(unittest.TestCase):
    def prepared_record(self):
        return preparer.build_record(task_id="parcel-resume-v1",
                                     scenario="interruption_recovery",
                                     kit_commit="6" * 40)

    def result_arguments(self, **overrides):
        values = {
            "status": "blocked",
            "claim_level": "installation_only",
            "run_id": "parcel-blocked-001",
            "observed_at_utc": "2026-11-13T08:00:00Z",
            "bob_interface": "shell_interactive",
            "bob_version": "recorded-version",
            "bob_mode": "agent",
            "os_name": "Linux",
            "python_version": "3.12.14",
            "execution_host_type": "local-disposable",
            "workspace_trust_decision": "trust_folder",
            "workspace_trust_evidence": "Trust dialog accepted for the fixture only.",
            "native_loading_evidence": "No loading observed; picker remained empty.",
            "installation_status": "healthy",
            "doctor_evidence": "doctor reported healthy",
            "fresh_conversation_confirmed": True,
            "live_bob_observed": True,
            "first_confusing_step": "The installed skill did not appear in the picker.",
            "limitations_and_redactions": "Public fixture only; local paths removed.",
        }
        values.update(overrides)
        return values

    def test_blocked_result_is_created_from_prepared_record(self):
        prepared = self.prepared_record()
        before = deepcopy(prepared)
        result = recorder.build_result(prepared, **self.result_arguments())
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["claim_level"], "installation_only")
        self.assertEqual(result["kit"], prepared["kit"])
        self.assertEqual(result["task"]["id"], "parcel-resume-v1")
        self.assertEqual(result["task"]["scenario"], "interruption_recovery")
        self.assertEqual(result["task"]["manual_acceptance"], "not_assessed")
        self.assertEqual(result["recovery_observations"]["status"], "not_assessed")
        self.assertEqual(validator.validate(result), [])
        self.assertEqual(prepared, before)

    def test_loading_observed_requires_matching_loading_evidence(self):
        prepared = self.prepared_record()
        with self.assertRaises(recorder.RecordingError):
            recorder.build_result(
                prepared, **self.result_arguments(claim_level="loading_observed"))
        result = recorder.build_result(
            prepared, **self.result_arguments(
                status="incomplete", claim_level="loading_observed", skill_loaded=True))
        self.assertEqual(result["status"], "incomplete")
        self.assertTrue(result["configuration"]["global_skill_observed_loaded"])
        self.assertEqual(validator.validate(result), [])

    def test_lower_claim_rejects_loading_flags(self):
        with self.assertRaises(recorder.RecordingError):
            recorder.build_result(
                self.prepared_record(), **self.result_arguments(rule_loaded=True))

    def test_recording_requires_explicit_observation_confirmations(self):
        for key in ("fresh_conversation_confirmed", "live_bob_observed"):
            with self.subTest(key=key), self.assertRaises(recorder.RecordingError):
                recorder.build_result(
                    self.prepared_record(), **self.result_arguments(**{key: False}))

    def test_recording_rejects_nonprepared_input_and_false_healthy_status(self):
        executed = self.prepared_record()
        executed.update(status="blocked", claim_level="installation_only")
        with self.assertRaises(recorder.RecordingError):
            recorder.build_result(executed, **self.result_arguments())
        with self.assertRaises(recorder.RecordingError):
            recorder.build_result(
                self.prepared_record(), **self.result_arguments(doctor_evidence=None))

    def test_load_rejects_invalid_or_executed_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaises(recorder.RecordingError):
                recorder.load_prepared(path)
            path.write_text(json.dumps(completed_record()), encoding="utf-8")
            with self.assertRaises(recorder.RecordingError):
                recorder.load_prepared(path)

    def test_cli_writes_new_result_without_changing_or_replacing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepared_path = Path(tmp) / "prepared.json"
            output_path = Path(tmp) / "blocked.json"
            prepared = self.prepared_record()
            prepared_path.write_text(json.dumps(prepared), encoding="utf-8")
            source_before = prepared_path.read_bytes()
            arguments = [
                "--input", str(prepared_path), "--output", str(output_path),
                "--status", "blocked", "--claim-level", "installation_only",
                "--run-id", "parcel-blocked-001",
                "--observed-at-utc", "2026-11-13T08:00:00Z",
                "--bob-interface", "shell_interactive",
                "--bob-version", "recorded-version", "--bob-mode", "agent",
                "--os", "Linux", "--python-version", "3.12.14",
                "--execution-host-type", "local-disposable",
                "--workspace-trust-decision", "trust_folder",
                "--workspace-trust-evidence", "Fixture trust dialog accepted.",
                "--native-loading-evidence", "Picker remained empty.",
                "--installation-status", "healthy",
                "--doctor-evidence", "doctor reported healthy",
                "--fresh-conversation-confirmed", "--live-bob-observed",
                "--first-confusing-step", "Skill absent from picker.",
                "--limitations-and-redactions", "Public fixture; paths removed.",
            ]
            output = io.StringIO()
            errors = io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(recorder.main(arguments), 0)
            result = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(validator.validate(result), [])
            self.assertEqual(prepared_path.read_bytes(), source_before)
            result_before = output_path.read_bytes()
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(recorder.main(arguments), 1)
            self.assertEqual(output_path.read_bytes(), result_before)


if __name__ == "__main__":
    unittest.main()
