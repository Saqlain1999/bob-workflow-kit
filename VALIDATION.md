# Validation record

Current package: **0.1.0-alpha.4**. Historical alpha.1 local preparation was recorded **9 October 2026 (UTC)**; hosted CI was added **10 October 2026 (UTC)**.

This record distinguishes the implemented package, local software tests, an independent written-skill trial, and work that has not been executed. Nothing in this record establishes that the kit has been loaded by a live IBM Bob client.

## Alpha.3 candidate validation

Alpha.4 adds `plan-project-change`, an on-demand evidence/decision reference, a delivery-plan template, and fixed-scope installer support for three packaged skills. The skill requires repository evidence, acceptance traceability, an architecture decision, and recovery state before implementation. Static validation does not prove plan quality, future implementation, or live Bob activation.

Local checks executed on **18 October 2026 (UTC), Linux, Python 3.12.14**:

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` from kit root | **26 tests passed**, exit 0, including missing/unlisted skill rejection, directory-name validation, and the existing lifecycle/recovery suite |
| `python3 -B -m unittest discover -s tests -v` from `examples/tiny-ledger` | **9 tests, 8 passes, 1 deliberate failure**, exit 1; original regression preserved |
| Python files parsed with Python 3.10 grammar; JSON parsed; relative Markdown targets checked | **5 Python files**, **2 JSON files**, and **60 local Markdown links** checked; no syntax/JSON errors or missing local targets |
| Packaged-payload preview against an explicit temporary Bob home | **10 managed text files** accepted; target reported `ready`; no live Bob configuration used |

The hosted matrix for the final candidate commit must pass before release. The local checks establish installer behavior and static content properties only. No live Bob client loaded or activated the new skill, and no model trial established that the instructions preserve meaning in practice.

## Alpha.2 validation

This update adds first-use, comparison, reporting and release materials. The seven installed payload files and installer ownership behavior are unchanged from alpha.1. The installer reports the new package version, with a consistency check against `VERSION` in the existing suite. The version change still requires the supported uninstall-then-install update path.

Local checks executed on **10 October 2026 (UTC), Linux, Python 3.12.14**:

| Check | Observed result |
| --- | --- |
| `python3 -B -m unittest discover -s tests -v` from kit root | **24 tests passed**, exit 0, including package-version consistency |
| Same command from `examples/tiny-ledger` | **9 tests, 8 passes, 1 deliberate failure**, exit 1; original regression preserved |
| Python files parsed with Python 3.10 grammar; JSON parsed; relative Markdown targets checked | No syntax/JSON errors or missing local file targets |

These checks use disposable installer targets. No live Bob configuration or model was used.

The tagged release notes record the exact alpha.2 source commit and its CI results. The historical evidence below stays attributed to alpha.1; the constructed Parcel Resume exercise and its helper checks live in the companion [evaluation repository](https://github.com/Saqlain1999/bob-workflow-evals/blob/main/VALIDATION.md). Neither that offline exercise nor this documentation update is a live Bob trial.

## Historical alpha.1 executed checks

| Check | Environment and method | Observed result |
| --- | --- | --- |
| Offline installer suite | Linux; Python 3.12.14; `python3 -B -m unittest discover -s tests -v` | **24 tests passed**, exit 0 |
| Real packaged payload | Thirteen Markdown rule/skill/reference/template files; covered by suite and CLI lifecycle tests | Payload validation and installation lifecycle passed in temporary targets |
| Tiny Ledger baseline | Shipped fixture; Python standard-library unittest | **9 tests: 8 pass, 1 deliberate failure**, exit 1 |
| Written-skill trial | A separate assistant read the skill and repaired a disposable fixture copy | Only `ledger.py` changed; tests and docs preserved |
| Repaired fixture verification | Local unittest run on the trial copy | **9 tests passed**, exit 0 |
| Source syntax and documentation | Python files parsed using Python 3.10 grammar; JSON parsed; 36 local Markdown links checked | Syntax and JSON checks passed; **0 broken local links** |

The independent assistant completed a small repair directly without inventing a large plan or unnecessary checkpoint. This is useful evidence of the written skill's proportionality on one fixture. It is **not** live Bob execution, an estimate of model accuracy, or a test of interrupted large-project recovery.

Actual fixture outputs and the observed diff are in [trial-evidence.md](docs/trial-evidence.md). Machine-readable outcomes and hashes of the tested installer, test suite, and payload are in [evaluation-record.json](docs/evaluation-record.json).

## What the installer suite covers

- Read-only preview/doctor behaviour, module import, and help.
- Explicit temporary targets, preserving unrelated file contents and timestamps.
- Installation, inspection, removal, and byte-identical repeated installation.
- Unowned collisions, including same-byte collisions, and locally edited managed files.
- Changed-source/version refusal and the uninstall-then-install update policy.
- Invalid metadata, traversal, unexpected managed paths, symlinks, and simulated Windows reparse attributes.
- JSON result fields, source-payload integrity, and process exit statuses.
- Failure during installation, publication followed by an exception/interruption, and staging cleanup errors.
- Incomplete rollback with retained journal, actual hard process termination, and safe recovery/retry behaviour.
- Interrupted uninstall and preservation of shared/nonempty directories.

Tests use disposable explicit Bob roots; no live user Bob configuration, model endpoint, or credentials are needed.

## Historical alpha.1 hosted publication checks

[GitHub Actions run 38008042613](https://github.com/Saqlain1999/bob-workflow-kit/actions/runs/38008042613) completed successfully for published commit `3226221bc7b085666fd64b8f2e7dc2e1b6acb80f` on 10 October 2026 (UTC). All six installer-test jobs passed: `ubuntu-latest`, `windows-latest`, and `macos-latest`, each with Python 3.10 and 3.12. The recorded test step was **Run installer tests in disposable targets**.

This establishes execution of the offline installer suite on those hosted runners. It does not establish Bob client loading, behavior on a particular work laptop, or large-codebase effectiveness. The local preparation evidence above remains separate from this hosted run.

## Not executed or not established

| Area | Status |
| --- | --- |
| IBM Bob IDE loading and behaviour | **Not tested** |
| IBM Bob Shell loading and behaviour | **Not tested** |
| Remote SSH / containers / managed laptop policies | **Not qualified** |
| Large-repository checkpoint/recovery trial | **Not run** |
| Native Bob plugin or Marketplace installation | **Not implemented or claimed** |
| External workflow controller | **Design preview; evaluate existing runtimes before implementation** |

The filesystem must support the installer's required hard links and usable file identity. The installer handles tested interruption cases on a cooperative local filesystem; it is not a security boundary against malicious concurrent mutation.

## Reproduce and extend

Run the suite from the exact source being evaluated. Keep the shipped fixture baseline intact and work in disposable copies. Record new client/OS results with the exact kit/Bob versions and observed evidence. Follow [evaluation.md](docs/evaluation.md) before making broader effectiveness claims.
