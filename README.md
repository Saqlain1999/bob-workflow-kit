# Bob Workflow Evals

A small, reproducible evaluation starter for IBM Bob project workflows.

Eleven tasks offer first trials: repair a deliberately faulty Python ledger,
resume a parcel-pricing change from a constructed checkpoint, or restructure a
dense migration runbook while preserving a bounded technical contract, or turn
a reminder-service request and current source into a traceable, resumable delivery plan,
or resume and complete that reminder change from an interrupted implementation,
or independently review that implementation for seeded correctness/security defects,
or prepare truthful documentation and a blocked release handoff for those unresolved findings,
or return those findings to implementation for bounded remediation, or
independently re-review the exact repaired state before release preparation, or
prepare that remediated candidate for a bounded human release review, or
complete a conditional backend-neutral project-memory contract. Each has
a fixture, public tests, a participant prompt, a manual acceptance checklist,
and an offline helper that runs trusted tests against a disposable workspace.

**Status: evaluation starter. No live Bob evaluation, third-party memory-backend qualification, or large-repository
benchmark has been performed for this repository.** These are small correctness
and recovery exercises. Passing them does not establish reliable performance on
large projects, prove that a workflow caused an improvement, or guarantee future
results. This is an independent community project, not an IBM product.

## What is here

| Path | Purpose |
| --- | --- |
| `fixtures/tiny-ledger/` | Deliberately faulty original and its nine public tests |
| `tasks/tiny-ledger-atomicity/` | Task definition, agent prompt, and acceptance checklist |
| `fixtures/parcel-resume/` | Multi-file pricing fixture and ten public tests |
| `tasks/parcel-resume/` | Constructed interruption, current-state and preservation exercise |
| `fixtures/technical-writing-fidelity/` | Dense runbook, protected contract, and eight public checks |
| `tasks/technical-writing-fidelity/` | Fidelity-preserving rewrite prompt and manual review boundary |
| `fixtures/project-planning-handoff/` | Small existing reminder project and intentionally incomplete delivery plan |
| `tasks/project-planning-handoff/` | Evidence-backed requirements/architecture prompt and manual review boundary |
| `fixtures/reminder-implementation-debugging/` | Interrupted reminder implementation, protected handoffs, and ten trusted checks |
| `tasks/reminder-implementation-debugging/` | Bounded implementation/debugging prompt and manual recovery review |
| `fixtures/reminder-independent-review/` | Implemented reminder change with two deliberate review defects and ten trusted checks |
| `tasks/reminder-independent-review/` | Read-only independent review/security prompt and manual findings review |
| `fixtures/reminder-release-handoff/` | Reviewed reminder candidate with unresolved blockers, unsafe initial docs, and twelve trusted checks |
| `tasks/reminder-release-handoff/` | Documentation/release prompt and manual blocked-decision review |
| `fixtures/reminder-review-remediation/` | Blocked reminder candidate, preserved gate records, and twelve remediation checks |
| `tasks/reminder-review-remediation/` | Two-finding remediation prompt and manual evidence-chain review |
| `fixtures/reminder-remediated-review/` | Repaired reminder candidate, historical blocked records, and twelve re-review checks |
| `tasks/reminder-remediated-review/` | Read-only remediation re-review prompt and manual disposition review |
| `fixtures/reminder-remediated-release-handoff/` | Repaired and re-reviewed reminder candidate, preserved gate history, and twelve release-readiness checks |
| `tasks/reminder-remediated-release-handoff/` | Current documentation/release prompt and manual ready-for-review boundary |

| `fixtures/bob-project-memory/` | Two-project memory contract with seventeen trusted checks |
| `tasks/bob-project-memory/` | Isolation, freshness, conflict, deletion, outage, and handoff exercise |
| `qualifications/` | Pinned backend-specific evidence gates; no installation or runtime claim |
| `scripts/evaluate.py` | Prepare a fresh workspace and collect local test evidence |
| `tests/` | Checks for the evaluation helper itself, separate from fixture tests |
| `docs/protocol.md` | How to run and report a manual evaluation |
| `results/result-template.json` | Structured record for an actual participant run |

The financial fixtures use integer cents; every executable check uses Python's standard library.
No packages, services, API keys, or network access are needed.
The helper makes no model calls. Running Bob is a separate, manual step using
the installation and account you already have.

