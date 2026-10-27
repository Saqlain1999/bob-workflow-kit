# Reminder review remediation

This task returns the same small reminder project from an independent
`changes required` review and blocked release handoff to a bounded
implementation stage. The participant must remediate REV-001 and REV-002,
preserve the review/release evidence trail, and hand the exact repaired
candidate to a new independent review.

```sh
python3 scripts/evaluate.py prepare --task reminder-review-remediation --output runs/remediation-001
python3 scripts/evaluate.py baseline --task reminder-review-remediation --workspace runs/remediation-001 --result runs/remediation-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-review-remediation --workspace runs/remediation-001 --result runs/remediation-001-candidate.json
```

Only `notifier/service.py` and `IMPLEMENTATION_HANDOFF.md` may change. Passing
twelve trusted checks demonstrates the finite public remediation contract; it
does not clear the historical review, change the blocked release decision, or
establish security, production readiness, general implementation quality,
process-safe concurrency, compatibility, or live Bob behavior.

Use [AGENT_PROMPT.md](AGENT_PROMPT.md) for the participant and complete
[ACCEPTANCE.md](ACCEPTANCE.md) after independent helper collection.
