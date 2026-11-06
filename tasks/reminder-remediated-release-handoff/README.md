# Reminder remediated release handoff

This task closes the bounded public reminder journey after remediation and an
independent re-review. It preserves the exact repaired source, trusted tests,
accepted inputs, implementation evidence, current `REMEDIATION_REVIEW.md`, and
the earlier changes-required and release-blocked records. The participant may
change only `USER_GUIDE.md` and `RELEASE_READINESS_HANDOFF.md`.

The automatic checks cover the two repaired behavior boundaries, current-review
reconciliation, truthful unreleased documentation, acceptance and finding
disposition, exact validation, operational/rollback truthfulness, the precise
`ready for release review` decision, claim limits, preservation, and recovery.
Manual review still owns release judgment, evidence quality, audience clarity,
and whether the finite candidate warrants the bounded decision.

Run from the repository root:

```sh
python3 scripts/evaluate.py prepare --task reminder-remediated-release-handoff --output runs/release-ready-001
python3 scripts/evaluate.py baseline --task reminder-remediated-release-handoff --workspace runs/release-ready-001 --result runs/release-ready-001-baseline.json
# Use AGENT_PROMPT.md in the prepared workspace.
python3 scripts/evaluate.py candidate --task reminder-remediated-release-handoff --workspace runs/release-ready-001 --result runs/release-ready-001-candidate.json
```

A passing candidate is ready for human release review only. It does not
authorize a release, tag, artifact, deployment, publication, or announcement,
and does not prove general security, production readiness, compatibility,
performance, process-safe concurrency, or live Bob behavior.
