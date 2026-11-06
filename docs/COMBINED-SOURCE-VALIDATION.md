# Combined evaluator source — local offline integration evidence

This is a local source-layout integration, not publication, release approval,
live Bob/model behavior, a participant result, or memory-backend qualification.

## Inputs and reconciliation

The combined branch starts at accepted source-layout merge
`c48c2f8d3e397d8ea5b74bc1fc387444930a82b6`. Current reviewed prerequisites
#4–#10 were merged in order, retaining #3 ancestry, followed by corrected memory
source `c1b471a0658989e4341ad7fcf194d91e93b284fc`. The resulting source merge is
`99e8cab3f2c4e1f9e4766b4eb8cd7b6f10662850`.
No reset, squash, source-main change or monorepo integration edit was used.

Conflicts in CONTRIBUTING, README, protocol, fixture index and validation were
resolved by retaining the full task journey plus the optional memory task.
The evaluator retains all eleven registrations. Its single memory registration
uses the common protected-file and candidate-scope machinery with corrected
17-test/14-failure semantics. The memory source's `only_allowed_changes` report
field is retained conditionally as an alias of the common scope verdict.
The reminder state-bound set is retained in full and extended with memory.

The first combined helper run executed 133 tests but had two errors: memory's
positive and scope-negative controls expected the `only_allowed_changes` report
field. Adding that conditional compatibility field corrected both errors; no
test assertions or fixture bytes were changed to obtain a pass.

## Actual offline execution

Executed on Linux, Python 3.13.5, using `/usr/bin/python3 -B -W
error::ResourceWarning -m unittest discover -s tests -v`:

- 133 helper tests passed, exit 0, no skips or resource warnings; unittest
  reported 34.774 seconds on the corrected merged code.
- Separate real CLI memory baseline: 17 checks, exactly 14 failures,
  `expected_baseline_failure`, exit 0.
- Separate disposable repaired memory control: 17 checks passed,
  `public_tests_passed`, exit 0; only adapter and handoff changed.
- Separate reminder implementation baseline: 10 checks, exactly four failures,
  `expected_baseline_failure`, exit 0.
- Separate disposable repaired reminder implementation: 10 checks passed,
  `public_tests_passed`, exit 0.
- Both baseline and repaired internal-result attempts for each of those two
  tasks returned exit 2, created no result, and left workspace bytes unchanged.

The helper suite additionally executes the inherited-writer watchdog, current
release-readiness controls, memory scope/fresh-process/write-failure controls,
and disabled Engram preview checks. Positive candidates are software controls
from repository-owned test code, not agent work or actual backend adoption.
All child execution used an allowlisted nonsecret environment and disposable
HOME/TMPDIR beneath existing scratch. No network, Bob/model, install, service or
backend execution occurred. This is not an OS network/security sandbox.

## Preservation and attribution

Exact Git-object comparisons established:

- All 118 old source fixture/task/helper-test files at `c48c2f8` are unchanged.
- All 136 current #10 fixture/task/helper-test files are unchanged.
- All 12 corrected memory fixture/task/new-helper-test files are unchanged.
- The fixture index is the sole intentionally edited `fixtures/` index file;
  no original deliberately faulty source was repaired, including memory_adapter.
- `_run_bounded_process` is source-byte-identical to reviewed #10, as is the
  entire helper test file containing its independently supervised watchdog.
- All pinned reviewed source heads and corrected #11/#12 heads are ancestors.

Historical validation bodies are preserved verbatim, not relabelled as fresh
combined observations:

- [Pre-refresh source](HISTORICAL-VALIDATION-pre-refresh.md): exact body from
  `c48c2f8:VALIDATION.md`, including historical 80/91/103 assertions.
- [Pre-refresh monorepo fork](HISTORICAL-VALIDATION-pre-refresh-fork.md): exact body
  from `61b55be389cac60c718f1c0e28e0e0becee90678:evals/VALIDATION.md`, including its
  separate local-port attribution. Its historical relative links retain their
  original root-file context.
- [Corrected memory source](HISTORICAL-VALIDATION-memory-source.md): exact body
  from `c1b471a:VALIDATION.md`, including the separate correction appendix.

The main validation file retains upstream #10's reconciled observations as
upstream history. Those counts are not fresh combined-tree observations.
Machine-readable ancestry, byte-preservation, CLI reports and full suite logs
are retained outside the product tree in the parent's refresh evidence folder.

## Limits

Memory remains a conditional local fixture, not a default/personal capture path.
Engram preview remains disabled and optional; no backend was started or
qualified. Manual/semantic acceptance, hosted CI, native Windows/macOS,
concurrent atomic CAS and production durability remain unqualified. Source
success does not qualify an unbuilt future consolidated subtree. Parent owns
subtree/fork mapping and provenance updates after accepting this exact source.
Prowl was unavailable; bounded local Git objects and AST inspection were used.
