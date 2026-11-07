# Contributing

This repository contains eleven small, public coding, documentation, planning,
review, and release-handoff tasks. Contributions should improve repeatability
or add well-defined tasks, not imply benchmark coverage that has not been
measured.

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
Parcel Resume, Technical Writing Fidelity, Project Planning Handoff, Reminder
Implementation and Debugging, Reminder Independent Review, and Reminder
Release Handoff, Reminder Review Remediation, Reminder Remediated Re-review,
and Reminder Remediated Release Handoff use their documented fixed task
selectors.

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

For Technical Writing Fidelity, keep `contract.json` protected, reproduce only
the two named baseline structure failures, exercise modality, negation,
condition and order negative controls, and keep qualitative semantic review
manual. Do not convert a finite public contract into a semantic-equivalence or
controlled-language certification claim.

For Project Planning Handoff, keep the request and source evidence protected,
reproduce the seven named baseline failures, and allow only
`DELIVERY_PLAN.md` to change. Keep design quality and implementation
correctness as manual or future-work questions; a structured plan is not an
implemented feature.

For Reminder Implementation and Debugging, preserve the accepted request,
plan, checkpoint, and team note; reproduce the four named baseline failures;
and allow only the notifier package plus `IMPLEMENTATION_HANDOFF.md` to
change. Do not weaken trusted tests to obtain a pass.

For Reminder Independent Review, keep product source, tests, and prior handoffs
read-only; reproduce both seeded defects; and allow only
`REVIEW_HANDOFF.md` to change. A structured finding is not security,
compliance, production-readiness, or live Bob evidence.

For Reminder Release Handoff, preserve both unresolved findings and all product
inputs, allow only `USER_GUIDE.md` and `RELEASE_HANDOFF.md` to change, and
require the decision to remain `release blocked` while either finding is open.
Documentation completion does not authorize a tag, publication, deployment, or
announcement.

For Reminder Review Remediation, preserve the independent review, blocked
release handoff, user guide, accepted request and plan, team note, store, public
contract, and trusted tests. Allow only `notifier/service.py` and
`IMPLEMENTATION_HANDOFF.md` to change. Both findings must be repaired together,
and the handoff must require a fresh independent review; passing remediation
checks does not clear the historical release block.

For Reminder Remediated Re-review, preserve the exact repaired source, trusted
tests, accepted inputs, implementation handoff, and historical review and
release records. Allow only `REMEDIATION_REVIEW.md` to change. The new review
must dispose both findings with current code and behavioral evidence; `ready for
release preparation` is a handoff to a separate stage, not release approval.

For Reminder Remediated Release Handoff, preserve the exact repaired source,
trusted tests, accepted inputs, implementation evidence, current re-review,
and historical review/release records. Allow only `USER_GUIDE.md` and
`RELEASE_READINESS_HANDOFF.md` to change. The exact `ready for release review`
decision hands a finite candidate to human review; it is not release approval
and authorizes no tag, artifact, deployment, publication, or announcement.

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
into a compatibility claim.

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