## Quick start

Use Python 3.10 or later. The examples use `python`; use `python3` if that is the
executable name on your system. Run these commands from the repository root.
Tiny Ledger remains the default task, so its existing commands are unchanged.

### 1. Check the helper

```sh
python -m unittest discover -s tests -v
```

This suite should pass. It is separate from the fixture's deliberately failing
test suite.

### 2. Prepare a disposable workspace

```sh
python scripts/evaluate.py prepare --output runs/ledger-001
```

The output directory must not already exist. Keep the original under
`fixtures/` unchanged, and use a new run directory for each independent attempt.

### 3. Verify the expected baseline

```sh
python scripts/evaluate.py baseline --workspace runs/ledger-001 --result runs/ledger-001-baseline.json
```

Expected helper status: `expected_baseline_failure`, exit code `0`.

The **underlying fixture suite** should run nine tests with eight passes and
one failure. The helper succeeds because it verified that specific faulty
baseline. This is not a claim that the application is correct.

To inspect the ordinary failing test output directly, change into the prepared
workspace and run:

```sh
python -m unittest discover -s tests -v
```

That direct command should exit with code `1` before the repair.

### 4. Run the task with Bob

Open `runs/ledger-001` as the workspace. Start a fresh Agent conversation and
paste [the task prompt](tasks/tiny-ledger-atomicity/AGENT_PROMPT.md). Record the
client version, active mode, relevant configuration, and whether the Workflow
Kit is installed. Do not assume those settings are identical across runs.

Let Bob investigate, modify the candidate, and report its verification evidence.
Use the existing public tests and documented behaviour. No large framework,
package installation, deployment, or external data is necessary.

### 5. Collect candidate evidence independently

Return to this repository's root and run:

```sh
python scripts/evaluate.py candidate --workspace runs/ledger-001 --result runs/ledger-001-candidate.json
```

Expected after a correct repair: `public_tests_passed`, exit code `0`.

The helper loads the public tests from this repository's original fixture and
runs them against the candidate's `ledger.py`. Editing or deleting tests inside
the candidate does not change that trusted test suite. The report includes
source and test fingerprints and flags whether the candidate's test files
differ from the original. Additional candidate tests require separate review
and execution; the helper does not silently count them as trusted checks.

**Public-test success is not final acceptance.** Complete the
[manual checklist](tasks/tiny-ledger-atomicity/ACCEPTANCE.md), inspect the diff,
and record the result using the [run template](results/result-template.json).

## Try the checkpoint and current-state exercise

[Parcel Resume](tasks/parcel-resume/README.md) adds a small multi-file recovery
trial. Preparation really executes a historical ten-test passing check, writes
an explicitly constructed checkpoint, then changes the policy and appends an
unrelated teammate note. The prepared state has two expected failures. The
participant must inspect current files, finish both entry points, and preserve
the two teammate-owned files byte for byte.

```sh
python3 scripts/evaluate.py prepare --task parcel-resume --output runs/parcel-001
python3 scripts/evaluate.py baseline --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-baseline.json
```

Open that workspace in a fresh Bob conversation and use the
[Parcel prompt](tasks/parcel-resume/AGENT_PROMPT.md). Afterwards:

```sh
python3 scripts/evaluate.py candidate --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-candidate.json
```

Keep Parcel reports beside the workspace, as shown. Its helper success requires
ten passing public tests, unchanged protected inputs, and stable recorded file
state during verification. New runtime files enter the state fingerprints.
[Human review](tasks/parcel-resume/ACCEPTANCE.md) still decides whether the
participant used the checkpoint well or actually noticed stale evidence. No
live Bob observation is inferred from a software test or a passing candidate.

## Try the technical-writing fidelity exercise

[Technical Writing Fidelity](tasks/technical-writing-fidelity/README.md) pairs
with the Workflow Kit's optional technical-communication skill without
depending on that skill or its PR. The task asks a participant to restructure a
dense migration note while preserving exact commands, values, modal strength,
negation, conditions, and order.

```sh
python3 scripts/evaluate.py prepare --task technical-writing-fidelity --output runs/writing-001
python3 scripts/evaluate.py baseline --task technical-writing-fidelity --workspace runs/writing-001 --result runs/writing-001-baseline.json
```

