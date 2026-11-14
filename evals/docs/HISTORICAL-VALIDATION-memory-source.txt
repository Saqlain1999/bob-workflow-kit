# Local software validation

## Engram Alpha v0.11.0 source qualification gate — 5 November 2026 (UTC)

The qualification record pins upstream source, release, licence, and Linux asset
digest, maps all ten backend-neutral memory behaviors to a candidate mechanism
or explicit gap, and renders a disabled project-only Bob MCP preview. Engram and
Bob were not installed or executed.

Observed on Linux with Python 3.12.14:

| Check | Observed result |
| --- | --- |
| Pinned source controls | Tag `v0.11.0`, commit `ed4fe24d97f16f1c362d0c4d6b74bfe4d2caf0c3`, MIT licence, 1 November release event, and published asset SHA-256 matched the reviewed profile |
| Contract mapping | All ten `bob-project-memory-v1` behaviors mapped once; none marked qualified; revision conflict and deletion remained blocked |
| Preview controls | Project-only `.bob/mcp.json`; absolute command/project paths; project-local database; explicit briefing; disabled by default; no automatic approvals |
| Preservation controls | No file was written, no process was started, and relative project/binary paths were rejected |
| Runtime-side-effect record | Detached local core, graph/log files, loopback metadata, project registration, downloads, stop and removal all remain explicit runtime observations |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **52/52 passed**, exit 0; no skips or resource warnings |

This is static source-review and preview-harness evidence. It is not Engram
runtime behavior, asset verification on a downloaded file, MCP initialization,
live Bob discovery or tool use, contract acceptance, backup erasure, privacy
compliance, or production readiness. A later disposable trial must verify the
asset digest independently and retain repository evidence as the outage
fallback.

## Backend-neutral project-memory fixture — 4 November 2026 (UTC)

The new `bob-project-memory-v1` fixture uses only constructed public data and
Python's standard library. Its two projects and explicit shared-lessons scope
exercise observable memory boundaries without installing or calling a real
backend.

Observed on Linux with Python 3.12.14:

| Check | Observed result |
| --- | --- |
| Prepared baseline | 12 trusted checks; exactly 10 named expected failures; helper status `expected_baseline_failure` |
| Disposable known-good control | 12/12 passed; protected inputs unchanged; only `memory_adapter.py` and `MEMORY_HANDOFF.md` changed |
| Negative controls | Missing handoff, protected-contract edit, test edit, unrelated file, and in-workspace result output were rejected |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **43/43 passed**, exit 0; no skips or resource warnings |

This is offline contract evidence, not a participant run. It does not establish
live Bob discovery or workflow-following, a third-party MCP/backend integration,
production durability, concurrent-process safety, privacy compliance, or
backup deletion. No model, Bob credential, network service, hook, transcript,
private project, or paid API was used.

## Inherited diagnostic-pipe follow-up — 26 October 2026 (UTC)

Blocking review finding EVAL-001 reproduced that the earlier branch could wait
on `BufferedReader.close()` after a direct worker exited while a descendant kept
an inherited diagnostic write end open. The 25 October fix switched the worker
diagnostic pipes to unbuffered raw streams, allowing cleanup to return the
existing incomplete-capture exit-2 result after the reader grace period. The
cross-platform follow-up also avoids closing a pipe whose daemon reader is still
blocked; that pipe is retained until the short-lived helper exits or the
uncontained descendant closes its inherited writer. It does not add descendant
containment.

Observed on Linux with Python 3.12.14:

| Check | Observed result |
| --- | --- |
| Independently supervised inherited-pipe probe | Returned incomplete stdout/stderr capture within the six-second watchdog; the 20-second descendant was explicitly killed by PID on POSIX and with `taskkill /T /F` on Windows |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **37/37 passed**, exit 0; no skips or resource warnings |
| Python and documentation checks | **11 Python files** parsed with Python 3.10 grammar; **2 JSON files** parsed; **18 local Markdown links** checked across **17 Markdown files**; `git diff --check` passed |

The revised watchdog removes the earlier Windows skip and is exercised by the
same six-job hosted matrix when that exact head runs. A passing test establishes
bounded helper return for this constructed case, not safe execution of hostile
code, general descendant cleanup, continuous resource containment, or live Bob
behavior.

## Bounded worker diagnostics — 13 October 2026 (UTC)

Observed on Linux (`Linux-6.18.44-x86_64-with-glibc2.39`), Python 3.12.14.
These are local software checks of the maintenance branch, not a Bob participant
run or a live-client compatibility result.

