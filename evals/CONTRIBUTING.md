# Contributing

This repository contains two small, public coding tasks. Contributions should
improve repeatability or add well-defined tasks, not imply benchmark coverage
that has not been measured.

## Improve the helper or documentation

Use Python 3.10+ and the standard library. Preserve the existing commands and
report semantics unless a change is explicitly documented. Add a meaningful
test for changed behaviour, then run from the repository root:

```sh
python -m unittest discover -s tests -v
```

Keep helper tests separate from fixture tests, which deliberately contain a
baseline failure or acquire known failures during preparation. Do not repair
the original fixtures as incidental cleanup. Tiny Ledger is the default task;
Parcel Resume uses the fixed `--task parcel-resume` selector.

Worker stdout, stderr, unittest diagnostics, and the structured worker report
have documented byte limits. A limit regression must remain an explicit exit-2
non-pass, preserve bounded evidence, drain both process pipes, and cover the
exact-limit boundary. A descendant that inherits a diagnostic write end must not
make the helper block while closing its buffered reader; exercise that condition
under an independent watchdog and clean up the probe explicitly. Do not replace
these limits with silent truncation.

For changes to Parcel Resume, verify that preparation executes its real
historical check, both expected current failures reproduce, protected policy
and note bytes survive, and new/changed runtime files affect the state check.
Keep constructed handoffs, helper checks and live participant observations
distinct. This helper is not an extensible task platform or process sandbox.

Explain the problem, the proposed change, and the observed checks. Avoid
unnecessary package dependencies, model SDKs, credentials, and network calls.

## Propose a task

A task contribution needs:

- A clearly licensed, self-contained starting fixture.
- A task identifier and observable acceptance criteria.
- A reproducible faulty or incomplete baseline.
- A prompt describing the problem without giving the patch.
- Checks that detect the target failure and a manual review checklist.
- A description of what the task does and does not measure.

Keep fixtures small enough to inspect. If a task requires services or special
hardware, state that before anyone begins. Do not claim a task represents
large-repository work merely because it generates many files.

## Submit a participant run

Use `results/result-template.json` and follow `docs/protocol.md`. Report the
condition, client/version information that is actually visible, the prompt,
fresh-start procedure, attempts, interventions, validation evidence, and
limitations. Include failed and abandoned attempts in comparisons.

Use `null` for unavailable measurements. Test time, agent wall time, token usage,
and cost are different measurements. Do not substitute one for another.

Share only material you are entitled to publish. Remove credentials, private
paths, organization data, and conversation content that is not part of the
public exercise. Record any redactions so reviewers understand the evidence
limits. A result report is a claim to review, not a trusted leaderboard entry.

## Licensing and attribution

Your original contribution is offered under this repository's MIT License.
Keep third-party notices intact and identify the source and license of any
copied material. Product names and links do not imply vendor endorsement.
