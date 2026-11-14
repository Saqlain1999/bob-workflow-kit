# Task: rewrite the Orbit migration runbook without changing its contract

Rewrite `RUNBOOK.md` so an on-call engineer can scan and execute it safely.

Requirements:

- Preserve every command, path, version, value, error identifier, condition,
  negation, operation order, owner, and requirement strength.
- Use the exact normative keywords `MUST`, `MUST NOT`, and `MAY` where the
  source uses them.
- Add exactly these level-two sections in this order: `Purpose`,
  `Before you begin`, `Procedure`, and `Recovery and ownership`.
- Put the four commands into four numbered procedure steps in their existing
  execution order.
- Do not add new operational claims or invent missing technical details.
- Change only `RUNBOOK.md`. Do not change `contract.json` or tests.

Run the public tests and report the command and observed result. If a safe
rewrite would require guessing, stop and identify the unresolved ambiguity.