| Check | Observed result |
| --- | --- |
| `git diff --check` | Passed |
| `python3 -m py_compile scripts/evaluate.py tests/test_evaluate.py tests/test_parcel_resume.py` | Passed |
| `python3 -B -m unittest discover -s tests -v` | 36 helper tests passed; exit 0; no skips or resource warnings |
| 300,000-byte candidate stdout negative control | Status `resource_limit_exceeded`; exit 2; channel `worker_stdout`; `tests` remained `null` |
| Tiny Ledger disposable preparation and baseline | Nine trusted tests; one named expected failure; helper status `expected_baseline_failure` |
| Parcel Resume disposable preparation and baseline | Historical pass executed; current baseline had the two named failures; protected inputs matched |
| Independent disposable Parcel repair smoke | Ten trusted tests passed; protected inputs matched; before/after state stable; helper status `public_tests_passed` |

The new unit coverage checks stdout, stderr, simultaneous pipe draining,
exact-limit and limit-plus-one behavior, invalid UTF-8, nonzero exit, timeout and
direct-worker reaping, bounded multibyte unittest failure text, malformed worker
data, and the structured-report read boundary. Diagnostic exhaustion is an
explicit exit-2 non-pass; truncated evidence cannot become test acceptance.

The helper still is not a sandbox, a general memory quota, or descendant-process
containment. No Bob client, model, credential, network service, or paid API was
used. Hosted results for the final exact commit belong in the pull request so a
later documentation-only commit cannot inherit an earlier run.

## Parcel Resume addition — 10 October 2026 (UTC)

Observed on Linux (`Linux-6.18.44-x86_64-with-glibc2.39`), Python 3.12.14.
These are local software checks of the edited checkout, not a Bob participant
result or hosted CI qualification of the new change.

| Check | Observed result |
| --- | --- |
| `python3 -B -m unittest discover -s tests -v` | 27 helper tests passed; exit 0; no skips |
| Parcel preparation | Actual historical suite: ten tests, no failures/errors/skips; constructed checkpoint written afterwards |
| Parcel prepared baseline | Ten tests, the two named expected failures; helper status `expected_baseline_failure`, exit 0 |
| Independent disposable-copy repair smoke | Ten candidate tests passed; protected policy/note bytes matched; before/after state stable; helper exit 0 |
| Original Parcel fixture integrity during smoke | All original file hashes unchanged |

The independent smoke made pricing read the current threshold and made CSV
export delegate its delivery calculation to the quote API. It was a manual
software control, separate from the helper-test repair that updates both entry
points. Neither repair was made to the original fixture or presented as Bob's
work.

The helper suite retains all nine Tiny Ledger checks and adds 18 Parcel checks.
The new negative controls cover treating the historical pass as current,
repairing only one entry point, policy reversion, overwritten/deleted teammate
notes, weakened candidate tests, newly added runtime files, source/configuration
changes during the worker, redirected paths, malformed/skipped worker results,
timeout, preparation failure cleanup, result placement and fixed task selection.
Worker mutation cases produced passing tests but were rejected as unstable
current-state evidence. Policy/note changes also remained non-passes even when
the functional tests passed.

No Bob client or model was run. Token usage, cost, observed checkpoint use and
manual participant acceptance are unknown. The helper made zero model calls.
Native Windows/macOS execution and live Bob version compatibility remain
unverified. Python 3.10+ is the documented minimum; this new change was locally
executed on 3.12.14 only.

## Hosted Parcel Resume checks

