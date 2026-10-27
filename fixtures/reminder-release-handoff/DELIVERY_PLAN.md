# Accepted delivery plan

The reminder service stores the idempotency key with each append-only record.
Scheduling scans records for the owner/key pair, returns the original reminder
for identical content, and rejects different content. `list_for` must isolate
records by owner. Existing unkeyed and legacy-record behavior remains unchanged.

Validation originally covered retries, conflicts, owner scoping, legacy records,
invalid dates, public fields, and no rewrite on service construction. The
independent review must reconcile that historical claim with current source and
trusted fixture checks before making a decision.
