# Task: rejected transfers preserve balances

**Task ID:** `tiny-ledger-atomicity-v1`

**Scope:** a small local bug fix, not a large-codebase benchmark.

## Starting state

Use a fresh copy of `fixtures/tiny-ledger/`. The public API and behavioural
contract are documented in the fixture's README. Its nine public tests have
exactly one intentional baseline failure.

The user-visible report is: a rejected transfer sometimes changes an account
balance. Give the participant [AGENT_PROMPT.md](AGENT_PROMPT.md), without adding
a suggested patch or pointing at the implementation statement to reorder.

## What the task observes

- Whether the participant locates the relevant behaviour and reproduces it.
- Whether the repair preserves the documented public contract.
- Whether the participant runs the real checks and describes their outcomes
  honestly.
- Whether the change remains proportionate to the small task.

The task does not measure broad repository navigation, multi-agent throughput,
long-running recovery, deployment, production safety, or provider/model quality
in general. It also does not isolate the causal effect of a workflow from the
model, client, user interventions, or repeated exposure to the task.

## Evidence

Collect baseline and candidate reports using the helper. It runs the original
public test suite against the candidate's `ledger.py`, rather than trusting
tests edited in the candidate workspace. Record any additional tests separately.

Complete [ACCEPTANCE.md](ACCEPTANCE.md). A test pass is one piece of evidence;
manual review still decides whether the contract, scope, and reporting criteria
were satisfied.

Use a new task identifier if you change the starting defect or acceptance
criteria. Do not silently merge results from different versions of the task.
