# Reminder independent review and security

This task is the review stage of the same small reminder project used by the
planning and implementation exercises. The prepared current source contains two
deliberate problems introduced after an author handoff: owner filtering is
inverted, and a conflict exception exposes stored record content.

The participant writes only `REVIEW_HANDOFF.md`. Trusted public checks confirm
the defects and inspect the report's evidence and decision contract. This
evaluates a narrow public journey: it does not measure general code-review
accuracy, penetration testing, compliance, production readiness, or live Bob
skill activation.

```sh
python3 scripts/evaluate.py prepare --task reminder-independent-review --output runs/review-001
python3 scripts/evaluate.py baseline --task reminder-independent-review --workspace runs/review-001 --result runs/review-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-independent-review --workspace runs/review-001 --result runs/review-001-candidate.json
```

Use [AGENT_PROMPT.md](AGENT_PROMPT.md) for the participant and complete
[ACCEPTANCE.md](ACCEPTANCE.md) after independent helper collection.
