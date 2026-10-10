# Validation record

Package: **0.1.0-alpha.1**. Local preparation recorded **9 October 2026 (UTC)**; hosted CI added **10 October 2026 (UTC)**.

This record distinguishes the implemented package, local software tests, an independent written-skill trial, and work that has not been executed. Nothing in this record establishes that the kit has been loaded by a live IBM Bob client.

## Executed checks

| Check | Environment and method | Observed result |
| --- | --- | --- |
| Offline installer suite | Linux; Python 3.12.14; `python3 -B -m unittest discover -s tests -v` | **24 tests passed**, exit 0 |
| Real packaged payload | Seven Markdown rule/skill/reference/template files; covered by suite and CLI lifecycle tests | Payload validation and installation lifecycle passed in temporary targets |
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

## Hosted publication checks

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
| External workflow controller | **Planned only** |

The filesystem must support the installer's required hard links and usable file identity. The installer handles tested interruption cases on a cooperative local filesystem; it is not a security boundary against malicious concurrent mutation.

## Reproduce and extend

Run the suite from the exact source being evaluated. Keep the shipped fixture baseline intact and work in disposable copies. Record new client/OS results with the exact kit/Bob versions and observed evidence. Follow [evaluation.md](docs/evaluation.md) before making broader effectiveness claims.
