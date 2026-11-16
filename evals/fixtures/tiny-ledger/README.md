# Tiny Ledger

Tiny Ledger is an in-memory transfer exercise using integer cents. It is a
learning fixture, not a payment system. It runs with Python 3.8 or later using
only the standard library.

## Public behaviour

- Create uniquely named accounts with non-negative integer opening balances.
- Transfer a positive integer number of cents between different existing accounts.
- Reject invalid amounts, insufficient funds, and unknown accounts with
  `LedgerError`.
- A successful transfer conserves the total balance.
- A rejected operation leaves existing balances unchanged.
- `snapshot()` returns a copy rather than exposing the internal balance mapping.

## Run the checks

From this directory, use the command for your Python installation:

```sh
python -m unittest discover -s tests -v
```

On systems where the executable is named `python3`, substitute that name.

**Expected baseline: nine tests run, with exactly one failure.** The defect is
deliberately seeded so an agent has a real regression to investigate. The tests
are public; there are no hidden tests, external fixtures, or dependencies.

## Try it with Bob

1. Copy this entire directory to a disposable workspace.
2. Open that copy in Bob after installing the Workflow Kit.
3. Start a fresh Agent conversation and paste the contents of `PROMPT.md`.
4. Review the changes and rerun the command above independently.

Completion means the tests pass, the public behaviour remains intact, and the
diff contains a focused repair. Deleting or weakening a regression test does
not satisfy the exercise. No package installation, networking, deployment, or
large new architecture is needed.

The fixture is intentionally small. A useful agent should inspect the relevant
code, reproduce the defect, make a bounded repair, and report observed evidence.
It need not use subagents or create extensive planning documents.
