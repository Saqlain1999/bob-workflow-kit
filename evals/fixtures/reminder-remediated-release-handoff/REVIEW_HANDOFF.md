# Review handoff: reminder idempotency

## Reviewed state and decision

The current fixture independently reproduces two blocking defects. The author's historical 10/10 result is stale and is not current release evidence. Decision: **changes required**.

## Findings

- **REV-001 — High, confirmed:** `ReminderService.list_for` uses an inverted owner comparison and returns another owner's reminder. This is a reachable cross-owner data disclosure. AC-1 fails. Remediate with equality filtering and owner-isolation regression tests.
- **REV-002 — Medium, confirmed:** the idempotency-conflict exception formats the complete stored record, including message and reminder ID. This exposes stored reminder data across the error boundary. AC-2 fails. Remediate with a generic conflict and exception-text regression tests.

Both findings are unresolved and blocking. Process-safe concurrency remains untested. Product source and tests were not changed by this review. After remediation, rerun the exact trusted suite and perform a new independent review; do not carry this decision forward as current evidence.
