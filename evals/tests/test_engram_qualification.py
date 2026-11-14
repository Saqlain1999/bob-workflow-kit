"""Static and non-mutating controls for the pinned Engram qualification gate."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "qualifications" / "engram-v0.11.0" / "profile.json"
SCRIPT = ROOT / "scripts" / "preview_engram.py"
EXPECTED_COMMIT = "ed4fe24d97f16f1c362d0c4d6b74bfe4d2caf0c3"
EXPECTED_SHA256 = "287708d36f27d72dca86d45ea40d269fd57525e8ab8a987c5cf00837998bf8d5"


class EngramQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        self.temporary = tempfile.TemporaryDirectory(prefix="engram-preview-")
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.project = root / "project-alpha"
        self.project.mkdir()
        self.binary = root / "reviewed-bin" / "engram-alpha"

    def invoke(self, project: Path | str, binary: Path | str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--project", str(project), "--binary", str(binary)],
            cwd=str(ROOT), text=True, capture_output=True, timeout=10, check=False,
        )

    def test_source_pin_license_release_and_digest_are_exact(self) -> None:
        source = self.profile["source"]
        self.assertEqual(source["tag"], "v0.11.0")
        self.assertEqual(source["commit"], EXPECTED_COMMIT)
        self.assertEqual(source["license"], "MIT")
        self.assertEqual(source["release_published_utc"], "2026-11-01T00:05:43Z")
        self.assertEqual(source["asset"]["sha256"], EXPECTED_SHA256)

    def test_mapping_matches_internal_brief_contract_without_external_claim(self) -> None:
        mapping = self.profile["contract_mapping"][0]["candidate_mechanism"]
        self.assertNotIn("brief(project=", mapping)
        self.assertIn("brief with {}", mapping)
        self.assertEqual(self.profile["bob_trial_contract"]["first_tool_call"], {"tool": "brief", "arguments": {}})
        self.assertEqual(self.profile["source"]["external_verification"], "NOT RUN")

    def test_every_backend_neutral_behavior_has_one_honest_mapping(self) -> None:
        contract = json.loads(
            (ROOT / "fixtures" / "bob-project-memory" / "contract.json").read_text(encoding="utf-8")
        )
        mappings = self.profile["contract_mapping"]
        self.assertEqual([item["behavior"] for item in mappings], contract["required_behaviors"])
        self.assertEqual(len({item["behavior"] for item in mappings}), len(mappings))
        self.assertTrue(all(item["status"] != "qualified" for item in mappings))

    def test_revision_conflict_and_deletion_remain_blocked(self) -> None:
        status = {item["behavior"]: item["status"] for item in self.profile["contract_mapping"]}
        self.assertEqual(status["revision conflict refusal"], "blocked")
        self.assertEqual(status["direct and indexed deletion"], "blocked")
        self.assertEqual(self.profile["decision"], "adapt_after_runtime_qualification")

    def test_preview_is_project_local_disabled_and_has_no_auto_approval(self) -> None:
        result = self.invoke(self.project, self.binary)
        self.assertEqual(result.returncode, 0, result.stderr)
        preview = json.loads(result.stdout)
        self.assertEqual(preview["configuration_path"], str(self.project / ".bob" / "mcp.json"))
        server = preview["configuration"]["mcpServers"]["engram-alpha"]
        self.assertEqual(server["command"], str(self.binary))
        self.assertEqual(server["args"], ["mcp", "--db", str(self.project / ".engram" / "graph.db")])
        self.assertEqual(server["cwd"], str(self.project))
        self.assertTrue(server["disabled"])
        self.assertEqual(server["alwaysAllow"], [])
        self.assertNotIn("url", server)

    def test_preview_emits_brief_for_db_pinned_project(self) -> None:
        result = self.invoke(self.project, self.binary)
        preview = json.loads(result.stdout)
        self.assertEqual(
            preview["first_tool_call"],
            {"server": "engram-alpha", "tool": "brief", "arguments": {}},
        )

    def test_preview_does_not_write_or_start_a_process(self) -> None:
        before = sorted(path.relative_to(Path(self.temporary.name)) for path in Path(self.temporary.name).rglob("*"))
        result = self.invoke(self.project, self.binary)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = sorted(path.relative_to(Path(self.temporary.name)) for path in Path(self.temporary.name).rglob("*"))
        self.assertEqual(after, before)
        preview = json.loads(result.stdout)
        self.assertFalse(preview["writes_performed"])
        self.assertFalse(preview["processes_started"])
        self.assertFalse(self.binary.exists())

    def test_relative_project_or_binary_is_rejected(self) -> None:
        relative_project = self.invoke("relative-project", self.binary)
        self.assertEqual(relative_project.returncode, 2)
        self.assertIn("project must be an absolute path", relative_project.stderr)
        relative_binary = self.invoke(self.project, "engram-alpha")
        self.assertEqual(relative_binary.returncode, 2)
        self.assertIn("binary must be an absolute path", relative_binary.stderr)

    def test_first_trial_excludes_unsafe_or_unreviewed_modes(self) -> None:
        prohibited = "\n".join(self.profile["bob_trial_contract"]["prohibited_first_trial"])
        for expected in ("global Bob", "transcript", "hooks", "HTTP", "cloud", "private", "paid"):
            self.assertIn(expected, prohibited)
        self.assertIn("project folder explicitly trusted", "\n".join(self.profile["bob_trial_contract"]["prerequisites"]))

    def test_detached_core_and_removal_side_effects_are_not_hidden(self) -> None:
        effects = "\n".join(self.profile["runtime_side_effects_to_observe"])
        for expected in ("detached machine-local core", "mcp.log", "loopback", "registration", "download", "removal"):
            self.assertIn(expected, effects)


if __name__ == "__main__":
    unittest.main()
