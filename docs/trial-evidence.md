# Tiny Ledger local trial evidence

Recorded 9 October 2026 (UTC), Python 3.12.14.

The repair was produced by a separate assistant reading the kit skill. These commands were then executed locally to record the baseline and repaired state. This is not a Bob runtime test or a large-repository benchmark. The shipped fixture remains unchanged. Absolute traceback paths are normalized to <fixture> for this public record.

## fixture_baseline

Command: `python3 -B -m unittest discover -s tests -v` from that fixture directory. Exit code: **1**.

```text
test_account_creation_rejects_invalid_opening_values (test_ledger.LedgerTests.test_account_creation_rejects_invalid_opening_values) ... ok
test_duplicate_account_preserves_its_balance (test_ledger.LedgerTests.test_duplicate_account_preserves_its_balance) ... ok
test_insufficient_funds_leave_balances_unchanged (test_ledger.LedgerTests.test_insufficient_funds_leave_balances_unchanged) ... ok
test_invalid_transfer_amounts_leave_balances_unchanged (test_ledger.LedgerTests.test_invalid_transfer_amounts_leave_balances_unchanged) ... ok
test_same_account_transfer_is_rejected (test_ledger.LedgerTests.test_same_account_transfer_is_rejected) ... ok
test_snapshot_does_not_expose_internal_balances (test_ledger.LedgerTests.test_snapshot_does_not_expose_internal_balances) ... ok
test_transfer_updates_both_accounts_and_conserves_total (test_ledger.LedgerTests.test_transfer_updates_both_accounts_and_conserves_total) ... ok
test_unknown_destination_leaves_balances_unchanged (test_ledger.LedgerTests.test_unknown_destination_leaves_balances_unchanged) ... FAIL
test_unknown_source_leaves_balances_unchanged (test_ledger.LedgerTests.test_unknown_source_leaves_balances_unchanged) ... ok

======================================================================
FAIL: test_unknown_destination_leaves_balances_unchanged (test_ledger.LedgerTests.test_unknown_destination_leaves_balances_unchanged)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<fixture>/tests/test_ledger.py", line 45, in test_unknown_destination_leaves_balances_unchanged
    self.assertEqual(self.ledger.snapshot(), before)
AssertionError: {'alice': 1075, 'bob': 500} != {'alice': 1250, 'bob': 500}
- {'alice': 1075, 'bob': 500}
?             --

+ {'alice': 1250, 'bob': 500}
?            ++


----------------------------------------------------------------------
Ran 9 tests in 0.001s

FAILED (failures=1)
```

## independent_assistant_trial

Command: `python3 -B -m unittest discover -s tests -v` from that fixture directory. Exit code: **0**.

```text
test_account_creation_rejects_invalid_opening_values (test_ledger.LedgerTests.test_account_creation_rejects_invalid_opening_values) ... ok
test_duplicate_account_preserves_its_balance (test_ledger.LedgerTests.test_duplicate_account_preserves_its_balance) ... ok
test_insufficient_funds_leave_balances_unchanged (test_ledger.LedgerTests.test_insufficient_funds_leave_balances_unchanged) ... ok
test_invalid_transfer_amounts_leave_balances_unchanged (test_ledger.LedgerTests.test_invalid_transfer_amounts_leave_balances_unchanged) ... ok
test_same_account_transfer_is_rejected (test_ledger.LedgerTests.test_same_account_transfer_is_rejected) ... ok
test_snapshot_does_not_expose_internal_balances (test_ledger.LedgerTests.test_snapshot_does_not_expose_internal_balances) ... ok
test_transfer_updates_both_accounts_and_conserves_total (test_ledger.LedgerTests.test_transfer_updates_both_accounts_and_conserves_total) ... ok
test_unknown_destination_leaves_balances_unchanged (test_ledger.LedgerTests.test_unknown_destination_leaves_balances_unchanged) ... ok
test_unknown_source_leaves_balances_unchanged (test_ledger.LedgerTests.test_unknown_source_leaves_balances_unchanged) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
```

## Observed change

Only `ledger.py` changed in the trial. Tests and documentation matched the original.

Zero-context diff:

```diff
--- baseline/ledger.py
+++ trial/ledger.py
@@ -42,0 +43 @@
+        destination_balance = self.balance(destination)
@@ -44 +44,0 @@
-        destination_balance = self.balance(destination)
```
