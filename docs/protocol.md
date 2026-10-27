# Manual evaluation protocol

## 1. Declare the condition

Record the task ID, repository revision if available, Python environment, Bob client and
version, active mode, and relevant configuration. If comparing a workflow with
an alternative, describe the difference precisely. Do not assume the model is
fixed or visible when the client routes requests automatically.

Python 3.10+ is the common prerequisite. The helper records its own file hash,
the actual interpreter/platform, trusted-test hashes and workspace fingerprints.
A candidate workspace need not be a Git repository. If no revision is recorded,
use those file fingerprints and do not imply that an unchanged HEAD establishes
the checked state.

The result template is a reporting aid, not a machine-enforced scorecard. Use
`null` for information you could not observe. Separate a model run's metrics
from the helper's local test metrics.

## 2. Start fresh

Use the helper to prepare a new workspace. Confirm the baseline before giving
the task to an agent. Keep the original fixture unchanged. Start a fresh
conversation and note any global or project rules that could affect the run.

Use the same task prompt and acceptance criteria for comparable attempts.
Repeated exposure can make the task easier; record run order and prior exposure
rather than claiming independence without evidence.

For `parcel-resume-v1`, use `prepare --task parcel-resume`. Its historical test
result is actually executed by preparation; its checkpoint is deliberately
constructed, not a transcript or output from Bob. The helper then changes the
policy and adds a teammate note, so the recorded historical pass is stale for
the prepared state. Preserve the historical report, preparation record and
current baseline. Do not describe this as an observed real interruption.

For `technical-writing-fidelity-v1`, use
`prepare --task technical-writing-fidelity`. Treat `contract.json` as a
protected evaluation input and change only `RUNBOOK.md`. The baseline's two
structure failures are deliberate; the remaining passing checks establish only
that the source contains the selected tokens and clauses.

For `project-planning-handoff-v1`, use
`prepare --task project-planning-handoff`. Treat the request, current source,
and project-test note as protected evidence; change only `DELIVERY_PLAN.md`.
The seven baseline failures show that the starting plan lacks the selected
evidence, acceptance, decision, traceability, risk, and recovery properties.

For `reminder-implementation-debugging-v1`, use
`prepare --task reminder-implementation-debugging`. The accepted request, plan,
constructed checkpoint, and teammate note are protected. The source is a
partial implementation: key storage exists, while retry matching and conflict
handling remain unfinished. The four baseline failures are deliberate. Change
only the notifier package and `IMPLEMENTATION_HANDOFF.md`; candidate test edits
are out of scope even though the helper always runs its trusted original suite.

## 3. Observe the participant

Let the participant work within the stated scope and native permissions.
Record the start and end times, interventions, retries, and whether work was
abandoned. Do not silently substitute an edited prompt or manually repaired
candidate and present it as an uninterrupted agent result.

Do not require a complex workflow for a small task. Evaluate whether the work
was proportionate and evidence-based, not whether it used every available tool.

## 4. Validate independently

Run the helper's `candidate` command from this evaluation repository against
the participant's workspace. It runs the trusted original public tests in a
separate local Python process. A subprocess provides execution separation, not
a security sandbox.

Inspect the diff, review any changed tests, and run relevant additional checks
separately. Complete the manual acceptance checklist. The helper's pass means
the public tests passed and the task's automatic conditions were satisfied; it
cannot establish all qualitative criteria. Parcel additionally requires exact
prepared policy/note bytes and unchanged recorded state during the test run.
Technical Writing Fidelity additionally requires an unchanged contract; its
manual review covers scanability, contradictions, and unsupported additions.
Project Planning Handoff additionally protects the request and current source;
its manual review covers evidence quality, proportional design, and whether the
handoff would actually support safe implementation and resumption.
Reminder Implementation and Debugging protects the accepted inputs and team
note; its manual review covers whether current evidence was actually gathered,
the checkpoint was reconciled, the diff remained minimal, and the handoff can
support independent review and safe resumption.

Preserve raw helper reports locally. Each report records file fingerprints and
test output. Keep the command, result, and relevant revision together so an
outdated pass cannot be mistaken for the state of a later candidate.

The state map includes new files throughout the workspace, except the named
handoff artifacts (`CHECKPOINT.md`, `handoff/historical-check.json`,
`handoff/preparation.json`), `.git/` and `__pycache__/`. Keep relevant runtime and
configuration inputs outside those excluded paths. Handoff edits are reviewed
manually. Before/after snapshots detect changes that persist between them;
they are not continuous monitoring and cannot establish the absence of a
temporary edit that was restored. Rerun verification after later edits.

The helper is for a cooperative local exercise. Candidate code and tests share
a worker runtime. Worker stdout, worker stderr, and unittest text each have a
256 KiB retained-byte limit; the structured worker report has a 512 KiB read
limit. Exhausting one produces `resource_limit_exceeded` with exit code `2`,
not a partial test pass. The helper terminates and reaps its direct worker after
a timeout or diagnostic-limit failure, but it does not impose a general memory
quota or contain descendant processes. It is not a sandbox, a generic runner,
or protection against candidates manipulating the evaluation process. Review
code before running it; do not submit untrusted code to a service built around
this helper.

For Parcel, separately review whether the participant used the checkpoint,
noticed or checked stale evidence, and preserved others' work. Code correctness
does not prove that those actions occurred. Mark behavior unknown without a
usable observation record; keep manual acceptance independent of helper status.

## 5. Report without overclaiming

Use `results/result-template.json` for each participant attempt. Link the
baseline/candidate reports and diff, and describe any redactions. Keep failed,
incomplete, and abandoned runs visible in a comparison.

Useful observations include the task outcome, actual agent wall time, manual
interventions, reported resource use if available, and scope of validation.
Do not convert test-execution time into agent duration or use a missing cost
measurement as zero cost.

This repository contains five tiny public fixtures. A successful example is
not a large-project benchmark. A controlled comparison would need enough tasks
and repeated runs, a declared protocol, comparable conditions, and analysis of
uncertainty before supporting general conclusions. No such study is included.
