# Delivery plan: reminder idempotency

## Accepted boundary

Implement AC-1 through AC-4 in the existing append-only reminder service.
Preserve public `Reminder` fields, old newline-delimited JSON records, no-key
behavior, user data, trusted tests, and unrelated files. Use only the Python
standard library. Do not add a migration or rewrite the store at startup.

## Current evidence and decision

- `notifier/service.py` currently appends every request.
- `notifier/store.py` reads and appends newline-delimited JSON records.
- `tests/test_idempotency.py` is the trusted regression command's source.
- Selected design: store an optional internal key on new records and match by
  owner/key/content before appending. Old records omit the internal field.
- The scan-and-append sequence is not process-safe; revisit only if concurrent
  multi-process scheduling becomes an accepted requirement.

## Implementation slices

1. Reproduce the interrupted baseline with
   `python3 -m unittest discover -s tests -v`.
2. Complete matching and conflict behavior in `notifier/service.py`, retaining
   compatible reads and public objects.
3. Rerun the focused suite, inspect the complete diff and preservation state,
   then write `IMPLEMENTATION_HANDOFF.md` with exact current evidence.

## Stop conditions

Stop before expanding the storage boundary, changing protected inputs,
weakening tests, adding a dependency, or claiming concurrent-process safety.
Reconcile the checkpoint with current source and tests before trusting it.
