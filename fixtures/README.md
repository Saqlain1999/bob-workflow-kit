# Fixtures

`tiny-ledger/` is the original deliberately faulty Python example copied from
the companion `bob-workflow-kit` project. The files are kept unchanged so the
same starting task can be used across both projects.

The upstream source is
<https://github.com/Saqlain1999/bob-workflow-kit/tree/main/examples/tiny-ledger>.


Keep this original intact. Prepare a disposable copy with:

```sh
python scripts/evaluate.py prepare --output runs/ledger-001
```

The original fixture has nine tests and one intentional failure. Do not include
it in a blanket command that assumes every discovered test should pass. The
helper's `baseline` command checks that the known failure remains reproducible.

`parcel-resume/` is a second, original standard-library fixture for
[parcel-resume-v1](../tasks/parcel-resume/README.md). It starts with ten passing
tests despite an unfinished policy-driven change. Preparation actually records
that historical check, writes a constructed checkpoint, then changes the policy
and appends a teammate note. The resulting workspace has two known failures.
Use its helper rather than manually copying it:

```sh
python3 scripts/evaluate.py prepare --task parcel-resume --output runs/parcel-001
```

`technical-writing-fidelity/` is an original documentation fixture for
[technical-writing-fidelity-v1](../tasks/technical-writing-fidelity/README.md).
Its dense runbook already contains the bounded technical contract; two public
structure checks fail until it is safely reorganized. `contract.json` remains a
protected input.

```sh
python3 scripts/evaluate.py prepare --task technical-writing-fidelity --output runs/writing-001
```

`project-planning-handoff/` is an original requirements/architecture fixture
for [project-planning-handoff-v1](../tasks/project-planning-handoff/README.md).
It contains a small existing reminder project and an intentionally incomplete
`DELIVERY_PLAN.md`. The participant may change only that plan.

```sh
python3 scripts/evaluate.py prepare --task project-planning-handoff --output runs/planning-001
```

`reminder-implementation-debugging/` continues the reminder journey from an
interrupted partial implementation. `reminder-independent-review/` continues
from a later author handoff and deliberately seeds a cross-owner disclosure and
stored-data exception leak. The review participant may change only
`REVIEW_HANDOFF.md`. `reminder-release-handoff/` continues from that review
without repairing the defects. Its participant may change only `USER_GUIDE.md`
and `RELEASE_HANDOFF.md`, and the correct release decision remains blocked.

```sh
python3 scripts/evaluate.py prepare --task reminder-independent-review --output runs/review-001
python3 scripts/evaluate.py prepare --task reminder-release-handoff --output runs/release-001
```

Preserve all seven original fixtures. Their tests are public evidence for these
small tasks, not large-repository coverage or observed Bob performance.
