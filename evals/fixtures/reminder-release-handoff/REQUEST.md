# Accepted request

Review the completed reminder idempotency change independently before the next
release-handoff stage. Do not modify product source, tests, configuration, or
the accepted planning/implementation records during this review.

## Acceptance criteria

- **AC-1:** `list_for(owner)` returns only that owner's reminders; another
  owner's record is never returned.
- **AC-2:** reusing an owner/key pair with different content raises
  `IdempotencyConflict` without appending and without exposing stored reminder
  data in the exception text.
- **AC-3:** same-content retries still return the original reminder, including
  from a new service instance; unkeyed calls and legacy records remain compatible.
- **AC-4:** the review independently checks current state, preserves every
  product/input file, records precise blocking findings, and hands remediation
  back without claiming release or security approval.

Process-concurrent scheduling remains outside this bounded review. Record it as
a residual risk; do not present it as one of the seeded reproduced defects.
