Please investigate and repair this Tiny Ledger project. A user reports that a
rejected transfer sometimes changes an account balance.

Read the project README and applicable instructions, inspect the relevant code,
and establish the test baseline before changing behaviour. Keep the public API
and documented requirements intact. Make a focused fix and preserve the existing
regression tests; add a check only if it covers a meaningful missing case.

Use the installed Workflow Kit proportionately. This is a small, local exercise:
use the existing Python standard-library checks, with no package installation,
network access, external services, or unrelated redesign.

Verify the result and inspect the final diff. Report the cause, what changed,
the exact test command and observed outcome, and any remaining uncertainty.
Do not call a test successful unless you actually ran it to completion.
