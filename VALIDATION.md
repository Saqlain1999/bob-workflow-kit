# Local software validation

## New source snapshots (PR #13/#14)

The new backend gates remain source/protocol-only. Exact incoming validation
records are preserved as raw text, with their original counts and attribution:
[PR #13 snapshot](docs/HISTORICAL-VALIDATION-pr13-6d487eb.txt).
The [accepted pre-port snapshot](docs/HISTORICAL-VALIDATION-accepted-7a432e0.txt)
is also retained byte-for-byte. Current combined checks belong in the separate
[combined-source record](docs/COMBINED-SOURCE-VALIDATION.md), not those historical tables.

## Reminder Remediated Release Handoff — 3 November 2026 (UTC)

Observed on Linux with Python 3.12.14 after deriving the release-readiness
fixture from the exact repaired state and current independent re-review. The
results below are offline software checks, not a participant result, a live Bob
observation, or release approval.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **116 helper tests passed**, exit 0; no skips or resource warnings |
| Prepared release-readiness baseline | Twelve trusted checks; both repaired behavior boundaries passed and exactly ten named documentation/release-record failures reproduced; helper status `expected_baseline_failure` |
| Known-good release-readiness control | Twelve checks passed; exact source, tests, current re-review, and historical gate records unchanged; only `USER_GUIDE.md` and `RELEASE_READINESS_HANDOFF.md` changed; helper status `public_tests_passed` |
| Release-readiness negative controls | Release approval, missing current review, false 11/12 evidence, source edit, current-review edit, historical release edit, candidate-test edit, unrelated file, and result output inside the workspace were rejected |
| Static checks | **48 Python files** parsed with Python 3.10 grammar; **3 JSON files** parsed; **48 local Markdown links** checked across **93 Markdown files**; complete 24-file diff and `git diff --check` passed |

The known-good control uses the exact decision `ready for release review` only
after the current re-review disposes REV-001 and REV-002. That decision hands a
finite candidate to human review; it does not authorize or perform a release,
tag, artifact, deployment, publication, or announcement. These checks establish
no general release judgment, production readiness, security proof,
process-safe concurrency, broad compatibility, performance, or live Bob
behavior. No model, Bob client, credential, network service, upstream content,
release artifact, tag, deployment, publication, or paid API was used.

## Reminder Remediated Re-review — 2 November 2026 (UTC)

Observed after reconciling the re-review branch with the current remediation
head on Linux with Python 3.12.14. The results below are offline software
checks, not a participant result or evidence that Bob discovered or followed
an independent-review skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **104 helper tests passed**, exit 0; no skips or resource warnings |
| Prepared re-review baseline | Twelve trusted checks; both repaired behaviors passed and exactly six named review-record failures reproduced; helper status `expected_baseline_failure` |
| Known-good re-review control | Twelve checks passed; protected exact candidate and historical records unchanged; only `REMEDIATION_REVIEW.md` changed; helper status `public_tests_passed` |
| Re-review negative controls | Superficial approval, missing REV-002 disposition, false 11/12 evidence, source edit, historical review/release edits, candidate-test edit, unrelated file, and result output inside the workspace were rejected |
| Static checks | **43 Python files** parsed with Python 3.10 grammar; **3 JSON files** parsed; **46 local Markdown links** checked across **80 Markdown files**; complete 23-file diff and `git diff --check` passed |

The control records both historical findings as resolved with current source and
behavior evidence, keeps process-safe concurrency unknown, and hands the exact
candidate to a separate release-preparation stage. `ready for release
preparation` is not release approval and establishes no production readiness,
general security proof, compatibility, performance, deployment, or live Bob
behavior. No model, Bob client, credential, network service, upstream content,
release artifact, tag, deployment, publication, or paid API was used.

## Reminder Review Remediation — 2 November 2026 (UTC)

Observed after reconciling the remediation branch with the current blocked
release-handoff head on Linux 6.18.55 x86_64 with Python 3.12.14. The results
below are offline software checks, not a participant result or evidence that
Bob discovered or followed an implementation skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **92 helper tests passed**, exit 0; no skips or resource warnings |
| Prepared remediation baseline | Twelve trusted checks; both seeded defects reproduced and exactly nine named behavior/handoff failures; helper status `expected_baseline_failure` |
| Known-good remediation control | Twelve checks passed; protected request/plan/review/release/documentation/team/store inputs unchanged; only `notifier/service.py` and `IMPLEMENTATION_HANDOFF.md` changed; helper status `public_tests_passed` |
| Remediation negative controls | Owner-only fix, conflict-only fix, missing fresh-review gate, review/release record edits, candidate-test edit, unrelated file, and result output inside the workspace were rejected |
| Static checks | **38 Python files** parsed with Python 3.10 grammar; **3 JSON files** parsed; **44 local Markdown links** checked across **68 Markdown files**; `git diff --check` passed |

The control corrects the two public fixture defects and hands the exact state to
a fresh independent review. It deliberately preserves the prior `changes
required` review and `release blocked` record as historical evidence; a helper
pass does not clear those gates or establish general implementation quality,
security, process-safe concurrency, compatibility, production readiness,
release approval, or live Bob activation. No model, Bob client, credential,
network service, upstream content, release artifact, tag, deployment,
publication, or paid API was used.

## Reminder Documentation and Release Handoff — 1 November 2026 (UTC)

Observed after reconciling the release-handoff branch with the current
independent-review head on Linux 6.18.55 / Python 3.12.14. The results below are
offline software checks, not a participant result or evidence that Bob
discovered or followed the release-handoff skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **81 helper tests passed**, exit 0; no skips or resource warnings |
| Prepared release baseline | Twelve trusted checks; both seeded defects reproduced and exactly ten named documentation/release-contract failures; helper status `expected_baseline_failure` |
| Known-good blocked control | Twelve checks passed; all request/plan/implementation/review/team/source inputs unchanged; only `RELEASE_HANDOFF.md` and `USER_GUIDE.md` changed; helper status `public_tests_passed` |
| Release negative controls | False ready decision, missing High finding, helper-as-correctness claim, source edit, candidate-test edit, unrelated file, and result output inside the workspace were rejected |
| Static checks | **33 Python files** parsed with Python 3.10 grammar; **3 JSON files** parsed; **40 local Markdown links** checked across **57 Markdown files**; `git diff --check` passed |

The fixture preserves two unresolved review findings, so a correct known-good output remains `release blocked`; passing the helper cannot establish corrected behavior, release readiness, deployment approval, compatibility, performance, or live Bob activation. No model, Bob client, credential, network service, upstream content, release artifact, tag, deployment, publication, or paid API was used.

## Reminder Independent Review and Security — 23 October 2026 (UTC)

Observed on Linux, Python 3.12.14. This branch is stacked on the bounded
diagnostics, technical-writing, planning, and implementation branches. The
results below are offline software checks, not a participant result or evidence
that Bob discovered or followed the independent-review skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | **70 helper tests passed**, exit 0; no skips or resource warnings |
| Prepared review baseline | Ten trusted checks; the two seeded defects reproduced and exactly eight named report-contract failures; helper status `expected_baseline_failure` |
| Independent known-good review control | Ten checks passed; all request/plan/handoff/team/source inputs unchanged; only `REVIEW_HANDOFF.md` changed; helper status `public_tests_passed` |
| Review negative controls | Superficial approval, missing second finding, false current-pass evidence, source edit, candidate-test edit, unrelated file, and result output inside the workspace were rejected |
| Static checks | **28 Python files** parsed with Python 3.10 grammar; **3 JSON files** parsed; **36 local Markdown links** checked across **46 Markdown files**; `git diff --check` passed |

The fixture checks two public, deliberately seeded issues: an inverted owner
filter that returns another owner's reminder, and conflict text that exposes
stored record content. It checks a precise review/remediation artifact without
allowing product edits. Manual review still owns reasoning quality, severity
judgment, scope proportionality, and whether a real participant independently
found the issues. Passing does not prove general defect discovery, security,
compliance, production readiness, release approval, large-project behavior, or
live Bob activation. No model, Bob client, credential, network service, scanner,
upstream content, or paid API was used.

## Reminder Implementation and Debugging — 22 October 2026 (UTC)

Observed on Linux (`Linux-6.18.55-x86_64-with-glibc2.39`), Python 3.12.14.
This branch is stacked on the bounded-diagnostics, technical-writing, and
project-planning branches. The results below are offline software checks, not a
Bob participant result or evidence that Bob discovered or followed the
implementation/debugging skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | 60 helper tests passed; exit 0; no skips or resource warnings |
| Prepared interrupted baseline | Ten trusted checks; exactly four named retry/conflict/handoff failures; helper status `expected_baseline_failure` |
| Independent known-good control | Ten checks passed; protected request/plan/checkpoint/team note unchanged; only `notifier/service.py` and `IMPLEMENTATION_HANDOFF.md` changed; helper status `public_tests_passed` |
| Implementation negative controls | Missing handoff, weakened conflict behavior, protected plan edit, candidate-test edit, and unrelated file were rejected |
| Static checks | Edited Python files compiled; 3 repository JSON files parsed; 32 local Markdown links across 37 Markdown files and `git diff --check` passed |

The fixture covers selected behavior, compatibility, preservation, bounded
scope, and recovery-evidence properties for one small append-only reminder
project. Manual review still owns diagnosis quality, minimality, evidence
truthfulness, and whether the handoff supports safe independent review and
resumption. Passing does not prove process-safe concurrency, security,
performance, deployment, production readiness, large-project behavior, or live
Bob activation. The checkpoint is a constructed fixture artifact, not an
observed agent interruption. No model, Bob client, credential, network service,
or paid API was used.

## Project Planning Handoff — 21 October 2026 (UTC)

Observed on Linux (`Linux-6.18.55-x86_64-with-glibc2.39`), Python 3.12.14.
This branch is stacked on the bounded-diagnostics and technical-writing branches.
The results below are offline software checks, not a Bob participant result or
evidence that Bob discovered or followed the planning skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | 52 helper tests passed; exit 0; no skips or resource warnings |
| Planning prepared baseline | Ten trusted checks; exactly seven named evidence/acceptance/decision/traceability/risk/recovery failures; helper status `expected_baseline_failure` |
| Independent known-good plan control | Ten checks passed; protected request/source unchanged; only `DELIVERY_PLAN.md` changed; helper status `public_tests_passed` |
| Planning negative controls | Missing acceptance trace, missing stale-evidence guidance, protected source edit, and unrelated added file were rejected |
| Static checks | Edited Python files compiled; repository JSON parsed; local Markdown links and `git diff --check` passed |

The fixture covers selected properties of one small append-only reminder
project. Manual review still owns evidence quality, design proportionality,
completeness, and whether the handoff could guide safe implementation. Passing
does not prove architecture quality, future implementation, security,
scalability, large-project behavior, or live Bob activation. No model, Bob
client, credential, network service, or paid API was used.

## Technical Writing Fidelity — 20 October 2026 (UTC)

Observed on Linux (`Linux-6.18.55-x86_64-with-glibc2.39`), Python 3.12.14.
This feature branch is intentionally stacked on the bounded-diagnostics branch,
so the counts below cover both changes. They are offline software checks, not a
Bob participant result or evidence that Bob discovered or followed a skill.

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` | 45 helper tests passed; exit 0; no skips or resource warnings |
| Technical-writing prepared baseline | Eight trusted checks; exactly the two named structure failures; helper status `expected_baseline_failure` |
| Independent known-good rewrite control | Eight checks passed; protected contract unchanged; only `RUNBOOK.md` changed; helper status `public_tests_passed` |
| Fidelity negative controls | Weakened retry permission/condition, removed negation, reordered commands, changed contract, and unrelated added file were all rejected |
| Python/JSON/static checks | Five edited Python files compiled; every repository JSON file parsed; `git diff --check` passed |
| Local Markdown links | 24 relative links checked; no missing target |

The fixture's deterministic contract covers selected exact tokens, commands,
modal keywords, negation, retry conditions, execution order, protected input,
and candidate file scope. The manual checklist still owns scanability,
contradictions and unsupported additions. Passing the helper does not prove
general semantic equivalence, technical correctness, ASD-STE100 compliance, or
the quality or cause of a live participant's behavior. No model, Bob client,
credential, network service, or paid API was used.

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

## Historical observations and local integration

The exact pre-refresh validation body is retained in
[HISTORICAL-VALIDATION-pre-refresh.md](docs/HISTORICAL-VALIDATION-pre-refresh.md).
The corrected memory source validation body is retained in
[HISTORICAL-VALIDATION-memory-source.md](docs/HISTORICAL-VALIDATION-memory-source.md).
Their historical counts are observations at their own source heads, not this
combined tree. The exact separately attributed monorepo-fork body is retained in
[HISTORICAL-VALIDATION-pre-refresh-fork.md](docs/HISTORICAL-VALIDATION-pre-refresh-fork.md).
New combined-tree execution is recorded separately in
[COMBINED-SOURCE-VALIDATION.md](docs/COMBINED-SOURCE-VALIDATION.md).
