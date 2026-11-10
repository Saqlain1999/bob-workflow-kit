# Validation record

Current package: **0.1.0-alpha.7**. Historical alpha.1 local preparation was recorded **9 October 2026 (UTC)**; hosted CI was added **10 October 2026 (UTC)**.

This record distinguishes the implemented package, local software tests, an independent written-skill trial, and work that has not been executed. Nothing in this record establishes that the kit has been loaded by a live IBM Bob client.

## Fail-closed live-trial evidence — 10 November 2026 (UTC)

Review found that the shipped live-trial template could describe a result as a
manual Bob trial without binding it to a run, host, exact kit commit, Bob
version/mode, explicit workspace-trust decision or affirmative live-client
observation. That made blocked or completed reports ambiguous and could let
non-interactive `bob run` evidence cross an interactive manual-approval
boundary.

The template is now schema 2 and a read-only validator requires bounded claim
levels. Executed results must identify the run and host, use an interactive IDE
or Shell client, record the exact kit and Bob revisions, record explicit trust
and native-loading evidence, and affirm that Bob was actually observed. A
completed result must additionally carry healthy installation evidence, both
rule and skill loading, exact task evidence, manual acceptance and preservation
observations. Blocked and incomplete records remain valid evidence, but cannot
claim a completed task. The validator checks record shape and consistency; it
does not attest that the recorded observations are true.

Fresh local checks on Linux 6.18.57 x86_64 with Python 3.12.14:

- Focused fail-closed live-trial suite: **7/7 passed**, including template
  preservation, non-interactive rejection, identity/trust/live-observation
  controls, overclaim rejection, bounded blocked results and CLI read-only
  behavior.
- `python3 -B -W error::ResourceWarning tools/check_all.py --require-history`:
  **73/73 root tests** and **157/157 evaluator tests** passed with zero
  failures, errors or skips; catalogue, provenance and local links passed.
- Exact-content archive with no `.git` and a `PATH` containing Python but no
  Git: all content/offline checks passed; root discovered and ran **73** cases
  with **24 explicit Git-only skips**, and all **157** evaluator tests ran.
  This archive result does not establish independent history proof.
- Complete current diff and `git diff --check` passed.

No live IBM Bob client, model, credential, private repository, hook, MCP server,
paid service or unreviewed third-party content was used. These results establish
offline validation and honest reporting controls only—not Bob discovery,
activation, workflow-following, compatibility, task quality or release
readiness.

## Consolidation refresh — 9 November 2026 (UTC)

Review found that the consolidation branch still embedded evaluator PR #14's
schema-v1 head `12cec9029682e14b57f9ace38605951fb091b605` after the source PR
had advanced to reviewed final head
`083ed29533ca292fefa4784efac644f57de9735a`. The stale port omitted required
run/host/client identity, complete evidence for blocked or incomplete live-Bob
observations, and the source-backed rejection of non-interactive `bob run`.

The final source revision remains pinned, its five active protocol/code/test
files retain the exact source Git blob identities under `evals/`, and combined
contributor/validation records retain their separate attribution. The
reviewed-fork manifest binds the complete 181-file evaluator tree to reviewed
port `e6c39afdc03d4a044788952eaa6b009eadbba393`. A root regression binds the PR
map to final head `083ed295...`, requires protocol schema 2, verifies the five
source blob identities, and checks the fourteen native source heads plus the
reviewed port as ancestors in a full checkout.

Fresh local checks on Linux 6.18.57 x86_64 with Python 3.12.14:

- `python3 -B -W error::ResourceWarning tools/check_all.py --require-history`:
  **66/66 root tests** and **157/157 evaluator tests** passed with zero
  failures, errors or skips; catalogue, provenance and local links passed.
- Focused runtime-protocol suite: **13/13 passed**.
- Exact-commit archive with no `.git` and a `PATH` containing Python but no
  Git: all content/offline checks passed; root discovered **66** cases, executed
  **42** bodies and reported **24 explicit Git-only skips**; all **157**
  evaluator tests executed. This archive check does not establish independent
  history proof.
- Complete current diff and `git diff --check` passed.

No Engram or Basic Memory artifact, Bob client, MCP server, model, credential,
private project, hook, or paid service was downloaded or executed. These are
offline source, provenance and regression results—not live Bob loading,
workflow-following, backend qualification, licence/privacy approval, production
readiness, release approval or repository-transition approval.

## Local one-product kit-port validation

Reviewed kit candidates #5, #6 and #7 were merged locally in dependency order without squashing. The sections below headed Alpha.5, Alpha.6 and Alpha.7 retain their original candidate-specific evidence; their dates, environments and counts do not describe this consolidated checkout. Historical alpha.4 and earlier evidence remains unchanged, including the seven-file alpha.1 payload.

Fresh local checks on the kit-port payload based on merge `100c4f3` (Linux, Python 3.13.5):

- ResourceWarning-fatal root suite: **57 tests passed**; installer-only suite: **26 tests passed**.
- `python3 tools/check_all.py --require-history`: root **57 tests**, included evaluator **37 tests**, catalogue, provenance and local Markdown links all passed.
- Actual packaged preview/install/doctor/uninstall: **22 managed files**, **six skills**, explicit disposable Bob home; doctor healthy, all managed files removed, unrelated sentinel preserved.
- Tiny Ledger: **9 tests, 8 passes, 1 intentional failure**, exit 1; shipped fixture unchanged.

These results are offline only. Logs and exact final-head metadata are in the separate local `kit-port-result.json` handoff and `kit-port-evidence/` directory, not a hosted CI or live Bob result. No active Bob configuration, model, credentials or network was used. Combined-tree independent review, other feature ports, hosted CI, client loading and explicit publication/merge/release approval remain separate gates.

