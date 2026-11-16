# Task: resume parcel pricing after the policy changes

**Task ID:** `parcel-resume-v1`

**Helper selector:** `--task parcel-resume`

**Prerequisite:** Python 3.10+; standard library only.

This is a small, inspectable exercise in using a checkpoint, rechecking current
files, and completing a change across two entry points. It is not a large-repo
benchmark or an actual recorded interruption of Bob. No live Bob run is
included or required to check the local evaluation helper.

## The prepared interruption

The fixture has a quote API, a CSV export, a shared JSON policy loader, and ten
public tests. During preparation the helper:

1. Copies the original fixture into a new disposable directory.
2. **Actually executes** the trusted suite against that copy and requires all
   ten tests to pass. It records the command, environment, test output and file
   fingerprints in `handoff/historical-check.json`.
3. Writes a clearly labelled constructed `CHECKPOINT.md` describing the
   unfinished policy-driven change and that historical passing check.
4. Changes the policy's free-delivery threshold from 5,000 to 7,500 cents and
   appends an unrelated teammate note to `TEAM_NOTES.md`.
5. Records the resulting state in `handoff/preparation.json`. Exactly those two
   files differ from the state of the historical check.

The prepared current state has **ten tests and two failures**, one in each
entry point. The old passing result is real, but does not describe the current
policy. The participant must finish the implementation while preserving both
the updated policy and the complete teammate note byte for byte.

## Run an attempt

Run these commands from this evaluation repository's root. Use a fresh run
directory and new result filenames for every attempt. The helper refuses to
overwrite existing workspaces or reports.

```sh
python3 scripts/evaluate.py prepare --task parcel-resume --output runs/parcel-001
python3 scripts/evaluate.py baseline --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-baseline.json
```

Preparation runs trusted fixture Python locally. If the historical check fails
or times out, preparation fails and removes its newly created disposable copy.
Expected baseline helper status is `expected_baseline_failure`, exit `0`: the
known pair of application failures was reproduced. This is not application
success. By default the worker timeout is 30 seconds; `--timeout` accepts a
finite positive number on prepare and check commands.

Open `runs/parcel-001` as the Bob workspace in a **fresh conversation** and paste
[AGENT_PROMPT.md](AGENT_PROMPT.md). Do not import a previous conversation or tell
the participant the exact patch. Keep the prepared handoff available. Record
the Bob client/version, visible mode, enabled rules/skills, permissions and
interventions. There is no verified client/version compatibility matrix or
live Bob qualification for this exercise yet.

After the participant finishes, return to this repository's root:

```sh
python3 scripts/evaluate.py candidate --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-candidate.json
```

The candidate result must be **outside** `runs/parcel-001`, as shown. Otherwise
writing the result itself would change the workspace whose state was checked.
Expected for a complete focused repair: ten passing tests, matching protected
inputs, stable before/after state fingerprints, status `public_tests_passed`
and exit `0`. The helper always leaves `manual_acceptance` and
`observed_bob_behavior` as `not_assessed`.

Complete [ACCEPTANCE.md](ACCEPTANCE.md), then copy the
[result template](../../results/result-template.json). Set its task ID to
`parcel-resume-v1` and prompt path to `tasks/parcel-resume/AGENT_PROMPT.md`.
Reference all three evidence files: historical check, baseline and candidate.
No Git repository is needed inside the workspace; retain the recorded file
fingerprints. A repository revision may be recorded separately if known.

## What counts as evidence

The helper runs the original public tests from the evaluation checkout against
the candidate. Removing tests in the candidate cannot remove those trusted
checks. A required test skipped, missing or failing prevents success. Candidate
tests added during repair need separate review and execution.

Policy and teammate-note hashes must match the deterministic prepared bytes.
Reverting the policy can make ordinary tests green while still failing this
preservation check. A new runtime file enters the workspace fingerprint; any
recorded file added, removed or changed between the pre-test and post-test
snapshots invalidates current-state evidence, even when all tests pass.

The snapshot covers regular files throughout the workspace except named
handoff artifacts (`CHECKPOINT.md`, `handoff/historical-check.json`,
`handoff/preparation.json`), `.git/` and `__pycache__/`. It rejects redirected
or nonregular paths within that scope. Handoff edits are reviewed manually.
Keep runtime/configuration inputs out of the excluded metadata directories.
Rerun verification after a later code/configuration change; a report remains
evidence about its recorded state, not a continuing promise.

This is a cooperative local fixture, not an adversarial evaluator or sandbox.
Candidate Python and the public tests share a worker runtime. Before/after
hashes cannot prove that no file was briefly changed and restored, or that
unrecorded external inputs were absent. The worker timeout is not descendant
process containment, and captured output is not size-bounded. Do not use this
helper for untrusted submissions or a long-running service.

## Questions the human review answers

Did the participant treat the checkpoint as a useful starting point, inspect
the current policy and notes, reproduce the new failure, preserve others' work,
and report fresh verification accurately? A passing candidate alone does not
establish any of these process observations. Record visible actions or mark
them unknown; do not infer that Bob noticed stale evidence just because the
final code passes.

For a comparison, declare the condition before starting, keep the same task,
prompt and acceptance criteria, use fresh copies and conversations, record
prior exposure, and include failed or abandoned attempts. This single exercise
cannot establish workflow superiority, long-session memory quality or reliable
large-project performance.
