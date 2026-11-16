# Reminder idempotency candidate

## Availability

This change is unreleased and its release is blocked. Do not deploy or use this candidate with private reminder content.

## Intended behavior

- AC-1 intends `list_for(owner)` to return only that owner's records.
- AC-2 intends a repeated owner/key with different content to raise a generic conflict without exposing stored content.
- AC-3 covers retry persistence; AC-4 preserves accepted inputs and unrelated files.

These are requirements, not claims about corrected current behavior.

## Known blocking issues

- REV-001 is an unresolved High cross-owner data exposure: the current owner filter returns another owner's record.
- REV-002 is an unresolved Medium conflict-path exposure: exception text includes the stored reminder message and identifier.
- Decision: release blocked.

## Operator guidance

Do not use this unreleased candidate with private or production data. There is no safe upgrade and no rollback artifact because no release artifact exists. Keep the previous supported version or fixture state, remediate both findings, and complete a new independent review before release review.

## Evidence limits

The public fixture checks reproduce two seeded defects and validate a finite documentation contract. They do not prove corrected behavior, compatibility, performance, production readiness, or live Bob behavior.
