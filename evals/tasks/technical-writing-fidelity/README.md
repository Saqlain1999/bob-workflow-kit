# Technical Writing Fidelity

**Task ID:** `technical-writing-fidelity-v1`

This paired fixture evaluates one narrow specialist capability: restructuring a
dense operational note while preserving selected technical meaning. It is
designed to accompany the Workflow Kit's optional
`write-clear-technical-content` skill, but it can also be run without that skill
as a comparison condition. The fixture does not depend on the kit PR being
merged or installed.

## What it measures

- preservation of exact commands, paths, versions, values, and error IDs;
- preservation of `MUST`, `MUST NOT`, and `MAY` requirement strength;
- preservation of negation, retry conditions, and execution order;
- production of the required sections and numbered procedure; and
- manual reviewer judgment about scanability and unsupported additions.

It does not measure general documentation quality, arbitrary semantic
equivalence, technical correctness, large-codebase work, ASD-STE100 compliance,
or native Bob skill discovery/activation.

## Run it

```sh
python3 scripts/evaluate.py prepare --task technical-writing-fidelity --output runs/writing-001
python3 scripts/evaluate.py baseline --task technical-writing-fidelity --workspace runs/writing-001 --result runs/writing-001-baseline.json
```

The helper baseline succeeds after confirming eight checks with the two named
structure failures. Open the prepared workspace in a fresh participant
conversation and use [the prompt](AGENT_PROMPT.md). Then run:

```sh
python3 scripts/evaluate.py candidate --task technical-writing-fidelity --workspace runs/writing-001 --result runs/writing-001-candidate.json
```

Complete the [manual checklist](ACCEPTANCE.md) and inspect the diff. A helper
pass proves only that the candidate met this public bounded contract.
