# Reminder independent-review fixture

This is a deliberately flawed, local-only reminder service for
`reminder-independent-review-v1`. It continues the accepted reminder journey
after an implementation handoff. A later unreviewed change introduced two
observable problems in `notifier/service.py`; the author handoff therefore
describes stale evidence.

The participant may change only `REVIEW_HANDOFF.md`. The trusted checks confirm
that both seeded problems are present and then assess whether the review report
identifies them with reproducible evidence and a bounded remediation decision.
They do not ask the participant to fix the product.

No Bob output, production incident, private record, network service, credential,
scanner, or model call is included. The defects and all handoffs are constructed
public evaluation artifacts. The prepared copy has no revision history or
author diff; record that limit and review the complete current source instead.
