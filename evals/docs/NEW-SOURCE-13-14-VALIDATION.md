# New evaluator source #13/#14 — offline port verification

This source-layout branch starts at accepted `7a432e056295f314e45121839b1c5584225aded9`.
It merges exact public #13 `6d487eb118f79f313815a884e5b3af19d9bcd859`
then #14 `12cec9029682e14b57f9ace38605951fb091b605` without squash.
The public PR API and fetched pull refs matched those hashes and their stated
bases. Complete base-to-head diffs were reviewed before porting; no concrete
source blocker was found. No monorepo, accepted-source or correction worktree
was edited.

The consolidation later reconciled PR #14's final reviewed head
`083ed29533ca292fefa4784efac644f57de9735a` without replacing this historical
schema-v1 record. The final delta adds schema-v2 run/host/client identity,
requires explicit version/trust/live evidence for every executed IBM Bob result,
and rejects non-interactive `bob run` because it pre-approves tools. Its exact
source-focused protocol suite passed 13/13; fresh consolidated-tree execution is
recorded by the parent product rather than relabelled here.

## Executed checks

On Linux with Python 3.13.5, the ResourceWarning-fatal full suite passed twice:
155 discovered/executed, zero failures/errors/skips. The second execution used
an allowlisted environment with disposable HOME and temporary paths. This
includes ten new Basic Memory preview controls and twelve new protocol controls,
plus all 133 previously accepted tests. This is offline local software evidence,
not a sandbox or native Windows/macOS qualification.

Additional real CLI controls reproduced:

- Memory baseline: 17 checks with exactly 14 failures; expected baseline failure.
- Disposable repaired memory: 17 checks passed; public tests passed.
- Reminder implementation baseline: ten checks with exactly four failures.
- Disposable repaired reminder implementation: ten checks passed.
- Baseline and repaired internal-result attempts for both tasks: exit 2, no
  result created, candidate bytes unchanged (four independent attempts).
- Twelve extra validator rejection controls: unknown profile, wrong commit,
  unverified digest, missing authorization reference, integer safeguard,
  missing behavior, blank evidence, HTTP transport, missing process observation,
  unattempted cleanup, unqualified claim and production claim.

The template validates only as `not_run`. A constructed all-pass JSON control
can validate as `qualified`; this proves consistency of assertions, not real
permission, digest verification, observations, or backend qualification. A
reviewer must independently establish actual authority and evidence. The
validator neither authenticates references nor obtains execution authority.
Its JSON input is a cooperative local record, not an untrusted-input resource
sandbox or independent evidence attestation.

## Preservation

The production evaluator, raw-pipe `_run_bounded_process`, all fixtures and task
files, corrected 17/14 memory gate, deliberately faulty adapters, and existing
historical archives remain unchanged from the accepted source. The sole
existing test-file change is the exact reviewed #13 watchdog improvement:
remove inherited PYTHONWARNINGS only from the intentionally short-lived direct
worker that leaves a descendant alive, and allow one second for startup while
retaining the outer six-second watchdog and explicit descendant cleanup. The
full suite remains ResourceWarning-fatal; no production warning policy changed.

Validation conflicts were resolved without replacing old counts. Raw original
root-file snapshots, whose relative links retain their original context, are
archived as `.txt`:

- [Accepted 7a432e0](HISTORICAL-VALIDATION-accepted-7a432e0.txt)
- [Incoming #13](HISTORICAL-VALIDATION-pr13-6d487eb.txt)
- [Incoming #14](HISTORICAL-VALIDATION-pr14-12cec90.txt)

[Earlier combined-source evidence](COMBINED-SOURCE-VALIDATION.md) remains
historical evidence for its own source, not a rewritten fresh count.

## Limits

Basic Memory and Engram pins remain research/source records, not independently
qualified installed assets. The preview renders disabled project-only settings
without writing configuration or invoking uvx. No third-party download,
installation, Bob/model/MCP/backend/service execution, secret/private-data read,
push, post, publication, merge to main, release or archive action occurred.
The parent still owns assembled monorepo verification and any later draft-PR
authority. Prowl was unavailable; exact Git diffs, inventories and AST reads
provided bounded discovery instead.
