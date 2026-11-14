# Project Planning Handoff

**Task ID:** `project-planning-handoff-v1`

This paired fixture evaluates one requirements/architecture slice of a larger delivery journey. A participant must inspect a small existing reminder project and replace an intentionally incomplete plan without changing source or tests.

## What it measures

- repository observations tied to named evidence;
- observable, uniquely identified acceptance criteria;
- comparison and selection of a repository-fit design;
- traceability from criteria to files and validation;
- explicit risk, stop, rollback, stale-evidence, and resume guidance; and
- preservation of the planning-only file boundary.

It does not measure implementation quality, arbitrary architecture quality, security, scale, performance, large-repository behavior, or live Bob skill discovery/activation.

## Run it

```sh
python3 scripts/evaluate.py prepare --task project-planning-handoff --output runs/planning-001
python3 scripts/evaluate.py baseline --task project-planning-handoff --workspace runs/planning-001 --result runs/planning-001-baseline.json
```

The helper baseline succeeds after confirming ten checks with the seven named planning failures. Open the prepared workspace in a fresh participant conversation and use [the prompt](AGENT_PROMPT.md). Then run:

```sh
python3 scripts/evaluate.py candidate --task project-planning-handoff --workspace runs/planning-001 --result runs/planning-001-candidate.json
```

Complete the [manual checklist](ACCEPTANCE.md) and inspect the diff. A helper pass proves only that the candidate met this public bounded contract.
