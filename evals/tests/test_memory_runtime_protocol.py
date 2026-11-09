"""Controls for the non-executing project-memory runtime evidence protocol."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "results" / "memory-runtime-trial-template.json"
SCRIPT = ROOT / "scripts" / "validate_memory_trial.py"


class MemoryRuntimeProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    def write_and_validate(self, record: dict) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory(prefix="memory-trial-record-") as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            before = path.read_bytes()
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPT), str(path)],
                cwd=str(ROOT), text=True, capture_output=True, timeout=10, check=False,
            )
            self.assertEqual(path.read_bytes(), before)
            return result

    def executed(self, decision: str = "qualified", client: str = "direct_mcp") -> dict:
        record = copy.deepcopy(self.record)
        record["run_id"] = "constructed-runtime-control"
        record["source"]["asset_digest_verified"] = True
        record["authorization"] = {
            "third_party_execution_authorized": True,
            "authorization_reference": "reviewed authorization record",
        }
        record["environment"].update({
            "operating_system": "constructed-os",
            "architecture": "constructed-arch",
            "client": client,
            "client_mode": "direct_mcp" if client == "direct_mcp" else "ide_interactive",
            "workspace_trust": "not_applicable_direct" if client == "direct_mcp" else "explicit_trust",
        })
        record["side_effects"] = {
            "processes": ["observed process lifecycle"],
            "files": ["observed project-local files"],
            "network": ["observed no network after startup"],
            "model_downloads": ["observed no model download"],
            "mcp_initialization_instructions": ["observed no initialization instructions"],
        }
        for item in record["behaviors"]:
            item["status"] = "pass"
            item["evidence"] = f"constructed evidence for {item['behavior']}"
        record["cleanup"] = {
            "attempted": True,
            "processes_stopped": True,
            "project_files_removed": True,
            "machine_state_removed_or_absent": True,
            "notes": "constructed cleanup evidence",
        }
        record["decision"] = decision
        record["decision_rationale"] = "constructed decision control"
        record["claims"]["backend_runtime_qualified"] = decision == "qualified"
        record["limitations"] = ["Constructed validator control; not a real backend result."]
        return record

    def test_not_run_template_is_valid_and_claims_nothing(self) -> None:
        result = self.write_and_validate(self.record)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("decision=not_run", result.stdout)
        self.assertFalse(self.record["authorization"]["third_party_execution_authorized"])
        self.assertFalse(any(self.record["claims"].values()))

    def test_profiles_and_contract_are_pinned_in_protocol(self) -> None:
        protocol = json.loads(
            (ROOT / "qualifications" / "memory-runtime-trial-v1" / "protocol.json").read_text(encoding="utf-8")
        )
        self.assertEqual(protocol["allowed_backend_profiles"], [
            "qualifications/engram-v0.11.0/profile.json",
            "qualifications/basic-memory-v1.0.0/profile.json",
        ])
        contract = json.loads((ROOT / protocol["contract_path"]).read_text(encoding="utf-8"))
        self.assertEqual([item["behavior"] for item in self.record["behaviors"]], contract["required_behaviors"])

    def test_wrong_profile_digest_is_rejected(self) -> None:
        self.record["source"]["asset_sha256"] = "0" * 64
        result = self.write_and_validate(self.record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("asset digest", result.stderr)

    def test_same_template_can_bind_exact_basic_memory_profile(self) -> None:
        self.record.update({
            "backend_profile": "qualifications/basic-memory-v1.0.0/profile.json",
            "backend_qualification_id": "basic-memory-v1.0.0-source-gate",
        })
        self.record["source"].update({
            "commit": "c9bd187b83baba549d5cd16bacc180f8023d51c8",
            "asset_sha256": "a2d2c1589616c9599aec9edd6597d508028c5af88632312fc0990dcaccf02867",
        })
        result = self.write_and_validate(self.record)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("decision=not_run", result.stdout)

    def test_unauthorized_execution_claim_is_rejected(self) -> None:
        record = self.executed()
        record["authorization"] = {
            "third_party_execution_authorized": False,
            "authorization_reference": None,
        }
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit third-party execution authorization", result.stderr)

    def test_executed_record_requires_host_and_matching_client_mode(self) -> None:
        record = self.executed()
        record["run_id"] = None
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("non-empty run_id", result.stderr)
        for key in ("operating_system", "architecture"):
            with self.subTest(key=key):
                record = self.executed()
                record["environment"][key] = None
                result = self.write_and_validate(record)
                self.assertEqual(result.returncode, 2)
                self.assertIn(f"environment.{key}", result.stderr)
        record = self.executed()
        record["environment"]["client_mode"] = "ide_interactive"
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("direct_mcp client requires direct_mcp client_mode", result.stderr)

    def test_global_settings_or_automatic_approval_are_rejected(self) -> None:
        for safeguard in ("global_settings_changed", "automatic_tool_approval"):
            with self.subTest(safeguard=safeguard):
                record = copy.deepcopy(self.record)
                record["safeguards"][safeguard] = True
                result = self.write_and_validate(record)
                self.assertEqual(result.returncode, 2)
                self.assertIn(safeguard, result.stderr)

    def test_missing_duplicate_or_reordered_behaviors_are_rejected(self) -> None:
        for behaviors in (
            self.record["behaviors"][:-1],
            self.record["behaviors"][:-1] + [copy.deepcopy(self.record["behaviors"][0])],
            list(reversed(self.record["behaviors"])),
        ):
            with self.subTest(length=len(behaviors), first=behaviors[0]["behavior"]):
                record = copy.deepcopy(self.record)
                record["behaviors"] = behaviors
                result = self.write_and_validate(record)
                self.assertEqual(result.returncode, 2)
                self.assertIn("contract order", result.stderr)

    def test_qualified_requires_all_pass_with_evidence(self) -> None:
        for mutation in ("blocked_status", "missing_evidence"):
            with self.subTest(mutation=mutation):
                record = self.executed()
                if mutation == "blocked_status":
                    record["behaviors"][5]["status"] = "blocked"
                else:
                    record["behaviors"][5]["evidence"] = ""
                result = self.write_and_validate(record)
                self.assertEqual(result.returncode, 2)
                self.assertTrue("every contract behavior" in result.stderr or "requires evidence" in result.stderr)

    def test_qualified_requires_side_effects_and_complete_cleanup(self) -> None:
        for field in ("network", "model_downloads", "mcp_initialization_instructions"):
            with self.subTest(field=field):
                record = self.executed()
                record["side_effects"][field] = []
                result = self.write_and_validate(record)
                self.assertEqual(result.returncode, 2)
                self.assertIn("requires process, file, network", result.stderr)
        record = self.executed()
        record["cleanup"]["machine_state_removed_or_absent"] = False
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("complete observed cleanup", result.stderr)

    def test_blocked_record_requires_a_named_nonpass(self) -> None:
        record = self.executed(decision="blocked")
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("failed or blocked behavior", result.stderr)
        record["behaviors"][8]["status"] = "blocked"
        record["behaviors"][8]["evidence"] = "indexed deletion remained visible"
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("decision=blocked", result.stdout)

    def test_any_executed_bob_record_requires_version_trust_and_live_observation(self) -> None:
        record = self.executed(decision="blocked", client="ibm_bob")
        record["behaviors"][8]["status"] = "blocked"
        record["behaviors"][8]["evidence"] = "indexed deletion remained visible"
        record["claims"]["live_bob_observed"] = True
        record["environment"]["client_version"] = "constructed-version"
        for section, key, value, message in (
            ("environment", "client_version", None, "client version"),
            ("environment", "workspace_trust", "not_assessed", "explicit workspace trust"),
            ("claims", "live_bob_observed", False, "live_bob_observed true"),
        ):
            with self.subTest(key=key):
                candidate = copy.deepcopy(record)
                candidate[section][key] = value
                result = self.write_and_validate(candidate)
                self.assertEqual(result.returncode, 2)
                self.assertIn(message, result.stderr)
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 0, result.stderr)

        incomplete = copy.deepcopy(record)
        incomplete["decision"] = "incomplete"
        incomplete["decision_rationale"] = "constructed incomplete Bob observation"
        result = self.write_and_validate(incomplete)
        self.assertEqual(result.returncode, 0, result.stderr)

        noninteractive = copy.deepcopy(record)
        noninteractive["environment"]["client_mode"] = "shell_non_interactive"
        result = self.write_and_validate(noninteractive)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pre-approves tools", result.stderr)

    def test_production_readiness_can_never_be_claimed(self) -> None:
        record = self.executed()
        record["claims"]["production_ready"] = True
        result = self.write_and_validate(record)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot establish production readiness", result.stderr)


if __name__ == "__main__":
    unittest.main()