Use the [writing prompt](tasks/technical-writing-fidelity/AGENT_PROMPT.md), then
collect candidate evidence with:

```sh
python3 scripts/evaluate.py candidate --task technical-writing-fidelity --workspace runs/writing-001 --result runs/writing-001-candidate.json
```

The helper requires eight passing public checks and an unchanged protected
contract. The [manual checklist](tasks/technical-writing-fidelity/ACCEPTANCE.md)
still decides scanability and unsupported additions. A pass does not establish
general semantic equivalence, ASD-STE100 compliance, or live Bob activation.

## Try the project-planning handoff exercise

[Project Planning Handoff](tasks/project-planning-handoff/README.md) asks a
participant to inspect a small reminder service and replace only an incomplete
`DELIVERY_PLAN.md`. The public checks cover selected evidence, acceptance,
architecture-choice, traceability, risk, and recovery properties.

```sh
python3 scripts/evaluate.py prepare --task project-planning-handoff --output runs/planning-001
python3 scripts/evaluate.py baseline --task project-planning-handoff --workspace runs/planning-001 --result runs/planning-001-baseline.json
python3 scripts/evaluate.py candidate --task project-planning-handoff --workspace runs/planning-001 --result runs/planning-001-candidate.json
```

Use the [planning prompt](tasks/project-planning-handoff/AGENT_PROMPT.md) between
the baseline and candidate commands. A pass does not establish design quality,
future implementation correctness, security, scalability, or live Bob
activation.

## Try the implementation and debugging exercise

[Reminder Implementation and Debugging](tasks/reminder-implementation-debugging/README.md)
continues the same accepted reminder journey. The prepared fixture already
accepts and stores idempotency keys but does not yet recognize retries or
conflicts. Its constructed checkpoint is explicitly not Bob output and its
historical smoke is stale.

```sh
python3 scripts/evaluate.py prepare --task reminder-implementation-debugging --output runs/implementation-001
python3 scripts/evaluate.py baseline --task reminder-implementation-debugging --workspace runs/implementation-001 --result runs/implementation-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-implementation-debugging --workspace runs/implementation-001 --result runs/implementation-001-candidate.json
```

Use the [implementation prompt](tasks/reminder-implementation-debugging/AGENT_PROMPT.md)
between the baseline and candidate commands. Candidate success requires ten
trusted checks, unchanged request/plan/checkpoint/team note, bounded file scope,
and a current `IMPLEMENTATION_HANDOFF.md`. It does not prove process-safe
concurrency, security, production readiness, independent review, or live Bob
behavior.

## Try the independent review and security exercise

[Reminder Independent Review and Security](tasks/reminder-independent-review/README.md)
continues the same journey after an author implementation handoff. Current
source deliberately returns another owner's reminder and includes stored record
content in a conflict exception. The participant changes only
`REVIEW_HANDOFF.md`; product fixes belong to the next implementation stage.

```sh
python3 scripts/evaluate.py prepare --task reminder-independent-review --output runs/review-001
python3 scripts/evaluate.py baseline --task reminder-independent-review --workspace runs/review-001 --result runs/review-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-independent-review --workspace runs/review-001 --result runs/review-001-candidate.json
```

Use the [review prompt](tasks/reminder-independent-review/AGENT_PROMPT.md)
between baseline and candidate collection. Candidate success requires ten
trusted checks, unchanged product/input files, only `REVIEW_HANDOFF.md` changed,
both findings reproduced, and a `changes required` remediation handoff. It does
not prove general review accuracy, compliance, absence of vulnerabilities,
release readiness, production security, or live Bob behavior.

## Try the documentation and release-handoff exercise

[Reminder Documentation and Release Handoff](tasks/reminder-release-handoff/README.md)
continues the same journey with REV-001 and REV-002 still unresolved. The
participant may change only `USER_GUIDE.md` and `RELEASE_HANDOFF.md`; the
correct outcome is a truthful blocked decision, not a release.

```sh
python3 scripts/evaluate.py prepare --task reminder-release-handoff --output runs/release-001
python3 scripts/evaluate.py baseline --task reminder-release-handoff --workspace runs/release-001 --result runs/release-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-release-handoff --workspace runs/release-001 --result runs/release-001-candidate.json
```

