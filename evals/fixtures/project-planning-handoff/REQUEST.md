# Change request

Add caller-supplied idempotency keys to `ReminderService.schedule`.

- A retry by the same owner with the same key and identical `message` and `due_at` must return the original reminder without appending another record.
- Reusing that owner/key pair with different content must raise `IdempotencyConflict`.
- The same key may be used independently by different owners.
- Retry behavior must survive creating a new service instance over the same store.
- Existing records without an idempotency key must remain readable.
- Keep the public `Reminder` fields compatible, use only the Python standard library, and do not migrate or rewrite the store during service startup.

Planning only: change `DELIVERY_PLAN.md`, not source, tests, or this request.
