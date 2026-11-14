# Change request

Complete caller-supplied idempotency keys for `ReminderService.schedule`.

- AC-1: A retry by the same owner with the same key and identical `message` and
  `due_at` returns the original reminder without appending another record.
- AC-2: Reusing that owner/key pair with different content raises
  `IdempotencyConflict` and appends nothing.
- AC-3: The same key may be used independently by different owners, and retry
  behavior survives a new service instance over the same store.
- AC-4: Calls without a key retain append-per-call behavior; existing records
  without a key remain readable; public `Reminder` fields remain compatible.

Use only the Python standard library. Do not migrate or rewrite the store at
startup. Preserve trusted tests and `TEAM_NOTES.md`. Process-safe concurrency is
out of scope; report that limitation rather than claiming it is solved.