Use the [release prompt](tasks/reminder-release-handoff/AGENT_PROMPT.md) between
baseline and candidate collection. Candidate success requires twelve trusted
checks, unchanged product/input files, only the two agreed documentation files
changed, an explicit `release blocked` decision, and no false artifact, tag,
deployment, publication, production-readiness, or live-Bob claim. A helper pass
does not establish general release judgment or corrected product behavior.

## Try the review-remediation exercise

[Reminder Review Remediation](tasks/reminder-review-remediation/README.md)
returns REV-001 and REV-002 from the blocked review/release state to bounded
implementation. The participant may change only `notifier/service.py` and
`IMPLEMENTATION_HANDOFF.md`; prior review, documentation, and release records
remain protected historical evidence.

```sh
python3 scripts/evaluate.py prepare --task reminder-review-remediation --output runs/remediation-001
python3 scripts/evaluate.py baseline --task reminder-review-remediation --workspace runs/remediation-001 --result runs/remediation-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-review-remediation --workspace runs/remediation-001 --result runs/remediation-001-candidate.json
```

Use the [remediation prompt](tasks/reminder-review-remediation/AGENT_PROMPT.md)
between baseline and candidate collection. Candidate success requires both
defects to be corrected, twelve trusted checks, unchanged protected inputs,
exactly two allowed file changes, and a current handoff to fresh independent
review. It does not clear the historical review, change the blocked release
decision, or prove security, production readiness, process-safe concurrency,
general implementation quality, or live Bob behavior.

## Try the remediated re-review exercise

[Reminder Remediated Re-review](tasks/reminder-remediated-review/README.md)
starts from the exact known-good remediation control. Product source, trusted
tests, implementation evidence, and the earlier blocked review/release records
are protected; the participant may change only `REMEDIATION_REVIEW.md`.

```sh
python3 scripts/evaluate.py prepare --task reminder-remediated-review --output runs/rereview-001
python3 scripts/evaluate.py baseline --task reminder-remediated-review --workspace runs/rereview-001 --result runs/rereview-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-remediated-review --workspace runs/rereview-001 --result runs/rereview-001-candidate.json
```

Use the [re-review prompt](tasks/reminder-remediated-review/AGENT_PROMPT.md)
between baseline and candidate collection. Candidate success requires twelve
trusted checks, current evidence for both resolved findings, preservation of
the exact repaired candidate and historical records, and the bounded decision
`ready for release preparation`. It does not authorize or establish a release,
production readiness, a general security proof, process-safe concurrency, or
live Bob behavior.

## Try the remediated release-handoff exercise

[Reminder Remediated Release Handoff](tasks/reminder-remediated-release-handoff/README.md)
starts from the exact repaired candidate and its current independent re-review.
Source, trusted tests, accepted inputs, implementation evidence, current review,
and the earlier blocked records are protected; the participant may change only
`USER_GUIDE.md` and `RELEASE_READINESS_HANDOFF.md`.

```sh
python3 scripts/evaluate.py prepare --task reminder-remediated-release-handoff --output runs/release-ready-001
python3 scripts/evaluate.py baseline --task reminder-remediated-release-handoff --workspace runs/release-ready-001 --result runs/release-ready-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-remediated-release-handoff --workspace runs/release-ready-001 --result runs/release-ready-001-candidate.json
```

Use the [release-readiness prompt](tasks/reminder-remediated-release-handoff/AGENT_PROMPT.md)
between baseline and candidate collection. Candidate success requires twelve
trusted checks, current finding and acceptance disposition, truthful unreleased
documentation, preservation of current and historical evidence, and the exact
decision `ready for release review`. That is a handoff to human review, not
release approval; it authorizes no tag, artifact, deployment, publication, or
announcement.

## Try the backend-neutral project-memory contract

[Bob Project Memory](tasks/bob-project-memory/README.md) is an original,
standard-library contract over two fictional projects and an explicit
shared-lessons scope. It exercises recall, isolation, sanitized promotion,
supersession, evidence freshness, revision conflicts, interrupted-write
recovery, untrusted stored content, deletion, outage handling, and an honest
handoff. It does not install or qualify a real memory backend.

```sh
python3 scripts/evaluate.py prepare --task project-memory --output runs/memory-001
python3 scripts/evaluate.py baseline --task project-memory --workspace runs/memory-001 --result runs/memory-001-baseline.json
```

