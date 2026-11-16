Please investigate and repair this Tiny Ledger project. A user reports that a
rejected transfer sometimes changes an account balance.

Read the README and applicable instructions, inspect the relevant code, and
establish the test baseline before changing behaviour. Keep the public API and
documented requirements intact. Make a focused fix and preserve the existing
regression tests; add a check only if it covers a meaningful missing case.

This is a small local exercise. Use the existing Python standard-library checks,
without package installation, network access, external services, or unrelated
redesign. If a workflow skill is available, use it proportionately.

Verify the result and inspect the final diff. Report the cause, what changed,
the exact test command and observed outcome, and any remaining uncertainty.
Do not call a test successful unless you actually ran it to completion.
