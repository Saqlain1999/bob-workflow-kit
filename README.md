# Bob Workflow Evals

A small, reproducible evaluation starter for IBM Bob project workflows.

Four tasks offer first trials: repair a deliberately faulty Python ledger,
resume a parcel-pricing change from a constructed checkpoint, or restructure a
dense migration runbook while preserving a bounded technical contract, or turn
a reminder-service request and current source into a traceable, resumable delivery plan. Each has
a fixture, public tests, a participant prompt, a manual acceptance checklist,
and an offline helper that runs trusted tests against a disposable workspace.

**Status: evaluation starter. No live Bob evaluation or large-repository
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
| `scripts/evaluate.py` | Prepare a fresh workspace and collect local test evidence |
| `tests/` | Checks for the evaluation helper itself, separate from fixture tests |
| `docs/protocol.md` | How to run and report a manual evaluation |
| `results/result-template.json` | Structured record for an actual participant run |

The code fixtures use integer cents; every check uses Python's standard library.
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
