# Contributing

This repository contains three small, public coding tasks. Contributions should
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
Parcel Resume uses `--task parcel-resume`, and Bob Project Memory uses
`--task project-memory`.

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

For Project Memory, preserve `contract.json`, both project evidence files, and
the trusted tests. Candidate scope is exactly `memory_adapter.py` and
`MEMORY_HANDOFF.md`. Keep hostile stored text inert, cross-project promotion
explicit and sanitized, stale/conflicting evidence non-current, and outage
fallback honest. The local control is not a production backend or live Bob
qualification.

For backend qualification records, pin an exact source commit, release event,
licence, and reviewed asset digest when one exists. Map every Project Memory
behavior to evidence, adapter work, or a named block. Preview helpers must be
non-mutating and must not install or execute a backend, edit global Bob settings,
grant automatic approval, capture transcripts, or turn missing runtime evidence
into a compatibility claim. Package-based records must also expose interpreter
and dependency requirements, avoid unversioned resolution, isolate backend
state, and keep licence obligations distinct from technical compatibility.

Runtime trial records must use the shared memory protocol, bind to one allowed
profile and exact digest, retain constructed public data and manual approvals,
and record process, file, network, model-download and cleanup observations.
Never turn a structurally valid `not_run`, `incomplete`, or `blocked` record into
a qualification claim. A runtime record does not establish production
readiness, and a live Bob claim additionally needs an observed client version
and explicit workspace trust.

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
