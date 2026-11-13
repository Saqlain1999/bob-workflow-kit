# Exercises: one checkout, separate evidence

No companion download, extra installation, API key or live model is needed for the offline checks. Live Bob observation is a different acceptance step.

## Start small

Follow the [first-use guide](try-alpha.md) and the [Tiny Ledger exercise](../examples/README.md) in a disposable copy. Its original test failure is intentional; do not repair the packaged fixture.

## Try interruption recovery

The [Parcel Resume task](../evals/tasks/parcel-resume/README.md) and its helper are included under `evals/`. From the kit root, change to that directory before following the task's commands:

```sh
cd evals
python3 scripts/evaluate.py prepare --task parcel-resume --output runs/parcel-001
python3 scripts/evaluate.py baseline --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-baseline.json
```

Use a new run name for every attempt. Baseline exit 0 means the **expected application failures were reproduced**, not that the application works. Open the prepared disposable workspace in Bob only when ready to perform a separately observed live trial. After a repair, from the same `evals/` directory:

```sh
python3 scripts/evaluate.py candidate --task parcel-resume --workspace runs/parcel-001 --result runs/parcel-001-candidate.json
```

Keep result files outside the candidate workspace. The [task acceptance checklist](../evals/tasks/parcel-resume/ACCEPTANCE.md) separates public-test results from process observations. Return to the kit root with `cd ..` before using the root installer or quality commands.

For the kit-level live result, return to the kit root and prepare a new record
bound to the exact checkout. The command refuses to overwrite an existing path:

```sh
python3 tools/prepare_live_trial.py --output /path/to/result.json --task-id parcel-resume-v1 --scenario interruption_recovery
python3 tools/validate_live_trial.py /path/to/result.json
```

When using a source archive without Git history, pass the reviewed archive's
exact `--kit-commit` and `--archive-sha256` to the preparation command. Keep the
shipped [template](live-trial-template.json) unchanged and never guess either
identifier.

If the interactive attempt blocks or stops before the task is complete, do not
edit or replace the prepared record. Use the bounded blocked/incomplete recorder
described in [Troubleshooting](troubleshooting.md#record-a-blocked-or-incomplete-trial)
to create a separate result. It cannot claim task completion or observed
recovery; keep the helper reports and human observations separate.

For this prepared fixture, record `constructed_handoff` as the interruption
type. Preparation creates a stale checkpoint and changed current state; it does
not pretend that a real Bob process was interrupted. A completed recovery claim
requires observed evidence that the participant read the handoff, reconciled
current files, detected the stale historical pass, reran relevant checks,
updated the checkpoint, and preserved the teammate change. Keep helper reports
and visible Bob/process observations separate; passing tests alone do not
satisfy the recovery fields.

## Optional deeper exercises

The [release-readiness exercise](../evals/tasks/reminder-remediated-release-handoff/README.md) extends the reminder sequence through a bounded documentation/handoff check. A passing helper is not permission to release.

The [project-memory fixture](../evals/tasks/bob-project-memory/README.md) tests an intentionally faulty file-backed adapter and a written handoff. From `evals/`, its selector is `--task project-memory`. The corrected gate exercises separate writer/reader processes, actual save/replace failures and sequential stale-instance refusal. It does not prove Bob remembers tasks, qualify a real memory backend, guarantee power-loss safety or provide concurrent transactions.

[Engram qualification notes](../evals/qualifications/README.md) are optional research and a disabled text preview only. No extra memory service, download, API key or install is required to use the kit or run its offline checks.

## Check the repository, not a live model

From the kit root:

```sh
python3 tools/check_all.py
```

This executes the installer/consolidation and evaluator helper suites, catalogue validation, imported-source checks and local Markdown-link validation. It does not execute a live Bob task or treat the deliberately failing application fixtures as ordinary passing suites. Logs and `summary.json` go to a newly created temporary directory whose path is printed. Use `--log-dir NEW_DIRECTORY` to choose a new evidence directory; existing directories are refused.

The imported evaluator has documented cooperative-fixture limits, not an adversarial sandbox. Only use trusted public exercise code. Historical evidence in the imported tree remains attributed to its original repository and source revision.
