# Reminder documentation and release handoff

This task is the documentation/release stage of the same small reminder project used by the planning, implementation, and independent-review exercises. The review has two unresolved blocking findings: inverted owner filtering and stored record content in a conflict exception.

The participant writes only `USER_GUIDE.md` and `RELEASE_HANDOFF.md`. Trusted public checks reproduce the defects and inspect whether the documentation preserves the blocked decision rather than converting a completed review into a false release claim. This evaluates a narrow public journey; it does not measure general release judgment, production readiness, compatibility, performance, deployment, or live Bob activation.

```sh
python3 scripts/evaluate.py prepare --task reminder-release-handoff --output runs/release-001
python3 scripts/evaluate.py baseline --task reminder-release-handoff --workspace runs/release-001 --result runs/release-001-baseline.json
python3 scripts/evaluate.py candidate --task reminder-release-handoff --workspace runs/release-001 --result runs/release-001-candidate.json
```

Use [AGENT_PROMPT.md](AGENT_PROMPT.md) for the participant and complete
[ACCEPTANCE.md](ACCEPTANCE.md) after independent helper collection.
