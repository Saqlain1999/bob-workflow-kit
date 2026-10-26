"""Integration checks for the offline helper, separate from fixture tests."""

import importlib.util
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate.py"
FIXTURE = ROOT / "fixtures" / "tiny-ledger"
SPEC = importlib.util.spec_from_file_location("evaluate_output_tests", SCRIPT)
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class EvaluationHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="bob-eval-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.workspace = self.directory / "candidate"

    def invoke(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, arguments)],
            cwd=str(ROOT), env=environment, text=True, capture_output=True,
            timeout=10, check=False,
        )

    def copy_fixture(self) -> None:
        shutil.copytree(FIXTURE, self.workspace)

    def test_prepare_copies_fixture_and_refuses_overwrite(self) -> None:
        first = self.invoke("prepare", "--output", self.workspace)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(
            (self.workspace / "ledger.py").read_bytes(),
            (FIXTURE / "ledger.py").read_bytes(),
        )
        marker = self.workspace / "my-work.txt"
        marker.write_text("preserve this", encoding="utf-8")
        second = self.invoke("prepare", "--output", self.workspace)
        self.assertEqual(second.returncode, 2)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve this")

    def test_prepare_refuses_a_directory_inside_original_fixture(self) -> None:
        destination = FIXTURE / "must-not-be-created"
        self.assertFalse(destination.exists())
        result = self.invoke("prepare", "--output", destination)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(destination.exists())

    def test_baseline_confirms_known_failure_and_writes_report(self) -> None:
        self.copy_fixture()
        destination = self.directory / "baseline.json"
        result = self.invoke(
            "baseline", "--workspace", self.workspace, "--result", destination
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "expected_baseline_failure")
        self.assertEqual(report["tests"]["tests_run"], 9)
        self.assertEqual(len(report["tests"]["failures"]), 1)
        self.assertEqual(report["tests"]["errors"], [])
        self.assertEqual(report["manual_acceptance"], "not_assessed")
        self.assertEqual(report["model_calls_made_by_helper"], 0)

    def test_faulty_candidate_fails_public_checks(self) -> None:
        self.copy_fixture()
        result = self.invoke("candidate", "--workspace", self.workspace)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "public_tests_failed")
        self.assertIn("FAIL:", report["tests"]["output"])

    def test_focused_repair_passes_but_does_not_claim_manual_acceptance(self) -> None:
        self.copy_fixture()
        source = self.workspace / "ledger.py"
        text = source.read_text(encoding="utf-8")
        old = (
            "        self._balances[source] = source_balance - cents\n"
            "        destination_balance = self.balance(destination)\n"
        )
        new = (
            "        destination_balance = self.balance(destination)\n"
            "        self._balances[source] = source_balance - cents\n"
        )
        self.assertEqual(text.count(old), 1)
        source.write_text(text.replace(old, new), encoding="utf-8")
        candidate = self.invoke("candidate", "--workspace", self.workspace)
        self.assertEqual(candidate.returncode, 0, candidate.stderr)
        report = json.loads(candidate.stdout)
        self.assertEqual(report["status"], "public_tests_passed")
        self.assertEqual(report["tests"]["tests_run"], 9)
        self.assertEqual(report["tests"]["failures"], [])
        self.assertFalse(report["fingerprints"]["source_matches_original"])
        self.assertTrue(report["fingerprints"]["workspace_tests_match_original"])
        self.assertEqual(report["manual_acceptance"], "not_assessed")
        baseline = self.invoke("baseline", "--workspace", self.workspace)
        self.assertEqual(baseline.returncode, 1)
        self.assertEqual(json.loads(baseline.stdout)["status"], "unexpected_baseline")
        self.assertIn(old, (FIXTURE / "ledger.py").read_text(encoding="utf-8"))

    def test_weakened_workspace_tests_do_not_hide_the_bug(self) -> None:
        self.copy_fixture()
        tests = self.workspace / "tests" / "test_ledger.py"
        tests.write_text("# Removed by the candidate\n", encoding="utf-8")
        result = self.invoke("candidate", "--workspace", self.workspace)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["tests"]["tests_run"], 9)
        self.assertEqual(len(report["tests"]["failures"]), 1)
        self.assertFalse(report["fingerprints"]["workspace_tests_match_original"])

    def test_result_file_is_never_overwritten(self) -> None:
        self.copy_fixture()
        destination = self.directory / "existing.json"
        destination.write_text("keep prior evidence", encoding="utf-8")
        result = self.invoke(
            "baseline", "--workspace", self.workspace, "--result", destination
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(destination.read_text(encoding="utf-8"), "keep prior evidence")

    def test_timeout_reports_execution_problem_not_a_test_pass(self) -> None:
        self.copy_fixture()
        source = self.workspace / "ledger.py"
        source.write_text("while True:\n    pass\n", encoding="utf-8")
        result = self.invoke(
            "candidate", "--workspace", self.workspace, "--timeout", "0.5"
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "runner_error")
        self.assertIsNone(report["tests"])
        self.assertIn("timeout", report["error"])

    def test_oversized_candidate_stdout_is_an_explicit_non_pass(self) -> None:
        self.copy_fixture()
        source = self.workspace / "ledger.py"
        source.write_text(
            "import os\nos.write(1, b'x' * 300000)\n" + source.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        result = self.invoke("candidate", "--workspace", self.workspace)
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "resource_limit_exceeded")
        self.assertEqual(report["resource_limit"]["channel"], "worker_stdout")
        self.assertEqual(
            report["resource_limit"]["limit_bytes"],
            HELPER.DIAGNOSTIC_LIMIT_BYTES,
        )
        self.assertGreater(
            report["resource_limit"]["bytes_seen"],
            HELPER.DIAGNOSTIC_LIMIT_BYTES,
        )
        self.assertIsNone(report["tests"])
        self.assertNotEqual(report["status"], "public_tests_passed")

    def test_invalid_timeout_does_not_disable_the_execution_bound(self) -> None:
        self.copy_fixture()
        for value in ("0", "-1", "nan", "inf"):
            with self.subTest(timeout=value):
                result = self.invoke(
                    "candidate", "--workspace", self.workspace, "--timeout", value
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("finite and positive", result.stderr)


class OutputLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="bob-output-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.environment = dict(os.environ)
        self.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def run_code(self, code: str, limit: int = 64, timeout: float = 2.0):
        return HELPER._run_bounded_process(
            [sys.executable, "-B", "-c", code],
            str(self.directory), self.environment, timeout, limit,
        )

    def test_stdout_exact_limit_is_retained_and_limit_plus_one_is_rejected(self) -> None:
        exact = self.run_code("import os; os.write(1, b'x' * 64)")
        self.assertEqual(exact["returncode"], 0)
        self.assertEqual(exact["stdout"], "x" * 64)
        self.assertEqual(exact["limit_exceeded_channels"], [])

        oversized = self.run_code("import os; os.write(1, b'x' * 65)")
        self.assertIn("stdout", oversized["limit_exceeded_channels"])
        self.assertEqual(len(oversized["stdout"]), 64)
        self.assertGreater(oversized["bytes_seen"]["stdout"], 64)

    def test_stderr_and_simultaneous_channels_are_drained_without_deadlock(self) -> None:
        stderr = self.run_code("import os; os.write(2, b'e' * 65)")
        self.assertIn("stderr", stderr["limit_exceeded_channels"])
        self.assertLessEqual(len(stderr["stderr"]), 64)

        both = self.run_code(
            "import os, threading; "
            "a=threading.Thread(target=lambda: os.write(1, b'o' * 65536)); "
            "b=threading.Thread(target=lambda: os.write(2, b'e' * 65536)); "
            "a.start(); b.start(); a.join(); b.join()",
        )
        self.assertTrue(both["limit_exceeded_channels"])
        self.assertLessEqual(len(both["stdout"]), 64)
        self.assertLessEqual(len(both["stderr"]), 64)
        self.assertFalse(both["timed_out"])

    def test_invalid_utf8_is_replaced_and_nonzero_exit_is_preserved(self) -> None:
        result = self.run_code("import os; os.write(1, b'\\xffbad'); raise SystemExit(7)")
        self.assertEqual(result["returncode"], 7)
        self.assertIn("\ufffd", result["stdout"])
        self.assertEqual(result["limit_exceeded_channels"], [])

    def test_timeout_reaps_the_direct_worker(self) -> None:
        result = self.run_code("while True: pass", timeout=0.1)
        self.assertTrue(result["timed_out"])
        self.assertIsNotNone(result["returncode"])

    def test_inherited_pipe_writer_returns_incomplete_without_hanging(self) -> None:
        descendant_pid = self.directory / "descendant.pid"
        worker_code = (
            "import pathlib, subprocess, sys; "
            "child=subprocess.Popen([sys.executable, '-B', '-c', "
            "'import time; time.sleep(20)']); "
            f"pathlib.Path({str(descendant_pid)!r}).write_text(str(child.pid), encoding='utf-8')"
        )
        probe = self.directory / "probe.py"
        probe.write_text(textwrap.dedent(f"""
            import importlib.util
            import json
            import os
            import sys

            spec = importlib.util.spec_from_file_location("evaluate_probe", {str(SCRIPT)!r})
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
            result = helper._run_bounded_process(
                [sys.executable, "-B", "-c", {worker_code!r}],
                {str(self.directory)!r}, dict(os.environ), 0.2, 64,
            )
            print(json.dumps(result))
        """), encoding="utf-8")

        process = subprocess.Popen(
            [sys.executable, "-B", str(probe)],
            cwd=self.directory, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        timed_out = False
        try:
            stdout, stderr = process.communicate(timeout=6)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            stdout, stderr = process.communicate(timeout=2)
        finally:
            if descendant_pid.is_file():
                pid = int(descendant_pid.read_text(encoding="utf-8"))
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/PID", str(pid), "/T", "/F"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        timeout=5, check=False,
                    )
                else:
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

        self.assertFalse(timed_out, stderr)
        self.assertEqual(process.returncode, 0, stderr)
        result = json.loads(stdout)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["capture_incomplete_channels"], ["stdout", "stderr"])
        self.assertFalse(result["timed_out"])

    def test_unittest_diagnostics_are_bounded_with_multibyte_text(self) -> None:
        stream = HELPER._BoundedTextBuffer(64)

        class NoisyFailure(unittest.TestCase):
            def runTest(self) -> None:
                self.fail("€" * 100)

        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
            unittest.TestSuite([NoisyFailure()])
        )
        self.assertFalse(result.wasSuccessful())
        self.assertTrue(stream.exceeded)
        self.assertGreater(stream.bytes_seen, 64)
        self.assertLessEqual(len(stream._buffer), 64)

    def test_worker_report_read_has_an_exact_byte_boundary(self) -> None:
        report = self.directory / "worker.json"
        report.write_bytes(b"x" * 32)
        content, exceeded = HELPER._read_bounded(report, 32)
        self.assertEqual(content, b"x" * 32)
        self.assertFalse(exceeded)

        report.write_bytes(b"x" * 33)
        content, exceeded = HELPER._read_bounded(report, 32)
        self.assertEqual(content, b"x" * 32)
        self.assertTrue(exceeded)


if __name__ == "__main__":
    unittest.main()
