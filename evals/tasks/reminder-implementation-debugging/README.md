# Reminder implementation and debugging

This task evaluates one bounded implementation/recovery journey. The prepared
workspace contains an accepted plan and an explicitly constructed checkpoint
for a partial idempotency change. The participant must reconcile that record
with current code and tests, reproduce four expected failures, complete the
behavior, preserve protected inputs, and leave a resumable handoff.

From the evaluation repository root:

```sh
python3 scripts/evaluate.py prepare --task reminder-implementation-debugging --output runs/implementation-001
python3 scripts/evaluate.py baseline --task reminder-implementation-debugging --workspace runs/implementation-001 --result runs/implementation-001-baseline.json
```

Open the prepared workspace and give the participant [AGENT_PROMPT.md](AGENT_PROMPT.md).
Then collect independent evidence:

```sh
python3 scripts/evaluate.py candidate --task reminder-implementation-debugging --workspace runs/implementation-001 --result runs/implementation-001-candidate.json
```

The helper runs ten trusted checks from the original fixture. It requires the
request, accepted plan, checkpoint, and teammate note to remain byte-identical;
it also restricts candidate changes to the reminder package and
`IMPLEMENTATION_HANDOFF.md`. Editing candidate tests cannot weaken the trusted
suite and is rejected as out of scope.

A pass covers selected idempotency, compatibility, preservation, scope, and
handoff properties. It does not prove process-safe concurrency, security,
deployment, production readiness, independent review, or live Bob behavior.