Use the [memory task prompt](tasks/bob-project-memory/AGENT_PROMPT.md) in the
prepared workspace. A correct candidate may change only `memory_adapter.py`
and `MEMORY_HANDOFF.md`; the helper runs the original seventeen trusted checks and
protects the contract and project evidence:

```sh
python3 scripts/evaluate.py candidate --task project-memory --workspace runs/memory-001 --result runs/memory-001-candidate.json
```

A pass is local contract evidence only. It is not evidence of native Bob
discovery, workflow-following, an MCP integration, durable multi-process
storage, backup erasure, or Engram/Basic Memory/Honcho behavior.

The first backend-specific record is the
[Engram Alpha v0.11.0 qualification gate](qualifications/engram-v0.11.0/README.md).
It pins reviewed source and release evidence, maps every contract behavior to a
candidate mechanism or gap, and provides a non-mutating disabled project-config
preview. It does not install or execute Engram and leaves runtime adoption
blocked pending the named cases.

## What the helper reports

`--result` writes a JSON report and refuses to overwrite an existing report.
Without that option the report is printed to standard output. Test reports
include observed test counts, failures, errors, skip counts, output, execution
time, environment details, and file fingerprints. Time measured by the helper
is **test-execution time**, not the agent's task duration.

The helper retains at most **256 KiB per diagnostic channel** for worker stdout,
worker stderr, and unittest text. The structured worker report has a separate
**512 KiB** read limit. Limits are measured on bytes before UTF-8 decoding. If a
limit is exceeded, the check exits `2` with status `resource_limit_exceeded`, a
channel name, the configured limit, the observed byte count when available, and
a bounded excerpt. `tests` remains `null`; truncated evidence can never become
`public_tests_passed`. Invalid UTF-8 in worker stdout/stderr is replaced in the
diagnostic excerpt rather than crashing the helper.

| Exit code | Meaning |
| --- | --- |
| `0` | Requested check succeeded: known faulty baseline confirmed, or candidate checks passed (including task-specific protected-input/state checks) |

| `0` | Requested check succeeded: known faulty baseline confirmed, or candidate checks passed (including task-specific preservation and scope checks) |
| `1` | Tests ran, but the requested baseline or candidate condition was not satisfied |
| `2` | Invalid arguments, file/output error, timeout, diagnostic/report limit, changed inputs during verification, or helper execution problem |

Each check has a 30-second timeout by default; override with a positive
`--timeout` value when needed. The helper executes local candidate Python code
as part of the test run. It is a cooperative local fixture helper, not a sandbox
or service for untrusted submissions. On a timeout or diagnostic-limit failure,
the helper terminates and reaps its direct worker. If a descendant keeps a
worker diagnostic pipe open, the helper returns an incomplete-capture error
rather than waiting for that descendant. It does not provide a general memory
quota or contain descendant processes. Before/after hashes describe the
recorded scope, not continuous monitoring of every possible input; see the
[protocol](docs/protocol.md).

## Reporting an evaluation

Follow [the protocol](docs/protocol.md). Record actual observations rather than
the agent's own success claim. Keep missing metrics as `null`; do not infer
token usage, cost, or model identity from elapsed time or marketing labels.

For an exploratory comparison, start every attempt from a fresh fixture and a
fresh conversation. Change one condition at a time, preserve the same task and
acceptance criteria, and report all attempts. A single successful run is useful
as an example, not as evidence of broad superiority.

The local software checks are recorded in [VALIDATION.md](VALIDATION.md). No participant run or aggregate benchmark score is included. Contributions
should keep that distinction visible. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Companion projects

These public companion repositories have separate responsibilities. Check each project's status and validation notes before relying on a feature.

- [bob-workflow-kit](https://github.com/Saqlain1999/bob-workflow-kit): portable rules and a focused Bob workflow skill.
- [bob-workflow-runner](https://github.com/Saqlain1999/bob-workflow-runner): Controller design preview; no executable runner.
- [awesome-bob-workflows](https://github.com/Saqlain1999/awesome-bob-workflows): Curated workflow references with source and review-status metadata.

## License

Original repository content is provided under the [MIT License](LICENSE).
The Tiny Ledger fixture was copied from the companion Workflow Kit's original
example; its intentionally faulty baseline is preserved here. IBM Bob and any
other named products remain the property of their respective owners.
