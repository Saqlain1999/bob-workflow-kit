# Participant prompt

Independently review the implemented reminder idempotency change in this
prepared workspace before its next release-handoff stage.

Read `README.md`, `REQUEST.md`, `DELIVERY_PLAN.md`,
`IMPLEMENTATION_HANDOFF.md`, `TEAM_NOTES.md`, the current source, and the trusted
tests. Reconcile the author's historical validation with current state. Run the
smallest trusted checks needed to reproduce or reject suspected issues.

Change **only** `REVIEW_HANDOFF.md`. Do not repair source, rewrite trusted tests,
or change any accepted input. Record precise findings with stable IDs,
classification, severity/confidence rationale, paths/symbols, triggers,
observed/expected behavior, consequences, evidence, remediation direction, and
blocking status. Map acceptance and preservation evidence, make one bounded
next-gate decision, and record stale evidence, unrun checks, residual risks,
stop/recovery conditions, and explicit claim limits.

Do not claim compliance, certification, production readiness, deployment
approval, absence of vulnerabilities, or live Bob behavior. The two deliberate
fixture defects are public test artifacts, not a real incident.
