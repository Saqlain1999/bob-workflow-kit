# Reminder remediated re-review

This task re-enters independent review after the bounded remediation of REV-001
and REV-002. It protects the accepted inputs, exact repaired source and tests,
current implementation handoff, and earlier blocked gate records. The only
participant output is a new `REMEDIATION_REVIEW.md`.

The automatic checks cover the repaired behaviors, selected compatibility, the
new review structure, finding disposition, exact current evidence, decision
limits, preservation, and recovery. Manual review still owns independence,
reasoning quality, severity proportionality, new-finding quality, and whether
the evidence supports the bounded decision.

Run from the repository root:

```sh
python3 scripts/evaluate.py prepare --task reminder-remediated-review --output runs/rereview-001
python3 scripts/evaluate.py baseline --task reminder-remediated-review --workspace runs/rereview-001 --result runs/rereview-001-baseline.json
# Use AGENT_PROMPT.md in the prepared workspace.
python3 scripts/evaluate.py candidate --task reminder-remediated-review --workspace runs/rereview-001 --result runs/rereview-001-candidate.json
```

The prepared baseline already contains the repaired source; its expected
failures concern the absent fresh review record. A passing candidate is ready
for a separate release-preparation stage, not ready for release. It does not
prove general security, process-safe concurrency, production readiness,
compatibility, performance, or live Bob behavior.
