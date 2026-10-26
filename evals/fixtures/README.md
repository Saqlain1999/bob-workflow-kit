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

Preserve both original fixtures. Their tests are public evidence for these small
tasks, not large-repository coverage or observed Bob performance.
