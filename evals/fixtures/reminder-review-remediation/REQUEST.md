# Accepted remediation request

Remediate the two blocking findings in the reviewed reminder idempotency
candidate. Preserve the independent review and blocked release records so a
new reviewer can distinguish historical evidence from the repaired candidate.

## Acceptance criteria

- **AC-1:** `list_for(owner)` returns only that owner's reminders; another
  owner's record is never returned.
- **AC-2:** reusing an owner/key pair with different content raises
  `IdempotencyConflict` without appending and without exposing stored reminder
  data in the exception text.
- **AC-3:** same-content retries still return the original reminder, including
  from a new service instance; unkeyed calls and legacy records remain compatible.
- **AC-4:** only the two reviewed source defects and implementation evidence are
  changed; the review and blocked release records remain intact, and a fresh
  independent review is required before release preparation resumes.

Process-concurrent scheduling remains outside this bounded remediation. Record
it as unrun; do not turn it into an unsupported security or readiness claim.
