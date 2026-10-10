# Manual acceptance example

`tiny-ledger/` is a deliberately faulty, self-contained Python project for trying
the Bob Workflow Kit. Use Python 3.10 or later for the complete kit walkthrough and the standard
library. It has no packages to install, network calls, credentials, or services.

**The example's baseline test suite intentionally fails.** The repository's own
installer tests should be run separately; do not interpret this fixture failure
as an installer failure.

Use a disposable copy of `tiny-ledger/` as a Bob workspace. Follow its README,
then paste `tiny-ledger/PROMPT.md` into a fresh Agent conversation after installing
the kit. The prompt describes a user-visible defect without providing a patch.

The example demonstrates a real failing check and a subsequent behaviour fix.
It does not prove that a workflow can handle arbitrary large repositories or
that global instructions will always be followed. Review the diff and test
evidence yourself. A small task should receive a small, proportionate solution.