[GitHub Actions run 38027907242](https://github.com/Saqlain1999/bob-workflow-evals/actions/runs/38027907242) passed for commit `8cf1bf67133b63f83b9f0ce268542b6e9f524404` on 10 October 2026 (UTC). Both Ubuntu jobs passed with Python 3.10 and 3.12, executing **Run helper tests in temporary workspaces** against the new helper and its 27-test suite. These hosted software checks establish no live Bob behavior or native Windows/macOS qualification.

## Previous Tiny Ledger preparation record

Recorded 10 October 2026 (Europe/Dublin). This is a local preparation record, not a participant benchmark result.

| Check | Observed result |
| --- | --- |
| Offline helper suite on Linux, Python 3.12.14 | 9 tests passed with exit code 0 |
| Original fixture baseline | Nine public tests; eight passed and the intended missing-recipient atomicity regression failed |
| Fixture integrity | All four fixture files matched the Workflow Kit example byte for byte |
| Participant result template | Parses as JSON; no-run status retained |

The helper suite exercises fresh preparation, preservation of existing files, the expected baseline, a failing candidate, a focused temporary repair, changed candidate tests, timeout reporting, and rejection of invalid timeout limits. A temporary repaired fixture inside a software test is not a live agent evaluation.

## Hosted publication checks for an earlier revision

[GitHub Actions run 38008089567](https://github.com/Saqlain1999/bob-workflow-evals/actions/runs/38008089567) completed successfully for published commit `7291d345aa9507cf5d4e07a1557959202ea922c6` on 10 October 2026 (UTC). Both helper-test jobs passed on `ubuntu-latest`, using Python 3.10 and 3.12. The recorded test step was **Run helper tests in temporary workspaces**.

These hosted software checks predate Parcel Resume and do not qualify the new
change. They are separate from local preparation and participant benchmarks.
Native Windows/macOS execution, live Bob behavior, and large-repository
evaluations are not established by this record.

Use the [evaluation protocol](docs/protocol.md) to collect an actual participant run. Keep helper test results, participant behavior, and manual acceptance separate.


## Local memory-gate corrections — separate follow-up evidence

This section corrects the automatic gate and its disposable positive control on
top of exact source `4dff443f9ee51d0d9862aa29ff605f7d802d6ad6`.
All preceding historical prose and counts are preserved, not re-attributed to
this revision. The intentionally faulty packaged `memory_adapter.py`, protected
contract, and both evidence documents remain byte-identical to that source.

Observed locally on Linux, `/usr/bin/python3` **3.13.5**:

| Check | Actual result |
| --- | --- |
| Full source helper suite, `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **54/54 passed**, exit 0, 13.925 s; no skips or emitted resource warnings |
| Direct prepared memory baseline | **17 trusted tests, exactly 14 named failures**, no errors/skips; helper exit 0 / `expected_baseline_failure` means intended defects reproduced |
| Direct repaired disposable control | **17/17 passed**, exit 0 / `public_tests_passed`; only adapter and handoff changed, protected bytes preserved, before/after state stable |
| Existing negative controls | Missing handoff, protected contract edit, weakened candidate tests, unrelated file and in-candidate result path still rejected |
| New process-local-only negative control | Rejected specifically by distinct writer/reader-process recall; memory-only state cannot manufacture persistence |
| Python/JSON compatibility checks | All 16 tracked Python files parse with Python 3.10 grammar; all 4 tracked JSON files parse; execution was on 3.13.5 only |
| Original adapter/contract/project evidence | Exact byte comparison against the supplied base passed |
| Whitespace | `git diff --check` passed |

Failing-first sequence was exercised, not inferred: the new identifier-domain
test failed against the old repaired control (unknown scopes and colons were
accepted), then passed after rejection was added. The process-local-only
regression first failed because the old gate had no fresh-process failure; it
passed only after distinct writer and reader subprocesses were added. Actual
partial-save and replace-failure tests failed against the old control's retained
temporary output, then passed with cleanup. The raw baseline additionally failed
on corrupted committed bytes during partial direct write, and on absence of the
replace boundary. The independent-instance stale-write test failed with
`RevisionConflict not raised`, then passed after disk refresh before the revision
check. The internal Engram brief-mapping regression failed on `brief(project=...)`,
then passed with wording matching the existing empty-argument, DB-pinned preview.

The five added trusted tests cover identifier domain, distinct processes,
partial save, failed replace and sequential stale instances. All original twelve
checks remain; the legacy orphan-temp test is explicitly identified as a narrower
load check. Baseline failures grew from ten to fourteen based on real execution;
the baseline already passed distinct-process recall and still passes both old
fresh-object and orphan-temp checks. Full exact failure IDs are enforced in
`scripts/evaluate.py`.

Execution used only `PATH=/usr/bin:/bin`, a scratch-only `HOME`, the existing
profile scratch `TMPDIR`, `LANG=C.UTF-8`, `PYTHONDONTWRITEBYTECODE=1`, and
`PYTHONNOUSERSITE=1`. Fresh-process children use the same nonsecret allowlist with
their disposable state root as HOME. No installed providers or credentials were
inherited. Prowl discovery was attempted but unavailable (exit 127); bounded
source inspection and local Git objects were used instead. No network isolation
claim is made: inspected stdlib-only tests, not an OS sandbox, establish the
bounded execution path. Logs and direct-control JSON are retained outside this
worktree in the local consolidation evidence directory.

See `tasks/bob-project-memory/ACCEPTANCE.md` for the exact boundary: local
Path-based injected failures are not power-loss durability; sequential refresh is
not atomic multiprocess CAS; source tokens are not verified evidence hashes;
promotion provenance and whole-surface outage semantics remain manual. Fixture
green is **not live backend qualification**. Engram remains optional inert
research plus a disabled preview. External source/asset verification is **NOT RUN**;
actual upstream API compatibility, Engram/MCP/Bob execution, model behavior,
concurrency, backup erasure and production readiness are **NOT RUN / NOT QUALIFIED**.
No downloads, installs, services, model/provider calls, private memory, publication
or main/integration merge occurred. Native Python 3.10 and hosted matrix execution
were not performed; the grammar check does not substitute for them.
