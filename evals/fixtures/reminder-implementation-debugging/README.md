# Reminder implementation and recovery fixture

This small standard-library project resumes an interrupted idempotency change.
The partial implementation accepts and stores a key, but it does not yet
recognize retries or conflicts. Read the protected request, accepted delivery
plan, constructed checkpoint, current source, trusted tests, and teammate note
before editing.

Implement the bounded change and create `IMPLEMENTATION_HANDOFF.md`. Do not
change the request, plan, checkpoint, teammate note, or trusted tests. The
public evaluator checks selected behavior, compatibility, scope, preservation,
and recovery evidence. It cannot prove production readiness or concurrency
safety.