## Alpha.7 candidate validation

Alpha.7 adds `document-and-prepare-release`, an on-demand release-evidence reference, a release-handoff template, and fixed-scope installer support for six packaged skills. The skill reconciles exact-state implementation and independent-review evidence, updates only agreed documentation, and requires `release blocked` while a confirmed blocking finding or essential evidence gap remains. It cannot tag, publish, deploy, approve a release, prove production readiness, or turn offline packaging checks into live Bob or product-behavior evidence.

Local checks executed on **24 October 2026 (UTC), Linux, Python 3.12.14**:

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` from kit root | **26 tests passed**, exit 0, including six-skill fixed-pack validation and the existing lifecycle/recovery suite |
| `python3 -B -m unittest discover -s tests -v` from `examples/tiny-ledger` | **9 tests, 8 passes, 1 deliberate failure**, exit 1; original regression preserved |
| Python files parsed with Python 3.10 grammar; JSON parsed; relative Markdown targets checked | **5 Python files**, **2 JSON files**, and **60 local Markdown links** checked across **45 Markdown files** with no syntax/JSON errors or missing local targets |
| Preview/install/doctor/uninstall against an explicit temporary Bob home | **22 managed text files** accepted; install reported `installed`, doctor reported `healthy`, and uninstall removed the manifest and managed files; no live Bob configuration used |

The hosted matrix for the final candidate commit must pass before the pull request is ready. The paired reminder release-handoff evaluation lives in the companion evaluation repository and remains separate evidence. No live Bob client loaded or activated this skill, and no model participant established that its release decisions are generally reliable.

## Alpha.6 candidate validation

Alpha.6 adds `review-and-secure-change`, an on-demand findings/severity reference, a review-handoff template, and fixed-scope installer support for five packaged skills. The skill requires current-state reconciliation, a read-only first pass, independently reproduced evidence, applicable trust-boundary review, precise findings, and a bounded next-gate decision. Static and installer validation do not prove review quality, security, absence of defects, compliance, production readiness, reviewer independence, or live Bob activation.

Local checks executed on **23 October 2026 (UTC), Linux, Python 3.12.14**:

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` from kit root | **26 tests passed**, exit 0, including fixed-pack validation and the existing lifecycle/recovery suite |
| `python3 -B -m unittest discover -s tests -v` from `examples/tiny-ledger` | **9 tests, 8 passes, 1 deliberate failure**, exit 1; original regression preserved |
| Python files parsed with Python 3.10 grammar; JSON parsed; relative Markdown targets checked | **5 Python files**, **2 JSON files**, and **60 local Markdown links** checked across **42 Markdown files** with no syntax/JSON errors or missing local targets |
| Preview/install/doctor/uninstall against an explicit temporary Bob home | **19 managed text files** accepted; install reported `installed`, doctor reported `healthy`, and uninstall removed all managed files; no live Bob configuration used |

The hosted matrix for the final candidate commit must pass before release. The paired reminder review/security evaluation lives in the companion evaluation repository and remains separate evidence. No live Bob client loaded or activated the skill, and no model participant established that these instructions find defects reliably.

## Alpha.5 candidate validation

Alpha.5 adds `implement-and-debug-change`, an on-demand debugging-evidence reference, an implementation-handoff template, and fixed-scope installer support for four packaged skills. The skill requires a current input contract, a reproducible baseline, a criterion-linked minimal change, current-state checks, preservation evidence, and a resumable handoff. Static and installer validation do not prove implementation quality, independent review, production readiness, or live Bob activation.

Local checks executed on **22 October 2026 (UTC), Linux, Python 3.12.14**:

| Check | Observed result |
| --- | --- |
| `python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` from kit root | **26 tests passed**, exit 0, including missing/unlisted skill rejection, directory-name validation, and the existing lifecycle/recovery suite |
| `python3 -B -m unittest discover -s tests -v` from `examples/tiny-ledger` | **9 tests, 8 passes, 1 deliberate failure**, exit 1; original regression preserved |
| Python files parsed with Python 3.10 grammar; JSON parsed; relative Markdown targets checked | **5 Python files**, **2 JSON files**, and **60 local Markdown links** checked across 39 Markdown files; no syntax/JSON errors or missing local targets |
| Preview/install/doctor/uninstall against an explicit temporary Bob home | **16 managed text files** accepted; install reported `installed`, doctor reported `healthy`, and uninstall removed all managed files; no live Bob configuration used |

The hosted matrix for the final candidate commit must pass before release. The local checks establish installer behavior and static content properties only. No live Bob client loaded or activated the new skill, and no model trial established that the instructions produce correct implementations in practice.

## Alpha.4 integration validation — 26 October 2026 (UTC)

Alpha.4 adds `plan-project-change`, its evidence/decision reference and delivery-plan template, and fixed-scope support for three packaged skills. During review, the historical alpha.1 payload count and alpha.3 candidate attribution were restored rather than relabelled as evidence for this new payload.

Fresh validation on the current edited integration candidate (based on `2f9eed20d023374eca146f394b01d17472adff2f`, reconciled with main after PR #2), Linux/Python 3.13.5: the ResourceWarning-fatal installer suite passed 26/26 and the actual packaged preview/install/doctor/uninstall lifecycle accepted thirteen managed files in an explicit disposable Bob home. These are new offline results, not a historical Python 3.12.14 run or live Bob qualification. Hosted checks must pass on the resulting exact head before merge.

## Alpha.3 candidate validation

Alpha.3 adds the `write-clear-technical-content` skill, two on-demand references, and fixed-scope installer support for both packaged skills. The skill protects exact technical tokens, conditions, ordering, negation, uncertainty, and requirement strength during rewriting. It explicitly does not claim ASD-STE100 compliance or semantic-equivalence proof.

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
